"""Deterministic, engine-specific personal-input builders."""
from future import face_reading, phrenology

def select(key,label,choices,default='unknown'):
    return dict(key=key,label=label,type='select',choices=choices,default=default)

def contract(technique):
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
    if technique not in [9,10]:raise ValueError('Dedicated builder is not implemented for this technique')
    if not isinstance(answers,dict):raise ValueError('Input answers must be an object')
    spec=contract(technique);a={}
    for field in spec['fields']:
        value=answers.get(field['key'],field['default'])
        if value not in field['choices']:raise ValueError('Choose '+field['label'])
        a[field['key']]=value
    if technique==10:
        native=dict(schema_version=1,profile=phrenology.PROFILE,task='historical_reference',schematic=a['schematic'],selections=[dict(label_id=a['label'])])
        phrenology.validate(native)
        return dict(technique_id=10,operation='phrenology-reference',input=native)
    native=dict(schema_version=1,profile=face_reading.PROFILE,task='historical_reference',mode='manual',orientation=dict(view=a['view'],side_frame=a['frame'],mirrored={'yes':True,'no':False}.get(a['mirrored'],'unknown')),observations=[dict(region_id=a['region'],side=a['side'],visibility=a['visibility'],geometry={k:a[k] for k in face_reading.GEOMETRY},markings=[a['marking']])])
    face_reading.validate(native)
    return dict(technique_id=9,operation='face-reference',input=native)
