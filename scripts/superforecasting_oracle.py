"""Independent pre-production rational oracle and original synthetic inputs.

No imports from Future or the production engine. Expected calculations use odds,
separate category losses and independently enumerated group frequencies.
"""
import copy
from decimal import Decimal,localcontext,ROUND_HALF_EVEN
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def source(name='plan-source',at='2024-12-30T00:00:00Z',snapshot=None):
    text=snapshot or 'Original synthetic software validation evidence: '+name
    return dict(id=name,locator='original:'+name,rights='self_authored',attribution='Original synthetic fixture;no actual participant or geopolitical skill.',snapshot=text,snapshot_sha256=hashlib.sha256(text.encode()).hexdigest(),available_at=at)


def reference_class(outcomes=None):
    outcomes=[1,1,1,0,0,0,0,0,0,0] if outcomes is None else outcomes
    members=[dict(id=f'm{i}',event_id=f'historical-{i}',dependency_group='history',eligibility='included',reason='Eligible under the frozen synthetic rule',status='resolved' if y is not None else 'unresolved',outcome=y,event_at=f'2024-12-{i+1:02}T00:00:00Z',observed_at='2024-12-20T00:00:00Z',source=source(f'member-{i}','2024-12-20T00:00:00Z')) for i,y in enumerate(outcomes)]
    return dict(id='class1',version=1,target_question_id='q1',definition='Original finite synthetic historical switch events',eligibility_rule='All distinct synthetic switch events in the declared historical window',frozen_at='2024-12-30T00:00:00Z',availability_cutoff='2024-12-29T00:00:00Z',comparability='Synthetic demonstration only;no population representativeness claimed.',members=members,source=source('class-source','2024-12-29T00:00:00Z'))


def plan(count=4):
    c=reference_class();qs=[];slots=[]
    for i in range(1,count+1):
        q=dict(id=f'q{i}',version=1,event_id=f'event{i}',dependency_group=f'test{i}',partition='test',text=f'Will synthetic switch {i} enter state 1 in the declared observation window?',event_definition='Binary occurrence recorded by the synthetic switch log',window_start='2025-01-01T00:00:00Z',window_end='2025-01-10T00:00:00Z',cutoff='2025-01-03T00:00:00Z',created_at='2024-12-31T00:00:00Z',locked_at='2024-12-31T00:00:00Z',timezone='UTC',clarity_confirmed=True,resolution=dict(source_ref='original-synthetic-switch-log',positive_rule='First state1 observation within the half-open window',negative_rule='No state1 observation through the complete window',dispute_policy='Disputed questions are excluded pending a sourced correction',void_policy='Incomplete observation logs void the question'),class_id='class1' if i==1 else None,class_sha256=sha(c) if i==1 else None,baseline=dict(kind='constant',probability='1/2',frozen_at='2024-12-31T00:00:00Z',domain='synthetic-switches',horizon='fixed-window',source=source('baseline-source')),reasoning={k:[] if k in ('assumptions','subquestions','evidence_gaps','alternatives') else 'Documentary synthetic reasoning only' for k in ('base_rate_rationale','comparability','assumptions','subquestions','evidence_gaps','alternatives','dependence','disagreement')},source=source('question-source'))
        qs.append(q);slots.append(dict(forecast_id=f'f{i}',question_id=f'q{i}',participant='person1',participant_kind='individual'))
    return dict(study_id='synthetic-study',created_at='2025-01-01T00:00:00Z',evidence_mode='synthetic_software_validation',domain='synthetic-switches',horizon='fixed-window',partition=dict(frozen_at='2024-12-31T00:00:00Z',train_groups=['history'],test_groups=[q['dependency_group'] for q in qs]),questions=qs,classes=[c],slots=slots,provenance=source('study-source'))


def forecast(p=None,index=0,probability='1/5',version=1,parent=None,at='2025-01-01T12:00:00Z'):
    p=plan() if p is None else p;q=p['questions'][index];slot=p['slots'][index]
    return dict(forecast_id=slot['forecast_id'],question_id=q['id'],question_version=1,question_sha256=sha(q),participant=slot['participant'],version=version,parent_sha256=parent,recorded_at=at,knowledge_at=at,probability=probability,mode='manual',reason='Original synthetic judgment' if version==1 else 'Manual synthetic revision',evidence=[],assumptions=['Submitted probability is a synthetic judgment,not measured expertise'],outcome_known=False,bayes=None)


def update(previous,p=None,index=0,ratio='3',evidence_id='evidence1',group='evidence-group1',fact='fact1',at='2025-01-02T00:00:00Z',dependence='first',conditioned_on=None):
    p=plan() if p is None else p
    v=forecast(p,index,str(bayes(Q(previous['probability']),Q(ratio))),previous['version']+1,sha(previous),at)
    v.update(mode='bayes',reason='Explicit synthetic likelihood-ratio update',evidence=[dict(id=evidence_id,dependency_group=group,original_fact_id=fact,statement='An original synthetic observation,not geopolitical evidence',source=source('source-'+evidence_id,at))],bayes=dict(kind='ratio',ratio=ratio,likelihood_h=None,likelihood_not_h=None,dependence=dependence,conditioned_on=conditioned_on or [],independent_given_h=dependence=='independent',independent_given_not_h=dependence=='independent',model_status='user_assumed',measurement_notes='Assumed illustrative likelihood model;not measured evidence',source=source('likelihood-'+evidence_id,at)))
    return v


