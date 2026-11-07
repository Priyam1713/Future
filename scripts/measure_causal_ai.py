"""Actual finite causal complete-report measurements,not predictive validation."""
import itertools,json,platform,statistics,subprocess,sys,time,tracemalloc
from future.causal_ai import read
from scripts.causal_ai_oracle import R,request,structural,digest
from scripts.measure_ai_predictive_modeling import peak_memory
def workload(n,k):
    names=['n'+str(i) for i in range(n-2)]+['X','Y'];q=request(names,list(itertools.combinations(names,2)),names[:-2]);states=[str(i) for i in range(k)]
    for node in q['nodes']:node['states']=states
    q['joint']=[dict(assignment=dict(zip(names,v)),weight='1/'+str(k**n)) for v in itertools.product(states,repeat=n)];return q
def run():
    results=[]
    for name,q in [('small',structural()[0]),('medium',workload(5,2)),('dense',workload(7,3)),('diagnostic',request(('Z','X','Y'),(('Z','X'),('Z','Y'),('X','Y'))))]:
        times=[]
        for _ in range(3):
            start=time.perf_counter();r=read(q);times.append(time.perf_counter()-start)
        tracemalloc.start();read(q);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        inp=R/('data/causal-ai-'+name+'-benchmark-input.json');inp.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8',newline='\n')
        start=time.perf_counter();cp=subprocess.run([sys.executable,'-m','future','causal-ai',str(inp)],cwd=R,capture_output=True);elapsed=time.perf_counter()-start;assert cp.returncode==0,cp.stderr
        results.append(dict(id=name,nodes=len(q['nodes']),joint_rows=len(q['joint']),input_sha256=digest(q),budget=r['budget'],identification_status=r['identification_status'],seconds=times,median_seconds=statistics.median(times),cli_seconds=elapsed,python_traced_peak_bytes=peak,under_proposed_five_seconds=max(times+[elapsed])<=5))
    peak=peak_memory();out=dict(measured=True,environment=dict(python=sys.version,platform=platform.platform()),profile_sha256=r['profile']['sha256'],code_sha256=r['code_sha256'],protocol='Three untraced complete in-process reports; separate tracemalloc report; one complete CLI. Native peak covers whole helper,imports,all workloads and tracing,not CLI-child/per-workload peak.',process_peak_working_set_bytes=peak,under_proposed_128_MiB=peak is not None and peak<=128*1024**2,results=results,scope='Local synthetic measurements only; not universal performance or empirical causal validation.')
    (R/'data/causal-ai-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print([(r['id'],r['median_seconds'],r['cli_seconds']) for r in results],peak)
if __name__=='__main__':run()
