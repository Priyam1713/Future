"""Actual local measurements, separate from deterministic numerical reports."""
import json,platform,statistics,subprocess,sys,time,tracemalloc
from future.digital_twin import read
from scripts.digital_twin_oracle import R,request,digest
from scripts.measure_ai_predictive_modeling import peak_memory
def run():
    short=request((2,2));long=request(tuple(2 for _ in range(256)));missing=request(tuple(None if i%3 else 2 for i in range(256)));multi=request(tuple(2 for _ in range(128)));multi['parameters']['B']='1';multi.update(horizon=128,scenarios=[dict(id='s'+str(i),controls=[str(i%2)]*128) for i in range(8)],reference_scenario='s0')
    results=[]
    for name,q in [('short',short),('long',long),('missing-data',missing),('multi-scenario',multi)]:
        times=[]
        for _ in range(5):
            start=time.perf_counter_ns();report=read(q);times.append((time.perf_counter_ns()-start)/1e9)
        tracemalloc.start();read(q);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        inp=R/('data/digital-twin-'+name+'-benchmark-input.json');inp.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8',newline='\n')
        start=time.perf_counter_ns();cp=subprocess.run([sys.executable,'-m','future','digital-twin',str(inp)],cwd=R,capture_output=True);cli=(time.perf_counter_ns()-start)/1e9;assert cp.returncode==0
        results.append(dict(id=name,records=len(q['records']),horizon=q['horizon'],scenarios=len(q['scenarios']),request_sha256=digest(q),budget=report['budget'],seconds=times,median_seconds=statistics.median(times),cli_seconds=cli,python_traced_peak_bytes=peak,under_proposed_five_seconds=max(times+[cli])<=5))
    memory=peak_memory();out=dict(version=1,measured=True,environment=dict(python=sys.version,platform=platform.platform(),processor=platform.processor()),profile_sha256=report['profile']['sha256'],code_sha256=report['code_sha256'],protocol='Five untraced complete in-process report repetitions per workload;separate tracemalloc run per workload;one complete CLI invocation including imports,registry andserialization. Native memory iswhole measurement-process peak includingall imports,workloads andtracing;notisolated perworkload orCLIchild.',process_peak_working_set_bytes=memory,under_proposed_128_MiB=memory is not None and memory<=128*1024**2,results=results,scope='Representative local synthetic workloads;not universal performance or empirical accuracy.')
    (R/'data/digital-twin-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
