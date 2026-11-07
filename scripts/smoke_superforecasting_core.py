"""Exact saved accepted/rejected JSON and Markdown CLI replay."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from future.scrying import load_input
from scripts.superforecasting_scenarios import cases
R=Path(__file__).resolve().parents[1]
D=R/'data/superforecasting-cli'


def run(write=False):
    D.mkdir(exist_ok=True)
    if write:(D/'.gitattributes').write_bytes(b'* -text\n')
    records=[]
    for name,(q,code) in cases().items():
        payload=json.dumps(q,ensure_ascii=False,indent=2)+'\n'
        if name=='unicode-whitespace':payload=' \n'+payload+'\t\n'
        records.append((name,payload,code,'.json'))
    records.extend((name,payload,2,'.txt') for name,payload in [('duplicate','{"schema_version":1,"schema_version":1}'),('nan','{"probability":NaN}'),('infinity','{"ratio":Infinity}'),('negative-infinity','{"ratio":-Infinity}')])
    manifest=[]
    for name,payload,code,ext in records:
        inp=D/(name+'-input'+ext);raw=payload.encode('utf-8')
        if write:inp.write_bytes(raw)
        else:assert inp.read_bytes()==raw,('Rawinput replay mismatch',name)
        outputs={}
        for fmt,suffix in [('json','.json'),('markdown','.md')]:
            cp=subprocess.run([sys.executable,'-m','future','superforecasting',str(inp),'--format',fmt],cwd=R,capture_output=True)
            assert cp.returncode==code,(name,cp.returncode,cp.stderr)
            data=cp.stdout.replace(b'\r\n',b'\n');path=D/(name+'-'+fmt+suffix)
            if write:path.write_bytes(data)
            else:assert path.read_bytes()==data,('Exact output replay mismatch',name,fmt)
            outputs[fmt]=hashlib.sha256(data).hexdigest()
            if fmt=='json':assert json.loads(data)['status']==('accepted' if code==0 else 'rejected')
        manifest.append(dict(id=name,input=inp.relative_to(R).as_posix(),raw_input_sha256=hashlib.sha256(raw).hexdigest(),exit_code=code,outputs=outputs))
    out=dict(passed=True,cli_cases=2*len(records),accepted_pairs=sum(c==0 for _,_,c,_ in records),rejected_pairs=sum(c==2 for _,_,c,_ in records),records=manifest)
    path=R/'data/superforecasting-cli-replay.json'
    if write:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    else:assert load_input(path)==out
    print(str(out['cli_cases'])+' CLI cases pass;'+str(out['accepted_pairs'])+'accepted/'+str(out['rejected_pairs'])+'rejected exact JSON/Markdown pairs')

if __name__=='__main__':run('--write' in sys.argv)
