"""Actual complete-report CPU/allocation/process measurements; not regression output."""
import json,platform,statistics,subprocess,sys,time,tracemalloc
from future.agent_based import read
from scripts.agent_based_oracle import R,request,grid,digest
from scripts.measure_ai_predictive_modeling import peak_memory
def run():
    small=request(grid(7,7,{(1,2),(2,3),(3,1),(3,2),(3,3)}),4)
    medium=request([[int((r*17+c*11)%5<2) for c in range(32)] for r in range(32)],64,False)
    dense=request([[1]*64 for _ in range(64)],128,False)
    scenarios=request([[int((r*17+c*11)%5<2) for c in range(32)] for r in range(32)],64,False)
    scenarios['scenarios']=[dict(id='s'+str(i),initial_grid=[[int((r*17+c*11+i)%5<2) for c in range(32)] for r in range(32)]) for i in range(4)];scenarios['reference_scenario']='s0'
    results=[]
    for name,q in [('small',small),('medium',medium),('dense',dense),('scenarios',scenarios)]:
        times=[]
        for _ in range(5):
            start=time.perf_counter_ns();report=read(q);times.append((time.perf_counter_ns()-start)/1e9)
        tracemalloc.start();read(q);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        inp=R/('data/agent-based-'+name+'-benchmark-input.json');inp.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8',newline='\n')
        start=time.perf_counter_ns();cp=subprocess.run([sys.executable,'-m','future','agent-based',str(inp)],cwd=R,capture_output=True);cli=(time.perf_counter_ns()-start)/1e9;assert cp.returncode==0
        results.append(dict(id=name,geometry=q['geometry'],ticks=q['ticks'],scenarios=len(q['scenarios']),initialization='Explicitdeterministic pattern;nostochastic initialization',request_sha256=digest(q),budget=report['budget'],seconds=times,median_seconds=statistics.median(times),cli_seconds=cli,python_traced_peak_bytes=peak,under_proposed_five_seconds=max(times+[cli])<=5))
    memory=peak_memory();out=dict(version=1,measured=True,environment=dict(python=sys.version,platform=platform.platform(),processor=platform.processor()),profile_sha256=report['profile']['sha256'],code_sha256=report['code_sha256'],protocol='Five untraced complete in-process report repetitions perworkload;separate tracemalloc repetition forPythonallocations;onecompleteCLI invocation includingimports,registry andserialization. Native memory iswhole measurement-process peak includingimports,allworkloads andtracing;notisolated perworkload orCLIchild.',process_peak_working_set_bytes=memory,under_proposed_128_MiB=memory is not None and memory<=128*1024**2,results=results,scope='Localrepresentative explicit syntheticboards only;notuniversal performance orreal-world predictive accuracy.')
    (R/'data/agent-based-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
