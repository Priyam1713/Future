"""Offline five-choice trial records. No hidden-information or prediction mechanism.

All chronology, identity, permissions and entropy origins are declarations. Retain an
independent commitment anchor and transfer only the intended public packet files.
"""
import base64
import copy
from datetime import datetime
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import re
import secrets
import struct
import zlib

from .scrying import load_input, freeze

ROOT=Path(__file__).resolve().parents[1]
PROFILE='rv-air1995-five-choice-blind-trial-v1'
PROFILE_HASH='bb08a51d84d03ad858d65c1530fd763de8bbee686488ce512e54154877d2a60b'
ALIASES=['c1','c2','c3','c4','c5']
TERMINAL=['aborted','invalid','leaked','excluded','conflicted']
LIMITS=[
    'Procedural file validation is not evidence of extrasensory perception or prediction.',
    'File owner can rewrite all history; retain an independently held commitment anchor.',
    'Clocks, identities, rights, knowledge and operational separation are declarations.',
    'Packet allowlists cannot establish absence of semantic clues, collusion or prior knowledge.',
    'No independently witnessed status or inferential p-value is certified.'
]


def canonical(v):
    return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')


def digest(v):return hashlib.sha256(canonical(v)).hexdigest()
def bytes_hash(b):return hashlib.sha256(b).hexdigest()


def assets():
    p=load_input(ROOT/'knowledge/remote_viewing_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned protocol integrity mismatch')
    s=load_input(ROOT/'knowledge/remote_viewing_sources.json')
    f=load_input(ROOT/'knowledge/remote_viewing_source_freeze_v1.json')
    if digest(s)!=p['source_manifest_sha256'] or digest(f)!=p['source_freeze_sha256']:
        raise ValueError('Pinned source integrity mismatch')
    return p,s


DATA=freeze(assets()[0])


def obj(v,fields,optional=()):
    if not isinstance(v,dict) or set(v)-set(fields)-set(optional) or set(fields)-set(v):
        raise ValueError('Missing or unsupported object fields')


def text(v,limit=20000):
    if not isinstance(v,str) or len(v)>limit or any(ord(c)<32 and c not in '\r\n\t' for c in v):
        raise ValueError('Bounded UTF8 text required')
    try:v.encode('utf-8')
    except UnicodeError:raise ValueError('Bounded UTF8 text required') from None
    return v


def identifier(v):
    if not isinstance(v,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}',v):
        raise ValueError('Opaque bounded ASCII identifier required')
    return v


def integer(v,low,high):
    if type(v) is not int or not low<=v<=high:raise ValueError('Exact bounded integer required')
    return v


def timestamp(v):
    if not isinstance(v,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:[0-5]\d)',v):
        raise ValueError('Timezone-aware timestamp with seconds required')
    try:return datetime.fromisoformat(v.replace('Z','+00:00'))
    except ValueError:raise ValueError('Invalid timestamp') from None


def hexhash(v):
    if not isinstance(v,str) or re.fullmatch(r'[0-9a-f]{64}',v) is None:raise ValueError('Lowercase SHA256 required')
    return v


def file_bytes(root,ref):
    if not isinstance(ref,str) or '\\' in ref or ':' in ref or not ref or len(ref)>240:
        raise ValueError('Relative package path required')
    path=PurePosixPath(ref)
    if path.is_absolute() or '..' in path.parts or path.as_posix()!=ref:
        raise ValueError('Relative package path required')
    base=Path(root).resolve();target=(base/ref).resolve()
    if not target.is_relative_to(base) or not target.is_file():raise ValueError('Asset unavailable within package root')
    if target.stat().st_size>4000000:raise ValueError('Asset exceeds supported byte bound')
    return target.read_bytes()


