import json
from unittest import TestCase

from fastapi.testclient import TestClient

from fate.api import create_app
from fate.build_signs import OUT, build
from fate.signs import ENGINES, SignInput, native_request, read_sign


SAMPLES = {
    28:['rim','anchor'], 29:['cup','two_humped_camel'],
    30:['high','persistent','persisted','hypothetical'],
    31:['perceived_fogginess','subjective','source_context'],
    32:['hake','east_west','bedfordshire'], 34:['onyx','2:-1'],
    35:['9A+9B'], 37:['gao-alpha'], 38:['crow','call','left'],
    39:['liver_head','absent','sound'],
}


class WorldOfSignsTest(TestCase):
    def setUp(self):
        self.client = TestClient(create_app())
        self.client.__enter__()
        self.addCleanup(self.client.__exit__,None,None,None)

    def submit(self, oracle, values):
        return self.client.post('/api/world-of-signs',json=dict(oracle=oracle,values=values))

    def test_every_room_equal_to_direct_native_read(self):
        for oracle, values in SAMPLES.items():
            with self.subTest(oracle=oracle):
                response = self.submit(oracle,values)
                self.assertEqual(response.status_code,200,response.text)
                self.assertEqual(response.headers['cache-control'],'no-store')
                envelope = response.json()
                request = native_request(oracle,values)
                self.assertEqual(envelope['result'],json.loads(json.dumps(ENGINES[oracle].read(request))))
                self.assertEqual(envelope['snapshot'],dict(oracle=oracle,values=values,profile=ENGINES[oracle].PROFILE))
                self.assertIn(envelope['result']['mode'],['manual','documentary'])

    def test_archive_covers_every_permitted_snapshot(self):
        for filename, expected in zip(('edition-v1.json','reference-v1.json'),build()):
            self.assertEqual(json.loads((OUT/filename).read_text(encoding='utf-8')),expected)
        for oracle, values in SAMPLES.items():
            frozen=json.loads((OUT/'reference-v1.json').read_text(encoding='utf-8'))
            self.assertEqual(read_sign(SignInput(oracle=oracle,values=values))['view'],
                frozen[str(oracle)]['|'.join(values)])

    def test_declared_inputs_are_not_inferred_by_artifacts(self):
        stone=self.submit(34,SAMPLES[34]).json()
        self.assertEqual(stone['view']['metric'],dict(distanceSquared=5,direction=['right','below']))
        lot=self.submit(37,SAMPLES[37]).json()['result']
        self.assertFalse(lot['selection']['generated'])
        self.assertFalse(lot['selection']['physical_selection_verified'])
        self.assertEqual(lot['selection']['canonical_id'],'gao-alpha')
        osteo=self.submit(35,SAMPLES[35]).json()['result']
        self.assertEqual(osteo['selected_case_ids'],['9A','9B'])
        self.assertEqual(osteo['task'],'compare')
        bird=self.submit(38,SAMPLES[38]).json()['result']
        self.assertFalse(bird['observations'][0]['modern_species_inferred'])

    def test_hazard_removes_symbolic_content_and_save_action(self):
        data=self.submit(30,['high','persistent','hazard','reported_real']).json()
        self.assertTrue(data['result']['safety']['symbolic_hold'])
        self.assertEqual(data['view']['status'],'Safety hold')
        self.assertEqual(data['view']['excerpts'],[])
        self.assertIsNone(data['snapshot'])

    def test_no_random_route_or_unstructured_observation_fields(self):
        for oracle, values in [(28,['rim']), (32,['hake','east','bedfordshire']),
                               (34,['onyx','100:3']), (35,['toss']), (37,['random']), (39,['harm','present','sound'])]:
            with self.subTest(oracle=oracle):
                self.assertEqual(self.submit(oracle,values).status_code,422)
        self.assertEqual(self.client.post('/api/world-of-signs',
            json=dict(oracle=28,values=SAMPLES[28],image='not accepted',seed='not accepted')).status_code,422)
