"""Real bounded API timings and independent native parity for 1/7/30-day windows."""
from pathlib import Path
from time import perf_counter
from datetime import datetime
import copy
import json
from fastapi.testclient import TestClient
from fate.api import create_app
from future.natal import SkyfieldEphemeris
from future.knowledge import Registry
from future.transits import forecast
from future.forecast_report import present
from future.western import load_context,interpreter,traditional_configuration_context

ROOT=Path(__file__).resolve().parents[1]


def main():
    source=json.loads((ROOT/'fate/evidence/western-engine.json').read_text(encoding='utf-8'))
    receipt=dict(scope='Synthetic QA natal moment. Quiet sequential bounded subprocess API timings; no native mocks, provider calls or personal-event validation.',start='2026-11-19T00:00:00Z',profiles=[])
    with TestClient(create_app()) as client:
        envelope=client.post('/api/western',json=source['input']).json()
        for days in (1,7,30):
            t=perf_counter();response=client.post('/api/western/transits',json=dict(origin=envelope['transit_origin'],start=receipt['start'],days=days));elapsed=perf_counter()-t
            assert response.status_code==200,response.text
            actual=response.json();engine=SkyfieldEphemeris(ROOT/'data/de440s.bsp');registry=Registry()
            try:
                n=copy.deepcopy(envelope['transit_origin']['natal']);n['traditional_configuration_context']=traditional_configuration_context(n)
                records=load_context(registry,'modern psychological')
                native=present(forecast(engine,n,datetime.fromisoformat(receipt['start']),days,interpreter=interpreter(records,n)))
                assert actual['report']==json.loads(json.dumps(native))
                for f in actual['sky_samples']:
                    _,positions=engine.positions(datetime.fromisoformat(f['utc']));assert f['planets']==positions
            finally:registry.close();engine.kernel.close()
            row=dict(days=days,wall_seconds=round(elapsed,3),worker=actual['computation'],native_parity=True,daily_sample_parity=True,events=len(actual['report']['exact_events']),configurations=len(actual['report']['configurations']),repeated_sequences=len(actual['report']['presentation']['repeated_patterns']),bytes=len(response.content),raw_birth_fields_present='birth' in actual['report']['natal_summary'])
            assert not row['raw_birth_fields_present'] and row['worker']['seconds']<=62
            receipt['profiles'].append(row);print(row,flush=True)
            (ROOT/f'tmp/turning-parity-{days}.json').write_text(json.dumps(actual),encoding='utf-8')
    (ROOT/'fate/evidence/turning-computation.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