def png(b):
    """Conservative metadata-free RGB subset. Reject instead of claiming sanitization."""
    if not isinstance(b,bytes) or not b.startswith(b'\x89PNG\r\n\x1a\n') or len(b)>4000000:
        raise ValueError('Supported metadata-free PNG required')
    pos=8;chunks=[]
    while pos<len(b):
        if pos+12>len(b):raise ValueError('Invalid PNG framing')
        n=struct.unpack('>I',b[pos:pos+4])[0];kind=b[pos+4:pos+8]
        if n>4000000 or pos+12+n>len(b):raise ValueError('Invalid PNG framing')
        data=b[pos+8:pos+8+n];crc=struct.unpack('>I',b[pos+8+n:pos+12+n])[0]
        if zlib.crc32(kind+data)&0xffffffff!=crc:raise ValueError('PNG CRC mismatch')
        chunks.append((kind,data));pos+=12+n
    if [k for k,_ in chunks]!=[b'IHDR',b'IDAT',b'IEND'] or chunks[-1][1]:
        raise ValueError('PNG metadata or unsupported chunks rejected')
    if len(chunks[0][1])!=13:raise ValueError('Invalid PNG header')
    width,height,depth,color,compression,filtering,interlace=struct.unpack('>IIBBBBB',chunks[0][1])
    if not 1<=width<=1024 or not 1<=height<=1024 or (depth,color,compression,filtering,interlace)!=(8,2,0,0,0):
        raise ValueError('PNG requires bounded noninterlaced 8bit RGB')
    expected=height*(1+3*width)
    try:
        decoder=zlib.decompressobj();pixels=decoder.decompress(chunks[1][1],expected+1)
    except zlib.error:raise ValueError('Invalid PNG compression') from None
    if len(pixels)!=expected or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ValueError('Invalid PNG decoded size or trailing stream')
    if any(pixels[y*(1+3*width)]!=0 for y in range(height)):
        raise ValueError('Only metadata-free filter0 PNG supported')
    return width,height


def check_asset(a,root):
    obj(a,DATA['candidate_fields']);identifier(a['id']);hexhash(a['sha256'])
    if not text(a['provenance'],4000).strip():raise ValueError('Asset provenance required')
    r=a['rights'];obj(r,DATA['rights_fields'])
    if r['basis'] not in ('user_owned','permission','public_domain','license'):raise ValueError('Explicit supported rights basis required')
    for k in ('holder','permission','attribution'):
        if not text(r[k],4000).strip():raise ValueError('Asset rights declaration required')
    b=file_bytes(root,a['path'])
    if bytes_hash(b)!=a['sha256']:raise ValueError('Asset digest mismatch')
    return png(b)


def validate_plan(p,root):
    obj(p,DATA['plan_fields'])
    if type(p['schema_version']) is not int or p['schema_version']!=1 or p['profile']!=PROFILE or p['profile_sha256']!=PROFILE_HASH:
        raise ValueError('Exact protocol/version/hash required')
    for k in ('experiment_id','trial_id','tasker','viewer'):identifier(p[k])
    ids=p['trial_ids']
    if not isinstance(ids,list) or not 1<=len(ids)<=1000:raise ValueError('Fixed bounded trial ledger required')
    for x in ids:identifier(x)
    if len(set(ids))!=len(ids) or p['trial_id'] not in ids:raise ValueError('Unique planned trial IDs required')
    js=p['judges']
    if not isinstance(js,list) or not 1<=len(js)<=8:raise ValueError('Predeclared judges required')
    for x in js:identifier(x)
    participants=[p['tasker'],p['viewer']]+js
    if p['monitor'] is not None:participants.append(identifier(p['monitor']))
    if len(set(participants))!=len(participants):raise ValueError('Conflicting participant roles')
    if p['origin'] not in ('human','simulated') or p['mode'] not in ('blind_evaluation','training_feedback'):
        raise ValueError('Explicit supported origin and mode required')
    if p['assignment_policy'] not in ('os_uniform','simulated_seed','manual'):
        raise ValueError('Unsupported assignment policy')
    if p['assignment_policy']=='simulated_seed' and p['origin']!='simulated':
        raise ValueError('Predictable assignment is simulated only')
    if p['separation'] not in ('transferred_packets','shared_filesystem'):raise ValueError('Explicit access separation required')
    k=p['knowledge'];obj(k,DATA['knowledge_fields'])
    if k['tasker']!='aware' or k['monitor'] not in ('aware','unaware','absent') or k['viewer'] not in ('aware','unaware') or k['judges'] not in ('aware','unaware'):
        raise ValueError('Unsupported knowledge declaration')
    if (p['monitor'] is None)!=(k['monitor']=='absent'):raise ValueError('Conflicting monitor declaration')
    if p['mode']=='blind_evaluation' and (k['viewer']!='unaware' or k['judges']!='unaware' or k['monitor']=='aware'):
        raise ValueError('Blind evaluation conflicts with participant knowledge')
    order=p['presentation_order']
    if not isinstance(order,list) or any(type(x) is not int for x in order) or sorted(order)!=list(range(5)):
        raise ValueError('Predeclared five-candidate presentation permutation required')
    for key in ('primary_endpoint','tie_policy','stopping_rule','exclusion_rule'):
        if p[key]!=DATA['plan_constants'][key]:raise ValueError('Frozen scoring/stopping/exclusion policy required')
    if p['reuse_policy'] not in ('reject','declare_dependence'):raise ValueError('Explicit reuse policy required')
    timestamp(p['created_at'])
    pool=p['pool'];obj(pool,DATA['pool_fields']);identifier(pool['id']);integer(pool['version'],1,100000)
    candidates=pool['candidates']
    if not isinstance(candidates,list) or len(candidates)!=5:raise ValueError('Exactly five candidates required')
    dimensions=[check_asset(a,root) for a in candidates]
    if len({a['id'] for a in candidates})!=5 or len({a['sha256'] for a in candidates})!=5 or len({a['path'] for a in candidates})!=5:
        raise ValueError('Duplicate candidate IDs,paths or bytes rejected')
    if len(set(dimensions))!=1:raise ValueError('Equal candidate image dimensions required')


