"""Public CLI acceptance and reproducible example artifacts."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.oracle import PROFILE, read
from future.card_random import PROTOCOL


def run():
    base=dict(schema_version=1,profile=PROFILE,task='symbolic_reading',mode='seeded',spread='three',
        seed='Future-Lenormand-v1',protocol=PROTOCOL,orientation_policy='upright_only',
        question='What symbolic themes might help me reflect on a project?')
    manual={k:v for k,v in base.items() if k not in ('seed','protocol')}|dict(mode='manual',
        cards=[dict(card_id='lenormand-'+n) for n in ['28','25','09']])
    examples={'one':base|dict(spread='one'),'three':base,'five':base|dict(spread='five'),'manual':manual}
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            p=subprocess.run([sys.executable,'-X','utf8','-m','future','oracle',str(path),'--format',fmt],
                capture_output=True,text=True,encoding='utf-8')
            assert (p.returncode!=0)==reject,(name,p.stderr)
            if not reject:
                expected=read(value)
                if fmt=='json':assert json.loads(p.stdout)==expected
                else:
                    replay=json.loads(p.stdout.split('```json\n')[1].split('\n```')[0])
                    assert read(replay['request'])==expected
            if output:Path('data',output).write_text(p.stdout,encoding='utf-8')
            cases.append(dict(case=name,passed=True))
        for name,value in examples.items():
            Path('data',f'oracle-{name}-input.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',value,output=f'oracle-{name}.json')
            check(name+' Markdown',value,'markdown',output=f'oracle-{name}.md')
        for name,value in [
            ('unknown deck',base|dict(profile='Kipper')),
            ('unknown protocol',base|dict(protocol='v2')),
            ('reversed policy',base|dict(orientation_policy='seeded_reversals')),
            ('empty seed',base|dict(seed='')),
            ('mixed mode',base|dict(cards=[])),
            ('unknown spread',base|dict(spread='nine')),
            ('duplicate cards',manual|dict(cards=[dict(card_id='lenormand-01')]*3)),
            ('invalid draw count',manual|dict(cards=[])),
            ('unknown card',manual|dict(cards=[dict(card_id='major-00')]*3)),
            ('explicit reversal',manual|dict(cards=[dict(card_id='lenormand-'+n,orientation='reversed') for n in ['01','02','03']])),
            ('unsupported input',base|dict(significator='auto')),
            ('factual prediction',base|dict(task='predict'))]:
            check(name,value,reject=True)
    Path('data/oracle-lenormand-input.json').write_text(json.dumps(base,indent=2)+'\n',encoding='utf-8')
    Path('data/oracle-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Oracle CLI cases passed')


if __name__=='__main__':run()
