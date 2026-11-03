import json
from pathlib import Path
from future.iridology import PROFILE,reference


def run():
    f=json.loads(Path('tests/fixtures/iridology_source_examples.json').read_text(encoding='utf-8'))
    base=dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',diagram='frontispiece',view='source_plate_upright')
    cases=[]
    for eye,label,text,parent,placement in f['cases']:
        r=reference(base|dict(selections=[dict(eye=eye,label_id=label)]));t=r['selections'][0]['reference']
        assert [t['printed_label'],t['parent_label'],t['placement']]==[text,parent,placement]
        cases.append(dict(case=eye+'-'+label,expected=[text,parent,placement],actual=[t['printed_label'],t['parent_label'],t['placement']],passed=True))
    for eye,position in f['orientation_cases']:
        r=reference(base|dict(selections=[dict(eye=eye,label_id='stomach')]))
        assert r['selections'][0]['placement_on_plate']==position
        cases.append(dict(case=eye+'-orientation',expected=position,passed=True))
    for label,placement,page in f['chapter_cases']:
        t=reference(base|dict(selections=[dict(eye='right',label_id=label)]))['selections'][0]['reference']
        assert t['placement']==placement and 'p'+str(page) in t['locator']
        cases.append(dict(case='chapter-'+label,expected=placement,page=page,passed=True))
    for e in f['published_examples']:
        request={k:v for k,v in base.items() if k!='mode'}|dict(mode='source_example',example_id=e['id'])
        r=reference(request);assert [x['selection'] for x in r['selections']]==e['selections']
        for row in r['selections']:
            assert row['reference'] is not None
            cases.append(dict(case=e['id']+'-'+row['reference']['id'],passed=True))
    result=dict(profile=PROFILE,source_id=f['source_id'],method=f['method'],passed=len(cases),cases=cases,
        independent_numeric_geometry=False,diagnostic_validation=False,limitation='Independently transcribed labels from the same primary plate,not independent clinical evidence. No polar boundaries invented.')
    Path('data/iridology-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'original-source Iridology checks passed')


if __name__=='__main__':run()
