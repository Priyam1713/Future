"""Numerical Moon-to-moving-planet contacts; no inferred historical prohibitions."""
from datetime import timedelta, timezone
from functools import lru_cache
import math
from .natal import signed
from .transits import roots, branches, phase

CLASSICAL = ('Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn')

def sequence(e, start, days=4):
    if start.tzinfo is None or not 0 < days <= 8:
        raise ValueError('Aware start and horizon in (0,8] days required')
    start = start.astimezone(timezone.utc)
    end = start + timedelta(days=days)
    times = [start + timedelta(hours=i) for i in range(math.ceil(days*24))] + [end]
    @lru_cache(maxsize=8192)
    def lon(body, t): return float(e.longitudes(body, [t])[0])
    def speed(body, t):
        return signed(lon(body,t+timedelta(minutes=1))-lon(body,t-timedelta(minutes=1)))*720
    moon = e.longitudes('Moon',times)
    events=[]
    for boundary in range(0,360,30):
        for t in roots(times,moon,boundary,lambda d:lon('Moon',d)):
            events.append({'type':'moon_ingress','utc':t.isoformat(),'entering_sign':int((lon('Moon',t+timedelta(seconds=1)))//30)})
    for body in CLASSICAL:
        relative=(moon-e.longitudes(body,times))%360
        for angle in (0,60,90,120,180):
            for branch in branches(angle):
                for t in roots(times,relative,branch%360,lambda d,b=body:(lon('Moon',d)-lon(b,d))%360):
                    events.append({'type':'exact_aspect','utc':t.isoformat(),'target':body,'aspect_degrees':angle,
                        'branch_degrees':branch,'residual_degrees':abs(signed(lon('Moon',t)-lon(body,t)-branch)),
                        'target_retrograde':speed(body,t)<0,
                        'phase_before':phase(signed(lon('Moon',t-timedelta(minutes=1))-lon(body,t-timedelta(minutes=1))-branch),speed('Moon',t)-speed(body,t)),
                        'phase_after':phase(signed(lon('Moon',t+timedelta(minutes=1))-lon(body,t+timedelta(minutes=1))-branch),speed('Moon',t)-speed(body,t))})
        # A target station is reported, never assumed to cancel a faster Moon's contact.
        tt=e.ts.from_datetimes(times).tt
        velocities=((e.longitudes_at_tt(body,tt+1/1440)-e.longitudes_at_tt(body,tt-1/1440)+180)%360-180)*720
        for t in roots(times,velocities,0,lambda d,b=body:speed(b,d)):
            events.append({'type':'target_station','utc':t.isoformat(),'target':body})
    events.sort(key=lambda x:(x['utc'],x['type'],x.get('target','')))
    ingress=next((x['utc'] for x in events if x['type']=='moon_ingress'),None)
    contacts=[x for x in events if x['type']=='exact_aspect' and (ingress is None or x['utc']<ingress)]
    applications=[]
    for i,event in enumerate(contacts):
        item=dict(event,intervening_contacts=[{'utc':x['utc'],'target':x['target'],'aspect_degrees':x['aspect_degrees']} for x in contacts[:i]],
                  perfection='computed before next lunar ingress',historical_prohibition='indeterminate: intervening contact alone is not a sourced prohibition rule')
        applications.append(item)
    return {'start_utc':start.isoformat(),'end_exclusive_utc':end.isoformat(),'next_moon_ingress_utc':ingress,
        'events':events,'contacts_before_ingress':applications,
        'method':{'scan_hours':1,'root_bracket_seconds':.25,'coordinates':'apparent geocentric tropical ecliptic longitude of date'},
        'limitations':['Finite horizon; a contact after ingress is not certified as same-sign perfection.',
                      'Aspect sequence is geometry, not adjudication of reception, translation, collection or prohibition.',
                      'Unseen multiple reversals within a scan hour are outside completeness guarantees.']}
