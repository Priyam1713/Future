"""Exact eligible matched losses; descriptive calibration, no skill certification."""
import copy
from decimal import Decimal,localcontext,ROUND_HALF_EVEN
from fractions import Fraction as F
from .common import LabError,checked,rational,digest
def mean(values):
    total=F(0)
    for value in values:total=checked(total+value)
    return checked(total/len(values)) if values else None
def number(value,sqrt=False):
    if value is None:return dict(status='not_estimable',exact=None,decimal=None)
    with localcontext() as ctx:
        ctx.prec=80;ctx.rounding=ROUND_HALF_EVEN
        x=Decimal(value.numerator)/Decimal(value.denominator)
        if sqrt:x=x.sqrt()
        text=format(x.quantize(Decimal('0.000000000001')),'f') if x.adjusted()<=65 else None
    return dict(status='finite',exact='sqrt('+str(value)+')' if sqrt else str(value),decimal=text)
def scores(predictions,outcomes,kind):
    if len(predictions)!=len(outcomes):raise LabError('Matched score lengths required')
    ps=[rational(x) for x in predictions];ys=[rational(x) for x in outcomes];errors=[checked(p-y) for p,y in zip(ps,ys)];squares=[checked(x*x) for x in errors]
    if kind=='binary':
        if any(not 0<=p<=1 for p in ps) or any(y not in (0,1) for y in ys):raise LabError('Binary scoring requires probabilities and0/1outcomes')
        bins=[]
        for i in range(10):
            selected=[(p,y) for p,y in zip(ps,ys) if min(9,(10*p).numerator//(10*p).denominator)==i]
            bins.append(dict(index=i,count=len(selected),mean_probability=str(mean([p for p,y in selected])) if selected else None,observed_frequency=str(mean([y for p,y in selected])) if selected else None))
        brier=mean(squares)
        return dict(count=len(ps),brier=number(brier),two_category_brier=number(checked(2*brier) if brier is not None else None),calibration=bins)
    if kind!='numeric':raise LabError('Unsupported score kind')
    return dict(count=len(ps),mae=number(mean([abs(x) for x in errors])),mse=number(mean(squares)),rmse=number(mean(squares),True),bias=number(mean(errors)))
def evaluate(ledger):
    from .experiments import replay
    state=replay(ledger);p=ledger['plan'];forecast=state['forecast'];outcomes=state['outcomes'];cases=[];mp=[];bp=[];ys=[];ids=[]
    for t in sorted(p['targets'],key=lambda x:x['id']):
        tid=t['id'];o=outcomes.get(tid);pred=None if forecast is None else forecast['predictions'][tid];base=None if forecast is None else forecast['baseline_predictions'][tid];reason=[]
        if o is None:reason.append('outcome_not_recorded')
        elif o['status']!='resolved':reason.append('outcome_'+o['status'])
        if pred is None:reason.append('forecast_missing')
        if base is None:reason.append('baseline_missing')
        eligible=not reason
        if eligible:mp.append(pred);bp.append(base);ys.append(o['value']);ids.append(tid)
        cases.append(dict(target_id=tid,event_id=t['event_id'],dependency_group=t['dependency_group'],target_at=t['target_at'],prediction=pred,baseline=base,outcome=None if o is None else o['value'],outcome_status='unrecorded' if o is None else o['status'],outcome_record=copy.deepcopy(o),eligible=eligible,exclusion_reasons=reason))
    kind='numeric' if p['technique_id']==49 else 'binary';model=scores(mp,ys,kind);baseline=scores(bp,ys,kind);metric=p['metric'];difference=None;direction='Negative matched loss difference favors model; synthetic differences are not empirical skill.'
    if metric in ['brier','two_category_brier','mae'] and ids:difference=str(checked(F(model[metric]['exact'])-F(baseline[metric]['exact'])))
    elif metric=='rmse' and ids:difference='sqrt('+model['mse']['exact']+')-sqrt('+baseline['mse']['exact']+')'
    if metric in ['bias','calibration']:direction='Diagnostic only; no scalar superiority ordering.'
    r=dict(schema_version=1,experiment_id=p['id'],experiment_version=p['version'],mode=p['mode'],visibly_synthetic=p['mode']=='synthetic',technique_id=p['technique_id'],registry_sha256=p['registry_sha256'],profile_identifiers=p['profile_identifiers'],plan_sha256=ledger['plan_sha256'],ledger_sha256=digest(ledger),forecast_output_sha256=None if forecast is None else forecast['native_output_sha256'],metric=metric,target_definition=p['target_definition'],target_unit=p['target_unit'],dataset=copy.deepcopy(p['dataset']),selection=copy.deepcopy(p['selection']),splits=copy.deepcopy(p['splits']),cases=cases,coverage=dict(planned=len(cases),matched=len(ids),matched_target_ids=ids,missing_outcomes=sum(x['outcome_status'] in ['missing','unrecorded'] for x in cases),excluded_outcomes=sum(x['outcome_status']=='excluded' for x in cases),missing_forecasts=sum(x['prediction'] is None for x in cases),missing_baselines=sum(x['baseline'] is None for x in cases),unique_matched_events=len({x['event_id'] for x in cases if x['eligible']}),matched_dependency_groups=len({x['dependency_group'] for x in cases if x['eligible']})),model=model,baseline=baseline,comparison=dict(status='estimable' if ids and metric not in ['bias','calibration'] else 'not_estimable',model_minus_baseline=difference,direction=direction,matched_only=True),uncertainty=dict(independence_certified=False,effective_sample_size=None,confidence_interval=None,note='Descriptive counts and calibration only. Shared events, horizons and groups can be dependent.'),source_vintage_certified=False,empirical_skill_certified=False,independent_held_out_superiority_certified=False,limitations=['Rights,clocks,availability andtargetdefinitions aredeclared; semantic leakage andexternaltruth arenotcertified.','No tuning or selection using newly recorded test outcomes.','One immutable forecast and one outcome record pertarget/version; corrections require an explicitnewversion.'])
    r.update(cutoff=p['cutoff'],created_at=p['created_at'],forecast_execution_provenance=None if forecast is None else forecast['execution_provenance'])
    r['report_sha256']=digest(r);return r
def compare(reports):
    if not isinstance(reports,list) or len(reports)<2:raise LabError('At least two research reports required')
    first=reports[0]
    for r in reports:
        required=['report_sha256','technique_id','target_definition','target_unit','metric','mode','dataset','cases','cutoff']
        if not isinstance(r,dict) or any(k not in r for k in required):raise LabError('Only eligible Lab research reports can be compared; native symbolic outputs are not forecast reports')
        body=copy.deepcopy(r);sha=body.pop('report_sha256',None)
        if digest(body)!=sha:raise LabError('Research report hash mismatch')
        if any(r[k]!=first[k] for k in ['target_definition','target_unit','metric','mode','dataset','cutoff']):raise LabError('Incompatible targets,units,metrics,datasets,cutoffs orprotocol modes')
        if r['technique_id'] not in [49,51,57] or (r['technique_id']==49)!=(first['technique_id']==49):raise LabError('Unsupported cross-technique comparison')
    common=set.intersection(*[{c['target_id'] for c in r['cases'] if c['eligible']} for r in reports]);rows=[]
    for r in reports:
        selected=sorted([c for c in r['cases'] if c['target_id'] in common],key=lambda x:x['target_id']);reference={c['target_id']:c for c in first['cases']}
        if any(any(c[k]!=reference[c['target_id']][k] for k in ['event_id','dependency_group','outcome','target_at']) for c in selected):raise LabError('Matched outcome/event identities disagree')
        rows.append(dict(report_sha256=r['report_sha256'],technique_id=r['technique_id'],scores=scores([c['prediction'] for c in selected],[c['outcome'] for c in selected],'numeric' if r['technique_id']==49 else 'binary')))
    return dict(status='estimable' if common else 'not_estimable',matched_target_ids=sorted(common),matched_count=len(common),models=rows,empirical_superiority_certified=False,limits='Compatible targets and exact matched scores do not establish independent held-out superiority.')
def markdown(report):
    import json,re
    body=json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False);fence='`'*max(3,max([len(x) for x in re.findall(r'`+',body)]+[0])+1)
    payload=report.get('result',report);synthetic=bool(report.get('visibly_synthetic'))
    if isinstance(payload,dict):synthetic=synthetic or payload.get('visibly_synthetic') is True or payload.get('mode')=='synthetic' or isinstance(payload.get('plan'),dict) and payload['plan'].get('mode')=='synthetic'
    label='**SYNTHETIC DEMONSTRATION — no empirical skill claim.**' if synthetic else '**User-declared research or native procedural output — no empirical skill certification.**'
    return '# Future Lab research report\n\n'+label+'\n\n'+fence+'json\n'+body+'\n'+fence+'\n'
