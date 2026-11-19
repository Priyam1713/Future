import json
from unittest import TestCase

from fastapi.testclient import TestClient
from fate.api import create_app
from fate.build_ritual import build, OUT
from fate.ritual import bibliomancy_request
from future import bibliomancy, dream, geomancy, mirror, oracle, pendulum, scrying

SEED = 'fate-block07-parity-v1'
NOTES = 'Synthetic QA only: I noticed a pale reflection near the edge.'
MOTHERS = ['1212', '2112', '1122', '2121']


class RitualWingTest(TestCase):
    def setUp(self):
        self.client = TestClient(create_app())
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)

    def native(self, room, inputs, engine, expected):
        response = self.client.post('/api/ritual-wing', json=dict(oracle=room, input=inputs))
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.headers['cache-control'], 'no-store')
        data = response.json()
        request = dict(schema_version=1, profile=engine.PROFILE, **expected)
        self.assertEqual(data['result'], json.loads(json.dumps(engine.read(request))))
        self.assertEqual(set(data['snapshot']), {'oracle','profile','values'})
        self.assertEqual(data['snapshot']['oracle'], room)
        return data

    def test_native_lenormand_all_spreads(self):
        for spread,count in [('one',1),('three',3),('five',5)]:
            inputs = dict(seed=SEED, spread=spread)
            report = self.native(17, inputs, oracle, dict(inputs, mode='seeded',
                task='symbolic_reading', protocol=oracle.PROTOCOL, orientation_policy='upright_only'))
            ids = [row['card']['id'] for row in report['result']['readings']]
            self.assertEqual(report['snapshot']['values'], ids)
            self.assertEqual(len(set(ids)),count)

    def test_pendulum_modes_do_not_confuse_animation_or_simulation_with_motion(self):
        digital = self.native(20, dict(seed=SEED), pendulum, dict(task='symbolic_response',
            mode='seeded', seed=SEED, protocol=pendulum.PROTOCOL, distribution=pendulum.DISTRIBUTION))
        self.assertIsNone(digital['result']['generated_signal'])
        self.assertFalse(digital['result']['physical_motion_observed_by_engine'])
        inputs = dict(calibration=[dict(signal='clockwise',response='yes'),dict(signal='horizontal',response='no')],
                      observations=[dict(signal='clockwise',quality='partial')])
        manual = self.native(20, inputs, pendulum, dict(inputs, task='symbolic_response', mode='manual'))
        self.assertEqual(manual['snapshot']['values'], ['manual','unresolved'])
        self.assertNotIn('clockwise', json.dumps(manual['snapshot']))

    def test_empty_and_manual_journals_remain_distinct_source_profiles(self):
        for room,engine,task in [(21,scrying,'guided_journal'),(22,mirror,'guided_mirror_journal')]:
            for journal in ([],[dict(experience_type='observed_reflection',description=NOTES)]):
                inputs = dict(journal=journal, session=dict(status='completed'))
                out = self.native(room, inputs, engine, dict(inputs, task=task, mode='manual'))
                self.assertEqual(out['snapshot']['values'], [])
                self.assertEqual(len(out['result']['journal']),len(journal))
                self.assertFalse(out['result']['perception_detected'])
                self.assertNotIn(NOTES,json.dumps(out['snapshot']))

    def test_dream_lookups_only_happen_for_selected_motifs(self):
        inputs = dict(narrative='Synthetic QA: a serpent and a meal.', context={'hungry':True}, lookups=['eating'])
        out = self.native(23, inputs, dream, dict(inputs, task='historical_reflection', mode='manual'))
        self.assertEqual(out['snapshot']['values'],['eating'])
        self.assertEqual(out['result']['motif_references'][0]['status'],'conditional_reference')
        self.assertFalse(out['result']['replay']['automatic_matching'])
        self.assertNotIn('hungry',json.dumps(out['snapshot']))
        no_lookup = self.native(23, {'narrative':inputs['narrative']}, dream,
            dict(narrative=inputs['narrative'],task='historical_reflection',mode='manual'))
        self.assertEqual(no_lookup['result']['motif_references'],[])

    def test_four_mothers_and_fifteen_positions(self):
        data = self.native(33, {'mothers':MOTHERS}, geomancy, dict(task='shield',
            mode='manual', input_mode='patterns',figure_convention=geomancy.CONVENTION,mothers=MOTHERS))
        self.assertEqual(data['snapshot']['values'],geomancy.chart(MOTHERS))
        self.assertEqual(data['result']['input_mothers'],MOTHERS)
        self.assertTrue(data['result']['invariants']['judge_even_total_points'])
        self.assertFalse(data['result']['replay']['rng'])

    def test_selected_sentence_and_context_boundary(self):
        inputs = dict(selections=[dict(path=[1,1,2,1],sentence_id='RUT.1.s001')],context=2)
        data = self.native(36,inputs,bibliomancy,dict(inputs,**bibliomancy_request(),mode='manual_coarse'))
        self.assertEqual(data['snapshot']['values'],['2','RUT.1.s001'])
        self.assertEqual(data['result']['selections'][0]['context_before'],[])
        self.assertEqual(len(data['result']['selections'][0]['context_after']),2)
        self.assertTrue(data['result']['replay']['integrity_checked'])

    def test_protocol_substitution_and_malformed_input_rejected(self):
        for room,inputs in [
            (17,{'spread':'seven','seed':SEED}), (20,{'seed':SEED,'calibration':[]}),
            (21,{'mode':'seeded','journal':[]}), (22,{'session':{'surface':'crystal'}}),
            (23,{'preferences':{'historical_references':False},'lookups':['serpent']}),
            (33,{'seed':SEED}), (33,{'mothers':['1111','2112','0111','1111']}),
            (36,{'seed':SEED}), (36,{'selections':[{'path':[1,1,2,1],'sentence_id':'RUT.1.s002'}],'context':1}),
        ]:
            with self.subTest(room=room,inputs=inputs):
                result = self.client.post('/api/ritual-wing', json=dict(oracle=room,input=inputs))
                self.assertEqual(result.status_code,422,result.text)

    def test_reference_archive_matches_native_and_does_not_contain_journal_data(self):
        for name,value in zip(('edition-v1.json','reference-v1.json'),build()):
            self.assertEqual(json.loads((OUT/name).read_text(encoding='utf-8')),value)
        self.assertEqual(len(build()[1]['cards']),36)
        self.assertEqual(len(build()[0]['sentences']),141)
