"""Real stdlib CPU wall/allocation/process measurements, outside replay contracts."""
import itertools
import json
import platform
import statistics
import subprocess
import sys
import time
import tracemalloc
from future.psychohistory import read
from scripts.psychohistory_oracle import R,request,digest
from scripts.measure_ai_predictive_modeling import peak_memory

def run():
    results=[]
    workloads=[('sparse',request(128,runs=16,trace=False)),('dense',request(64,list(itertools.combinations(range(64),2)),phi='1/64',runs=4,trace=False)),('ensemble',request(32,runs=128,trace=False))]
    workloads[2][1]['scenarios'][0]['initial'].update(mode='bernoulli',probability='1/8',fixed_seeds=[])
    for name,q in workloads:
        elapsed=[]
        for _ in range(5):
            start=time.perf_counter_ns();report=read(q);elapsed.append((time.perf_counter_ns()-start)/1e9)
        tracemalloc.start();read(q);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        inp=R/('data/psychohistory-'+name+'-benchmark-input.json');inp.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8',newline='\n')
        start=time.perf_counter_ns();cp=subprocess.run([sys.executable,'-m','future','psychohistory',str(inp)],cwd=R,capture_output=True);cli=(time.perf_counter_ns()-start)/1e9;assert cp.returncode==0
        results.append(dict(id=name,nodes=q['population']['size'],edges=len(q['scenarios'][0]['edges']),runs=q['runs'],round_cap=q['rounds'],request_sha256=digest(q),budget=report['budget'],seconds=elapsed,median_seconds=statistics.median(elapsed),cli_seconds=cli,python_traced_peak_bytes=peak,under_proposed_five_seconds=max(elapsed+[cli])<=5))
    memory=peak_memory()
    out=dict(version=1,measured=True,environment=dict(python=sys.version,platform=platform.platform(),processor=platform.processor()),profile_sha256=report['profile']['sha256'],code_sha256=report['code_sha256'],protocol='Five untraced complete in-process report repetitions per workload;separate tracemalloc repetition for Python allocations;one whole CLI invocation including imports,registry,serialization. Native memory is whole measurement helper peak including all workloads/imports/tracing,not isolated per workload or CLI child.',process_peak_working_set_bytes=memory,under_proposed_128_MiB=memory is not None and memory<=128*1024**2,results=results,scope='Local representative synthetic workloads only;not universal or real-world forecast performance.')
    (R/'data/psychohistory-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
