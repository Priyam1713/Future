import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.mirror import PROFILE,read


def run():
    base=dict(schema_version=1,profile=PROFILE,task='guided_mirror_journal',mode='manual',
        session=dict(surface='ordinary_mirror',view='self_reflection_excluded',lighting='User-declared lamp behind chair',background='Dark fabric',intention='Reflect on my own notes',status='planned'))
    examples={'guided':base,'associations':base|dict(journal=[dict(experience_type='subjective_imagery',description='  I thought of a familiar person;perhaps only an impression.  ',uncertainty=True,associations=['A memory that matters to me.'])]),
        'no-imagery':base|dict(journal=[dict(experience_type='no_imagery',description='Nothing noticed.')]),
        'uncertain':base|dict(journal=[dict(experience_type='uncertain',description='Unclear shape\nI cannot classify it.',uncertainty=True)]),
        'discontinued':base|dict(session=dict(surface='unknown',status='discontinued'),journal=[]),
        'multiple':base|dict(session=dict(surface='ordinary_mirror',view='self_reflection_visible',status='completed',timestamp='2026-11-04T18:00:00+05:30'),stages=[dict(stage_id='gaze',status='completed')],journal=[dict(sequence=1,experience_type='observed_reflection',description='My ordinary reflection.'),dict(sequence=2,experience_type='imagined_imagery',description='A scene I deliberately imagined.',associations=['My own association.'])]),
        'skipped':base|dict(session=dict(status='completed'),stages=[dict(stage_id='gaze',status='skipped')],journal=[{}])}
    invalid_example=base|dict(stages=[dict(stage_id='gaze',status='skipped'),dict(stage_id='gaze',status='completed')])
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            proc=subprocess.run([sys.executable,'-m','future','mirror-scrying',str(path),'--format',fmt],capture_output=True)
            assert proc.returncode==(2 if reject else 0),(name,proc.stderr)
            actual=proc.stdout.decode('utf-8').replace('\r\n','\n')
            if reject:
                if fmt=='json':assert json.loads(actual)['status']=='rejected' and json.loads(actual)['session_report'] is None
                else:assert 'request rejected' in actual
            else:
                expected=read(value)
                if fmt=='json':assert json.loads(actual)==expected
                else:
                    replay=json.loads(actual.split('## Exact replay metadata')[1].split('```json\n')[1].split('\n```')[0])
                    assert read(replay['request'])==expected
            if output:Path('data',output).write_text(actual,encoding='utf-8')
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,value in examples.items():
            Path('data',f'mirror-{name}-input.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',value,output=f'mirror-{name}.json')
            check(name+' Markdown',value,'markdown',output=f'mirror-{name}.md')
        Path('data/mirror-invalid-input.json').write_text(json.dumps(invalid_example,indent=2)+'\n',encoding='utf-8')
        check('conflicting configuration JSON',invalid_example,reject=True,output='mirror-invalid.json')
        check('conflicting configuration Markdown',invalid_example,'markdown',True,'mirror-invalid.md')
        invalid=[('wrong profile',base|dict(profile='atkinson-pg43954-guided-journal-v1')),('wrong task',base|dict(task='contact')),
            ('seed unsupported',base|dict(seed='vision')),('seeded mode',base|dict(mode='seeded')),
            ('obsidian substitution',base|dict(session=dict(surface='obsidian'))),('invented angle',base|dict(session=dict(mirror_angle_degrees=45))),
            ('detected spirit',base|dict(journal=[dict(experience_type='verified_spirit')])),('bad timestamp',base|dict(session=dict(timestamp='now'))),
            ('planned completed stage',base|dict(stages=[dict(stage_id='gaze',status='completed')])),
            ('fake dictionary',base|dict(symbol_dictionary='universal')),('bad uncertainty',base|dict(journal=[dict(uncertainty='yes')])),
            ('bad association',base|dict(journal=[dict(associations=[True])]))]
        for name,value in invalid:check(name,value,reject=True)
    Path('data/mirror-input.json').write_text(json.dumps(examples['multiple'],indent=2)+'\n',encoding='utf-8')
    Path('data/mirror-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Mirror CLI cases passed')


if __name__=='__main__':run()
