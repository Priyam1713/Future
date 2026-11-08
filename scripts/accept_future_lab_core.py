"""Full inherited acceptance plus Lab checks, without rewriting inherited receipts."""
import concurrent.futures,hashlib,json,re,subprocess,sys
from pathlib import Path
from scripts.accept_multiverse_core import execute
from future.knowledge import Registry
from future.scrying import load_input
R=Path(__file__).resolve().parents[1]
def save(p,x):(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def run(resume=False):
    original=load_input(R/'data/future-final-acceptance-checks.json');baseline=load_input(R/'data/future-lab-preservation-baseline.json')
    if resume:unit=load_input(R/'data/future-lab-unit.json')
    else:unit=execute([sys.executable,'-m','unittest','discover','-s','tests']);save('data/future-lab-unit.json',unit)
    assert unit['returncode']==0;checks=[unit]
    inherited=[c['command'] for c in original['checks'] if len(c['command'])>2 and c['command'][1]=='-m' and c['command'][2].startswith(('scripts.smoke_','scripts.verify_'))]
    assert sum(c[2].startswith('scripts.smoke_') for c in inherited)==54 and sum(c[2].startswith('scripts.verify_') for c in inherited)==51
    cmds=inherited+[['python','-m','scripts.smoke_future_lab_core'],['python','-m','scripts.verify_future_lab']];assert len(cmds)==len({tuple(c) for c in cmds})
    done={}
    if resume:done={tuple(c['command']):c for c in load_input(R/'data/future-lab-acceptance-checks.json')['checks'] if c['returncode']==0}
    ordered={i:done[tuple(c)] for i,c in enumerate(cmds) if tuple(c) in done}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures={pool.submit(execute,c):i for i,c in enumerate(cmds) if i not in ordered}
        for future in concurrent.futures.as_completed(futures):
            i=futures[future];ordered[i]=future.result();print(('PASS ' if ordered[i]['returncode']==0 else 'FAIL ')+' '.join(cmds[i]),flush=True);save('data/future-lab-acceptance-checks.json',dict(complete=False,checks=checks+[ordered[i] for i in sorted(ordered)]))
    checks += [ordered[i] for i in range(len(cmds))]
    for cmd in [['python','-m','scripts.audit_dependencies'],['python','-m','pip','check'],['git','diff','--check'],['python','-m','scripts.check_inventory_workbook']]:checks.append(execute(cmd))
    assert all(c['returncode']==0 for c in checks),[c for c in checks if c['returncode']]
    changed=[p for p,h in baseline['pre_lab_sha256'].items() if p not in baseline['allowed_existing_edits'] and (not (R/p).is_file() or hashlib.sha256((R/p).read_bytes()).hexdigest()!=h)];assert not changed,changed
    references=[];skipped=[];registry=Registry(':memory:')
    try:
        for path in sorted((R/'knowledge').glob('*sources.json')):
            records=load_input(path)
            if not isinstance(records,list):continue
            for r in records:
                if not isinstance(r,dict) or 'id' not in r:continue
                if r['id']=='chinese-inventory-2-v1':skipped.append(r['id']);continue
                registry.add_source(r);references.append(r)
        for r in references:registry.add_source(r)
        unique=registry.db.execute('SELECT COUNT(*) FROM sources').fetchone()[0]
    finally:registry.close()
    strict=0;invalid={'data/feng-shui-duplicate-json-input.json','data/feng-shui-nonfinite-input.json'}
    for folder in ['knowledge','data','tests/fixtures']:
        for path in (R/folder).rglob('*.json'):
            if path.relative_to(R).as_posix() in invalid:
                try:load_input(path)
                except ValueError:continue
                raise AssertionError('Historical malformed JSON no longer rejects')
            load_input(path);strict+=1
    tests=int(re.search(r'Ran (\d+) tests',unit['stderr'])[1]);cli=sum(int(re.match(r'(\d+)',c['stdout'])[1]) for c in checks if len(c['command'])>2 and c['command'][2].startswith('scripts.smoke_'));verifiers=sum(len(c['command'])>2 and c['command'][2].startswith('scripts.verify_') for c in checks);assert (tests,cli,verifiers)==(2522,3515,52),(tests,cli,verifiers)
    assert subprocess.check_output(['git','cat-file','-t','core-v1.0.0'],cwd=R,text=True).strip()=='tag';target=subprocess.check_output(['git','rev-parse','core-v1.0.0^{}'],cwd=R,text=True).strip();assert target==baseline['baseline_commit']
    from future.lab.registry import registry as capabilities
    from future.lab.common import REGISTRY_HASH,PROFILE_HASH,code_sha,digest
    caps=capabilities();assert len(caps['entries'])==54 and caps['excluded_ids']==[25,27,41,42,47,48]
    labcode=digest({p.relative_to(R).as_posix():code_sha(p.relative_to(R).as_posix()) for p in sorted((R/'future/lab').glob('*.py'))});perf=load_input(R/'data/future-lab-resource-measurements.json');assert perf['measured'] and perf['lab_code_sha256']==labcode
    demo=load_input(R/'data/future-lab-experiment-demo.json');assert demo['synthetic'] and demo['research_report']['coverage']['matched']==2 and demo['research_report']['model']['brier']['exact']=='17/50'
    out=dict(passed=True,complete=True,checks=checks,tests=tests,inherited_tests=2402,new_tests=tests-2402,cli_cases=cli,inherited_cli_cases=3453,new_cli_cases=cli-3453,independent_verifiers=verifiers,inherited_verifiers=51,protected_files=baseline['protected_count'],changed_protected_files=changed,allowed_existing_edits=baseline['allowed_existing_edits'],registry=dict(references_checked_twice=len(references),unique=unique,skipped=skipped),capability_registry=dict(entries=54,registry_sha256=REGISTRY_HASH,profile_sha256=PROFILE_HASH,excluded_ids=caps['excluded_ids']),strict_json_files=strict,historical_invalid_json_rejections=sorted(invalid),milestone_tag=dict(name='core-v1.0.0',kind='annotated',object_id=subprocess.check_output(['git','rev-parse','core-v1.0.0'],cwd=R,text=True).strip(),target=target),lab_code_sha256=labcode,verification=load_input(R/'data/future-lab-verification.json'),cli_replay=load_input(R/'data/future-lab-cli-replay.json'),performance=perf,demo_sha256=demo['demo_sha256'],scope='All inherited engines/releases/profile/fixtures/resources preserved. Lab software verification andsynthetic demonstration are not empirical superiority.')
    save('data/future-lab-acceptance-checks.json',out);print(str(tests)+'tests;'+str(cli)+'CLI cases;'+str(verifiers)+'verifiers;'+str(baseline['protected_count'])+'protected files unchanged',flush=True)
if __name__=='__main__':run('--resume' in sys.argv)
