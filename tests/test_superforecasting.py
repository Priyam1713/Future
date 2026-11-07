import copy
import unittest
from pathlib import Path
from future import superforecasting as e
from future.scrying import load_input
from scripts.superforecasting_oracle import plan,reference_class,sha

FIX=load_input(Path('tests/fixtures/superforecasting_reference_v1.json'))
class SuperforecastingTests(unittest.TestCase):
    def test_original_plan_and_hash(self):
        p=plan();self.assertEqual(p,FIX['original_plan']);l=e.create(p);self.assertEqual(l['plan_sha256'],sha(p));l['plan']['questions'][0]['text']='changed';self.assertEqual(p,plan())
    def test_question_lock(self):
        q=plan()['questions'][0];q['locked_at']='2025-01-04T00:00:00Z'
        with self.assertRaises(ValueError):e.question(q)
    def test_ambiguous_question_declaration(self):
        q=plan()['questions'][0];q['clarity_confirmed']=False
        with self.assertRaises(ValueError):e.question(q)
    def test_missing_resolution_rule(self):
        q=plan()['questions'][0];q['resolution']['negative_rule']=' '
        with self.assertRaises(ValueError):e.question(q)
    def test_class_unknown_members_retained(self):
        c=reference_class([1,None,0]);c['members'][0]['eligibility']='ambiguous';r=e.reference_class(c);self.assertEqual(r['denominator'],1);self.assertEqual(r['base_rate']['exact'],'0');self.assertEqual(len(r['members']),3)
    def test_duplicate_historical_event(self):
        c=reference_class();c['members'][1]['event_id']=c['members'][0]['event_id']
        with self.assertRaises(ValueError):e.reference_class(c)
    def test_class_after_freeze(self):
        c=reference_class();c['members'][0]['observed_at']='2025-01-01T00:00:00Z'
        with self.assertRaises(ValueError):e.reference_class(c)
    def test_class_mutation_hash(self):
        p=plan();p['classes'][0]['members'][0]['outcome']=0
        with self.assertRaises(ValueError):e.create(p)
    def test_test_group_leak(self):
        p=plan();p['classes'][0]['members'][0]['dependency_group']='test1'
        with self.assertRaises(ValueError):e.create(p)
    def test_event_leak(self):
        p=plan();p['classes'][0]['members'][0]['event_id']='event1';p['questions'][0]['class_sha256']=sha(p['classes'][0])
        with self.assertRaises(ValueError):e.create(p)
    def test_duplicate_slot(self):
        p=plan();p['slots'].append(copy.deepcopy(p['slots'][0]))
        with self.assertRaises(ValueError):e.create(p)
    def test_invalid_class_type(self):
        p=plan();p['classes']=[None]
        with self.assertRaises(ValueError):e.create(p)
    def test_rights(self):
        c=reference_class();c['source']['rights']='unknown'
        with self.assertRaises(ValueError):e.reference_class(c)
    def test_snapshot_hash(self):
        c=reference_class();c['source']['snapshot']+='rewrite'
        with self.assertRaises(ValueError):e.reference_class(c)
    def test_source_identity(self):
        p=plan();p['questions'][1]['source']['locator']='different'
        with self.assertRaises(ValueError):e.create(p)
    def test_reference_baseline(self):
        p=plan();p['questions'][0]['baseline'].update(kind='reference_class',probability='3/10');e.create(p)
        p['questions'][0]['baseline']['probability']='1/2'
        with self.assertRaises(ValueError):e.create(p)
    def test_empirical_mode_reject(self):
        p=plan();p['evidence_mode']='validated_superforecaster'
        with self.assertRaises(ValueError):e.create(p)

for i,c in enumerate(FIX['base_rates']):
    def test(self,c=c):
        r=e.reference_class(reference_class(c['outcomes']));self.assertEqual((r['numerator'],r['denominator'],r['base_rate']['exact']),(c['k'],c['n'],c['rate']))
    setattr(SuperforecastingTests,f'test_reference_{i}',test)

