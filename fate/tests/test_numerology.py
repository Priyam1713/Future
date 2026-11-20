import copy
import json
from pathlib import Path
import unittest
from fastapi.testclient import TestClient
from fate.api import create_app
from fate.build_gallery import build
from future.numerology import calculate, readings

INPUT = dict(name='Ada Lovelace', birth='1815-12-10', target='2026-11-19', basis='birth', y_roles='')


class NumberBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.now = 1000
        def provider(prompt):
            self.calls.append(prompt)
            themes = json.loads(prompt.split('DATA: ')[1])
            return dict(themes=[dict(scope=r['scope'], source_id=r['source_id'], reflection='Consider the supplied theme as a reflection, not a forecast.') for r in themes]), dict(provider='gemini', model='test-provider')
        self.client = TestClient(create_app(provider=provider, signing_key=b'numbers-test', clock=lambda:self.now))

    def tearDown(self):
        self.client.close()

    def test_native_exact_and_independently_summed_example(self):
        response = self.client.post('/api/numerology', json=INPUT)
        self.assertEqual(response.status_code, 200)
        result = response.json()['result']
        self.assertEqual(result, readings(calculate(INPUT['birth'], INPUT['name'], 'birth', INPUT['target'])))
        # Independently hand-summed A+D+A=6, L+O+V+E+L+A+C+E=30→3; 6+3=9.
        self.assertEqual(result['expression']['result'], 9)
        # Month12→3, day10→1, year1815→15→6; 3+1+6=10→1.
        self.assertEqual(result['life_path']['result'], 1)
        # Sun12+10=22→4; 4+2026=2030→5.
        self.assertEqual(result['cycles']['year']['result'], 5)
        self.assertEqual([r['scope'] for r in result['readings'] if r['coverage']=='direct'], ['expression','personal_year'])
        self.assertFalse(self.calls)

    def test_input_rejection_and_explicit_y_roles(self):
        for delta in [dict(name='Priyā'), dict(name='Amy'), dict(birth='2026-02-30'), dict(target='2026-1-01'), dict(basis='other'), dict(name='A'*161), dict(unknown=True), dict(name='Amy',y_roles='z')]:
            with self.subTest(delta=delta):
                self.assertEqual(self.client.post('/api/numerology',json=dict(INPUT,**delta)).status_code,422)
        for role in ('v','c'):
            q=dict(INPUT,name='Amy',y_roles=role,basis='current')
            result=self.client.post('/api/numerology',json=q).json()['result']
            self.assertEqual(result,readings(calculate(q['birth'],q['name'],'current',q['target'],role)))
        self.assertIsNone(self.client.post('/api/numerology',json=dict(INPUT,name='BC')).json()['result']['soul_urge']['result'])

    def test_commentary_receipt_consent_and_privacy(self):
        envelope=self.client.post('/api/numerology',json=INPUT).json()
        q=dict(draw=INPUT,receipt=envelope['receipt'],cloud_consent=True)
        for value in (False,1,'true',None):
            self.assertEqual(self.client.post('/api/numerology/explain',json=dict(q,cloud_consent=value)).status_code,422)
        self.assertEqual(self.client.post('/api/numerology/explain',json=q).status_code,200)
        self.assertEqual(len(self.calls),1)
        for personal in ('Ada','Lovelace','1815-12-10','2026-11-19'):
            self.assertNotIn(personal,self.calls[0])
        changed=copy.deepcopy(q);changed['draw']['name']='Grace Hopper'
        self.assertEqual(self.client.post('/api/numerology/explain',json=changed).status_code,403)
        self.now+=86401
        self.assertEqual(self.client.post('/api/numerology/explain',json=q).status_code,403)

    def test_provider_mismatch_is_rejected(self):
        with TestClient(create_app(provider=lambda _:({'themes':[]},{}))) as client:
            envelope=client.post('/api/numerology',json=INPUT).json()
            response=client.post('/api/numerology/explain',json=dict(draw=INPUT,receipt=envelope['receipt'],cloud_consent=True))
            self.assertEqual(response.status_code,422)

    def test_gallery_exact_retained_projection(self):
        root=Path(__file__).resolve().parents[2]
        snapshot=json.loads((root/'fate/web/src/gallery/inventory.json').read_text(encoding='utf-8'))
        self.assertEqual(snapshot,build())
        self.assertEqual(len(snapshot['methods']),54)
        self.assertEqual([m['id'] for m in snapshot['methods'] if m['status']=='available'],[1,2,3,4,16,17,18,19,20,21,22,23,28,29,30,31,32,33,34,35,36,37,38,39])
        self.assertEqual([m['id'] for m in snapshot['methods'] if m['status']=='historical'],[9,10,13,15])
        self.assertTrue(set(snapshot['excluded_ids']).isdisjoint(m['id'] for m in snapshot['methods']))


if __name__=='__main__':unittest.main()
