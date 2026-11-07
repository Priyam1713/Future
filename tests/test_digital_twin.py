"""Independent frozen state-estimation oracles and causal chronology boundaries."""
import copy
from fractions import Fraction as F
from unittest import TestCase
from unittest.mock import patch
from future.digital_twin import read,mul,add,div,product
from scripts.verify_digital_twin import fixture,verify_case
FIXTURE=fixture()
class DigitalTwinTests(TestCase):
    def test_input_immutable(self):
        q=copy.deepcopy(FIXTURE['cases']['controls']['input']);before=copy.deepcopy(q);read(q);self.assertEqual(q,before)
    def test_budget_before_prediction(self):
        with patch('future.digital_twin.predict',side_effect=AssertionError('executed before budget')):
            with self.assertRaisesRegex(ValueError,'budget'):read(FIXTURE['cases']['cell-cap']['input'])
    def test_evaluation_cutoff_cannot_change_posterior(self):
        a=read(FIXTURE['cases']['not-yet-known']['input']);b=read(FIXTURE['cases']['later-evaluation']['input']);self.assertEqual(a['scenario_fork'],b['scenario_fork']);self.assertNotEqual(a['evaluation'],b['evaluation'])
    def test_unavailable_value_does_not_change_filter(self):
        a=read(FIXTURE['cases']['delayed']['input']);b=read(FIXTURE['cases']['delayed-changed']['input']);self.assertEqual(a['scenario_fork'],b['scenario_fork'])
    def test_future_branch_cannot_change_history(self):
        q=copy.deepcopy(FIXTURE['cases']['controls']['input']);a=read(q);q.update(horizon=0,scenarios=[],reference_scenario=None);b=read(q);self.assertEqual(a['rows'],b['rows'])
    def test_scenario_order_invariant_by_identity(self):
        q=copy.deepcopy(FIXTURE['cases']['controls']['input']);a=read(q);q['scenarios'].reverse();b=read(q);self.assertEqual({s['id']:s for s in a['scenarios']},{s['id']:s for s in b['scenarios']})
    def test_preoperation_product_reservation(self):
        with self.assertRaisesRegex(ValueError,'product bit'):product(1<<4096,1<<4096)
    def test_preoperation_addition_reservation(self):
        with self.assertRaisesRegex(ValueError,'addition bit'):add(F(1<<8191),F(-(1<<8191)))
    def test_cross_cancel_before_reservation(self):self.assertEqual(mul(F(1<<8191),F(1,1<<8191)),1)
    def test_zero_denominator_rejects(self):
        with self.assertRaises(ValueError):div(1,0)
    def test_exact_noise_boundary(self):
        r=read(FIXTURE['cases']['zero-prior']['input']);self.assertEqual([x['gain'] for x in r['rows']],['0','0'])

def make_case(name,c):
    def test(self):verify_case(name,c)
    return test
for name,c in FIXTURE['cases'].items():setattr(DigitalTwinTests,'test_fixture_'+name.replace('-','_'),make_case(name,c))
