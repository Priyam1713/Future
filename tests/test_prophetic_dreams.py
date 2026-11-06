import copy
from datetime import datetime,timedelta
import json
from pathlib import Path
import tempfile
import unittest
from future import prophetic_dreams as p

F=json.loads(Path('tests/fixtures/prophetic_dreams_reference_v1.json').read_text(encoding='utf-8'))
def tm(day=7,hour=6,minute=0):return f'2026-11-{day:02d}T{hour:02d}:{minute:02d}:00+05:30'
def action(l,name,payload=None,at=None,actor=None,check=True):
    if at is None:at=(p.timestamp(l['events'][-1]['at'] if l['events'] else l['plan']['created_at'])+timedelta(minutes=1)).isoformat()
    if actor is None:actor=l['plan']['participant'] if name in ('record','lock_entry','amend') else l['plan']['universe']['collector'] if name=='event' else l['plan']['coordinator']
    out=p.apply(l,name,actor,at,payload or {})
    if check:assert out['events'][-1]['accepted'],out['events'][-1]
    return out
def build(stage='reported',plan=None,entries=None,events=None):
    plan=copy.deepcopy(plan or F['plan']);entries=copy.deepcopy(entries if entries is not None else F['entries']);events=copy.deepcopy(events if events is not None else F['events'])
    l=p.create(plan)
    for i,e in enumerate(entries):
        l=action(l,'record',dict(entry=e),at=e['first_record_at'])
        lock=(p.timestamp(e['first_record_at'])+timedelta(minutes=2)).isoformat()
        l=action(l,'lock_entry',dict(entry_id=e['id'],digest=p.original_lock(e,lock)),at=lock)
    l=action(l,'slot_status',dict(slot_id='s3',status='nonrecall',reason='No dream recalled.'),at=tm(7,9))
    for i,e in enumerate(events):l=action(l,'event',dict(event=e),at=tm(9,16,i))
    if stage=='recording':return l
    l=action(l,'seal',at=tm(9,17))
    if stage=='sealed':return l
    rows=p.pairs(l)
    for i,j in enumerate(plan['judges']):
        l=action(l,'expose',dict(judge_id=j,knowledge='unaware'),at=tm(9,18,i*2))
        if stage=='exposed':return l
        eligible=[r['pair_id'] for r in rows if r['eligible']]
        ratings={r['pair_id']:('match' if r['pair_id']==eligible[i%len(eligible)] else 'nonmatch') if r['eligible'] else 'protocol_invalid' for r in rows} if eligible else {r['pair_id']:'unscorable' for r in rows}
        l=action(l,'rate',dict(ratings=ratings,notes='  Original human-declared fixture ratings\r\n'),at=tm(9,18,i*2+1),actor=j)
    l=action(l,'lock_judges',dict(digest=p.judge_lock(l)),at=tm(9,18,30))
    if stage=='judge_locked':return l
    l=action(l,'reveal',at=tm(9,19))
    if stage=='revealed':return l
    return action(l,'finish',at=tm(9,20))

