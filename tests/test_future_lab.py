import unittest
from scripts.verify_future_lab import fixture,native_sample,protocol_cases,protocol_case,boundary_check,BOUNDARIES,demo,numeric_plan,collective_plan
from future.lab import create,forecast,replay,evaluate,capability,registry
from future.lab.evaluation import scores,number
from fractions import Fraction as F
class FutureLabTests(unittest.TestCase):
    def test_registry_coverage(self):self.assertEqual([e['technique_id'] for e in registry()['entries']],fixture()['retained_ids'])
    def test_excluded_boundaries(self):
        for i in fixture()['excluded_ids']:
            with self.subTest(i=i),self.assertRaises(ValueError):capability(i)
    def test_admission_scope(self):
        self.assertEqual([e['technique_id'] for e in registry()['entries'] if e['evaluation']['lab_v1_supported']],[49,51,57]);self.assertFalse(capability(55)['evaluation']['lab_v1_supported']);self.assertEqual(capability(60)['capability_type'],'editorial_finite_scenario_thought_experiment')
        self.assertEqual(capability(4)['capability_type'],'deterministic_symbolic_numerology');self.assertEqual(capability(45)['capability_type'],'explicit_heuristic_decision_and_binary_scoring')
        from future import superforecasting as native
        from future.lab.common import digest
        p=fixture()['demo_plan'];p['mode']='declared_prospective';old=p['native_input']['payload'];plan=old['plan'];plan['evidence_mode']='user_supplied_unvalidated';ledger=native.create(plan)
        for action in old['actions']:ledger=native.append(ledger,action['kind'],action['record'])
        p['native_input']['payload']=ledger;p['selection']['native_input_sha256']=digest(p['native_input']);self.assertEqual(create(p)['plan']['mode'],'declared_prospective')
    def test_complete_demo(self):demo()
    def test_unresolved_not_estimable(self):
        r=evaluate(create(fixture()['demo_plan']));self.assertEqual(r['model']['brier']['status'],'not_estimable');self.assertEqual(r['coverage']['missing_outcomes'],3)
    def test_numeric_forecast(self):
        l=forecast(create(numeric_plan()),'2025-04-01T00:00:00Z');s=replay(l)['forecast'];self.assertEqual(s['predictions'],dict(t0='1',t1='4'));self.assertEqual(s['baseline_predictions'],dict(t0='-2',t1='-2'))
    def test_pool_forecast(self):self.assertEqual(replay(forecast(create(collective_plan()),'2025-01-06T00:00:00Z'))['forecast']['predictions'],dict(q1='1/2'))
    def test_numeric_ledger_evaluation(self):
        from future.lab import resolve
        p=numeric_plan();l=forecast(create(p),p['cutoff'])
        for t in p['targets']:
            o=fixture()['demo_outcomes'][0];o.update(target_id=t['id'],event_id=t['event_id'],value='2',known_at=t['target_at']);o['evidence']['available_at']='2025-07-01T00:00:00Z';l=resolve(l,o,'2025-07-01T00:00:00Z')
        r=evaluate(l);self.assertEqual(r['model']['mae']['exact'],'3/2');self.assertEqual(r['baseline']['mae']['exact'],'4');self.assertEqual(r['comparison']['model_minus_baseline'],'-5/2');self.assertEqual(r['coverage']['matched_dependency_groups'],1)
    def test_pool_ledger_evaluation(self):
        from future.lab import resolve
        p=collective_plan();l=forecast(create(p),'2025-01-06T00:00:00Z');t=p['targets'][0];o=fixture()['demo_outcomes'][0];o.update(target_id=t['id'],event_id=t['event_id'],known_at=t['target_at']);o['evidence']['available_at']='2025-01-21T00:00:00Z';l=resolve(l,o,'2025-01-21T00:00:00Z');r=evaluate(l);self.assertEqual(r['model']['brier']['exact'],'1/4');self.assertEqual(r['comparison']['model_minus_baseline'],'0')
    def test_numeric_known_answers(self):
        n=fixture()['numeric_vector'];r=scores(n['predictions'],n['outcomes'],'numeric')
        for name in ['mae','mse','bias']:self.assertEqual(r[name]['exact'],n[name])
        self.assertEqual(r['rmse']['exact'],n['rmse_expression']);self.assertEqual(r['rmse']['decimal'],n['rmse_decimal'])
    def test_binary_domain(self):
        for p,y in [('6/5','1'),('1/2','2'),(True,'1'),('NaN','1')]:
            with self.subTest(p=p,y=y),self.assertRaises(ValueError):scores([p],[y],'binary')
    def test_large_exact_display_bound(self):
        n=F(10**100);r=number(n);self.assertEqual(r['exact'],str(n));self.assertIsNone(r['decimal'])
    def test_noaa_reference(self):
        from future.lab.reference import noaa_reference
        r=noaa_reference();self.assertFalse(r['new_held_out_result']);self.assertIn('underperformed',r['primary_result'])
def native_test(i):
    def test(self):native_sample(i)
    return test
def protocol_test(name):
    def test(self):protocol_case(name)
    return test
def boundary_test(name):
    def test(self):boundary_check(name)
    return test
for i in fixture()['retained_ids']:setattr(FutureLabTests,'test_native_'+str(i),native_test(i))
for name in protocol_cases():setattr(FutureLabTests,'test_protocol_'+name.replace('-','_'),protocol_test(name))
for name in BOUNDARIES:setattr(FutureLabTests,'test_boundary_'+name.replace('-','_'),boundary_test(name))
for i,v in enumerate(fixture()['binary_vectors']):
    def vector(self,v=v):
        a=scores(v['predictions'],list(map(str,v['outcomes'])),'binary');b=scores(v['baseline'],list(map(str,v['outcomes'])),'binary');self.assertEqual(a['brier']['exact'],v['brier']);self.assertEqual(a['two_category_brier']['exact'],v['two_category']);self.assertEqual(b['brier']['exact'],v['baseline_brier'])
    setattr(FutureLabTests,'test_binary_vector_'+str(i),vector)
