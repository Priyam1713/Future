"""Named Parashari D1 profile; Skyfield astronomy, independent symbolic rules."""
from datetime import datetime,timedelta
from pathlib import Path
import json,math,hashlib
import numpy as np
from skyfield.functions import rot_x
from skyfield.api import wgs84
from .natal import birth_utc,angles,SIGNS,signed

ROOT=Path(__file__).resolve().parents[1]
CONVENTIONS=json.loads((ROOT/'knowledge/vedic_conventions.json').read_text(encoding='utf-8'))
TABLES=json.loads((ROOT/'knowledge/vedic_tables.json').read_text(encoding='utf-8'))
PROFILE=CONVENTIONS['profile']
CLASSICAL=('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn')

def normalized(value):
    if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value):
        raise ValueError('Finite numeric longitude required')
    return value%360

def sector(longitude,count):
    x=normalized(longitude)*count/360
    # Canonicalize only machine-level representations of rational sector edges.
    if abs(x-round(x))<1e-12:x=float(round(x))
    index=int(math.floor(x))%count
    fraction=x-math.floor(x)
    return index,fraction

def nakshatra(longitude):
    index,fraction=sector(longitude,27)
    pada,_=sector(longitude,108)
    return {'index':index,'name':TABLES['nakshatras'][index],'pada':pada%4+1,
        'lord':TABLES['nakshatra_lords'][index%9],'elapsed_fraction':fraction,'remaining_fraction':1-fraction,
        'boundary_sensitive':min(fraction,1-fraction)*(360/27)<.01,'rule_id':'vedic.nakshatra'}

def mean_ecliptic_rotation(t):return rot_x(-t._mean_obliquity_radians)@t.P

def ayanamsha(ts,t):
    t0=ts.tt_jd(CONVENTIONS['astronomy']['anchor_jd_tt'])
    a0=CONVENTIONS['astronomy']['anchor_true_degrees']-math.degrees(float(t0._nutation_angles_radians[0]))
    equinox_at_anchor=mean_ecliptic_rotation(t0)@mean_ecliptic_rotation(t).T@np.array([1.,0.,0.])
    mean=a0-math.degrees(math.atan2(equinox_at_anchor[1],equinox_at_anchor[0]))
    nutation=math.degrees(float(t._nutation_angles_radians[0]))
    return {'name':'lahiri-1956-skyfield','mean_degrees':mean,'true_degrees':mean+nutation,
        'nutation_longitude_degrees':nutation,'definition_source_id':'vedic-lahiri-definition-v1'}

def mean_node(jd_tt):
    t=(jd_tt-2451545.)/36525.
    a,b,c,d,e=CONVENTIONS['astronomy']['node_polynomial_arcseconds']
    return ((a+t*(b+t*(c+t*(d+t*e))))/3600)%360

def dignity(body,longitude):
    sign,_=sector(longitude,12);degree=normalized(longitude)-sign*30
    if body not in CLASSICAL:return {'flags':[],'moolatrikona':'unsupported','coverage':'unsupported nodal dignity/co-rulership','rule_id':'vedic.dignity'}
    flags=[]
    if TABLES['rulers'][sign]==body:flags.append('own_sign')
    ex=TABLES['exaltation_signs'][body]
    if sign==ex:flags.append('exaltation_sign')
    if sign==(ex+6)%12:flags.append('debilitation_sign')
    mt=TABLES['moolatrikona_intervals'].get(body)
    moola=bool(mt and sign==mt[0] and mt[1]<=degree<mt[2]) if mt else 'unsupported: source discrepancy'
    return {'flags':flags,'moolatrikona':moola,'rule_id':'vedic.dignity',
        'interpretation':'Documented symbolic dignity; no numerical strength total or outcome probability.'}

def graha_aspects(positions):
    result=[]
    for body in CLASSICAL:
        sign=positions[body]['sign_index']
        for place in TABLES['full_aspect_places'][body]:
            target=(sign+place-1)%12
            result.append({'from':body,'place_from_planet':place,'target_sign':SIGNS[target],
                'targets':[n for n,p in positions.items() if p['sign_index']==target],
                'rule_id':'vedic.drishti','scope':'Full whole-sign graha drishti, not Western angular-orb or Jaimini sign aspects.'})
    return result

