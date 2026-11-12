"""Deterministic, engine-specific personal-input builders."""
from future import face_reading, phrenology, moleosophy, podomancy, graphology, aura, iridology, oracle, iching, runes, pendulum
import secrets

def select(key,label,choices,default='unknown'):
    return dict(key=key,label=label,type='select',choices=choices,default=default)

def text(key,label,required=True):
    return dict(key=key,label=label,type='text',default='',required=required)

def contract(technique):
    if technique==20:
        signals=[v for v in pendulum.DATA['calibration']['mappable_signals'] if v!='irregular']
        return dict(title='Record your pendulum observation',description='Declare your yes/no calibration, then record the movement and its quality. Unclear observations remain unresolved.',fields=[text('question','Your question'),select('yes','Movement calibrated as yes',signals,''),select('no','Movement calibrated as no',signals,''),select('signal','Observed movement',list(pendulum.DATA['signals']),''),select('quality','Observation quality',list(pendulum.DATA['observations']['quality']),'')])
    if technique==19:
        return dict(title='Ask your rune-casting question',description='Choose one or three runes. The draw records a fresh seed and returns source-layered symbolic references.',fields=[text('question','Your question'),select('spread','Rune spread',list(runes.SPREADS),'three')])
    if technique==18:
        return dict(title='Enter your I Ching question and lines',description='Record six line values from the bottom upward: 6 old yin, 7 young yang, 8 young yin, 9 old yang.',fields=[text('question','Your question'),*[select('line'+str(i),'Line '+str(i)+(' (bottom)' if i==1 else ' (top)' if i==6 else ''),['6','7','8','9'],'') for i in range(1,7)]])
    if technique==17:
        return dict(title='Ask your oracle-card question',description='Choose a spread. A fresh recorded random seed produces a replayable draw and the source-supported symbolic reading.',fields=[text('question','Your question'),select('spread','Spread',list(oracle.SPREADS),'three')])
    if technique==15:
        return dict(title='Inspect a historical iris-chart label',description='Select a label from the upright source plate. Results describe the historical chart and its documented limitations.',fields=[select('entry','Eye and printed label',list(iridology.DATA['entries']),''),select('certainty','Selection certainty',['selected','uncertain','unknown'])],labels={'entry':{k:v['eye']+' eye: '+v['printed_label'] for k,v in iridology.DATA['entries'].items()}})
    if technique==14:
        return dict(title='Select your symbolic colors and context',description='Enter your own symbolic selection to retrieve the documented color meaning and context.',fields=[select('color','Color',list(aura.DATA['terms']),''),select('context','Symbolic context',list(aura.DATA['contexts']),''),select('certainty','Selection certainty',['selected','uncertain','unknown'])])
    if technique==13:
        return dict(title='Describe your handwriting observations',description='Select visible writing features. Unknown features remain unresolved. The engine returns descriptive terminology and historical sources.',fields=[select('direction','Writing direction',['ltr','rtl','unknown']),*[select(k,k.replace('_',' ').capitalize(),[t for t,v in graphology.DATA['terms'].items() if k in v['features']]+['unknown']) for k in graphology.FEATURES]])
    if technique==12:
        return dict(title='Choose a documented foot or sole feature',description='The selected source feature, orientation and certainty produce a documentary reference with any conflicts retained.',fields=[select('entry','Source feature',list(podomancy.DATA['entries']),''),select('side','Foot side',['left','right','both','unknown']),select('view','View',['dorsal','plantar','unknown']),select('certainty','Selection certainty',['certain','uncertain','unknown'])])
    if technique==11:
        return dict(title='Choose a historical body-region reference',description='Select a documented region and side to retrieve the source passage and its limits.',fields=[select('region','Body region',sorted({e['region_id'] for e in moleosophy.DATA['entries'].values()}),''),select('side','Subject-relative side',['left','right','midline','unknown']),select('view','View',['frontal','posterior','unknown'])])
    if technique==10:
        return dict(title='Inspect a historical schematic label',description='Choose a printed view and label from the source. The output explains the historical label and its documented location.',fields=[select('schematic','Printed schematic',list(phrenology.DATA['schematics']),''),select('label','Printed label',list(phrenology.DATA['entries']), '')],labels={'label':{k:k+' - '+v['original_name'] for k,v in phrenology.DATA['entries'].items()}})
    if technique!=9:return None
    f=face_reading
    return dict(title='Describe the region you want to inspect',description='Record visible features and inspect the historical source associated with that region. The result contains annotations and source references.',fields=[
        select('region','Face region',list(f.DATA['regions']),''),
        select('view','View',['frontal','left_profile','right_profile','unknown']),
        select('frame','Side labels refer to',['subject','viewer'],'subject'),
        select('mirrored','Is the view mirrored?',['unknown','yes','no']),
        select('side','Region side',['unknown','left','right','both','midline']),
        select('visibility','Visibility',['unknown','visible','occluded']),
        *[select(k,k.replace('_',' ').capitalize(),choices+['unknown','uncertain']) for k,choices in f.GEOMETRY.items()],
        select('marking','Visible marking',['unknown','none','line','spot','crease'])])

