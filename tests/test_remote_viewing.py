import base64
import copy
import itertools
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zlib

from future import remote_viewing as r

FIXTURE=json.loads(Path('tests/fixtures/remote_viewing_reference_v1.json').read_text(encoding='utf-8'))
KNOWN=FIXTURE['known_answer']


def fresh(**changes):
    p=copy.deepcopy(KNOWN['plan']);p.update(changes)
    return r.create(p,seed=KNOWN['seed'] if p['assignment_policy']=='simulated_seed' else None,target_id='t1' if p['assignment_policy']=='manual' else None)


def step(t,action,actor=None,payload=None,at=None):
    p=t['plan']
    if actor is None:actor=p['viewer'] if action in ('start','entry','lock_viewer') else p['judges'][0] if action=='rank' else p['tasker']
    if at is None:at=f'2026-11-06T09:{len(t["events"])+1:02d}:00+05:30'
    return r.apply(t,action,actor,at,payload or {})


def recording(t=None):return step(step(t or fresh(),'commit'),'start')
def viewer_locked(t=None):
    t=recording(t)
    t=step(t,'entry',payload=dict(text='  Café Café\r\n猫\t `````json  ',stage='II',attachments=[]))
    return step(t,'lock_viewer',payload=dict(digest=r.lock_digest(t,'viewer')))
def judged(t=None,target_rank=None):
    t=viewer_locked(t);t=step(t,'start_judge')
    alias=r.ALIASES[t['plan']['presentation_order'].index(t['selection']['index'])]
    for j,n in zip(t['plan']['judges'],itertools.cycle([target_rank or 3,5])):
        remaining=iter(x for x in range(1,6) if x!=n)
        ranks={a:n if a==alias else next(remaining) for a in r.ALIASES}
        t=step(t,'rank',j,dict(ranks=ranks,report='  original judge text\r\n'))
    return step(t,'lock_judge',payload=dict(digest=r.lock_digest(t,'judge')))
def completed(t=None,target_rank=None):
    t=judged(t,target_rank);t=step(t,'reveal',payload=dict(preimage=r.preimage(t)))
    return step(t,'report')


