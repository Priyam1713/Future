"""Secondary planetary motion, with explicitly separate angle conventions."""
from datetime import datetime,timedelta,timezone
from itertools import combinations
from functools import lru_cache
from pathlib import Path
import math,json
from .natal import chart,Settings,placement,signed
from .houses import frame,axes,cusps,house_for
from .transits import roots,branches,phase

YEAR_KEYS={'tropical':365.24219,'julian':365.25}
ANGLE_METHODS=('none','naibod-ra','solar-arc-mc','secondary-rotation')

def register_knowledge(registry):
    """Persist source-specific progression records without marking symbolic claims proven."""
    from .knowledge import Rule
    data=json.loads((Path(__file__).resolve().parents[1]/'knowledge/progression_methods.json').read_text())
    for r in data['records']:
        source_id='progression-source:'+r['id']
        registry.add_source({'id':source_id,'author':r.get('author',r['tradition']),
            'edition':'Online source checked 2026-11-02','url':r['source'],
            'ingestion':'metadata_only','rights_note':data['rights']})
        registry.add_rule(Rule(r['id'],1,1,'secondary progressions',r['tradition'],source_id,
            r['locator'],r['statement'],r['type'],{},'proposed','traditional',[]))
    return data

class Clock:
    def __init__(self,ephemeris,birth_utc,year_key):
        if year_key not in YEAR_KEYS:raise ValueError('Unknown symbolic year key')
        self.e=ephemeris;self.birth_tt=float(ephemeris.ts.from_datetime(birth_utc).tt)
        self.year_days=YEAR_KEYS[year_key]
    def epoch(self,target):
        if target.tzinfo is None:raise ValueError('Target requires an explicit UTC offset')
        age=(float(self.e.ts.from_datetime(target).tt)-self.birth_tt)/self.year_days
        if not 0<=age<=150:raise ValueError('Direct progressions support ages 0..150')
        return self.birth_tt+age,age

def pair_aspects(left,right,orbs,mutual=False):
    result=[]
    pairs=combinations(left.items(),2) if mutual else ((a,b) for a in left.items() for b in right.items())
    for (name,p),(target,q) in pairs:
        diff=signed(p['longitude']-q['longitude'])
        for angle,orb in orbs.items():
            if angle not in (0,60,90,120,180) or not math.isfinite(orb) or not 0<=orb<15:
                raise ValueError('Invalid progressed aspect/orb')
            branch=min(branches(angle),key=lambda b:abs(signed(diff-b)))
            error=signed(diff-branch)
            if abs(error)<=orb:
                speed=p['speed_degrees_per_day']-(q.get('speed_degrees_per_day',0) if mutual else 0)
                result.append({'progressed':name,'target':target,'aspect':angle,'orb':abs(error),
                               'phase':phase(error,speed),'coverage':'compositional',
                               'interpretation':'Progressed factors are interpreted symbolically; no direct pair delineation selected.',
                               'source':'https://www.astro.com/astrowiki/en/Secondary_Directions'})
    return result

