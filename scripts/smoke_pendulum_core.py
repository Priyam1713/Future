import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.pendulum import PROFILE,PROTOCOL,DISTRIBUTION,read


def run():
    manual=dict(schema_version=1,profile=PROFILE,task='symbolic_response',mode='manual',
        calibration=[dict(signal='clockwise',response='yes'),dict(signal='counterclockwise',response='no')],
        observations=[dict(signal='clockwise')],question='What perspectives could help me reflect?')
    seed={k:v for k,v in manual.items() if k not in ('calibration','observations')}|dict(mode='seeded',
        seed='Future-Pendulum-v1',protocol=PROTOCOL,distribution=DISTRIBUTION)
    examples={'manual-yes':manual,'manual-no':manual|dict(observations=[dict(signal='counterclockwise')]),
        'ambiguous':manual|dict(observations=[dict(signal='searching'),dict(signal='still')]),
        'partial':manual|dict(observations=[dict(signal='clockwise',quality='partial')]),
        'repeated-conflict':manual|dict(observations=[dict(signal='clockwise'),dict(signal='counterclockwise')]),
        'seeded':seed,'replay':seed}
    contradictory=manual|dict(calibration=manual['calibration']+[dict(signal='clockwise',response='no')])
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            proc=subprocess.run([sys.executable,'-m','future','pendulum',str(path),'--format',fmt],capture_output=True)
            assert proc.returncode==(2 if reject else 0),(name,proc.stderr)
            actual=proc.stdout.decode('utf-8').replace('\r\n','\n')
            if reject:
                if fmt=='json':assert json.loads(actual)['status']=='rejected' and json.loads(actual)['reading'] is None
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
            Path('data',f'pendulum-{name}-input.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',value,output=f'pendulum-{name}.json')
            check(name+' Markdown',value,'markdown',output=f'pendulum-{name}.md')
        Path('data/pendulum-contradictory-input.json').write_text(json.dumps(contradictory,indent=2)+'\n',encoding='utf-8')
        check('contradictory JSON',contradictory,reject=True,output='pendulum-contradictory.json')
        check('contradictory Markdown',contradictory,'markdown',True,'pendulum-contradictory.md')
        invalid=[('wrong profile',manual|dict(profile='Kit19')),('prediction task',manual|dict(task='prediction')),
            ('manual seed',manual|dict(seed='x')),('seeded observations',seed|dict(observations=[])),
            ('wrong protocol',seed|dict(protocol='other')),('wrong distribution',seed|dict(distribution='truth')),
            ('empty seed',seed|dict(seed='')),('long seed',seed|dict(seed='x'*257)),
            ('empty observations',manual|dict(observations=[])),('unknown field',manual|dict(sensor=True)),
            ('reserved signal mapping',manual|dict(calibration=[dict(signal='still',response='yes')])),
            ('invalid quality',manual|dict(observations=[dict(signal='clockwise',quality='certain')]))]
        for name,value in invalid:check(name,value,reject=True)
    assert Path('data/pendulum-seeded.json').read_bytes()==Path('data/pendulum-replay.json').read_bytes()
    Path('data/pendulum-input.json').write_text(json.dumps(seed,indent=2)+'\n',encoding='utf-8')
    Path('data/pendulum-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Pendulum CLI cases passed')


if __name__=='__main__':run()
