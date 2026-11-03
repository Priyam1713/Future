"""Public offline CLI checks and reproducible historical-reference reports."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from future.phrenology import PROFILE


def run():
    base=dict(schema_version=1,profile=PROFILE,task='historical_reference',schematic='frontis-frontal',
        selections=[dict(label_id='34'),dict(label_id='25'),dict(label_id='dagger'),dict(label_id='2'),
                    dict(candidates=['31','32']),dict(label_id='23',name='Size'),dict(label_id='36')])
    Path('data/phrenology-reference-input.json').write_text(json.dumps(base,indent=2)+'\n',encoding='utf-8')
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            p=subprocess.run([sys.executable,'-X','utf8','-m','future','phrenology-reference',str(path),'--format',fmt],capture_output=True,text=True,encoding='utf-8')
            assert (p.returncode!=0)==reject,(name,p.stderr)
            if not reject:
                if fmt=='json':
                    r=json.loads(p.stdout)
                    assert r['technique_id']==10 and not r['inference_enabled'] and r['individual_assessment'] is None
                    if name=='mixed reference':assert [x['status'] for x in r['results']]==['resolved']*4+['ambiguous','conflict','unknown_label']
                    if name=='region conflict':assert r['region_status']=='schematic_conflict'
                    if name=='posterior':assert r['results'][0]['entry']['location']
                else:assert 'Scientifically discredited' in p.stdout
            if output:Path('data',output).write_text(p.stdout,encoding='utf-8')
            cases.append(dict(case=name,passed=True))
        check('mixed reference',base,output='phrenology-reference.json')
        check('Markdown',base,'markdown',output='phrenology-reference.md')
        check('profile star',base|dict(schematic='frontis-profile',selections=[dict(label_id='star')]))
        check('posterior',base|dict(schematic='frontis-posterior',selections=[dict(label_id='3')]))
        check('alias',base|dict(selections=[dict(name='Weight')]))
        check('browse region',{k:v for k,v in base.items() if k!='selections'}|dict(region_id='frontal-central-column'))
        check('region conflict',base|dict(region_id='posterior-lower'))
        check('unknown name',base|dict(selections=[dict(name='new label')]))
        check('wrong edition',base|dict(profile='Combe'),reject=True)
        check('personal inference',base|dict(task='personality'),reject=True)
        check('head scan',base|dict(image='head.jpg'),reject=True)
        check('measurements',base|dict(measurements=dict(width=12)),reject=True)
    Path('data/phrenology-smoke.json').write_text(json.dumps(cases,indent=2)+'\n')
    print(len(cases),'Phrenology CLI cases passed')


if __name__=='__main__':run()
