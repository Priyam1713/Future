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


def seconds(delta):
    return Q(delta.days*86400+delta.seconds)+Q(delta.microseconds,1000000)


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
    # Exact fixed-place HALF_EVEN projection also handles very large skill ratios.
    # Logarithms use the separately frozen Decimal80 context.
    whole,remainder=divmod(abs(q.numerator)*10**12,q.denominator)
    if 2*remainder>q.denominator or 2*remainder==q.denominator and whole%2:whole+=1
    digits=str(whole).zfill(13);display=('-' if q<0 and whole else '')+digits[:-12]+'.'+digits[-12:]
    return dict(status='finite',exact=str(q),decimal=display,reason=None)


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
    return dict(input=copy.deepcopy(q),sha256=digest(q),binary_clarity='User-confirmed declaration;software cannot prove semantic resolvability.',lead_seconds=number(seconds(end-cutoff)),reasoning_probability_generated=False)


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


def log_value(p,y):
    success=p if y else 1-p
    if success==0:return None
    with localcontext() as ctx:
        ctx.prec=80
        return -(Decimal(success.numerator)/Decimal(success.denominator)).ln()


def decimal_number(v,expression=None):
    with localcontext() as ctx:
        ctx.prec=80;d=v.quantize(Decimal('.000000000001'),rounding=ROUND_HALF_EVEN)
    if d==0:d=abs(d)
    return dict(status='finite',exact=expression,decimal=format(d,'f'),reason=None)


def log_loss(p,y):
    p=p if isinstance(p,Q) else probability(p);integer(y,0,1)
    if not 0<=p<=1:raise ValueError('Probability outside0–1')
    value=log_value(p,y)
    if value is None:return dict(status='positive_infinity',exact=None,decimal=None,reason='contradicted_certain_forecast')
    success=p if y else 1-p
    return decimal_number(value,'0' if success==1 else '-ln('+str(success)+')')


def eligibility(q,v,history):
    reasons=[];recorded=at(v['recorded_at']);knowledge=at(v['knowledge_at'])
    if recorded>at(q['cutoff']) or knowledge>at(q['cutoff']):reasons.append('after_cutoff')
    if v['outcome_known']:reasons.append('outcome_declared_known')
    boundaries=[at(r['record'][key]) for r in history for key in ('outcome_known_at','occurrence_at') if r['record'][key] is not None]
    if boundaries and (recorded>=min(boundaries) or knowledge>=min(boundaries)):reasons.append('at_or_after_outcome_information')
    return reasons


