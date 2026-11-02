"""Source-specific symbolic context; no invented planet-pair predictions."""
import json
from pathlib import Path
from .knowledge import Rule

def load_context(registry,tradition):
    records=json.loads((Path(__file__).resolve().parents[1]/'knowledge/western_rules.json').read_text(encoding='utf-8'))
    records+=json.loads((Path(__file__).resolve().parents[1]/'knowledge/transit_rules.json').read_text(encoding='utf-8'))
    from .core_readings import DATA,register_knowledge
    register_knowledge(registry)
    records += [r for r in DATA['records'] if r['kind'] in ('house','planet_symbol')]
    selected=[]
    for r in records:
        if r['tradition']!=tradition or r['kind']=='methodology': continue
        if r['id'].startswith('core.'):
            selected.append(r)
            continue
        source_id='western-source:'+r['id']
        registry.add_source(dict(id=source_id,author=r['author'],edition=r['edition'],url=r['url'],
                                 ingestion='metadata_only',rights_note=r['rights']))
        # Source checking is not executable-rule validation. Symbolic records stay
        # proposed in the computational registry, with their distinct review state.
        parameters={'kind':r['kind'],'key':r['key']}
        if r['kind']=='transit':
            parameters.update(conditions=r.get('conditions',{}),transiting=r['transiting'],
                              natal_target=r['natal_target'],aspects=r['aspects'])
        registry.add_rule(Rule(r['id'],r['version'],1,'transits',tradition,source_id,r['locator'],r['text'],
                              'symbolic_context',parameters,'proposed','traditional',[]))
        selected.append(r)
    return selected

def natal_context(records,natal):
    results=[]
    for name,p in natal['planets'].items():
        for r in records:
            if r['kind']=='planet' and r['key']==name:
                dignities=[]
                if p['sign'] in r['domicile']: dignities.append('domicile')
                if p['sign']==r['exaltation']: dignities.append('exaltation')
                if p['sign']==r['fall']: dignities.append('fall')
                from .natal import SIGNS
                opposite=SIGNS[(SIGNS.index(p['sign'])+6)%12]
                if opposite in r['domicile']: dignities.append('detriment')
                results.append({'planet':name,'sign':p['sign'],'dignities':dignities,'rule_id':r['id'],
                                'source':r['url'],'locator':r['locator'],'meaning':r['text']})
            if r['kind']=='sign' and r['key']==p['sign']:
                results.append({'planet':name,'sign':p['sign'],'rule_id':r['id'],'meaning':r['text'],
                                'source':r['url'],'locator':r['locator']})
    return results

def interpreter(records,natal):
    def interpret(body,target,angle,context=None):
        matches=[]
        direct=[]
        house=natal['planets'].get(target,{}).get('house')
        for r in records:
            if r['kind']=='transit' and (r['transiting'],r['natal_target'])==(body,target) and angle in r['aspects']:
                if conditions_match(r.get('conditions',{}),context or {}):
                    direct.append({'rule_id':r['id'],'version':r['version'],'text':r['text'],'source':r['url'],
                                   'author':r['author'],'locator':r['locator'],'exceptions':r['exceptions'],
                                   'tradition':r['tradition'],'conditions':r.get('conditions',{}),'documentation_scope':r['documentation_scope']})
            if ((r['kind']=='aspect' and r['key']==str(angle)) or
                (r['kind'] in ('planet','planet_symbol') and r['key'] in (body,target)) or
                (r['kind']=='house' and r['key']==str(house))):
                matches.append({'rule_id':r['id'],'version':r['version'],'text':r['text'],
                                'source':r['url'],'author':r['author'],'locator':r['locator'],
                                'scope':r['kind'],'exceptions':r['exceptions']})
        return {'coverage':'documented' if direct else 'compositional' if matches else 'unsupported',
                'direct':direct,'components':matches,
                'missing_coverage':[] if direct else ['No direct planet-pair transit delineation for selected tradition and conditions.'],
                'predictive_validity':'unvalidated symbolic tradition'}
    return interpret

def conditions_match(conditions,context):
    """Missing context never satisfies a constrained rule. Unknown conditions fail."""
    allowed={'phase','retrograde','natal_house','dignity','rulership'}
    def matches(actual,expected):
        values=actual if isinstance(actual,list) else [actual]
        accepted=expected if isinstance(expected,list) else [expected]
        return any(v in accepted for v in values)
    return all(k in allowed and k in context and matches(context[k],v) for k,v in conditions.items())

def traditional_configuration_context(natal):
    """Explicit traditional rulership calculation layer, independent of reading school."""
    from .natal import SIGNS,placement
    all_records=json.loads((Path(__file__).resolve().parents[1]/'knowledge/western_rules.json').read_text(encoding='utf-8'))
    facts=[r for r in all_records if r['kind']=='planet']
    rulers={s:r for r in facts for s in r['domicile']}
    houses=[]; planets={}
    for number,cusp in enumerate(natal['house_cusps'],1):
        sign=placement(cusp)['sign']; r=rulers[sign]
        houses.append({'house':number,'cusp_sign':sign,'ruler':r['key'],'source':r['url'],'locator':r['locator']})
    for name,p in natal['planets'].items():
        r=next((r for r in facts if r['key']==name),None)
        if not r: continue
        ds=[]
        if p['sign'] in r['domicile']: ds.append('domicile')
        if SIGNS[(SIGNS.index(p['sign'])+6)%12] in r['domicile']: ds.append('detriment')
        if p['sign']==r['exaltation']:ds.append('exaltation')
        if p['sign']==r['fall']:ds.append('fall')
        planets[name]={'dignities':ds,'rules_houses':[h['house'] for h in houses if h['ruler']==name],
                       'source':r['url'],'locator':r['locator']}
    return {'configuration':'traditional sign rulerships and sign-level dignities; no cross-school interpretive claim',
            'house_rulers':houses,'planets':planets}
