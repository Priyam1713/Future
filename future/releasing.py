"""Bounded, source-named Zodiacal Releasing; pure elapsed-time arithmetic."""
from datetime import datetime,timedelta,timezone
from pathlib import Path
import json,math,hashlib
from .natal import SIGNS

KNOWLEDGE=json.loads((Path(__file__).resolve().parents[1]/'knowledge/zodiacal_releasing.json').read_text(encoding='utf-8'))
UNITS=KNOWLEDGE['rules'][0]['parameters']['sign_units']
SECONDS=KNOWLEDGE['rules'][1]['parameters']['unit_seconds']

def aware(t):
    if not isinstance(t,datetime) or t.tzinfo is None or t.utcoffset() is None:
        raise ValueError('Explicit offset-aware datetimes required')
    return t.astimezone(timezone.utc)

def periods(sign,start,end,level):
    """Yield one hierarchy's unfiltered periods, with one jump for child levels."""
    initial=sign;current=start;index=0;jumped=False
    while current<end:
        lb=level>1 and index==12 and not jumped
        if lb:sign=(initial+6)%12;jumped=True
        natural=current+timedelta(seconds=UNITS[sign]*SECONDS[level-1])
        stop=min(end,natural)
        yield sign,current,stop,natural,lb
        current=stop;sign=(sign+1)%12;index+=1