def register_knowledge(registry):
    from .knowledge import Rule
    for source in CONVENTIONS['sources']:registry.add_source(source)
    for r in CONVENTIONS['rules']:
        registry.add_rule(Rule(r['id'],1,2,'Parashari core',PROFILE,r['source_id'],r['locator'],r['method'],
            'vedic_procedure',{'exceptions':r['exceptions'],'profile':PROFILE},'proposed','traditional',[]))

def d1(e,local,zone,latitude,longitude,fold=None,profile=PROFILE):
    if profile!=PROFILE:raise ValueError('Unsupported Vedic convention; no fallback')
    if not all(math.isfinite(v) for v in (latitude,longitude)) or not abs(latitude)<66 or not -180<=longitude<=180:
        raise ValueError('Vedic core domain: latitude strictly within +/-66 degrees, longitude +/-180')
    utc=birth_utc(local,zone,fold);t,tropical=e.positions(utc)
    ayan=ayanamsha(e.ts,t);asc,mc=angles(t,latitude,longitude)
    sid_asc=(asc-ayan['true_degrees'])%360;asc_sign,_=sector(sid_asc,12)
    dt=.005
    am=ayanamsha(e.ts,e.ts.tt_jd(t.tt-dt));ap=ayanamsha(e.ts,e.ts.tt_jd(t.tt+dt))
    drift=(ap['true_degrees']-am['true_degrees'])/(2*dt)
    positions={n:{'longitude':(tropical[n]['longitude']-ayan['true_degrees'])%360,
        'speed_degrees_per_day':tropical[n]['speed_degrees_per_day']-drift} for n in CLASSICAL}
    node=(mean_node(float(t.tt))-ayan['mean_degrees'])%360
    node_speed=signed((mean_node(float(t.tt)+dt)-ap['mean_degrees'])-(mean_node(float(t.tt)-dt)-am['mean_degrees']))/(2*dt)
    positions.update(Rahu={'longitude':node,'speed_degrees_per_day':node_speed},Ketu={'longitude':(node+180)%360,'speed_degrees_per_day':node_speed})
    for body,p in positions.items():
        sign,_=sector(p['longitude'],12)
        p.update(sign_index=sign,sign=SIGNS[sign],degree_in_sign=p['longitude']-sign*30,
            house=(sign-asc_sign)%12+1,retrograde=p['speed_degrees_per_day']<0,
            sign_ruler=TABLES['rulers'][sign],dignity=dignity(body,p['longitude']),
            boundary_sensitive=min(p['longitude']%30,30-p['longitude']%30)<.01)
        p['rules_houses']=[(s-asc_sign)%12+1 for s,r in enumerate(TABLES['rulers']) if r==body] if body in CLASSICAL else []
    observer=e.kernel['earth']+wgs84.latlon(latitude,longitude)
    altitude=float(observer.at(t).observe(e.kernel['sun']).apparent().altaz()[0].degrees)
    return {'technique_id':2,'application':'D1/Rashi','profile':profile,'release_status':'Core v1 Ready',
        'birth':{'local':local,'zone':zone,'utc':utc.isoformat(),'latitude':latitude,'longitude':longitude},
        'times':{'jd_tt':float(t.tt),'jd_ut1':float(t.ut1),'delta_t_seconds':float(t.delta_t)},
        'ayanamsha':ayan,'ascendant':{'longitude':sid_asc,'sign_index':asc_sign,'sign':SIGNS[asc_sign],'degree_in_sign':sid_asc-asc_sign*30},
        'midheaven_longitude':(mc-ayan['true_degrees'])%360,'house_cusps':[((asc_sign+i)*30)%360 for i in range(12)],
        'planets':positions,'moon_nakshatra':nakshatra(positions['Moon']['longitude']),'graha_aspects':graha_aspects(positions),
        'solar_horizon':{'sun_center_altitude_degrees':altitude,'above_geometric_horizon':altitude>=0,'refraction':'none','scope':'Astronomical condition, not imported Western sect interpretation.'},
        'rule_trace':[r for r in CONVENTIONS['rules'] if r['id'] not in ('vedic.d9','vedic.vimshottari')],
        'sources':CONVENTIONS['sources'],'conventions':CONVENTIONS['astronomy'],
        'boundary_semantics':'Half-open sectors; machine-level rational-edge snaps within 1e-12 sector units. Values within .01 degree of a boundary flagged, not certified birth-time precision.',
        'reproducibility':{'skyfield':'1.54','kernel_sha256':e.digest,'profile_version':1,
            'rules_sha256':hashlib.sha256(json.dumps([CONVENTIONS,TABLES],sort_keys=True).encode()).hexdigest()},
        'unsupported':['True/osculating nodes','Nodal dignities/co-rulers/aspect schools','Mars degree-specific moolatrikona','Shadbala, advanced yogas, Jaimini/KP/Prashna','Direct personal-event predictions'],
        'predictive_validity':'Symbolic tradition; numerical/reference agreement does not establish real-world predictive accuracy.'}