def selection(policy,seed=None,target=None,candidates=None):
    if policy=='manual':
        if seed is not None:raise ValueError('Manual human assignment cannot use a deterministic nonce seed')
        if target not in [x['id'] for x in candidates]:raise ValueError('Manual target must belong to frozen pool')
        return dict(policy=policy,index=[x['id'] for x in candidates].index(target)),secrets.token_hex(32)
    if target is not None:raise ValueError('Random assignment cannot accept a chosen target')
    if policy=='os_uniform' and seed is not None:raise ValueError('OS assignment cannot accept a seed')
    if policy=='simulated_seed':
        if not isinstance(seed,str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,128}',seed):raise ValueError('Bounded synthetic seed required')
    draws=[]
    while True:
        d=(hashlib.sha256(seed.encode()+str(len(draws)).encode('ascii')).digest()[0] if policy=='simulated_seed' else secrets.token_bytes(1)[0])
        draws.append(d)
        if d<250:break
        if len(draws)>=1024:raise ValueError('Assignment draw bound exceeded')
    s=dict(policy=policy,draws=draws,index=draws[-1]%5)
    if policy=='simulated_seed':s['seed']=seed
    return s,(hashlib.sha256(seed.encode()+b'nonce').hexdigest() if policy=='simulated_seed' else secrets.token_hex(32))


def check_selection(t):
    s=t['selection'];policy=t['plan']['assignment_policy']
    fields=['policy','index']+([] if policy=='manual' else ['draws'])+(['seed'] if policy=='simulated_seed' else [])
    obj(s,fields)
    if s['policy']!=policy:raise ValueError('Assignment declaration conflict')
    integer(s['index'],0,4);hexhash(t['nonce'])
    if policy!='manual':
        ds=s['draws']
        if not isinstance(ds,list) or not 1<=len(ds)<=1024:raise ValueError('Assignment draw log required')
        for d in ds:integer(d,0,255)
        if any(d<250 for d in ds[:-1]) or ds[-1]>=250 or ds[-1]%5!=s['index']:
            raise ValueError('Invalid unbiased rejection-sampling log')
    if policy=='simulated_seed':
        expected,nonce=selection(policy,s['seed'])
        if s!=expected or t['nonce']!=nonce:raise ValueError('Synthetic assignment replay mismatch')


def preimage(t):
    p=t['plan'];a=p['pool']['candidates'][t['selection']['index']]
    return dict(domain=DATA['commitment_domain'],profile=PROFILE,profile_sha256=PROFILE_HASH,trial_id=p['trial_id'],plan_sha256=t['plan_sha256'],pool_sha256=t['pool_sha256'],target_id=a['id'],asset_sha256=a['sha256'],selection=copy.deepcopy(t['selection']),nonce=t['nonce'])


def create(plan,root=ROOT,seed=None,target_id=None):
    assets();validate_plan(plan,root)
    s,n=selection(plan['assignment_policy'],seed,target_id,plan['pool']['candidates'])
    t=dict(schema_version=1,visibility='private_tasker',plan=copy.deepcopy(plan),plan_sha256=digest(plan),pool_sha256=digest(plan['pool']),selection=s,nonce=n,commitment=None,events=[])
    t['commitment']=digest(preimage(t))
    return t


