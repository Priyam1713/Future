"""Bounded BaZi core: independent DE440s term roots and deterministic pillars.

Named modern clock profiles; not a claim of one universal historical school.
"""
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from functools import lru_cache
import json, math, hashlib
import numpy as np
from .natal import birth_utc, signed

ROOT=Path(__file__).resolve().parents[1]
CONVENTIONS=json.loads((ROOT/'knowledge/chinese_conventions.json').read_text(encoding='utf-8'))
STEMS='Jia Yi Bing Ding Wu Ji Geng Xin Ren Gui'.split()
GAN='甲乙丙丁戊己庚辛壬癸'
BRANCHES='Zi Chou Yin Mao Chen Si Wu Wei Shen You Xu Hai'.split()
ZHI='子丑寅卯辰巳午未申酉戌亥'
ANIMALS='Rat Ox Tiger Rabbit Dragon Snake Horse Goat Monkey Rooster Dog Pig'.split()
ELEMENTS='Wood Fire Earth Metal Water'.split()
BRANCH_ELEMENTS=[4,2,0,0,2,1,1,2,3,3,2,4]
TERM_NAMES=['Vernal Equinox','Bright and Clear','Corn Rain','Summer Commences','Corn Forms',
    'Corn on Ear','Summer Solstice','Moderate Heat','Great Heat','Autumn Commences',
    'End of Heat','White Dew','Autumnal Equinox','Cold Dew','Frost','Winter Commences',
    'Light Snow','Heavy Snow','Winter Solstice','Moderate Cold','Severe Cold',
    'Spring Commences','Spring Showers','Insects Waken']
PROFILES=tuple(CONVENTIONS['profiles'])
EPOCH=date.fromisoformat(CONVENTIONS['day_anchor'])

