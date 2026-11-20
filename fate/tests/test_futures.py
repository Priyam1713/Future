import json
from datetime import datetime, timezone
from unittest import TestCase

from fastapi.testclient import TestClient

from fate.api import create_app
from fate.build_futures import OUT, build
from fate.futures import DEFAULTS, MODULES, StudyInput, native_request
from future import prophetic_dreams, remote_viewing


class FutureRoomsTest(TestCase):
    def test_native_public_parity(self):
        clock = lambda: 1700000000
        with TestClient(create_app(clock=clock)) as client:
            for oracle, engine in MODULES.items():
                request = dict(oracle=oracle,option=DEFAULTS.get(oracle,0))
                response = client.post('/api/future-study',json=request)
                self.assertEqual(response.status_code,200,response.text[:500])
                self.assertEqual(response.headers['cache-control'],'no-store')
                output = response.json()
                native = native_request(StudyInput(**request),clock)
                self.assertEqual(output['request'],json.loads(json.dumps(native)))
                self.assertEqual(output['result'],json.loads(json.dumps(engine.read(native))))
                self.assertTrue(output['view']['title'])

    def test_frozen_public_catalog_and_control_domains(self):
        for name, expected in zip(('index-v1.json','folios-v1.json'),build()):
            self.assertEqual(json.loads((OUT/name).read_text(encoding='utf-8')),
                             json.loads(json.dumps(expected)))

    def test_text_consent_and_private_memory_projection(self):
        with TestClient(create_app()) as client:
            for oracle in (24,26,46,49):
                q = dict(oracle=oracle,text='QA private string')
                self.assertEqual(client.post('/api/future-study',json=q).status_code,422)
            private = client.post('/api/future-study',json=dict(oracle=46,option=1,
                text='QA private string',consent=True)).json()
            self.assertTrue(private['private'])
            self.assertNotIn('QA private string',json.dumps(private))
            self.assertNotIn('record',private['result']['result'])

    def test_model_bounded_grid_and_exact_integer_fields(self):
        with TestClient(create_app()) as client:
            for inputs in (dict(oracle=54,cells=[0]*48),dict(oracle=50,cells=[0]*49),
                           dict(oracle=54,cells=[0]*48+[True]),dict(oracle=54,option=13),
                           dict(oracle=50,option=True),dict(oracle=43),dict(oracle=25)):
                self.assertEqual(client.post('/api/future-study',json=inputs).status_code,422,inputs)
            output = client.post('/api/future-study',json=dict(oracle=54,option=2,cells=[0]*49)).json()
            self.assertEqual(output['view']['instrument']['counts'],[0,0,0])

    def test_remote_context_separation_and_native_commitment(self):
        with TestClient(create_app()) as viewer:
            base = '/api/archive-session'
            st = viewer.post(base,json=dict(action='remote_start',consent=True)).json()
            packet = st['packet']
            self.assertEqual(packet['visibility'],'blind_viewer')
            self.assertTrue(remote_viewing.validate_packet(packet))
            self.assertFalse(set(packet)&{'candidates','selection','nonce','trial','actual_target_id'})
            self.assertEqual(viewer.post(base,json=dict(action='judge_open',code=st['code'])).status_code,404)
            locked = viewer.post(base,json=dict(action='remote_lock',code=st['code'],
                text='Original test impression',consent=True)).json()
            self.assertEqual(locked['phase'],'judging')
            self.assertEqual(viewer.post(base,json=dict(action='judge_open',code=locked['invite'])).status_code,403)
            with TestClient(viewer.app) as judge:
                opened = judge.post(base,json=dict(action='judge_open',code=locked['invite'])).json()
                jp = opened['packet']
                self.assertEqual(jp['visibility'],'blind_judge')
                self.assertEqual(len(jp['candidates']),5)
                self.assertFalse(set(jp)&{'selection','nonce','trial','actual_target_id'})
                self.assertEqual(judge.post(base,json=dict(action='remote_status',code=st['code'])).status_code,404)
                self.assertEqual(judge.post(base,json=dict(action='judge_rank',code=locked['invite'],
                    ranks=[1,1,2,3,4])).status_code,422)
                finish = judge.post(base,json=dict(action='judge_rank',code=locked['invite'],
                    ranks=[1,2,3,4,5])).json()
                self.assertEqual(finish['phase'],'revealed')
                self.assertEqual(judge.post(base,json=dict(action='judge_open',code=locked['invite'])).status_code,409)
            report = viewer.post(base,json=dict(action='remote_status',code=st['code'])).json()['result']
            self.assertTrue(report['commitment_verified'])
            self.assertEqual(report['commitment'],packet['commitment'])
            self.assertEqual(report,remote_viewing.report(report['trial']))

    def test_dream_chronology_and_real_observation_requirement(self):
        now = [1700000000.0]
        with TestClient(create_app(clock=lambda:now[0])) as client:
            path = '/api/archive-session'
            def act(action,**values):
                return client.post(path,json=dict(action=action,code=code,**values))
            started = client.post(path,json=dict(action='dream_start',text='Blue cloth',consent=True)).json()
            code = started['code']; now[0] += 30
            locked = act('dream_lock',text='A blue cloth in a dream',consent=True).json()
            self.assertEqual(locked['phase'],'awaiting')
            self.assertNotIn('result',locked)
            self.assertEqual(act('dream_finish',rating='match').status_code,422)
            future = datetime.fromtimestamp(now[0]+3600,timezone.utc).isoformat().replace('+00:00','Z')
            self.assertEqual(act('dream_observe',at=future,text='This has not occurred',consent=True).status_code,422)
            now[0] += 60
            observed = datetime.fromtimestamp(now[0],timezone.utc).isoformat().replace('+00:00','Z')
            self.assertEqual(act('dream_observe',at=observed,text='I saw a blue cloth on a desk',consent=True).json()['phase'],'observed')
            self.assertEqual(act('dream_finish',rating='match').status_code,422)
            now[0] += 1400
            report = act('dream_finish',rating='match').json()['result']
            self.assertEqual(report['origin'],'human')
            self.assertFalse(report['declared_blind_judging'])
            self.assertEqual(report['pairs'][0]['chronology'],'future_event')
            self.assertEqual(report['original_entries']['original']['lock_sha256'],locked['originalLock'])
            self.assertEqual(len(report['ledger']['events']),9)
            self.assertEqual(act('discard').json()['phase'],'discarded')
            self.assertEqual(act('dream_status').status_code,404)
