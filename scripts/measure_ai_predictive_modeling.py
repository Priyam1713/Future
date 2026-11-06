"""Explicit benchmark acquisition of local resource evidence, separate from replay."""
import ctypes
import gc
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import threading
import time

ROOT=Path(__file__).resolve().parents[1]


def peak_memory(process=None):
    if os.name=='nt':
        from ctypes import wintypes as w
        class Counters(ctypes.Structure):
            _fields_=[('cb',w.DWORD),('PageFaultCount',w.DWORD)]+[(k,ctypes.c_size_t) for k in
                ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
        p=ctypes.WinDLL('psapi');k=ctypes.WinDLL('kernel32');k.GetCurrentProcess.restype=w.HANDLE
        p.GetProcessMemoryInfo.argtypes=[w.HANDLE,ctypes.POINTER(Counters),w.DWORD]
        c=Counters();c.cb=ctypes.sizeof(c)
        handle=k.GetCurrentProcess() if process is None else w.HANDLE(int(process._handle))
        return int(c.PeakWorkingSetSize) if p.GetProcessMemoryInfo(handle,ctypes.byref(c),c.cb) else None
    if process is not None:
        path=Path('/proc')/str(process.pid)/'status'
        if path.exists():
            for line in path.read_text().splitlines():
                if line.startswith('VmHWM:'):return int(line.split()[1])*1024
        return None
    import resource
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)*(1 if sys.platform=='darwin' else 1024)


def available_memory():
    if os.name!='nt':return dict(method='not measured on this platform',total=None,available=None)
    class Memory(ctypes.Structure):
        _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(k,ctypes.c_ulonglong) for k in ('total','available','total_page','available_page','total_virtual','available_virtual','extended')]
    m=Memory();m.length=ctypes.sizeof(m)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return dict(method='Windows GlobalMemoryStatusEx',total=int(m.total),available=int(m.available))


def run():
    from future import ai_predictive_modeling as e
    q=dict(schema_version=1,task='benchmark',profile=e.DATA['id'],profile_version=1)
    start=time.perf_counter();r=e.read(q);cold=time.perf_counter()-start
    times=[]
    for _ in range(3):
        start=time.perf_counter();warm=e.read(q);times.append(time.perf_counter()-start)
        assert warm==r;del warm;gc.collect()
    start=time.perf_counter();json_text=json.dumps(r,ensure_ascii=False,indent=2);md=e.markdown(r);serialization=time.perf_counter()-start
    del json_text,md;gc.collect()
    helper_peak=peak_memory()
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'request.json');path.write_text(json.dumps(q),encoding='utf-8')
        cmd=[sys.executable,'-m','future','ai-predictive-modeling',str(path)]
        start=time.perf_counter();cp=subprocess.Popen(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        captured={}
        def collect():captured['stdout'],captured['stderr']=cp.communicate()
        collector=threading.Thread(target=collect);collector.start();peaks=[]
        while collector.is_alive():
            value=peak_memory(cp)
            if value is not None:peaks.append(value)
            time.sleep(.02)
        collector.join();cli_wall=time.perf_counter()-start
        assert cp.returncode==0,captured['stderr']
        assert json.loads(captured['stdout'].decode('utf-8'))==r
    record=dict(profile_sha256=e.PROFILE_HASH,code_sha256=hashlib.sha256((ROOT/'future/ai_predictive_modeling.py').read_bytes()).hexdigest(),
        date='2026-11-07',cold_model_seconds=cold,warm_model_seconds=statistics.median(times),warm_model_repeats_seconds=times,
        cold_definition='First core read(benchmark) in this fresh measurement process after imports;OS caches not flushed.',
        warm_definition='Median of3repeat core read(benchmark) calls in same process;each performs every model/fold again,no forecast cache.',
        total_cli_wall_seconds=cli_wall,cli_definition='Fresh python -m future process,including interpreter/imports,core evaluation,JSON serialization and stdout capture;not a machine-cold disk-cache claim.',
        json_plus_markdown_serialization_seconds=serialization,helper_peak_process_bytes=helper_peak,
        cli_peak_process_bytes=max(peaks) if peaks else None,peak_process_bytes=max([v for v in [helper_peak,*peaks] if v is not None]),
        memory_method='Windows GetProcessMemoryInfo native peak working set for helper and20ms CLI samples;Linux VmHWM/resource fallback. Native peaks retain prior spikes;CLI last-exit interval can be missed.',
        physical_memory=available_memory(),python=platform.python_version(),platform=platform.platform(),processor=platform.processor(),logical_cpus=os.cpu_count(),
        model_execution_threads=1,thread_policy='Single calling Python thread;no BLAS/neural/GPU model execution. Parent monitor thread only collects CLI output.',gpu_used=False,
        series=1,origins=50,horizons=12,candidates=7,forecast_cells=4200,stdout_sha256=hashlib.sha256(captured['stdout']).hexdigest(),
        environment_versions={'python':platform.python_version(),'numeric':'stdlib Fraction/Decimal','model_dependencies_added':[]},
        target=dict(warm_seconds=10,peak_bytes=512*1024*1024),limits='Measured on this machine only;timings/resource costs are frozen evidence,not universal performance guarantees.')
    record['target_passed']=record['warm_model_seconds']<10 and record['peak_process_bytes']<512*1024*1024
    (ROOT/'data/ai-predictive-modeling-resource-measurements.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    q['resource_evidence']=dict(record=record,sha256=e.digest(record))
    report=e.read(q)
    for path,value in [('data/ai-predictive-modeling-noaa-benchmark-input.json',q),('data/ai-predictive-modeling-noaa-benchmark.json',report)]:
        (ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'data/ai-predictive-modeling-noaa-benchmark.md').write_text(e.markdown(report),encoding='utf-8')
    # Compact companion is directly reviewable without hiding the complete ledger.
    summary=dict(profile=report['profile'],dataset_sha256=e.DATA['dataset_sha256'],protocol_sha256=e.DATA['protocol_sha256'],
                 selection=report['result']['evaluation']['selection'],summary=report['result']['evaluation']['summary'],
                 resource_evidence=q['resource_evidence'],full_report='data/ai-predictive-modeling-noaa-benchmark.json')
    (ROOT/'data/ai-predictive-modeling-benchmark-summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:record[k] for k in ['cold_model_seconds','warm_model_seconds','total_cli_wall_seconds','peak_process_bytes','target_passed']},indent=2))


if __name__=='__main__':run()
