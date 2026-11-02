"""Source-scoped components connected to calculated placements, without invented synthesis."""
import json
from pathlib import Path

DATA=json.loads((Path(__file__).resolve().parents[1]/'knowledge/core_interpretations.json').read_text(encoding='utf-8'))

def reference(r):
    return {k:r[k] for k in ('id','version','tradition','text','url','author','locator','exceptions')}

def register_knowledge(registry):
    from .knowledge import Rule
    for s in DATA['sources']:registry.add_source(s)
    for r in DATA['records']:
        registry.add_rule(Rule(r['id'],r['version'],1,r['variation'],r['tradition'],r['source_id'],r['locator'],r['text'],
            'symbolic_component',{'kind':r['kind'],'key':r['key'],'exceptions':r['exceptions']},'proposed','traditional',[]))

def placements(c,registry):
    from .western import load_context
    register_knowledge(registry)
    records=load_context(registry,c['settings']['tradition'])
    rows=[]
    for body,p in c['planets'].items():
        parts=[reference(r) for r in records if (r['kind'] in ('planet','planet_symbol') and r['key']==body) or
            (r['kind']=='sign' and r['key']==p['sign']) or (r['kind']=='house' and r['key']==str(p['house']))]
        present={r['kind'] for r in records if any(r['id']==x['id'] for x in parts)}
        rows.append({'planet':body,'sign':p['sign'],'house':p['house'],
            'coverage':'compositional' if parts else 'unsupported','components':parts,
            'missing_components':[k for k,ok in [('planet meaning',bool(present & {'planet','planet_symbol'})),
                ('sign meaning','sign' in present),('house meaning','house' in present)] if not ok]})
    aspects=[]
    for a in c['aspects']:
        parts=[reference(r) for r in records if r['kind']=='aspect' and float(r['key'])==a['angle']]
        aspects.append(dict(bodies=a['bodies'],angle=a['angle'],orb=a['orb'],coverage='compositional' if parts else 'unsupported',
            components=parts,direct_pair_coverage='unsupported'))
    return {'tradition':c['settings']['tradition'],'placements':rows,'aspects':aspects,
        'scope':'Documented components, explicitly composed; no direct planet-sign-house or natal pair delineation implied.',
        'predictive_validity':'Not established by source review or numerical tests.'}

def progression_context(natal,planets,phase):
    if natal['settings']['tradition']!='modern psychological':
        return {'coverage':'unsupported','reason':'Modern progression symbolism is not transferred to the selected tradition.'}
    moon=planets['Moon'];house=moon['natal_house']
    parts=[reference(r) for r in DATA['records'] if (r['kind']=='phase' and r['key']==phase) or (r['kind']=='house' and r['key']==str(house))]
    return {'coverage':'compositional','progressed_moon_natal_house':house,'calculated_phase':phase,'components':parts,
        'method_source':{'url':'https://cafeastrology.com/secondaryprogressions.html','locator':'Significant secondary progressions items 2–3'},
        'limitation':'Phase and house context only; no direct progressed planet-pair or real-event prediction.'}

def return_context(c):
    if c['settings']['tradition']!='modern psychological' or c['settings']['houses']!='placidus':
        return {'coverage':'unsupported','reason':'This reading profile requires modern tropical nonprecessed Placidus; calculation remains available.'}
    rows=[]
    for body,p in c['planets'].items():
        rows.append({'planet':body,'return_house':p['house'],'coverage':'compositional',
            'house_components':[reference(r) for r in DATA['records'] if r['kind']=='house' and r['key']==str(p['house'])],
            'retrograde_reading':[reference(r) for r in DATA['records'] if r['kind']=='return_retrograde' and r['key']==body and p['retrograde']]})
    return {'coverage':'compositional','method':[reference(r) for r in DATA['records'] if r['kind']=='return_method'],
        'placements':rows,'limitation':'House topics compose separate modern components with Shea methodology. They are not direct Shea planet-house book readings.'}