def resolution(p=None,index=0,outcome=1,status='resolved',version=1,parent=None,at='2025-01-11T00:00:00Z'):
    p=plan() if p is None else p;q=p['questions'][index]
    known='2025-01-05T01:00:00Z' if outcome==1 else q['window_end'];available='2025-01-06T00:00:00Z' if outcome==1 else '2025-01-10T01:00:00Z'
    return dict(question_id=q['id'],question_version=1,question_sha256=sha(q),version=version,parent_sha256=parent,status=status,outcome=outcome if status=='resolved' else None,occurrence_at='2025-01-05T00:00:00Z' if status=='resolved' and outcome==1 else None,window_end=q['window_end'],outcome_known_at=known if status=='resolved' else None,publication_at=available,recorded_at=at,reason='Original synthetic resolution;no real outcome represented',source=source(f'resolution-{index}-{version}',available))


def bayes(p,L):
    if p==1:
        if L==0:raise ValueError('Impossible evidence')
        return Q(1)
    odds=p/(1-p);posterior_odds=odds*L
    return posterior_odds/(1+posterior_odds)


def scores(ps,ys):
    ps=[Q(x) for x in ps];n=len(ps)
    if not n:return dict(binary=None,two_category=None)
    category=[(p-y)**2+((1-p)-(1-y))**2 for p,y in zip(ps,ys)];binary=sum(category,Q(0))/(2*n)
    groups={p:[y for v,y in zip(ps,ys) if v==p] for p in sorted(set(ps))};overall=Q(sum(ys),n)
    rel=sum((Q(len(v),n)*(p-Q(sum(v),len(v)))**2 for p,v in groups.items()),Q(0));res=sum((Q(len(v),n)*(Q(sum(v),len(v))-overall)**2 for v in groups.values()),Q(0));unc=overall*(1-overall)
    assert binary==rel-res+unc
    return dict(binary=str(binary),two_category=str(sum(category,Q(0))/n),reliability=str(rel),resolution=str(res),uncertainty=str(unc))


def build():
    b=[]
    for p in [Q(0),Q(1,1000),Q(1,5),Q(1,2),Q(9,10),Q(1)]:
        for L in [Q(0),Q(1,10),Q(1),Q(3),Q(1000000000000000000000000000000)]:
            try:posterior=str(bayes(p,L));status='finite'
            except ValueError:posterior=None;status='undefined'
            b.append(dict(prior=str(p),ratio=str(L),posterior=posterior,status=status))
    losses=[]
    with localcontext() as ctx:
        ctx.prec=80
        for n in range(11):
            p=Q(n,10)
            for y in (0,1):
                success=p if y else 1-p
                log=None if success==0 else format(-(Decimal(success.numerator)/Decimal(success.denominator)).ln().quantize(Decimal('.000000000001'),rounding=ROUND_HALF_EVEN),'f')
                if log=='-0.000000000000':log='0.000000000000'
                losses.append(dict(p=str(p),y=y,binary=str((p-y)**2),two_category=str(2*(p-y)**2),log_status='positive_infinity' if success==0 else 'finite',log_decimal=log,calibration_bin=min(9,n)))
    a=json.loads(Path('knowledge/superforecasting_resource_audit.json').read_text(encoding='utf-8'))
    return dict(version=1,provenance='Original synthetic independently authored odds/category/group calculations;production engine did not exist at freeze',families={x['id']:x['expected'] for x in a['independent_fixture_plan']},base_rates=[dict(outcomes=ys,k=sum(y for y in ys if y is not None),n=sum(y is not None for y in ys),rate=str(Q(sum(y for y in ys if y is not None),sum(y is not None for y in ys))) if any(y is not None for y in ys) else None) for ys in ([],[None],[0]*5,[1]*5,[1]*3+[0]*7)],bayes=b,losses=losses,paired=dict(ps=['4/5','3/10'],ys=[1,0],expected=scores(['4/5','3/10'],[1,0]),baseline='1/4',improvement='37/200',skill='37/50'),decomposition=dict(ps=['1/5','1/5','4/5','4/5'],ys=[0,1,1,1],expected=scores(['1/5','1/5','4/5','4/5'],[0,1,1,1])),calibration=dict(ps=['1/5','1/5'],ys=[0,1],count=2,mean='1/5',frequency='1/2'),chronology=[dict(id='before-cutoff',recorded_at='2025-01-02T12:00:00Z',eligible=True),dict(id='at-cutoff',recorded_at='2025-01-03T00:00:00Z',eligible=True),dict(id='after-cutoff',recorded_at='2025-01-03T00:00:01Z',eligible=False),dict(id='positive-at-occurrence',recorded_at='2025-01-05T00:00:00Z',eligible=False),dict(id='negative-known-at-window-end',occurrence_at=None,known_at='2025-01-10T00:00:00Z',valid=True)],original_plan=plan(),version_expected=dict(selected_version=2,selected_probability='2/5',retained_versions=3),nonindependent=dict(prior='1/5',first='3/7',naive_duplicate='9/13',second_must_reject=True))

if __name__=='__main__':
    out=build();Path('tests/fixtures/superforecasting_reference_v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(len(out['families']),'families;',len(out['bayes']),'Bayes cases;',len(out['losses']),'loss cases')
