"""Frozen independent model tables, strict rejection and pairing invariants."""
import copy
import json
from unittest import TestCase
from unittest.mock import patch
from future.psychohistory import read,words
from scripts.verify_psychohistory import fixture,verify_case,R

F=fixture()
class PsychohistoryTests(TestCase):
    def test_prng_known_answers(self):self.assertEqual(words(1,5),F['prng_seed1_first5'])
    def test_no_execution_before_budget_refusal(self):
        for name in ['count-cap','state-cap','work-cap']:
            with patch('future.psychohistory.words',side_effect=AssertionError('draw before preflight')):
                with self.assertRaises(ValueError):read(F['cases'][name]['input'])
    def test_input_not_mutated(self):
        q=copy.deepcopy(F['cases']['overrides']['input']);before=copy.deepcopy(q);read(q);self.assertEqual(q,before)
    def test_scenario_order_does_not_change_stream(self):
        q=copy.deepcopy(F['cases']['paired-rho']['input']);a=read(q);q['scenarios'].reverse();b=read(q)
        self.assertEqual(a['stream_sha256'],b['stream_sha256']);self.assertEqual({s['id']:s['rows'] for s in a['scenarios']},{s['id']:s['rows'] for s in b['scenarios']})
    def test_scenario_override_preserves_draw_consumption(self):
        a=read(F['cases']['overrides']['input']);b=read(F['cases']['paired-rho']['input']);self.assertEqual(a['stream_sha256'],b['stream_sha256'])
    def test_relabelled_physical_fixed_seed_system(self):
        a=read(F['cases']['node-thresholds']['input']);b=read(F['cases']['relabelled']['input']);self.assertEqual(a['scenarios'][0]['rows'][0]['active_counts'],b['scenarios'][0]['rows'][0]['active_counts'])

def make_case(name,c):
    def test(self):verify_case(name,c)
    return test
for name,c in F['cases'].items():setattr(PsychohistoryTests,'test_fixture_'+name.replace('-','_'),make_case(name,c))

def make_boundary(c):
    def test(self):
        if c['exit_code']:
            with patch('future.psychohistory.words',side_effect=AssertionError('draw before cap')):
                with self.assertRaisesRegex(ValueError,'count_cells'):read(c['input'])
        else:self.assertEqual(read(c['input'])['scenarios'][0]['rows'][0]['initial_active'],c['initial_active'])
    return test
for name,c in json.loads((R/'tests/fixtures/psychohistory-boundaries-v1.json').read_text())['cases'].items():setattr(PsychohistoryTests,'test_boundary_'+name.replace('-','_'),make_boundary(c))