def build(technique,answers):
    if technique not in [9,10,11,12,13,14,15,17,18,19,20]:raise ValueError('Dedicated builder is not implemented for this technique')
    if not isinstance(answers,dict):raise ValueError('Input answers must be an object')
    spec=contract(technique);a={}
    for field in spec['fields']:
        value=answers.get(field['key'],field['default'])
        if field['type']=='select' and value not in field['choices']:raise ValueError('Choose '+field['label'])
        if field['type']=='text' and (not isinstance(value,str) or len(value)>10000 or (field.get('required') and not value.strip())):raise ValueError('Enter '+field['label'])
        a[field['key']]=value
    if technique==20:
        native=dict(schema_version=1,profile=pendulum.PROFILE,task='symbolic_response',mode='manual',question=a['question'],calibration=[dict(signal=a['yes'],response='yes'),dict(signal=a['no'],response='no')],observations=[dict(signal=a['signal'],quality=a['quality'])])
        pendulum.validate(native)
        return dict(technique_id=20,operation='pendulum',input=native)
    if technique==19:
        native=dict(schema_version=1,profile=runes.PROFILE,task='symbolic_reading',mode='seeded',spread=a['spread'],question=a['question'],seed=secrets.token_hex(16),protocol=runes.PROTOCOL,orientation_policy='upright_only')
        runes.validate(native)
        return dict(technique_id=19,operation='runes',input=native)
    if technique==18:
        native=dict(schema_version=1,profile=iching.PROFILE,reading_policy=iching.POLICY,task='symbolic_reading',mode='manual',method='manual',line_order='bottom_to_top',lines=[int(a['line'+str(i)]) for i in range(1,7)],question=a['question'])
        iching.validate(native)
        return dict(technique_id=18,operation='iching',input=native)
    if technique==17:
        native=dict(schema_version=1,profile=oracle.PROFILE,task='symbolic_reading',mode='seeded',spread=a['spread'],question=a['question'],seed=secrets.token_hex(16),protocol=oracle.PROTOCOL,orientation_policy='upright_only')
        oracle.validate(native)
        return dict(technique_id=17,operation='oracle',input=native)
    if technique==15:
        entry=iridology.DATA['entries'][a['entry']]
        native=dict(schema_version=1,profile=iridology.PROFILE,task='historical_reference',mode='manual',diagram='frontispiece',view='source_plate_upright',selections=[dict(eye=entry['eye'],label_id=entry['label_id'],certainty=a['certainty'])])
        iridology.validate(native)
        return dict(technique_id=15,operation='iridology-reference',input=native)
    if technique==14:
        native=dict(schema_version=1,profile=aura.PROFILE,task='symbolic_reference',mode='manual',components=[dict(color=a['color'],context=a['context'],certainty=a['certainty'])])
        aura.validate(native)
        return dict(technique_id=14,operation='aura-reference',input=native)
    if technique==13:
        native=dict(schema_version=1,profile=graphology.PROFILE,task='historical_reference',mode='manual',script='latin',writing_direction=a['direction'],observations=[dict(feature=k,category=a[k],scope='whole_sample',certainty='unknown' if a[k]=='unknown' else 'certain') for k in graphology.FEATURES])
        graphology.validate(native)
        return dict(technique_id=13,operation='graphology-reference',input=native)
    if technique==12:
        native=dict(schema_version=1,profile=podomancy.PROFILE,task='historical_reference',mode='manual',orientation=dict(frame='subject',view=a['view'],mirrored=False),selections=[dict(entry_id=a['entry'],side=a['side'],certainty=a['certainty'])])
        podomancy.validate(native)
        return dict(technique_id=12,operation='podomancy-reference',input=native)
    if technique==11:
        native=dict(schema_version=1,profile=moleosophy.PROFILE,task='historical_reference',mode='manual',orientation=dict(frame='subject',view=a['view'],mirrored=False),selections=[dict(region_id=a['region'],side=a['side'])])
        moleosophy.validate(native)
        return dict(technique_id=11,operation='moleosophy-reference',input=native)
    if technique==10:
        native=dict(schema_version=1,profile=phrenology.PROFILE,task='historical_reference',schematic=a['schematic'],selections=[dict(label_id=a['label'])])
        phrenology.validate(native)
        return dict(technique_id=10,operation='phrenology-reference',input=native)
    native=dict(schema_version=1,profile=face_reading.PROFILE,task='historical_reference',mode='manual',orientation=dict(view=a['view'],side_frame=a['frame'],mirrored={'yes':True,'no':False}.get(a['mirrored'],'unknown')),observations=[dict(region_id=a['region'],side=a['side'],visibility=a['visibility'],geometry={k:a[k] for k in face_reading.GEOMETRY},markings=[a['marking']])])
    face_reading.validate(native)
    return dict(technique_id=9,operation='face-reference',input=native)