from scripts.superforecasting_oracle import forecast,update,resolution
class SuperforecastingActionTests(unittest.TestCase):
    def setup_update(self):
        p=plan();v=forecast(p);l=e.append(e.create(p),'forecast',v);u=update(v,p);l=e.append(l,'update',u);return p,l,v,u
    def test_positive_update(self):
        p,l,v,u=self.setup_update();r=e.replay(l)['forecasts']['f1'][-1];self.assertEqual(r['calculation']['posterior']['exact'],'3/7');self.assertFalse(r['calculation']['empirically_validated'])
    def test_conditional_likelihoods(self):
        p=plan();v=forecast(p);u=update(v,p);u['bayes'].update(kind='conditional_likelihoods',ratio=None,likelihood_h='3/5',likelihood_not_h='1/5');l=e.append(e.append(e.create(p),'forecast',v),'update',u);self.assertEqual(e.replay(l)['forecasts']['f1'][-1]['record']['probability'],'3/7')
    def test_duplicate_evidence_attempt(self):
        p,l,v,u=self.setup_update();bad=update(u,p,at='2025-01-02T01:00:00Z',dependence='independent');out=e.append(l,'update',bad,keep_rejected=True);self.assertEqual(len(e.replay(out)['forecasts']['f1']),2);self.assertEqual(out['actions'][-1]['decision'],'rejected');self.assertIn('Duplicate evidence',out['actions'][-1]['reason']);self.assertEqual(out['actions'][-1]['record'],bad)
    def test_same_fact_new_article(self):
        p,l,v,u=self.setup_update();bad=update(u,p,evidence_id='e2',group='newgroup',fact='fact1',at='2025-01-02T01:00:00Z',dependence='independent')
        with self.assertRaises(ValueError):e.append(l,'update',bad)
    def test_same_snapshot_new_id(self):
        p,l,v,u=self.setup_update();bad=update(u,p,evidence_id='e2',group='newgroup',fact='fact2',at='2025-01-02T01:00:00Z',dependence='independent');bad['evidence'][0]['source']=copy.deepcopy(u['evidence'][0]['source'])
        with self.assertRaises(ValueError):e.append(l,'update',bad)
    def test_independence_both_hypotheses(self):
        p,l,v,u=self.setup_update();bad=update(u,p,evidence_id='e2',group='newgroup',fact='fact2',at='2025-01-02T01:00:00Z',dependence='independent');bad['bayes']['independent_given_not_h']=False
        with self.assertRaises(ValueError):e.append(l,'update',bad)
    def test_same_group_cannot_claim_independence(self):
        p,l,v,u=self.setup_update();bad=update(u,p,evidence_id='e2',group='evidence-group1',fact='fact2',at='2025-01-02T01:00:00Z',dependence='independent')
        with self.assertRaises(ValueError):e.append(l,'update',bad)
    def test_independent_new_facts(self):
        p,l,v,u=self.setup_update();new=update(u,p,evidence_id='e2',group='newgroup',fact='fact2',at='2025-01-02T01:00:00Z',dependence='independent');out=e.append(l,'update',new);self.assertEqual(e.replay(out)['forecasts']['f1'][-1]['record']['probability'],'9/13')
    def test_conditional_same_group_new_fact(self):
        p,l,v,u=self.setup_update();new=update(u,p,evidence_id='e2',fact='fact2',at='2025-01-02T01:00:00Z',dependence='conditional',conditioned_on=['evidence1']);e.append(l,'update',new);new['bayes']['conditioned_on']=[]
        with self.assertRaises(ValueError):e.append(l,'update',new)
    def test_wrong_posterior(self):
        p=plan();v=forecast(p);u=update(v,p);u['probability']='1/2'
        with self.assertRaises(ValueError):e.append(e.append(e.create(p),'forecast',v),'update',u)
    def test_manual_revision_not_backsolved(self):
        p,l,v,u=self.setup_update();m=forecast(p,probability='2/5',version=3,parent=sha(u),at='2025-01-02T02:00:00Z');l=e.append(l,'forecast',m);self.assertIsNone(e.replay(l)['forecasts']['f1'][-1]['calculation'])
    def test_late_forecast_retained(self):
        p=plan();v=forecast(p,at='2025-01-04T00:00:00Z');l=e.append(e.create(p),'forecast',v);self.assertEqual(len(e.replay(l)['forecasts']['f1']),1)
    def test_wrong_parent(self):
        p=plan();v=forecast(p,version=2,parent='0'*64)
        with self.assertRaises(ValueError):e.append(e.create(p),'forecast',v)
    def test_backward_action_time(self):
        p,l,v,u=self.setup_update();m=forecast(p,version=3,parent=sha(u),at='2025-01-01T20:00:00Z')
        with self.assertRaises(ValueError):e.append(l,'forecast',m)
    def test_resolution_negative_null_occurrence(self):
        p=plan();r=resolution(p,outcome=0);l=e.append(e.create(p),'resolve',r);self.assertIsNone(e.replay(l)['resolutions']['q1'][0]['record']['occurrence_at']);r['occurrence_at']=r['window_end']
        with self.assertRaises(ValueError):e.append(e.create(p),'resolve',r)
    def test_negative_before_window_close(self):
        p=plan();r=resolution(p,outcome=0);r['outcome_known_at']='2025-01-09T23:59:59Z'
        with self.assertRaises(ValueError):e.append(e.create(p),'resolve',r)
    def test_positive_window_end_excluded(self):
        p=plan();r=resolution(p);r['occurrence_at']=r['window_end']
        with self.assertRaises(ValueError):e.append(e.create(p),'resolve',r)
    def test_resolution_correction_history(self):
        p=plan();r=resolution(p);l=e.append(e.create(p),'resolve',r);new=resolution(p,outcome=0,version=2,parent=sha(r),at='2025-01-12T00:00:00Z')
        with self.assertRaises(ValueError):e.append(l,'resolve',new)
        dispute=resolution(p,status='disputed',version=2,parent=sha(r),at='2025-01-12T00:00:00Z');l=e.append(l,'resolve',dispute);new=resolution(p,outcome=0,version=3,parent=sha(dispute),at='2025-01-13T00:00:00Z');l=e.append(l,'resolve',new);self.assertEqual(len(e.replay(l)['resolutions']['q1']),3)
    def test_action_chain_mutation(self):
        p,l,v,u=self.setup_update();l['actions'][0]['record']['probability']='1'
        with self.assertRaises(ValueError):e.replay(l)
    def test_forged_rejection(self):
        p,l,v,u=self.setup_update();l['actions'][-1]['decision']='rejected';l['actions'][-1]['reason']='false';l['actions'][-1]['sha256']=sha({k:v for k,v in l['actions'][-1].items() if k!='sha256'})
        with self.assertRaises(ValueError):e.replay(l)
    def test_impossible_conditional_evidence(self):
        p=plan();v=forecast(p);u=update(v,p);u['bayes'].update(kind='conditional_likelihoods',ratio=None,likelihood_h='0',likelihood_not_h='0')
        with self.assertRaises(ValueError):e.append(e.append(e.create(p),'forecast',v),'update',u)

for i,c in enumerate(FIX['bayes']):
    def test(self,c=c):
        if c['status']=='undefined':
            with self.assertRaises(ValueError):e.posterior(c['prior'],c['ratio'])
        else:self.assertEqual(str(e.posterior(c['prior'],c['ratio'])),c['posterior'])
    setattr(SuperforecastingActionTests,f'test_bayes_{i}',test)
