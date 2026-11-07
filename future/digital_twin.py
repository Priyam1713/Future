"""Bounded exact offline scalar state replay; no live or empirical twin certification."""
import copy
from datetime import timedelta
from fractions import Fraction as Q
import hashlib,json,math,re
from pathlib import Path
from .remote_viewing import digest,obj,identifier,integer,text,timestamp
from .scrying import load_input,freeze

ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='3a16aa2f9855eae8351726f565a616dcefc3a7d1a14db0c9642dadd7df091db4'
BITS=8192
def assets():
    p=load_input(ROOT/'knowledge/digital_twin_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned Digital Twin profile mismatch')
    for file,key in [('digital_twin_sources.json','source_manifest_sha256'),('digital_twin_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/file))!=p[key]:raise ValueError('Pinned source integrity mismatch')
    return p
_PROFILE=assets();SCHEMA_HASH=digest(_PROFILE['schema']);DATA=freeze(_PROFILE)

def bounded(v):
    if abs(v.numerator).bit_length()>BITS or v.denominator.bit_length()>BITS:raise ValueError('Rational integer bit limit exceeded')
    return v
def product(a,b):
    if not a or not b:return 0
    if abs(a)==1:return a*b
    if abs(b)==1:return a*b
    if abs(a).bit_length()+abs(b).bit_length()>BITS:raise ValueError('Rational product bit reservation exceeded')
    return a*b
def mul(a,b):
    a=bounded(Q(a));b=bounded(Q(b));g=math.gcd(abs(a.numerator),b.denominator);h=math.gcd(abs(b.numerator),a.denominator)
    return bounded(Q(product(a.numerator//g,b.numerator//h),product(a.denominator//h,b.denominator//g)))
def add(a,b):
    a=bounded(Q(a));b=bounded(Q(b));g=math.gcd(a.denominator,b.denominator)
    left=product(a.numerator,b.denominator//g);right=product(b.numerator,a.denominator//g)
    if left and right and max(abs(left).bit_length(),abs(right).bit_length())+1>BITS:raise ValueError('Rational addition bit reservation exceeded')
    return bounded(Q(left+right,product(a.denominator,b.denominator//g)))
def sub(a,b):return add(a,-Q(b))
def div(a,b):
    b=bounded(Q(b))
    if not b:raise ValueError('Zero rational divisor')
    return mul(a,Q(b.denominator,b.numerator))
def square(v):return mul(v,v)
def rational(v):
    if not isinstance(v,str) or re.fullmatch(r'-?(?:0|[1-9][0-9]{0,17})(?:/[1-9][0-9]{0,17})?',v) is None:raise ValueError('Exact rational string with at most18 digits required')
    return bounded(Q(v))
def fields(v,name):obj(v,DATA['schema'][name])
def sequence(v,limit):
    if not isinstance(v,list) or len(v)>limit:raise ValueError('Bounded list required')
    return v
def at(v):
    if not isinstance(v,str) or re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',v) is None:raise ValueError('Whole-second UTC Z timestamp required')
    return timestamp(v)
def stamp(v):return v.isoformat().replace('+00:00','Z')
def nonempty(v):
    if not text(v,4000).strip():raise ValueError('Nonempty text required')
    return v

def validate(q):
    fields(q,'root');integer(q['schema_version'],1,1);fields(q['profile'],'profile')
    if q['profile']!=dict(id=DATA['id'],sha256=PROFILE_HASH,catalog_sha256=DATA['source_manifest_sha256']):raise ValueError('Profile identity mismatch')
    if q['mode'] not in ('synthetic','archival'):raise ValueError('Only synthetic or independently reviewed archival replay supported')
    asset=q['asset'];fields(asset,'asset')
    for value in asset.values():identifier(value)
    p=q['parameters'];fields(p,'parameters');identifier(p['version'])
    if p['version']!=asset['parameter_version']:raise ValueError('Parameter version mismatch')
    for key in ('A','B','H','Q','R','m0','P0'):rational(p[key])
    if rational(p['P0'])<0 or rational(p['Q'])<0 or rational(p['R'])<=0:raise ValueError('P0>=0,Q>=0,R>0 required')
    timeline=q['timeline'];fields(timeline,'timeline');initial=at(timeline['initial_at']);evaluation=at(timeline['evaluation_at']);step=integer(timeline['step_seconds'],1,86400)
    rows=sequence(q['records'],256);ids=[]
    for tick,row in enumerate(rows,1):
        fields(row,'record');identifier(row['id']);ids.append(row['id']);integer(row['tick'],tick,tick)
        if (row['asset_id'],row['state_unit'],row['measurement_unit'])!=(asset['id'],asset['state_unit'],asset['measurement_unit']):raise ValueError('Mixed asset or units rejected')
        if at(row['timestamp'])!=initial+timedelta(seconds=tick*step):raise ValueError('Contiguous ordered grid timestamps required')
        rational(row['control'])
        if row['value'] is None:
            if row['available_at'] is not None:raise ValueError('Missing observations require null availability')
        else:
            rational(row['value'])
            if at(row['available_at'])<at(row['timestamp']):raise ValueError('Availability precedes sample')
    if len(set(ids))!=len(ids):raise ValueError('Duplicate observation ID')
    end=initial+timedelta(seconds=len(rows)*step)
    if evaluation<end:raise ValueError('Evaluation cutoff precedes historical end')
    horizon=integer(q['horizon'],0,128);scenarios=sequence(q['scenarios'],8);scenario_ids=[]
    for s in scenarios:
        fields(s,'scenario');identifier(s['id']);scenario_ids.append(s['id']);sequence(s['controls'],128)
        if len(s['controls'])!=horizon:raise ValueError('Scenario control length mismatch')
        for value in s['controls']:rational(value)
    if len(set(scenario_ids))!=len(scenario_ids):raise ValueError('Duplicate scenario ID')
    if scenarios:
        identifier(q['reference_scenario'])
        if q['reference_scenario'] not in scenario_ids:raise ValueError('Unknown reference scenario')
    elif horizon or q['reference_scenario'] is not None:raise ValueError('Absent scenarios require zero horizon and null reference')
    try:end+timedelta(seconds=horizon*step)
    except OverflowError:raise ValueError('Scenario timestamp exceeds supported calendar') from None
    provenance=q['provenance'];fields(provenance,'provenance');fields(provenance['archive_checks'],'archive_checks')
    if any(type(v) is not bool for v in provenance['archive_checks'].values()):raise ValueError('Exact review booleans required')
    required=q['mode']=='archival'
    if any(v!=required for v in provenance['archive_checks'].values()):raise ValueError('Explicit mode-appropriate independent archival review declarations required')
    if provenance['source_ref'] not in [s['id'] for s in load_input(ROOT/'knowledge/digital_twin_sources.json')]:raise ValueError('Unknown source')
    if provenance['rights'] not in ('self_authored','permission_granted','public_domain','cc_by'):raise ValueError('Declared snapshot rights required')
    nonempty(provenance['attribution']);nonempty(provenance['snapshot'])
    if provenance['snapshot_sha256']!=hashlib.sha256(provenance['snapshot'].encode('utf-8')).hexdigest():raise ValueError('Snapshot hash mismatch')
    budget=dict(combined_steps=len(rows)+len(scenarios)*horizon,scalar_cells=48*len(rows)+8*len(scenarios)*(horizon+1)+128,integer_bits=BITS)
    if budget['combined_steps']>2048 or budget['scalar_cells']>20000:raise ValueError('Combined step/scalar-cell budget exceeded')
    return budget

def predict(m,p,A,B,u,Qn):return add(mul(A,m),mul(B,u)),add(mul(square(A),p),Qn)
def score(values):
    if not values:return dict(status='not_estimable',count=0,sum_squared_error=None,mean_squared_error=None)
    total=Q(0)
    for value in values:total=add(total,value)
    return dict(status='finite',count=len(values),sum_squared_error=str(total),mean_squared_error=str(div(total,len(values))))

def read(q,registry=None):
    assets();budget=validate(q);q=copy.deepcopy(q);params=q['parameters'];A,B,H,Qn,Rn=[rational(params[k]) for k in ('A','B','H','Q','R')]
    m=rational(params['m0']);p=rational(params['P0']);om=m;op=p;rows=[];history=[];origin=at(q['timeline']['initial_at']);evaluation=at(q['timeline']['evaluation_at']);step=q['timeline']['step_seconds']
    filter_errors=[];open_errors=[];matched={k:[] for k in ('filter','open_loop','persistence')};eligible_ids=[];matched_ids=[];exclusions=[]
    for record in q['records']:
        # Current observation is not read until both model predictions are committed.
        u=rational(record['control']);prior,pv=predict(m,p,A,B,u,Qn);om,op=predict(om,op,A,B,u,Qn)
        forecast=mul(H,prior);open_forecast=mul(H,om);S=add(mul(square(H),pv),Rn)
        if S<=0:raise ValueError('Innovation covariance must be positive')
        candidates=[r for r in history if r['value'] is not None and at(r['available_at'])<=origin]
        persistence=rational(candidates[-1]['value']) if candidates else None
        z=rational(record['value']) if record['value'] is not None else None
        apply=z is not None and record['available_at']==record['timestamp'];known=z is not None and at(record['available_at'])<=evaluation
        innovation=sub(z,forecast) if apply else None;gain=div(mul(pv,H),S) if apply else None
        m=add(prior,mul(gain,innovation)) if apply else prior;p=mul(sub(1,mul(gain,H)),pv) if apply else pv
        if p<0:raise ValueError('Negative posterior variance')
        fe=square(sub(z,forecast)) if known else None;oe=square(sub(z,open_forecast)) if known else None;pe=square(sub(z,persistence)) if known and persistence is not None else None
        if known:
            eligible_ids.append(record['id']);filter_errors.append(fe);open_errors.append(oe)
            if persistence is not None:
                matched_ids.append(record['id'])
                for key,value in [('filter',fe),('open_loop',oe),('persistence',pe)]:matched[key].append(value)
            else:exclusions.append(dict(id=record['id'],reason='no_previous_available_observation',scope='three_way_matched'))
        else:exclusions.append(dict(id=record['id'],reason='missing' if z is None else 'not_available_at_evaluation',scope='all_scores'))
        rows.append(dict(id=record['id'],tick=record['tick'],forecast_origin=stamp(origin),timestamp=record['timestamp'],available_at=record['available_at'],available_at_update=apply,available_at_evaluation=known,
            value=record['value'],prior_mean=str(prior),prior_variance=str(pv),predicted_measurement=str(forecast),innovation_variance=str(S),innovation=str(innovation) if innovation is not None else None,gain=str(gain) if gain is not None else None,
            posterior_mean=str(m),posterior_variance=str(p),correction='applied' if apply else 'missing' if z is None else 'not_available_at_update',open_loop_mean=str(om),open_loop_variance=str(op),open_loop_measurement=str(open_forecast),persistence_measurement=str(persistence) if persistence is not None else None,
            persistence_source_id=candidates[-1]['id'] if candidates else None,filter_squared_error=str(fe) if fe is not None else None,open_loop_squared_error=str(oe) if oe is not None else None,persistence_squared_error=str(pe) if pe is not None else None))
        history.append(record);origin=at(record['timestamp'])
    committed_keys=('id','tick','timestamp','prior_mean','prior_variance','posterior_mean','posterior_variance','innovation','gain','correction')
    branches=[];fork=dict(timestamp=stamp(origin),mean=str(m),variance=str(p),accepted_history_sha256=digest([{k:r[k] for k in committed_keys} for r in rows]))
    for s in q['scenarios']:
        bm,bp=m,p;trajectory=[]
        for tick in range(q['horizon']+1):
            if tick:bm,bp=predict(bm,bp,A,B,rational(s['controls'][tick-1]),Qn)
            trajectory.append(dict(tick=tick,timestamp=stamp(origin+timedelta(seconds=tick*step)),mean=str(bm),variance=str(bp),measurement_mean=str(mul(H,bm)),measurement_variance=str(add(mul(square(H),bp),Rn))))
        branches.append(dict(id=s['id'],controls_sha256=digest(s['controls']),fork=dict(fork),trajectory=trajectory))
    comparisons=[]
    if branches:
        reference=next(s for s in branches if s['id']==q['reference_scenario'])
        for branch in branches:
            differences=[dict(tick=a['tick'],mean_difference=str(sub(Q(a['mean']),Q(b['mean']))),variance_difference=str(sub(Q(a['variance']),Q(b['variance'])))) for a,b in zip(branch['trajectory'],reference['trajectory'])]
            comparisons.append(dict(scenario=branch['id'],reference=reference['id'],identical_controls=branch['controls_sha256']==reference['controls_sha256'],differences=differences,interpretation='Conditional model differences; not causal effects or a variance of paired random outcomes'))
    sources=load_input(ROOT/'knowledge/digital_twin_sources.json')
    if registry is not None:
        for source in sources:registry.add_source(source)
    report=dict(status='accepted',technique_id=53,schema_version=1,profile=dict(q['profile']),schema_sha256=SCHEMA_HASH,request=q,input_sha256=digest(q),parameters_sha256=digest(params),asset_sha256=digest(q['asset']),model_sha256=digest(dict(profile=PROFILE_HASH,asset=q['asset'],parameters=params,initial_at=q['timeline']['initial_at'],step_seconds=step)),
        source_manifest_sha256=DATA['source_manifest_sha256'],source_freeze_sha256=DATA['source_freeze_sha256'],snapshot_sha256=q['provenance']['snapshot_sha256'],code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),budget=budget,rows=rows,final_posterior=dict(mean=str(m),variance=str(p),timestamp=stamp(origin)),
        evaluation=dict(eligible_target_ids=eligible_ids,filter_all=score(filter_errors),open_loop_all=score(open_errors),matched_target_ids=matched_ids,three_way_matched={k:score(v) for k,v in matched.items()},exclusions=exclusions,meaning='Pre-update measurement-scale squared errors; no latent-state ground truth, posterior-fit score, empirical skill or uncertainty-coverage certification'),
        scenario_fork=fork,scenarios=branches,comparisons=comparisons,sources=sources,scope=dict(mode=q['mode'],synthetic_correctness='Supported bounded numerical replay',archival='Requires independent source, units, timestamp and rights review; declarations are not certification',empirical_accuracy='Not certified without real data and held-out validation',live_synchronization=False,decision_feedback=False,actuator_control=False,complete_real_time_twin_certified=False,covariance='Conditional model variance under declared linear/noise assumptions; not calibrated empirical uncertainty'),limits=list(DATA['unsupported']))
    report['report_sha256']=digest(report);return report

def markdown(report):
    body=json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False);fence='`'*max(3,1+max([len(x) for x in re.findall(r'`+',body)]+[0]))
    return '# Digital Twin — offline scalar replay\n\n'+fence+'json\n'+body+'\n'+fence+'\n'
