"""Summarize independent fixture error; no claims of historical judgment validity."""
from pathlib import Path
from datetime import datetime
import json
from future.natal import SkyfieldEphemeris,signed
from future.horary import assess,planetary_hour

def run():
    f=json.loads(Path('tests/fixtures/horary_reference.json').read_text())
    e=SkyfieldEphemeris('data/de440s.bsp');cases=[]
    try:
        for c in f['cases']:
            utc=datetime.fromisoformat(c['utc'])
            r=assess(e,'Illustrative advice-intent question','advice-intent',c['utc'][:-6],'UTC',c['latitude'],c['longitude'])
            n=r['question_chart'];events=r['future_motion']['events']
            assert len(events)==len(c['events'])
            for a,b in zip(events,c['events']):
                assert (a['type'],a['bodies'],a.get('angle'))==(b['type'],b['bodies'],b.get('angle'))
            hour=planetary_hour(e,utc,c['latitude'],c['longitude'])
            errors={'max_planet_longitude_error_degrees':max(abs(signed(n['planets'][b]['longitude']-p['longitude'])) for b,p in c['positions'].items()),
                'max_cusp_error_degrees':max(abs(signed(a-b)) for a,b in zip(n['house_cusps'],c['cusps'])),
                'max_motion_event_error_seconds':max(abs((datetime.fromisoformat(a['utc'])-utc).total_seconds()-b['seconds_from_start']) for a,b in zip(events,c['events'])),
                'max_rise_set_error_seconds':max(abs((datetime.fromisoformat(hour[k+'_utc'])-utc).total_seconds()-c[k+'_seconds_from_start']) for k in ('sunrise','sunset','next_sunrise')),
                'mean_node_error_degrees':abs(signed(r['nodes']['positions']['North Node']['longitude']-c['mean_node_longitude']))}
            assert errors['max_planet_longitude_error_degrees']<f['longitude_tolerance_degrees']
            assert errors['max_cusp_error_degrees']<f['angle_tolerance_degrees']
            assert errors['max_motion_event_error_seconds']<f['event_tolerance_seconds']
            assert errors['max_rise_set_error_seconds']<120 and errors['mean_node_error_degrees']<.02
            cases.append(dict(utc=c['utc'],latitude=c['latitude'],longitude=c['longitude'],errors=errors,
                motion_events=len(events),classification=r['classification']))
    finally:e.kernel.close()
    out={'technique_id':5,'oracle':f['oracle'],'fixture':'tests/fixtures/horary_reference.json','cases':cases,
         'numerical_result':'pass within declared tolerances; convergence is not absolute timing uncertainty',
         'source_examples':'Lilly p107 moiety,p112 reception,pp483–485 unequal hours; Cambridge pp200–201 documentary only',
         'historical_fidelity':'partial: source-specific p194 testimonies calculated, full caution clearance and same-category published validation unresolved',
         'core_v1_acceptance':'not met; retain Developing and do not start Technique6',
         'predictive_validity':'not established or quantified'}
    Path('data/horary-validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':run()
