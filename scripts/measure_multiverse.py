"""Measure complete exact finite scenario reports; no universe-prediction benchmark."""
import json,platform,statistics,subprocess,sys,time,tracemalloc
from future.multiverse import read
from scripts.multiverse_oracle import R,request,node,digest
from scripts.measure_ai_predictive_modeling import peak_memory
def workload(n,qcount,deep=False):
    q=request()
    if deep:q['nodes']=[node('n'+str(i),'n'+str(i-1) if i else None,'1','-1' if i==n-1 else None) for i in range(n)];root='n0'
    else:q['nodes']=[node('R',None,'1')]+[node('n'+str(i),'R','1/'+str(n-1),str(i-(n//2))) for i in range(n-1)];root='R'
    ids=[x['id'] for x in q['nodes']];q['queries']=[dict(id='q'+str(i),given=ids[i%len(ids)],target=root if i%2 else ids[(i+1)%len(ids)]) for i in range(qcount)];return q
def run():
    results=[]
    for name,q in [('small',request()),('medium',workload(64,64)),('dense',workload(256,256)),('depth',workload(33,256,True))]:
        times=[]
        for _ in range(3):start=time.perf_counter();r=read(q);times.append(time.perf_counter()-start)
        tracemalloc.start();read(q);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop();inp=R/('data/multiverse-'+name+'-benchmark-input.json');inp.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8',newline='\n')
        start=time.perf_counter();cp=subprocess.run([sys.executable,'-m','future','multiverse',str(inp)],cwd=R,capture_output=True);elapsed=time.perf_counter()-start;assert cp.returncode==0,cp.stderr
        results.append(dict(id=name,nodes=len(q['nodes']),queries=len(q['queries']),leaves=len(r['leaves']),budget=r['budget'],input_sha256=digest(q),seconds=times,median_seconds=statistics.median(times),cli_seconds=elapsed,python_traced_peak_bytes=peak,under_proposed_five_seconds=max(times+[elapsed])<=5))
    peak=peak_memory();out=dict(measured=True,environment=dict(python=sys.version,platform=platform.platform()),profile_sha256=r['profile']['sha256'],code_sha256=r['code_sha256'],protocol='Three untraced complete in-process reports; separate tracemalloc report; one full CLI perworkload. Native peak covers whole helper/imports/allworkloads/tracing,not CLIchild/perworkload.',process_peak_working_set_bytes=peak,under_proposed_128_MiB=peak is not None and peak<=128*1024**2,results=results,scope='Declared finite synthetic scenario probability/utility arithmetic;no empiricaluniverseobservations.')
    (R/'data/multiverse-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print([(r['id'],r['median_seconds'],r['cli_seconds']) for r in results],peak)
if __name__=='__main__':run()
