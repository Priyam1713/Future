"""Prospective evidence ledger and descriptive human comparisons,not prophecy."""
import copy
import html
import json
from pathlib import Path
import re
from .scrying import load_input,freeze
# Narrow pure utilities only;no43ranking,nullmodel ortrial schema reused.
from .remote_viewing import canonical,digest,bytes_hash,obj,text,identifier,integer,timestamp,hexhash,file_bytes

ROOT=Path(__file__).resolve().parents[1]
PROFILE='dunne-revised-prospective-dream-ledger-v1'
PROFILE_HASH='9f1bf381bf473d31c9cb62b159c890e46437c84b1a69f1e8d551652e8596c712'


def assets():
    p=load_input(ROOT/'knowledge/prophetic_dreams_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned dream protocol mismatch')
    for name,key in [('sources','source_manifest_sha256'),('source_freeze_v1','source_freeze_sha256'),('reference_v1','reference_sha256')]:
        value=load_input(ROOT/f'knowledge/prophetic_dreams_{name}.json')
        if digest(value)!=p[key]:raise ValueError('Pinned dream provenance mismatch')
    return p


DATA=freeze(assets())


def interval(v):
    if v is None:return None
    obj(v,['start','end','precision']);start=timestamp(v['start']);end=timestamp(v['end'])
    if start>end or v['precision'] not in ('second','minute','hour','day','reported_interval'):
        raise ValueError('Ordered declared interval andprecision required')
    return start,end


def window_status(value,window):
    i=interval(value)
    if i is None:return 'unknown'
    start,end=timestamp(window['start']),timestamp(window['end'])
    if start>end:raise ValueError('Reversed window')
    if i[1]<start or i[0]>end:return 'outside'
    return 'inside' if i[0]>=start and i[1]<=end else 'uncertain'


def chronology(record_at,lock_at,occurrence,discovery_at,outcome_known=False,conflicts=False):
    record=timestamp(record_at);lock=timestamp(lock_at)
    if record>lock:raise ValueError('Record cannot follow original lock')
    if conflicts:return 'conflicting_time'
    if outcome_known:return 'outcome_known_at_capture'
    i=interval(occurrence)
    if i is None:return 'timing_unknown'
    if i[0]>lock:return 'future_event'
    if i[1]<record and discovery_at is not None and timestamp(discovery_at)>lock:
        return 'record_after_event_before_discovery'
    if i[1]<=record:return 'event_before_or_at_record'
    return 'overlaps_lock'


def _nonempty(v,limit=4000):
    if not text(v,limit).strip():raise ValueError('Nonempty declared text required')


def asset(a,root):
    obj(a,DATA['asset_fields']);hexhash(a['sha256'])
    for k in ('holder','permission','provenance'):_nonempty(a[k])
    if bytes_hash(file_bytes(root,a['path']))!=a['sha256']:raise ValueError('Local evidence/attachment digest mismatch')


