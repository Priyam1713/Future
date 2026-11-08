"""Fresh final staged-runtime exports replay every55–60 golden output in both modes."""
import ast,concurrent.futures,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
TECHNIQUES=[(55,'brain_intention','brain-intention'),(56,'causal_ai','causal-ai'),(57,'collective_intelligence','collective-intelligence'),(58,'prediction_markets','prediction-markets'),(59,'chaos_theory','chaos-theory'),(60,'multiverse','multiverse')]
def run():
    tracked=subprocess.check_output(['git','ls-files'],cwd=R,text=True).splitlines();normalized=set();records=[];prefixes=[]
    for i,module,slug in TECHNIQUES:
        manifest=json.loads((R/('data/'+slug+'-cli-replay.json')).read_text(encoding='utf-8'));records += [(i,slug,record) for record in manifest['records']];prefixes.append('data/'+slug+'-cli/')
        tree=ast.parse((R/('scripts/check_'+module+'_checkout.py')).read_text(encoding='utf-8'))
        normalized.update(next(ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='normalized' for t in n.targets)))
    # gaps.json is the mutable completion index, not an input of these runtimes.
    files=sorted(set(p for p in tracked if p!='knowledge/gaps.json' and p.startswith(tuple(['future/','knowledge/']+prefixes)))|normalized);receipts=[]
    snapshot=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
    for setting in ['false','true']:
        with tempfile.TemporaryDirectory(prefix='future-final-checkout-') as directory:
            destination=Path(directory).resolve();assert destination.is_relative_to(Path(tempfile.gettempdir()).resolve())
            subprocess.run(['git','-c','core.autocrlf='+setting,'checkout-index','--prefix='+destination.as_posix()+'/','--stdin'],cwd=R,input=('\n'.join(files)+'\n').encode(),capture_output=True,check=True)
            corpus=[p for p in files if p.startswith(tuple(prefixes))]
            for p in corpus:assert (destination/p).read_bytes()==(R/p).read_bytes(),(setting,p)
            for p in normalized:assert (destination/p).read_bytes().replace(b'\r\n',b'\n')==(R/p).read_bytes().replace(b'\r\n',b'\n'),(setting,p)
            def check(item):
                i,slug,record=item
                for fmt in ['json','markdown']:
                    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1');cp=subprocess.run([sys.executable,'-m','future',slug,str(destination/record['input']),'--format',fmt],cwd=destination,capture_output=True,env=env);assert cp.returncode==record['exit_code'],(setting,i,record['id'],cp.stderr);assert hashlib.sha256(cp.stdout).hexdigest()==record['outputs'][fmt],(setting,i,record['id'],fmt)
                return i,2
            counts={str(i):0 for i,_,_ in TECHNIQUES}
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                for i,count in pool.map(check,records):counts[str(i)]+=count
            assert sum(counts.values())==670;receipts.append(dict(autocrlf=setting,passed=True,actual_cli_replays=sum(counts.values()),by_technique=counts,raw_corpus_files=len(corpus),normalized_commitments=len(normalized)));print(setting+':670actual final-tree raw CLI outputs pass',flush=True)
    out=dict(passed=True,runtime_snapshot_commit=snapshot,exports=receipts,method='Fresh git checkout-index exports ofstagedcurrentruntime,pinnedknowledge andall55–60corpora;actual subprocesses hashrawstdoutwithoutnewline normalization.',scope='Mutablegapsstatusindex excluded;not readbytheseengines. FulllegacyCLIreplay runsseparately infinalacceptance;earliercorecheckoutreceipts retained.',environment=dict(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1'),cli_workers=4)
    (R/'data/future-final-checkout-replay.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':run()
