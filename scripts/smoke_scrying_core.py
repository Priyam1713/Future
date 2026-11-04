import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.scrying import PROFILE,read


def run():
    base=dict(schema_version=1,profile=PROFILE,task='guided_journal',mode='manual',
        session=dict(surface='crystal',lighting='Window behind my seat',background='Dark cloth',intention='Record what I notice',status='planned'))
    examples={'guided':base,'dark':base|dict(session=dict(surface='dark_backed_glass',lighting=None,background='Black cloth')),
        'associations':base|dict(journal=[dict(experience_type='subjective_imagery',description='  A pale circle; perhaps just a reflection.  ',uncertainty=True,associations=['For me,this recalls a familiar ring.'])]),
        'no-imagery':base|dict(journal=[dict(experience_type='no_imagery',description='Nothing noticed.')]),
        'uncertain':base|dict(journal=[dict(experience_type='uncertain',description='Not sure what I noticed.\nI will leave it open.',uncertainty=True)]),
        'multiple':base|dict(session=dict(surface='glass',timestamp='2026-11-04T17:30:00+05:30',status='completed'),journal=[dict(sequence=1,experience_type='observed_reflection',description='The window outline.'),dict(sequence=2,experience_type='imagined_imagery',description='A chair I deliberately pictured.',associations=['My own workspace.'])]),
        'visualization':base|dict(session=dict(surface='water_glass',practice='familiar_visualization',visualization_subject='a familiar cup'),journal=[dict(experience_type='imagined_imagery',description='A cup I chose to picture.')]),
        'empty':base|dict(session=dict(surface='unknown',status='discontinued'),journal=[{},dict(description='')])}
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            proc=subprocess.run([sys.executable,'-m','future','scrying',str(path),'--format',fmt],capture_output=True)
            assert proc.returncode==(2 if reject else 0),(name,proc.stderr)
            actual=proc.stdout.decode('utf-8').replace('\r\n','\n')
            if reject:assert json.loads(actual)['status']=='rejected'
            else:
                expected=read(value)
                if fmt=='json':assert json.loads(actual)==expected
                else:
                    replay=json.loads(actual.split('## Exact replay metadata')[1].split('```json\n')[1].split('\n```')[0])
                    assert read(replay['request'])==expected
            if output:Path('data',output).write_text(actual,encoding='utf-8')
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,value in examples.items():
            Path('data',f'scrying-{name}-input.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',value,output=f'scrying-{name}.json')
            check(name+' Markdown',value,'markdown',output=f'scrying-{name}.md')
        invalid=[('wrong profile',base|dict(profile='Thomas1905')),('wrong task',base|dict(task='prediction')),
            ('seed unsupported',base|dict(seed='x')),('seeded mode',base|dict(mode='seeded')),
            ('unsupported surface',base|dict(session=dict(surface='camera'))),('null session',base|dict(session=None)),
            ('generated observation',base|dict(journal=[dict(experience_type='generated_creative_prompt')])),
            ('duplicate sequence',base|dict(journal=[dict(sequence=1),dict(sequence=1)])),
            ('bad timestamp',base|dict(session=dict(timestamp='now'))),('fake dictionary',base|dict(symbol_dictionary='universal')),
            ('invalid uncertainty',base|dict(journal=[dict(uncertainty='yes')])),('invalid association',base|dict(journal=[dict(associations=[True])]))]
        for name,value in invalid:check(name,value,reject=True)
    Path('data/scrying-input.json').write_text(json.dumps(examples['multiple'],indent=2)+'\n',encoding='utf-8')
    Path('data/scrying-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Scrying CLI cases passed')


if __name__=='__main__':run()