def check_plan(p):
    obj(p,DATA['plan_fields'])
    if type(p['schema_version']) is not int or p['schema_version']!=1 or p['profile']!=PROFILE or p['profile_sha256']!=PROFILE_HASH:
        raise ValueError('Exact dream protocol/version/hash required')
    for k in ('study_id','participant','coordinator'):identifier(p[k])
    if p['origin'] not in ('human','simulated') or type(p['privacy_consent']) is not bool:raise ValueError('Explicit origin/privacy declaration required')
    if p['blinding'] not in ('declared_blind','descriptive_unblinded'):raise ValueError('Explicit blinding policy required')
    js=p['judges']
    if not isinstance(js,list) or not 1<=len(js)<=8:raise ValueError('Predeclared judges required')
    for j in js:identifier(j)
    if len(set([p['participant'],p['coordinator'],*js]))!=len(js)+2:raise ValueError('Distinct participant/coordinator/judge roles required')
    created=timestamp(p['created_at']);slots=p['slots']
    if not isinstance(slots,list) or not 1<=len(slots)<=100:raise ValueError('Bounded planned slots required')
    for s in slots:
        obj(s,DATA['slot_fields']);identifier(s['id'])
        if not created<timestamp(s['open_at'])<=timestamp(s['due_at']):raise ValueError('Plan must precede ordered slot schedule')
    if len({s['id'] for s in slots})!=len(slots):raise ValueError('Duplicate slot IDs')
    u=p['universe'];obj(u,DATA['universe_fields']);identifier(u['id']);identifier(u['collector']);integer(u['version'],1,10000);_nonempty(u['collection_rule'])
    if p['universe_sha256']!=digest(u):raise ValueError('Frozen universe hash mismatch')
    if not isinstance(u['event_ids'],list) or not 1<=len(u['event_ids'])<=100:raise ValueError('Finite event manifest required')
    for e in u['event_ids']:identifier(e)
    if len(set(u['event_ids']))!=len(u['event_ids']):raise ValueError('Duplicate event IDs')
    obj(u['collection_window'],['start','end'])
    if timestamp(u['collection_window']['start'])>timestamp(u['collection_window']['end']):raise ValueError('Reversed collection window')
    win=p['window'];obj(win,DATA['window_fields'])
    if win['boundary']!='closed' or win['endpoint'] not in ('occurrence','publication','discovery') or timestamp(win['start'])>timestamp(win['end']):
        raise ValueError('Frozen closed comparison window required')
    fs=p['features']
    if not isinstance(fs,list) or not 1<=len(fs)<=12:raise ValueError('Bounded predeclared human features required')
    for f in fs:obj(f,DATA['feature_fields']);identifier(f['id']);_nonempty(f['description'])
    if len({f['id'] for f in fs})!=len(fs):raise ValueError('Duplicate feature IDs')
    for k,v in DATA['plan_constants'].items():
        if p[k]!=v:raise ValueError('Frozen denominator/scoring policy required')


def version_hash(entry):return digest(dict(domain=DATA['domains']['version'],entry=entry))
def original_lock(entry,at):return digest(dict(domain=DATA['domains']['lock'],kind='original',entry_sha256=version_hash(entry),at=at))


def create(plan):
    assets();check_plan(plan)
    return dict(schema_version=1,visibility='private_ledger',plan=copy.deepcopy(plan),plan_sha256=digest(plan),events=[])


def _dream(entry,p,at,root):
    obj(entry,DATA['dream_fields']);identifier(entry['id'])
    slot=next((s for s in p['slots'] if s['id']==entry['slot_id']),None)
    if slot is None or entry['participant']!=p['participant']:raise ValueError('Wrong participant orslot')
    record=timestamp(entry['first_record_at'])
    if record<timestamp(slot['open_at']) or record>timestamp(at):raise ValueError('Invalid first-record chronology')
    occurrence=interval(entry['occurrence'])
    if occurrence and occurrence[1]>record:raise ValueError('Dream occurrence cannot follow first record')
    text(entry['text']);obj(entry['details'],[],[f['id'] for f in p['features']])
    for v in entry['details'].values():text(v,4000)
    if type(entry['outcome_known']) is not bool or type(entry['privacy_consent']) is not bool:raise ValueError('Explicit knowledge/consent declarations required')
    if entry['witness'] not in ('none','declared_unverified'):raise ValueError('No independently verified witness supported')
    ats=entry['attachments']
    if not isinstance(ats,list) or len(ats)>8:raise ValueError('Bounded attachment list required')
    for a in ats:asset(a,root)


def _event_record(e,p,at,root):
    obj(e,DATA['event_fields']);u=p['universe']
    if e['id'] not in u['event_ids'] or e['universe_id']!=u['id'] or type(e['universe_version']) is not int or e['universe_version']!=u['version']:
        raise ValueError('Wrong event universe/version/ID')
    identifier(e['dedup_group']);text(e['text']);interval(e['occurrence'])
    for k in ('publication_at','discovery_at'):
        if e[k] is not None:timestamp(e[k])
    if type(e['common']) is not bool or e['coverage'] not in ('complete','known_omissions','unknown'):raise ValueError('Explicit common-event andcoverage declarations required')
    if not isinstance(e['conflicts'],list) or len(e['conflicts'])>12:raise ValueError('Bounded conflict list required')
    for c in e['conflicts']:_nonempty(c)
    asset(e['evidence'],root)
    collection=p['universe']['collection_window']
    if not timestamp(collection['start'])<=timestamp(at)<=timestamp(collection['end']):raise ValueError('Collection outside fixed collection window')


def _ctx(plan):return dict(state='recording',last_at=plan['created_at'],entries={},slot_status={},event_records={},exposures={},ratings={},judge_lock=None,comments=[])


