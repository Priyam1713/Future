"""Run inherited acceptance in isolation; write ONLY Workbench receipts."""
import concurrent.futures, hashlib, json, re, subprocess, sys
from pathlib import Path
from scripts.accept_multiverse_core import execute
R=Path(__file__).resolve().parents[1]
def run():
    baseline=json.loads((R/'data/future-lab-acceptance-checks.json').read_text(encoding='utf-8'))
    protected={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in subprocess.check_output(['git','ls-files'],cwd=R,text=True).splitlines() if p not in ['README.md','PROGRESS.md','.gitignore'] and not p.startswith('workbench/')}
    cmds=[c['command'] for c in baseline['checks'] if len(c['command'])>2 and c['command'][1]=='-m' and c['command'][2].startswith(('scripts.smoke_','scripts.verify_'))]
    checks=[];unit=execute([sys.executable,'-m','unittest','discover','-s','tests']);checks.append(unit);print('Inherited unit suite: '+str(unit['returncode']),flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        pending={pool.submit(execute,c):c for c in cmds}
        for f in concurrent.futures.as_completed(pending):
            r=f.result();checks.append(r);print(('PASS ' if r['returncode']==0 else 'FAIL ')+' '.join(pending[f]),flush=True)
            (R/'workbench/inherited-acceptance.json').write_text(json.dumps(dict(complete=False,checks=checks),indent=2)+'\n',encoding='utf-8')
    changed=[p for p,h in protected.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
    count=int(re.search(r'Ran (\d+) tests',unit['stderr'])[1]);cli=sum(int(re.match(r'(\d+)',c['stdout'])[1]) for c in checks if len(c['command'])>2 and c['command'][2].startswith('scripts.smoke_'));verifiers=sum(len(c['command'])>2 and c['command'][2].startswith('scripts.verify_') for c in checks)
    out=dict(complete=True,passed=all(c['returncode']==0 for c in checks) and not changed and (count,cli,verifiers)==(2522,3515,52),tests=count,cli_cases=cli,independent_verifiers=verifiers,protected_count=len(protected),changed_protected_files=changed,checks=checks)
    (R/'workbench/inherited-acceptance.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print({k:v for k,v in out.items() if k!='checks'},flush=True)
    if not out['passed']:raise SystemExit(1)
if __name__=='__main__':run()
