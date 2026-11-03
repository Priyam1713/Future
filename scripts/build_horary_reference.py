"""Optional Swiss/Moshier verification oracle, never imported by production.

Independent 15-minute TT scan and scalar bisection; no Future imports.
Swiss Ephemeris use/distribution remains subject to its own dual license.
"""
from datetime import datetime
from itertools import combinations
from pathlib import Path
import json
import swisseph as s

NAMES=('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn')
def signed(x):return (x+180)%360-180

def build():
    cases=[]
    for date,lat,lon in [('2026-11-03T06:30:00+00:00',28.6139,77.209),
                         ('2024-04-01T00:00:00+00:00',-33.8688,151.2093),
                         ('2000-02-28T00:00:00+00:00',51.5074,-.1278)]:
        d=datetime.fromisoformat(date)
        base,ut=s.utc_to_jd(d.year,d.month,d.day,d.hour,d.minute,d.second)
        def value(t,b):return s.calc(base+t,b,s.FLG_MOSEPH|s.FLG_SPEED)[0]
        # Cache scan samples only; roots independently evaluate Swiss positions.
        grid=[[value(i/96,b) for i in range(385)] for b in range(7)]
        events=[]
        def solve(samples,f,target,kind,bodies,**extra):
            for i in range(384):
                a,b=i/96,(i+1)/96;fa,fb=signed(samples[i]-target),signed(samples[i+1]-target)
                if fa*fb>=0 or abs(fa-fb)>180:continue
                for _ in range(35):
                    m=(a+b)/2;fm=signed(f(m)-target)
                    if fa*fm<=0:b=m
                    else:a=m;fa=fm
                events.append(dict(type=kind,bodies=bodies,seconds_from_start=(a+b)*43200,**extra))
        for b,name in enumerate(NAMES):
            for boundary in range(0,360,30):
                solve([x[0] for x in grid[b]],lambda t,b=b:value(t,b)[0],boundary,'ingress',[name])
            if b>1:solve([x[3] for x in grid[b]],lambda t,b=b:value(t,b)[3],0,'station',[name])
        for a,b in combinations(range(7),2):
            for angle in (0,60,90,120,180):
                for branch in ([angle] if angle in (0,180) else [angle,-angle]):
                    solve([x[0]-y[0] for x,y in zip(grid[a],grid[b])],
                          lambda t,a=a,b=b:value(t,a)[0]-value(t,b)[0],branch,'exact_aspect',[NAMES[a],NAMES[b]],angle=angle)
        cusps,angles=s.houses_ex(ut,lat,lon,b'R')
        def rise_set(jd,kind):
            status,result=s.rise_trans(jd,s.SUN,kind,(lon,lat,0),0,15,s.FLG_MOSEPH)
            if status!=0:raise ValueError('Reference rise/set unavailable')
            return result[0]
        rise=rise_set(ut-1,s.CALC_RISE)
        set_=rise_set(rise+1e-6,s.CALC_SET);next_rise=rise_set(rise+1e-6,s.CALC_RISE)
        cases.append({'utc':date,'latitude':lat,'longitude':lon,
            'positions':{n:{'longitude':value(0,b)[0],'retrograde':value(0,b)[3]<0} for b,n in enumerate(NAMES)},
            'mean_node_longitude':s.calc(base,s.MEAN_NODE,s.FLG_MOSEPH)[0][0],
            'sunrise_seconds_from_start':(rise-ut)*86400,'sunset_seconds_from_start':(set_-ut)*86400,
            'next_sunrise_seconds_from_start':(next_rise-ut)*86400,
            'cusps':list(cusps),'ascendant':angles[0],'midheaven':angles[1],
            'events':sorted(events,key=lambda x:x['seconds_from_start'])})
    out={'oracle':f'Swiss Ephemeris {s.version}, Moshier apparent tropical geocentric; Regiomontanus; own UTC-to-TT/UT conversion',
         'generator':'scripts/build_horary_reference.py; no Future imports',
         'longitude_tolerance_degrees':.01,'angle_tolerance_degrees':.03,'event_tolerance_seconds':120,
         'rise_model':'Swiss apparent upper limb; standard atmosphere inferred from sea-level altitude,15C;120-second tolerance allows refraction/radius-model differences from Skyfield.',
         'limitations':'Modern independent numerical fixtures, not published historical judgment validation; finite scan may miss unresolved tangencies.',
         'cases':cases}
    Path('tests/fixtures/horary_reference.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
if __name__=='__main__':build()
