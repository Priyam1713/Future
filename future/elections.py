"""Narrow, source-configurable Ramesey elections. No auspiciousness score."""
from datetime import datetime,timedelta,timezone
from pathlib import Path
from functools import lru_cache
import json,math
from .natal import chart,Settings,SIGNS,signed
from .houses import frame,cusps,axes,house_for
from .doctrines import TABLES,analyze,CLASSICAL
from .transits import roots,phase,branches

CATALOG=json.loads((Path(__file__).resolve().parents[1]/'knowledge/electional_profiles.json').read_text(encoding='utf-8'))
REQUIREMENTS=json.loads((Path(__file__).resolve().parents[1]/'knowledge/electional_requirements_v2.json').read_text(encoding='utf-8'))

def certify(ephemeris,candidate,latitude,longitude,houses,profile_name):
    """Preserve legacy partial matches, but assess smaller, explicitly classified cells."""
    from .lunar_sequence import sequence
    a=datetime.fromisoformat(candidate['start_inclusive_utc']);b=datetime.fromisoformat(candidate['end_exclusive_utc'])
    lunar=sequence(ephemeris,a)
    cuts={a,b}
    cuts.update(datetime.fromisoformat(x['utc']) for x in lunar['events'] if a<datetime.fromisoformat(x['utc'])<b)
    times=[a+timedelta(minutes=5*i) for i in range(math.ceil((b-a).total_seconds()/300))]+[b]
    @lru_cache(maxsize=4096)
    def relative(date,index):
        armc,eps=frame(ephemeris.ts.from_datetime(date),longitude)
        cs=cusps(armc,latitude,eps,houses)
        return (float(ephemeris.longitudes('Moon',[date])[0])-cs[index])%360
    for index in (0,1):
        cuts.update(roots(times,[relative(t,index) for t in times],0,lambda t,i=index:relative(t,i)))
    windows=[]
    for left,right in zip(sorted(cuts),sorted(cuts)[1:]):
        mid=left+(right-left)/2
        c=chart(ephemeris,mid.replace(tzinfo=None).isoformat(),'UTC',latitude,longitude,Settings(tradition='medieval/traditional',houses=houses))
        checked=[left+(right-left)*f for f in (.1,.5,.9)]
        moon_houses=[]
        for t in checked:
            armc,eps=frame(ephemeris.ts.from_datetime(t),longitude)
            moon_houses.append(house_for(float(ephemeris.longitudes('Moon',[t])[0]),cusps(armc,latitude,eps,houses)))
        supported=profile_name=='ramesey-retain-money'
        failure=supported and all(h==1 for h in moon_houses)
        status='rejected' if failure else 'indeterminate'
        unknown=[r['id'] for r in REQUIREMENTS['rules'] if r['status']!='implemented']
        trace=[dict(r,source_reference=REQUIREMENTS['sources'][r['source']],
                    result=('violated' if failure else 'satisfied' if all(h!=1 for h in moon_houses) else 'indeterminate') if r['id']=='moon-not-ascendant' and supported else
                    'satisfied' if r['id'] in ('retention-fixed','asc-lord-direct') and supported and not candidate['rule_trace'].get('disabled_rules') and all(x['required'] for x in candidate['rule_trace']['rules']) else 'indeterminate',
                    evaluated_utc=mid.isoformat()) for r in REQUIREMENTS['rules']]
        lord=candidate['rule_trace']['ascendant_lord'];second=candidate['rule_trace']['second_lord']
        elongations={n:abs(signed(c['planets'][n]['longitude']-c['planets']['Sun']['longitude'])) for n in set(('Moon','Jupiter',lord,second))}
        windows.append({'start_inclusive_utc':left.isoformat(),'end_exclusive_utc':right.isoformat(),'classification':status,
            'reason':'Moon occupies first house: general retention-profile prohibition.' if failure else 'Complete mandatory coverage unavailable; partial matches cannot be promoted.',
            'rule_trace':trace,'missing_requirements':unknown,'chief_significator_elongations_degrees':elongations,
            'moon_house_checks':[{'utc':t.isoformat(),'house':h} for t,h in zip(checked,moon_houses)],
            'window_precision':'Solved Moon-house/contact boundaries; probe agreement is bounded numerical evidence, not a completeness proof.'})
    candidate.update(classification='rejected' if windows and all(w['classification']=='rejected' for w in windows) else 'indeterminate',
        assessment_windows=windows,lunar_sequence=lunar,qualification='Legacy selected-rule match; use assessment_windows classifications. No eligible election established.')
    return windows

