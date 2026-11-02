"""Independent Swiss/Moshier daily search, TT bisection, and return charts."""
from pathlib import Path
import json
import swisseph as s
cases=[]
for birth,year,lat,lon in [((1990,7,15,9),2026,28.6139,77.209),((1990,7,15,9),2024,-33.9,151.2),
                         ((2000,2,29,12),2025,51.5,0),((1999,12,31,23),2000,40.7,-74),((1999,12,31,23),2001,-33.9,151.2)]:
    y,m,d,h=birth
    b=s.utc_to_jd(y,m,d,int(h),0,0)[0]
    target=s.calc(b,s.SUN,s.FLG_MOSEPH)[0][0]
    start=s.julday(year,1,1,0);end=s.julday(year+1,1,1,0)
    def f(jd):return (s.calc(jd,s.SUN,s.FLG_MOSEPH)[0][0]-target+180)%360-180
    candidates=[]
    for i in range(int(end-start)):
        a,bb=start+i,start+i+1;fa,fb=f(a),f(bb)
        if fa*fb<0 and abs(fa-fb)<180:
            for _ in range(50):
                mid=(a+bb)/2
                if f(mid)>0:bb=mid
                else:a=mid
            candidates.append((a+bb)/2)
    assert len(candidates)==1
    jd=candidates[0];ut=jd-s.deltat(jd)
    positions=[s.calc(jd,i,s.FLG_MOSEPH)[0][0] for i in range(10)]
    cases.append({'birth':birth,'year':year,'latitude':lat,'longitude':lon,'jd_tt':jd,'longitudes':positions,
                  'placidus_cusps':list(s.houses(ut,lat,lon,b'P')[0])})
Path('tests/fixtures/solar_return_reference.json').write_text(json.dumps({'oracle':'Swiss Ephemeris 2.10.3.2 Moshier, TT root; UT1 house chart via Swiss delta-T','cases':cases},indent=2))
