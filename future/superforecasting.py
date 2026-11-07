"""Offline versioned binary forecasting ledger;no empirical skill certification."""
import copy
from decimal import Decimal,localcontext,ROUND_HALF_EVEN
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re
from .remote_viewing import digest,obj,integer,identifier,text,hexhash,timestamp
from .scrying import load_input,freeze

ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='bd6d71ded4dbb2ddc1f60b230c46daff2b735793f6bfe4098899d49bfc6b9933'


def assets():
    p=load_input(ROOT/'knowledge/superforecasting_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned Superforecasting profile mismatch')
    for name,key in [('superforecasting_sources.json','source_manifest_sha256'),('superforecasting_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/name))!=p[key]:raise ValueError('Pinned source integrity mismatch')
    return p


DATA=freeze(assets())


def fields(v,key):obj(v,DATA['schema'][key])


def nonempty(v):
    if not text(v,4000).strip():raise ValueError('Nonempty bounded text required')
    return v


def sequence(v,maximum=1000):
    if not isinstance(v,list) or len(v)>maximum:raise ValueError('Bounded list required')
    return v


def boolean(v):
    if type(v) is not bool:raise ValueError('Exact boolean required')
    return v


def at(v):
    if not isinstance(v,str) or not v.endswith('Z'):raise ValueError('UTC Z timestamp required')
    return timestamp(v)


def rational(v):
    if not isinstance(v,str) or len(v)>128 or re.fullmatch(r'-?(?:0|[1-9][0-9]{0,59})(?:/[1-9][0-9]{0,59}|\.[0-9]{1,60})?',v) is None:raise ValueError('Bounded exact rational string required')
    return Q(v)


def probability(v):
    p=rational(v)
    if not 0<=p<=1:raise ValueError('Probability outside0–1')
    return p


def number(q,reason=None):
    if q is None:return dict(status='not_estimable',exact=None,decimal=None,reason=reason or 'empty_denominator')
    q=Q(q)
    with localcontext() as ctx:
        ctx.prec=80;d=(Decimal(q.numerator)/Decimal(q.denominator)).quantize(Decimal('.000000000001'),rounding=ROUND_HALF_EVEN)
    return dict(status='finite',exact=str(q),decimal=format(d,'f'),reason=None)


def source(v,book=None,not_after=None):
    fields(v,'source');identifier(v['id']);nonempty(v['locator']);nonempty(v['attribution']);nonempty(v['snapshot']);hexhash(v['snapshot_sha256'])
    if v['rights'] not in ('self_authored','public_domain','permission_granted','cc_by'):raise ValueError('Explicit snapshot rights required')
    if hashlib.sha256(v['snapshot'].encode('utf-8')).hexdigest()!=v['snapshot_sha256']:raise ValueError('Snapshot bytes mismatch')
    t=at(v['available_at'])
    if not_after is not None and t>not_after:raise ValueError('Source availability after allowed cutoff')
    if book is not None:
        h=digest(v)
        if v['id'] in book and book[v['id']]!=h:raise ValueError('Source identity rewritten')
        book[v['id']]=h
    return t


def reference_class(c,book=None):
    fields(c,'reference_class');identifier(c['id']);identifier(c['target_question_id']);integer(c['version'],1,1)
    for key in ('definition','eligibility_rule','comparability'):nonempty(c[key])
    frozen=at(c['frozen_at']);cutoff=at(c['availability_cutoff'])
    if cutoff>frozen:raise ValueError('Class availability after freeze')
    source(c['source'],book,cutoff);sequence(c['members'],1000);ids=set();events=set();selected=[]
    eligibility={k:0 for k in ('included','excluded','ambiguous')};statuses={k:0 for k in ('resolved','unresolved','disputed','void')}
    for m in c['members']:
        fields(m,'member')
        for key in ('id','event_id','dependency_group'):identifier(m[key])
        if m['id'] in ids or m['event_id'] in events:raise ValueError('Duplicate historical member/event')
        ids.add(m['id']);events.add(m['event_id']);nonempty(m['reason'])
        if m['eligibility'] not in eligibility or m['status'] not in statuses:raise ValueError('Explicit class member status required')
        eligibility[m['eligibility']]+=1;statuses[m['status']]+=1
        observed=at(m['observed_at'])
        if at(m['event_at'])>observed or observed>cutoff:raise ValueError('Historical observation after allowed availability')
        source(m['source'],book,observed)
        if m['status']=='resolved':integer(m['outcome'],0,1)
        elif m['outcome'] is not None:raise ValueError('Unknown historical outcomes remain null')
        if m['eligibility']=='included' and m['status']=='resolved':selected.append(m)
    n=len(selected);k=sum(m['outcome'] for m in selected)
    return dict(input=copy.deepcopy(c),sha256=digest(c),members=copy.deepcopy(c['members']),included_resolved_ids=[m['id'] for m in selected],numerator=k,denominator=n,base_rate=number(Q(k,n) if n else None),counts=dict(universe=len(c['members']),eligibility=eligibility,statuses=statuses,unique_events=len(events),dependency_groups=len({m['dependency_group'] for m in c['members']})),limits=['Observed frequency is not a guarantee of future probability or population certainty.','Membership,availability andcomparability are declarations;nominal n isnot an independent effective sample size.'])


def question(q,book=None):
    fields(q,'question')
    for key in ('id','event_id','dependency_group'):identifier(q[key])
    integer(q['version'],1,1)
    for key in ('text','event_definition'):nonempty(q[key])
    if q['partition'] not in ('train','test') or q['timezone']!='UTC' or not boolean(q['clarity_confirmed']):raise ValueError('Explicit binary clarity/timezone/partition declaration required')
    start,end,cutoff,created,locked=(at(q[k]) for k in ('window_start','window_end','cutoff','created_at','locked_at'))
    if not start<end or not created<=locked<=cutoff<=end:raise ValueError('Question window/lock/cutoff chronology')
    source(q['source'],book,locked);fields(q['resolution'],'resolution_policy')
    for v in q['resolution'].values():nonempty(v)
    if q['class_id'] is None:
        if q['class_sha256'] is not None:raise ValueError('Class identity pair required')
    else:identifier(q['class_id']);hexhash(q['class_sha256'])
    fields(q['reasoning'],'reasoning')
    for key,v in q['reasoning'].items():
        if key in ('assumptions','subquestions','evidence_gaps','alternatives'):
            sequence(v,20)
            for item in v:nonempty(item)
        else:text(v,4000)
    b=q['baseline']
    if b is not None:
        fields(b,'baseline');probability(b['probability'])
        if b['kind'] not in ('constant','reference_class'):raise ValueError('Precommitted baseline kind')
        for key in ('domain','horizon'):nonempty(b[key])
        source(b['source'],book,at(b['frozen_at']))
    return dict(input=copy.deepcopy(q),sha256=digest(q),binary_clarity='User-confirmed declaration;software cannot prove semantic resolvability.',lead_seconds=int((end-cutoff).total_seconds()),reasoning_probability_generated=False)


def identifiers(v):
    sequence(v,1000)
    for x in v:identifier(x)
    if len(v)!=len(set(v)):raise ValueError('Distinct identifiers required')
    return set(v)


def check_plan(p):
    fields(p,'plan');identifier(p['study_id']);created=at(p['created_at'])
    if p['evidence_mode'] not in ('synthetic_software_validation','user_supplied_unvalidated'):raise ValueError('No empirical skill certification mode')
    for key in ('domain','horizon'):nonempty(p[key])
    book={};source(p['provenance'],book,created);part=p['partition'];fields(part,'partition')
    if at(part['frozen_at'])>created:raise ValueError('Partition frozen after plan')
    train=identifiers(part['train_groups']);test=identifiers(part['test_groups'])
    if train&test:raise ValueError('Train/test dependency overlap')
    sequence(p['questions'],100);sequence(p['classes'],100);sequence(p['slots'],500)
    if not p['questions'] or not p['slots']:raise ValueError('Nonempty question/slot plan required')
    classes={};total=0
    for c in p['classes']:
        summary=reference_class(c,book)
        if c['id'] in classes:raise ValueError('Duplicate class identity')
        if at(c['frozen_at'])>created:raise ValueError('Class frozen after plan')
        if any(m['dependency_group'] not in train for m in c['members']):raise ValueError('Historical group outside training partition')
        classes[c['id']]=summary;total+=len(c['members'])
    if total>5000:raise ValueError('Total class bound')
    questions={};events=set()
    for q in p['questions']:
        question(q,book)
        if q['id'] in questions or q['event_id'] in events:raise ValueError('Duplicate question/event identity')
        if not at(q['locked_at'])<=created<=at(q['cutoff']):raise ValueError('Question not locked before plan/cutoff')
        if q['dependency_group'] not in (train if q['partition']=='train' else test):raise ValueError('Question group partition mismatch')
        if q['class_id'] is not None:
            if q['class_id'] not in classes:raise ValueError('Unknown reference class')
            c=classes[q['class_id']]
            if q['class_sha256']!=c['sha256'] or c['input']['target_question_id']!=q['id']:raise ValueError('Frozen class target/hash mismatch')
        b=q['baseline']
        if b is not None:
            if at(b['frozen_at'])>created or (b['domain'],b['horizon'])!=(p['domain'],p['horizon']):raise ValueError('Baseline freeze/domain/horizon mismatch')
            if b['kind']=='reference_class':
                c=classes.get(q['class_id']);rate=c['base_rate']['exact'] if c else None
                if rate is None or probability(b['probability'])!=Q(rate) or at(c['input']['frozen_at'])>at(b['frozen_at']):raise ValueError('Baseline not exact frozen class rate')
        questions[q['id']]=q;events.add(q['event_id'])
    for c in classes.values():
        if c['input']['target_question_id'] not in questions:raise ValueError('Class target not planned')
        if any(m['event_id'] in events for m in c['members']):raise ValueError('Historical/evaluation event leakage')
    slots={};pairs=set()
    for s in p['slots']:
        fields(s,'slot')
        for key in ('forecast_id','question_id','participant'):identifier(s[key])
        pair=(s['question_id'],s['participant'])
        if s['forecast_id'] in slots or pair in pairs or s['question_id'] not in questions or s['participant_kind'] not in ('individual','team'):raise ValueError('Slot identity/type mismatch')
        slots[s['forecast_id']]=s;pairs.add(pair)
    return dict(questions=questions,classes=classes,slots=slots,sources=book)


def create(plan):
    check_plan(plan)
    return dict(schema_version=1,profile_sha256=PROFILE_HASH,plan=copy.deepcopy(plan),plan_sha256=digest(plan),actions=[])