def lock_digest(t,kind):
    actions=['entry','feedback'] if kind=='viewer' else ['rank']
    records=[e for e in t['events'] if e['accepted'] and e['action'] in actions]
    return digest(dict(domain=DATA['lock_domain'],kind=kind,trial_id=t['plan']['trial_id'],records=records))


def rank_result(ranks,index,order):
    obj(ranks,ALIASES)
    if any(type(x) is not int for x in ranks.values()) or sorted(ranks.values())!=[1,2,3,4,5]:
        raise ValueError('Strict complete rank permutation required;ties rejected')
    integer(index,0,4)
    if not isinstance(order,list) or any(type(x) is not int for x in order) or sorted(order)!=list(range(5)):
        raise ValueError('Invalid candidate display permutation')
    return ranks[ALIASES[order.index(index)]]


def _process(t,ctx,action,actor,at,payload,root):
    identifier(actor);timestamp(at)
    if timestamp(at)<=timestamp(ctx['last_at']):raise ValueError('Event chronology must strictly increase')
    if not isinstance(action,str) or action not in DATA['actions']:raise ValueError('Unsupported action')
    spec=DATA['actions'][action];obj(payload,spec['payload'])
    if ctx['state'] not in spec['from']:raise ValueError('Action prohibited in current state')
    p=t['plan'];who=spec['actor']
    permitted=([p['viewer']]+([p['monitor']] if p['monitor'] else []) if who=='viewer_or_monitor' else p['judges'] if who=='planned_judge' else [p[who]])
    if actor not in permitted:raise ValueError('Unauthorized actor for action')
    if action=='entry':
        text(payload['text'])
        if payload['stage'] is not None and payload['stage'] not in DATA['stages']:raise ValueError('Unsupported CRV documentary stage label')
        ats=payload['attachments']
        if not isinstance(ats,list) or len(ats)>8:raise ValueError('Bounded attachment list required')
        for a in ats:check_asset(a,root)
        if len({a['id'] for a in ats})!=len(ats):raise ValueError('Duplicate attachment IDs')
    elif action=='feedback':
        text(payload['text'])
        if payload['code'] not in ('C','PC','N','CFB','S','silence'):raise ValueError('Unknown historical feedback abbreviation')
        if ctx['state']=='viewer_recording' and p['mode']!='training_feedback':
            raise ValueError('Feedback before viewer lock invalid for blind evaluation')
    elif action=='lock_viewer':
        hexhash(payload['digest'])
        if payload['digest']!=lock_digest(t,'viewer'):raise ValueError('Transcript lock mismatch')
        ctx['viewer_lock']=payload['digest']
    elif action=='rank':
        rank_result(payload['ranks'],0,p['presentation_order']);text(payload['report'])
        if actor in ctx['ranked']:raise ValueError('Judge already submitted locked trial ranking')
        ctx['ranked'].append(actor)
    elif action=='lock_judge':
        if set(ctx['ranked'])!=set(p['judges']):raise ValueError('All predeclared judges must rank before lock')
        hexhash(payload['digest'])
        if payload['digest']!=lock_digest(t,'judge'):raise ValueError('Judge lock mismatch')
        ctx['judge_lock']=payload['digest']
    elif action=='reveal':
        if payload['preimage']!=preimage(t) or digest(payload['preimage'])!=t['commitment']:
            raise ValueError('Commitment opening mismatch')
    elif action=='terminate':
        if payload['status'] not in TERMINAL or not text(payload['reason'],4000).strip():
            raise ValueError('Explicit terminal status and reason required')
    to=spec['to']
    ctx['state']=(payload['status'] if action=='terminate' else ctx['state'] if to=='same' else to)
    ctx['last_at']=at
    return ctx


def _previous(t):
    return t['events'][-1]['sha256'] if t['events'] else digest(dict(plan_sha256=t['plan_sha256'],pool_sha256=t['pool_sha256'],commitment=t['commitment']))


def _event(t,action,actor,at,payload,accepted,error):
    e=dict(seq=len(t['events'])+1,previous=_previous(t),action=action,actor=actor,at=at,payload=copy.deepcopy(payload),accepted=accepted,error=error)
    e['sha256']=digest(dict(domain=DATA['event_domain'],event=e))
    return e