def stem(index):
    i=index%10
    return {'index':i,'name':STEMS[i],'character':GAN[i],'element':ELEMENTS[i//2],
        'polarity':'Yang' if i%2==0 else 'Yin'}

def pillar(si,bi):
    si%=10;bi%=12
    if si%2!=bi%2:raise ValueError('Incompatible stem/branch parity')
    cycle=next(i for i in range(60) if i%10==si and i%12==bi)
    return {'pair':GAN[si]+ZHI[bi],'name':STEMS[si]+' '+BRANCHES[bi],
        'sexagenary_index':cycle,'stem':stem(si),
        'branch':{'index':bi,'name':BRANCHES[bi],'character':ZHI[bi],
            'animal':ANIMALS[bi],'element':ELEMENTS[BRANCH_ELEMENTS[bi]],
            'polarity':'Yang' if bi%2==0 else 'Yin'}}

@lru_cache(maxsize=32)
def solar_terms(e,year):
    """UTC instants of all24 terms in Gregorian year; positive-time endpoint.

    At most5-day brackets cannot contain two15-degree solar crossings.
    Cache keyed by actual ephemeris object; callers must not mutate results.
    """
    if isinstance(year,bool) or not isinstance(year,int) or not 1851<=year<=2148:
        raise ValueError('Term year outside supported computation domain')
    a=datetime(year,1,1,tzinfo=timezone.utc)
    end=a.replace(year=year+1)
    dates=[a]
    while dates[-1]<end:dates.append(min(end,dates[-1]+timedelta(days=5)))
    unwrapped=np.degrees(np.unwrap(np.radians(e.longitudes('Sun',dates))))
    result=[]
    for n in range(math.floor(unwrapped[0]/15)+1,math.floor(unwrapped[-1]/15)+1):
        target=n*15;i=int(np.searchsorted(unwrapped,target))-1
        lo,hi=dates[i],dates[i+1]
        longitude=target%360
        while (hi-lo).total_seconds()>.005:
            mid=lo+(hi-lo)/2
            if signed(float(e.longitudes('Sun',[mid])[0])-longitude)>=0:hi=mid
            else:lo=mid
        result.append({'longitude':longitude,'name':TERM_NAMES[longitude//15],
            'utc':hi.isoformat(),'bracket_seconds':(hi-lo).total_seconds(),
            'kind':'jie' if longitude%30==15 else 'zhongqi'})
    if len(result)!=24:raise ValueError('Expected24 solar terms')
    return tuple(result)

def day_index(d):return (d-EPOCH).days%60

def day_hour(clock,profile):
    """Effective naive clock; hour uses next day's stem throughout late Zi."""
    if profile not in PROFILES:raise ValueError('Unsupported clock profile')
    if clock.tzinfo is not None:raise ValueError('Effective wall clock must be naive')
    late=clock.hour==23
    day=clock.date()+timedelta(days=int(late and profile!='civil-split-zi'))
    hour_day=clock.date()+timedelta(days=int(late))
    di=day_index(day);hb=((clock.hour+1)//2)%12
    hs=(2*(day_index(hour_day)%10%5)+hb)%10
    return pillar(di%10,di%12),pillar(hs,hb),day,hour_day

@lru_cache(maxsize=1)
def cny_data():
    records=json.loads((ROOT/'knowledge/chinese_new_years.json').read_text(encoding='utf-8'))['records']
    return {r['year']:r for r in records}

def animal_year(local_date):
    if not 1901<=local_date.year<=2100:raise ValueError('Animal-year table supports1901–2100')
    record=cny_data()[local_date.year];boundary=date.fromisoformat(record['cny'])
    y=local_date.year-int(local_date<boundary);i=(y-1984)%60
    return {'lunar_year':y,'animal':ANIMALS[i%12],'year_pair':pillar(i%10,i%12)['pair'],
        'civil_cny_date':record['cny'],'profile':'hko-cny-date-local-midnight',
        'source_id':'chinese-hko-cny-v1','table_url':record['url'],'table_sha256':record['sha256'],
        'limitation':'Festival date applied at local civil midnight; not the new-moon instant or a worldwide lunar-date converter.'}

def register_knowledge(registry):
    from .knowledge import Rule
    for r in CONVENTIONS['rules']:
        registry.add_rule(Rule(r['id'],r['version'],3,'BaZi core','named-modern-calendar-profiles',
            r['source_id'],r['locator'],r['method'],'chinese_procedure',
            {'exceptions':r['exceptions'],'profiles':list(PROFILES)},'proposed','traditional',[]))

def chart(e,local,zone,latitude,longitude,fold=None,profile='civil-zi23'):
    if profile not in PROFILES:raise ValueError('Unsupported Chinese profile; no fallback')
    if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in (latitude,longitude)) or not -90<=latitude<=90 or not -180<=longitude<=180:
        raise ValueError('Invalid latitude/longitude')
    utc=birth_utc(local,zone,fold)
    from zoneinfo import ZoneInfo
    civil=utc.astimezone(ZoneInfo(zone))
    if not 1901<=civil.year<=2100:raise ValueError('BaZi core supports Gregorian local years1901–2100')
    clock=civil.replace(tzinfo=None)
    if profile=='standard-zi23':clock-=civil.dst()
    terms=[dict(t) for y in (utc.year-1,utc.year,utc.year+1) for t in solar_terms(e,y)]
    jie=[t for t in terms if t['kind']=='jie']
    previous=max((t for t in jie if datetime.fromisoformat(t['utc'])<=utc),key=lambda t:t['utc'])
    following=min((t for t in jie if datetime.fromisoformat(t['utc'])>utc),key=lambda t:t['utc'])
    li=next(t for t in solar_terms(e,utc.year) if t['longitude']==315)
    sy=utc.year-int(utc<datetime.fromisoformat(li['utc']))
    yi=(sy-1984)%60;k=((previous['longitude']-315)%360)//30
    dp,hp,effective_day,hour_day=day_hour(clock,profile)
    ps={'year':pillar(yi%10,yi%12),'month':pillar((2*(yi%10%5)+2+k)%10,(2+k)%12),'day':dp,'hour':hp}
    def counts(items):
        items=list(items)
        return {el:sum(x==el for x in items) for el in ELEMENTS}
    nearest=min(abs((datetime.fromisoformat(t['utc'])-utc).total_seconds()) for t in jie)
    boundary_distance=min((clock.hour*3600+clock.minute*60+clock.second+clock.microsecond/1e6-x)%86400 for x in (0,3600,10800,18000,25200,32400,39600,46800,54000,61200,68400,75600,82800))
    return {'technique_id':3,'status':'Developing','profile':profile,'birth':{'local':local,'zone':zone,
        'fold':fold,'utc':utc.isoformat(),'latitude':latitude,'longitude':longitude},
        'clock':{'effective':clock.isoformat(),'basis':CONVENTIONS['profiles'][profile]['clock'],
            'civil_utc_offset_seconds':civil.utcoffset().total_seconds(),'dst_seconds':civil.dst().total_seconds(),
            'day_date':effective_day.isoformat(),'hour_stem_day_date':hour_day.isoformat(),
            'longitude_correction_applied':False},'solar_year':sy,'pillars':ps,'day_master':dp['stem'],
        'solar_month':{'index_from_tiger':k,'start_inclusive':previous,'end_exclusive':following},
        'lunar_year_animal':animal_year(civil.date()),
        'elements':{'visible_stem_counts':counts(p['stem']['element'] for p in ps.values()),
            'branch_phase_counts':counts(p['branch']['element'] for p in ps.values()),
            'meaning':'Raw symbolic counts, not qi weights, Day Master strength, favorable elements or probability.'},
        'boundary_sensitivity':{'nearest_jie_seconds':nearest,'within_120_seconds_of_jie':nearest<=120,
            'clock_seconds_since_last_boundary':boundary_distance,
            'warning':'Check birth-time uncertainty around term, day and two-hour edges; arithmetic precision is not physical time accuracy.'},
        'rule_trace':[dict(r) for r in CONVENTIONS['rules'] if r['id'] not in ('chinese.ten-gods','chinese.hidden-stems','chinese.pillar-context')],
        'conventions':{k:v for k,v in CONVENTIONS.items() if k not in ('sources','rules')},
        'sources':CONVENTIONS['sources'],
        'reproducibility':{'kernel_sha256':e.digest,'skyfield':'1.54','tzdata':'2025.2',
            'rules_sha256':hashlib.sha256((ROOT/'knowledge/chinese_conventions.json').read_bytes()).hexdigest()},
        'unsupported':['Local mean/apparent solar-time profiles','Luck-pillar onset and forecasts','Zi Wei Dou Shu','Nine Star Ki',
            'Historical Julian/lunar birth input','Universal strength scores or direct event probabilities'],
        'limitations':['Symbolic tradition; numerical correctness does not establish real-world predictive validity.',
            'Existing pinned UTC/leap-second/deltaT assumptions retained; no ancient calendar reconstruction.',
            'Season names refer to original northern Chinese calendar; no southern hemisphere reversal.']}

def markdown(result):
    lines=['# BaZi / Four Pillars','',f"Birth: {result['birth']['local']} {result['birth']['zone']}; profile {result['profile']}.",
        f"Day Master: {result['day_master']['name']} ({result['day_master']['polarity']} {result['day_master']['element']}).",'',
        '| Pillar | Pair | Stem | Branch / animal |','|---|---|---|---|']
    for name,p in result['pillars'].items():
        lines.append(f"| {name} | {p['pair']} / {p['name']} | {p['stem']['polarity']} {p['stem']['element']} | {p['branch']['name']} / {p['branch']['animal']} |")
    lines+=['',f"Lunar-year animal: {result['lunar_year_animal']['animal']} ({result['lunar_year_animal']['lunar_year']}); CNY date {result['lunar_year_animal']['civil_cny_date']}. Separately calculated from the BaZi year.",
        f"Solar month: [{result['solar_month']['start_inclusive']['utc']}, {result['solar_month']['end_exclusive']['utc']}).",'',
        'Full source/clock/root traces and unsupported configurations are in JSON. Symbolic counts do not measure strength or predictive accuracy.']
    return '\n'.join(lines)+'\n'
