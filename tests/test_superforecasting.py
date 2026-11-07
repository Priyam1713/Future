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