class RemoteViewingTests(unittest.TestCase):
    def test_known_commitment(self):
        t=fresh();self.assertEqual(t['commitment'],KNOWN['commitment']);self.assertEqual(r.preimage(t),KNOWN['preimage'])

    def test_known_source_locks(self):
        c=r.verify_trial(KNOWN['reported_trial'])
        self.assertEqual(c['viewer_lock'],KNOWN['viewer_lock']);self.assertEqual(c['judge_lock'],KNOWN['judge_lock'])
        self.assertEqual(r.report(KNOWN['reported_trial'])['judge_results'][0]['actual_target_rank'],KNOWN['expected_rank'])

    def test_lifecycle(self):
        t=completed();self.assertEqual(r.verify_trial(t)['state'],'reported')
        self.assertTrue(all(e['accepted'] for e in t['events']));self.assertTrue(r.report(t)['eligible_blinded_scoring'])

    def test_concealment(self):
        t=step(fresh(),'commit');p=r.viewer_packet(t)
        self.assertEqual(set(p),set(r.DATA['viewer_packet_fields']))
        for field in ('nonce','selection','pool','target_id','path','seed','preimage','plan'):
            self.assertNotIn(field,p)
        self.assertNotIn(t['nonce'],r.canonical(p).decode());self.assertNotIn(KNOWN['seed'],r.canonical(p).decode())

    def test_public_status(self):
        t=judged();p=r.report(t)
        self.assertEqual(p['visibility'],'public_status')
        for k in ('trial','selection','nonce','pool_sha256','plan_sha256','judge_results','events'):self.assertNotIn(k,p)
        self.assertNotIn(t['nonce'],r.markdown(p))

    def test_judge_packet(self):
        t=judged();t['events']=t['events'][:5];p=r.judge_packet(t,'judge')
        self.assertEqual(set(p),set(r.DATA['judge_packet_fields']));self.assertTrue(r.validate_packet(p))
        raw=r.canonical(p).decode()
        for forbidden in (t['nonce'],KNOWN['seed'],'target_id','presentation_order','data/remote-viewing-assets'):
            self.assertNotIn(forbidden,raw)

    def test_judge_public_text_mutation(self):
        p=r.judge_packet(viewer_locked(),'judge');p['transcript'][0]['text']+='changed'
        with self.assertRaises(ValueError):r.validate_packet(p)

    def test_transcript_mutation(self):
        t=completed();t['events'][2]['payload']['text']+='x'
        with self.assertRaises(ValueError):r.verify_trial(t)

    def test_rehashed_transcript_still_breaks_lock(self):
        t=completed();t['events'][2]['payload']['text']+='x'
        self._rehash(t)
        with self.assertRaises(ValueError):r.verify_trial(t)

    def _rehash(self,t):
        for i,e in enumerate(t['events']):
            e['previous']=t['events'][i-1]['sha256'] if i else r.digest(dict(plan_sha256=t['plan_sha256'],pool_sha256=t['pool_sha256'],commitment=t['commitment']))
            q={k:v for k,v in e.items() if k!='sha256'};e['sha256']=r.digest(dict(domain=r.DATA['event_domain'],event=q))

    def test_judge_mutation(self):
        t=completed();t['events'][5]['payload']['report']+='x';self._rehash(t)
        with self.assertRaises(ValueError):r.verify_trial(t)

    def test_original_whitespace(self):
        t=completed();self.assertEqual(t['events'][2]['payload']['text'],'  Café Café\r\n猫\t `````json  ')
        p=r.judge_packet(viewer_locked(),'judge');self.assertEqual(p['transcript'][0]['text'],t['events'][2]['payload']['text'])

    def test_replay(self):
        t=completed();self.assertEqual(r.canonical(r.report(t)),r.canonical(r.report(copy.deepcopy(t))))

    def test_scoring_precommitment(self):
        t=completed();t['plan']['primary_endpoint']='rank1'
        with self.assertRaises(ValueError):r.report(t)

    def test_premature_reveal_retained(self):
        t=step(fresh(),'commit');t=step(t,'reveal',payload=dict(preimage=r.preimage(t)))
        self.assertFalse(t['events'][-1]['accepted']);self.assertEqual(r.verify_trial(t)['state'],'committed')
        self.assertEqual(len(t['events']),2)

    def test_unauthorized_reveal(self):
        t=judged();t=step(t,'reveal','viewer',dict(preimage=r.preimage(t)))
        self.assertFalse(t['events'][-1]['accepted'])

    def test_wrong_opening(self):
        t=judged();p=r.preimage(t);p['nonce']='0'*64
        t=step(t,'reveal',payload=dict(preimage=p));self.assertFalse(t['events'][-1]['accepted'])

    def test_duplicate_judge_assignment(self):
        with self.assertRaises(ValueError):fresh(judges=['judge','judge'])

    def test_duplicate_alias(self):
        p=r.judge_packet(viewer_locked(),'judge');p['candidates'][1]['alias']='c1'
        with self.assertRaises(ValueError):r.validate_packet(p)

    def test_duplicate_trial_ledger(self):
        t=completed()
        with self.assertRaises(ValueError):r.summary([t,t])

    def test_full_ledger_required(self):
        t=completed(fresh(trial_ids=['trial001','trial002']))
        with self.assertRaises(ValueError):r.summary([t])

    def test_target_reuse_rejected(self):
        ts=[completed(fresh(trial_ids=['trial001','trial002'],trial_id=i)) for i in ('trial001','trial002')]
        with self.assertRaises(ValueError):r.summary(ts)

    def test_declared_dependence(self):
        ts=[completed(fresh(trial_ids=['trial001','trial002'],trial_id=i,reuse_policy='declare_dependence')) for i in ('trial001','trial002')]
        s=r.summary(ts);self.assertTrue(s['declared_dependence']);self.assertFalse(s['independence_verified']);self.assertNotIn('p_value',s)

    def test_timezone_missing_attempt(self):
        t=step(fresh(),'commit',at='2026-11-06T09:01:00')
        self.assertFalse(t['events'][-1]['accepted']);self.assertEqual(t['events'][-1]['at'],'2026-11-06T09:01:00')

    def test_reverse_chronology(self):
        t=step(fresh(),'commit');t=step(t,'start',at='2026-11-06T09:00:00+05:30')
        self.assertFalse(t['events'][-1]['accepted'])

    def test_offset_comparison(self):
        t=step(fresh(),'commit',at='2026-11-06T03:31:00Z');self.assertTrue(t['events'][-1]['accepted'])

    def test_role_collision(self):
        with self.assertRaises(ValueError):fresh(viewer='tasker')

    def test_aware_blind_viewer(self):
        k=copy.deepcopy(KNOWN['plan']['knowledge']);k['viewer']='aware'
        with self.assertRaises(ValueError):fresh(knowledge=k)

    def test_wrong_pool(self):
        t=completed();t['plan']['pool']['id']='other'
        with self.assertRaises(ValueError):r.verify_trial(t)

    def test_wrong_asset_digest(self):
        p=copy.deepcopy(KNOWN['plan']);p['pool']['candidates'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):r.create(p,seed=KNOWN['seed'])

    def test_asset_mutation(self):
        t=completed()
        with tempfile.TemporaryDirectory() as tmp:
            for a in t['plan']['pool']['candidates']:
                dest=Path(tmp,a['path']);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(Path(a['path']).read_bytes())
            Path(tmp,t['plan']['pool']['candidates'][0]['path']).write_bytes(b'changed')
            with self.assertRaises(ValueError):r.verify_trial(t,tmp)

    def test_chance_space(self):
        ranks=[v for x in FIXTURE['arithmetic']['permutations'] for v in x['expected_rank_by_target']]
        self.assertEqual(sum(ranks),1800);self.assertEqual(len(ranks),600);self.assertEqual(ranks.count(1),120)

    def test_judge_disagreement_one_trial(self):
        t=completed(fresh(judges=['j1','j2']));s=r.summary([t]);p=r.report(t)
        self.assertEqual(s['planned'],1);self.assertEqual(s['valid'],1);self.assertTrue(p['judge_disagreement'])
        self.assertEqual(set(s['per_judge']),{'j1','j2'})

    def test_judge_lock_requires_every_judge(self):
        t=viewer_locked(fresh(judges=['j1','j2']));t=step(t,'start_judge')
        t=step(t,'rank','j1',dict(ranks=dict(zip(r.ALIASES,range(1,6))),report=''))
        t=step(t,'lock_judge',payload=dict(digest=r.lock_digest(t,'judge')))
        self.assertFalse(t['events'][-1]['accepted'])

    def test_repeated_ranking_rejected(self):
        t=judged();t['events']=t['events'][:-1]
        t=step(t,'rank',payload=dict(ranks=dict(zip(r.ALIASES,range(1,6))),report='changed'))
        self.assertFalse(t['events'][-1]['accepted'])

    def test_simulated_every_packet(self):
        self.assertEqual(r.viewer_packet(step(fresh(),'commit'))['origin'],'simulated')
        self.assertEqual(r.judge_packet(viewer_locked(),'judge')['origin'],'simulated')
        self.assertEqual(r.report(completed())['origin'],'simulated')
        self.assertFalse(r.report(completed())['randomization']['chance_qualified'])

    def test_human_manual_no_uniform_claim(self):
        t=completed(fresh(origin='human',assignment_policy='manual'));p=r.report(t)
        self.assertEqual(p['origin'],'human');self.assertTrue(p['eligible_blinded_scoring']);self.assertFalse(p['chance_reference']['applicable'])

    def test_human_cannot_predictable_seed(self):
        with self.assertRaises(ValueError):fresh(origin='human')

    def test_private_os_rejection_sampling(self):
        with patch.object(r.secrets,'token_bytes',side_effect=[bytes([250]),bytes([255]),bytes([249])]),patch.object(r.secrets,'token_hex',return_value='a'*64):
            t=fresh(origin='human',assignment_policy='os_uniform')
        self.assertEqual(t['selection']['draws'],[250,255,249]);self.assertEqual(t['selection']['index'],4)
        self.assertEqual(len(t['nonce']),64);r.verify_trial(t)

    def test_malformed_uniform_log(self):
        t=fresh(origin='human',assignment_policy='os_uniform');t['selection']['draws']=[1,2]
        with self.assertRaises(ValueError):r.verify_trial(t)

    def test_unblinded_training(self):
        t=recording(fresh(mode='training_feedback'));t=step(t,'feedback',payload=dict(text='training feedback',code='N'))
        self.assertTrue(t['events'][-1]['accepted'])
        t=step(t,'lock_viewer',payload=dict(digest=r.lock_digest(t,'viewer')));t=step(t,'start_judge')
        t=step(t,'rank',payload=dict(ranks=dict(zip(r.ALIASES,range(1,6))),report=''))
        t=step(t,'lock_judge',payload=dict(digest=r.lock_digest(t,'judge')));t=step(t,'reveal',payload=dict(preimage=r.preimage(t)))
        self.assertFalse(r.report(t)['eligible_blinded_scoring'])

    def test_blind_feedback_rejected(self):
        t=step(recording(),'feedback',payload=dict(text='leak attempt',code='N'))
        self.assertFalse(t['events'][-1]['accepted'])

    def test_failure_then_success_preserved(self):
        t=step(fresh(),'reveal',payload=dict(preimage=r.preimage(fresh())))
        t=completed(t);p=r.report(t)
        self.assertEqual(p['attempts_rejected'],1);self.assertFalse(p['trial']['events'][0]['accepted'])

    def test_no_silent_amendment(self):
        t=step(viewer_locked(),'entry',payload=dict(text='amend',stage=None,attachments=[]))
        self.assertFalse(t['events'][-1]['accepted'])

    def test_pre_reveal_markdown_no_private_replay(self):
        t=step(fresh(),'commit');p=r.viewer_packet(t);md=r.markdown(p)
        self.assertNotIn(t['nonce'],md);self.assertNotIn('private_tasker',md);self.assertNotIn('"trial":',md)

    def test_export_fresh_directory(self):
        p=r.judge_packet(viewer_locked(),'judge')
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp,'judge');r.export_packet(p,out)
            self.assertEqual(sorted(x.name for x in out.iterdir()),['c1.png','c2.png','c3.png','c4.png','c5.png','packet.json'])
            self.assertEqual(json.loads((out/'packet.json').read_text(encoding='utf-8')),p)
            for a in p['candidates']:self.assertEqual(r.bytes_hash((out/a['name']).read_bytes()),a['sha256'])
            with self.assertRaises(ValueError):r.export_packet(p,out)

    def test_export_viewer_only_packet(self):
        p=r.viewer_packet(step(fresh(),'commit'))
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp,'v');r.export_packet(p,out);self.assertEqual([x.name for x in out.iterdir()],['packet.json'])

    def test_no_private_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):r.export_packet(r.report(completed()),Path(tmp,'out'))

    def test_pinned_profile(self):
        self.assertEqual(r.digest(r.assets()[0]),r.PROFILE_HASH);self.assertEqual(r.assets()[0]['stages'],FIXTURE['source_facts']['stages'])

    def test_packet_does_not_copy_sidecars(self):
        # Explicit export copies only whitelisted assets,not input directories or siblings.
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp,'secret.xmp').write_text('actual target t1')
            out=Path(tmp,'packet');r.export_packet(r.judge_packet(viewer_locked(),'judge'),out)
            self.assertNotIn('secret.xmp',[x.name for x in out.iterdir()])

    def test_attachment_lock_and_neutral_export(self):
        t=recording();a=copy.deepcopy(t['plan']['pool']['candidates'][0])
        t=step(t,'entry',payload=dict(text='sketch',stage='III',attachments=[a]));t=step(t,'lock_viewer',payload=dict(digest=r.lock_digest(t,'viewer')))
        p=r.judge_packet(t,'judge');self.assertEqual(p['transcript'][0]['attachments'][0]['name'],'a1-1.png');self.assertTrue(r.validate_packet(p))

    def test_nonstring_task_rejected(self):
        with self.assertRaises(ValueError):r.read(dict(schema_version=1,profile=r.PROFILE,task=[]))

    def test_nonstring_alias_rejected(self):
        p=r.judge_packet(viewer_locked(),'judge');p['candidates'][0]['alias']=[]
        with self.assertRaises(ValueError):r.validate_packet(p)

    def test_event_decision_mutation(self):
        t=completed();t['events'][2]['accepted']=False
        with self.assertRaises(ValueError):r.verify_trial(t)

    def test_event_counter_mutation(self):
        t=completed();t['events'][2]['seq']=True
        with self.assertRaises(ValueError):r.verify_trial(t)

    def test_png_trailing_and_crc(self):
        b=Path(KNOWN['plan']['pool']['candidates'][0]['path']).read_bytes()
        for bad in [b+b'secret',b[:-1]+bytes([b[-1]^1])]:
            with self.assertRaises(ValueError):r.png(bad)

    def test_relative_asset_escape(self):
        for ref in ['../secret.png','C:/secret.png','/secret.png','dir\\secret.png']:
            with self.assertRaises(ValueError):r.file_bytes(r.ROOT,ref)


