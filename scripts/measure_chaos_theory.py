"""Measure whole finite Lorenz reports, including full requested integrations."""
import copy,hashlib,json,platform,statistics,subprocess,sys,time,tracemalloc
from future.chaos_theory import read
from scripts.chaos_theory_oracle import R,request,digest
from scripts.measure_ai_predictive_modeling import peak_memory
def run():
    results=[]
    for name,steps,dt,stride in [('small',1,'1/100',1),('medium',1000,'1/1000',10),('dense',4096,'1/1000',1),('long',4000,'1/100',100)]:
        q=request();q['integration'].update(steps=steps,dt=dt,trace_stride=stride);times=[]
        for _ in range(3):start=time.perf_counter();r=read(q);times.append(time.perf_counter()-start)
        tracemalloc.start();read(q);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        inp=R/('data/chaos-theory-'+name+'-benchmark-input.json');inp.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8',newline='\n')
        start=time.perf_counter();cp=subprocess.run([sys.executable,'-m','future','chaos-theory',str(inp)],cwd=R,capture_output=True);elapsed=time.perf_counter()-start;assert cp.returncode==0,cp.stderr
        results.append(dict(id=name,steps=steps,dt=dt,horizon=r['diagnostics']['horizon'],returned_times=len(r['rows']),budget=r['budget'],input_sha256=digest(q),seconds=times,median_seconds=statistics.median(times),cli_seconds=elapsed,python_traced_peak_bytes=peak,under_proposed_five_seconds=max(times+[elapsed])<=5))
    peak=peak_memory();out=dict(measured=True,environment=dict(python=sys.version,platform=platform.platform()),profile_sha256=r['profile']['sha256'],code_sha256=r['code_sha256'],protocol='Three untraced complete in-process reports; separate tracemalloc report; one full CLI withimports/registry/serialization perworkload. Native peak covers whole helper includingimports/allworkloads/tracing; not CLIchild/perworkload.',process_peak_working_set_bytes=peak,under_proposed_128_MiB=peak is not None and peak<=128*1024**2,results=results,scope='Synthetic finite dimensionless trajectories;no empirical forecast accuracy.')
    (R/'data/chaos-theory-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print([(x['id'],x['median_seconds'],x['cli_seconds']) for x in results],peak)
if __name__=='__main__':run()