def _pairs(ctx,p):
    rows=[];groups={}
    for event_id in p['universe']['event_ids']:
        e=ctx['event_records'][event_id];groups.setdefault(e['dedup_group'],event_id)
    for di,(did,d) in enumerate(ctx['entries'].items(),1):
        if d['lock_at'] is None:continue
        entry=d['original'];slot=next(s for s in p['slots'] if s['id']==entry['slot_id'])
        for ei,eid in enumerate(p['universe']['event_ids'],1):
            e=ctx['event_records'][eid];occ=interval(e['occurrence']);conflicts=list(e['conflicts'])
            for k in ('publication_at','discovery_at'):
                if e[k] is not None and timestamp(e[k])>timestamp(e['_collected_at']):conflicts.append(k+'_after_collection')
            if occ and occ[1]>timestamp(e['_collected_at']):conflicts.append('occurrence_after_collection')
            if e['publication_at'] and e['discovery_at'] and timestamp(e['discovery_at'])<timestamp(e['publication_at']):conflicts.append('discovery_before_publication')
            chrono=chronology(entry['first_record_at'],d['lock_at'],e['occurrence'],e['discovery_at'],entry['outcome_known'],bool(conflicts))
            endpoint=p['window']['endpoint']
            v=e['occurrence'] if endpoint=='occurrence' else (dict(start=e[endpoint+'_at'],end=e[endpoint+'_at'],precision='second') if e[endpoint+'_at'] else None)
            inside=window_status(v,p['window']);iv=interval(v);reasons=[]
            if timestamp(entry['first_record_at'])>timestamp(slot['due_at']):reasons.append('late_entry')
            if ctx['slot_status'].get(entry['slot_id'],{}).get('status') in ('withdrawn','invalid','excluded'):reasons.append('slot_'+ctx['slot_status'][entry['slot_id']]['status'])
            if entry['outcome_known']:reasons.append('outcome_known_at_capture')
            if conflicts:reasons.append('conflicting_time')
            if inside!='inside':reasons.append('window_'+inside)
            if iv is None or iv[0]<=timestamp(d['lock_at']):reasons.append('endpoint_not_after_lock')
            if groups[e['dedup_group']]!=eid:reasons.append('duplicate_event')
            if e['discovery_at'] is not None and timestamp(e['discovery_at'])<=timestamp(d['lock_at']):reasons.append('outcome_discovered_before_lock')
            rows.append(dict(pair_id=f'd{di}:e{ei}',dream_id=did,event_id=eid,original_sha256=d['original_sha256'],original_lock=d['lock_sha256'],chronology=chrono,endpoint=endpoint,window_status=inside,eligible=not reasons,exclusion_reasons=reasons,conflicts=conflicts,duplicate=groups[e['dedup_group']]!=eid,common=e['common'],eligibility_scope='future_event_content' if endpoint=='occurrence' else 'prospective_'+endpoint+'_information'))
    return rows


def _judge_lock(ledger):
    records=[e for e in ledger['events'] if e['accepted'] and e['action'] in ('expose','rate')]
    return digest(dict(domain=DATA['domains']['lock'],kind='judges',records=records))


