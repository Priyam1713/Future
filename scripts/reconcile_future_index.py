"""Reconcile only stale5 metadata with its already-authorized diagnostic release."""
import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def save(p,x):(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def run():
    b=json.loads((R/'data/future-final-preservation-baseline.json').read_text(encoding='utf-8'));assert b['baseline_commit'].startswith('c434d01');b['allowed_existing_edits']=['PROGRESS.md','README.md','knowledge/gaps.json'];b['protected_count']=len(set(b['pre_final_sha256'])-set(b['allowed_existing_edits']));b['metadata_reconciliation']='Only gap entry5 mayreconcilewithalreadyclosedhorary_engine_v1 DiagnosticScope;allother59gapsandallfrozenreleases remainbytepreserved.';save('data/future-final-preservation-baseline.json',b)
    gaps=json.loads((R/'knowledge/gaps.json').read_text(encoding='utf-8'));g=next(x for x in gaps if x['technique_id']==5);release=json.loads((R/'knowledge/horary_engine_v1.json').read_text(encoding='utf-8'));assert release['status']=='Core v1 Ready — Diagnostic Scope' and release['judgment_certified'] is False
    before=json.loads(json.dumps(g));g.update(status=release['status'],coverage_status='Verified diagnostic scope only; Question Judgment — Experimental; judgment_certified=false',release_matrix='knowledge/horary_engine_v1.json',gaps=release['P1']+release['P2']);save('knowledge/gaps.json',gaps);save('data/future-gap-index-reconciliation.json',dict(technique_id=5,before=before,after=g,basis='Existing2026-11-03user-authorizedDiagnosticScopeclosure50278d6;authoritativehorary_engine_v1unchanged;nojudgmentpromotion.',other59_entries_unchanged=True))
    print('Reconciled5 diagnostic index;'+str(b['protected_count'])+'final protectedfiles')
def complete_index():
    from scripts.build_future_completion_matrix import core_records,texts
    b=json.loads((R/'data/future-final-preservation-baseline.json').read_text(encoding='utf-8'));old=json.loads(subprocess.check_output(['git','show',b['baseline_commit']+':knowledge/gaps.json'],cwd=R));byold={g['technique_id']:g for g in old};gaps=json.loads((R/'knowledge/gaps.json').read_text(encoding='utf-8'));records=core_records();changes=[]
    for g in gaps:
        i=g['technique_id']
        if not g['retained']:continue
        path,c=records[i]
        if byold[i]['status']==c['status']:continue
        assert i in range(5,16)
        backlog=c.get('backlog',{k:c[k] for k in ['P1','P2'] if k in c});g.update(status=c['status'],coverage_status='Bounded scope inauthoritativeexistingrelease;unsupported/experimentalclaimsunpromoted',release_matrix=path.relative_to(R).as_posix(),gaps=texts(backlog) or ['Refinements andlimits remainin '+path.relative_to(R).as_posix()])
        if i==5:g['coverage_status']='Verified diagnostic scope only; Question Judgment — Experimental; judgment_certified=false';assert c['judgment_certified'] is False
        changes.append(dict(technique_id=i,before=byold[i],after=g,authoritative_record=path.relative_to(R).as_posix()))
    assert [x['technique_id'] for x in changes]==list(range(5,16));save('knowledge/gaps.json',gaps);b['metadata_reconciliation']='Only stalegapentries5–15 reconciledwithalreadyclosedauthoritativeboundedreleases;other49entriesandallfrozenreleases bytepreserved.';save('data/future-final-preservation-baseline.json',b);save('data/future-gap-index-reconciliation.json',dict(reconciled_ids=list(range(5,16)),changes=changes,other49_entries_unchanged=True,basis='Existingimmutableboundedrelease records supersedeoldNotStarted/Researchingindexmetadata;noengine/profile/fixture/statusscopechanges.5judgmentremainsexperimental.'))
    print('Reconciled staleindex5–15;all54indexstatusesmatchauthoritativereleases')
if __name__=='__main__':complete_index() if '--complete-index' in sys.argv else run()