def aggregate(rows):
    selected=[r for r in rows if r['scored']];n=len(selected)
    ps=[Q(r['probability']['exact']) for r in selected];ys=[r['outcome'] for r in selected];losses=[(p-y)**2 for p,y in zip(ps,ys)]
    mean=sum(losses,Q(0))/n if n else None
    bins=[dict(index=i,lower=str(Q(i,10)),upper=str(Q(i+1,10)),upper_inclusive=i==9,count=0,positive_count=0,mean_probability=number(None),observed_frequency=number(None),unique_events=0,dependency_groups=0) for i in range(10)]
    for i,b in enumerate(bins):
        entries=[(r,p,y) for r,p,y in zip(selected,ps,ys) if min(9,(10*p).numerator//(10*p).denominator)==i]
        if entries:
            count=len(entries);b.update(count=count,positive_count=sum(y for _,_,y in entries),mean_probability=number(sum((p for _,p,_ in entries),Q(0))/count),observed_frequency=number(Q(sum(y for _,_,y in entries),count)),unique_events=len({r['event_id'] for r,_,_ in entries}),dependency_groups=len({r['dependency_group'] for r,_,_ in entries}))
    groups=[];rel=res=unc=None
    if n:
        overall=Q(sum(ys),n);rel=Q(0);res=Q(0);unc=overall*(1-overall)
        for p in sorted(set(ps)):
            outcomes=[y for v,y in zip(ps,ys) if v==p];count=len(outcomes);frequency=Q(sum(outcomes),count);rel+=Q(count,n)*(p-frequency)**2;res+=Q(count,n)*(frequency-overall)**2
            groups.append(dict(probability=number(p),count=count,observed_frequency=number(frequency)))
        if rel-res+unc!=mean:raise ValueError('Exact-category Brier decomposition failed')
    logs=[log_value(p,y) for p,y in zip(ps,ys)];infinite=sum(v is None for v in logs)
    if not n:logmean=number(None)
    elif infinite:logmean=dict(status='positive_infinity',exact=None,decimal=None,reason='at_least_one_contradicted_certain_forecast')
    else:
        with localcontext() as ctx:
            ctx.prec=80;logmean=decimal_number(sum(logs,Decimal(0))/n)
    paired=[r for r in selected if r['baseline_probability'] is not None];paired_model=[Q(r['binary_brier']['exact']) for r in paired];paired_base=[(Q(r['baseline_probability'])-r['outcome'])**2 for r in paired]
    pm=sum(paired_model,Q(0))/len(paired) if paired else None;pb=sum(paired_base,Q(0))/len(paired) if paired else None
    groupmeans={}
    for field in ('event_id','participant'):
        by={}
        for r in selected:by.setdefault(r[field],[]).append(Q(r['binary_brier']['exact']))
        means=[sum(v,Q(0))/len(v) for v in by.values()];groupmeans[field]=dict(mean=number(sum(means,Q(0))/len(means) if means else None),groups=len(by),members=[dict(id=k,slots=len(v),binary_brier=number(sum(v,Q(0))/len(v))) for k,v in by.items()])
    return dict(denominator=n,unique_questions=len({r['question_id'] for r in selected}),unique_events=len({r['event_id'] for r in selected}),dependency_groups=len({r['dependency_group'] for r in selected}),participants=len({r['participant'] for r in selected}),binary_brier=number(mean),two_category_sum_of_squares=number(2*mean if mean is not None else None),natural_log_loss=logmean,infinite_log_losses=infinite,calibration=bins,decomposition=dict(grouping='Exact identical probabilities;separate from coarse calibration bins',groups=groups,reliability=number(rel),resolution=number(res),uncertainty=number(unc),identity_passed=rel-res+unc==mean if n else None),baseline=dict(denominator=len(paired),paired_slot_ids=[r['forecast_id'] for r in paired],excluded_pairs=[dict(forecast_id=r['forecast_id'],reasons=r['exclusion_reasons'] or ['no_precommitted_baseline']) for r in rows if not r['scored'] or r['baseline_probability'] is None],forecast_brier_on_paired=number(pm),baseline_brier=number(pb),absolute_improvement=number(pb-pm if paired else None),relative_skill=number(1-pm/pb if paired and pb>0 else None,'zero_baseline_loss' if paired and pb==0 else 'empty_denominator')),event_average=groupmeans['event_id'],participant_average=groupmeans['participant'],team_aggregation=None)


def evaluate(l):
    state=replay(l);ctx=state['context'];p=l['plan'];rows=[];question_statuses=[]
    for qid,q in ctx['questions'].items():
        history=state['resolutions'][qid];latest=history[-1]['record'] if history else None
        question_statuses.append(dict(question_id=qid,event_id=q['event_id'],partition=q['partition'],status=latest['status'] if latest else 'unresolved',outcome=latest['outcome'] if latest else None,resolution_history=copy.deepcopy(history)))
    for fid,slot in ctx['slots'].items():
        q=ctx['questions'][slot['question_id']];rh=state['resolutions'][q['id']];latest=rh[-1]['record'] if rh else None;history=[];eligible=[]
        for v in state['forecasts'][fid]:
            reasons=eligibility(q,v['record'],rh);history.append(dict(**copy.deepcopy(v),exclusion_reasons=reasons))
            if not reasons:eligible.append(v)
        chosen=eligible[-1] if eligible else None;reasons=[]
        if chosen is None:reasons.append('no_eligible_forecast' if history else 'unsubmitted')
        status=latest['status'] if latest else 'unresolved'
        if status!='resolved':reasons.append(status)
        prob=probability(chosen['record']['probability']) if chosen else None;y=latest['outcome'] if status=='resolved' else None;scored=not reasons
        baseline=q['baseline'];training=None
        if q['class_id'] is not None:
            c=ctx['classes'][q['class_id']]['input'];training=dict(class_id=c['id'],class_sha256=digest(c),availability_cutoff=c['availability_cutoff'],frozen_at=c['frozen_at'],member_event_start=min((m['event_at'] for m in c['members']),key=at,default=None),member_observed_end=max((m['observed_at'] for m in c['members']),key=at,default=None))
        rows.append(dict(forecast_id=fid,question_id=q['id'],event_id=q['event_id'],dependency_group=q['dependency_group'],partition=q['partition'],participant=slot['participant'],participant_kind=slot['participant_kind'],question_sha256=digest(q),cutoff=q['cutoff'],lead_seconds=number(seconds(at(q['window_end'])-at(q['cutoff']))),versions=history,selected_version_sha256=chosen['sha256'] if chosen else None,selected_version=chosen['record']['version'] if chosen else None,probability=number(prob),status=status,outcome=y,scored=scored,primary_included=scored and q['partition']=='test',exclusion_reasons=reasons,binary_brier=number((prob-y)**2 if scored else None,'not_eligible_resolved_pair'),two_category_sum_of_squares=number(2*(prob-y)**2 if scored else None,'not_eligible_resolved_pair'),natural_log_loss=log_loss(prob,y) if scored else number(None,'not_eligible_resolved_pair'),baseline_probability=baseline['probability'] if baseline else None,baseline=copy.deepcopy(baseline),reference_training=training))
    bypart={part:aggregate([r for r in rows if r['partition']==part]) for part in ('train','test')};primary=bypart['test'];status_counts={k:sum(r['status']==k for r in question_statuses) for k in ('resolved','unresolved','disputed','void')}
    return dict(aggregation_policy='Equal forecast-slot weight on latest eligible fixed-cutoff resolved TEST questions;training separately summarized;not daily orquestion-standardized tournament replication',evidence_mode=p['evidence_mode'],empirical_skill_validated=False,questions=question_statuses,reference_classes=list(copy.deepcopy(ctx['classes']).values()),rows=rows,primary=primary,by_partition=bypart,denominators=dict(planned_questions=len(ctx['questions']),planned_events=len({q['event_id'] for q in ctx['questions'].values()}),planned_slots=len(rows),participants=len({s['participant'] for s in ctx['slots'].values()}),versions=sum(len(v) for v in state['forecasts'].values()),actions=len(l['actions']),rejected_attempts=sum(a['decision']=='rejected' for a in l['actions']),selected_slots=sum(r['selected_version'] is not None for r in rows),primary_scored_slots=primary['denominator'],primary_unique_events=primary['unique_events'],primary_dependency_groups=primary['dependency_groups'],question_statuses=status_counts,primary_excluded_slot_ids=[r['forecast_id'] for r in rows if not r['primary_included']]),rejected_attempts=[copy.deepcopy(a) for a in l['actions'] if a['decision']=='rejected'],limits=['Selection/availability,identity,rights,comparability andconditional independence aredeclared,not externallyattested.','Multiple participants/updates share events;counts are not effective independent sample sizes.','Calibration andscores are descriptive;synthetic validation establishes software mechanics,not human superforecasting skill.','Local owners can rewrite all hashes/history;prospective integrity requires independent anchoring.'])


REFERENCES={
    'workflow':dict(source='superforecasting-commandments-v1',locator='Items2–4,6–10',scope='Documentary outside-view,decomposition,updating andfeedback context;not a source-certified prose-to-probability algorithm.'),
    'tournament':dict(source='superforecasting-mellers-author-v1',locator='Methods pp3–4,results,Note1',scope='Historical study context;two-category loss anddaily/question aggregation differ from our fixed-cutoff binary software evaluation.'),
    'scores':dict(source='superforecasting-proper-scores-v1',locator='Sections1and3',scope='Proper scoring rewards translated into explicitly minimized squared-error/natural-log losses;correctness isnot skill validation.'),
    'bayes':dict(source='superforecasting-bayes-v1',locator='Slides10–14,18',scope='Posterior odds=likelihood ratio*prior odds;likelihood models andindependence remain user declarations.')
}


def request(task,payload):
    p=assets();return dict(schema_version=1,profile=dict(id=p['id'],sha256=PROFILE_HASH,catalog_sha256=p['source_manifest_sha256']),task=task,payload=copy.deepcopy(payload))


def read(q,registry=None):
    p=assets();fields(q,'request');integer(q['schema_version'],1,1);fields(q['profile'],'profile')
    if q['profile']!=dict(id=p['id'],sha256=PROFILE_HASH,catalog_sha256=p['source_manifest_sha256']) or q['task'] not in p['tasks']:raise ValueError('Unsupported task/profile/catalog')
    request_hash=digest(q);task=q['task'];v=q['payload'];ledger=None
    if task=='question':result=question(v)
    elif task=='reference-class':result=reference_class(v)
    elif task=='create':ledger=create(v)
    elif task in ('forecast','update','resolve'):
        obj(v,('ledger','record'));ledger=append(v['ledger'],task,v['record'])
    elif task=='attempt':
        obj(v,('ledger','kind','record','attempted_at'));ledger=append(v['ledger'],v['kind'],v['record'],v['attempted_at'],True)
    elif task in ('score','report'):ledger=copy.deepcopy(v)
    else:
        obj(v,('id',))
        if v['id'] not in REFERENCES:raise ValueError('Unknown reference')
        result=copy.deepcopy(REFERENCES[v['id']])
    if ledger is not None:result=dict(ledger=ledger,evaluation=evaluate(ledger))
    sources=load_input(ROOT/'knowledge/superforecasting_sources.json')
    if registry is not None:
        for row in sources:registry.add_source(row)
    out=dict(status='accepted',task=task,profile=copy.deepcopy(q['profile']),request=copy.deepcopy(q),request_sha256=request_hash,source_freeze_sha256=p['source_freeze_sha256'],sources=sources,result=result,code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),limits=['Arithmetic andledger correctness are not demonstrated human expertise,geopolitical skill orhistorical tournament replication.','Book later chapters andGJP file-level rights/completeness remain unverified;no corpus acquired.','Source facts andworkflow context areseparate fromeditorial schema,cutoff,binning andreport conventions.'])
    out['report_sha256']=digest(out);return out


def markdown(r):
    payload=json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False);fence='`'*max(3,max((len(x) for x in re.findall(r'`+',payload)),default=0)+1)
    lines=['# Superforecasting Workbench','','Status: '+r['status'],'']
    if r['status']=='accepted':
        result=r['result']
        if 'evaluation' in result:
            e=result['evaluation'];lines+=['Synthetic software validation or user-supplied unvalidated records;empirical skill validated: false.','', '| Slot | Selected version | Status | Binary Brier |','|---|---|---|---|']+[f"| {x['forecast_id']} | {x['selected_version']} | {x['status']} | {x['binary_brier']['exact']} |" for x in e['rows']]
            lines+=['','Primary binary Brier: '+str(e['primary']['binary_brier']['exact']),'Primary two-category sum: '+str(e['primary']['two_category_sum_of_squares']['exact']),'Natural-log loss status: '+e['primary']['natural_log_loss']['status'],'',*e['limits'],'']
        lines+=r['limits']+['']
    return '\n'.join(lines+[fence+'json',payload,fence,''])
