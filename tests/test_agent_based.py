"""Frozen independent Life states, complete-state cycles and resource gates."""
import copy
from unittest import TestCase
from unittest.mock import patch
from future.agent_based import read,transition,neighborhoods,next_cell
from scripts.verify_agent_based import fixture,verify_case,verify_local,inplace_negative
F=fixture()
class AgentBasedTests(TestCase):
    def test_input_immutable(self):
        q=copy.deepcopy(F['cases']['scenario-comparison']['input']);before=copy.deepcopy(q);read(q);self.assertEqual(q,before)
    def test_all512_local_configurations(self):verify_local(F)
    def test_inplace_negative(self):self.assertEqual(inplace_negative(),1);self.assertEqual(read(F['cases']['blinker']['input'])['scenarios'][0]['state_trace'][1][0][2],0)
    def test_preflight_before_neighborhood_construction(self):
        for n in ['work-cap','state-cap','count-cap']:
            with patch('future.agent_based.neighborhoods',side_effect=AssertionError('work before budget')):
                with self.assertRaises(ValueError):read(F['cases'][n]['input'])
    def test_zero_ticks_no_transition(self):
        with patch('future.agent_based.transition',side_effect=AssertionError('fabricated transition')):
            r=read(F['cases']['zero-tick']['input']);self.assertEqual(r['scenarios'][0]['executed_ticks'],0);self.assertTrue(r['scenarios'][0]['truncated'])
    def test_full_requested_horizon_after_fixed_point(self):
        r=read(F['cases']['full-horizon-fixed']['input'])['scenarios'][0];self.assertEqual(r['executed_ticks'],256);self.assertEqual(len(r['counts']),257);self.assertEqual(r['period'],1)
    def test_equal_counts_do_not_imply_equal_states(self):
        comp=read(F['cases']['equal-count-different-state']['input'])['comparisons'][1];self.assertEqual(comp['final_alive_difference'],0);self.assertEqual(comp['final_hamming_distance'],4)
    def test_period_two_is_not_fixed(self):
        s=read(F['cases']['blinker']['input'])['scenarios'][0];self.assertEqual(s['period'],2);self.assertFalse(s['fixed_point'])
    def test_scenario_order_invariant(self):
        q=copy.deepcopy(F['cases']['identical']['input']);a=read(q);q['scenarios'].reverse();b=read(q);self.assertEqual({s['id']:s for s in a['scenarios']},{s['id']:s for s in b['scenarios']})
    def test_rotation_and_reflection(self):
        original=read(F['cases']['rectangle']['input'])['scenarios'][0]['state_trace'];rotated=read(F['cases']['rotated']['input'])['scenarios'][0]['state_trace'];reflected=read(F['cases']['reflected']['input'])['scenarios'][0]['state_trace']
        self.assertEqual([[list(row) for row in zip(*s[::-1])] for s in original],rotated);self.assertEqual([[row[::-1] for row in s] for s in original],reflected)
    def test_interior_translation(self):
        a=read(F['cases']['glider']['input'])['scenarios'][0]['final_grid'];b=read(F['cases']['translated']['input'])['scenarios'][0]['final_grid'];self.assertEqual({(r+2,c+1) for r,row in enumerate(a) for c,x in enumerate(row) if x},{(r,c) for r,row in enumerate(b) for c,x in enumerate(row) if x})
    def test_kernel_does_not_mutate_snapshot(self):
        state=bytes([0,0,0,1,1,1,0,0,0]);before=bytes(state);transition(state,neighborhoods(3,3));self.assertEqual(state,before)

def make_case(name,c):
    def test(self):verify_case(name,c)
    return test
for name,c in F['cases'].items():setattr(AgentBasedTests,'test_fixture_'+name.replace('-','_'),make_case(name,c))
def make_local(row):
    def test(self):self.assertEqual(next_cell(row['current'],row['neighbors']),row['next'])
    return test
for row in F['local_truth']:setattr(AgentBasedTests,'test_local_'+str(row['current'])+'_'+str(row['neighbors']),make_local(row))
