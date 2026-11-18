import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from workbench.api import create_app
from workbench.gemini import assist
from future.lab.common import ROOT
class GeminiTests(unittest.TestCase):
 def test_all54_input_routes_review_validation(self):
  samples=json.loads((ROOT/'data/future-lab-invocation-examples.json').read_text(encoding='utf-8'))['entries']
  with tempfile.TemporaryDirectory() as directory,TestClient(create_app(directory),base_url='http://127.0.0.1') as client:
   for key,item in samples.items():
    with self.subTest(technique=key),patch('workbench.gemini.generate',return_value=({'request':item['request'],'missing_information':[]},{'provider':'gemini','model':'mock'})):
     r=client.post('/api/ai/assist',json=dict(technique_id=int(key),text='Explicit synthetic test data',cloud_consent=True))
     self.assertEqual(r.status_code,200,r.text[:500]);self.assertIsNone(r.json()['validation']['native_error'])
   self.assertEqual(client.get('/api/records').json(),[])
 def test_cloud_permission_and_followups(self):
  detail=dict(sample=dict(technique_id=4,operation='numerology'),workflow=dict(real_data_limitations='scope',important_user_fields=[]))
  with patch('workbench.gemini.generate') as generate:
   with self.assertRaises(ValueError):assist(detail,dict(text='test'))
   generate.assert_not_called()
  with patch('workbench.gemini.generate',return_value=({'request':None,'missing_information':['What is your birth date?']},{})):
   self.assertIsNone(assist(detail,dict(text='unknown',cloud_consent=True))['request'])
 def test_explanations_use_saved_result_and_guard_blind(self):
  sample=json.loads((ROOT/'data/future-lab-invocation-examples.json').read_text(encoding='utf-8'))['entries']['4']['request']
  with tempfile.TemporaryDirectory() as directory,TestClient(create_app(directory),base_url='http://127.0.0.1') as client:
   participant=client.post('/api/participants',json=dict(consent=True,scopes=['blind'],techniques=[4],retain_frozen=False),headers={'Idempotency-Key':'participant-test'}).json()
   case=client.post('/api/cases',json=dict(participant_id=participant['id'],title='Test'),headers={'Idempotency-Key':'case-test'}).json()
   session=client.post('/api/sessions',json=dict(request=sample,mode='blind',case_id=case['id'],hidden_answer='secret'),headers={'Idempotency-Key':'blind-test'}).json()
   with patch('workbench.gemini.generate') as generate:
    r=client.post('/api/ai/assist',json=dict(technique_id=4,mode='explain',session_id=session['id'],cloud_consent=True))
    self.assertEqual(r.status_code,422);generate.assert_not_called()