def _process(ledger,ctx,action,actor,at,payload,root):
    p=ledger['plan'];identifier(actor);time=timestamp(at)
    if time<=timestamp(ctx['last_at']):raise ValueError('Actions must strictly increase in time')
    if not isinstance(action,str) or action not in DATA['actions']:raise ValueError('Unsupported ledger action')
    obj(payload,DATA['actions'][action])
    if action not in DATA['state_machine'][ctx['state']]:raise ValueError('Action prohibited in current ledger state')
    role=p['participant'] if action in ('record','lock_entry','amend') else p['universe']['collector'] if action=='event' else None
    if action=='slot_status':permitted=[p['participant'],p['coordinator']]
    elif action=='rate':permitted=p['judges']
    else:permitted=[role or p['coordinator']]
    if actor not in permitted:raise ValueError('Unauthorized ledger role')
    if action=='record':
        e=payload['entry'];_dream(e,p,at,root)
        if e['id'] in ctx['entries'] or any(d['original']['slot_id']==e['slot_id'] for d in ctx['entries'].values()) or e['slot_id'] in ctx['slot_status']:
            raise ValueError('Duplicate entry oroccupied recording slot')
        ctx['entries'][e['id']]=dict(original=copy.deepcopy(e),original_sha256=version_hash(e),lock_at=None,lock_sha256=None,versions=[dict(sha256=version_hash(e),parent=None,at=e['first_record_at'],text=e['text'],outcome_known=e['outcome_known'],reason='original')])
    elif action=='slot_status':
        sid=payload['slot_id'];status=payload['status'];_nonempty(payload['reason'])
        slot=next((s for s in p['slots'] if s['id']==sid),None)
        if slot is None or time<timestamp(slot['open_at']) or sid in ctx['slot_status']:raise ValueError('Invalid/duplicate slot status')
        has=any(d['original']['slot_id']==sid for d in ctx['entries'].values())
        if status not in ('nonrecall','unsubmitted','withdrawn','invalid','excluded') or (has and status in ('nonrecall','unsubmitted')):raise ValueError('Conflicting recording slot declarations')
        if status=='unsubmitted' and time<=timestamp(slot['due_at']):raise ValueError('Unsubmitted slot cannot precede deadline')
        ctx['slot_status'][sid]=copy.deepcopy(payload)|dict(at=at)
    elif action=='lock_entry':
        identifier(payload['entry_id'])
        d=ctx['entries'].get(payload['entry_id'])
        if d is None or d['lock_at'] is not None:raise ValueError('Original entry missing oralready locked')
        expected=original_lock(d['original'],at)
        if payload['digest']!=expected:raise ValueError('Original entry lock mismatch')
        d['lock_at']=at;d['lock_sha256']=expected
    elif action=='amend':
        identifier(payload['entry_id'])
        d=ctx['entries'].get(payload['entry_id'])
        if d is None or d['lock_at'] is None or payload['parent_sha256']!=d['versions'][-1]['sha256']:raise ValueError('Amendment requires retained locked parent version')
        text(payload['text']);_nonempty(payload['reason'])
        if type(payload['outcome_known']) is not bool:raise ValueError('Amendment outcome knowledge required')
        value=copy.deepcopy(payload)|dict(at=at)
        value['sha256']=digest(dict(domain=DATA['domains']['version'],amendment=value))
        d['versions'].append(value)
    elif action=='event':
        e=payload['event'];_event_record(e,p,at,root)
        if e['id'] in ctx['event_records']:raise ValueError('Event slot already collected')
        ctx['event_records'][e['id']]=copy.deepcopy(e)|dict(_collected_at=at)
    elif action=='seal':
        if any(time<=timestamp(s['due_at']) for s in p['slots']):raise ValueError('Recording schedule not finished')
        if set(ctx['event_records'])!=set(p['universe']['event_ids']) or any(d['lock_at'] is None for d in ctx['entries'].values()):raise ValueError('Complete frozen event ledger andoriginal locks required')
        ctx['state']='sealed'
    elif action=='expose':
        j=payload['judge_id']
        if j not in p['judges'] or j in ctx['exposures'] or payload['knowledge'] not in ('unaware','aware','unknown'):raise ValueError('Invalid/duplicate judge exposure')
        ctx['exposures'][j]=dict(at=at,knowledge=payload['knowledge'])
    elif action=='rate':
        if actor not in ctx['exposures'] or actor in ctx['ratings']:raise ValueError('Judge must expose before one complete rating submission')
        ratings=payload['ratings'];pairs=[x['pair_id'] for x in _pairs(ctx,p)];obj(ratings,pairs);text(payload['notes'])
        if any(v not in DATA['ratings'] for v in ratings.values()):raise ValueError('Frozen human rating categories required')
        ctx['ratings'][actor]=dict(at=at,ratings=copy.deepcopy(ratings),notes=payload['notes'])
    elif action=='lock_judges':
        if set(ctx['ratings'])!=set(p['judges']) or payload['digest']!=_judge_lock(ledger):raise ValueError('All predeclared judge ratings andexact lock required')
        ctx['judge_lock']=payload['digest'];ctx['state']='judge_locked'
    elif action=='reveal':ctx['state']='revealed'
    elif action=='commentary':
        if payload['kind'] not in ('association','feedback'):raise ValueError('Explicit later commentary kind required')
        text(payload['text']);text(payload['event_reference'],1000);ctx['comments'].append(copy.deepcopy(payload)|dict(at=at))
    elif action=='finish':ctx['state']='reported'
    elif action=='terminate':
        if payload['status'] not in ('aborted','excluded'):raise ValueError('Explicit terminal ledger status required')
        _nonempty(payload['reason']);ctx['state']=payload['status']
    ctx['last_at']=at;return ctx


