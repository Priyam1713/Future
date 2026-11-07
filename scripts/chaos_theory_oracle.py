"""Pre-production exact RK4 stages and independent Taylor-series ODE oracle.

No production engine imports. Taylor reference is a convergence witness, not a
rigorous bound on the analytic remainder.
"""
import copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def save(p,x):(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def rhs(s,p):
    x,y,z=s;a,r,b=p
    return [a*(y-x),x*(r-z)-y,x*y-b*z]
def stages(s,h,p):
    k=[rhs(s,p)]
    for weight in [h/2,h/2,h]:k.append(rhs([x+weight*v for x,v in zip(s,k[-1])],p))
    out=[s[j]+h*(k[0][j]+2*k[1][j]+2*k[2][j]+k[3][j])/6 for j in range(3)]
    return dict(stages=[[str(x) for x in row] for row in k],next=[str(x) for x in out])
def taylor(s,p,t,order):
    a,r,b=p;x=[s[0]];y=[s[1]];z=[s[2]]
    for n in range(order):
        x.append(a*(y[n]-x[n])/(n+1))
        y.append((r*x[n]-sum(x[j]*z[n-j] for j in range(n+1))-y[n])/(n+1))
        z.append((sum(x[j]*y[n-j] for j in range(n+1))-b*z[n])/(n+1))
    return [sum(c*t**k for k,c in enumerate(row)) for row in [x,y,z]]
def request():
    p=json.loads((R/'knowledge/chaos_theory_profile_v1.json').read_text(encoding='utf-8'));snapshot='Self-authored synthetic Lorenz63 initial states; no observations.'
    return dict(schema_version=1,profile=dict(id=p['id'],version=1,sha256=digest(p),catalog_sha256=p['source_manifest_sha256']),parameters=dict(sigma='10',rho='28',beta='8/3'),initial=['1','1','1'],perturbed_initial=['1000001/1000000','1','1'],integration=dict(solver='classical_rk4',dt='1/100',steps=1,trace_stride=1),provenance=dict(synthetic=True,source_ref='chaos-theory-ucar-v1',rights='self_authored',attribution='Original synthetic educational fixture',snapshot=snapshot,snapshot_sha256=hashlib.sha256(snapshot.encode()).hexdigest()))
FAMILIES=['derivative','four-stages','exact-one-step','origin-fixed','nonzero-equilibrium','symmetry','zero-perturbation','explicit-perturbation','exact-time-grid','zero-horizon','matched-refinement','independent-taylor','local-convergence','full-integration-stride','finite-state-guard','parameter-bounds','time-bounds','work-caps','strict-schema','unsupported-modes','source-rights','snapshot-binding','canonical-replay']
def build():
    path=R/'tests/fixtures/chaos-theory-independent-v1.json'
    if path.exists():raise ValueError('Immutable fixture exists')
    cases={}
    def add(name,q,code,family,expect=None):cases[name]=dict(input=q,exit_code=code,family=family,expected=expect or {})
    q=request();add('one-step',q,0,'exact-one-step')
    def accepted(name,changes,family):
        q=request()
        for key,v in changes.items():q[key]=v
        add(name,q,0,family)
    accepted('origin',dict(initial=['0']*3,perturbed_initial=['0']*3),'origin-fixed')
    accepted('equilibrium',dict(parameters=dict(sigma='10',rho='2',beta='1'),initial=['1','1','1'],perturbed_initial=['-1','-1','1']),'nonzero-equilibrium')
    accepted('identical',dict(perturbed_initial=['1']*3),'zero-perturbation')
    accepted('zero-horizon',dict(integration=dict(solver='classical_rk4',dt='1/100',steps=0,trace_stride=1)),'zero-horizon')
    accepted('symmetric',dict(perturbed_initial=['-1','-1','1'],integration=dict(solver='classical_rk4',dt='1/100',steps=20,trace_stride=3)),'symmetry')
    accepted('short-coarse',dict(integration=dict(solver='classical_rk4',dt='1/200',steps=2,trace_stride=1)),'local-convergence')
    accepted('short-fine',dict(integration=dict(solver='classical_rk4',dt='1/400',steps=4,trace_stride=1)),'local-convergence')
    accepted('stride',dict(integration=dict(solver='classical_rk4',dt='1/1000',steps=11,trace_stride=4)),'full-integration-stride')
    accepted('tiny-step',dict(integration=dict(solver='classical_rk4',dt='1/100000',steps=10,trace_stride=4096)),'time-bounds')
    accepted('long-sensitive',dict(integration=dict(solver='classical_rk4',dt='1/100',steps=2000,trace_stride=200)),'explicit-perturbation')
    accepted('maximum-steps',dict(integration=dict(solver='classical_rk4',dt='1/1000',steps=4096,trace_stride=4096)),'work-caps')
    def bad(name,section,key,value,family):
        q=request()
        if section:q[section][key]=value
        else:q[key]=value
        add(name,q,2,family)
    for name,section,key,value,family in [
      ('sigma-zero','parameters','sigma','0','parameter-bounds'),('rho-negative','parameters','rho','-1','parameter-bounds'),('beta-too-large','parameters','beta','21','parameter-bounds'),('parameter-float','parameters','sigma',10.0,'strict-schema'),('parameter-bool','parameters','sigma',True,'strict-schema'),('bad-fraction','parameters','beta','1/0','strict-schema'),('nonfinite','parameters','rho','NaN','strict-schema'),('decimal','parameters','rho','28.0','strict-schema'),('huge-number','parameters','sigma','1'*50,'parameter-bounds'),('negative-zero','parameters','beta','-0','parameter-bounds'),('state-size',None,'initial',['1','2'],'strict-schema'),('state-too-large',None,'initial',['101','1','1'],'parameter-bounds'),('missing-perturbation',None,'perturbed_initial',None,'explicit-perturbation'),('dt-zero','integration','dt','0','time-bounds'),('dt-small','integration','dt','1/100001','time-bounds'),('dt-large','integration','dt','1','time-bounds'),('steps-negative','integration','steps',-1,'time-bounds'),('steps-large','integration','steps',4097,'work-caps'),('steps-bool','integration','steps',True,'strict-schema'),('stride-zero','integration','trace_stride',0,'strict-schema'),('solver-rk45','integration','solver','RK45','unsupported-modes'),('solver-lyapunov','integration','solver','lyapunov','unsupported-modes'),('source', 'provenance','source_ref','missing','source-rights'),('rights','provenance','rights','unknown','source-rights'),('not-synthetic','provenance','synthetic',False,'source-rights'),('empty-attribution','provenance','attribution','','source-rights'),('snapshot','provenance','snapshot_sha256','0'*64,'snapshot-binding'),('profile','profile','sha256','0'*64,'canonical-replay'),('catalog','profile','catalog_sha256','0'*64,'canonical-replay'),('version',None,'schema_version',True,'strict-schema'),('extra',None,'rng_seed',1,'unsupported-modes')]:bad(name,section,key,value,family)
    q=request();q['integration'].update(dt='1/20',steps=1001);add('time-product',q,2,'time-bounds')
    q=request();q['parameters'].update(sigma='50',rho='100',beta='20');q['initial']=['100','-100','100'];q['integration'].update(dt='1/20',steps=1000,trace_stride=1000);add('unstable-stage',q,2,'finite-state-guard')
    p=list(map(F,['10','28','8/3']));s=[F(1)]*3;t=F(1,100)
    a=taylor(s,p,t,80);b=taylor(s,p,t,100);difference=max(abs(x-y) for x,y in zip(a,b));assert difference<F(1,10**60)
    vectors=[dict(state=[str(x) for x in v],parameters=[str(x) for x in pp],dt=str(h),derivative=[str(x) for x in rhs(v,pp)],**stages(v,h,pp)) for v,pp,h in [(s,p,t),([F(0)]*3,p,t),([F(1)]*3,[F(10),F(2),F(1)],t),([F(-1),F(-1),F(1)],p,t)]]
    f=dict(version=1,technique_id=59,families=FAMILIES,cases=cases,numerical_vectors=vectors,taylor=dict(order=100,comparison_order=80,time='1/100',state=['1']*3,parameters=['10','28','8/3'],reference=[str(x) for x in b],order_difference=str(difference),limit='High-order local series stability witness; no analytic remainder certification.'))
    save(path.relative_to(R),f);save('knowledge/chaos_theory_fixture_freeze_v1.json',dict(version=1,technique_id=59,fixture_sha256=digest(f),oracle_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),families=FAMILIES,production_exists=(R/'future/chaos_theory.py').exists(),independent_method='ExactFraction four-stage formula and distinct Taylor ODE coefficient recurrence; all fixture inputs fixed before engine.'))
    print(len(cases),'cases',len(FAMILIES),'families; Taylor80/100 difference<1e-60')
if __name__=='__main__':build()
