"""Measured local complete synthetic play-ledger reports,not market accuracy."""
import json,platform,statistics,subprocess,sys,time,tracemalloc
from datetime import datetime,timedelta,timezone
from future.prediction_markets import read
from scripts.prediction_markets_oracle import R,request,event,digest
from scripts.verify_prediction_markets import fixture
from scripts.measure_ai_predictive_modeling import peak_memory
def workload(trades,accounts,settle=False):
    q=request();q['market']['liquidity']='10';q['accounts']=[dict(id='a'+str(i),initial_credit='1000') for i in range(accounts)];q['events']=[];start=datetime(2025,1,2,tzinfo=timezone.utc)
    for i in range(trades):
        actor='a'+str(i%accounts);qid='q'+str(i);quote=dict(id='quote'+str(i),type='quote',at=(start+timedelta(seconds=2*i)).isoformat().replace('+00:00','Z'),actor=actor,quote_id=qid,outcome='YES' if i%2==0 else 'NO',delta='1');execute=dict(id='execute'+str(i),type='execute',at=(start+timedelta(seconds=2*i+1)).isoformat().replace('+00:00','Z'),actor=actor,quote_id=qid);q['events'] += [quote,execute]
    if settle:q['events'] += [event('close','close',10,actor='admin'),event('resolve','resolve',11,actor='admin',outcome='YES')]
    return q
def run():
    results=[]
    for name,q in [('small',fixture()['cases']['buy-one']['input']),('medium',workload(32,4)),('dense',workload(256,8)),('settlement',workload(64,4,True))]:
        times=[]
        for _ in range(3):
            start=time.perf_counter();r=read(q);times.append(time.perf_counter()-start)
        tracemalloc.start();read(q);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        inp=R/('data/prediction-markets-'+name+'-benchmark-input.json');inp.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8',newline='\n')
        start=time.perf_counter();cp=subprocess.run([sys.executable,'-m','future','prediction-markets',str(inp)],cwd=R,capture_output=True);elapsed=time.perf_counter()-start;assert cp.returncode==0,cp.stderr
        results.append(dict(id=name,accounts=len(q['accounts']),events=len(q['events']),executed_trades=r['final']['executed_trades'],settlements=r['final']['settlements'],input_sha256=digest(q),budget=r['budget'],seconds=times,median_seconds=statistics.median(times),cli_seconds=elapsed,python_traced_peak_bytes=peak,under_proposed_five_seconds=max(times+[elapsed])<=5))
    peak=peak_memory();out=dict(measured=True,environment=dict(python=sys.version,platform=platform.platform()),profile_sha256=r['profile']['sha256'],code_sha256=r['code_sha256'],protocol='Three untraced complete in-process reports; separate tracemalloc report; one complete CLI including imports,registry andserialization. Native peak covers whole helper,imports,all workloads andtracing,not CLI-child/per-workload peak.',process_peak_working_set_bytes=peak,under_proposed_128_MiB=peak is not None and peak<=128*1024**2,results=results,scope='Recorded local self-authored synthetic play-credit workloads; no real money,traders or empirical market accuracy.')
    (R/'data/prediction-markets-resource-measurements.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print([(r['id'],r['median_seconds'],r['cli_seconds']) for r in results],peak)
if __name__=='__main__':run()
