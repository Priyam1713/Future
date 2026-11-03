"""Public CLI checks and reproducible historical examples; never real skin input."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from future.moleosophy import PROFILE,DATA


def run():
    base=dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',schematic_id=DATA['schematic']['id'],
        orientation=dict(frame='subject',view='frontal',mirrored=False),selections=[
            dict(region_id='eyebrow',side='right'),dict(region_id='eyebrow',side='left'),dict(entry_id='ear_general'),
            dict(region_id='ear',side='right',location_id='lower_tip'),dict(region_id='hand',location_id='excluding_fingers'),
            dict(region_id='mouth'),dict(region_id='forehead',side='unknown'),dict(region_id='unverified_region'),
            dict(entry_id='eyebrow_left',region_id='eyebrow',side='right')])
    example=dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='source_example',
        schematic_id=DATA['schematic']['id'],example_id='original-right-eyebrow')
    for name,v in [('moleosophy-reference-input.json',base),('moleosophy-source-example-input.json',example)]:
        Path('data',name).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            p.write_text(json.dumps(value),encoding='utf-8')
            result=subprocess.run([sys.executable,'-X','utf8','-m','future','moleosophy-reference',str(p),'--format',fmt],capture_output=True,text=True,encoding='utf-8')
            assert (result.returncode!=0)==reject,(name,result.stderr)
            if not reject:
                if fmt=='json':
                    r=json.loads(result.stdout);assert r['technique_id']==11 and not r['inference_enabled'] and r['individual_assessment'] is None
                    if name=='manual JSON':assert [x['status'] for x in r['results']]==['resolved']*6+['ambiguous','unsupported_reference','conflict']
                    if name=='source JSON':assert r['results'][0]['entry']['id']=='eyebrow_right'
                    if name=='mirrored':assert r['results'][0]['entry']['id']=='eyebrow_left'
                    if name=='unknown mirroring':assert r['results'][0]['status']=='orientation_unresolved'
                else:assert 'No individual assessment' in result.stdout
            if output:Path('data',output).write_text(result.stdout,encoding='utf-8')
            cases.append(dict(case=name,passed=True))
        check('manual JSON',base,output='moleosophy-reference.json')
        check('manual Markdown',base,'markdown',output='moleosophy-reference.md')
        check('source JSON',example,output='moleosophy-source-example.json')
        check('source Markdown',example,'markdown',output='moleosophy-source-example.md')
        for name,mirror in [('mirrored',True),('unknown mirroring','unknown')]:
            check(name,base|dict(selections=[dict(region_id='eyebrow',side='left')],orientation=dict(frame='viewer',view='frontal',mirrored=mirror)))
        check('unknown entry',base|dict(selections=[dict(entry_id='unknown')]))
        check('wrong profile',base|dict(profile='Yap'),reject=True)
        check('medical inference',base|dict(task='diagnosis'),reject=True)
        check('personal image',base|dict(image='skin.jpg'),reject=True)
        check('measurements',base|dict(measurements=dict(diameter=5)),reject=True)
        check('source override',example|dict(selections=base['selections']),reject=True)
    Path('data/moleosophy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Moleosophy CLI cases passed')


if __name__=='__main__':run()
