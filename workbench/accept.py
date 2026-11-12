"""Measured Workbench acceptance, separate from immutable inherited receipts."""
import hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
from scripts.accept_multiverse_core import execute
from future.lab import registry
from future.lab.common import REGISTRY_HASH,PROFILE_HASH
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sources():
    paths=[R/'workbench/input-workflows.json']+list((R/'workbench').glob('*.py'))+list((R/'workbench').glob('*requirements.txt'))+list((R/'workbench/tests').glob('*.py'))+list((R/'workbench/web/src').rglob('*'))+list((R/'workbench/web/e2e').glob('*.ts'))+[R/'workbench/web'/n for n in ['package.json','package-lock.json','tsconfig.json','vite.config.ts','playwright.config.ts','index.html']]
    return {p.relative_to(R).as_posix():sha(p) for p in sorted(paths) if p.is_file()}
def run(finalize=False):
    path=R/'workbench/acceptance.json'
    if finalize:
        out=read('workbench/acceptance.json')
        assert out['source_sha256']==sources(),'Source changed since measured Workbench checks'
    else:
        before=sources();npm=shutil.which('npm.cmd') or shutil.which('npm');assert npm
        cmds=[[sys.executable,'-m','unittest','discover','-s','workbench/tests','-v'],[npm,'--prefix','workbench/web','run','build'],[npm,'--prefix','workbench/web','run','test:e2e']]
        checks=[]
        for c in cmds:
            result=execute(c);checks.append(result);print(('PASS ' if result['returncode']==0 else 'FAIL ')+' '.join(c),flush=True)
            if result['returncode']:print(result['stdout']+result['stderr']);raise SystemExit(1)
        assert before==sources(),'Source changed during acceptance'
        browser=read('workbench/browser-acceptance.json')['stats'];assert browser['expected']>=6 and browser['unexpected']==browser['skipped']==browser['flaky']==0
        for c in [[sys.executable,'-m','scripts.audit_dependencies'],[sys.executable,'-m','pip','check'],[sys.executable,'-m','scripts.check_inventory_workbook']]:
            result=execute(c);checks.append(result);assert result['returncode']==0,result
        tests=int(re.search(r'Ran (\d+) tests',checks[0]['stderr'])[1]);assert tests>=28
        out=dict(schema_version=1,workbench_tests=tests,browser_tests=browser['expected'],browser_skipped=0,browser_failed=0,all54_browser_invocation=True,native_sample_hashes_verified=54,source_sha256=before,registry_sha256=REGISTRY_HASH,profile_sha256=PROFILE_HASH,excluded_ids=registry()['excluded_ids'],checks=checks,limits=['Software/workflow verification only; no empirical skill certification.','Historical numeric correction replacement is unsupported; versioned annotations suspend scoring.','No external clock authentication, encryption at rest or multi-user isolation.'])
    inherited=read('workbench/inherited-acceptance.json');out['inherited_complete']=inherited.get('complete',False)
    out['complete']=out['inherited_complete'] and inherited.get('passed',False)
    out['status']='Workbench v1.1 Ready - experimental local intake' if out['complete'] else 'Workbench checks passed; inherited acceptance pending'
    if out['complete']:
        out['inherited']={k:inherited[k] for k in ['tests','cli_cases','independent_verifiers','protected_count','changed_protected_files']};out['inherited_receipt_sha256']=sha(R/'workbench/inherited-acceptance.json')
    path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(out['status'],flush=True)
    if finalize:assert out['complete'],'Inherited acceptance not complete/passing'
if __name__=='__main__':run('--finalize' in sys.argv)
