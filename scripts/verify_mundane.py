"""Reproduce measured numerical comparisons, separately from symbolic validity."""
from pathlib import Path
from datetime import datetime
import json
from future.natal import SkyfieldEphemeris,signed
from future.mundane import ingresses,conjunctions

def run():
    f=json.loads(Path('tests/fixtures/mundane_swiss.json').read_text())
    usno=json.loads(Path('tests/fixtures/mundane_usno.json').read_text())
    green=json.loads(Path('tests/fixtures/mundane_green_published.json').read_text())
    e=SkyfieldEphemeris('data/de440s.bsp');rows=[];cycles=[];published=[]
    try:
        for year in f['years']:
            for site in year['events'][0]['sites']:
                r=ingresses(e,year['year'],'UTC',site['latitude'],site['longitude'])
                for a,b in zip(r['events'],year['events']):
                    expected=next(s for s in b['sites'] if s['latitude']==site['latitude'] and s['longitude']==site['longitude'])
                    err={'time_seconds':abs((datetime.fromisoformat(a['utc'])-datetime.fromisoformat(b['utc'])).total_seconds()),
                        'planet_degrees':max(abs(signed(a['chart']['planets'][n]['longitude']-p['longitude'])) for n,p in b['positions'].items()),
                        'cusp_degrees':max(abs(signed(x-y)) for x,y in zip(a['chart']['house_cusps'],expected['cusps']))}
                    assert err['time_seconds']<f['tolerances']['ingress_seconds']
                    assert err['planet_degrees']<f['tolerances']['planet_degrees'] and err['cusp_degrees']<f['tolerances']['cusp_degrees']
                    rows.append(dict(year=year['year'],sign=a['sign'],latitude=site['latitude'],longitude=site['longitude'],errors=err))
        r=ingresses(e,2026,'Europe/London',51.5,0)
        for a,b in zip(r['events'],usno['response_selected_seasons']['data']):
            stamp=f"{b['year']}-{b['month']:02}-{b['day']:02}T{b['time']}:00+00:00"
            seconds=(datetime.fromisoformat(a['utc'])-datetime.fromisoformat(stamp)).total_seconds()
            assert abs(seconds)<usno['tolerance_seconds']
            published.append({'sign':a['sign'],'calculated_utc':a['utc'],'usno_utc_minute':stamp,'difference_seconds':seconds})
        for c in f['cycles']:
            r=conjunctions(e,datetime.fromisoformat(c['start']),datetime.fromisoformat(c['end']),'UTC',51.5,0)
            actual=[dict(type='conjunction',utc=x['utc']) for x in r['events']]+r['motion_changes']
            actual.sort(key=lambda x:(x['utc'],x.get('body',''),x['type']))
            assert len(actual)==len(c['events'])
            for a,b in zip(actual,c['events']):
                assert (a['type'],a.get('body'),a.get('target_longitude'))==(b['type'],b.get('body'),b.get('target_longitude'))
                seconds=abs((datetime.fromisoformat(a['utc'])-datetime.fromisoformat(b['utc'])).total_seconds())
                row={'type':a['type'],'body':a.get('body'),'calculated_utc':a['utc'],'difference_seconds':seconds}
                if a['type']=='conjunction':
                    _,p=e.positions(datetime.fromisoformat(b['utc']))
                    error=abs(signed(p['Jupiter']['longitude']-p['Saturn']['longitude']))
                    speed=abs(p['Jupiter']['speed_degrees_per_day']-p['Saturn']['speed_degrees_per_day'])
                    bound=f['tolerances']['conjunction_angle_degrees']/speed*86400+1
                    assert error<f['tolerances']['conjunction_angle_degrees'] and seconds<bound
                    row.update({'relative_longitude_error_degrees':error,'relative_speed_degrees_per_day':speed,'angle_derived_timing_comparison_bound_seconds':bound})
                else:assert seconds<f['tolerances']['cycle_event_seconds']
                cycles.append(row)
        g=ingresses(e,1899,'Europe/London',51.5,0)['events'][0]
        green_comparison={'locator':green['locator'],'calculated_utc_proleptic':g['utc'],'source_time_gmt':green['source_time'],
            'planet_errors_degrees':{b:abs(signed(g['chart']['planets'][b]['longitude']-v)) for b,v in green['longitudes'].items()},
            'result':'PARTIAL agreement only; Saturn discrepancy preserved,not a fully passed historical reconstruction',
            'source_discrepancy':green['source_discrepancy'],'limits':green['limit']}
    finally:e.kernel.close()
    out={'technique_id':6,'oracle':f['oracle'],'ingress_chart_comparisons':rows,'published_usno_2026':published,
        'cycle_events':cycles,'historical_green_comparison':green_comparison,
        'result':'Independent current-era numerical comparisons pass declared bounds; historical discrepancy explicitly retained',
        'validity':'Numerical agreement does not validate symbolic or geopolitical/financial prediction.'}
    Path('data/mundane-validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('Verified',len(rows),'Swiss ingress/site charts,',len(published),'published USNO instants,',len(cycles),'cycle/motion events')
if __name__=='__main__':run()
