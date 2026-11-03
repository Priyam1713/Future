import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.iridology import PROFILE


def run():
    base=dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',diagram='frontispiece',view='source_plate_upright',
        selections=[dict(eye='right',label_id='liver'),dict(eye='left',label_id='spleen'),dict(eye='left',label_id='heart'),
            dict(eye='right',label_id='stomach'),dict(eye='left',label_id='skin_area')])
    example={k:v for k,v in base.items() if k not in ('mode','selections')}|dict(mode='source_example',example_id='central-and-peripheral-fields')
    for name,value in [('iridology-reference-input.json',base),('iridology-source-example-input.json',example)]:
        Path('data',name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            p=subprocess.run([sys.executable,'-X','utf8','-m','future','iridology-reference',str(path),'--format',fmt],capture_output=True,text=True,encoding='utf-8')
            assert (p.returncode!=0)==reject,(name,p.stderr)
            if not reject:
                if fmt=='json':
                    r=json.loads(p.stdout);assert r['technique_id']==15 and not r['inference_enabled'] and r['medical_assessment'] is None
                    if name=='manual JSON':assert r['coverage']['resolved']==5
                    if name=='source JSON':assert r['coverage']['resolved']==3 and r['source_example'] is not None
                    if name=='conflict':assert r['selections'][0]['status']=='conflict'
                    if name=='coordinate hints':assert r['geometry']['status']=='unsupported' and r['selections'][0]['reference'] is None
                    if name=='wrong eye':assert r['selections'][0]['status']=='unsupported_label_for_eye'
                else:assert 'No personal iris analysis or medical assessment' in p.stdout
            if output:Path('data',output).write_text(p.stdout,encoding='utf-8')
            cases.append(dict(case=name,passed=True))
        check('manual JSON',base,output='iridology-reference.json')
        check('manual Markdown',base,'markdown',output='iridology-reference.md')
        check('source JSON',example,output='iridology-source-example.json')
        check('source Markdown',example,'markdown',output='iridology-source-example.md')
        check('unknown',base|dict(selections=[{}]))
        check('ambiguous',base|dict(selections=[dict(eye='right',label_id=['liver','kidney'])]))
        check('conflict',base|dict(selections=[dict(eye='left',region_id='right-liver')]))
        check('coordinate hints',base|dict(selections=[dict(eye='right',sector_id='12R',clock_position='5:00',radial_band='outer')]))
        check('wrong eye',base|dict(selections=[dict(eye='right',label_id='heart')]))
        check('wrong edition',base|dict(profile='Jensen'),reject=True)
        check('mirror view',base|dict(view='mirror'),reject=True)
        check('patient photo',base|dict(photo='patient.jpg'),reject=True)
        check('diagnosis',base|dict(task='diagnosis'),reject=True)
        check('source override',example|dict(selections=base['selections']),reject=True)
    Path('data/iridology-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Iridology CLI cases passed')


if __name__=='__main__':run()