def _row(ledger,action,actor,at,payload,accepted,error):
    previous=ledger['events'][-1]['sha256'] if ledger['events'] else ledger['plan_sha256']
    e=dict(seq=len(ledger['events'])+1,previous=previous,action=action,actor=actor,at=at,payload=copy.deepcopy(payload),accepted=accepted,error=error)
    e['sha256']=digest(dict(domain=DATA['domains']['event'],event=e));return e


def verify(ledger,root=ROOT):
    assets();obj(ledger,['schema_version','visibility','plan','plan_sha256','events'])
    if type(ledger['schema_version']) is not int or ledger['schema_version']!=1 or ledger['visibility']!='private_ledger':raise ValueError('Private ledger schema required')
    check_plan(ledger['plan'])
    if ledger['plan_sha256']!=digest(ledger['plan']):raise ValueError('Frozen study plan changed')
    if not isinstance(ledger['events'],list) or len(ledger['events'])>5000:raise ValueError('Bounded complete history required')
    replay=copy.deepcopy(ledger);replay['events']=[];ctx=_ctx(ledger['plan'])
    for event in ledger['events']:
        obj(event,['seq','previous','action','actor','at','payload','accepted','error','sha256'])
        if type(event['seq']) is not int or event['seq']!=len(replay['events'])+1 or type(event['accepted']) is not bool:raise ValueError('Event counter/decision mismatch')
        new=copy.deepcopy(ctx)
        try:new=_process(replay,new,event['action'],event['actor'],event['at'],event['payload'],root);accepted=True;error=None
        except ValueError as exc:accepted=False;error=str(exc)
        expected=_row(replay,event['action'],event['actor'],event['at'],event['payload'],accepted,error)
        if expected!=event:raise ValueError('Ledger history,version,hash ordecision mismatch')
        replay['events'].append(event)
        if accepted:ctx=new
    return ctx


def apply(ledger,action,actor,at,payload,root=ROOT):
    ctx=verify(ledger,root);out=copy.deepcopy(ledger)
    try:_process(out,copy.deepcopy(ctx),action,actor,at,payload,root);accepted=True;error=None
    except ValueError as exc:accepted=False;error=str(exc)
    out['events'].append(_row(out,action,actor,at,payload,accepted,error));verify(out,root);return out


def pairs(ledger,root=ROOT):
    ctx=verify(ledger,root)
    if ctx['state']=='recording':raise ValueError('Comparison requires sealed complete ledger')
    return _pairs(ctx,ledger['plan'])


def judge_lock(ledger):return _judge_lock(ledger)


def judge_packet(ledger,judge_id,root=ROOT):
    ctx=verify(ledger,root);p=ledger['plan']
    if ctx['state']!='sealed' or judge_id not in ctx['exposures']:raise ValueError('Recorded exposure andsealed ledger required')
    if not p['privacy_consent'] or any(not d['original']['privacy_consent'] for d in ctx['entries'].values()):raise ValueError('Explicit participant/entry export consent required')
    ds=[dict(alias=f'd{i}',text=d['original']['text'],original_sha256=d['original_sha256']) for i,d in enumerate(ctx['entries'].values(),1)]
    es=[dict(alias=f'e{i}',text=ctx['event_records'][eid]['text']) for i,eid in enumerate(p['universe']['event_ids'],1)]
    out=dict(schema_version=1,visibility='judge_packet',profile=PROFILE,profile_sha256=PROFILE_HASH,cue=p['study_id'],origin=p['origin'],judge_id=judge_id,instructions='Content ratings only under declared features;all pairs required. Chronology assessed separately. Public-event familiarity may prevent blinding.',features=copy.deepcopy(p['features']),rating_scale=list(DATA['ratings']),dreams=ds,events=es,pairs=[f'{d["alias"]}:{e["alias"]}' for d in ds for e in es])
    out['packet_sha256']=digest(dict(domain=DATA['domains']['packet'],packet=out));validate_packet(out);return out


