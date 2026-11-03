import json
import subprocess
import sys
import tempfile
from pathlib import Path
from future.podomancy import PROFILE


def run():
    base=dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',
        orientation=dict(frame='subject',view='plantar',mirrored=False),selections=[
            dict(entry_id='sole_many_long_lines',side='left'),dict(entry_id='sole_short_crossed_lines',side='right'),
            dict(entry_id='foot_thin_lean_soft',side='both'),dict(region_id='sole',side='both'),dict(region_id='big_toe',side='left'),
            dict(entry_id='sole_thin_skin',region_id='whole_foot',side='right'),dict(entry_id='sole_thick_skin',side='left',certainty='uncertain')])
    example=dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='source_example',example_id='foot_broad_thick_long')
    for name,value in [('podomancy-reference-input.json',base),('podomancy-source-example-input.json',example)]:
        Path('data',name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            p.write_text(json.dumps(value),encoding='utf-8')
            r=subprocess.run([sys.executable,'-X','utf8','-m','future','podomancy-reference',str(p),'--format',fmt],capture_output=True,text=True,encoding='utf-8')
            assert (r.returncode!=0)==reject,(name,r.stderr)
            if not reject:
                if fmt=='json':
                    out=json.loads(r.stdout);assert out['technique_id']==12 and not out['inference_enabled'] and out['individual_assessment'] is None
                    if name=='manual JSON':assert [x['status'] for x in out['results']]==['resolved_reference']*3+['ambiguous','unsupported_reference','conflict','partial_reference']
                    if name=='dorsal conflict':assert out['results'][0]['status']=='view_conflict'
                    if name=='unknown side':assert out['results'][0]['status']=='partial_reference'
                else:assert 'No individualized' in r.stdout
            if output:Path('data',output).write_text(r.stdout,encoding='utf-8')
            cases.append(dict(case=name,passed=True))
        check('manual JSON',base,output='podomancy-reference.json')
        check('manual Markdown',base,'markdown',output='podomancy-reference.md')
        check('source JSON',example,output='podomancy-source-example.json')
        check('source Markdown',example,'markdown',output='podomancy-source-example.md')
        check('mirrored subject',base|dict(orientation=dict(frame='subject',view='plantar',mirrored=True)))
        check('dorsal conflict',base|dict(orientation=dict(frame='subject',view='dorsal',mirrored=False)))
        check('unknown side',base|dict(selections=[dict(entry_id='sole_thin_skin')]))
        check('wrong profile',base|dict(profile='Somogyi'),reject=True)
        check('personal inference',base|dict(task='personality'),reject=True)
        check('photograph',base|dict(image='foot.jpg'),reject=True)
        check('medical measurements',base|dict(measurements=dict(thickness=2)),reject=True)
        check('source override',example|dict(selections=base['selections']),reject=True)
    Path('data/podomancy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Podomancy CLI cases passed')


if __name__=='__main__':run()
