"""Source-specific symbolic context; no invented planet-pair predictions."""
import json
from pathlib import Path
from .knowledge import Rule

def load_context(registry,tradition):
    records=json.loads((Path(__file__).resolve().parents[1]/'knowledge/western_rules.json').read_text(encoding='utf-8'))
    selected=[]
    for r in records:
        if r['tradition']!=tradition or r['kind']=='methodology': continue
        source_id='western-source:'+r['id']
        registry.add_source(dict(id=source_id,author=r['author'],edition=r['edition'],url=r['url'],
                                 ingestion='metadata_only',rights_note=r['rights']))
        # Source checking is not executable-rule validation. Symbolic records stay
        # proposed in the computational registry, with their distinct review state.
        registry.add_rule(Rule(r['id'],r['version'],1,'transits',tradition,source_id,r['locator'],r['text'],
                              'symbolic_context',{'kind':r['kind'],'key':r['key']},'proposed','traditional',[]))
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
    def interpret(body,target,angle):
        matches=[]
        house=natal['planets'].get(target,{}).get('house')
        for r in records:
            if ((r['kind']=='aspect' and r['key']==str(angle)) or
                (r['kind']=='planet' and r['key'] in (body,target)) or
                (r['kind']=='house' and r['key']==str(house))):
                matches.append({'rule_id':r['id'],'version':r['version'],'text':r['text'],
                                'source':r['url'],'author':r['author'],'locator':r['locator'],
                                'scope':r['kind'],'exceptions':r['exceptions']})
        return {'coverage':'component symbolism only; planet-pair-specific delineation pending',
                'components':matches,'predictive_validity':'unvalidated symbolic tradition'}
    return interpret
