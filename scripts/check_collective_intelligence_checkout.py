"""Actually replay CLI from indexed exports under both Git newline settings."""
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

R=Path(__file__).resolve().parents[1]
def run():
    manifest=json.loads((R/'data/collective-intelligence-cli-replay.json').read_text())
    tracked=subprocess.check_output(['git','ls-files'],cwd=R,text=True).splitlines()
    files=[p for p in tracked if p.startswith(('future/','knowledge/','data/collective-intelligence-cli/'))]
    normalized=['future/collective_intelligence.py','scripts/collective_intelligence_oracle.py','tests/fixtures/collective-intelligence-independent-v1.json']
    files=sorted(set(files+normalized));receipts=[]
    for setting in ['false','true']:
        with tempfile.TemporaryDirectory(prefix='future57-checkout-') as directory:
            destination=Path(directory).resolve();assert destination.is_relative_to(Path(tempfile.gettempdir()).resolve())
            subprocess.run(['git','-c','core.autocrlf='+setting,'checkout-index','--prefix='+destination.as_posix()+'/','--stdin'],cwd=R,input=('\n'.join(files)+'\n').encode(),capture_output=True,check=True)
            corpus=[p for p in files if p.startswith('data/collective-intelligence-cli/')]
            for p in corpus:assert (destination/p).read_bytes()==(R/p).read_bytes(),(setting,p)
            for p in normalized:assert (destination/p).read_bytes().replace(b'\r\n',b'\n')==(R/p).read_bytes().replace(b'\r\n',b'\n'),(setting,p)
            def check(record):
                for fmt in ['json','markdown']:
                    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
                    cp=subprocess.run([sys.executable,'-m','future','collective-intelligence',str(destination/record['input']),'--format',fmt],cwd=destination,capture_output=True,env=env)
                    assert cp.returncode==record['exit_code'],(setting,record['id'],cp.stderr)
                    assert hashlib.sha256(cp.stdout).hexdigest()==record['outputs'][fmt],(setting,record['id'],fmt)
                return 2
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:count=sum(pool.map(check,manifest['records']))
            receipts.append(dict(autocrlf=setting,raw_corpus_files=len(corpus),normalized_commitments=len(normalized),actual_cli_replays=count,passed=True))
            print(setting+': '+str(count)+' exact raw-output CLI replays pass',flush=True)
    out=dict(passed=True,exports=receipts,method='git checkout-index from staged files with core.autocrlf false/true;actual exported CLI executions;stdout bytes SHA256 matches saved JSON/Markdown,without newline normalization',subprocess_environment=dict(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1'),harness_limit='Two parallel CLI processes; limits inherited numerical-library import threads,not the stdlib binary pooling engine.')
    (R/'data/collective-intelligence-checkout-replay.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':run()