def progress(ephemeris,local,zone,latitude,longitude,target,settings=Settings(),fold=None,
             year_key='tropical',angle_method='naibod-ra',orbs=None,window_days=365):
    if angle_method not in ANGLE_METHODS:raise ValueError('Unknown progressed-angle convention')
    if type(window_days) is not int or not 1<=window_days<=366:raise ValueError('Progression window must be 1..366 civil days')
    natal=chart(ephemeris,local,zone,latitude,longitude,settings,fold)
    birth=datetime.fromisoformat(natal['birth']['utc'])
    clock=Clock(ephemeris,birth,year_key)
    jd,age=clock.epoch(target)
    t,planets=ephemeris.positions_at_tt(jd)
    planets={k:v for k,v in planets.items() if k in natal['planets']}
    armc_birth,_=frame(ephemeris.ts.from_datetime(birth),longitude)
    armc,eps=frame(t,longitude)
    if angle_method=='naibod-ra':armc=(armc_birth+age*.98564733)%360
    elif angle_method=='solar-arc-mc':
        solar_arc=signed(planets['Sun']['longitude']-natal['planets']['Sun']['longitude'])
        mc=math.radians((natal['angles']['midheaven']+solar_arc)%360)
        armc=math.degrees(math.atan2(math.sin(mc)*math.cos(math.radians(eps)),math.cos(mc)))%360
    house_cusps=None;angles=None
    if angle_method!='none':
        house_cusps=cusps(armc,latitude,eps,settings.houses)
        asc,mc=axes(armc,latitude,eps);angles={'ascendant':asc,'midheaven':mc}
    for p in planets.values():
        p.update(placement(p['longitude']))
        p['speed_degrees_per_symbolic_year']=p['speed_degrees_per_day']
        p['speed_degrees_per_civil_day']=p['speed_degrees_per_day']/clock.year_days
        p['natal_house']=house_for(p['longitude'],natal['house_cusps'])
        p['progressed_house']=house_for(p['longitude'],house_cusps) if house_cusps else None
    orbs={0:1.,60:1.,90:1.,120:1.,180:1.} if orbs is None else orbs
    targets=dict(natal['planets']);targets.update({k:{'longitude':v} for k,v in natal['angles'].items()})
    to_natal=pair_aspects(planets,targets,orbs)
    mutual=pair_aspects(planets,planets,orbs,True)
    elongation=(planets['Moon']['longitude']-planets['Sun']['longitude'])%360
    phases=['new','crescent','first quarter','gibbous','full','disseminating','last quarter','balsamic']
    start=target.astimezone(timezone.utc)
    times=[start+timedelta(days=i) for i in range(window_days+1)]
    # Validate the full real-time search range before starting a calculation.
    epochs=[clock.epoch(d)[0] for d in times]
    samples={name:ephemeris.longitudes_at_tt(name,epochs) for name in planets}
    @lru_cache(maxsize=8192)
    def value(name,date):return float(ephemeris.longitudes_at_tt(name,[clock.epoch(date)[0]])[0])
    changes=[];moon_contacts=[];lunations=[]
    for name in planets:
        for boundary in range(0,360,30):
            fn=lambda d,n=name:value(n,d)
            for date in roots(times,samples[name],boundary,fn):
                # A station touching a boundary is not necessarily a sign change.
                before=placement(value(name,date-timedelta(hours=1)))['sign']
                after=placement(value(name,date+timedelta(hours=1)))['sign']
                if before!=after:changes.append({'planet':name,'real_utc':date.isoformat(),'from':before,'to':after})
    for name,p in targets.items():
        for angle in orbs:
            for branch in branches(angle):
                for date in roots(times,samples['Moon'],(p['longitude']+branch)%360,lambda d:value('Moon',d)):
                    moon_contacts.append({'target':name,'aspect':angle,'real_utc':date.isoformat(),
                        'coverage':'compositional','source':'https://www.astro.com/astrowiki/en/Secondary_Directions'})
    relative=(samples['Moon']-samples['Sun'])%360
    for angle in range(0,360,45):
        for date in roots(times,relative,angle,lambda d:(value('Moon',d)-value('Sun',d))%360):
            lunations.append({'phase':phases[angle//45],'elongation':angle,'real_utc':date.isoformat()})
    knowledge=json.loads((Path(__file__).resolve().parents[1]/'knowledge/progression_methods.json').read_text())
    interpretations=[{'rule_id':'secondary.moon-house','coverage':'compositional',
        'statement':f"The progressed Moon traverses natal house {planets['Moon']['natal_house']}; its topics supply symbolic context.",
        'source':'https://www.astro.com/astrowiki/en/Secondary_Directions','locator':'Interpretation: progressed Moon activates the natal house'},
        {'rule_id':'secondary.sun-sign','coverage':'compositional',
         'statement':f"Progressed Sun in {planets['Sun']['sign']} adds symbolic emphasis while natal Sun in {natal['planets']['Sun']['sign']} remains the birth placement.",
         'source':'https://cafeastrology.com/progressedsunsigns.html','locator':'Opening paragraphs'}]
    return {'technique_id':1,'application':'secondary progressions','target_utc':target.astimezone(timezone.utc).isoformat(),
            'natal_summary':natal,'conventions':{'year_key':year_key,'year_days':clock.year_days,
                'clock':'Continuous TT elapsed age / year_days; one 86400-second TT day per symbolic year.',
                'angle_method':angle_method,'obliquity':'true obliquity at progressed epoch',
                'distinction':'Only planets use secondary motion. Naibod/solar-arc-MC are separately labeled directed-angle options, not solar-arc planetary directions.',
                'houses':settings.houses,'orbs':orbs},
            'symbolic_age_years':age,'progressed_epoch':{'jd_tt':jd,'jd_ut1':float(t.ut1),'utc':t.utc_iso()},
            'planets':planets,'angles':angles,'house_cusps':house_cusps,
            'progressed_to_natal_aspects':to_natal,'progressed_to_progressed_aspects':mutual,
            'moon_cycle':{'elongation':elongation,'phase_sector':phases[int(elongation//45)],
                          'note':'Eight 45-degree sectors, not a physical lunar phase at the target civil date.'},
            'upcoming':{'start_utc':start.isoformat(),'end_exclusive_utc':times[-1].isoformat(),
                        'sign_changes':sorted(changes,key=lambda e:e['real_utc']),
                        'progressed_moon_contacts':sorted(moon_contacts,key=lambda e:e['real_utc']),
                        'progressed_lunation_boundaries':sorted(lunations,key=lambda e:e['real_utc'])},
            'knowledge':knowledge,'interpretations':interpretations,'reproducibility':natal['reproducibility'],
            'limitations':['Progression keys and angle options are symbolic conventions, not empirical validation.',
                'Civil future-event dates inherit the selected year key, birth-time and ephemeris uncertainty.',
                'One-day civil sampling with station refinement; very short unseen reversals may be missed.',
                'Pre-1972 civil timestamps use proleptic UTC with TT-UTC 42.184 seconds; historical UT1 reconstruction is not provided. Future leap seconds are not predicted.',
                'Detailed progression pair interpretations and historical time-scale reconstruction remain incomplete.']}
