"""Raw deterministic accepted/rejected JSON/Markdown CLI replay."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from future.scrying import load_input
from scripts.verify_psychohistory import fixture
R=Path(__file__).resolve().parents[1]
D=R/'data/psychohistory-cli'
POLICY=b'# Preserve exact CLI bytes and intentional replay whitespace.\n* -text\n*.md whitespace=-blank-at-eof\n'
def run(write=False):
    D.mkdir(exist_ok=True)
    if write:(D/'.gitattributes').write_bytes(POLICY)
    else:assert (D/'.gitattributes').read_bytes()==POLICY
    cases=dict(fixture()['cases']);cases.update(load_input(R/'tests/fixtures/psychohistory-boundaries-v1.json')['cases'])
    records=[(name,json.dumps(c['input'],ensure_ascii=False,indent=2)+'\n',c['exit_code'],'.json') for name,c in cases.items()]
    records += [(name,payload,2,'.txt') for name,payload in [('duplicate','{"schema_version":1,"schema_version":1}'),('nan','{"rho":NaN}'),('infinity','{"rho":Infinity}'),('negative-infinity','{"rho":-Infinity}')]]
    manifest=[]
    for name,payload,code,ext in records:
        inp=D/(name+'-input'+ext);raw=payload.encode('utf-8')
        if write:inp.write_bytes(raw)
        else:assert inp.read_bytes()==raw
        outputs={}
        for fmt,suffix in [('json','.json'),('markdown','.md')]:
            cp=subprocess.run([sys.executable,'-m','future','psychohistory',str(inp),'--format',fmt],cwd=R,capture_output=True)
            assert cp.returncode==code,(name,cp.returncode,cp.stderr)
            data=cp.stdout.replace(b'\r\n',b'\n');path=D/(name+'-'+fmt+suffix)
            if write:path.write_bytes(data)
            else:assert path.read_bytes()==data,(name,fmt)
            outputs[fmt]=hashlib.sha256(data).hexdigest()
            if fmt=='json':assert json.loads(data)['status']==('accepted' if code==0 else 'rejected')
        manifest.append(dict(id=name,input=inp.relative_to(R).as_posix(),raw_input_sha256=hashlib.sha256(raw).hexdigest(),exit_code=code,outputs=outputs))
    out=dict(passed=True,cli_cases=len(records)*2,accepted_pairs=sum(c==0 for _,_,c,_ in records),rejected_pairs=sum(c!=0 for _,_,c,_ in records),records=manifest)
    path=R/'data/psychohistory-cli-replay.json'
    if write:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    else:assert load_input(path)==out
    print(str(out['cli_cases'])+' CLI cases pass;'+str(out['accepted_pairs'])+'accepted/'+str(out['rejected_pairs'])+'rejected exact JSON/Markdown pairs')
if __name__=='__main__':run('--write' in sys.argv)