def verify_trial(t,root=ROOT):
    assets();obj(t,DATA['private_trial_fields'])
    if type(t['schema_version']) is not int or t['schema_version']!=1 or t['visibility']!='private_tasker':raise ValueError('Private trial schema required')
    validate_plan(t['plan'],root)
    if t['plan_sha256']!=digest(t['plan']) or t['pool_sha256']!=digest(t['plan']['pool']):raise ValueError('Frozen plan or pool changed')
    check_selection(t)
    if t['commitment']!=digest(preimage(t)):raise ValueError('Assignment commitment mismatch')
    events=t['events']
    if not isinstance(events,list) or len(events)>5000:raise ValueError('Bounded complete event history required')
    ctx=dict(state='planned',last_at=t['plan']['created_at'],viewer_lock=None,judge_lock=None,ranked=[])
    replay=copy.deepcopy(t);replay['events']=[]
    for e in events:
        obj(e,['seq','previous','action','actor','at','payload','accepted','error','sha256'])
        if type(e['seq']) is not int or e['seq']!=len(replay['events'])+1 or type(e['accepted']) is not bool:
            raise ValueError('Event counter or decision conflict')
        candidate=copy.deepcopy(ctx)
        try:
            candidate=_process(replay,candidate,e['action'],e['actor'],e['at'],e['payload'],root)
            accepted=True;error=None
        except ValueError as exc:accepted=False;error=str(exc)
        expected=_event(replay,e['action'],e['actor'],e['at'],e['payload'],accepted,error)
        if e!=expected:raise ValueError('Event hash,decision,lock or history mismatch')
        replay['events'].append(e)
        if accepted:ctx=candidate
    return ctx


def apply(t,action,actor,at,payload,root=ROOT):
    """Rejected actions are returned in the private artifact; persist it even on exit2."""
    ctx=verify_trial(t,root);out=copy.deepcopy(t)
    try:_process(out,copy.deepcopy(ctx),action,actor,at,payload,root);accepted=True;error=None
    except ValueError as exc:accepted=False;error=str(exc)
    out['events'].append(_event(out,action,actor,at,payload,accepted,error))
    verify_trial(out,root)
    return out


def _base_packet(t,visibility):
    return dict(schema_version=1,visibility=visibility,profile=PROFILE,profile_sha256=PROFILE_HASH,cue=t['plan']['trial_id'],origin=t['plan']['origin'])


def viewer_packet(t,root=ROOT):
    ctx=verify_trial(t,root)
    if ctx['state'] not in ('committed','viewer_recording'):raise ValueError('Viewer packet only before transcript lock')
    out=_base_packet(t,'blind_viewer')
    out.update(instructions='Record your own observations without consulting target material. No hidden-information ability is supplied.',stages=list(DATA['stages']),template=dict(text='',stage=None,attachments=[]),commitment=t['commitment'])
    validate_packet(out);return out


def _transcript(t):
    return [copy.deepcopy(e) for e in t['events'] if e['accepted'] and e['action'] in ('entry','feedback')]


def judge_packet(t,judge_id,root=ROOT):
    ctx=verify_trial(t,root)
    if ctx['state'] not in ('viewer_locked','judge_recording') or judge_id not in t['plan']['judges']:
        raise ValueError('Blind judge packet requires viewer lock and planned judge')
    # Separate public transcript schema: no private event chain, actor IDs or source attachment paths.
    transcript=[]
    for e in _transcript(t):
        payload=e['payload'];attachments=[]
        for n,a in enumerate(payload.get('attachments',[])):
            attachments.append(dict(name=f'a{len(transcript)+1}-{n+1}.png',sha256=a['sha256'],bytes_base64=base64.b64encode(file_bytes(root,a['path'])).decode('ascii')))
        transcript.append(dict(at=e['at'],kind=e['action'],text=payload['text'],stage=payload.get('stage'),code=payload.get('code'),attachments=attachments))
    candidates=[]
    for alias,index in zip(ALIASES,t['plan']['presentation_order']):
        a=t['plan']['pool']['candidates'][index]
        candidates.append(dict(alias=alias,name=alias+'.png',sha256=a['sha256'],bytes_base64=base64.b64encode(file_bytes(root,a['path'])).decode('ascii')))
    packet_lock=dict(source_digest=ctx['viewer_lock'],packet_digest=digest(dict(domain=DATA['lock_domain'],kind='public_viewer',trial_id=t['plan']['trial_id'],records=transcript)))
    out=_base_packet(t,'blind_judge');out.update(instructions='Rank all five aliases with strict unique ranks1..5 before reveal;one is closest. Preserve disagreement.',judge_id=judge_id,transcript=transcript,transcript_lock=packet_lock,candidates=candidates)
    validate_packet(out);return out


