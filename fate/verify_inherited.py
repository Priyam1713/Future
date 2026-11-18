"""Run inherited CLI/verifier gates without rewriting Workbench release receipts."""
import concurrent.futures
import hashlib
import json
import re
import subprocess
from pathlib import Path
from scripts.accept_multiverse_core import execute

ROOT=Path(__file__).resolve().parents[1]

def main():
    baseline=json.loads((ROOT/'data/future-lab-acceptance-checks.json').read_text())
    protected={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in subprocess.check_output(['git','ls-files','future','knowledge','resources','tests'],text=True,cwd=ROOT).splitlines()}
    commands=[c['command'] for c in baseline['checks'] if len(c['command'])>2 and c['command'][1]=='-m' and c['command'][2].startswith(('scripts.smoke_','scripts.verify_'))]
    checks=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        pending={pool.submit(execute,c):c for c in commands}
        for f in concurrent.futures.as_completed(pending):
            result=f.result();checks.append(result)
            print(('PASS ' if result['returncode']==0 else 'FAIL ')+' '.join(result['command']),flush=True)
            (ROOT/'fate/inherited-cli-acceptance.json').write_text(json.dumps(dict(complete=False,checks=checks),indent=2)+'\n')
    changed=[p for p,h in protected.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    out=dict(complete=True,passed=all(c['returncode']==0 for c in checks) and not changed,cli_cases=sum(int(re.match(r'(\d+)',c['stdout'])[1]) for c in checks if c['command'][2].startswith('scripts.smoke_')),independent_verifiers=sum(c['command'][2].startswith('scripts.verify_') for c in checks),protected_count=len(protected),changed_protected_files=changed,checks=checks)
    out['passed']=out['passed'] and (out['cli_cases'],out['independent_verifiers'])==(3515,52)
    (ROOT/'fate/inherited-cli-acceptance.json').write_text(json.dumps(out,indent=2)+'\n')
    print({k:v for k,v in out.items() if k!='checks'})
    if not out['passed']:raise SystemExit(1)

if __name__=='__main__':main()
