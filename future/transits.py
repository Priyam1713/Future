"""Transit-to-fixed-natal longitude contacts, independent of interpretations."""
from datetime import datetime, timedelta, timezone
import math
from functools import lru_cache
from .natal import signed, aspects, DEFAULT_ORBS
from .houses import house_for

def phase(error, speed, exact_tolerance=1e-5):
    if abs(error) <= exact_tolerance:
        return 'exact'
    if abs(speed) < 1e-8:
        return 'stationary'
    return 'applying' if error * speed < 0 else 'separating'

def branches(angle):
    return [angle] if angle in (0,180) else [angle,-angle]

def orb_intervals(times,samples,target,orb,evaluate):
    """Exact numerical orb boundary crossings, clipped to the requested window."""
    if orb==0: return []
    cuts=sorted(set([times[0],times[-1]]+
          roots(times,samples,(target-orb)%360,evaluate)+roots(times,samples,(target+orb)%360,evaluate)))
    spans=[]
    for a,b in zip(cuts,cuts[1:]):
        if abs(signed(evaluate(a+(b-a)/2)-target))<=orb:
            if spans and spans[-1][1]==a: spans[-1]=(spans[-1][0],b)
            else: spans.append((a,b))
    return [{'start_utc':a.isoformat(),'end_utc':b.isoformat(),'hours_in_window':(b-a).total_seconds()/3600,
             'start_clipped':a==times[0],'end_clipped':b==times[-1]} for a,b in spans]

def roots(sample_times, sample_longitudes, target, evaluate):
    """Bracket real angular crossings; reject the antipodal wrap discontinuity.

    Refine sampled reversals before bracketing so near-station repeated contacts
    are retained. Multiple unseen reversals inside one scan cell remain unsupported.
    """
    found=[]
    pairs=list(zip(sample_times,map(float,sample_longitudes)))
    additions=[]
    for (a,la),(m,lm),(b,lb) in zip(pairs,pairs[1:],pairs[2:]):
        da,db=signed(lm-la),signed(lb-lm)
        if da*db<0:
            left,right=a,b
            maximize=da>0
            for _ in range(32):
                p=left+(right-left)/3; q=right-(right-left)/3
                vp,vq=signed(evaluate(p)-lm),signed(evaluate(q)-lm)
                if (vp<vq)==maximize: left=p
                else: right=q
            station=left+(right-left)/2
            value=evaluate(station)
            additions.append((station,value))
            if abs(signed(value-target))<1e-8: found.append(station)
    pairs=sorted(pairs+additions)
    sample_times=[p[0] for p in pairs]
    sample_longitudes=[p[1] for p in pairs]
    for a,b,la,lb in zip(sample_times,sample_times[1:],sample_longitudes,sample_longitudes[1:]):
        ea,eb=signed(float(la)-target),signed(float(lb)-target)
        if abs(ea)<1e-9:
            found.append(a)
        if ea*eb < 0 and abs(ea-eb)<180:
            left,right=a,b
            while (right-left).total_seconds()>.25:
                mid=left+(right-left)/2
                em=signed(evaluate(mid)-target)
                if ea*em<=0: right=mid
                else: left=mid; ea=em
            found.append(left+(right-left)/2)
    # Half-open windows: start included, end excluded.
    unique=[]
    for t in sorted(found):
        if t < sample_times[-1] and (not unique or (t-unique[-1]).total_seconds()>1): unique.append(t)
    return unique