def markdown(r):
    lines=['# Vedic D1 / Rashi','',f"Birth: {r['birth']['local']} {r['birth']['zone']}; UTC {r['birth']['utc']}.",
        f"Profile: {r['profile']}. Lagna: {r['ascendant']['sign']} {r['ascendant']['degree_in_sign']:.5f} degrees.",
        f"Moon: {r['moon_nakshatra']['name']}, pada {r['moon_nakshatra']['pada']}, lord {r['moon_nakshatra']['lord']}.",'',
        '| Graha | Rashi | Degree | D1 house | Retrograde | Sign dignity |','|---|---|---|---|---|---|']
    for n,p in r['planets'].items():lines.append(f"| {n} | {p['sign']} | {p['degree_in_sign']:.5f} | {p['house']} | {p['retrograde']} | {', '.join(p['dignity']['flags']) or ('unsupported' if n not in CLASSICAL else 'none')} |")
    if 'd9' in r:
        lines+=['','## D9 / Navamsa','',f"D9 Lagna: {r['d9']['ascendant']['sign']}. Symbolic chart, separate from D1.",'',
            '| Graha | D9 rashi | D9 house | Same rashi as D1 |','|---|---|---|---|']
        for n,p in r['d9']['planets'].items():lines.append(f"| {n} | {p['sign']} | {p['house']} | {p['same_rashi_as_d1']} |")
        lines+=['',r['d9']['interpretation']['topics'],r['d9']['interpretation']['limitation']]
    if 'vimshottari' in r:
        d=r['vimshottari'];c=d['current']
        lines+=['','## Vimshottari','',f"Target: {d['target_utc']}; year convention: {d['year_key']} ({d['year_days']} elapsed days).",
            f"Current: **{c['mahadasa']['lord']} / {c['antardasha']['lord']}**. AD ends {c['antardasha']['end_exclusive_utc']}.",
            f"Birth balance: {d['birth_balance']['lord']}, {d['birth_balance']['years_remaining']:.8f} selected years.",'',
            '| Upcoming MD | Start UTC | End UTC |','|---|---|---|']
        for p in d['upcoming']['mahadasas']:lines.append(f"| {p['lord']} | {p['start_inclusive_utc']} | {p['end_exclusive_utc']} |")
        lines+=['','Full-parent AD boundaries and source trace are in JSON. Birth-time uncertainty is not an exact-event confidence score.']
    lines+=['','Whole-sign graha aspects and complete rule traces are in JSON. No strength total or event probability is inferred.','']
    lines += [f"- [{s['author']}]({s['url']}) — {s.get('locator',s['edition'])}" for s in r['sources']]
    lines += ['','Unsupported: '+ '; '.join(r['unsupported']),r['predictive_validity']]
    return '\n'.join(lines)+'\n'
