"""Optional Swiss numerical oracle. No Future/Skyfield imports or production use.

solcross() locates solar ingresses independently; cycle roots use hourly Swiss
TT samples and scalar bisection. Swiss retains its separate dual-license terms.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,math
import swisseph as s

NAMES=('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune')
FLAGS=s.FLG_MOSEPH|s.FLG_SPEED
def signed(x):return (x+180)%360-180
def utc(jd):
    y,m,d,h,minute,second=s.jdet_to_utc(jd)
    # Microsecond output from independent TT→UTC conversion.
    return datetime(y,m,d,h,minute,tzinfo=timezone.utc).timestamp()+second
def iso(jd):return datetime.fromtimestamp(utc(jd),timezone.utc).isoformat()
def jd_utc(text):
    d=datetime.fromisoformat(text)
    return s.utc_to_jd(d.year,d.month,d.day,d.hour,d.minute,d.second)[0]

def build():
    years=[]
    for year in (2000,2024,2026):
        start=jd_utc(f'{year}-01-01T00:00:00+00:00');events=[]
        for target in (0,90,180,270):
            tt=s.solcross(target,start,s.FLG_MOSEPH)
            y,m,d,h,minute,second=s.jdet_to_utc(tt)
            _,ut=s.utc_to_jd(y,m,d,h,minute,second)
            positions={n:{'longitude':s.calc(tt,b,FLAGS)[0][0],'retrograde':s.calc(tt,b,FLAGS)[0][3]<0} for b,n in enumerate(NAMES)}
            sites=[]
            for lat,lon in [(51.5,0),(-33.8688,151.2093)]:
                cusps,angles=s.houses_ex(ut,lat,lon,b'P')
                sites.append({'latitude':lat,'longitude':lon,'cusps':list(cusps),'ascendant':angles[0],'midheaven':angles[1]})
            events.append({'target':target,'utc':iso(tt),'positions':positions,'sites':sites})
        years.append({'year':year,'events':events})
    cycles=[]
    for start,end in [('2020-12-01T00:00:00+00:00','2021-01-01T00:00:00+00:00'),
                      ('1980-12-01T00:00:00+00:00','1981-08-01T00:00:00+00:00')]:
        base,stop=jd_utc(start),jd_utc(end);grid=[base+i/24 for i in range(math.ceil((stop-base)*24))]+[stop]
        def pos(t,b):return s.calc(t,b,FLAGS)[0]
        samples={b:[pos(t,b) for t in grid] for b in (s.JUPITER,s.SATURN)}
        events=[]
        def solve(values,evaluate,level,kind,**extra):
            for a,b,va,vb in zip(grid,grid[1:],values,values[1:]):
                fa,fb=signed(va-level),signed(vb-level)
                if fa==0:events.append(dict(type=kind,utc=iso(a),**extra));continue
                if fa*fb>=0 or abs(fa-fb)>180:continue
                for _ in range(35):
                    m=(a+b)/2;fm=signed(evaluate(m)-level)
                    if fa*fm<=0:b=m
                    else:a=m;fa=fm
                events.append(dict(type=kind,utc=iso((a+b)/2),**extra))
        solve([a[0]-b[0] for a,b in zip(samples[5],samples[6])],lambda t:pos(t,5)[0]-pos(t,6)[0],0,'conjunction')
        for body,name in [(5,'Jupiter'),(6,'Saturn')]:
            solve([p[3] for p in samples[body]],lambda t,b=body:pos(t,b)[3],0,'station',body=name)
            for boundary in range(0,360,30):
                solve([p[0] for p in samples[body]],lambda t,b=body:pos(t,b)[0],boundary,'ingress',body=name,target_longitude=boundary)
        cycles.append({'start':start,'end':end,'events':sorted(events,key=lambda x:(x['utc'],x.get('body',''),x['type']))})
    result={'oracle':f'Swiss Ephemeris {s.version}, Moshier; apparent geocentric tropical; Placidus, own UTC/TT/UT conversion',
        'generator':'scripts/build_mundane_reference.py; no Future or Skyfield imports',
        'tolerances':{'ingress_seconds':90,'planet_degrees':.01,'cusp_degrees':.03,'cycle_event_seconds':120,
            'conjunction_angle_degrees':.0002},
        'conjunction_time_comparison':'Subarcsecond(.0002deg) relative-longitude allowance divided by measured relative speed gives a local timing-comparison bound. Slow repeated contacts magnify DE440/Moshier coordinate differences; numerical root precision is separate. Stations/ingresses use120seconds.',
        'limits':'Modern numerical comparison only; does not validate historical calendar reconstruction or symbolic forecasts.',
        'years':years,'cycles':cycles}
    Path('tests/fixtures/mundane_swiss.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':build()