def forecast(ephemeris, natal, start, days=30, orbs=None, bodies=None, interpreter=None):
    if start.tzinfo is None: raise ValueError('Forecast start requires an explicit UTC offset')
    start=start.astimezone(timezone.utc)
    if isinstance(days,bool) or not isinstance(days,int) or not 1<=days<=30:
        raise ValueError('Forecast days must be an integer in 1..30')
    orbs=DEFAULT_ORBS if orbs is None else orbs
    aspects({},orbs)  # reuse validation
    bodies=list(natal['planets']) if bodies is None else list(bodies)
    if len(set(bodies))!=len(bodies) or any(b not in natal['planets'] for b in bodies):
        raise ValueError('Select unique transiting bodies supported by the natal tradition')
    end=start+timedelta(days=days)
    times=[start+timedelta(hours=3*i) for i in range(days*8+1)]
    targets={n:p['longitude'] for n,p in natal['planets'].items()}
    targets.update(natal['angles'])
    _,current=ephemeris.positions(start)
    events=[]; active=[]; configurations=[]
    for body in bodies:
        samples=ephemeris.longitudes(body,times)
        @lru_cache(maxsize=8192)
        def evaluate(t): return float(ephemeris.longitudes(body,[t])[0])
        speed=current[body]['speed_degrees_per_day']
        for target,lon in targets.items():
            for angle,orb in orbs.items():
                for branch in branches(angle):
                    error=signed(current[body]['longitude']-lon-branch)
                    cid=f'{body}:{target}:{angle}:{branch}'
                    common={'configuration_id':cid,'transiting':body,'natal_target':target,'aspect_degrees':angle,'branch_degrees':branch}
                    context={'phase':phase(error,speed),'retrograde':speed<0,
                             'natal_house':natal['planets'].get(target,{}).get('house'),
                             'dignity':natal.get('traditional_configuration_context',{}).get('planets',{}).get(target,{}).get('dignities',[]),
                             'rulership':natal['settings']['rulership']}
                    interpretation=interpreter(body,target,angle,context) if interpreter else []
                    if abs(error)<=orb:
                        active.append(dict(common,orb=abs(error),phase=phase(error,speed),retrograde=speed<0,
                                           speed_degrees_per_day=speed,near_station=abs(speed)<.01,
                                           interpretations=interpretation))
                    contacts=roots(times,samples,(lon+branch)%360,evaluate)
                    spans=orb_intervals(times,samples,(lon+branch)%360,orb,evaluate)
                    if spans or contacts:
                        configurations.append(dict(common,orb_limit=orb,intervals=spans,
                            hours_in_window=sum(s['hours_in_window'] for s in spans),interpretations=interpretation))
                    for t in contacts:
                        before,after=t-timedelta(minutes=1),t+timedelta(minutes=1)
                        motion=signed(evaluate(after)-evaluate(before))*720
                        residual=abs(signed(evaluate(t)-lon-branch))
                        exact_context=dict(context,phase='exact',retrograde=motion<0)
                        events.append(dict(common,exact_utc=t.isoformat(),phase='exact',retrograde=motion<0,
                            speed_degrees_per_day=motion,
                            near_station=abs(motion)<.01,
                            transit_natal_house=house_for(evaluate(t),natal['house_cusps']),
                            longitude=evaluate(t),angular_residual_degrees=residual,
                            interpretation_context=exact_context,
                            interpretations=interpreter(body,target,angle,exact_context) if interpreter else []))
    events.sort(key=lambda e:(e['exact_utc'],e['transiting'],e['natal_target'],e['aspect_degrees']))
    for i,event in enumerate(events,1): event['id']=f'event-{i:04d}'
    groups={}
    for event in events:
        key=(event['transiting'],event['natal_target'],event['aspect_degrees'],event['branch_degrees'])
        groups.setdefault(key,[]).append(event)
    for group in groups.values():
        for index,event in enumerate(group,1):
            event['pass_in_window']=index
            event['passes_in_window']=len(group)
    return {'technique_id':1,'application':'transits','natal_summary':natal,
            'window':{'start_utc':start.isoformat(),'end_utc':end.isoformat(),'end_exclusive':True},
            'current_planets':{b:current[b] for b in bodies},'active_at_start':active,'exact_events':events,
            'configurations':configurations,
            'precision':{'root_bracket_seconds':.25,'scan_hours':3,'coordinate_validation_tolerance_degrees':.01,
                         'near_station_speed_threshold_degrees_per_day':.01,
                         'note':'Root precision is numerical convergence, not absolute timing accuracy; near stations timing is less certain.'},
            'predictive_validity':'Traditional symbolic interpretation; no calibrated probability or demonstrated personal-event accuracy.',
            'limitations':['Fixed natal positions and angles; no progressed targets.',
                           'Sampled stations are refined; multiple unseen reversals in a three-hour scan cell may be missed.',
                           'Exact times are astronomical contacts, not promises of life events.'],
            'orbs':orbs,'reproducibility':natal['reproducibility']}