def add_case(name,fn):setattr(RemoteViewingTests,'test_'+name,fn)
for n in range(1,6):
    def case(self,n=n):self.assertEqual(r.report(completed(target_rank=n))['judge_results'][0]['actual_target_rank'],n)
    add_case('actual_target_rank_'+str(n),case)
for stage in ['I','II','III','IV','V','VI']:
    def case(self,stage=stage):
        t=step(recording(),'entry',payload=dict(text='',stage=stage,attachments=[]));self.assertTrue(t['events'][-1]['accepted'])
    add_case('crv_stage_'+stage,case)
for status in r.TERMINAL:
    def case(self,status=status):
        t=step(recording(),'terminate',payload=dict(status=status,reason='Recorded exception'))
        self.assertEqual(r.verify_trial(t)['state'],status)
        s=r.summary([t]);self.assertEqual(s['states'][status],1);self.assertEqual(s['valid'],0)
        t=step(t,'commit');self.assertFalse(t['events'][-1]['accepted'])
    add_case('terminal_'+status,case)
for n,bad in enumerate(FIXTURE['invalid_ranks']):
    def case(self,bad=bad):
        with self.assertRaises(ValueError):r.rank_result(dict(zip(r.ALIASES,bad)),0,list(range(5)))
    add_case('invalid_ranking_'+str(n),case)
