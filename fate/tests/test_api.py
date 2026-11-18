import copy
import json
import unittest
from fastapi.testclient import TestClient
from fate.api import create_app, native, Draw, POSITIONS
from future.tarot import read

REQUEST=dict(spread='three',seed='fate-independent-browser-test-v1',question='What themes invite reflection?',reversals=True)

class ConsumerTests(unittest.TestCase):
    def setUp(self):
        self.calls=[]
        def provider(prompt):
            self.calls.append(prompt)
            data=json.loads(prompt.split('DATA: ')[1])
            return dict(cards=[dict(card_id=r['card_id'],rule_id=r['rule_id'],reflection='Consider these supplied motifs as a symbolic lens.') for r in data['cards']]),dict(provider='gemini',model='test-provider')
        self.provider=provider
        self.clock=[1000]
        self.client=TestClient(create_app(provider=provider,signing_key=b'test-signing-key',clock=lambda:self.clock[0]))

    def tearDown(self): self.client.close()

    def draw(self,**changes):
        return self.client.post('/api/readings',json=dict(REQUEST,**changes))

    def test_real_engine_exact_match_and_replay(self):
        response=self.draw(); self.assertEqual(response.status_code,200)
        result=response.json()['result']
        self.assertEqual(result,read(result['replay']['request']))
        self.assertEqual([r['position']['label'] for r in result['readings']],POSITIONS)
        self.assertFalse(result['factual_prediction'])
        self.assertEqual(len(set(r['card']['id'] for r in result['readings'])),3)
        self.assertEqual(self.draw().json(),response.json())
        self.assertFalse(self.calls)

    def test_one_card_upright(self):
        result=self.draw(spread='one',reversals=False).json()['result']
        self.assertEqual(len(result['readings']),1)
        self.assertEqual(result['readings'][0]['orientation'],'upright')

    def test_multiline_question_is_plain_text_context(self):
        result=self.draw(question='First line\nSecond line').json()['result']
        self.assertEqual(result['question'],'First line Second line')
        self.assertEqual(result,read(result['replay']['request']))

    def test_profile_source_orientation_and_all_catalog_cards(self):
        # Exercise all 156 source meanings at the immutable engine boundary.
        from future.tarot_catalog import ORDER,PROFILE
        from future.tarot import validate
        for card_id in ORDER:
            for orientation in ['upright','reversed']:
                request=dict(schema_version=1,profile=PROFILE,task='symbolic_reading',mode='manual',spread='one',orientation_policy='explicit',cards=[dict(card_id=card_id,orientation=orientation)])
                result=read(validate(request))
                m=result['readings'][0]['direct_component']
                self.assertTrue(m['rule_id']);self.assertTrue(m['locator']);self.assertTrue(m['page_url'].startswith('https://en.wikisource.org/'))

    def test_schema_rejects_extra_invalid_and_unbounded_inputs(self):
        for patch in [dict(spread='waite_celtic'),dict(seed=''),dict(question='x'*1001),dict(reversals='true'),dict(seed='🙂'*100),dict(profile='fabricated'),dict(question='x\x00y')]:
            with self.subTest(patch=list(patch)):
                self.assertEqual(self.draw(**patch).status_code,422)

    def test_foreign_origin_and_body_boundary(self):
        self.assertEqual(self.client.post('/api/readings',json=REQUEST,headers={'Origin':'https://foreign.example'}).status_code,403)
        self.assertEqual(self.client.post('/api/readings',json=REQUEST,headers={'Sec-Fetch-Site':'cross-site'}).status_code,403)
        self.assertEqual(self.client.post('/api/readings',content='{}').status_code,415)
        self.assertEqual(self.client.post('/api/readings',content='x'*17000,headers={'Content-Type':'application/json'}).status_code,413)
        for raw in ['{"spread":"one","spread":"three"}', '{"spread":NaN}', '{']:
            self.assertEqual(self.client.post('/api/readings',content=raw,headers={'Content-Type':'application/json'}).status_code,422)

    def test_no_workbench_or_private_files(self):
        for path in ['/api/registry','/api/records','/.env','/../.env','/knowledge/tarot_waite_v1.json']:
            self.assertIn(self.client.get(path).status_code,[404,400])

    def test_security_headers(self):
        response=self.client.get('/api/health')
        self.assertEqual(response.headers['cache-control'],'no-store')
        self.assertIn("frame-ancestors 'none'",response.headers['content-security-policy'])
        self.assertEqual(response.headers['x-content-type-options'],'nosniff')

    def test_commentary_requires_true_consent_and_valid_signed_request(self):
        receipt=self.draw().json()['receipt']
        base=dict(draw=REQUEST,receipt=receipt)
        for consent in [False,None,'true',1,1.0,0]:
            self.clock[0]+=61
            self.assertEqual(self.client.post('/api/explain',json=dict(base,cloud_consent=consent)).status_code,422)
        self.assertEqual(self.client.post('/api/explain',json=base).status_code,422)
        self.assertFalse(self.calls)
        self.assertEqual(self.client.post('/api/explain',json=dict(base,cloud_consent=True)).status_code,200)
        self.assertEqual(len(self.calls),1)

    def test_tampered_expired_and_restarted_receipt(self):
        receipt=self.draw().json()['receipt']
        for draw,token in [(dict(REQUEST,seed='other'),receipt),(REQUEST,'bad'),(REQUEST,receipt+'a')]:
            self.assertEqual(self.client.post('/api/explain',json=dict(draw=draw,receipt=token,cloud_consent=True)).status_code,403)
        self.clock[0]+=86401
        self.assertEqual(self.client.post('/api/explain',json=dict(draw=REQUEST,receipt=receipt,cloud_consent=True)).status_code,403)
        self.assertFalse(self.calls)

    def test_invalid_provider_references_are_never_displayed(self):
        def invalid(prompt): return dict(cards=[dict(card_id='invented',rule_id='invented',reflection='invented')]*3),{}
        with TestClient(create_app(provider=invalid)) as client:
            response=client.post('/api/readings',json=REQUEST).json()
            answer=client.post('/api/explain',json=dict(draw=REQUEST,receipt=response['receipt'],cloud_consent=True))
            self.assertEqual(answer.status_code,422)

    def test_rate_limit(self):
        for _ in range(30):self.assertEqual(self.draw().status_code,200)
        self.assertEqual(self.draw().status_code,429)
        self.clock[0]+=61
        self.assertEqual(self.draw().status_code,200)

    def test_native_no_ai_dependency(self):
        self.assertEqual(native(Draw(**REQUEST))['replay']['seed'],REQUEST['seed'])

if __name__=='__main__':unittest.main()