def _packet_asset(a,attachment=False):
    obj(a,['name','sha256','bytes_base64']+([] if attachment else ['alias']))
    if not isinstance(a['name'],str) or re.fullmatch(r'a\d+-\d+\.png' if attachment else r'c[1-5]\.png',a['name']) is None:
        raise ValueError('Neutral export asset name required')
    if not attachment and (not isinstance(a['alias'],str) or a['alias'] not in ALIASES or a['name']!=a['alias']+'.png'):
        raise ValueError('Conflicting alias filename')
    hexhash(a['sha256'])
    try:b=base64.b64decode(a['bytes_base64'],validate=True)
    except (ValueError,TypeError):raise ValueError('Invalid packet asset bytes') from None
    if bytes_hash(b)!=a['sha256']:raise ValueError('Packet asset digest mismatch')
    png(b);return b


def validate_packet(v):
    kind=v.get('visibility') if isinstance(v,dict) else None
    if kind not in ('blind_viewer','blind_judge'):raise ValueError('Explicit blind packet schema required')
    obj(v,DATA['viewer_packet_fields'] if kind=='blind_viewer' else DATA['judge_packet_fields'])
    if type(v['schema_version']) is not int or v['schema_version']!=1 or v['profile']!=PROFILE or v['profile_sha256']!=PROFILE_HASH:
        raise ValueError('Exact packet protocol required')
    identifier(v['cue'])
    if v['origin'] not in ('human','simulated'):raise ValueError('Explicit packet origin required')
    neutral=('Record your own observations without consulting target material. No hidden-information ability is supplied.' if kind=='blind_viewer' else 'Rank all five aliases with strict unique ranks1..5 before reveal;one is closest. Preserve disagreement.')
    if v['instructions']!=neutral:raise ValueError('Fixed neutral packet instructions required')
    if kind=='blind_viewer':
        if v['stages']!=list(DATA['stages']) or v['template']!=dict(text='',stage=None,attachments=[]):raise ValueError('Blank allowlisted viewer template required')
        hexhash(v['commitment'])
    else:
        identifier(v['judge_id']);obj(v['transcript_lock'],['source_digest','packet_digest'])
        hexhash(v['transcript_lock']['source_digest']);hexhash(v['transcript_lock']['packet_digest'])
        if v['transcript_lock']['packet_digest']!=digest(dict(domain=DATA['lock_domain'],kind='public_viewer',trial_id=v['cue'],records=v['transcript'])):
            raise ValueError('Public transcript digest mismatch')
        cs=v['candidates']
        if not isinstance(cs,list) or len(cs)!=5:raise ValueError('Five exported candidates required')
        dimensions=[png(_packet_asset(a)) for a in cs]
        if [a['alias'] for a in cs]!=ALIASES or len({a['sha256'] for a in cs})!=5 or len(set(dimensions))!=1:
            raise ValueError('Duplicate/missing candidate alias or unequal asset dimensions')
        if not isinstance(v['transcript'],list) or len(v['transcript'])>5000:raise ValueError('Bounded transcript required')
        for e in v['transcript']:
            obj(e,['at','kind','text','stage','code','attachments']);timestamp(e['at']);text(e['text'])
            if e['kind'] not in ('entry','feedback') or e['stage'] not in (None,*DATA['stages']):raise ValueError('Unsupported transcript annotation')
            if e['code'] not in (None,'C','PC','N','CFB','S','silence'):raise ValueError('Unsupported feedback code')
            if not isinstance(e['attachments'],list) or len(e['attachments'])>8:raise ValueError('Bounded transcript attachments required')
            for a in e['attachments']:_packet_asset(a,True)
    return True


