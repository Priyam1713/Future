"""Bounded Vimshottari and Parashari D9; no LLM timing or solar-arc analogy."""
from datetime import datetime,timedelta,timezone
import math
from .vedic import nakshatra,sector,normalized,TABLES,CONVENTIONS,CLASSICAL
from .natal import SIGNS

YEAR_KEYS={'pvr-2000-savana':360.,'solar-365.2425':365.2425}
ORDER=TABLES['nakshatra_lords']
YEARS=TABLES['dasha_years']

def aware(date):
    if not isinstance(date,datetime) or date.tzinfo is None or date.utcoffset() is None:
        raise ValueError('Explicit offset-aware datetime required')
    return date.astimezone(timezone.utc)

def antardashas(lord,start,end):
    start,end=aware(start),aware(end)
    if lord not in ORDER or end<=start:raise ValueError('Valid MD lord and increasing endpoints required')
    duration=end-start;index=ORDER.index(lord);used=0;result=[]
    for i in range(9):
        child=ORDER[(index+i)%9];weight=YEARS[child]
        left=start+duration*(used/120);used+=weight
        right=end if used==120 else start+duration*(used/120)
        result.append({'lord':child,'start_inclusive_utc':left.isoformat(),'end_exclusive_utc':right.isoformat(),
            'fraction_of_full_md':weight/120,'rule_id':'vedic.vimshottari'})
    return result

def vimshottari(birth,moon_longitude,target,year_key='pvr-2000-savana'):
    if year_key not in YEAR_KEYS:raise ValueError('Unknown Vimshottari year convention; no fallback')
    birth,target=aware(birth),aware(target)
    year_days=YEAR_KEYS[year_key]
    if not birth<=target<=birth+timedelta(days=120*year_days):raise ValueError('Target must be within birth through 120 selected years')
    mansion=nakshatra(moon_longitude);lord=mansion['lord'];full_years=YEARS[lord]
    duration=timedelta(days=full_years*year_days)
    initial=birth-duration*mansion['elapsed_fraction']
    cursor=initial;index=ORDER.index(lord);rows=[]
    # Three circuits provide current and upcoming rows even near age 120.
    for i in range(27):
        body=ORDER[(index+i)%9];end=cursor+timedelta(days=YEARS[body]*year_days)
        rows.append({'lord':body,'start_inclusive_utc':cursor.isoformat(),'end_exclusive_utc':end.isoformat(),
            'full_years':YEARS[body]});cursor=end
    def contains(row,when):return datetime.fromisoformat(row['start_inclusive_utc'])<=when<datetime.fromisoformat(row['end_exclusive_utc'])
    current=next(r for r in rows if contains(r,target))
    first=rows[0];first_ad=antardashas(lord,initial,datetime.fromisoformat(first['end_exclusive_utc']))
    current_ad=antardashas(current['lord'],datetime.fromisoformat(current['start_inclusive_utc']),datetime.fromisoformat(current['end_exclusive_utc']))
    upcoming_ad=[]
    for r in rows[rows.index(current):rows.index(current)+2]:
        for ad in antardashas(r['lord'],datetime.fromisoformat(r['start_inclusive_utc']),datetime.fromisoformat(r['end_exclusive_utc'])):
            if datetime.fromisoformat(ad['start_inclusive_utc'])>target:upcoming_ad.append(dict(ad,mahadasa_lord=r['lord']))
    return {'system':'Moon-birthstar Vimshottari','year_key':year_key,'year_days':year_days,
        'time_convention':'Fixed elapsed UTC timedelta days; start inclusive/end exclusive. Full initial MD may precede birth; ADs divide that full parent, not the remaining balance.',
        'target_utc':target.isoformat(),'birth_moon_nakshatra':mansion,
        'birth_balance':{'lord':lord,'fraction_remaining':mansion['remaining_fraction'],
            'years_remaining':full_years*mansion['remaining_fraction'],
            'end_exclusive_utc':first['end_exclusive_utc'],'full_md':first,
            'antardasha_at_birth':next(r for r in first_ad if contains(r,birth)),'full_md_antardashas':first_ad},
        'current':{'mahadasa':current,'antardasha':next(r for r in current_ad if contains(r,target))},
        'current_md_antardashas':current_ad,
        'upcoming':{'mahadasas':[r for r in rows if datetime.fromisoformat(r['start_inclusive_utc'])>target][:9],
            'antardashas':upcoming_ad[:9]},
        'rule_trace':next(r for r in CONVENTIONS['rules'] if r['id']=='vedic.vimshottari'),
        'precision':{'arithmetic':'Datetime microsecond representation; this is not absolute timing accuracy.',
            'sensitivity':'Date shift = Moon longitude error / (40/3 degrees) * first full MD years * selected year duration. Birth-time uncertainty adds to cross-ephemeris differences.',
            'predictive_validity':'No statistical outcome confidence assigned.'},
        'limitations':['Birth-time, ayanamsha and rounded Moon position can shift transition dates substantially.',
            'PVR Example50 stated balance fraction verified; its approximate civil end date is inconsistent with fixed elapsed savana days.',
            'Alternative birth stars, Lagna starts and deeper dashas deferred; no event probabilities.']}

