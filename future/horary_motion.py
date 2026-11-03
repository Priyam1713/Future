"""Moving classical-planet contacts; geometric evidence, not universal judgments."""
from datetime import datetime,timedelta,timezone
from functools import lru_cache
from itertools import combinations
import math
from .natal import signed
from .transits import roots,branches,phase

CLASSICAL=('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn')
# Explicit first column of Lilly1647 p107. Alternate column is not merged.
ORBS={'Sun':17.,'Moon':12.5,'Mercury':7.,'Venus':8.,'Mars':7.5,'Jupiter':12.,'Saturn':10.}

def contact_roots(times,values,target,evaluate):
    """Refine flat sample pairs that can conceal a symmetric reversal.

    Shared roots already refines ordinary sampled reversals. Equal endpoint
    longitudes require an interior sample before that detection can work.
    This Horary-specific extension leaves existing Western interfaces intact.
    """
    pairs=list(zip(times,map(float,values)))
    extra=[]
    for (a,va),(b,vb) in zip(pairs,pairs[1:]):
        if abs(signed(vb-va))<1e-10:
            m=a+(b-a)/2;extra.append((m,evaluate(m)))
    pairs=sorted(pairs+extra)
    return roots([x[0] for x in pairs],[x[1] for x in pairs],target,evaluate)

def aspect_state(a,b,angle):
    separation=signed(a['longitude']-b['longitude'])
    branch=min(branches(angle),key=lambda x:abs(signed(separation-x)))
    error=signed(separation-branch)
    state=phase(error,a['speed_degrees_per_day']-b['speed_degrees_per_day'])
    ds=(int(a['longitude']//30)-int(b['longitude']//30))%12
    sign_agreement=ds in {0:(0,),60:(2,10),90:(3,9),120:(4,8),180:(6,)}[angle]
    return {'angle':angle,'branch':branch,'orb':abs(error),'moiety':(ORBS[a['name']]+ORBS[b['name']])/2,
        'within_orb':abs(error)<=(ORBS[a['name']]+ORBS[b['name']])/2,'phase':state,
        'sign_agreement':sign_agreement,'post_exact_within_six_arcminutes':state=='separating' and abs(error)<.1,
        'rule_id':'horary.aspect','locator':'Lilly1647 pp107–110',
        'convention':'Phase from relative longitude velocity; classical six-arcminute separation caution separately reported.'}

def motion(e,start,days=4):
    if start.tzinfo is None or isinstance(days,bool) or not isinstance(days,(int,float)) or not 0<days<=8:
        raise ValueError('Aware timestamp and motion horizon in(0,8] days required')
    start=start.astimezone(timezone.utc);end=start+timedelta(days=days)
    if start.year<1851 or end.year>2148:raise ValueError('Horary motion requires1851–2148 for padding')
    times=[start+timedelta(hours=i) for i in range(math.ceil(days*24))]+[end]
    @lru_cache(maxsize=32768)
    def lon(body,t):return float(e.longitudes(body,[t])[0])
    def speed(body,t):return signed(lon(body,t+timedelta(minutes=1))-lon(body,t-timedelta(minutes=1)))*720
    samples={b:e.longitudes(b,times) for b in CLASSICAL}
    events=[]
    for body in CLASSICAL:
        for boundary in range(0,360,30):
            for t in contact_roots(times,samples[body],boundary,lambda t,b=body:lon(b,t)):
                events.append({'type':'ingress','bodies':[body],'utc':t.isoformat(),
                    'entering_sign':int(lon(body,t+timedelta(seconds=1))//30)})
        if body not in ('Sun','Moon'):
            tt=e.ts.from_datetimes(times).tt
            vs=((e.longitudes_at_tt(body,tt+1/1440)-e.longitudes_at_tt(body,tt-1/1440)+180)%360-180)*720
            for t in contact_roots(times,vs,0,lambda t,b=body:speed(b,t)):
                events.append({'type':'station','bodies':[body],'utc':t.isoformat(),'speed_after':speed(body,t+timedelta(minutes=5))})
    for a,b in combinations(CLASSICAL,2):
        relative=(samples[a]-samples[b])%360
        for angle in (0,60,90,120,180):
            for branch in branches(angle):
                for t in contact_roots(times,relative,branch%360,lambda t,a=a,b=b:(lon(a,t)-lon(b,t))%360):
                    error=signed(lon(a,t)-lon(b,t)-branch)
                    events.append({'type':'exact_aspect','bodies':[a,b],'utc':t.isoformat(),'angle':angle,
                        'branch':branch,'residual_degrees':abs(error),
                        'phase_before':phase(signed(lon(a,t-timedelta(minutes=1))-lon(b,t-timedelta(minutes=1))-branch),speed(a,t)-speed(b,t)),
                        'phase_after':phase(signed(lon(a,t+timedelta(minutes=1))-lon(b,t+timedelta(minutes=1))-branch),speed(a,t)-speed(b,t))})
    events.sort(key=lambda x:(x['utc'],x['type'],x['bodies'],x.get('angle',0)))
    for i,event in enumerate(events):event['id']=f'motion-{i+1:04}'
    return {'start_inclusive_utc':start.isoformat(),'end_exclusive_utc':end.isoformat(),'events':events,
        'method':{'scan_hours':1,'root_bracket_seconds':.25,'coordinates':'Apparent geocentric true ecliptic/equinox of date'},
        'limitations':['Finite horizon; absence of a slow-planet contact is not absence of eventual perfection.',
            'Sampled reversals refined; no proof against multiple unseen reversals within an hour.',
            'Exact contact is geometry; historical prohibition/frustration needs stated significators and ordered contacts.']}

def ordered_candidates(events,first,second):
    """Explicit geometric candidates, never silently promoted to perfection."""
    events=sorted(events,key=lambda x:x['utc'])
    contacts=[x for x in events if x['type']=='exact_aspect']
    target=next((x for x in contacts if set(x['bodies'])=={first,second}),None)
    if target is None:return {'target_contact':None,'candidates':[],'status':'indeterminate: target not in finite horizon'}
    before=[x for x in events if x['utc']<target['utc']]
    candidates=[]
    for x in before:
        if x['type'] in ('station','ingress') and set(x['bodies'])&{first,second}:
            candidates.append({'kind':'motion_or_sign_change','event':x})
        elif x['type']=='exact_aspect' and set(x['bodies'])&{first,second}:
            candidates.append({'kind':'intervening_contact','event':x,
                'classification':'prohibition/frustration candidate, not automatically adverse'})
    return {'target_contact':target,'candidates':candidates,
        'status':'Geometric sequence only; categorical perfection not certified'}