def export_packet(packet,directory):
    """Only fresh directory, packet.json and strict neutral PNG names; no source dirs copied."""
    validate_packet(packet)
    target=Path(directory)
    if target.exists():raise ValueError('Packet export requires a new directory')
    files={}
    if packet['visibility']=='blind_judge':
        for a in packet['candidates']:files[a['name']]=_packet_asset(a)
        for e in packet['transcript']:
            for a in e['attachments']:
                if a['name'] in files:raise ValueError('Conflicting attachment export name')
                files[a['name']]=_packet_asset(a,True)
    target.mkdir(parents=True)
    for name,b in files.items():(target/name).write_bytes(b)
    (target/'packet.json').write_bytes(canonical(packet)+b'\n')


def _seal_report(v):
    v['report_sha256']=digest(dict(domain=DATA['report_domain'],report=v));return v


def report(t,root=ROOT):
    ctx=verify_trial(t,root);p=t['plan']
    if ctx['state'] not in ('revealed','reported',*TERMINAL):
        # Never include request/trial replay, plan/pool hashes, raw attempts or tasker data here.
        return _seal_report(dict(schema_version=1,visibility='public_status',profile=PROFILE,profile_sha256=PROFILE_HASH,cue=p['trial_id'],origin=p['origin'],state=ctx['state'],commitment=t['commitment'],limitations=LIMITS))
    revealed=any(e['accepted'] and e['action']=='reveal' for e in t['events'])
    declared=(p['mode']=='blind_evaluation' and p['separation']=='transferred_packets')
    eligible=revealed and ctx['state'] in ('revealed','reported') and declared
    uniform=p['assignment_policy']=='os_uniform'
    ranks=[]
    if revealed:
        for e in t['events']:
            if e['accepted'] and e['action']=='rank':
                r=rank_result(e['payload']['ranks'],t['selection']['index'],p['presentation_order'])
                ranks.append(dict(judge_id=e['actor'],actual_target_rank=r,rank1=r==1,ranks=copy.deepcopy(e['payload']['ranks']),raw_report=e['payload']['report']))
    return _seal_report(dict(schema_version=1,visibility='private_report',profile=PROFILE,profile_sha256=PROFILE_HASH,origin=p['origin'],state=ctx['state'],plan_sha256=t['plan_sha256'],pool_sha256=t['pool_sha256'],commitment=t['commitment'],commitment_verified=True,revealed=revealed,viewer_lock=ctx['viewer_lock'],judge_lock=ctx['judge_lock'],procedurally_validated_from_files=True,declared_participant_blinded=declared,independently_witnessed=False,eligible_blinded_scoring=eligible,randomization=dict(policy=p['assignment_policy'],declared_uniform_os=uniform,entropy_origin_independently_verified=False,chance_qualified=eligible and uniform,synthetic_reference=p['origin']=='simulated'),actual_target_id=preimage(t)['target_id'] if revealed else None,judge_results=ranks,judge_disagreement=len({x['actual_target_rank'] for x in ranks})>1,chance_reference=dict(expected_rank=3,top_rank={'numerator':1,'denominator':5},assumptions='Uniform target selection independent of fixed pre-reveal rankings;not established by file validation',applicable=eligible and uniform),attempts_rejected=sum(not e['accepted'] for e in t['events']),leakage_flags=['training_feedback'] if p['mode']=='training_feedback' else ['shared_filesystem'] if p['separation']=='shared_filesystem' else [],source_attribution=dict(manual='1986stage labels only;optional software fields are editorial',air='1995Utts five-choice ranking reference;Hyman judging/replication concerns',engineering='Future versioned editorial cryptographic/state policies;not historical certification'),rights='Declared permissions required and exact bytes verified;ownership/legal clearance not independently attested.',trial=copy.deepcopy(t),limitations=LIMITS))


