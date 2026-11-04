import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.iching import PROFILE, POLICY, read
from future.iching_cast import PROTOCOL


def run():
    base=dict(schema_version=1,profile=PROFILE,reading_policy=POLICY,task='symbolic_reading',
        mode='manual',method='manual',line_order='bottom_to_top',lines=[6,7,8,9,7,8],
        question='What symbolic perspectives could help me reflect on a project?')
    seed={k:v for k,v in base.items() if k!='lines'}|dict(mode='seeded',method='three-coin',protocol=PROTOCOL,seed='Future-IChing-v1')
    examples={'no-moving':base|dict(lines=[7]*6),'one-moving':base|dict(lines=[9,7,7,7,7,7]),
        'multiple-moving':base,'all-moving-1':base|dict(lines=[9]*6),'all-moving-2':base|dict(lines=[6]*6),
        'seeded':seed,'yarrow':seed|dict(method='yarrow-marginal'),
        'manual-known':base|dict(lines=[7,7,7,8,8,6]),'variant-64':base|dict(lines=[8,7,6,7,8,7])}
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            proc=subprocess.run([sys.executable,'-X','utf8','-m','future','iching',str(path),'--format',fmt],
                capture_output=True,text=True,encoding='utf-8')
            assert (proc.returncode!=0)==reject,(name,proc.stderr)
            if not reject:
                expected=read(value)
                if fmt=='json':assert json.loads(proc.stdout)==expected
                else:
                    replay=json.loads(proc.stdout.split('```json\n')[1].split('\n```')[0])
                    assert read(replay['request'])==expected
            if output:Path('data',output).write_text(proc.stdout,encoding='utf-8')
            cases.append(dict(case=name,passed=True))
        for name,value in examples.items():
            Path('data',f'iching-{name}-input.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',value,output=f'iching-{name}.json')
            check(name+' Markdown',value,'markdown',output=f'iching-{name}.md')
        for name,value in [('wrong profile',base|dict(profile='Wilhelm')),
            ('wrong policy',base|dict(reading_policy='single_priority')),
            ('wrong order',base|dict(line_order='top_to_bottom')),
            ('five lines',base|dict(lines=[7]*5)),('invalid value',base|dict(lines=[5]*6)),
            ('boolean value',base|dict(lines=[True]*6)),('mixed manual seed',base|dict(seed='x')),
            ('mixed seeded lines',seed|dict(lines=[7]*6)),('wrong method',seed|dict(method='physical-yarrow')),
            ('wrong protocol',seed|dict(protocol='future-cards-sha256-fy-v1')),
            ('empty seed',seed|dict(seed='')),('prediction input',base|dict(task='prediction'))]:
            check(name,value,reject=True)
    Path('data/iching-input.json').write_text(json.dumps(seed,indent=2)+'\n',encoding='utf-8')
    Path('data/iching-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'I Ching CLI cases passed')


if __name__=='__main__':run()
