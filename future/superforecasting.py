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


def posterior(prior,ratio):
    p=probability(prior);L=rational(ratio)
    if L<0:raise ValueError('Negative likelihood ratio')
    denominator=1-p+L*p
    if denominator==0:raise ValueError('Impossible zero-denominator evidence')
    return L*p/denominator


def model_ratio(b):
    fields(b,'bayes')
    if b['kind']=='ratio':
        if b['likelihood_h'] is not None or b['likelihood_not_h'] is not None:raise ValueError('Ratio andconditional inputs are distinct')
        L=rational(b['ratio'])
    elif b['kind']=='conditional_likelihoods':
        if b['ratio'] is not None:raise ValueError('Unexpected explicit ratio')
        h=probability(b['likelihood_h']);nh=probability(b['likelihood_not_h'])
        if nh==0:raise ValueError('Zero complement likelihood;infinite/undefined ratio unsupported')
        L=h/nh
    else:raise ValueError('Explicit likelihood model required')
    if L<0:raise ValueError('Negative likelihood ratio')
    for key in ('independent_given_h','independent_given_not_h'):boolean(b[key])
    identifiers(b['conditioned_on']);nonempty(b['measurement_notes'])
    if b['model_status'] not in ('user_assumed','declared_measured'):raise ValueError('Likelihood provenance declaration required')
    return L


def apply_record(kind,v,state,context,sequence_number):
    p=context['plan'];questions=context['questions'];slots=context['slots'];book=state['sources'];fields(v,'resolution' if kind=='resolve' else 'forecast')
    recorded=at(v['recorded_at'])
    if recorded<at(p['created_at']):raise ValueError('Record before plan creation')
    qid=v['question_id'];identifier(qid)
    if qid not in questions:raise ValueError('Unplanned question')
    q=questions[qid];integer(v['question_version'],1,1)
    if v['question_sha256']!=digest(q):raise ValueError('Question definition hash mismatch')
    integer(v['version'],1,2000);nonempty(v['reason'])
    if kind=='resolve':
        old=state['resolutions'][qid];expected=old[-1]['sha256'] if old else None
        if v['version']!=len(old)+1 or v['parent_sha256']!=expected:raise ValueError('Resolution parent/version mismatch')
        if v['status'] not in ('resolved','unresolved','disputed','void') or v['window_end']!=q['window_end']:raise ValueError('Resolution status/window mismatch')
        available=source(v['source'],book,recorded)
        if at(v['publication_at'])>available:raise ValueError('Publication after declared source availability')
        if v['status']=='resolved':
            integer(v['outcome'],0,1);known=at(v['outcome_known_at'])
            if not known<=available:raise ValueError('Outcome known after resolution evidence availability')
            if v['outcome']==1:
                occurred=at(v['occurrence_at'])
                if not at(q['window_start'])<=occurred<at(q['window_end']) or occurred>known:raise ValueError('Positive occurrence chronology')
            elif v['occurrence_at'] is not None or known<at(q['window_end']):raise ValueError('Negative outcome requires closedwindow andnull occurrence')
            if old and old[-1]['record']['status']=='resolved':raise ValueError('Resolution correction requires intervening dispute/void')
        else:
            if v['outcome'] is not None or v['occurrence_at'] is not None:raise ValueError('Nonresolved outcomes/occurrences remain null')
            if v['outcome_known_at'] is not None and at(v['outcome_known_at'])>available:raise ValueError('Nonresolved knowledge chronology')
        old.append(dict(record=copy.deepcopy(v),sha256=digest(v),action_sequence=sequence_number));return
    fid=v['forecast_id'];identifier(fid)
    if fid not in slots:raise ValueError('Unplanned forecast slot')
    slot=slots[fid]
    if slot['question_id']!=qid or slot['participant']!=v['participant']:raise ValueError('Forecast slot identity mismatch')
    prior=state['forecasts'][fid];expected=prior[-1]['sha256'] if prior else None
    if v['version']!=len(prior)+1 or v['parent_sha256']!=expected:raise ValueError('Forecast parent/version mismatch')
    knowledge=at(v['knowledge_at']);prob=probability(v['probability']);boolean(v['outcome_known'])
    if knowledge>recorded or recorded<at(q['locked_at']):raise ValueError('Forecast knowledge/lock chronology')
    sequence(v['assumptions'],20)
    for note in v['assumptions']:nonempty(note)
    sequence(v['evidence'],10)
    previous_evidence=[item for row in prior for item in row['record']['evidence']]
    ids={x['id'] for x in previous_evidence};facts={x['original_fact_id'] for x in previous_evidence};snapshots={x['source']['snapshot_sha256'] for x in previous_evidence};groups={x['dependency_group'] for x in previous_evidence}
    for item in v['evidence']:
        fields(item,'evidence')
        for key in ('id','dependency_group','original_fact_id'):identifier(item[key])
        nonempty(item['statement'])
        if item['id'] in ids or item['original_fact_id'] in facts:raise ValueError('Duplicate evidence ID orunderlying fact')
        source(item['source'],book,knowledge)
        if item['source']['snapshot_sha256'] in snapshots:raise ValueError('Duplicate evidence snapshot')
        ids.add(item['id']);facts.add(item['original_fact_id']);snapshots.add(item['source']['snapshot_sha256'])
    calculation=None
    if kind=='forecast':
        if v['mode']!='manual' or v['bayes'] is not None:raise ValueError('Manual forecasts require explicit manual mode')
    elif kind=='update':
        if v['mode']!='bayes' or not prior or len(v['evidence'])!=1:raise ValueError('Bayes update requires parent andone new evidence item')
        b=v['bayes'];L=model_ratio(b);source(b['source'],book,knowledge);dep=b['dependence'];history_ids=[x['id'] for x in previous_evidence]
        if not history_ids:
            if dep!='first' or b['conditioned_on'] or b['independent_given_h'] or b['independent_given_not_h']:raise ValueError('First evidence dependence declaration')
        elif dep=='conditional':
            if b['conditioned_on']!=history_ids or b['independent_given_h'] or b['independent_given_not_h']:raise ValueError('Conditional ratio must name complete earlier evidence history')
        elif dep=='independent':
            if b['conditioned_on'] or not b['independent_given_h'] or not b['independent_given_not_h'] or v['evidence'][0]['dependency_group'] in groups:raise ValueError('Independent update requires both conditional independence assumptions anddistinct groups')
        else:raise ValueError('Earlier evidence requires conditional orboth-hypothesis independence declaration')
        before=probability(prior[-1]['record']['probability']);denominator=1-before+L*before
        if denominator==0:raise ValueError('Impossible zero-denominator evidence')
        after=L*before/denominator
        if prob!=after:raise ValueError('Submitted posterior differs from exact Bayes update')
        calculation=dict(prior_sha256=prior[-1]['sha256'],prior=number(before),likelihood_ratio=number(L),posterior=number(after),evidence_id=v['evidence'][0]['id'],dependence=dep,conditioned_on=copy.deepcopy(b['conditioned_on']),model_status=b['model_status'],empirically_validated=False)
    else:raise ValueError('Unsupported action kind')
    prior.append(dict(record=copy.deepcopy(v),sha256=digest(v),action_sequence=sequence_number,calculation=calculation))


