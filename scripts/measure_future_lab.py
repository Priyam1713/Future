"""Observed full Lab operations; no measurements embedded in deterministic forecasts."""
import json,platform,statistics,subprocess,sys,time,tracemalloc
from future.lab import invoke,evaluate,list_techniques
from future.lab.reference import noaa_reference
from scripts.verify_future_lab import fixture,demo
from scripts.measure_ai_predictive_modeling import peak_memory
from future.lab.common import ROOT as R,code_sha,digest
def run():
    f=fixture();ledger,_=demo();results=[]
    for name,fn in [('discovery54',list_techniques),('native51',lambda:invoke(f['native_samples']['51']['request'])),('complete_demo_report',lambda:evaluate(ledger)),('noaa_reference',noaa_reference)]:
        times=[]
        for _ in range(3):start=time.perf_counter();r=fn();times.append(time.perf_counter()-start)
        tracemalloc.start();fn();_,peak=tracemalloc.get_traced_memory();tracemalloc.stop();results.append(dict(id=name,seconds=times,median_seconds=statistics.median(times),python_traced_peak_bytes=peak,output_sha256=digest(r)))
    cli=[]
    for name,args in [('demo',['evaluate','data/future-lab-demo/final-ledger.json']),('noaa_reference',['noaa-reference'])]:
        start=time.perf_counter();cp=subprocess.run([sys.executable,'-m','future.lab']+args,cwd=R,capture_output=True);elapsed=time.perf_counter()-start;assert cp.returncode==0,cp.stderr;cli.append(dict(id=name,seconds=elapsed,raw_stdout_sha256=__import__('hashlib').sha256(cp.stdout).hexdigest()))
    out=dict(measured=True,environment=dict(python=sys.version,platform=platform.platform()),lab_code_sha256=digest({p.relative_to(R).as_posix():code_sha(p.relative_to(R).as_posix()) for p in sorted((R/'future/lab').glob('*.py'))}),results=results,cli=cli,process_peak_working_set_bytes=peak_memory(),protocol='Three untraced completeoperations,then separatetracemalloc run;fullCLI calls includeimports/serialization. Nativeprocesspeak coversentirehelper/imports/allworkloads/tracing,notperworkloadorCLIchild. Observations arenotuniversalperformanceguarantees.')
    (R/'data/future-lab-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print([(r['id'],r['median_seconds']) for r in results],out['process_peak_working_set_bytes'])
if __name__=='__main__':run()
