"""Explicit single-dream/event record review with native chronology and locks."""
import hashlib
from future import prophetic_dreams as engine
ACTIONS=['record','lock_entry','event','seal','expose','rate','lock_judges','reveal','finish']

def build(a):
    if a['permission']!='yes':raise ValueError('Permission to retain the dream and evidence is required')
    raw=a['evidence'].encode('utf-8');sha=hashlib.sha256(raw).hexdigest()
    path=engine.ROOT/'tmp/workbench-evidence'/(sha+'.txt');path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    universe=dict(id='events',version=1,event_ids=['event1'],collector=a['collector'],collection_rule=a['rule'],collection_window=dict(start=a['collection_start'],end=a['collection_end']))
    plan=dict(schema_version=1,profile=engine.PROFILE,profile_sha256=engine.PROFILE_HASH,study_id=a['study'],participant=a['participant'],coordinator=a['coordinator'],origin='human',created_at=a['created'],slots=[dict(id='slot1',open_at=a['slot_open'],due_at=a['slot_due'])],universe=universe,universe_sha256=engine.digest(universe),window=dict(start=a['window_start'],end=a['window_end'],boundary='closed',endpoint='occurrence'),features=[dict(id='feature1',description=a['feature'])],judges=[a['judge']],blinding='descriptive_unblinded',privacy_consent=True,**dict(engine.DATA['plan_constants']))
    ledger=engine.create(plan)
    entry=dict(id='dream1',slot_id='slot1',participant=a['participant'],occurrence=None,first_record_at=a['record_at'],text=a['narrative'],details={'feature1':a['detail']},outcome_known=a['known']=='yes',attachments=[],privacy_consent=True,witness='none')
    event=dict(id='event1',universe_id='events',universe_version=1,dedup_group='event1',text=a['event_text'],occurrence=dict(start=a['event_start'],end=a['event_end'],precision='reported_interval'),publication_at=None,discovery_at=a['discovery'],common=a['common']=='yes',coverage=a['coverage'],conflicts=[],evidence=dict(path=path.relative_to(engine.ROOT).as_posix(),sha256=sha,holder=a['holder'],permission='User declares permission for retained local evidence',provenance=a['source']))
    for action in ACTIONS:
        actor=a['participant'] if action in ('record','lock_entry') else a['collector'] if action=='event' else a['judge'] if action=='rate' else a['coordinator']
        payload=dict(entry=entry) if action=='record' else dict(entry_id='dream1',digest=engine.original_lock(entry,a['lock_entry_at'])) if action=='lock_entry' else dict(event=event) if action=='event' else dict(judge_id=a['judge'],knowledge='aware') if action=='expose' else dict(ratings={row['pair_id']:a['rating'] for row in engine.pairs(ledger)},notes=a['reason']) if action=='rate' else dict(digest=engine.judge_lock(ledger)) if action=='lock_judges' else {}
        ledger=engine.apply(ledger,action,actor,a[action+'_at'],payload)
        if not ledger['events'][-1]['accepted']:raise ValueError(ledger['events'][-1]['error'])
    return dict(technique_id=44,operation='prophetic-dreams',input=dict(schema_version=1,profile=engine.PROFILE,task='report',ledger=ledger))