def release(birth,fortune_longitude,spirit_longitude,start,end,lot='Spirit',levels=4,profile='brennan-2019-360'):
    if profile!=KNOWLEDGE['profile']:raise ValueError('Unsupported releasing convention; no fallback')
    if lot not in ('Spirit','Fortune'):raise ValueError('Select Spirit or Fortune separately')
    if type(levels) is not int or not 1<=levels<=4:raise ValueError('Supported levels are integers 1..4')
    if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not 0<=x<360 for x in (fortune_longitude,spirit_longitude)):
        raise ValueError('Lot longitudes must be finite in [0,360)')
    birth,start,end=map(aware,(birth,start,end))
    try:lifetime=birth+timedelta(days=120*360)
    except OverflowError:raise ValueError('Birth outside supported datetime arithmetic range') from None
    if not birth<=start<end<=lifetime:raise ValueError('Range must lie within birth through 120 symbolic years')
    if (end-start)>timedelta(days=366*5):raise ValueError('Output range limited to five civil years; query in batches')
    fortune=int(fortune_longitude//30);spirit=int(spirit_longitude//30)
    adjusted=lot=='Spirit' and fortune==spirit
    initial=(spirit+int(adjusted))%12 if lot=='Spirit' else fortune
    output=[]
    def walk(sign,a,b,level,path):
        for s,left,right,natural,lb in periods(sign,a,b,level):
            if right<=start or left>=end:continue
            ident=f'L{level}:{left.isoformat()}'
            place=(s-fortune)%12+1;angular=place in (1,4,7,10)
            row={'id':ident,'parent_id':path[-1] if path else None,'level':level,'sign_index':s,'sign':SIGNS[s],
                'start_inclusive_utc':left.isoformat(),'end_exclusive_utc':right.isoformat(),
                'natural_end_utc':natural.isoformat(),'truncated_by_parent':right<natural,
                'visible_start_utc':max(left,start).isoformat(),'visible_end_exclusive_utc':min(right,end).isoformat(),
                'loosing_of_bond':lb,'fortune_whole_sign_place':place,'angular_from_fortune':angular,
                'symbolic_peak':angular if lot=='Spirit' else None,
                'interpretation_coverage':'documented procedural label; qualitative delineation unsupported',
                'rule_ids':['sign-periods','level-units','nested-boundaries','fortune-angles']+(['loosing-of-bond'] if lb else [])}
            output.append(row)
            if level<levels:walk(s,left,right,level+1,path+[ident])
    walk(initial,birth,lifetime,1,[])
    output.sort(key=lambda x:(x['start_inclusive_utc'],x['level']))
    return {'technique_id':1,'application':'zodiacal releasing','tradition':KNOWLEDGE['tradition'],'profile':profile,
        'lot':lot,'birth_utc':birth.isoformat(),'window':{'start_utc':start.isoformat(),'end_exclusive_utc':end.isoformat()},
        'lots':{'Fortune':fortune_longitude,'Spirit':spirit_longitude,'fortune_reference_sign':SIGNS[fortune]},
        'starting_sign':SIGNS[initial],'spirit_shifted_one_sign':adjusted,'levels':levels,'periods':output,
        'conventions':{'year_days':360,'level_unit_seconds':SECONDS,'time_scale':'Fixed UTC timedelta days; leap seconds not accumulated',
            'calendar':'Proleptic Gregorian display; no Egyptian/Julian historical calendar conversion','boundary':'start inclusive, end exclusive',
            'bond':'One opposite-parent-sign jump after first child circuit; reset at each parent boundary'},
        'rule_trace':KNOWLEDGE['rules'],'sources':KNOWLEDGE['sources'],
        'reproducibility':{'rule_version':KNOWLEDGE['version'],'rules_sha256':hashlib.sha256(json.dumps(KNOWLEDGE,sort_keys=True).encode()).hexdigest()},
        'unsupported':KNOWLEDGE['disputed_or_unresolved'],
        'precision':{'arithmetic':'Integer-second durations through L4; input birth microseconds retained',
            'historical_fidelity':'Named modern reconstruction; not all Valens variants',
            'predictive_validity':'Not established by numerical agreement or historical authority'}}

def from_natal(e,natal,start,end,lot='Spirit',levels=4,profile='brennan-2019-360'):
    from .doctrines import analyze,DoctrineSettings
    if natal['settings']['tradition']!='Hellenistic':raise ValueError('Releasing requires the explicit Hellenistic natal/Lots profile')
    conditions=analyze(e,natal,DoctrineSettings())
    lots=conditions['lots']
    result=release(datetime.fromisoformat(natal['birth']['utc']),lots['Fortune']['longitude'],lots['Spirit']['longitude'],start,end,lot,levels,profile)
    result.update(natal=natal,lot_calculation={'sect':conditions['sect'],'lots':lots,'settings':conditions['settings'],
        'kernel_sha256':e.digest,'date_scope':'Natal astronomy remains restricted to the existing DE440s supported range; symbolic periods are not ancient-date astronomical validation.'})
    return result

def register_knowledge(registry):
    from .knowledge import Rule
    for s in KNOWLEDGE['sources']:registry.add_source(s)
    for r in KNOWLEDGE['rules']:
        registry.add_rule(Rule('zr.'+r['id'],1,1,'zodiacal releasing',KNOWLEDGE['tradition'],r['source_id'],r['locator'],
            r['method'],'zodiacal_releasing',r,'proposed','traditional',[]))

def markdown(r):
    lines=[f"# Zodiacal Releasing from {r['lot']}",'',f"Profile: {r['profile']}. Start sign: {r['starting_sign']}; Spirit adjustment: {r['spirit_shifted_one_sign']}.",
        'Fixed 360-day symbolic years. Fortune angularity is geometry; a symbolic peak is not a positive-outcome prediction.','',
        '| Level | Sign | Start UTC | End UTC | Bond | Fortune place |','|---|---|---|---|---|---|']
    for p in r['periods']:
        if p['level']<=2 or p['loosing_of_bond']:
            lines.append(f"| L{p['level']} | {p['sign']} | {p['start_inclusive_utc']} | {p['end_exclusive_utc']} | {p['loosing_of_bond']} | {p['fortune_whole_sign_place']} |")
    lines+=['','Full L1–L4 rows, parent IDs, truncation flags and calculation/rule trace are retained in JSON.','',
        'Published validation: Valens IV.4 Gemini circuit and Brennan/Schaim episode 192 Diana bond date (1997-07-22); L3/L4 unit table checks. No published absolute L3/L4 chronology independently verified.','']
    lines += [f"- [{s['author']}]({s['url']}) — {s['edition']}" for s in r['sources']]
    lines+=['','Remaining limitations:']+['- '+s for s in r['unsupported']]
    return '\n'.join(lines)+'\n'
