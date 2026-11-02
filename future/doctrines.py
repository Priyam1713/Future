"""Traditional condition rules with named, unmerged source conventions."""
from dataclasses import dataclass,asdict
from datetime import datetime
from pathlib import Path
import json,math
from skyfield.api import wgs84
from .natal import signed,SIGNS,placement
from .houses import house_for

TABLES=json.loads((Path(__file__).resolve().parents[1]/'knowledge/doctrine_tables.json').read_text(encoding='utf-8'))
CLASSICAL=('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn')

def register_knowledge(registry):
    from .knowledge import Rule
    data=json.loads((Path(__file__).resolve().parents[1]/'knowledge/doctrine_sources.json').read_text(encoding='utf-8'))
    for r in data['rules']:
        sid='doctrine-source:'+r['id']
        registry.add_source({'id':sid,'author':r['author'],'edition':r['edition'],'url':r['source'],
                             'ingestion':'metadata_only','rights_note':data['rights']})
        registry.add_rule(Rule(r['id'],1,1,'planetary conditions',r['tradition'],sid,r['locator'],r['method'],
                              'documented_doctrine',{'exceptions':r.get('exceptions',[])},'proposed','traditional',[]))
    return data

@dataclass(frozen=True)
class DoctrineSettings:
    bounds: str='egyptian'
    triplicity: str='dorothean'
    solar: str='hellenistic-beams'
    lots: str='sect-reversing'
    reception: str='domicile-dispositorship'