def profile_for(name,category,tradition='Ramesey 1653'):
    if name not in CATALOG['profiles']:raise ValueError('Unknown source profile')
    p=CATALOG['profiles'][name]
    if p['category']!=category or p['tradition']!=tradition:raise ValueError('Category/tradition does not match selected source profile')
    return p

def evaluate(signs,speeds,asc,mc,second,profile,required=None):
    """Pure documented predicates. Signs are zero-based tropical sign indices."""
    required=profile['rules'] if required is None else required
    if not set(required)<=set(profile['rules']) or not required:raise ValueError('Select nonempty supported required rules')
    asc_sign=int((asc%360)//30);second_sign=int((second%360)//30)
    asc_lord=TABLES['domicile'][asc_sign];second_lord=TABLES['domicile'][second_sign]
    allowed=profile['signs']
    values={'asc-sign':asc_sign in allowed,'asc-ruler-sign':signs[asc_lord] in allowed,
            'moon-sign':signs['Moon'] in allowed,'second-ruler-sign':signs[second_lord] in allowed,
            'angles-sign':asc_sign in allowed and int((mc%360)//30) in allowed,
            'asc-ruler-direct':speeds[asc_lord]>=0}
    traces=[]
    for rid,ok in values.items():
        source=CATALOG['rule_parameters'][rid]
        traces.append({'id':rid,'status':'satisfied' if ok else 'violated','required':rid in required,
                       'source':source.get('source',profile['source']),'locator':source.get('locator',profile['locator']),
                       'meaning':source['meaning']})
    return {'passes_selected_rules':all(values[k] for k in required),'rules':traces,
            'ascendant_lord':asc_lord,'second_lord':second_lord}

def diagnostics(ephemeris,c):
    # Ramesey's general word "fortify" is not reduced to an invented score.
    positions=c['planets']
    actual=analyze(ephemeris,c)
    conditions,reception=actual['planets'],actual['receptions']
    applications=[];moon=positions['Moon']
    for name in ('Venus','Jupiter','Mars','Saturn'):
        p=positions[name]
        for angle in (0,60,90,120,180):
            diff=signed(moon['longitude']-p['longitude'])
            branch=min(branches(angle),key=lambda b:abs(signed(diff-b)))
            error=signed(diff-branch)
            if abs(error)<=3:
                applications.append({'planet':name,'aspect':angle,'orb':abs(error),
                    'phase':phase(error,moon['speed_degrees_per_day']-p['speed_degrees_per_day']),
                    'orb_convention':'3 degrees, explicit search diagnostic, not attributed to Ramesey',
                    'exception':'Instantaneous application; no guarantee of perfection before a station, sign change or intervening contact.'})
    return {'moon_first_house':moon['house']==1,
            'diagnostic_rule_trace':[
                {'id':'moon-angular-caution','status':'violated' if moon['house']==1 else 'satisfied',
                 'source':CATALOG['diagnostics'][0]['source'],'locator':CATALOG['diagnostics'][0]['locator']},
                {'id':'benefics-malefics','status':'requires-review','reason':'Natural status alone does not resolve event-specific significators and natal exceptions.'},
                {'id':'moon-application','status':'requires-review','reason':'Instantaneous aspect phases do not prove future perfection.'},
                {'id':'significator-condition','status':'unresolved','reason':'Source fortification is broader than a single dignity or an invented total.'}],
            'angular_benefics':[n for n in ('Venus','Jupiter') if positions[n]['house'] in (1,4,7,10)],
            'angular_malefics':[n for n in ('Mars','Saturn') if positions[n]['house'] in (1,4,7,10)],
            'moon_aspects':applications,'planetary_conditions':conditions,'receptions':reception,
            'sect':actual['sect'],'condition_settings':actual['settings'],
            'condition_source':'Comparative Lilly-profile dignity/proximity diagnostics, not a claim to a complete Ramesey dignity prescription.',
            'source_rules':CATALOG['diagnostics'],
            'scope':'Diagnostics are not all selection filters. Unimplemented criteria are unknown, never counted as satisfied.'}

def search(ephemeris,category,start,end,latitude,longitude,profile_name='ramesey-retain-money',
           tradition='Ramesey 1653',houses='regiomontanus',required=None,min_minutes=5,utc_hours=None,
           ascendant_signs=None,angle_step_minutes=10):
    p=profile_for(profile_name,category,tradition)
    required=p['rules'] if required is None else list(required)
    if start.tzinfo is None or end.tzinfo is None:raise ValueError('Search bounds require explicit UTC offsets')
    start,end=start.astimezone(timezone.utc),end.astimezone(timezone.utc)
    days=(end-start).total_seconds()/86400
    if not 0<days<=7:raise ValueError('Search duration must be positive and at most seven days')
    if not math.isfinite(latitude) or not math.isfinite(longitude) or abs(latitude)>60 or not -180<=longitude<=180:
        raise ValueError('Electional search validated for latitudes -60..60, longitudes -180..180')
    if not math.isfinite(min_minutes) or min_minutes<0:raise ValueError('Minimum window must be finite/nonnegative')
    if angle_step_minutes not in (5,10):raise ValueError('Supported angular scan steps: 5 or 10 minutes')
    if utc_hours and not (len(utc_hours)==2 and all(type(v) is int for v in utc_hours) and 0<=utc_hours[0]<utc_hours[1]<=24):
        raise ValueError('UTC-hour constraint requires two integers, 0 <= start < end <= 24')
    if ascendant_signs is not None and (not ascendant_signs or any(type(v) is not int or not 0<=v<12 for v in ascendant_signs)):
        raise ValueError('Ascendant constraint uses nonempty zero-based sign indices 0..11')
    if not required or not set(required)<=set(p['rules']):raise ValueError('Unknown or empty required-rule selection')
    conflicts=[]
    if ascendant_signs and 'asc-sign' in required and not set(ascendant_signs)&set(p['signs']):
        conflicts.append({'type':'constraint_conflict','rule':'asc-sign','description':'User Ascendant signs and source profile modality have no intersection.'})
    # Partition at every predicate discontinuity. No chart/time grid is used to
    # declare an entire interval favorable merely because a midpoint passed.
    planet_times=[start+timedelta(hours=3*i) for i in range(math.ceil(days*8))]+[end]
    cuts={start,end};samples={};speed_samples={}
    @lru_cache(maxsize=32768)
    def value(name,date):return float(ephemeris.longitudes(name,[date])[0])
    @lru_cache(maxsize=16384)
    def speed(name,date):
        t=ephemeris.ts.from_datetime(date)
        values=ephemeris.longitudes_at_tt(name,[t.tt-.005,t.tt+.005])
        return signed(float(values[1]-values[0]))/.01
    for name in CLASSICAL:
        samples[name]=ephemeris.longitudes(name,planet_times)
        for boundary in range(0,360,30):
            cuts.update(roots(planet_times,samples[name],boundary,lambda d,n=name:value(n,d)))
        speed_samples[name]=[speed(name,d) for d in planet_times]
        cuts.update(roots(planet_times,speed_samples[name],0,lambda d,n=name:speed(n,d)))
    angular_times=[start+timedelta(minutes=angle_step_minutes*i) for i in range(math.ceil(days*1440/angle_step_minutes))]+[end]
    @lru_cache(maxsize=32768)
    def geometry(date):
        armc,eps=frame(ephemeris.ts.from_datetime(date),longitude)
        cs=cusps(armc,latitude,eps,houses);asc,mc=axes(armc,latitude,eps)
        return asc,mc,cs[1]
    for index in range(3):
        series=[geometry(t)[index] for t in angular_times]
        for boundary in range(0,360,30):
            cuts.update(roots(angular_times,series,boundary,lambda d,i=index:geometry(d)[i]))
    if utc_hours:
        day=start.replace(hour=0,minute=0,second=0,microsecond=0)
        while day<end:
            for hour in utc_hours:
                cut=day+timedelta(hours=hour)
                if start<cut<end:cuts.add(cut)
            day+=timedelta(days=1)
    ordered=sorted(cuts)
    probe_dates=sorted({a+(b-a)*f for a,b in zip(ordered,ordered[1:]) for f in (.25,.5,.75)})
    probe_jds=ephemeris.ts.from_datetimes(probe_dates).tt
    probe_positions={n:ephemeris.longitudes(n,probe_dates) for n in CLASSICAL}
    probe_speeds={n:((ephemeris.longitudes_at_tt(n,probe_jds+.005)-ephemeris.longitudes_at_tt(n,probe_jds-.005)+180)%360-180)/.01 for n in CLASSICAL}
    probe_index={date:i for i,date in enumerate(probe_dates)}
    def state(date):
        i=probe_index.get(date)
        signs={n:int((value(n,date) if i is None else float(probe_positions[n][i]))//30) for n in CLASSICAL}
        speeds={n:(speed(n,date) if i is None else float(probe_speeds[n][i])) for n in CLASSICAL}
        a,mc,second=geometry(date)
        trace=evaluate(signs,speeds,a,mc,second,p,required)
        user_ok=(not utc_hours or utc_hours[0]<=date.hour+date.minute/60+date.second/3600<utc_hours[1]) and (ascendant_signs is None or int(a//30) in ascendant_signs)
        return trace,user_ok
    intervals=[];rejected=[];unresolved=[]
    for a,b in zip(ordered,ordered[1:]):
        if (b-a).total_seconds()<=2:
            unresolved.append({'start':a.isoformat(),'end':b.isoformat(),'reason':'Partition narrower than two-second boundary guard; not certified.'})
            continue
        mid=a+(b-a)/2;trace,user_ok=state(mid)
        checks=[state(a+(b-a)*fraction) for fraction in (.25,.75)]
        signature=lambda result:([r['status'] for r in result[0]['rules']],result[1])
        if any(signature(check)!=signature((trace,user_ok)) for check in checks):
            unresolved.append({'start':a.isoformat(),'end':b.isoformat(),'reason':'Predicate changed within derived partition; not returned as a candidate.'})
            continue
        if trace['passes_selected_rules'] and user_ok:
            if intervals and intervals[-1][1]==a:intervals[-1]=(intervals[-1][0],b)
            else:intervals.append((a,b))
        else:rejected.append({'start':a.isoformat(),'end':b.isoformat(),'violated_required':[r['id'] for r in trace['rules'] if r['required'] and r['status']=='violated'],'user_constraints_satisfied':user_ok})
    candidates=[]
    for a,b in intervals:
        a=a if a==start else a+timedelta(seconds=1)
        b=b if b==end else b-timedelta(seconds=1)
        if (b-a).total_seconds()<min_minutes*60:continue
        mid=a+(b-a)/2;trace,_=state(mid)
        c=chart(ephemeris,mid.replace(tzinfo=None).isoformat(),'UTC',latitude,longitude,Settings(tradition='medieval/traditional',houses=houses))
        candidates.append({'start_inclusive_utc':a.isoformat(),'end_exclusive_utc':b.isoformat(),
            'duration_minutes':(b-a).total_seconds()/60,'representative_utc':mid.isoformat(),'chart':c,
            'rule_trace':trace,'diagnostics':diagnostics(ephemeris,c),'qualification':'Satisfies selected implemented predicates only; complete source requirements remain unknown.'})
    assessments=[]
    for candidate in candidates:
        assessments.extend(certify(ephemeris,candidate,latitude,longitude,houses,profile_name))
    for interval in rejected:
        interval.update(classification='rejected',rule_trace=[{'id':rid,'status':'violated',
            'source':CATALOG['rule_parameters'][rid].get('source',p['source']),
            'locator':CATALOG['rule_parameters'][rid].get('locator',p['locator'])} for rid in interval['violated_required']])
    for interval in unresolved:interval['classification']='indeterminate'
    return {'technique_id':1,'application':'electional search','release_status':'experimental','category':category,'profile':profile_name,'tradition':tradition,
        'range':{'start_utc':start.isoformat(),'end_exclusive_utc':end.isoformat()},'location':{'latitude':latitude,'longitude':longitude},
        'houses':houses,'required_rules':required,'disabled_rules':[r for r in p['rules'] if r not in required],
        'constraints':{'minimum_minutes':min_minutes,'utc_hours':utc_hours,'ascendant_signs':ascendant_signs},
        'candidates':candidates,'assessed_windows':assessments,'eligible_windows':[],
        'classification_policy':REQUIREMENTS['classification'],'requirements_version':2,
        'rejected_intervals':rejected,'unresolved_intervals':unresolved,'conflicts':conflicts,
        'source_profile':p,'source_conflicts':CATALOG['source_conflicts'],'unknown_criteria':CATALOG['incomplete_criteria'],
        'search_method':{'planet_scan_hours':3,'angle_scan_minutes':angle_step_minutes,'root_bracket_seconds':.25,
            'boundary_guard_seconds':1,'partition_points':len(ordered),
            'coverage':'Partitions at computed sign ingresses, Ascendant/MC/second-cusp sign changes and stations; quarter-point checks flag unresolved cells.',
            'limitation':'Not a formal global completeness proof; unseen multiple reversals within a scan interval can be missed. Minimum-duration/user constraints can exclude short intervals.'},
        'reproducibility':{'kernel_sha256':ephemeris.digest,'skyfield':'1.54'},
        'limitations':['No universal score, probability of success, or guarantee that these incomplete traditional criteria establish a favorable outcome.',
                       'No horary question-chart analysis; Technique #5 remains out of scope.',
                       'Exact lunar sequence is computed; source-complete historical prohibition, fortification and radix adjudication remain indeterminate.']}

def register_knowledge(registry):
    from .knowledge import Rule
    for name,p in CATALOG['profiles'].items():
        sid='election-source:'+name
        registry.add_source({'id':sid,'author':'William Ramesey','edition':'Astrologia Restaurata 1653, Liber III',
            'url':p['source'],'ingestion':'metadata_only','rights_note':CATALOG['rights']})
        registry.add_rule(Rule('election.'+name,1,1,'electional',p['tradition'],sid,p['locator'],p['interpretation'],
            'election_profile',{'category':p['category'],'signs':p['signs'],'required_rules':p['rules']},'proposed','traditional',[]))
    for key,source in REQUIREMENTS['sources'].items():
        registry.add_source({'id':'ramesey-v2:'+key,'author':'William Ramesey','edition':'Astrologia Restaurata, 1653',
            'url':source['url'],'ingestion':'metadata_only','rights_note':REQUIREMENTS['rights']})
    for r in REQUIREMENTS['rules']:
        registry.add_rule(Rule('election.retention.'+r['id'],2,1,'electional','Ramesey 1653','ramesey-v2:'+r['source'],
            r['locator'],r['method'],'election_requirement',r,'proposed','traditional',[]))
