"""Measured complete synthetic reports; process peak includes all helper work."""
import copy,json,platform,statistics,subprocess,sys,time,tracemalloc
from future.brain_intention import read
from scripts.brain_intention_oracle import R,request,digest
from scripts.measure_ai_predictive_modeling import peak_memory
def workload(n,c,samples):
    q=request('windows');template=q['trials'][0];q['trials']=[];q['channels']=[dict(id='c'+str(j),unit='arbitrary_units') for j in range(c)];q['fit_at']=10000
    for i in range(n):
        t=copy.deepcopy(template);t.update(id='t'+str(i),subject='subject'+str(i),source_id='file'+str(i),trial_id='trial'+str(i),start=0,end=samples,available_at=1000 if i<n//2 else 11000,predict_at=2000 if i<n//2 else 12000,label_available_at=3000 if i<n//2 else 13000,partition='TRAIN' if i<n//2 else 'TEST',label='A' if i%2==0 else 'B',values=[[((k*3+i+j)%7)-3 for k in range(samples)] for j in range(c)]);q['trials'].append(t)
    return q
def run():
    results=[]
    for name,q in [('small',request('windows')),('medium',workload(32,4,64)),('dense',workload(64,8,512)),('features',request())]:
        times=[]
        for _ in range(3):
            start=time.perf_counter();r=read(q);times.append(time.perf_counter()-start)
        tracemalloc.start();read(q);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        inp=R/('data/brain-intention-'+name+'-benchmark-input.json');inp.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8',newline='\n')
        start=time.perf_counter();cp=subprocess.run([sys.executable,'-m','future','brain-intention',str(inp)],cwd=R,capture_output=True);elapsed=time.perf_counter()-start;assert cp.returncode==0,cp.stderr
        results.append(dict(id=name,trials=len(q['trials']),channels=len(q['channels']),mode=q['mode'],samples=0 if q['mode']=='features' else len(q['trials'][0]['values'][0]),input_sha256=digest(q),budget=r['budget'],seconds=times,median_seconds=statistics.median(times),cli_seconds=elapsed,python_traced_peak_bytes=peak,under_proposed_five_seconds=max(times+[elapsed])<=5))
    peak=peak_memory();out=dict(measured=True,environment=dict(python=sys.version,platform=platform.platform()),profile_sha256=r['profile']['sha256'],code_sha256=r['code_sha256'],protocol='Three untraced complete-report repetitions; separate tracemalloc repetition; one full CLI including imports,registry and serialization. Native peak is whole helper process including all workloads and tracing, not CLI-child or per-workload peak.',process_peak_working_set_bytes=peak,under_proposed_128_MiB=peak is not None and peak<=128*1024**2,results=results,scope='Local synthetic examples; no empirical accuracy or universal performance bound.')
    (R/'data/brain-intention-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print([(r['id'],r['median_seconds'],r['cli_seconds']) for r in results],peak)
if __name__=='__main__':run()
