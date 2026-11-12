import base64,io,json,tempfile,unittest
from unittest.mock import patch
from PIL import Image
from fastapi.testclient import TestClient
from workbench import vision
from workbench.api import create_app
class VisionBoundaryTests(unittest.TestCase):
    def test_nested_model_fields_are_validated_without_fabrication(self):
        response={'message':{'content':json.dumps(dict(usable=True,life=dict(presence='present')))}}
        with patch.object(vision,'ensure_runtime',return_value='pinned'),patch.object(vision,'call',return_value=response):
            result=vision.analyze(self.payload())
        lines=result['request']['input']['hands'][0]['lines']
        self.assertEqual(lines['life']['presence'],'present');self.assertEqual(lines['heart']['presence'],'unknown')
    def test_monthly_real_input_builder_exact_drift(self):
        with tempfile.TemporaryDirectory() as directory,TestClient(create_app(directory),base_url='http://127.0.0.1') as client:
            q=dict(rows='2026-01, 10\n2026-02, 12\n2026-03, 14',units='counts',source='My observations',self_authored=True,model='drift',horizon=1)
            r=client.post('/api/intake/monthly',json=q);self.assertEqual(r.status_code,200,r.text)
            result=client.post('/api/validate',json=r.json()['request']).json()['invocation']['native_output']
            self.assertEqual(result['result']['cells'][0]['prediction']['exact'],'16')
            q['self_authored']=False;self.assertEqual(client.post('/api/intake/monthly',json=q).status_code,422)
    def payload(self):
        b=io.BytesIO();Image.new('RGB',(80,80),'white').save(b,format='PNG')
        return dict(image=base64.b64encode(b.getvalue()).decode(),side='left',dominance='right',consent=True)
    def response(self,usable=True,observations=None):return {'message':{'content':json.dumps(dict(usable=usable,observations=observations or {}))}}
    def test_permission_before_inference(self):
        q=self.payload();q['consent']=False
        with patch.object(vision,'call') as call:
            with self.assertRaises(ValueError):vision.analyze(q)
            call.assert_not_called()
    def test_unreadable_photo_rejects(self):
        q=self.payload();q['image']=base64.b64encode(b'not an image').decode()
        with self.assertRaises(ValueError):vision.analyze(q)
    def test_unknowns_stay_unknown_and_no_measurements(self):
        with patch.object(vision,'ensure_runtime',return_value='pinned'),patch.object(vision,'call',return_value=self.response()):r=vision.analyze(self.payload())
        hand=r['request']['input']['hands'][0]
        self.assertEqual(hand['side'],'left');self.assertNotIn('shape',hand);self.assertNotIn('proportions_mm',hand)
        self.assertTrue(all(v=='unknown' for line in hand['lines'].values() for v in line.values()));self.assertFalse(r['provenance']['photo_stored'])
    def test_non_palm_rejects(self):
        with patch.object(vision,'ensure_runtime',return_value='pinned'),patch.object(vision,'call',return_value=self.response(False)):
            with self.assertRaises(ValueError):vision.analyze(self.payload())
    def test_unsupported_observations_reject(self):
        with patch.object(vision,'ensure_runtime',return_value='pinned'),patch.object(vision,'call',return_value=self.response(observations={'life.length':'will live to 90'})):
            with self.assertRaises(ValueError):vision.analyze(self.payload())
    def test_no_image_in_public_receipt(self):
        with tempfile.TemporaryDirectory() as directory,TestClient(create_app(directory),base_url='http://127.0.0.1') as client,patch.object(vision,'ensure_runtime',return_value='pinned'),patch.object(vision,'call',return_value=self.response()):
            q=self.payload();r=client.post('/api/vision/palm',json=q);self.assertEqual(r.status_code,200,r.text);d=r.json();self.assertNotIn(q['image'],r.text)
            body=dict(request=d['request'],origin='manual',vision=dict(token=d['review_token'],reviewed=False))
            headers={'Idempotency-Key':'test-vision-review'};self.assertEqual(client.post('/api/sessions',json=body,headers=headers).status_code,422)
            body['vision']['reviewed']=True;r=client.post('/api/sessions',json=body,headers=headers);self.assertEqual(r.status_code,200,r.text);self.assertTrue(r.json()['vision']['reviewed']);self.assertIsNone(r.json()['result']['native_error'])
    def test_all54_intake_profiles(self):
        from pathlib import Path
        r=json.loads((Path(__file__).parents[1]/'input-workflows.json').read_text(encoding='utf-8'));self.assertEqual(len(r['entries']),54)
        for e in r['entries'].values():self.assertTrue(e['prompt']);self.assertTrue(e['important_user_fields']);self.assertTrue(e['real_data_limitations'])
    def test_intake_cannot_change_engine(self):
        d=dict(sample=dict(technique_id=4,operation='numerology'),workflow=dict(important_user_fields=['name'],real_data_limitations='symbolic'))
        with patch.object(vision,'ensure_runtime',return_value='pinned'),patch.object(vision,'call',return_value={'message':{'content':json.dumps(dict(request=dict(technique_id=9,operation='face'),missing_information=[]))}}):
            with self.assertRaises(ValueError):vision.prepare_input(d,{'name':'test'})
