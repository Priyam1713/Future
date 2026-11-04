import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.runes import PROFILE, PROTOCOL, read


def run():
    seed=dict(schema_version=1,profile=PROFILE,task='symbolic_reading',mode='seeded',spread='three',
        protocol=PROTOCOL,seed='Future-Runes-v1',orientation_policy='upright_only')
    manual={k:v for k,v in seed.items() if k not in ('seed','protocol')}|dict(mode='manual',
        runes=[dict(rune_id=k) for k in ['rune-01','rune-10','rune-18']])
    examples={'one':seed|dict(spread='one'),'three':seed,'manual':manual,
        'unknown':manual|dict(runes=[dict(rune_id=k) for k in ['rune-06','rune-14','rune-15']]),
        'custom':seed|dict(positions=['Resources','Friction','Next reflection']),
        'manual-one':manual|dict(spread='one',runes=[dict(rune_id='rune-13')])}
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            # Deliberately no -X utf8: the runes command must emit Unicode on Windows itself.
            proc=subprocess.run([sys.executable,'-m','future','runes',str(path),'--format',fmt],capture_output=True)
            assert (proc.returncode!=0)==reject,(name,proc.stderr)
            if not reject:
                actual=proc.stdout.decode('utf-8').replace('\r\n','\n');expected=read(value)
                if fmt=='json':assert json.loads(actual)==expected
                else:
                    replay=json.loads(actual.split('```json\n')[1].split('\n```')[0])
                    assert read(replay['request'])==expected
                if output:Path('data',output).write_text(actual,encoding='utf-8')
            cases.append(dict(case=name,passed=True))
        for name,value in examples.items():
            Path('data',f'runes-{name}-input.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',value,output=f'runes-{name}.json')
            check(name+' Markdown',value,'markdown',output=f'runes-{name}.md')
        for name,value in [('wrong profile',seed|dict(profile='Blum25')),('wrong protocol',seed|dict(protocol='other')),
            ('empty seed',seed|dict(seed='')),('long seed',seed|dict(seed='x'*257)),
            ('mixed modes',seed|dict(runes=manual['runes'])),('manual seed',manual|dict(seed='x')),
            ('duplicates',manual|dict(runes=[dict(rune_id='rune-01')]*3)),
            ('blank',manual|dict(runes=[dict(rune_id='blank')]*3)),
            ('reversals',seed|dict(orientation_policy='reversed')),('prediction',seed|dict(task='prediction')),
            ('wrong count',manual|dict(spread='one')),('duplicate labels',seed|dict(positions=['a','a','b']))]:
            check(name,value,reject=True)
    Path('data/runes-input.json').write_text(json.dumps(seed,indent=2)+'\n',encoding='utf-8')
    Path('data/runes-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Rune CLI cases passed')


if __name__=='__main__':run()
