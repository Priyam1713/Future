"""Green-based collective chart components, separated from astronomical geometry."""
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo,reset_tzpath
from pathlib import Path
from itertools import combinations
import hashlib,json,math
from .natal import chart,Settings,signed,SIGNS
from .doctrines import TABLES
from .transits import roots,branches,phase

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'knowledge/mundane_green_v1.json'
DATA=json.loads(PATH.read_text(encoding='utf-8'))
PROFILE=DATA['profile'];RULES={r['id']:r for r in DATA['rules']}
CARDINAL=('Aries','Cancer','Libra','Capricorn')
UTC=timezone.utc

def _site(zone,latitude,longitude,profile):
    if profile!=PROFILE:raise ValueError('Select the named Green profile; no tradition fallback')
    if not all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in (latitude,longitude)) or abs(latitude)>=60 or not -180<=longitude<=180:
        raise ValueError('Explicit location requires abs(latitude)<60 and longitude within±180; no polar fallback')
    reset_tzpath(());ZoneInfo.clear_cache()
    return ZoneInfo(zone)

def _aware(t):
    if not isinstance(t,datetime) or t.tzinfo is None or t.utcoffset() is None:
        raise ValueError('Offset-aware UTC range endpoints required')
    return t.astimezone(UTC)

def _component(identifier):
    r=RULES[identifier]
    return {'rule_id':identifier,'version':r['version'],'source_id':r['source_id'],
        'locator':r['locator'],'coverage':'direct','text':r['method'],'exceptions':r['exceptions']}

def register_knowledge(registry):
    from .knowledge import Rule
    registry.add_source(DATA['source'])
    for r in DATA['rules']:
        registry.add_rule(Rule(r['id'],r['version'],6,'ingresses and selected conjunctions',PROFILE,
            r['source_id'],r['locator'],r['method'],'mundane_component',{'exceptions':r['exceptions']},'proposed','traditional',[]))

def ingress_instants(e,year):
    if type(year) is not int or not 1851<=year<=2148:raise ValueError('UTC ingress years1851–2148 required')
    start=datetime(year,1,1,tzinfo=UTC);end=datetime(year+1,1,1,tzinfo=UTC)
    times=[start+timedelta(days=i) for i in range((end-start).days+1)]
    samples=e.longitudes('Sun',times)
    def longitude(t):return float(e.longitudes('Sun',[t])[0])
    result=[]
    for sign,target in zip(CARDINAL,(0,90,180,270)):
        found=roots(times,samples,target,longitude)
        if len(found)!=1:raise ValueError('Expected exactly one cardinal crossing per UTC year')
        # A shared root estimate may lie just before the boundary. Refine its
        # bracket and select the post-crossing endpoint: Sun.sign must actually
        # be the entered sign, including Aries across360/0. No longitude snapped.
        a,b=found[0]-timedelta(seconds=1),found[0]+timedelta(seconds=1)
        if not signed(longitude(a)-target)<0<=signed(longitude(b)-target):raise ValueError('Solar crossing bracket failed')
        while (b-a).total_seconds()>.001:
            m=a+(b-a)/2
            if signed(longitude(m)-target)<0:a=m
            else:b=m
        if not start<=b<end:raise ValueError('Ingress outside half-open UTC year')
        result.append({'sign':sign,'target_longitude':target,'utc':b.isoformat(),
            'solar_longitude':longitude(b),'residual_degrees':abs(signed(longitude(b)-target)),
            'bracket_utc':[a.isoformat(),b.isoformat()],'bracket_seconds':(b-a).total_seconds(),
            'rule':_component('green1911.ingresses')})
    return result

def aspect_geometry(planets):
    """Nearest major angle per pair, never an invented within-orb judgment."""
    result=[]
    for a,b in combinations(planets,2):
        p,q=planets[a],planets[b]
        angle,branch=min(((angle,branch) for angle in (0,60,90,120,180) for branch in branches(angle)),
                         key=lambda ab:abs(signed(p['longitude']-q['longitude']-ab[1])))
        error=signed(p['longitude']-q['longitude']-branch)
        result.append({'bodies':[a,b],'nearest_major_angle':angle,'branch':branch,'deviation_degrees':abs(error),
            'relative_motion_phase':phase(error,p['speed_degrees_per_day']-q['speed_degrees_per_day']),
            'within_orb':None,'scope':'Nearest geometry only; no verified Green numerical orb threshold'})
    return sorted(result,key=lambda a:(a['deviation_degrees'],a['bodies']))