def summary(trials,root=ROOT):
    if not isinstance(trials,list) or not 1<=len(trials)<=1000:raise ValueError('Complete bounded trial ledger required')
    contexts=[verify_trial(t,root) for t in trials];plans=[t['plan'] for t in trials];first=plans[0]
    ids=[p['trial_id'] for p in plans]
    if len(set(ids))!=len(ids) or set(ids)!=set(first['trial_ids']):raise ValueError('Full planned trial ledger required;no dropping or duplicate trials')
    # All analysis decisions and judge IDs fixed across this experiment, apart from trial-specific origins/assignments/pools.
    keys=['experiment_id','trial_ids','profile','profile_sha256','judges','primary_endpoint','tie_policy','stopping_rule','exclusion_rule','reuse_policy']
    if any(any(p[k]!=first[k] for k in keys) for p in plans):raise ValueError('Incompatible or posthoc experiment declarations')
    seen=set();dependent=False
    for t in trials:
        # Asset reuse is conservative across the whole candidate set, not just the eventual target.
        hashes={a['sha256'] for a in t['plan']['pool']['candidates']}
        if hashes&seen:
            if first['reuse_policy']=='reject':raise ValueError('Reused candidates violate predeclared no-reuse policy')
            dependent=True
        seen.update(hashes)
    reports=[report(t,root) for t in trials];rows=[];per_judge={j:[] for j in first['judges']}
    for t,ctx,r in zip(trials,contexts,reports):
        jr=r.get('judge_results',[]);eligible=r.get('eligible_blinded_scoring',False)
        rows.append(dict(trial_id=t['plan']['trial_id'],origin=t['plan']['origin'],state=ctx['state'],eligible=eligible,judge_results=jr,rejected_attempts=sum(not e['accepted'] for e in t['events'])))
        if eligible:
            for x in jr:per_judge[x['judge_id']].append(x['actual_target_rank'])
    counts={s:sum(c['state']==s for c in contexts) for s in DATA['states']}
    metrics={j:dict(trials=len(rs),rank1_count=rs.count(1),mean_rank={'numerator':sum(rs),'denominator':len(rs)} if rs else None) for j,rs in per_judge.items()}
    return _seal_report(dict(schema_version=1,visibility='private_summary',profile=PROFILE,profile_sha256=PROFILE_HASH,experiment_id=first['experiment_id'],planned=len(first['trial_ids']),completed=sum(c['state'] in ('revealed','reported') for c in contexts),valid=sum(r.get('eligible_blinded_scoring',False) for r in reports),states=counts,per_trial=rows,per_judge=metrics,declared_dependence=dependent,independence_verified=False,chance_reference=dict(expected_rank=3,top_rank={'numerator':1,'denominator':5},qualification='Reference only under uniform independent target labels and fixed stopping/judging;no inferential p-values. Manual/simulated/training trials not certified uniform human randomization.'),trials=copy.deepcopy(trials),limitations=LIMITS))


def read(value,root=ROOT,registry=None):
    assets()
    if not isinstance(value,dict):raise ValueError('Request object required')
    task=value.get('task')
    if not isinstance(task,str) or task not in DATA['requests']:raise ValueError('Unsupported Remote Viewing task')
    required=['schema_version','profile','task'];optional=list(DATA['requests'][task])
    obj(value,required,optional)
    if type(value['schema_version']) is not int or value['schema_version']!=1 or value['profile']!=PROFILE:
        raise ValueError('Exact Remote Viewing request schema/profile required')
    # Task argument shapes are explicit;no implicit missing-argument repair.
    required_args={'create':['plan'],'apply':['trial','action','actor','at','payload'],'viewer_packet':['trial'],'judge_packet':['trial','judge_id'],'report':['trial'],'summary':['trials'],'validate_packet':['packet']}[task]
    if any(k not in value for k in required_args):raise ValueError('Missing task arguments')
    if registry:
        for s in assets()[1]:registry.add_source(s)
    if task=='create':return dict(visibility='private_tasker',accepted=True,trial=create(value['plan'],root,value.get('seed'),value.get('target_id')))
    if task=='apply':
        t=apply(value['trial'],value['action'],value['actor'],value['at'],value['payload'],root)
        return dict(visibility='private_tasker',accepted=t['events'][-1]['accepted'],error=t['events'][-1]['error'],trial=t)
    if task=='viewer_packet':return viewer_packet(value['trial'],root)
    if task=='judge_packet':return judge_packet(value['trial'],value['judge_id'],root)
    if task=='report':return report(value['trial'],root)
    if task=='summary':return summary(value['trials'],root)
    validate_packet(value['packet']);return dict(visibility='public_validation',packet_validated=True,profile=PROFILE,limitations=LIMITS)


def markdown(result):
    # JSON replay block is exact output only. Blind packets/status NEVER embed private request metadata.
    s=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    fence='`'*max(3,max((len(x) for x in re.findall(r'`+',s)),default=0)+1)
    return '# Remote Viewing procedural record\n\nVisibility: '+html.escape(result['visibility'])+'\n\n'+ '\n'.join('- '+x for x in LIMITS)+'\n\n## Exact replay output\n\n'+fence+'json\n'+s+'\n'+fence+'\n'
