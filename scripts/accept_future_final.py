"""Final complete post60 regression: all smoke commands and every verifier script."""
import concurrent.futures,hashlib,json,re,subprocess,sys
from pathlib import Path
from scripts.accept_multiverse_core import execute
from future.scrying import load_input
from future.knowledge import Registry
R=Path(__file__).resolve().parents[1]
def save(p,x):(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def run(resume=False):
    inherited=load_input(R/'data/multiverse-acceptance-checks.json');checks=[]
    if resume:unit=load_input(R/'data/future-final-unit.json')
    else:unit=execute([sys.executable,'-m','unittest','discover','-s','tests']);save('data/future-final-unit.json',unit)
    assert unit['returncode']==0;checks.append(unit)
    smokes=[c['command'] for c in inherited['checks'] if len(c['command'])>2 and c['command'][1]=='-m' and c['command'][2].startswith('scripts.smoke_')]
    verifiers=sorted({'scripts.'+p.stem for p in (R/'scripts').glob('verify_*.py')}|{'scripts.verify_future_interfaces'})
    cmds=smokes+[['python','-m',v] for v in verifiers];assert len(cmds)==len({tuple(c) for c in cmds})
    done={}
    if resume:done={tuple(c['command']):c for c in load_input(R/'data/future-final-acceptance-checks.json')['checks'] if c['returncode']==0}
    ordered={i:done[tuple(c)] for i,c in enumerate(cmds) if tuple(c) in done}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures={pool.submit(execute,c):i for i,c in enumerate(cmds) if i not in ordered}
        for future in concurrent.futures.as_completed(futures):
            i=futures[future];ordered[i]=future.result();print(('PASS ' if ordered[i]['returncode']==0 else 'FAIL ')+' '.join(cmds[i]),flush=True);save('data/future-final-acceptance-checks.json',dict(complete=False,checks=checks+[ordered[i] for i in sorted(ordered)]))
    checks += [ordered[i] for i in range(len(cmds))]
    for cmd in [['python','-m','scripts.audit_dependencies'],['python','-m','pip','check'],['git','diff','--check'],['python','-m','scripts.check_inventory_workbook']]:checks.append(execute(cmd))
    assert all(c['returncode']==0 for c in checks),[c for c in checks if c['returncode']]
    registry=Registry(':memory:');references=[];skipped=[]
    try:
        for path in sorted((R/'knowledge').glob('*sources.json')):
            records=load_input(path)
            if not isinstance(records,list):continue
            for record in records:
                if not isinstance(record,dict) or 'id' not in record:continue
                if record['id']=='chinese-inventory-2-v1':skipped.append(record['id']);continue
                registry.add_source(record);references.append(record)
        for record in references:registry.add_source(record)
        unique=registry.db.execute('SELECT COUNT(*) FROM sources').fetchone()[0]
    finally:registry.close()
    invalid={'data/feng-shui-duplicate-json-input.json','data/feng-shui-nonfinite-input.json'};strict=0
    for folder in ['knowledge','data','tests/fixtures']:
        for path in (R/folder).rglob('*.json'):
            if path.relative_to(R).as_posix() in invalid:
                try:load_input(path)
                except ValueError:continue
                raise AssertionError('Historical malformed JSON no longer rejects')
            load_input(path);strict+=1
    baseline=load_input(R/'data/future-final-preservation-baseline.json');changed=[p for p,h in baseline['pre_final_sha256'].items() if p not in baseline['allowed_existing_edits'] and (not (R/p).is_file() or hashlib.sha256((R/p).read_bytes()).hexdigest()!=h)];assert not changed,changed
    old=json.loads(subprocess.check_output(['git','show',baseline['baseline_commit']+':knowledge/gaps.json'],cwd=R));new=load_input(R/'knowledge/gaps.json');reconciled=set(range(5,16));assert [g for g in old if g['technique_id'] not in reconciled]==[g for g in new if g['technique_id'] not in reconciled]
    assert next(g for g in new if g['technique_id']==5)['status']=='Core v1 Ready — Diagnostic Scope'
    from scripts.build_future_completion_matrix import core_records
    for i,(_,release) in core_records().items():assert next(g for g in new if g['technique_id']==i)['status']==release['status']
    assert len(new)==60 and sum(bool(g['retained']) for g in new)==54 and [g['technique_id'] for g in new if not g['retained']]==[25,27,41,42,47,48]
    tests=int(re.search(r'Ran (\d+) tests',unit['stderr'])[1]);cli=sum(int(re.match(r'(\d+)',c['stdout'])[1]) for c in checks if len(c['command'])>2 and c['command'][2].startswith('scripts.smoke_'));assert (tests,cli,len(verifiers))==(2402,3453,51),(tests,cli,len(verifiers))
    out=dict(passed=True,complete=True,checks=checks,tests=tests,cli_cases=cli,independent_verifiers=len(verifiers),smoke_commands=len(smokes),verifier_commands=verifiers,earlier_verifiers_added=sorted(set(verifiers)-{c['command'][2] for c in inherited['checks'] if len(c['command'])>2 and c['command'][2].startswith('scripts.verify_')}),protected_files=baseline['protected_count'],changed_protected_files=changed,allowed_existing_edits=baseline['allowed_existing_edits'],gap_index_reconciliation=dict(reconciled_ids=sorted(reconciled),other49_entries_unchanged=True,all54_index_statuses_match_releases=True,judgment_certified=False),registry=dict(references_checked_twice=len(references),unique=unique,skipped=skipped),strict_json_files=strict,historical_invalid_json_rejections=sorted(invalid),taxonomy=dict(total=60,retained=54,excluded=[25,27,41,42,47,48]),interface_verification=load_input(R/'data/future-interface-verification.json'),checkout_replays={str(i):load_input(R/('data/'+stem+'-checkout-replay.json')) for i,stem in [(55,'brain-intention'),(56,'causal-ai'),(57,'collective-intelligence'),(58,'prediction-markets'),(59,'chaos-theory'),(60,'multiverse')]},harness_environment=dict(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1'),baseline_commit=baseline['baseline_commit'],metadata_gates_revalidated_after_index_reconciliation=resume)
    save('data/future-final-acceptance-checks.json',out);print(str(tests)+'tests;'+str(cli)+'CLI cases;'+str(len(verifiers))+'verifiers;'+str(baseline['protected_count'])+'protected files unchanged',flush=True)
if __name__=='__main__':run('--resume' in sys.argv)