def _conditions(n):
    result={}
    for b,p in n['planets'].items():
        sign=int(p['longitude']//30)
        own=[];bad=[]
        if b not in ('Uranus','Neptune'):
            if TABLES['domicile'][sign]==b:own.append('domicile')
            if TABLES['domicile'][(sign+6)%12]==b:bad.append('detriment')
            if b in TABLES['exaltation']:
                ex=TABLES['exaltation'][b][0]
                if sign==ex:own.append('exaltation')
                if sign==(ex+6)%12:bad.append('fall')
        distances={a:abs(signed(p['longitude']-lon)) for a,lon in n['angles'].items()}
        result[b]={'retrograde':p['retrograde'],'speed_degrees_per_day':p['speed_degrees_per_day'],
            'own_dignities':own,'debilities':bad,'dignity_coverage':'unsupported' if b in ('Uranus','Neptune') else 'shared classical-seven factual table',
            'dignity_table_source':{'source_id':'horary-lilly-1647-images-v1','locator':'Lilly1647 p104 factual domicile/exaltation table; Green pp108–109 interpretation'},
            'angular_house':p['house'] in (1,4,7,10),'angular_cusp_distances_degrees':distances,
            'nearest_angular_cusp':min(distances,key=distances.get),'prominence_certification':None,
            'source_rule_ids':['green1911.dignity','green1911.angular'],
            'limitations':['House membership is not proximity to a cusp. No unsourced proximity orb/strength score.',
                           'No full affliction,visibility,sect,bounds,combustion or reception doctrine imported into Green profile.']}
    return result

def historical_duration(ascendant,enabled,aries=True):
    if type(enabled) is not bool:raise ValueError('Historical duration option must be Boolean')
    result={'enabled':enabled,'applicable':enabled and aries,'rule':_component('green1911.duration'),
        'scope':'Historical symbolic suggestion only; no forecast-expiry date or guaranteed duration'}
    if enabled and aries:
        mode=int((ascendant%360)//30)%3
        result.update({'ascendant_modality':('cardinal','fixed','mutable')[mode],'symbolic_months':(3,12,6)[mode]})
    return result

def readings(n):
    placements=[];counts={'direct':0,'compositional':0,'unsupported':0}
    for b,p in n['planets'].items():
        planet='green1911.planet.'+b;house='green1911.house.'+str(p['house']);pair=f'green1911.pair.{b}.{p["house"]}'
        components=[_component(house)]
        if planet in RULES:components.insert(0,_component(planet))
        if pair in RULES:
            coverage='direct';text=RULES[pair]['method'];components.append(_component(pair))
        elif planet in RULES:
            coverage='compositional';text=f"Consider {b}'s documented collective topics in relation to house{p['house']}: {RULES[house]['method']}"
        else:
            coverage='unsupported';text=f'No verified Green planetary interpretation component for {b} in this core; house topic supplied separately.'
        counts[coverage]+=1
        placements.append({'planet':b,'house':p['house'],'coverage':coverage,'text':text,'components':components,
            'affliction_judgment':'unsupported: do not assert conditional favorable/adverse source conclusions as unconditional outcomes'})
    return {'placements':placements,'coverage_counts':counts,'composition_rule':_component('green1911.composition'),
        'angular_context':_component('green1911.angular'),
        'conflicting_indications':{'status':'retained as separate components; no aggregate verdict',
            'reason':'Dignity,prominence and conditional planetary statements are different dimensions. Full affliction/synthesis is unsupported.'}}

def _event_chart(e,instant,tz,latitude,longitude):
    n=chart(e,instant.replace(tzinfo=None).isoformat(),'UTC',latitude,longitude,
            Settings(houses='placidus'),orbs={})
    n['technique_id']=6;n['settings'].update({'tradition':PROFILE,'application':'mundane event','rulership':'classical factual table; no automatic collective lord'})
    n['planets']={b:p for b,p in n['planets'].items() if b in DATA['planet_set']}
    n.pop('birth');local=instant.astimezone(tz)
    n['epoch']={'utc':instant.isoformat(),'local':local.isoformat(),'zone':tz.key,'fold':local.fold,
        'latitude':latitude,'longitude':longitude,'site_role':'Caller-selected; no automatic country/capital inference'}
    asc,mc=n['angles']['ascendant'],n['angles']['midheaven']
    n['angles'].update({'descendant':(asc+180)%360,'imum_coeli':(mc+180)%360})
    n['aspect_geometry']=aspect_geometry(n['planets'])
    n['conventions']['aspects']='No fixed orbs; empty aspects list,nearest-major geometry reported separately'
    n['conventions']['houses']='Explicit Placidus numerical realization; not a claim Green mandates a named system'
    n['conditions']=_conditions(n)
    return n

def _base(application):
    release=ROOT/'knowledge/mundane_core_v1.json'
    status=json.loads(release.read_text(encoding='utf-8'))['status'] if release.exists() else 'Developing'
    return {'technique_id':6,'application':application,'profile':PROFILE,'release_status':status,
        'source':DATA['source'],'conventions':DATA['conventions'],
        'provenance':{'profile_sha256':hashlib.sha256(PATH.read_bytes()).hexdigest(),'skyfield':'1.54','tzdata':'2025.2'},
        'limitations':['Symbolic historical interpretation; no calibrated geopolitical,economic or personal-event probability.',
            'Modern apparent-longitude/Placidus realization is explicit; not every historical printed chart convention is reconstructed.',
            'UT1 uses existing modeled delta T; pre1972 UTC is proleptic and future leap seconds are not forecast.',
            'Unverified authors,national founding moments,eclipses,financial predictions and full affliction synthesis are unsupported.']}

def ingresses(e,year,zone,latitude,longitude,profile=PROFILE,historical_duration_option=False):
    tz=_site(zone,latitude,longitude,profile)
    if type(historical_duration_option) is not bool:raise ValueError('Historical duration option must be Boolean')
    events=[]
    for event in ingress_instants(e,year):
        instant=datetime.fromisoformat(event['utc']);n=_event_chart(e,instant,tz,latitude,longitude)
        events.append(dict(event,chart=n,reading=readings(n),
            optional_duration=historical_duration(n['angles']['ascendant'],historical_duration_option,event['sign']=='Aries'),
            cardinal_prominence={'coverage':'direct','rule':_component('green1911.angular'),
                'context':'Sun at a cardinal beginning has zodiacal prominence; not automatically favorable.'}))
    return dict(_base('four cardinal ingresses'),utc_year=year,events=events,
        location_rule=_component('green1911.location'),kernel_sha256=e.digest,
        boundary_semantics='UTC year half-open; event timestamp is post-crossing endpoint of <=1ms bracket,never a snapped longitude')

def conjunctions(e,start,end,zone,latitude,longitude,profile=PROFILE):
    tz=_site(zone,latitude,longitude,profile);start,end=_aware(start),_aware(end)
    if not datetime(1851,1,1,tzinfo=UTC)<=start<end<=datetime(2149,1,1,tzinfo=UTC) or end-start>timedelta(days=366):
        raise ValueError('Conjunction search requires positive<=366-day window within1851–2148; end exclusive')
    count=math.ceil((end-start).total_seconds()/10800)
    times=[start+timedelta(hours=3*i) for i in range(count)]+[end]
    a,b='Jupiter','Saturn'
    values={body:e.longitudes(body,times) for body in (a,b)}
    def relative(t):return float((e.longitudes(a,[t])[0]-e.longitudes(b,[t])[0])%360)
    contacts=roots(times,(values[a]-values[b])%360,0,relative)
    events=[];changes=[]
    for t in contacts:
        before=t-timedelta(minutes=1);after=t+timedelta(minutes=1)
        speed=signed(relative(after)-relative(before))*720
        n=_event_chart(e,t,tz,latitude,longitude)
        events.append({'utc':t.isoformat(),'bodies':[a,b],'angle':0,'residual_degrees':abs(signed(relative(t))),
            'relative_speed_degrees_per_day':speed,
            'phase_before':phase(signed(relative(before)),speed),'phase_after':phase(signed(relative(after)),speed),
            'chart':n,'reading':readings(n),'rule':_component('green1911.conjunction'),
            'pair_interpretation':{'coverage':'compositional','components':[_component('green1911.planet.Jupiter'),_component('green1911.planet.Saturn')],
                'limitation':'No verified direct Jupiter–Saturn pair delineation,duration or prediction strength in this core'}})
    tt=e.ts.from_datetimes(times).tt
    for body in (a,b):
        speeds=((e.longitudes_at_tt(body,tt+1/1440)-e.longitudes_at_tt(body,tt-1/1440)+180)%360-180)*720
        def velocity(t,body=body):return signed(float(e.longitudes(body,[t+timedelta(minutes=1)])[0])-float(e.longitudes(body,[t-timedelta(minutes=1)])[0]))*720
        for t in roots(times,speeds,0,velocity):changes.append({'utc':t.isoformat(),'type':'station','body':body,'speed_after':velocity(t+timedelta(minutes=5))})
        for boundary in range(0,360,30):
            for t in roots(times,values[body],boundary,lambda t,body=body:float(e.longitudes(body,[t])[0])):
                changes.append({'utc':t.isoformat(),'type':'ingress','body':body,'target_longitude':boundary})
    r=dict(_base('selected major-planet conjunctions'),start_inclusive_utc=start.isoformat(),end_exclusive_utc=end.isoformat(),
        bodies=[a,b],events=events,motion_changes=sorted(changes,key=lambda x:(x['utc'],x['body'],x['type'])),kernel_sha256=e.digest,
        numerical_method={'scan_hours':3,'root_bracket_seconds':.25,'motion':'Moving geocentric longitudes,not fixed natal targets'},
        current_geometry={'signed_longitude_difference':signed(relative(start)),
            'scope':'Geometric separation,not an active-orb or duration claim'})
    r['limitations']+=['Finite scan refines sampled reversals; multiple unseen reversals inside a3-hour cell are not formally excluded.',
        'Slow contacts magnify small coordinate-model differences into timing differences; root convergence is not absolute event-time accuracy.']
    return r

def markdown(r):
    lines=['# Mundane Astrology — Green1911','',f"Profile: {r['profile']}; status: {r['release_status']}.",
        'Symbolic source-grounded components; no geopolitical/economic outcome probability.','']
    for event in r['events']:
        n=event['chart'];ep=n['epoch']
        label=event.get('sign','Jupiter–Saturn conjunction')
        lines += [f'## {label}',f"UTC: **{event['utc']}**; local: {ep['local']} ({ep['zone']}).",
            f"Explicit site: {ep['latitude']}, {ep['longitude']}; Placidus. ASC {n['angles']['ascendant']:.6f}°, MC {n['angles']['midheaven']:.6f}°.",
            '', '| Planet | Sign | Degree | House | Retrograde | Dignity / debility |','|---|---|---|---|---|---|']
        for b,p in n['planets'].items():
            c=n['conditions'][b];flags=', '.join(c['own_dignities']+c['debilities']) or c['dignity_coverage']
            lines.append(f"| {b} | {p['sign']} | {p['degree_in_sign']:.6f} | {p['house']} | {p['retrograde']} | {flags} |")
        lines+=['','### Sourced readings','']
        for reading in event['reading']['placements']:
            loc='; '.join(f"{c['rule_id']} ({c['locator']})" for c in reading['components'])
            lines.append(f"- **{reading['planet']} / house{reading['house']} — {reading['coverage']}**: {reading['text']} [{loc}]")
        lines+=['','Conditional source claims are not unconditional favorable/adverse judgments. Angular distances and all nearest-major geometries are in JSON; no invented orb or strength score.']
        d=event.get('optional_duration',{})
        if d.get('applicable'):lines+=['',f"Optional old Aries-ASC rule: {d['ascendant_modality']}, {d['symbolic_months']} symbolic months. Green p4 questions close application; all four charts retained. No expiry or guaranteed forecast duration."]
        lines.append('')
    if not r['events']:lines+=['No exact selected conjunction in this finite window.','']
    lines += [f"[H. S. Green,1911 original scan]({DATA['source']['document_url']})",'',*('- '+x for x in r['limitations'])]
    return '\n'.join(lines)+'\n'