def validate_packet(v):
    obj(v,DATA['packet_fields'])
    if type(v['schema_version']) is not int or v['schema_version']!=1 or v['visibility']!='judge_packet' or v['profile']!=PROFILE or v['profile_sha256']!=PROFILE_HASH:raise ValueError('Exact judge packet schema required')
    raw={k:x for k,x in v.items() if k!='packet_sha256'}
    if v['packet_sha256']!=digest(dict(domain=DATA['domains']['packet'],packet=raw)):raise ValueError('Judge packet digest mismatch')
    identifier(v['cue']);identifier(v['judge_id'])
    if v['origin'] not in ('human','simulated') or v['rating_scale']!=list(DATA['ratings']):raise ValueError('Explicit origin/frozen categories required')
    if v['instructions']!='Content ratings only under declared features;all pairs required. Chronology assessed separately. Public-event familiarity may prevent blinding.':raise ValueError('Neutral fixed judge instructions required')
    if not isinstance(v['features'],list) or not 1<=len(v['features'])<=12:raise ValueError('Bounded human features required')
    for f in v['features']:obj(f,['id','description']);identifier(f['id']);text(f['description'],4000)
    for key,prefix in [('dreams','d'),('events','e')]:
        xs=v[key]
        if not isinstance(xs,list) or len(xs)>100:raise ValueError('Bounded packet entries required')
        for i,x in enumerate(xs,1):
            obj(x,['alias','text']+(['original_sha256'] if key=='dreams' else []));text(x['text'])
            if x['alias']!=prefix+str(i):raise ValueError('Neutral ordered aliases required')
            if key=='dreams':hexhash(x['original_sha256'])
    if v['pairs']!=[f'{d["alias"]}:{e["alias"]}' for d in v['dreams'] for e in v['events']]:raise ValueError('Complete packet pairspace required')
    return True


def export_packet(packet,directory):
    validate_packet(packet);out=Path(directory)
    if out.exists():raise ValueError('Fresh packet directory required')
    out.mkdir(parents=True);(out/'packet.json').write_bytes(canonical(packet)+b'\n')


def report(ledger,root=ROOT):
    ctx=verify(ledger,root);p=ledger['plan'];complete=ctx['state']!='recording' and set(ctx['event_records'])==set(p['universe']['event_ids']) and all(d['lock_at'] is not None for d in ctx['entries'].values())
    ps=_pairs(ctx,p) if complete else [];slots=[]
    for s in p['slots']:
        d=next((d for d in ctx['entries'].values() if d['original']['slot_id']==s['id']),None)
        status=ctx['slot_status'].get(s['id'],{}).get('status')
        if status is None:status=('late' if timestamp(d['original']['first_record_at'])>timestamp(s['due_at']) else 'recorded') if d else 'unsubmitted' if timestamp(ctx['last_at'])>timestamp(s['due_at']) else 'pending'
        slots.append(copy.deepcopy(s)|dict(status=status,entry_id=d['original']['id'] if d else None,declaration=ctx['slot_status'].get(s['id'])))
    categories={};disagreements=[]
    for j,data in ctx['ratings'].items():
        categories[j]={c:sum(data['ratings'][x['pair_id']]==c for x in ps if x['eligible']) for c in DATA['ratings']}
    for x in ps:
        x['ratings']={j:data['ratings'][x['pair_id']] for j,data in ctx['ratings'].items()}
        if len(set(x['ratings'].values()))>1:disagreements.append(x['pair_id'])
    reveals=[e for e in ledger['events'] if e['accepted'] and e['action']=='reveal']
    all_blind=p['blinding']=='declared_blind' and set(ctx['exposures'])==set(p['judges']) and all(e['knowledge']=='unaware' for e in ctx['exposures'].values())
    all_categories={j:{category:sum(value==category for value in data['ratings'].values()) for category in DATA['ratings']} for j,data in ctx['ratings'].items()}
    out=dict(schema_version=1,visibility='private_report',profile=PROFILE,profile_sha256=PROFILE_HASH,source_edition=DATA['source_edition'],origin=p['origin'],state=ctx['state'],plan_sha256=ledger['plan_sha256'],universe_sha256=p['universe_sha256'],procedural_integrity_verified_from_files=True,independently_witnessed=False,declared_blind_judging=all_blind,source_layers=dict(direct='RevisedDunne recording practices anddocumentary references;not1927wordingcertification.',participant='Manualrawtext,times,knowledge,rights andhumanratings areattributed declarations.',editorial='Frozen chronology,version/hash,pair enumeration anddenominator policies.',unsupported='Prophecy,retrocausalphysics,hiddeninformation,diagnosis,universalchance orsymbolmeaning.'),slots=slots,slot_counts={status:sum(s['status']==status for s in slots) for status in ['recorded','late','nonrecall','unsubmitted','pending','withdrawn','invalid','excluded']},original_entries=copy.deepcopy(ctx['entries']),events=copy.deepcopy(ctx['event_records']),universe=copy.deepcopy(p['universe']),collection_complete=bool(ctx['event_records']) and all(e['coverage']=='complete' for e in ctx['event_records'].values()) and len(ctx['event_records'])==len(p['universe']['event_ids']),window=copy.deepcopy(p['window']),features=copy.deepcopy(p['features']),pairs=ps,pair_counts=dict(total=len(ps),eligible=sum(x['eligible'] for x in ps),excluded=sum(not x['eligible'] for x in ps),duplicates=sum(x['duplicate'] for x in ps),common=sum(x['common'] for x in ps)),per_judge_category_counts=categories,judge_records=copy.deepcopy(ctx['ratings']),judge_exposures=copy.deepcopy(ctx['exposures']),judge_lock=ctx['judge_lock'],judge_disagreements=disagreements,reveal_at=reveals[0]['at'] if reveals else None,post_reveal_commentary=copy.deepcopy(ctx['comments']),rejected_attempts=[copy.deepcopy(e) for e in ledger['events'] if not e['accepted']],statistical_scope='Descriptive only;no validated sampling/nullmodel. No inherited43five-choice chance baseline.',rights_privacy=DATA['privacy'],limitations=list(DATA['limits']),ledger=copy.deepcopy(ledger))
    out['per_judge_all_pair_category_counts']=all_categories
    out['eligible_category_count_scope']='per_judge_category_counts includes only eligible rows;all_pair counts retain ratings onexcluded rows.'
    out['report_sha256']=digest(dict(domain=DATA['domains']['report'],report=out));return out


