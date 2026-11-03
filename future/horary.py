"""Source-bounded Lilly advice-intent diagnostics with honest completeness gates."""
from datetime import datetime,timedelta,timezone
from pathlib import Path
import json,math,hashlib
from skyfield import almanac
from skyfield.api import wgs84
from .natal import chart,Settings,signed
from .houses import house_for
from .doctrines import analyze,TABLES
from .horary_motion import motion,aspect_state,ordered_candidates,CLASSICAL

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'knowledge/horary_lilly_v1.json').read_text(encoding='utf-8'))
SCOPE=json.loads((ROOT/'knowledge/horary_engine_v1.json').read_text(encoding='utf-8'))
ORDER=('Saturn','Jupiter','Mars','Sun','Venus','Mercury','Moon')
WEEK=('Moon','Mars','Mercury','Jupiter','Venus','Saturn','Sun')

def hour_from_events(rise,set_,next_rise,instant,weekday):
    if isinstance(weekday,bool) or not isinstance(weekday,int) or not rise<set_<next_rise or not rise<=instant<next_rise or weekday not in range(7):
        raise ValueError('Ordered sunrise/sunset bounds and weekday0–6 required')
    night=instant>=set_;a,b=(set_,next_rise) if night else (rise,set_)
    duration=(b-a)/12;index=min(11,int((instant-a)/duration))
    hour=index+1+12*night
    return {'lord':ORDER[(ORDER.index(WEEK[weekday])+hour-1)%7],'hour':hour,
        'start_inclusive_utc':(a+index*duration).isoformat(),'end_exclusive_utc':(a+(index+1)*duration).isoformat(),
        'sunrise_utc':rise.isoformat(),'sunset_utc':set_.isoformat(),'next_sunrise_utc':next_rise.isoformat(),
        'rule_id':'horary.hours','locator':'Lilly1647 pp482–485'}

def planetary_hour(e,utc,lat,lon):
    site=wgs84.latlon(lat,lon)
    f=almanac.sunrise_sunset(e.kernel,site)
    ts,states=almanac.find_discrete(e.ts.from_datetime(utc-timedelta(days=2)),e.ts.from_datetime(utc+timedelta(days=2)),f)
    events=[(t.utc_datetime(),bool(s)) for t,s in zip(ts,states)]
    previous=[t for t,state in events if state and t<=utc]
    if not previous:return {'lord':None,'reason':'No preceding sunrise in bounded polar search'}
    rise=previous[-1]
    set_=next((t for t,state in events if not state and t>rise),None)
    next_rise=next((t for t,state in events if state and t>rise),None)
    if set_ is None or next_rise is None:return {'lord':None,'reason':'Sunrise/sunset sequence incomplete'}
    # Local mean solar date fixes the weekday, independent of an arbitrary
    # display timezone. Sunrise occurs far from local midnight in this domain.
    weekday=(rise+timedelta(hours=lon/15)).weekday()
    result=hour_from_events(rise,set_,next_rise,utc,weekday)
    result['sunrise_model']='Skyfield standard solar upper-limb/refraction convention, geometric center about−0.8333 degrees; no terrain/weather'
    result['weekday_basis']='Local mean solar date at sunrise; unequal daylight/night twelfths'
    return result

def classify(predicates,cautions):
    """No heuristic scoring or invented precedence between conflicting rules."""
    unknown=[r['id'] for r in predicates+cautions if r['value'] is None]
    blocked=[r['id'] for r in cautions if r['value'] is not True]
    pos=[r['id'] for r in predicates if r['direction']=='positive' and r['value'] is True]
    neg=[r['id'] for r in predicates if r['direction']=='negative' and r['value'] is True]
    verdict='indeterminate'
    if not unknown and not blocked and bool(pos)!=bool(neg):
        verdict='supported_positive' if pos else 'supported_negative'
    return {'classification':verdict,'positive_testimonies':pos,'negative_testimonies':neg,
        'conflict':bool(pos and neg),'unknown_rules':unknown,'withholding_cautions':blocked,
        'meaning':'Traditional symbolic assessment of adviser intent only; not factual verification or real-world outcome probability.'}

