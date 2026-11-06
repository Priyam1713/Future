"""Saved accepted/rejected exact CLI JSON and Markdown replay."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from future import quantum_probability_forecasting as e
from future.scrying import load_input
from scripts.verify_quantum_probability_forecasting import negative_requests
R=Path(__file__).resolve().parents[1]
D=R/'data/quantum-probability-forecasting-cli'


def cases():
    f=load_input(R/'tests/fixtures/quantum_probability_forecasting_reference_v1.json');out={}
    for c in f['circuits'][:15]:out[c['id']]=(e.request(qubits=c['qubits'],gates=c['gates']),0)
    ry=[dict(op='ry',target=0,angle=math.pi/3)]
    for shots in (1,100):
        for seed in (1,2,4294967295):out[f'sample-{shots}-{seed}']=(e.request('sample',gates=ry,shots=shots,seed=seed),0)
    for name,g in [('certain',[dict(op='x',target=0)]),('impossible',[]),('bell',[dict(op='h',target=0),dict(op='cx',target=1,control=0)])]:out[name+'-shots']=(e.request('compare',qubits=2 if name=='bell' else 1,gates=g,shots=100),0)
    out['compare-common']=(e.request('compare',gates=ry,shots=100),0)
    out['compare-independent']=(e.request('compare',gates=ry,shots=100,stream='independent',comparator_seed=2),0)
    out['report']=(e.request('report',gates=ry,shots=100),0)
    out['report-ideal']=(e.request('report',gates=ry),0)
    out['maximum']=(e.request('sample',qubits=4,gates=[dict(op='h',target=k%4) for k in range(64)],shots=100000),0)
    for name in e.REFERENCES:out['reference-'+name]=(e.request('reference',reference=name),0)
    q=e.request('report',gates=ry,shots=100);q['provenance']['attribution']='  Original\nनमस्ते ```json\n  ';out['unicode-whitespace']=(q,0)
    out.update({'reject-'+name:(q,2) for name,q in negative_requests().items()})
    raw=[('duplicate','{"schema_version":1,"schema_version":1}'),('nan','{"angle":NaN}'),('infinity','{"angle":Infinity}'),('negative-infinity','{"angle":-Infinity}')]
    return out,raw


def run(write=False):
    D.mkdir(exist_ok=True);out,raw=cases();records=[]
    for name,(q,code) in out.items():
        payload=json.dumps(q,ensure_ascii=False,indent=2)+'\n'
        if name=='unicode-whitespace':payload=' \n'+payload+'\t\n'
        records.append((name,payload,code))
    records.extend((name,payload,2) for name,payload in raw)
    manifest=[]
    for name,payload,code in records:
        inp=D/(name+'-input.json')
        # Deliberately malformed raw fixtures use .txt to preserve strict-JSON audit semantics.
        if name in [r[0] for r in raw]:inp=inp.with_suffix('.txt')
        data=payload.encode('utf-8')
        if write:inp.write_bytes(data)
        else:assert inp.read_bytes()==data
        outputs={}
        for fmt,ext in [('json','.json'),('markdown','.md')]:
            cp=subprocess.run([sys.executable,'-m','future','quantum-probability-forecasting',str(inp),'--format',fmt],cwd=R,capture_output=True)
            assert cp.returncode==code,(name,cp.stderr)
            value=cp.stdout.replace(b'\r\n',b'\n');path=D/(name+'-'+fmt+ext)
            if write:path.write_bytes(value)
            else:assert path.read_bytes()==value,('Replay mismatch',name,fmt)
            outputs[fmt]=hashlib.sha256(value).hexdigest()
            if fmt=='json':
                parsed=json.loads(value);assert parsed['status']==('accepted' if code==0 else 'rejected')
        manifest.append(dict(id=name,input=inp.relative_to(R).as_posix(),raw_input_sha256=hashlib.sha256(data).hexdigest(),exit_code=code,outputs=outputs))
    report=dict(passed=True,cli_cases=len(records)*2,accepted_pairs=sum(c==0 for _,_,c in records),rejected_pairs=sum(c==2 for _,_,c in records),records=manifest)
    path=R/'data/quantum-probability-forecasting-cli-replay.json'
    if write:path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    else:assert load_input(path)==report
    print(str(report['cli_cases'])+' CLI cases pass;exact accepted/rejected JSON and Markdown replay')

if __name__=='__main__':run('--write' in sys.argv)
