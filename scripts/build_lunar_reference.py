"""Independent Swiss/Moshier oracle: moving-target contacts, ingresses, stations.
No Future imports; 15-minute brackets and scalar bisection in TT.
"""
from datetime import datetime,timedelta,timezone
from pathlib import Path
import json
import swisseph as s

def signed(x):return (x+180)%360-180
cases=[]
for start in ('2026-11-01T00:00:00+00:00','2024-04-01T00:00:00+00:00','2000-02-28T00:00:00+00:00'):
    date=datetime.fromisoformat(start)
    base=s.utc_to_jd(date.year,date.month,date.day,0,0,0)[0]
    events=[]
    def value(t,body):return s.calc(base+t,body,s.FLG_MOSEPH|s.FLG_SPEED)[0]
    def solve(f,level,kind,**extra):
        for i in range(4*96):
            a,b=i/96,(i+1)/96;fa,fb=signed(f(a)-level),signed(f(b)-level)
            if fa*fb>=0 or abs(fa-fb)>180:continue
            for _ in range(36):
                m=(a+b)/2;fm=signed(f(m)-level)
                if fa*fm<=0:b=m
                else:a=m;fa=fm
            events.append(dict(type=kind,seconds_from_start=(a+b)/2*86400,**extra))
    for boundary in range(0,360,30):solve(lambda t:value(t,1)[0],boundary,'moon_ingress')
    for name,body in [('Sun',0),('Mercury',2),('Venus',3),('Mars',4),('Jupiter',5),('Saturn',6)]:
        for angle in (0,60,90,120,180):
            for branch in ([angle] if angle in (0,180) else [angle,-angle]):
                solve(lambda t,b=body:value(t,1)[0]-value(t,b)[0],branch,'exact_aspect',target=name,aspect_degrees=angle)
        solve(lambda t,b=body:value(t,b)[3],0,'target_station',target=name)
    cases.append({'start_utc':start,'events':sorted(events,key=lambda x:x['seconds_from_start'])})
Path('tests/fixtures/lunar_reference.json').write_text(json.dumps({'oracle':'Swiss Ephemeris 2.10.3.2 Moshier; TT elapsed seconds from UTC start; no Future imports','tolerance_seconds':120,'cases':cases},indent=2))