def navamsa_point(longitude):
    sign,part_of_sign=sector(longitude,12)
    part,fraction=sector(part_of_sign*360,9)
    start=(sign+(0,8,4)[sign%3])%12
    mapped=(start+part)%12
    return {'longitude_symbolic':mapped*30+fraction*30,'sign_index':mapped,'sign':SIGNS[mapped],
        'degree_in_symbolic_sign':fraction*30,'d1_navamsa_part':part+1}

def navamsa(natal):
    if natal.get('technique_id')!=2:raise ValueError('D9 requires a Vedic D1 report, not a Western chart')
    asc=navamsa_point(natal['ascendant']['longitude']);positions={}
    for n,p in natal['planets'].items():
        q=navamsa_point(p['longitude']);sign=q['sign_index'];flags=[]
        if n in CLASSICAL:
            if TABLES['rulers'][sign]==n:flags.append('own_sign')
            if TABLES['exaltation_signs'][n]==sign:flags.append('exaltation_sign')
            if (TABLES['exaltation_signs'][n]+6)%12==sign:flags.append('debilitation_sign')
        q.update(house=(sign-asc['sign_index'])%12+1,d1_sign=p['sign'],
            same_rashi_as_d1=sign==p['sign_index'],d1_retrograde=p['retrograde'],sign_ruler=TABLES['rulers'][sign],
            sign_dignities=flags,sign_dignity_coverage='documented sign flags' if n in CLASSICAL else 'unsupported for nodes',
            degree_specific_dignity='unsupported: do not apply D1 degree intervals to harmonic degrees')
        positions[n]=q
    return {'chart':'D9/Navamsa','ascendant':asc,'planets':positions,
        'houses':'Whole-sign from D9 Lagna, distinct from D1 houses',
        'longitude_convention':'Symbolic within-division interpolation, not a physical ephemeris position or new planetary retrograde state.',
        'rule_trace':next(r for r in CONVENTIONS['rules'] if r['id']=='vedic.d9'),
        'interpretation':{'coverage':'documented methodology plus compositional sign/house conditions',
            'source_id':'vedic-pvr-procedures-v1','locator':'6.2.9 p.55; 6.3 Table11 pp.60–61; compare BPHS6.12 construction',
            'topics':'D9 is a separate symbolic frame for dharma/inner life and relationship context; D1 remains the physical birth-chart frame.',
            'limitation':'No compatibility, spouse traits, marriage date or personal outcome inferred from these flags.'}}

def enrich(natal,target=None,year_key='pvr-2000-savana',include_d9=False):
    if include_d9:natal['d9']=navamsa(natal)
    if target is not None:
        d=vimshottari(datetime.fromisoformat(natal['birth']['utc']),natal['planets']['Moon']['longitude'],target,year_key)
        current_lords={d['current']['mahadasa']['lord'],d['current']['antardasha']['lord']}
        d['interpretation']={'coverage':'compositional','source_id':'vedic-pvr-procedures-v1','locator':'16.5.1 p.214, general principles',
            'method':'Examine the active lords in their natal divisional contexts; no transit or Western time-lord rule substituted.',
            'd1_lord_context':{n:{'sign':natal['planets'][n]['sign'],'house':natal['planets'][n]['house'],
                'rules_houses':natal['planets'][n]['rules_houses'],'dignity':natal['planets'][n]['dignity']} for n in sorted(current_lords)},
            'limitations':'Conditions are symbolic inputs, not direct pair readings, success scores or event guarantees.'}
        natal['vimshottari']=d
    return natal
