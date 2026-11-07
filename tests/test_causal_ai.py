import copy,unittest
from fractions import Fraction as F
from future.causal_ai import read,operation,ratio
from scripts.verify_causal_ai import fixture,check_case,graph_checks,expanded_graph_checks
class CausalAITests(unittest.TestCase):
    def test_graphs(self):graph_checks()
    def test_all_treatment_outcome_pairs(self):self.assertEqual(expanded_graph_checks(),3072)
    def test_structural_contrasts(self):
        r=read(fixture()['cases']['confounding']['input']);self.assertEqual(r['interventional']['contrast_last_minus_first'],'1/5');self.assertEqual(r['interventional']['contrast_first_minus_last'],'-1/5');self.assertEqual(r['observational']['contrast_last_minus_first'],'2/5')
    def test_zero_mass(self):
        r=read(fixture()['cases']['zero-mass-stratum']['input']);self.assertEqual(len(r['positivity']['zero_mass_strata']),1);self.assertTrue(any(s['skipped_zero_mass'] and s['conditional'] is None for s in r['strata']))
    def test_canonical(self):
        f=fixture();a=read(f['cases']['confounding']['input']);b=read(f['cases']['reordered']['input'])
        for key in ['model_sha256','table_sha256','interventional']:self.assertEqual(a[key],b[key])
    def test_positivity_no_smoothing(self):
        r=read(fixture()['cases']['missing-positivity']['input']);self.assertIsNone(r['interventional']);self.assertFalse(r['positivity']['passed']);self.assertEqual(len(r['positivity']['failures']),2)
    def test_bit_reservation(self):
        with self.assertRaisesRegex(ValueError,'bit reservation'):operation(F(1,2**8190),F(1,2**8190),'mul')
        with self.assertRaises(ValueError):ratio(F(1),F(0))
    def test_joint_cell_cap(self):
        q=copy.deepcopy(fixture()['cases']['no-confounding']['input']);q['nodes']=[dict(id=n,states=['0','1','2'],observed=True) for n in ['X','Y','a','b','c','d','e','f']]
        with self.assertRaisesRegex(ValueError,'joint_cells cap'):read(q)
def make_case(c):
    def test(self):check_case(c)
    return test
for name,c in fixture()['cases'].items():setattr(CausalAITests,'test_fixture_'+name.replace('-','_'),make_case(c))
if __name__=='__main__':unittest.main()
