"""Bounded Lorenz63 RK4 with explicit initial-pair and refinement diagnostics."""
import copy,hashlib,json,math,re
from fractions import Fraction as F
from pathlib import Path
from .remote_viewing import digest,obj,integer,text
from .scrying import load_input,freeze
ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='9cefe49f10b6a149c86ee527abd16f2932e939364a1088fcc2a3fe5d26750d0f'
def assets():
    p=load_input(ROOT/'knowledge/chaos_theory_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned Lorenz profile mismatch')
    for name,key in [('chaos_theory_sources.json','source_manifest_sha256'),('chaos_theory_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/name))!=p[key]:raise ValueError('Pinned source integrity mismatch')
    return p
DATA=freeze(assets())
def fields(v,k):obj(v,DATA['schema'][k])
def rational(v):
    if not isinstance(v,str) or re.fullmatch(r'-?(?:0|[1-9][0-9]{0,8})(?:/[1-9][0-9]{0,8})?',v) is None:raise ValueError('Bounded rational string required')
    return F(v)
def state(v):
    if not isinstance(v,list) or len(v)!=3:raise ValueError('Exactly three state components required')
    s=[rational(x) for x in v]
    if any(abs(x)>100 for x in s):raise ValueError('Initial state bound exceeded')
    return tuple(map(float,s))
def guard(s):
    if any(not math.isfinite(x) or abs(x)>1000000 for x in s):raise ValueError('Finite numerical stage/state guard exceeded')
    return s
def derivative(s,p):
    guard(s);x,y,z=s;a,r,b=p
    return guard((a*(y-x),x*(r-z)-y,x*y-b*z))
def rk4(s,h,p,with_stages=False):
    k1=derivative(s,p)
    k2=derivative(tuple(s[j]+h*k1[j]/2 for j in range(3)),p)
    k3=derivative(tuple(s[j]+h*k2[j]/2 for j in range(3)),p)
    k4=derivative(tuple(s[j]+h*k3[j] for j in range(3)),p)
    out=guard(tuple(s[j]+(h/6)*(k1[j]+2*k2[j]+2*k3[j]+k4[j]) for j in range(3)))
    return (out,(k1,k2,k3,k4)) if with_stages else out
def distance(a,b):return math.hypot(*(x-y for x,y in zip(a,b)))
def validate(q):
    fields(q,'root');integer(q['schema_version'],1,1);fields(q['profile'],'profile');integer(q['profile']['version'],1,1)
    if q['profile']!=dict(id=DATA['id'],version=1,sha256=PROFILE_HASH,catalog_sha256=DATA['source_manifest_sha256']):raise ValueError('Profile identity mismatch')
    fields(q['parameters'],'parameters');p=[rational(q['parameters'][k]) for k in ('sigma','rho','beta')]
    if any(not 0<x<=cap for x,cap in zip(p,[50,100,20])):raise ValueError('Positive bounded parameters required')
    a=state(q['initial']);b=state(q['perturbed_initial']);i=q['integration'];fields(i,'integration')
    if i['solver']!='classical_rk4':raise ValueError('Only classical_rk4 supported')
    dt=rational(i['dt']);n=integer(i['steps'],0,4096);stride=integer(i['trace_stride'],1,4096)
    if not F(1,100000)<=dt<=F(1,20) or dt*n>50:raise ValueError('Step/time bounds exceeded')
    indices=sorted(set(range(0,n+1,stride))|{n});budget=dict(work=24*n,returned_cells=17*len(indices))
    if any(v>DATA['bounds'][k] for k,v in budget.items()):raise ValueError('Combined resource cap exceeded')
    v=q['provenance'];fields(v,'provenance')
    if v['synthetic'] is not True or v['rights']!='self_authored':raise ValueError('Self-authored synthetic inputs required')
    if v['source_ref'] not in [x['id'] for x in load_input(ROOT/'knowledge/chaos_theory_sources.json')]:raise ValueError('Unknown source')
    for k in ('attribution','snapshot'):
        if not text(v[k],4000).strip():raise ValueError('Nonempty bounded provenance required')
    if v['snapshot_sha256']!=hashlib.sha256(v['snapshot'].encode()).hexdigest():raise ValueError('Snapshot hash mismatch')
    return tuple(map(float,p)),a,b,dt,n,indices,budget
def read(request,registry=None):
    q=copy.deepcopy(request);p,a,b,dt,n,indices,budget=validate(q);h=float(dt);ar=a;br=b;wanted=set(indices);rows=[];maxima=dict(coarse_separation=0.0,refined_separation=0.0,base_refinement_difference=0.0,perturbed_refinement_difference=0.0)
    initial_separation=distance(a,b)
    for step in range(n+1):
        distances=dict(coarse_separation=distance(a,b),refined_separation=distance(ar,br),base_refinement_difference=distance(a,ar),perturbed_refinement_difference=distance(b,br))
        for k,v in distances.items():maxima[k]=max(maxima[k],v)
        if step in wanted:rows.append(dict(time=str(step*dt),coarse_base=list(a),coarse_perturbed=list(b),refined_base=list(ar),refined_perturbed=list(br),**distances))
        if step<n:
            a=rk4(a,h,p);b=rk4(b,h,p)
            ar=rk4(rk4(ar,h/2,p),h/2,p);br=rk4(rk4(br,h/2,p),h/2,p)
    sources=load_input(ROOT/'knowledge/chaos_theory_sources.json')
    if registry is not None:
        for source in sources:registry.add_source(source)
    result=dict(status='accepted',technique_id=59,schema_version=1,profile=q['profile'],request=q,input_sha256=digest(q),model_sha256=digest(dict(parameters=q['parameters'],equations=list(DATA['equations']))),schema_sha256=digest(dict(DATA['schema'])),source_manifest_sha256=DATA['source_manifest_sha256'],source_freeze_sha256=DATA['source_freeze_sha256'],code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),budget=budget,rows=rows,diagnostics=dict(maxima_over_all_aligned_times=maxima,initial_separation=initial_separation,final_refined_amplification=distances['refined_separation']/initial_separation if initial_separation else None,amplification_status='finite_pair_ratio_only' if initial_separation else 'not_estimable_zero_initial_separation',integrated_coarse_steps_per_trajectory=n,integrated_refined_steps_per_trajectory=2*n,aligned_times=n+1,returned_times=len(rows),horizon=str(n*dt),lyapunov_exponent=None,validated_forecast_horizon=None,refinement_is_rigorous_error_bound=False),sources=sources,numerics=dict(DATA['numeric']),empirical_forecast_accuracy_validated=False,limitations=list(DATA['configuration_matrix']['unsupported'])+['Initial-state separation and step-refinement difference are separate diagnostics.','No original Lorenz RK2 replication or long-horizon accuracy certification.','Binary64 integration uses approximate h; displayed times are exact nominal grid values.'])
    result['report_sha256']=digest(result);return result
def markdown(result):
    body=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False);fence='`'*max(3,1+max([len(x) for x in re.findall(r'`+',body)]+[0]))
    return '# Chaos theory — finite Lorenz63 simulation\n\n'+fence+'json\n'+body+'\n'+fence+'\n'
