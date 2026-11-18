"""Explicit opt-in live check using a synthetic developer question, never user data."""
import json
from pathlib import Path
from fastapi.testclient import TestClient
from .api import create_app

def main():
    draw=dict(spread='one',seed='FATE-live-provider-acceptance-v1',question='What symbolic themes invite reflection on a creative project?',reversals=True)
    with TestClient(create_app()) as client:
        envelope=client.post('/api/readings',json=draw).json()
        response=client.post('/api/explain',json=dict(draw=draw,receipt=envelope['receipt'],cloud_consent=True))
        assert response.status_code==200,response.text
        body=response.json()
        assert body['cards'][0]['card_id']==envelope['result']['readings'][0]['card']['id']
        assert body['cards'][0]['rule_id']==envelope['result']['readings'][0]['direct_component']['rule_id']
        assert client.post('/api/readings',json=draw).json()['result']==envelope['result']
        report=dict(passed=True,scope='One live Gemini response to a synthetic developer question with explicit cloud consent. No user information. Reference/shape checks, not semantic or predictive validation.',draw=draw,native_card=envelope['result']['readings'][0],commentary=body)
        (Path(__file__).parent/'live-gemini-acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
        print('Live commentary passed; native output unchanged; '+body['provenance']['model'])

if __name__=='__main__':main()
