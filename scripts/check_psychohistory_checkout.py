"""Actually replay CLI from indexed exports under both Git newline settings."""
import concurrent.futures
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

R=Path(__file__).resolve().parents[1]
def run():
    manifest=json.loads((R/'data/psychohistory-cli-replay.json').read_text())
    tracked=subprocess.check_output(['git','ls-files'],cwd=R,text=True).splitlines()
    files=[p for p in tracked if p.startswith(('future/','knowledge/','data/psychohistory-cli/'))]
    normalized=['future/psychohistory.py','scripts/psychohistory_oracle.py','scripts/freeze_psychohistory_boundary_fixtures.py','tests/fixtures/psychohistory-independent-v1.json','tests/fixtures/psychohistory-boundaries-v1.json']
    files=sorted(set(files+normalized));receipts=[]
    for setting in ['false','true']:
        with tempfile.TemporaryDirectory(prefix='future52-checkout-') as directory:
            destination=Path(directory).resolve();assert destination.is_relative_to(Path(tempfile.gettempdir()).resolve())
            subprocess.run(['git','-c','core.autocrlf='+setting,'checkout-index','--prefix='+destination.as_posix()+'/','--stdin'],cwd=R,input=('\n'.join(files)+'\n').encode(),capture_output=True,check=True)
            corpus=[p for p in files if p.startswith('data/psychohistory-cli/')]
            for p in corpus:assert (destination/p).read_bytes()==(R/p).read_bytes(),(setting,p)
            for p in normalized:assert (destination/p).read_bytes().replace(b'\r\n',b'\n')==(R/p).read_bytes().replace(b'\r\n',b'\n'),(setting,p)
            def check(record):
                for fmt in ['json','markdown']:
                    cp=subprocess.run([sys.executable,'-m','future','psychohistory',str(destination/record['input']),'--format',fmt],cwd=destination,capture_output=True)
                    assert cp.returncode==record['exit_code'],(setting,record['id'],cp.stderr)
                    assert hashlib.sha256(cp.stdout).hexdigest()==record['outputs'][fmt],(setting,record['id'],fmt)
                return 2
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:count=sum(pool.map(check,manifest['records']))
            receipts.append(dict(autocrlf=setting,raw_corpus_files=len(corpus),normalized_commitments=len(normalized),actual_cli_replays=count,passed=True))
            print(setting+': '+str(count)+' exact raw-output CLI replays pass',flush=True)
    out=dict(passed=True,exports=receipts,method='git checkout-index from staged files with core.autocrlf false/true;actual exported CLI executions;stdout bytes SHA256 matches saved JSON/Markdown,without newline normalization')
    (R/'data/psychohistory-checkout-replay.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':run()