for field in ['nonce','seed','actual_target_id','path','caption','outcome','candidate_names']:
    def case(self,field=field):
        p=r.viewer_packet(step(fresh(),'commit'));p[field]='planted secret'
        with self.assertRaises(ValueError):r.validate_packet(p)
    add_case('viewer_leak_'+field,case)
for chunk_name in [b'eXIf',b'tEXt',b'iTXt',b'zTXt',b'tIME']:
    def case(self,chunk_name=chunk_name):
        b=Path(KNOWN['plan']['pool']['candidates'][0]['path']).read_bytes();data=b'planted target'
        c=struct.pack('>I',len(data))+chunk_name+data+struct.pack('>I',zlib.crc32(chunk_name+data)&0xffffffff)
        with self.assertRaises(ValueError):r.png(b[:33]+c+b[33:])
    add_case('metadata_chunk_'+chunk_name.decode(),case)
for key in ['holder','permission','attribution','basis']:
    def case(self,key=key):
        p=copy.deepcopy(KNOWN['plan']);p['pool']['candidates'][0]['rights'][key]=''
        with self.assertRaises(ValueError):r.create(p,seed=KNOWN['seed'])
    add_case('rights_'+key,case)
for field in ['primary_endpoint','tie_policy','stopping_rule','exclusion_rule','profile_sha256']:
    def case(self,field=field):
        p=copy.deepcopy(KNOWN['plan']);p[field]='posthoc'
        with self.assertRaises(ValueError):r.create(p,seed=KNOWN['seed'])
    add_case('frozen_'+field,case)

if __name__=='__main__':unittest.main()
