"""Verify exact frozen stages, independent local reference and paired diagnostics."""
import copy,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
from future.remote_viewing import digest
from future.scrying import load_input
R=Path(__file__).resolve().parents[1]
def fixture():
    f=load_input(R/'tests/fixtures/chaos-theory-independent-v1.json');fr=load_input(R/'knowledge/chaos_theory_fixture_freeze_v1.json')
    assert digest(f)==fr['fixture_sha256'] and not fr['production_exists']
    assert hashlib.sha256((R/'scripts/chaos_theory_oracle.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==fr['oracle_sha256']
    return f
def vector(v):
    from future.chaos_theory import derivative,rk4
    s=tuple(float(F(x)) for x in v['state']);p=tuple(float(F(x)) for x in v['parameters']);h=float(F(v['dt']));out,stages=rk4(s,h,p,True)
    for actual,expected in [(derivative(s,p),v['derivative']),(out,v['next'])]+list(zip(stages,v['stages'])):
        assert all(abs(F(x)-F(y))<=F(1,10**12) for x,y in zip(actual,expected))
def report(r):
    from future.chaos_theory import distance
    q=r['request'];i=q['integration'];n=i['steps'];dt=F(i['dt']);indices=sorted(set(range(0,n+1,i['trace_stride']))|{n})
    assert [row['time'] for row in r['rows']]==[str(x*dt) for x in indices]
    assert r['budget']==dict(work=24*n,returned_cells=17*len(indices))
    for row in r['rows']:
        pairs=[('coarse_separation','coarse_base','coarse_perturbed'),('refined_separation','refined_base','refined_perturbed'),('base_refinement_difference','coarse_base','refined_base'),('perturbed_refinement_difference','coarse_perturbed','refined_perturbed')]
        for key,a,b in pairs:
            # Independent direct sum/sqrt of squared coordinate differences.
            e=math.sqrt(sum((x-y)**2 for x,y in zip(row[a],row[b])))
            assert math.isclose(row[key],e,rel_tol=1e-14,abs_tol=1e-15)
        assert all(math.isfinite(x) for key in ['coarse_base','coarse_perturbed','refined_base','refined_perturbed'] for x in row[key])
    assert r['diagnostics']['integrated_coarse_steps_per_trajectory']==n and r['diagnostics']['integrated_refined_steps_per_trajectory']==2*n
    assert r['diagnostics']['lyapunov_exponent'] is None and r['diagnostics']['validated_forecast_horizon'] is None and not r['diagnostics']['refinement_is_rigorous_error_bound'] and not r['empirical_forecast_accuracy_validated']
    original=copy.deepcopy(r);sha=original.pop('report_sha256');assert digest(original)==sha
def case(name):
    from future.chaos_theory import read
    c=fixture()['cases'][name];before=copy.deepcopy(c['input'])
    if c['exit_code']:
        try:read(c['input'])
        except (ValueError,TypeError):return
        raise AssertionError('Expected rejection: '+name)
    r=read(c['input']);assert c['input']==before;report(r)
    if name=='origin':assert all(row[k]==[0.0]*3 for row in r['rows'] for k in ['coarse_base','coarse_perturbed','refined_base','refined_perturbed'])
    if name=='equilibrium':assert all(row['coarse_base']==[1.0]*3 and row['coarse_perturbed']==[-1.,-1.,1.] and row['base_refinement_difference']==0 for row in r['rows'])
    if name in ['identical','origin']:assert r['diagnostics']['final_refined_amplification'] is None and all(row['coarse_separation']==row['refined_separation']==0 for row in r['rows'])
    if name=='zero-horizon':assert len(r['rows'])==1 and r['rows'][0]['base_refinement_difference']==0
    if name=='symmetric':
        for row in r['rows']:
            for prefix in ['coarse','refined']:
                x,y,z=row[prefix+'_base'];assert row[prefix+'_perturbed']==[-x,-y,z]
    return r
def local_reference():
    from future.chaos_theory import read
    from scripts.chaos_theory_oracle import taylor
    f=fixture();t=f['taylor'];s=list(map(F,t['state']));p=list(map(F,t['parameters']));time=F(t['time']);a=taylor(s,p,time,80);b=taylor(s,p,time,100)
    assert list(map(str,b))==t['reference'] and str(max(abs(x-y) for x,y in zip(a,b)))==t['order_difference'] and F(t['order_difference'])<F(1,10**60)
    reference=list(map(float,b));errors=[]
    for name in ['short-coarse','short-fine']:
        r=read(f['cases'][name]['input']);errors.append(math.dist(r['rows'][-1]['coarse_base'],reference))
    ratio=errors[0]/errors[1];assert 14<ratio<18,ratio
    # Euler is an intentionally lower-order negative control at the same horizon.
    euler=[1.,1.26,1.-.01*5/3];euler_error=math.dist(euler,reference);assert euler_error>1000*errors[0]
    return dict(errors=errors,observed_refinement_ratio=ratio,euler_negative_control_error=euler_error,taylor_order_difference=t['order_difference'])
def stride_check():
    from future.chaos_theory import read
    q=fixture()['cases']['stride']['input'];a=read(q);q['integration']['trace_stride']=1;b=read(q)
    assert a['rows'][-1]==b['rows'][-1] and a['diagnostics']['maxima_over_all_aligned_times']==b['diagnostics']['maxima_over_all_aligned_times']
def run():
    f=fixture()
    for v in f['numerical_vectors']:vector(v)
    for name in f['cases']:case(name)
    local=local_reference();stride_check()
    families={k:dict(passed=True,cases=[name for name,c in f['cases'].items() if c['family']==k],additional_check=('exact frozen numerical stages' if k in ['derivative','four-stages'] else 'Taylor recurrence and local convergence witness' if k=='independent-taylor' else 'aligned rows,independent distances,integrated counts andreport hashes' if k in ['exact-time-grid','matched-refinement','canonical-replay'] else None)) for k in f['families']}
    assert all(v['cases'] or v['additional_check'] for v in families.values())
    out=dict(passed=True,fixture_families=len(families),families=families,numerical_vectors=len(f['numerical_vectors']),accepted_cases=sum(c['exit_code']==0 for c in f['cases'].values()),rejected_cases=sum(c['exit_code']!=0 for c in f['cases'].values()),local_reference=local,scope='Deterministic synthetic finite Lorenz ODE software verification; no empirical forecast or global Lyapunov validation.')
    (R/'data/chaos-theory-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(str(len(families))+' independent families pass;4 exact stage vectors;Taylor/local convergence andEuler negative control pass')
if __name__=='__main__':run()
