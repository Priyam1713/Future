import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.aura import PROFILE


def run():
    base=dict(schema_version=1,profile=PROFILE,task='symbolic_reference',mode='manual',
        components=[dict(color='pale_rose',context='thought_form'),dict(color='primrose',context='mental_body'),dict(color='violet')],
        subjective_description='A palette selected for a fictional scene;not a detected field.')
    example=dict(schema_version=1,profile=PROFILE,task='symbolic_reference',mode='source_example',example_id='figure-12')
    for name,value in [('aura-reference-input.json',base),('aura-source-example-input.json',example)]:
        Path('data',name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            p=subprocess.run([sys.executable,'-X','utf8','-m','future','aura-reference',str(path),'--format',fmt],capture_output=True,text=True,encoding='utf-8')
            assert (p.returncode!=0)==reject,(name,p.stderr)
            if not reject:
                if fmt=='json':
                    r=json.loads(p.stdout);assert r['technique_id']==14 and not r['inference_enabled'] and r['individual_assessment'] is None and not r['physical_aura_detected']
                    if name=='manual JSON':assert r['configuration']['coverage']=='compositional'
                    if name=='source JSON':assert r['configuration']['coverage']=='direct_published_example' and r['source_example']['figure']==12
                    if name=='conflicting slot':assert r['conflicts'] and all(x['status']=='conflict' for x in r['components'])
                    if name=='unknown':assert r['components'][0]['reference'] is None
                    if name=='unsupported layer':assert r['components'][0]['status']=='unsupported_context'
                    if name=='ambiguous':assert r['components'][0]['status']=='ambiguous'
                else:assert 'No personal assessment or physical aura detection' in p.stdout
            if output:Path('data',output).write_text(p.stdout,encoding='utf-8')
            cases.append(dict(case=name,passed=True))
        check('manual JSON',base,output='aura-reference.json')
        check('manual Markdown',base,'markdown',output='aura-reference.md')
        check('source JSON',example,output='aura-source-example.json')
        check('source Markdown',example,'markdown',output='aura-source-example.md')
        check('unknown',base|dict(components=[dict(color=None)]))
        check('ambiguous',base|dict(components=[dict(color=['blue','violet'])]))
        check('unsupported layer',base|dict(components=[dict(color='violet',context='crown_chakra')]))
        check('conflicting slot',base|dict(components=[dict(color='blue',slot='center'),dict(color='green',slot='center')]))
        check('uncertain',base|dict(components=[dict(color='black',certainty='uncertain')]))
        check('wrong profile',base|dict(profile='Brennan'),reject=True)
        check('photo',base|dict(photo='portrait.jpg'),reject=True)
        check('diagnosis',base|dict(task='diagnosis'),reject=True)
        check('strength',base|dict(aura_strength=9),reject=True)
        check('source override',example|dict(components=base['components']),reject=True)
    Path('data/aura-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Aura CLI cases passed')


if __name__=='__main__':run()
