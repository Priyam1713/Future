"""Exact public Lab JSON/Markdown replay, alongside all54 unchanged native smokes."""
import concurrent.futures,copy,hashlib,json,os,subprocess,sys
from pathlib import Path
from future.lab.common import digest
from scripts.verify_future_lab import fixture,protocol_cases
R=Path(__file__).resolve().parents[1];D=R/'data/future-lab-cli';POLICY=b'* -text\n*.md whitespace=-blank-at-eof\n'
def cases():
    f=fixture();out=[]
    def add(name,command,payloads=None,code=0):out.append(dict(id=name,command=command,payloads=payloads or {},exit_code=code))
    add('list',['list']);add('inspect49',['inspect','49']);add('inspect60',['inspect','60'])
    for i in [4,8,51,57,60]:add('run'+str(i),['run','{request}'],dict(request=f['native_samples'][str(i)]['request']))
    add('validate',['validate','{request}'],dict(request=f['native_samples']['55']['request']))
    bad=copy.deepcopy(f['native_samples']['55']['request']);bad['input']['profile']['id']='wrong';add('native-error',['run','{request}'],dict(request=bad),2)
    add('create',['create','{plan}'],dict(plan=f['demo_plan']))
    created=json.loads((R/'data/future-lab-demo/created-ledger.json').read_text(encoding='utf-8'));forecast=json.loads((R/'data/future-lab-demo/forecast-ledger.json').read_text(encoding='utf-8'));final=json.loads((R/'data/future-lab-demo/final-ledger.json').read_text(encoding='utf-8'));report=json.loads((R/'data/future-lab-demo/research-report.json').read_text(encoding='utf-8'))
    add('forecast',['forecast','{ledger}','--at','2025-01-02T00:00:00Z'],dict(ledger=created));add('resolve',['resolve','{ledger}','{outcome}','--at','2025-01-11T00:00:00Z'],dict(ledger=forecast,outcome=f['demo_outcomes'][0]));add('evaluate',['evaluate','{ledger}'],dict(ledger=final));add('unresolved',['evaluate','{ledger}'],dict(ledger=created));add('compare',['compare','{one}','{two}'],dict(one=report,two=report))
    add('excluded',['inspect','25'],code=2);add('unknown-id',['inspect','61'],code=2)
    bad=copy.deepcopy(f['native_samples']['51']['request']);bad['operation']='multiverse';add('unknown-operation',['run','{request}'],dict(request=bad),2)
    for name in ['registry-hash','profile-identity','snapshot-binding','metric-combination','cross-split-group']:
        p,_=protocol_cases()[name];add(name,['create','{plan}'],dict(plan=p),2)
    add('late-forecast',['forecast','{ledger}','--at','2025-01-04T00:00:00Z'],dict(ledger=created),2);add('duplicate-forecast',['forecast','{ledger}','--at','2025-01-02T00:00:00Z'],dict(ledger=forecast),2);add('early-outcome',['resolve','{ledger}','{outcome}','--at','2025-01-11T00:00:00Z'],dict(ledger=created,outcome=f['demo_outcomes'][0]),2)
    for name,raw in [('duplicate','{"technique_id":1,"technique_id":1}'),('nan','{"x":NaN}'),('infinity','{"x":Infinity}'),('negative-infinity','{"x":-Infinity}')]:add(name,['run','{request}'],dict(request=raw),2)
    return out
def run(write=False):
    D.mkdir(exist_ok=True)
    if write:(D/'.gitattributes').write_bytes(POLICY)
    else:assert (D/'.gitattributes').read_bytes()==POLICY
    def check(case):
        paths={};hashes={}
        for key,payload in case['payloads'].items():
            raw=(payload if isinstance(payload,str) else json.dumps(payload,indent=2,ensure_ascii=False)+'\n').encode('utf-8');path=D/(case['id']+'-'+key+('.txt' if isinstance(payload,str) else '.json'))
            if write:path.write_bytes(raw)
            else:assert path.read_bytes()==raw
            paths[key]=str(path);hashes[path.relative_to(R).as_posix()]=hashlib.sha256(raw).hexdigest()
        cmd=[s.format(**paths) for s in case['command']];outputs={}
        for fmt,ext in [('json','.json'),('markdown','.md')]:
            env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1');cp=subprocess.run([sys.executable,'-m','future.lab']+cmd+['--format',fmt],cwd=R,capture_output=True,env=env);assert cp.returncode==case['exit_code'],(case['id'],cp.returncode,cp.stderr)
            path=D/(case['id']+'-'+fmt+ext)
            if write:path.write_bytes(cp.stdout)
            else:assert path.read_bytes()==cp.stdout,(case['id'],fmt)
            outputs[fmt]=hashlib.sha256(cp.stdout).hexdigest()
            if fmt=='json':assert json.loads(cp.stdout)['status'] in (['accepted'] if case['exit_code']==0 else ['rejected','native_rejected'])
        return dict(id=case['id'],exit_code=case['exit_code'],input_sha256=hashes,command=case['command'],outputs=outputs)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:records=list(pool.map(check,cases()))
    out=dict(passed=True,cli_cases=2*len(records),accepted_pairs=sum(r['exit_code']==0 for r in records),rejected_pairs=sum(r['exit_code']!=0 for r in records),records=records)
    path=R/'data/future-lab-cli-replay.json'
    if write:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    else:assert json.loads(path.read_text(encoding='utf-8'))==out
    print(str(out['cli_cases'])+' Lab CLI cases pass;'+str(out['accepted_pairs'])+'accepted/'+str(out['rejected_pairs'])+'rejected JSON/Markdown pairs')
if __name__=='__main__':run('--write' in sys.argv)