class PropheticDreamsTests(unittest.TestCase):
    def test_lifecycle(self):self.assertEqual(p.verify(build())['state'],'reported')
    def test_prospective_lock(self):
        l=build();rows=p.pairs(l);self.assertEqual(sum(r['eligible'] for r in rows),2)
        self.assertEqual(rows[0]['chronology'],'future_event')
    def test_known_original_hashes(self):
        for e,h in zip(F['entries'],F['original_sha256']):self.assertEqual(p.version_hash(e),h)
    def test_known_lock_hashes(self):
        for e,h in zip(F['entries'],F['lock_sha256']):self.assertEqual(p.original_lock(e,(p.timestamp(e['first_record_at'])+timedelta(minutes=2)).isoformat()),h)
    def test_occurrence_vs_record(self):
        r=p.report(build());self.assertIsNone(r['original_entries']['dream1']['original']['occurrence']);self.assertIsNotNone(r['original_entries']['dream1']['original']['first_record_at'])
    def test_occurrence_vs_discovery(self):self.assertEqual(p.pairs(build())[1]['chronology'],'record_after_event_before_discovery')
    def test_version_mutation(self):
        l=build();l['events'][0]['payload']['entry']['text']+='x'
        with self.assertRaises(ValueError):p.verify(l)
    def test_after_outcome_edit(self):
        l=build();ctx=p.verify(l);parent=ctx['entries']['dream1']['versions'][-1]['sha256'];before=p.pairs(l)
        l=action(l,'amend',dict(entry_id='dream1',parent_sha256=parent,text='Much more specific after event.',reason='Later clarification',outcome_known=True))
        r=p.report(l);self.assertEqual(p.pairs(l),before);self.assertEqual(len(r['original_entries']['dream1']['versions']),2)
        self.assertEqual(r['original_entries']['dream1']['original']['text'],F['entries'][0]['text'])
    def test_amend_wrong_parent(self):
        l=action(build(),'amend',dict(entry_id='dream1',parent_sha256='0'*64,text='x',reason='correction',outcome_known=True),check=False)
        self.assertFalse(l['events'][-1]['accepted'])
    def test_window_boundaries(self):
        win=dict(start=tm(8,0),end=tm(9,0))
        for time in (tm(8,0),tm(9,0)):self.assertEqual(p.window_status(dict(start=time,end=time,precision='second'),win),'inside')
    def test_uncertain_window(self):self.assertEqual(p.pairs(build())[3]['window_status'],'uncertain')
    def test_unknown_event_time(self):
        es=copy.deepcopy(F['events']);es[0]['occurrence']=None;r=p.report(build(events=es));self.assertEqual(r['pairs'][0]['chronology'],'timing_unknown');self.assertFalse(r['pairs'][0]['eligible'])
    def test_missing_conflicting_time(self):
        es=copy.deepcopy(F['events']);es[0]['discovery_at']=tm(8,0)
        r=p.report(build(events=es));self.assertEqual(r['pairs'][0]['chronology'],'conflicting_time')
    def test_missing_timezone(self):
        l=action(p.create(F['plan']),'seal',at='2026-11-09T17:00:00',check=False);self.assertFalse(l['events'][-1]['accepted'])
    def test_criteria_precommit(self):
        l=build();l['plan']['features'][0]['description']='posthoc'
        with self.assertRaises(ValueError):p.verify(l)
    def test_universe_version(self):
        l=build();l['plan']['universe']['version']=2
        with self.assertRaises(ValueError):p.verify(l)
    def test_wrong_universe_hash(self):
        plan=copy.deepcopy(F['plan']);plan['universe_sha256']='0'*64
        with self.assertRaises(ValueError):p.create(plan)
    def test_nonmatches_denominator(self):
        r=p.report(build());self.assertEqual(r['pair_counts'],dict(total=8,eligible=2,excluded=6,duplicates=2,common=2));self.assertEqual(r['slot_counts']['nonrecall'],1);self.assertEqual(r['slot_counts']['unsubmitted'],1)
        self.assertEqual(r['per_judge_category_counts']['j1']['nonmatch'],1)
        self.assertEqual(sum(r['per_judge_all_pair_category_counts']['j1'].values()),8)
    def test_duplicate_common_event(self):
        rows=p.pairs(build());self.assertEqual(sum(x['duplicate'] for x in rows),2);self.assertEqual(sum(x['common'] for x in rows),2)
    def test_one_to_many(self):
        rows=p.pairs(build());self.assertEqual([x['event_id'] for x in rows if x['dream_id']=='dream1'],['e1','e2','e3','e4'])
    def test_judge_blinding(self):
        v=p.judge_packet(build('exposed'),'j1');self.assertTrue(p.validate_packet(v));raw=p.canonical(v).decode()
        for word in ('dedup_group','eligible','discovery_at','publication_at','path','outcome_known','answer_flag'):self.assertNotIn('"'+word+'"',raw)
        self.assertEqual(len(v['pairs']),8);self.assertEqual(v['dreams'][0]['text'],F['entries'][0]['text'])
    def test_judge_disagreement(self):self.assertEqual(len(p.report(build())['judge_disagreements']),2)
    def test_feedback_contamination(self):
        l=build();before=p.pairs(l);l=action(l,'commentary',dict(kind='feedback',text='Later feedback',event_reference='new external event'))
        l=action(l,'commentary',dict(kind='association',text='Later association',event_reference='outside the fixed universe'))
        r=p.report(l);self.assertEqual(len(r['post_reveal_commentary']),2);self.assertEqual(p.pairs(l),before)
    def test_zero_information(self):
        es=copy.deepcopy(F['entries']);es[0]['text']='';es[0]['details']={};r=p.report(build(entries=es))
        self.assertEqual(r['original_entries']['dream1']['original']['text'],'');self.assertNotIn('p_value',r);self.assertNotIn('chance_reference',r)
    def test_replay_rights(self):
        l=build();self.assertEqual(p.canonical(p.report(l)),p.canonical(p.report(copy.deepcopy(l))))
    def test_source_isolation(self):
        q=dict(schema_version=1,profile=p.PROFILE,task='reference',ids=['martinique','lecture-nonmatch','wargo-envelope']);r=p.read(q)
        self.assertEqual(r['records'][0]['claim_number'],4000);self.assertEqual(r['records'][0]['newspaper_number'],40000);self.assertFalse(r['records'][0]['prospective_timestamp_verified']);self.assertEqual(r['records'][1]['author_assessment'],'None');self.assertFalse(r['records'][2]['same_endpoint'])
    def test_late_entry(self):
        es=copy.deepcopy(F['entries']);es[0]['first_record_at']=tm(7,7,1)
        r=p.report(build(entries=es));self.assertEqual(r['slot_counts']['late'],1);self.assertIn('late_entry',r['pairs'][0]['exclusion_reasons'])
    def test_withdrawn_entry(self):
        l=build('recording');l=action(l,'slot_status',dict(slot_id='s1',status='withdrawn',reason='Withdrawal'),at=tm(9,16,20));l=action(l,'seal',at=tm(9,17))
        self.assertIn('slot_withdrawn',p.pairs(l)[0]['exclusion_reasons'])
    def test_coverage_omissions(self):
        es=copy.deepcopy(F['events']);es[0]['coverage']='known_omissions';self.assertFalse(p.report(build(events=es))['collection_complete'])
    def test_complete_events_required(self):
        l=build('recording',events=F['events'][:-1]);l=action(l,'seal',at=tm(9,17),check=False);self.assertFalse(l['events'][-1]['accepted'])
    def test_premature_reveal(self):
        l=action(build('sealed'),'reveal',check=False);self.assertFalse(l['events'][-1]['accepted']);self.assertEqual(len(p.report(l)['rejected_attempts']),1)
    def test_after_reveal_rating_rejected(self):
        l=build();old=p.verify(l)['ratings']['j1'];l=action(l,'rate',old|dict(at='ignored'),actor='j1',check=False);self.assertFalse(l['events'][-1]['accepted'])
    def test_all_judges_required(self):
        l=build('exposed');self.assertFalse(p.report(l)['declared_blind_judging']);l=action(l,'lock_judges',dict(digest=p.judge_lock(l)),check=False);self.assertFalse(l['events'][-1]['accepted'])
    def test_wrong_local_bytes(self):
        l=build()
        with tempfile.TemporaryDirectory() as tmp:
            for e in F['events']:
                path=Path(tmp,e['evidence']['path']);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(Path(e['evidence']['path']).read_bytes())
            Path(tmp,F['events'][0]['evidence']['path']).write_bytes(b'mutated')
            with self.assertRaises(ValueError):p.verify(l,tmp)
    def test_privacy_gate(self):
        plan=copy.deepcopy(F['plan']);plan['privacy_consent']=False;l=build('exposed',plan=plan)
        with self.assertRaises(ValueError):p.judge_packet(l,'j1')
    def test_exported_bytes(self):
        v=p.judge_packet(build('exposed'),'j1')
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp,'judge');p.export_packet(v,out);self.assertEqual([x.name for x in out.iterdir()],['packet.json']);self.assertEqual(json.loads((out/'packet.json').read_text(encoding='utf-8')),v)
            with self.assertRaises(ValueError):p.export_packet(v,out)
    def test_public_packet_mutation(self):
        v=p.judge_packet(build('exposed'),'j1');v['dreams'][0]['text']+='changed'
        with self.assertRaises(ValueError):p.validate_packet(v)
    def test_known_outcome_capture(self):
        es=copy.deepcopy(F['entries']);es[0]['outcome_known']=True;r=p.report(build(entries=es));self.assertFalse(r['pairs'][0]['eligible']);self.assertEqual(r['pairs'][0]['chronology'],'outcome_known_at_capture')
    def test_publication_endpoint_separate(self):
        plan=copy.deepcopy(F['plan']);plan['window'].update(endpoint='publication',end=tm(9,23));r=p.report(build(plan=plan));self.assertEqual(r['pairs'][1]['chronology'],'record_after_event_before_discovery');self.assertEqual(r['pairs'][1]['eligibility_scope'],'prospective_publication_information')
    def test_invalid_dream_occurrence(self):
        e=copy.deepcopy(F['entries'][0]);e['occurrence']=dict(start=tm(8,0),end=tm(8,0),precision='second')
        l=action(p.create(F['plan']),'record',dict(entry=e),at=tm(7,6,30),check=False);self.assertFalse(l['events'][-1]['accepted'])
    def test_no_amend_original_replacement(self):
        l=build();l=action(l,'record',dict(entry=copy.deepcopy(F['entries'][0])),check=False);self.assertFalse(l['events'][-1]['accepted'])
    def test_unicode_whitespace(self):self.assertEqual(p.report(build())['original_entries']['dream1']['original']['text'],F['entries'][0]['text'])
    def test_combining_and_whitespace_mutations(self):
        for changed in [F['entries'][0]['text'].strip(),F['entries'][0]['text'].replace('Café','Café')]:
            l=build();l['events'][0]['payload']['entry']['text']=changed
            with self.assertRaises(ValueError):p.verify(l)
    def test_posthoc_window_expansion(self):
        l=build();l['plan']['window']['end']=tm(10,0)
        with self.assertRaises(ValueError):p.verify(l)
    def test_aware_judge_unblinded(self):
        l=build('sealed');l=action(l,'expose',dict(judge_id='j1',knowledge='aware'))
        self.assertFalse(p.report(l)['declared_blind_judging'])
    def test_locked_rating_mutation(self):
        l=build();event=next(e for e in l['events'] if e['action']=='rate');event['payload']['ratings']['d1:e1']='nonmatch'
        with self.assertRaises(ValueError):p.verify(l)

