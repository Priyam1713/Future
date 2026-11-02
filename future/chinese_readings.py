"""Source-scoped symbolic relationships, independent of astronomical solving."""
from copy import deepcopy
from pathlib import Path
import hashlib,json
from .chinese import ELEMENTS,PROFILES,CONVENTIONS,stem,rule_trace

ROOT=Path(__file__).resolve().parents[1]
CATALOG=json.loads((ROOT/'knowledge/chinese_components_v1.json').read_text(encoding='utf-8'))

def ten_god(day_stem,other_stem):
    if any(isinstance(i,bool) or not isinstance(i,int) or not 0<=i<10 for i in (day_stem,other_stem)):
        raise ValueError('Stem indices must be integers0–9')
    offset=(other_stem//2-day_stem//2)%5
    same=day_stem%2==other_stem%2
    table=CATALOG['relations'];prefix='same' if same else 'opposite'
    a,b=ELEMENTS[day_stem//2],ELEMENTS[other_stem//2]
    explanation=[f'{a} and {b} share an element',f'{a} generates {b}',f'{a} controls {b}',
        f'{b} controls {a}',f'{b} generates {a}'][offset]
    return {'name':table[prefix+'_polarity'][offset],'character':table[prefix+'_chinese'][offset],
        'family':table['families'][offset],'element_relation':table['phase_differences'][offset],
        'polarity_relation':'same' if same else 'opposite','source_id':table['source_id'],
        'locator':table['locator'],'rule_id':'chinese.ten-gods','coverage':'direct relationship definition',
        'reason':f"{explanation}; {'same' if same else 'opposite'} polarity."}

def enrich(natal):
    if natal.get('technique_id')!=3 or natal.get('profile') not in PROFILES:
        raise ValueError('Only named BaZi natal profiles supported; no cross-technique fallback')
    n=deepcopy(natal);dm=n['day_master']['index'];context={r['pillar']:r for r in CATALOG['pillar_components']}
    rows=[];hidden_count={e:0 for e in ELEMENTS};visible_gods={};hidden_gods={}
    for key,p in n['pillars'].items():
        god=ten_god(dm,p['stem']['index'])
        if key=='day':
            p['ten_god']={'name':'Day Master','character':'日主','coverage':'reference, not a counted Ten God'}
        else:
            p['ten_god']=god
            visible_gods[god['name']]=visible_gods.get(god['name'],0)+1
        hidden=[]
        for i in CATALOG['hidden_stems']['stems_by_branch'][p['branch']['index']]:
            g=ten_god(dm,i);s=stem(i);hidden_count[s['element']]+=1
            hidden_gods[g['name']]=hidden_gods.get(g['name'],0)+1
            hidden.append({'stem':s,'ten_god':g,'source_id':CATALOG['hidden_stems']['source_id'],
                'locator':CATALOG['hidden_stems']['locator'],'profile':CATALOG['hidden_stems']['profile']})
        p['hidden_stems']=hidden
        role='reference for relationships' if key=='day' else f"{god['name']} ({god['family']})"
        rows.append({'pillar':key,'pair':p['pair'],'coverage':'compositional',
            'text':f"{key.title()} {p['name']}: {p['stem']['name']} is the {role}. {context[key]['text']}",
            'reason':god['reason'] if key!='day' else 'Day stem defines the Day Master; branch components remain independently labeled.',
            'documented_topic':context[key],'relationship':p['ten_god'],
            'source_ids':list(dict.fromkeys([context[key]['source_id'],CATALOG['relations']['source_id']])),
            'limitations':'Combination of documented components; no direct delineation of this full chart or personal outcome.'})
    interactions=[]
    # Ordered relations among visible stems; no favorable/unfavorable judgement.
    for a,p in n['pillars'].items():
        for b,q in n['pillars'].items():
            if a==b:continue
            relation=ten_god(p['stem']['index'],q['stem']['index'])
            interactions.append({'from_pillar':a,'to_pillar':b,'from_element':p['stem']['element'],
                'to_element':q['stem']['element'],'relation':relation['element_relation'],
                'source_id':relation['source_id'],'locator':'5.1, printedp74; general generating/controlling cycle',
                'scope':'Symbolic element relation only, not a confirmed stem combination/transformation.'})
    image=next(r for r in CATALOG['day_master_components'] if r['stem_index']==dm)
    n['reading']={'day_master':deepcopy(image),'pillars':rows,'element_interactions':interactions,
        'summary':f"{n['day_master']['name']} {n['day_master']['polarity']} {n['day_master']['element']} is the chart reference. "+image['text'],
        'ten_god_occurrences':{'visible_excluding_day_master':visible_gods,'hidden_memberships':hidden_gods},
        'coverage':deepcopy(CATALOG['coverage']),
        'limitations':['Occurrences are not weights, strengths, useful gods or outcome probabilities.',
            'No literal personality diagnosis, event forecast, or classical doctrine of automatic good/bad fortune inferred.',
            'Classical imagery and modern relation tables are labeled components; incompatible seasonal-qi tables are not merged.']}
    n['elements']['hidden_stem_membership_counts']=hidden_count
    n['rule_trace']+=[rule_trace(r) for r in CONVENTIONS['rules'] if r['id'] in ('chinese.ten-gods','chinese.hidden-stems','chinese.pillar-context')]
    n['luck_pillars']={'status':'unsupported','blocker':CONVENTIONS['luck_pillars']['blocker'],
        'source_leads':CONVENTIONS['luck_pillars']['source_leads'],'scope':'No invented start age, timestamps or personal forecast.'}
    n['reproducibility']['components_sha256']=hashlib.sha256((ROOT/'knowledge/chinese_components_v1.json').read_bytes()).hexdigest()
    return n

def register_knowledge(registry):
    from .knowledge import Rule
    for component in CATALOG['day_master_components']+CATALOG['pillar_components']:
        registry.add_rule(Rule(component['id'],component['version'],3,'BaZi symbolic components',
            CATALOG['traditions']['classical'],component['source_id'],component['locator'],component['text'],
            'chinese_component',{'limitation':component['limitation'],'coverage':component['coverage']},
            'proposed','traditional',[]))

def markdown(n):
    from .chinese import markdown as base
    text=base(n)+'\n## Source-grounded symbolic context\n\n'
    image=n['reading']['day_master']
    text+=n['reading']['summary']+f" Source: [{image['source_id']}]({next(s['url'] for s in n['sources'] if s['id']==image['source_id'])}), {image['locator']}.\n\n"
    text+='| Pillar | Ten God / reference | Hidden stems and relationships |\n|---|---|---|\n'
    for key,p in n['pillars'].items():
        hidden='; '.join(h['stem']['name']+': '+h['ten_god']['name'] for h in p['hidden_stems'])
        text+=f"| {key} | {p['ten_god']['name']} | {hidden} |\n"
    text+='\n'
    for row in n['reading']['pillars']:
        text+=f"- **{row['pillar'].title()} — compositional:** {row['text']} {row['reason']}\n"
    text+='\nVisible stem element counts: '+str(n['elements']['visible_stem_counts'])+'. Counts do not establish strength or a favorable element.\n\n'
    text+='Relationships: [Andrew Tan](https://fengshuibazicentre.com/pdf/Module_2_BaZi_Destiny%5BF%5D.pdf), printedpp73–79. Hidden stems: [6tail reference table](https://github.com/6tail/lunar-python), corroborated by [Yap workshop](https://www.joeyyap.com/notes/smw/BZ_For_Smart_Money_Workshop.pdf), PDFp2. Complete rule/source traces are in JSON.\n\n'
    text+='Luck-pillar onset remains unsupported: '+n['luck_pillars']['blocker']+'\n\n'
    text+='Direct components and assembled readings are separately labeled. These symbolic interpretations do not establish real-world predictive accuracy.\n'
    return text