def read(v,root=ROOT,registry=None):
    assets()
    if not isinstance(v,dict) or not isinstance(v.get('task'),str) or v['task'] not in DATA['requests']:raise ValueError('Supported dream ledger request required')
    task=v['task'];obj(v,['schema_version','profile','task',*DATA['requests'][task]])
    if type(v['schema_version']) is not int or v['schema_version']!=1 or v['profile']!=PROFILE:raise ValueError('Exact dream request profile/schema required')
    if registry:
        for source in load_input(ROOT/'knowledge/prophetic_dreams_sources.json'):registry.add_source(source)
    if task=='create':return dict(visibility='private_ledger',accepted=True,ledger=create(v['plan']))
    if task=='apply':
        ledger=apply(v['ledger'],v['action'],v['actor'],v['at'],v['payload'],root)
        return dict(visibility='private_ledger',accepted=ledger['events'][-1]['accepted'],error=ledger['events'][-1]['error'],ledger=ledger)
    if task=='report':return report(v['ledger'],root)
    if task=='judge_packet':return judge_packet(v['ledger'],v['judge_id'],root)
    if task=='validate_packet':validate_packet(v['packet']);return dict(visibility='public_validation',packet_valid=True,profile=PROFILE)
    ids=v['ids']
    if not isinstance(ids,list) or not 1<=len(ids)<=3 or any(not isinstance(x,str) for x in ids) or len(set(ids))!=len(ids):raise ValueError('Exact documentary reference IDs required')
    records=load_input(ROOT/'knowledge/prophetic_dreams_reference_v1.json')['records'];by={x['id']:x for x in records}
    if any(x not in by for x in ids):raise ValueError('Unknown documentary reference')
    return dict(visibility='documentary_reference',profile=PROFILE,source_edition=DATA['source_edition'],records=[by[x] for x in ids],qualification='Historicalattribution only;notverifiedprediction orparticipantdata.')


def markdown(v):
    s=json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False);fence='`'*max(3,max((len(x) for x in re.findall(r'`+',s)),default=0)+1)
    return '# Prospective dream/event ledger\n\nVisibility: '+html.escape(v['visibility'])+'\n\nDescriptive procedural evidence only;no prophecy orstatisticalcertification.\n\n## Exact replay output\n\n'+fence+'json\n'+s+'\n'+fence+'\n'