def add(name,fn):setattr(PropheticDreamsTests,'test_'+name,fn)
for field in ['answer_flag','caption','filename','private_ratings','event_time']:
    def test(self,field=field):
        v=p.judge_packet(build('exposed'),'j1');v[field]='planted'
        with self.assertRaises(ValueError):p.validate_packet(v)
    add('packet_leak_'+field,test)
for field in ['stopping_rule','pair_policy','duplicate_policy','uncertainty_policy','primary_endpoint','profile_sha256']:
    def test(self,field=field):
        plan=copy.deepcopy(F['plan']);plan[field]='posthoc'
        with self.assertRaises(ValueError):p.create(plan)
    add('invalid_plan_'+field,test)
for field in ['holder','permission','provenance']:
    def test(self,field=field):
        e=copy.deepcopy(F['events'][0]);e['evidence'][field]='';l=action(build('recording',events=[]),'event',dict(event=e),check=False);self.assertFalse(l['events'][-1]['accepted'])
    add('rights_'+field,test)
for field in ['text','first_record_at','details','occurrence']:
    def test(self,field=field):
        l=build();l['events'][0]['payload']['entry'][field]='mutated'
        with self.assertRaises(ValueError):p.verify(l)
    add('mutation_'+field,test)
for state in ['aborted','excluded']:
    def test(self,state=state):
        l=action(p.create(F['plan']),'terminate',dict(status=state,reason='Recorded stop'));self.assertEqual(p.verify(l)['state'],state);l=action(l,'seal',check=False);self.assertFalse(l['events'][-1]['accepted'])
    add('terminal_'+state,test)

if __name__=='__main__':unittest.main()
