import copy,unittest
from fractions import Fraction as F
from future.collective_intelligence import read,operation
from scripts.verify_collective_intelligence import fixture,check_case,convention_checks,compatibility_51
class CollectiveIntelligenceTests(unittest.TestCase):
    def test_conventions_and_identities(self):convention_checks()
    def test_51_compatibility(self):self.assertTrue(compatibility_51())
    def test_weight_scale(self):
        f=fixture();a=read(f['cases']['weighted']['input']);b=read(f['cases']['weight-scale']['input'])
        self.assertEqual(a['questions']['q1']['probability'],b['questions']['q1']['probability']);self.assertEqual(a['questions']['q1']['normalized_weights'],b['questions']['q1']['normalized_weights'])
    def test_abstention_not_fallback(self):
        r=read(fixture()['cases']['abstention']['input']);self.assertEqual(r['questions']['q1']['probability'],'4/5');self.assertEqual(r['questions']['q1']['selected_versions']['fa'],2);self.assertIsNone(r['questions']['q1']['selected_probabilities']['fa'])
    def test_revisions_not_voters(self):
        r=read(fixture()['cases']['revision']['input']);self.assertEqual(r['questions']['q1']['probability'],'3/5');self.assertEqual(r['questions']['q1']['contributors'],2)
    def test_isolated_outcome_information(self):
        r=read(fixture()['cases']['informed-revision']['input']);self.assertEqual(r['questions']['q1']['selected_versions']['fa'],1);self.assertEqual(r['questions']['q1']['participant_accounting'][0]['revisions'][-1]['reasons'],['at_or_after_outcome_information'])
    def test_no_independence_certification(self):
        r=read(fixture()['cases']['llm']['input']);self.assertEqual(r['denominators']['forecaster_dependency_groups'],1);self.assertEqual(r['denominators']['forecasters'],2);self.assertFalse(r['dependence']['independence_certified']);self.assertIsNone(r['dependence']['effective_sample_size'])
    def test_heldout_separate(self):
        r=read(fixture()['cases']['train-test']['input']);self.assertEqual(r['primary']['question_ids'],['q1']);self.assertEqual(r['train']['question_ids'],['q2']);self.assertEqual(r['train']['binary_brier'],'1/25')
    def test_calibration_upper_endpoint(self):
        r=read(fixture()['cases']['perfect']['input']);self.assertEqual(r['primary']['calibration'][9]['count'],1);self.assertEqual(r['primary']['binary_brier'],'0')
    def test_forecast_after_lock(self):
        q=copy.deepcopy(fixture()['cases']['equal']['input']);q['forecasts'][0].update(issued_at='2025-01-01T12:00:00Z',knowledge_at='2025-01-01T00:00:00Z')
        with self.assertRaisesRegex(ValueError,'before question lock'):read(q)
    def test_intermediate_bit_guard(self):
        with self.assertRaisesRegex(ValueError,'bit reservation'):operation(F(1,2**8190),F(1,2**8190),'mul')
def make_case(c):
    def test(self):check_case(c)
    return test
for name,c in fixture()['cases'].items():setattr(CollectiveIntelligenceTests,'test_fixture_'+name.replace('-','_'),make_case(c))
if __name__=='__main__':unittest.main()
