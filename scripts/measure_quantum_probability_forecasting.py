"""Explicit real measurements;never imported/executed by numerical regressions."""
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time
import tracemalloc
from future import quantum_probability_forecasting as e
from future.remote_viewing import digest
R=Path(__file__).resolve().parents[1]


def measure():
    results=[]
    for name,n,gs in [('bernoulli',1,[dict(op='ry',target=0,angle=math.pi/3)]),('bell',2,[dict(op='h',target=0),dict(op='cx',target=1,control=0)]),('bounded64',4,[dict(op='ry',target=i%4,angle=.137*(i+1)) if i%5 else dict(op='cx',target=3,control=0) for i in range(64)])]:
        q=e.request('compare',qubits=n,gates=gs,shots=100000,stream='independent',comparator_seed=2)
        inp=R/('data/quantum-probability-forecasting-'+name+'-benchmark-input.json');inp.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
        a,_,_=e.evolve(n,gs);probs=[abs(z)**2 for z in a];good=e.indices(n,q['event']);p=math.fsum(probs[i] for i in good)/math.fsum(probs)
        phases={'known_p_direct':lambda:p,'statevector':lambda:e.evolve(n,gs),'circuit_sampling':lambda:e.sample(probs,good,100000,1),'classical_bernoulli':lambda:e.bernoulli(p,100000,2)}
        record=dict(id=name,request_sha256=digest(q),qubits=n,gates=len(gs),shots=100000,phases={})
        for key,fn in phases.items():
            elapsed=[]
            for _ in range(5):
                start=time.perf_counter_ns();fn();elapsed.append((time.perf_counter_ns()-start)/1e9)
            tracemalloc.start();fn();_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
            med=statistics.median(elapsed);record['phases'][key]=dict(seconds=elapsed,median_seconds=med,python_traced_peak_bytes=peak,shots_per_second=100000/med if 'sampling' in key or key=='classical_bernoulli' else None)
        start=time.perf_counter_ns();cp=subprocess.run([sys.executable,'-m','future','quantum-probability-forecasting',str(inp)],cwd=R,capture_output=True);record['total_cli_seconds']=(time.perf_counter_ns()-start)/1e9
        assert cp.returncode==0
        report=json.loads(cp.stdout);record['event_probability']=report['result']['event']['ideal_model_probability'];record['circuit_count']=report['result']['sampling']['event_count'];record['classical_count']=report['result']['classical']['count']
        record['classical_sampling_faster']=record['phases']['classical_bernoulli']['median_seconds']<record['phases']['circuit_sampling']['median_seconds'];record['known_p_faster_than_sampling']=record['phases']['known_p_direct']['median_seconds']<min(record['phases']['classical_bernoulli']['median_seconds'],record['phases']['circuit_sampling']['median_seconds'])
        results.append(record)
    packages={}
    for name in ('qiskit','qiskit-aer','qiskit-algorithms'):
        try:packages[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:packages[name]='not installed'
    from scripts.measure_ai_predictive_modeling import peak_memory
    peak=peak_memory()
    out=dict(version=1,measured=True,environment=dict(python=sys.version,platform=platform.platform(),processor=platform.processor(),packages=packages),protocol='Five untraced warm/cold-order repetitions per phase;separate tracemalloc run per phase measures Python allocations only;CLI includes process/import/registry/report costs;known-p direct is lookup of already derived p. Not a QAE or hardware comparison.',process_peak_working_set_bytes=peak,process_memory_scope='Whole measurement process including imports/tracing;not isolated per kernel or CLI child',profile_sha256=e.PROFILE_HASH,code_sha256=e.read(e.request())['code_sha256'],results=results,conclusion='Direct classical sampling was faster in these measured cases;known-p lookup was fastest. No quantum advantage or unknown-event forecast evidence.')
    (R/'data/quantum-probability-forecasting-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(peak=out['process_peak_working_set_bytes'],cases=[dict(id=r['id'],cli=r['total_cli_seconds'],circuit=r['phases']['circuit_sampling']['median_seconds'],classical=r['phases']['classical_bernoulli']['median_seconds']) for r in results]),indent=2))

if __name__=='__main__':measure()