def register_knowledge(registry):
    from .knowledge import Rule
    registry.add_source(DATA['source'])
    for r in DATA['rules']+SCOPE['rules']:
        registry.add_rule(Rule(r['id'],r['version'],5,'Lilly advice intent',DATA['profile'],
            r['source_id'],r['locator'],r['method'],'horary_procedure',{'exceptions':r['exceptions']},'proposed','traditional',[]))

def assess(e,question,category,local,zone,latitude,longitude,protocol='advice-begins',fold=None,profile=DATA['profile']):
    if not isinstance(question,str) or not question.strip():raise ValueError('Nonempty explicit question required')
    if category!='advice-intent':
        return {'technique_id':5,'question':question,'category':category,'classification':'unsupported_question',
            'reason':'Only specific advice-intent assessment is implemented; no category inferred from text.'}
    if profile!=DATA['profile'] or protocol!='advice-begins':raise ValueError('Use named Lilly advice-begins profile; no silent protocol substitution')
    if not all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in (latitude,longitude)) or abs(latitude)>=60 or not -180<=longitude<=180:
        raise ValueError('Horary core location requires abs(latitude)<60 and longitude±180')
    n=chart(e,local,zone,latitude,longitude,Settings(tradition='medieval/traditional',houses='regiomontanus'),fold)
    utc=datetime.fromisoformat(n['birth']['utc'])
    if not 1851<=utc.year<=2148:raise ValueError('Padded Horary motion domain1851–2148')
    condition=analyze(e,n)
    n['technique_id']=5;n['settings']['application']='question'
    ps={b:dict(n['planets'][b],name=b) for b in CLASSICAL}
    lords=[TABLES['domicile'][int(lon//30)] for lon in n['house_cusps']]
    ruler=lords[0]
    future=motion(e,utc,4)
    ingress=next((x for x in future['events'] if x['type']=='ingress' and x['bodies']==['Moon']),None)
    aspects=[]
    for a in CLASSICAL:
        for b in CLASSICAL:
            if CLASSICAL.index(a)>=CLASSICAL.index(b):continue
            for angle in (0,60,90,120,180):
                state=aspect_state(ps[a],ps[b],angle)
                if state['within_orb']:aspects.append(dict(bodies=[a,b],**state))
    # Explicit mean node formula already independently checked as an astronomy
    # component; no Jyotish interpretation/table imported.
    t=e.ts.from_datetime(utc);centuries=(float(t.tt)-2451545)/36525
    node=((450160.398036+centuries*(-6962890.5431+centuries*(7.4722+centuries*(.007702-centuries*.00005939))))/3600)%360
    nodes={key:{'longitude':lon,'house':house_for(lon,n['house_cusps'])} for key,lon in [('North Node',node),('South Node',(node+180)%360)]}
    occupants=[b for b,p in ps.items() if p['house']==10]+[b for b,p in nodes.items() if p['house']==10]
    predicates=[];cautions=[]
    def item(target,id,value,reason,page,direction=None,**evidence):
        engineering=id in ('gate.cusps','gate.moon_degree')
        record={'id':id,'value':value,'reason':reason,'source_id':DATA['source']['id'],'locator':f'Printed p{page}',
            'at_utc':utc.isoformat(),'evidence':evidence,
            'implementation_scope':'conservative engineering restriction, source page is contextual rather than the numerical threshold' if engineering else 'source-specific predicate or explicitly partial caution'}
        if direction:record['direction']=direction
        target.append(record)
    item(predicates,'advice.tenth.favorable',any(x in occupants for x in ('Sun','Jupiter','Venus','North Node')),
        'Sun/Jupiter/Venus/North Node occupying tenth give favorable-intent testimony.',194,'positive',occupants=occupants)
    item(predicates,'advice.tenth.adverse',any(x in occupants for x in ('Saturn','Mars','South Node')),
        'Saturn/Mars/South Node occupying tenth give deceptive-intent testimony.',194,'negative',occupants=occupants)
    app_states=[];app=None;exact=None
    if ruler!='Moon':
        app_states=[aspect_state(ps['Moon'],ps[ruler],a) for a in (0,60,90,120,180)]
        active=[s for s in app_states if s['within_orb'] and s['phase']=='applying']
        if any(not s['sign_agreement'] for s in active):app=None
        else:
            app=bool(active)
            if app:
                exact=next((x for x in future['events'] if x['type']=='exact_aspect' and set(x['bodies'])=={'Moon',ruler} and x['angle'] in [s['angle'] for s in active]),None)
                if exact is None or ingress is None or exact['utc']>=ingress['utc']:app=None
    item(predicates,'advice.moon.application',app,'Moon application to ASC lord; shared significator/out-of-sign or unconfirmed same-sign contact withheld.',194,'positive',states=app_states,exact_contact=exact)
    movable=all(int(x//30)%3==0 for x in (n['angles']['ascendant'],ps[ruler]['longitude'],ps['Moon']['longitude']))
    item(predicates,'advice.haly.movable',movable,'ASC,ASC ruler and Moon all in movable signs: distinct Haly testimony.',194,'negative')
    # Conservative geometrical gates prevent cusp/orb conventions from silently
    # changing a verdict. These margins are engineering restrictions, not Lilly
    # numerical definitions of truth or likelihood.
    relevant={b:p['longitude'] for b,p in ps.items()};relevant.update({b:p['longitude'] for b,p in nodes.items()})
    close={b:min(abs(signed(lon-c)) for c in n['house_cusps']) for b,lon in relevant.items()}
    item(cautions,'gate.cusps',all(d>5 for d in close.values()),'Withhold inside5-degree cusp ambiguity margin; no universal5-degree house substitution.',123,distances_degrees=close)
    asc_degree=n['angles']['ascendant']%30
    item(cautions,'gate.asc_degree',3<=asc_degree<27,'Early/late ASC exceptions not assumed; absent age/appearance/event exception =>withhold.',122,degree=asc_degree)
    moon=ps['Moon']['longitude'];moon_degree=moon%30
    item(cautions,'gate.moon_degree',moon_degree<15 and not 195<=moon<225,
        'Strict earlier-half Moon domain avoids undefined late-degree threshold;15 is a conservative restriction, not Lilly definition. Via combusta withheld.',122,longitude=moon)
    lunar_contacts=[x for x in future['events'] if x['type']=='exact_aspect' and 'Moon' in x['bodies'] and ingress and x['utc']<ingress['utc']]
    item(cautions,'gate.moon_void',bool(lunar_contacts) if ingress else None,
        'Same-sign lunar exact contacts available; void-of-course exceptions not used to force a verdict.',112,next_ingress=ingress,contacts=lunar_contacts)
    item(cautions,'gate.saturn',ps['Saturn']['house'] not in (1,7),'Saturn in first/seventh cautions retained.',122,house=ps['Saturn']['house'])
    item(cautions,'gate.combust',condition['planets'][ruler]['solar'] is None or condition['planets'][ruler]['solar']['state'] not in ('combust','under_beams'),
        'ASC lord combustion caution; beams also conservatively withheld.',123,condition=condition['planets'][ruler]['solar'])
    seventh=condition['planets'][lords[6]]
    seventh_clear=not seventh['retrograde'] and not seventh['debilities'] and seventh['rulers']['bound'] not in ('Mars','Saturn')
    item(cautions,'gate.seventh_basic',seventh_clear,'Explicit retrograde/fall/detriment/malefic-term seventh-lord cautions.',123,lord=lords[6],condition=seventh)
    # The text also says 'unfortunate/impeded' without limiting that term to
    # these checks. Fixed stars/besiegement and full accidentals are not yet
    # independently verified here. No supported verdict may bypass this gap.
    item(cautions,'gate.seventh_full',None,'Full meaning of unfortunate/impeded seventh lord (pp122–123/115), including besiegement/fixed-star exceptions, not yet fully certified.',123)
    hour=planetary_hour(e,utc,latitude,longitude)
    trip=TABLES['triplicities']['lilly'][('fire','earth','air','water')[int(n['angles']['ascendant']//30)%4]][:2]
    affinity=hour['lord']==ruler or hour['lord'] in trip or {hour['lord'],ruler}=={'Sun','Mars'}
    item(cautions,'gate.hour_affinity',True if hour['lord'] and affinity else None,
        'Identity/triplicity or explicit Sun–Mars hot/dry example; other nature matches not invented.',121,hour=hour,asc_ruler=ruler)
    result=classify(predicates,cautions)
    result.update({'technique_id':5,'release_status':'Developing','profile':profile,'category':category,'question':question.strip(),
        'protocol':{'name':protocol,'definition':'Actual instant adviser first discloses advice; caller supplies moment/location. Not software invocation time.','source_page':194},
        'question_chart':n,'significators':{'querent':ruler,'co_significator':'Moon','house_lords':lords,
            'category_house':10,'adviser':'Tenth occupants and lunar application per p194; no invented exclusive adviser-ruler assignment'},
        'conditions':condition,'nodes':{'model':'IERS2010 mean node, true ecliptic comparison convention inherited from verified mean-node component','positions':nodes},
        'current_aspects':aspects,'planetary_hour':hour,'future_motion':future,
        'significator_sequence':ordered_candidates(future['events'],'Moon',ruler) if ruler!='Moon' else {'status':'shared significator'},
        'rule_diagnostics':predicates+cautions,'source':DATA['source'],'procedures':DATA['rules']+SCOPE['rules'],
        'coverage':{'supported':SCOPE['supported'],'experimental':SCOPE['experimental'],'unsupported':SCOPE['unsupported']},
        'interpretations':[{'coverage':'direct','rule_id':r['id'],'text':r['reason'],
            'source_id':r['source_id'],'locator':r['locator'],
            'limitation':'Individual testimony only; overall classification and unresolved cautions govern.'}
            for r in predicates if r['value'] is True],
        'method_limits':['Advice intent only; no event-outcome prediction, factual verification or person diagnosis.',
            'Full historical Lilly judgment clearance remains incomplete; source gaps force indeterminate.',
            'Historical1643 source chart is not recomputed outside supported kernel dates.',
            'No universal probability, strength score or automatic NLP category assignment.'],
        'reproducibility':dict(n['reproducibility'],profile_sha256=hashlib.sha256((ROOT/'knowledge/horary_lilly_v1.json').read_bytes()).hexdigest(),
            scope_sha256=hashlib.sha256((ROOT/'knowledge/horary_engine_v1.json').read_bytes()).hexdigest())})
    return result

def markdown(r):
    lines=['# Lilly Horary assessment','',f"Question: {r['question']}",f"Category: {r['category']}",f"Classification: **{r['classification']}**",'']
    if r['classification']=='unsupported_question':return '\n'.join(lines+[r['reason']])+'\n'
    lines+=[f"Moment: {r['question_chart']['birth']['utc']}; protocol {r['protocol']['name']}.",
        f"Querent: {r['significators']['querent']}; Moon co-significator. Tenth-house occupants: source-specific adviser-intent testimony.",'',
        '| Rule | Evaluated value | Reason | Source page |','|---|---|---|---|']
    for d in r['rule_diagnostics']:lines.append(f"| {d['id']} | {d['value']} | {d['reason']} | {d['locator']} |")
    lines+=['','## Upcoming contacts and motion changes','']
    for x in r['future_motion']['events']:
        detail=f", {x['angle']} degrees" if x['type']=='exact_aspect' else ''
        lines.append(f"- {x['utc']}: {x['type']}, {' / '.join(x['bodies'])}{detail}.")
    lines+=['',f"Source: [Lilly1647 original page images]({r['source']['url']}).",'',*r['method_limits']]
    return '\n'.join(lines)+'\n'
