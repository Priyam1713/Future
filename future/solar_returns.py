"""Non-precessed tropical geocentric Solar Returns, independent of birthdays."""
from datetime import datetime,timedelta,timezone
from pathlib import Path
import json
from itertools import combinations
from .natal import chart,Settings,signed,DEFAULT_ORBS
from .transits import roots
from .progressions import pair_aspects
from .houses import house_for

def aspect_patterns(aspects):
    edges={frozenset(a['bodies']):a['angle'] for a in aspects}
    names=sorted({p for edge in edges for p in edge})
    result=[]
    for triple in combinations(names,3):
        angles=[edges.get(frozenset(pair)) for pair in combinations(triple,2)]
        if angles.count(120)==3:result.append({'type':'grand trine','bodies':list(triple)})
        if angles.count(90)==2 and angles.count(180)==1:result.append({'type':'T-square','bodies':list(triple)})
    return {'geometric_patterns':result,'orb_basis':'Selected major-aspect orbs; no strength score.',
            'source':'https://www.skyscript.co.uk/aspects2.html','locator':'Aspect Patterns: T Square and grand-trine geometry'}

def solar_return(ephemeris,natal,year,latitude,longitude,houses='placidus',orbs=None):
    if type(year) is not int or not 1850<=year<=2148:
        raise ValueError('Solar Return UTC calendar years supported: 1850..2148')
    start=datetime(year,1,1,tzinfo=timezone.utc);end=datetime(year+1,1,1,tzinfo=timezone.utc)
    times=[start+timedelta(days=i) for i in range((end-start).days+1)]
    target=natal['planets']['Sun']['longitude']
    def longitude_at(t):return float(ephemeris.longitudes('Sun',[t])[0])
    contacts=roots(times,ephemeris.longitudes('Sun',times),target,longitude_at)
    if len(contacts)!=1:raise ValueError(f'Expected one return in UTC year, found {len(contacts)}')
    instant=contacts[0]
    returned=chart(ephemeris,instant.replace(tzinfo=None).isoformat(),'UTC',latitude,longitude,
                   Settings(tradition=natal['settings']['tradition'],houses=houses),orbs=orbs)
    targets=dict(natal['planets']);targets.update({k:{'longitude':v} for k,v in natal['angles'].items()})
    cross=pair_aspects(returned['planets'],targets,DEFAULT_ORBS if orbs is None else orbs)
    # Progression and return interpretations are separate even when geometry is shared.
    for a in cross:
        a['return_planet']=a.pop('progressed')
        a['interpretation']='Return-to-natal aspect geometry; specific return-pair delineation not yet sourced.'
        a['coverage']='unsupported'
        a.pop('source',None)
    source='https://www.maryshea.com/frequently-asked-questions'
    compatible=houses=='placidus'
    interpretation={'coverage':'documented methodology with compositional chart context' if compatible else 'unsupported by Shea profile for selected house system',
        'source':source,'author':'Mary Fortier Shea','locator':'FAQ questions 1–3',
        'rules':[{'id':'shea.nonprecessed','statement':'Her published method uses tropical, nonprecessed Placidus returns.'},
                 {'id':'shea.location','statement':'Location changes houses and angles, not geocentric planetary positions or interplanetary aspects.'}],
        'calculated_context':{'return_sun_house':returned['planets']['Sun']['house'],
            'natal_ascendant_in_return_house':house_for(natal['angles']['ascendant'],returned['house_cusps'])},
        'exceptions':['Other house systems are calculated but not represented as Shea methodology.',
                      'No copyrighted Planets in Solar Returns delineations ingested or attributed without access.']}
    return {'technique_id':1,'application':'solar return','return_year_utc':year,
        'exact_utc':instant.isoformat(),'solar_residual_degrees':abs(signed(longitude_at(instant)-target)),
        'natal':natal,'return_chart':returned,'return_to_natal_aspects':cross,
        'return_configurations':aspect_patterns(returned['aspects']),'interpretation':interpretation,
        'conventions':{'longitude':'Apparent geocentric tropical ecliptic/equinox of date; no precession correction.',
            'year':'Unique crossing in [January 1 UTC, January 1 next UTC year).',
            'location':'Explicit caller-selected coordinates; return instant is independent of them.',
            'root_bracket_seconds':.25,'birthday':'Not a civil birthday or a profection boundary.'},
        'reproducibility':returned['reproducibility'],
        'limitations':['Numerical root precision is not absolute ephemeris timing accuracy.',
                       'Natal birth-time and historical timescale uncertainties propagate into the return.',
                       'Return symbolism has no calibrated personal-event probabilities.']}

def register_knowledge(registry):
    from .knowledge import Rule
    sid='shea-solar-return-faq-v1'
    registry.add_source({'id':sid,'author':'Mary Fortier Shea','edition':'Online FAQ checked 2026-11-02',
        'url':'https://www.maryshea.com/frequently-asked-questions','ingestion':'metadata_only',
        'rights_note':'Concise methodological facts only; copyrighted book not ingested.'})
    registry.add_rule(Rule('shea.solar-return.method',1,1,'solar returns','Shea tropical Placidus',sid,
        'FAQ questions 1–3','Use nonprecessed tropical Placidus returns; relocation affects angles/houses.',
        'return_method',{'zodiac':'tropical','precession_correction':False,'houses':'placidus'},'proposed','traditional',[]))

def markdown(r):
    c=r['return_chart'];lines=['# Solar Return — July 1990 example','',
        f"Return in UTC calendar year {r['return_year_utc']}: **{r['exact_utc']}**.",
        f"Selected location: {c['birth']['latitude']}, {c['birth']['longitude']}; house system: {c['settings']['houses']}.",
        f"Solar longitude residual: {r['solar_residual_degrees']:.9f} degrees.",'',
        '| Planet | Sign | Degree | Return house | Retrograde |','|---|---|---|---|---|']
    for name,p in c['planets'].items():lines.append(f"| {name} | {p['sign']} | {p['degree_in_sign']:.6f} | {p['house']} | {p['retrograde']} |")
    lines+=['','## Return-to-natal aspects','', '| Return | Natal target | Aspect | Orb |','|---|---|---|---|']
    for a in r['return_to_natal_aspects']:lines.append(f"| {a['return_planet']} | {a['target']} | {a['aspect']} | {a['orb']:.6f} |")
    lines+=['','## Interpretation scope','',r['interpretation']['coverage'],
        f"[Mary Fortier Shea, FAQ 1–3]({r['interpretation']['source']}): her method is tropical, nonprecessed and Placidus; relocation changes house placements and angles.",
        'Individual planet-pair meanings remain unsupported; the JSON contains complete natal, return and aspect calculations.','']
    lines.extend('- '+l for l in r['limitations'])
    return '\n'.join(lines)+'\n'
