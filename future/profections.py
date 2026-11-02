"""Annual whole-sign profections with explicit civil anniversary conventions."""
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from copy import deepcopy
from pathlib import Path
import calendar,json
from .natal import birth_utc,SIGNS
from .doctrines import TABLES,analyze,CLASSICAL

def anniversary(natal,year,boundary='birth-time',leap_day='march-1',anniversary_fold=None):
    if boundary not in ('birth-time','midnight'):raise ValueError('Unknown birthday boundary convention')
    if leap_day not in ('march-1','february-28'):raise ValueError('Unknown leap-day anniversary policy')
    born=datetime.fromisoformat(natal['birth']['local'])
    month,day=born.month,born.day
    if month==2 and day==29 and not calendar.isleap(year):month,day=(3,1) if leap_day=='march-1' else (2,28)
    wall=datetime(year,month,day,born.hour if boundary=='birth-time' else 0,
                  born.minute if boundary=='birth-time' else 0,born.second if boundary=='birth-time' else 0,
                  born.microsecond if boundary=='birth-time' else 0)
    return birth_utc(wall.isoformat(),natal['birth']['zone'],anniversary_fold)

def annual(natal,target,boundary='birth-time',leap_day='march-1',anniversary_fold=None,conditions=None):
    if target.tzinfo is None:raise ValueError('Profection target needs an explicit UTC offset')
    target=target.astimezone(timezone.utc)
    if target<datetime.fromisoformat(natal['birth']['utc']):raise ValueError('Target precedes birth')
    born=datetime.fromisoformat(natal['birth']['local'])
    local_target=target.astimezone(ZoneInfo(natal['birth']['zone']))
    year=local_target.year
    this=anniversary(natal,year,boundary,leap_day,anniversary_fold)
    active_year=year if target>=this else year-1
    age=active_year-born.year
    # At birth itself the first year begins; midnight convention can precede the
    # birth instant, but an earlier target is always rejected above.
    if age<0:age=0;active_year=born.year
    sign_index=(int(natal['angles']['ascendant']//30)+age)%12
    ruler=TABLES['domicile'][sign_index]
    start=anniversary(natal,active_year,boundary,leap_day,anniversary_fold)
    end=anniversary(natal,active_year+1,boundary,leap_day,anniversary_fold)
    p=natal['planets'][ruler]
    whole_house=(int(p['longitude']//30)-int(natal['angles']['ascendant']//30))%12+1
    knowledge=json.loads((Path(__file__).resolve().parents[1]/'knowledge/profection_rules.json').read_text(encoding='utf-8'))
    topics=knowledge['house_topics']['topics'][age%12]
    return {'technique_id':1,'application':'annual profections','tradition':'Hellenistic whole-sign profection',
        'target_utc':target.isoformat(),'completed_age':age,'cycle':age//12,
        'activated_house':age%12+1,'activated_sign':SIGNS[sign_index],'lord_of_year':ruler,
        'period':{'start_inclusive_utc':max(start,datetime.fromisoformat(natal['birth']['utc'])).isoformat(),
                  'end_exclusive_utc':end.isoformat()},
        'conventions':{'boundary':boundary,'leap_day':leap_day,'zone':natal['birth']['zone'],
            'anniversary_fold':anniversary_fold,'solar_return':'not used',
            'natal_house_system':natal['settings']['houses'],
            'profection_house_logic':'Whole-sign from natal ascending sign, independent of natal quadrant cusps.'},
        'lord_natal_context':{'longitude':p['longitude'],'sign':p['sign'],'selected_natal_house':p['house'],
            'whole_sign_natal_house':whole_house,'conditions':conditions['planets'].get(ruler) if conditions else None},
        'interpretation':{'coverage':'compositional','theme':topics,
            'statement':f"Whole-sign house {age%12+1} and {ruler} are the selected annual timing context; examine the lord's natal conditions and transits separately.",
            'source':'https://theastrologypodcast.com/transcripts/ep-153-annual-profections-an-ancient-time-lord-technique/',
            'locator':'Method: one sign per completed year, traditional domicile ruler; examples age 12, 24, 36.',
            'topic_source':knowledge['house_topics']['source'],
            'limitations':'Symbolic focus does not assign event likelihood or validate an outcome.'},
        'provenance':knowledge}

def context(ephemeris,natal,target,**kwargs):
    explicit=deepcopy(natal)
    explicit['settings']['tradition']='Hellenistic'
    explicit['planets']={k:v for k,v in natal['planets'].items() if k in CLASSICAL}
    conditions=analyze(ephemeris,explicit)
    return annual(natal,target,conditions=conditions,**kwargs)

def register_knowledge(registry):
    from .knowledge import Rule
    data=json.loads((Path(__file__).resolve().parents[1]/'knowledge/profection_rules.json').read_text(encoding='utf-8'))
    for r in data['rules']:
        sid='profection-source:'+r['id']
        registry.add_source({'id':sid,'author':r['author'],'edition':r['edition'],'url':r['source'],
                             'ingestion':'metadata_only','rights_note':data['rights']})
        registry.add_rule(Rule(r['id'],1,1,'annual profections',r['tradition'],sid,r['locator'],r['method'],
                              'symbolic_timing',r.get('parameters',{}),'proposed','traditional',[]))
