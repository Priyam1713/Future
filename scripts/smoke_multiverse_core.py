"""Exact raw UTF8/LF accepted/rejected CLI reports."""
import concurrent.futures,hashlib,json,os,subprocess,sys
from pathlib import Path
from future.scrying import load_input
from scripts.verify_multiverse import fixture
R=Path(__file__).resolve().parents[1];D=R/'data/multiverse-cli'
POLICY=b'# Preserve exact CLI bytes and intentional replay whitespace.\n* -text\n*.md whitespace=-blank-at-eof\n'
def run(write=False):
    D.mkdir(exist_ok=True)
    if write:(D/'.gitattributes').write_bytes(POLICY)
    else:assert (D/'.gitattributes').read_bytes()==POLICY
    records=[(name,json.dumps(c['input'],ensure_ascii=False,indent=2)+'\n',c['exit_code'],'.json') for name,c in fixture()['cases'].items()]
    records += [(name,payload,2,'.txt') for name,payload in [('duplicate','{"schema_version":1,"schema_version":1}'),('nan','{"R":NaN}'),('infinity','{"R":Infinity}'),('negative-infinity','{"R":-Infinity}')]]
    def check(item):
        name,payload,code,ext=item;inp=D/(name+'-input'+ext);raw=payload.encode('utf-8')
        if write:inp.write_bytes(raw)
        else:assert inp.read_bytes()==raw
        outputs={}
        for fmt,suffix in [('json','.json'),('markdown','.md')]:
            env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
            cp=subprocess.run([sys.executable,'-m','future','multiverse',str(inp),'--format',fmt],cwd=R,capture_output=True,env=env)
            assert cp.returncode==code,(name,cp.returncode,cp.stderr)
            data=cp.stdout;path=D/(name+'-'+fmt+suffix)
            if write:path.write_bytes(data)
            else:assert path.read_bytes()==data,(name,fmt)
            outputs[fmt]=hashlib.sha256(data).hexdigest()
            if fmt=='json':assert json.loads(data)['status']==('accepted' if code==0 else 'rejected')
        return dict(id=name,input=inp.relative_to(R).as_posix(),raw_input_sha256=hashlib.sha256(raw).hexdigest(),exit_code=code,outputs=outputs)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:manifest=list(pool.map(check,records))
    out=dict(passed=True,cli_cases=len(records)*2,accepted_pairs=sum(c==0 for _,_,c,_ in records),rejected_pairs=sum(c!=0 for _,_,c,_ in records),records=manifest)
    path=R/'data/multiverse-cli-replay.json'
    if write:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    else:assert load_input(path)==out
    print(str(out['cli_cases'])+' CLI cases pass;'+str(out['accepted_pairs'])+'accepted/'+str(out['rejected_pairs'])+'rejected exact JSON/Markdown pairs')
if __name__=='__main__':run('--write' in sys.argv)
