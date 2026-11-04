import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.dream import PROFILE,read


def run():
    base=dict(schema_version=1,profile=PROFILE,task='historical_reflection',mode='manual')
    examples={'complete':base|dict(narrative='I was eating at a table,then saw a serpent.',recall='complete',lookups=['eating','serpent'],context=dict(hungry=True)),
        'multiple':base|dict(scenes=[dict(sequence=1,description='I drank from a cup.',objects=['cup']),dict(sequence=2,description='A serpent crossed the path.',uncertainty=True)],timestamp='2026-11-04T18:30:00+05:30',lookups=['drinking'],context=dict(thirsty=True)),
        'taxonomy':base|dict(narrative='A scene I later thought resembled an event.',taxonomy_claims=['theorematic'],context=dict(exact_correspondence_reported=True)),
        'context':base|dict(narrative='I dreamed my nose was missing.',lookups=['lost_nose'],context=dict(circumstances=['perfume_trade'])),
        'missing':base|dict(narrative='A staff seemed broken.',lookups=['broken_staff','unverified_motif']),
        'associations':base|dict(narrative='  A serpent curled near the door.  ',lookups=['serpent'],associations=['For me,a garden memory.'],personal_reflection='My association is my own.'),
        'fragmented':base|dict(narrative='',recall='fragmented',scenes=[{},dict(description=None,uncertainty=True)]),
        'conflicting':base|dict(narrative='A broken staff.',lookups=['broken_staff'],context=dict(staff_cases=['initial_account','repeat_during_paralysis']),taxonomy_claims=['enypnion','allegorical']),
        'annotated':base|dict(narrative=' A🐍 Café Cafe\u0301 ',annotations=[dict(motif_id='serpent',start=2,end=3),dict(motif_id='eating',start=4,end=8,decision='exclude')])}
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            proc=subprocess.run([sys.executable,'-m','future','dream',str(path),'--format',fmt],capture_output=True)
            assert proc.returncode==(2 if reject else 0),(name,proc.stderr)
            actual=proc.stdout.decode('utf-8').replace('\r\n','\n')
            if reject:assert json.loads(actual)['status']=='rejected' and json.loads(actual)['dream_report'] is None
            else:
                expected=read(value)
                if fmt=='json':assert json.loads(actual)==expected
                else:
                    replay=json.loads(actual.split('## Exact replay metadata')[1].split('```json\n')[1].split('\n```')[0])
                    assert read(replay['request'])==expected
            if output:Path('data',output).write_text(actual,encoding='utf-8')
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,value in examples.items():
            Path('data',f'dream-{name}-input.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',value,output=f'dream-{name}.json')
            check(name+' Markdown',value,'markdown',output=f'dream-{name}.md')
        invalid=[('wrong profile',base|dict(profile='Freud1913')),('wrong task',base|dict(task='diagnosis')),
            ('seed unsupported',base|dict(seed='x')),('automatic matching unsupported',base|dict(auto_tagging=True)),
            ('invalid context',base|dict(context=dict(hungry='yes'))),('invalid scene order',base|dict(scenes=[dict(sequence=2),dict(sequence=1)])),
            ('duplicate claims',base|dict(taxonomy_claims=['oneiros']*2)),('invalid timestamp',base|dict(timestamp='now')),
            ('bad span',base|dict(narrative='abc',annotations=[dict(motif_id='serpent',start=0,end=10)])),
            ('duplicate annotations',base|dict(annotations=[dict(motif_id='eating')]*2)),
            ('preference conflict',base|dict(lookups=['eating'],preferences=dict(historical_references=False))),
            ('unknown historical category',base|dict(taxonomy_claims=['universal']))]
        for name,value in invalid:check(name,value,reject=True)
    Path('data/dream-input.json').write_text(json.dumps(examples['complete'],indent=2)+'\n',encoding='utf-8')
    Path('data/dream-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Dream CLI cases passed')


if __name__=='__main__':run()