def candidate(kind,record,state,context,sequence_number,action_at):
    out=copy.deepcopy(state)
    try:
        if kind not in ('forecast','update','resolve'):raise ValueError('Unsupported action kind')
        if not isinstance(record,dict) or at(record.get('recorded_at'))!=at(action_at):raise ValueError('Record time differs from action time')
        apply_record(kind,record,out,context,sequence_number)
    except ValueError as error:return state,'rejected',str(error)
    return out,'accepted',None


def replay(l):
    fields(l,'ledger');integer(l['schema_version'],1,1)
    if l['profile_sha256']!=PROFILE_HASH or l['plan_sha256']!=digest(l['plan']):raise ValueError('Ledger profile/plan integrity mismatch')
    context=check_plan(l['plan']);context['plan']=l['plan'];state=dict(forecasts={s:[] for s in context['slots']},resolutions={q:[] for q in context['questions']},sources=copy.deepcopy(context['sources']))
    sequence(l['actions'],2000);parent=l['plan_sha256'];last=at(l['plan']['created_at'])
    for i,a in enumerate(l['actions'],1):
        fields(a,'action');integer(a['sequence'],i,i);when=at(a['at'])
        if when<last or a['parent_sha256']!=parent or a['sha256']!=digest({k:v for k,v in a.items() if k!='sha256'}):raise ValueError('Action chronology/hash chain mismatch')
        state,decision,reason=candidate(a['kind'],a['record'],state,context,i,a['at'])
        if (a['decision'],a['reason'])!=(decision,reason):raise ValueError('Action decision replay mismatch')
        last=when;parent=a['sha256']
    state['context']=context
    return state


def append(l,kind,record,attempted_at=None,keep_rejected=False):
    state=replay(l);context=state.pop('context');action_at=attempted_at if attempted_at is not None else record.get('recorded_at') if isinstance(record,dict) else None
    when=at(action_at);last=at(l['actions'][-1]['at'] if l['actions'] else l['plan']['created_at'])
    if when<last or len(l['actions'])>=2000:raise ValueError('Append chronology/bound')
    _,decision,reason=candidate(kind,record,state,context,len(l['actions'])+1,action_at)
    if decision=='rejected' and not keep_rejected:raise ValueError(reason)
    a=dict(sequence=len(l['actions'])+1,kind=kind,at=action_at,record=copy.deepcopy(record),parent_sha256=l['actions'][-1]['sha256'] if l['actions'] else l['plan_sha256'],decision=decision,reason=reason);a['sha256']=digest(a)
    out=copy.deepcopy(l);out['actions'].append(a);replay(out);return out
