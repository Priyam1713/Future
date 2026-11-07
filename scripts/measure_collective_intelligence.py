"""Actual local binary-pool complete-report measurements,not skill validation."""
import json,platform,statistics,subprocess,sys,time,tracemalloc
from fractions import Fraction as F
from future.collective_intelligence import read
from scripts.collective_intelligence_oracle import R,request,question,append,digest
from scripts.measure_ai_predictive_modeling import peak_memory
def workload(n,f,revisions=1,missing=False):
    q=request();q['questions']=[question('q'+str(i),'e'+str(i),outcome=i%2) for i in range(n)];q['forecasts']=[];q['forecasters']=[dict(id='f'+str(j),kind='synthetic',dependency_group='g'+str(j//4),weight=str(0 if j%3==0 else j+1) if missing else '1') for j in range(f)]
    if missing:q['pool']['kind']='declared_weight'
    for i in range(n):
        for j in range(f):
            if missing and (i+j)%4!=0:continue
            for v in range(revisions):append(q,'f'+str(j),str(F((i+j+v)%11,10)),'2025-01-0'+str(5+v)+'T00:00:00Z',qid='q'+str(i))
    return q
def run():
    results=[]
    for name,q in [('small',request()),('medium',workload(8,8)),('dense',workload(32,32,2)),('missing-weighted',workload(32,32,missing=True))]:
        times=[]
        for _ in range(3):
            start=time.perf_counter();r=read(q);times.append(time.perf_counter()-start)
        tracemalloc.start();read(q);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        inp=R/('data/collective-intelligence-'+name+'-benchmark-input.json');inp.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8',newline='\n')
        start=time.perf_counter();cp=subprocess.run([sys.executable,'-m','future','collective-intelligence',str(inp)],cwd=R,capture_output=True);elapsed=time.perf_counter()-start;assert cp.returncode==0,cp.stderr
        results.append(dict(id=name,questions=len(q['questions']),forecasters=len(q['forecasters']),revisions=len(q['forecasts']),input_sha256=digest(q),budget=r['budget'],seconds=times,median_seconds=statistics.median(times),cli_seconds=elapsed,python_traced_peak_bytes=peak,under_proposed_five_seconds=max(times+[elapsed])<=5))
    peak=peak_memory();out=dict(measured=True,environment=dict(python=sys.version,platform=platform.platform()),profile_sha256=r['profile']['sha256'],code_sha256=r['code_sha256'],protocol='Three untraced complete in-process reports; separate tracemalloc report; one complete CLI including imports/registry/serialization. Native peak is whole helper including imports,all workloads and tracing,not CLI-child/per-workload peak.',process_peak_working_set_bytes=peak,under_proposed_128_MiB=peak is not None and peak<=128*1024**2,results=results,scope='Recorded local synthetic workloads,not universal performance or empirical forecast skill.')
    (R/'data/collective-intelligence-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print([(r['id'],r['median_seconds'],r['cli_seconds']) for r in results],peak)
if __name__=='__main__':run()
