"""Opt-in real local model smoke test; not an extraction accuracy evaluation."""
import base64,io,json,tempfile,time
from pathlib import Path
from PIL import Image
from fastapi.testclient import TestClient
from .api import create_app

def main():
    start=time.monotonic();root=Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory() as home,TestClient(create_app(home),base_url='http://127.0.0.1') as client:
        q=dict(image=base64.b64encode((root/'tests/assets/palm-cc0.png').read_bytes()).decode(),side='left',dominance='unknown',consent=True)
        response=client.post('/api/vision/palm',json=q);assert response.status_code==200,response.text
        palm=response.json()
        response=client.post('/api/sessions',json=dict(request=palm['request'],origin='manual',vision=dict(token=palm['review_token'],reviewed=True)),headers={'Idempotency-Key':'live-fixture-only'})
        assert response.status_code==200,response.text
        assert response.json()['result']['native_error'] is None
        blank=io.BytesIO();Image.new('RGB',(300,300),'white').save(blank,format='PNG');q['image']=base64.b64encode(blank.getvalue()).decode()
        response=client.post('/api/vision/palm',json=q)
        assert response.status_code==422 and 'clear open palm' in response.json()['error'],response.text
        response=client.post('/api/intake/prepare',json=dict(technique_id=18,answers={'Question':'How should I approach studying?','Six line values':'From bottom to top: 7, 8, 7, 8, 7, 8','Casting method':'manual','Reading policy':'Use the supported core default'}))
        assert response.status_code==200,response.text
        draft=response.json();assert not draft['missing_information'] and draft['validation']['native_error'] is None,draft
        assert draft['request']['input']['lines']==[7,8,7,8,7,8]
        receipt=dict(passed=True,scope='One public palm fixture, blank-image rejection, reviewed native execution and one I Ching transcription; not accuracy certification',provenance=palm['provenance'],palm_observations=palm['request']['input'],blank_rejected=True,iching_lines_preserved=True,elapsed_seconds=round(time.monotonic()-start,2))
        (root/'live-vision-acceptance.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
        print('Live local model smoke passed',flush=True)

if __name__=='__main__':main()