def dignity(longitude,day,settings):
    if settings.bounds not in TABLES['bounds'] or settings.triplicity not in TABLES['triplicities']:
        raise ValueError('Unknown dignity table')
    lon=longitude%360; sign=int(lon//30);degree=lon%30
    bound=next(p for p,end in TABLES['bounds'][settings.bounds]['rows'][sign] if degree<end)
    element=('fire','earth','air','water')[sign%4]
    trip=TABLES['triplicities'][settings.triplicity][element]
    exalt=next((p for p,(s,d) in TABLES['exaltation'].items() if s==sign),None)
    fall=next((p for p,(s,d) in TABLES['exaltation'].items() if (s+6)%12==sign),None)
    return {'domicile':TABLES['domicile'][sign],'exaltation':exalt,'triplicity':trip[0 if day else 1],
            'participating':trip[2],'bound':bound,'face':TABLES['faces']['sequence'][int(lon//10)%7],
            'detriment':TABLES['domicile'][(sign+6)%12],'fall':fall}

def solar_condition(lon,sun,system):
    distance=abs(signed(lon-sun));same=int((lon%360)//30)==int((sun%360)//30)
    if system=='lilly-ca113':
        state='cazimi' if distance<=17/60 else 'combust' if same and distance<8.5 else 'under_beams' if distance<17 else 'outside_beams'
    elif system=='hellenistic-beams':
        state='under_beams' if distance<15 else 'outside_beams'
    else: raise ValueError('Unknown solar proximity convention')
    return {'state':state,'longitude_distance_degrees':distance,'same_sign':same,'system':system,
            'actual_naked_eye_visibility':'not inferred; requires atmosphere, extinction and heliacal-rise model'}

def lots(asc,sun,moon,day,system='sect-reversing'):
    if system not in ('sect-reversing','fixed-day-fortune'):raise ValueError('Unknown Lots convention')
    fortune=(asc+moon-sun)%360 if day or system=='fixed-day-fortune' else (asc+sun-moon)%360
    spirit=(asc+sun-moon)%360 if day else (asc+moon-sun)%360
    return {'Fortune':fortune,'Spirit':spirit,'system':system,
            'exception':'Fixed-day option changes Fortune only; Spirit retains its separately identified sect formula.' if system=='fixed-day-fortune' else None}

def condition_report(positions,asc,day,settings):
    owners={n:dignity(p['longitude'],day,settings) for n,p in positions.items() if n in CLASSICAL}
    result={}
    for name,p in positions.items():
        if name not in CLASSICAL:continue
        d=owners[name]
        own=[k for k in ('domicile','exaltation','triplicity','bound','face') if d[k]==name]
        debilities=[k for k in ('detriment','fall') if d[k]==name]
        affiliation='day' if name in ('Sun','Jupiter','Saturn') else 'night'
        elong=signed(p['longitude']-positions['Sun']['longitude'])
        if name=='Mercury':affiliation='day' if elong<0 else 'night' if elong>0 else 'undetermined'
        result[name]={'longitude':p['longitude'],'sign':placement(p['longitude'])['sign'],
            'rulers':d,'own_dignities':own,'debilities':debilities,
            'peregrine_in_selected_primary_rulers':not own,
            'sect_affiliation':affiliation,'of_chart_sect':affiliation==('day' if day else 'night'),
            'retrograde':p['retrograde'],'longitude_speed_degrees_per_day':p['speed_degrees_per_day'],
            'near_station':abs(p['speed_degrees_per_day'])<.01,
            'solar':solar_condition(p['longitude'],positions['Sun']['longitude'],settings.solar) if name!='Sun' else None,
            'solar_longitude_phase':'west_of_sun' if elong<0 else 'east_of_sun' if elong>0 else 'conjunct',
            'exceptions':['Mercury affiliation uses morning/evening longitude phase, not an observed heliacal rise.',
                          'Participating triplicity lord is reported separately, not counted as primary triplicity dignity.']}
    edges=[]
    for guest,d in owners.items():
        for host in owners:
            if host==guest:continue
            kinds=[k for k in ('domicile','exaltation','triplicity','bound','face') if d[k]==host]
            if settings.reception=='domicile-dispositorship':kinds=[k for k in kinds if k=='domicile']
            elif settings.reception not in ('dignity-occupancy','aspect-required'):raise ValueError('Unknown reception policy')
            if not kinds:continue
            separation=abs(int(positions[guest]['longitude']//30)-int(positions[host]['longitude']//30))%12
            aspect=separation in (0,2,3,4,6,8,9,10)
            if settings.reception=='aspect-required' and (not aspect or not (set(kinds)&{'domicile','exaltation'} or len(kinds)>=2)):continue
            edges.append({'host':host,'guest':guest,'dignities':kinds,'whole_sign_configuration':aspect,
                          'policy':settings.reception})
    for e in edges:e['mutual']=any(x['host']==e['guest'] and x['guest']==e['host'] for x in edges)
    return result,edges

def analyze(ephemeris,natal,settings=None):
    tradition=natal['settings']['tradition']
    if tradition not in ('Hellenistic','medieval/traditional'):
        raise ValueError('Select an explicit Hellenistic or medieval/traditional configuration')
    if settings is None:
        settings=DoctrineSettings() if tradition=='Hellenistic' else DoctrineSettings('lilly-ptolemaic','lilly','lilly-ca113','fixed-day-fortune','dignity-occupancy')
    if tradition=='Hellenistic' and (settings.triplicity!='dorothean' or settings.solar!='hellenistic-beams' or settings.reception!='domicile-dispositorship'):
        raise ValueError('Incompatible doctrine settings for the implemented Hellenistic profile')
    utc=datetime.fromisoformat(natal['birth']['utc']);t=ephemeris.ts.from_datetime(utc)
    observer=ephemeris.kernel['earth']+wgs84.latlon(natal['birth']['latitude'],natal['birth']['longitude'])
    altitude=float(observer.at(t).observe(ephemeris.kernel['sun']).apparent().altaz()[0].degrees)
    day=altitude>=0
    planets,receptions=condition_report(natal['planets'],natal['angles']['ascendant'],day,settings)
    points=lots(natal['angles']['ascendant'],natal['planets']['Sun']['longitude'],natal['planets']['Moon']['longitude'],day,settings.lots)
    lot_outputs={name:{'longitude':points[name],**placement(points[name]),'house':house_for(points[name],natal['house_cusps']),
                       'sign_ruler':TABLES['domicile'][int(points[name]//30)]} for name in ('Fortune','Spirit')}
    return {'technique_id':1,'application':'traditional planetary conditions','tradition':tradition,
        'settings':asdict(settings),'sect':{'type':'day' if day else 'night','sun_center_altitude_degrees':altitude,
            'convention':'Topocentric apparent center, geometric horizon, no refraction or terrain; altitude >= 0 is day.',
            'boundary_sensitive':abs(altitude)<.5},'planets':planets,'receptions':receptions,
        'lots':lot_outputs,'lot_formulas':points,
        'provenance':json.loads((Path(__file__).resolve().parents[1]/'knowledge/doctrine_sources.json').read_text(encoding='utf-8')),
        'limitations':['Traditional symbolic conditions are not validated predictive probabilities.',
            'No strength total, medical interpretation, observed visibility or complete medieval horary perfection is inferred.',
            'Station threshold 0.01 degree/day is an explicit numerical display flag, not a historical strength score.',
            'Published rules are tested on supported 1850–2149 charts; no ancient-date ephemeris validation claimed.']}
