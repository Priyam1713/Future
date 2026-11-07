"""Pre-engine independent information-form oracle and original synthetic cases.

No production imports. Future moments use closed-form powers/convolution, not a filter loop.
"""
import copy
from datetime import datetime,timedelta,timezone
from fractions import Fraction as F
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def stamp(tick):return (datetime(2020,1,1,tzinfo=timezone.utc)+timedelta(seconds=tick)).isoformat().replace('+00:00','Z')
def request(values=(2,2)):
    p=json.loads((R/'knowledge/digital_twin_profile_v1.json').read_text(encoding='utf-8'));snapshot='Original synthetic scalar observations; no real people or devices.'
    return dict(schema_version=1,profile=dict(id=p['id'],sha256=digest(p),catalog_sha256=p['source_manifest_sha256']),mode='synthetic',asset=dict(id='asset-1',state_unit='V',measurement_unit='V',parameter_version='v1'),parameters=dict(version='v1',A='1',B='0',H='1',Q='0',R='1',m0='0',P0='1'),timeline=dict(initial_at=stamp(0),step_seconds=1,evaluation_at=stamp(len(values)+5)),records=[dict(id='r'+str(i),asset_id='asset-1',state_unit='V',measurement_unit='V',tick=i,timestamp=stamp(i),available_at=stamp(i) if z is not None else None,value=str(z) if z is not None else None,control='0') for i,z in enumerate(values,1)],horizon=0,scenarios=[],reference_scenario=None,provenance=dict(source_ref='digital-twin-welch-bishop-2002-v1',rights='self_authored',attribution='Future original scalar fixture',snapshot=snapshot,snapshot_sha256=hashlib.sha256(snapshot.encode()).hexdigest(),archive_checks=dict(source=False,units=False,timestamps=False,rights=False)))

def oracle(q):
    p=q['parameters'];A,B,H,Q,Rn=[F(p[x]) for x in ['A','B','H','Q','R']];mean=F(p['m0']);var=F(p['P0']);open_mean=mean;open_var=var;rows=[];previous=[];origin=q['timeline']['initial_at']
    for record in q['records']:
        u=F(record['control']);prior=A*mean+B*u;prior_var=A*A*var+Q;open_mean=A*open_mean+B*u;open_var=A*A*open_var+Q
        measurement_pred=H*prior;S=H*H*prior_var+Rn
        candidates=[r for r in previous if r['value'] is not None and r['available_at']<=origin];persistence=F(candidates[-1]['value']) if candidates else None
        z=F(record['value']) if record['value'] is not None else None;apply=z is not None and record['available_at']==record['timestamp']
        known=z is not None and record['available_at']<=q['timeline']['evaluation_at']
        if apply and prior_var:
            precision=1/prior_var+H*H/Rn;information=prior/prior_var+H*z/Rn;mean=information/precision;var=1/precision
        else:mean=prior;var=prior_var
        row=dict(prior_mean=str(prior),prior_variance=str(prior_var),predicted_measurement=str(measurement_pred),innovation_variance=str(S),gain=str(prior_var*H/S) if apply else None,innovation=str(z-measurement_pred) if apply else None,posterior_mean=str(mean),posterior_variance=str(var),correction='applied' if apply else 'missing' if z is None else 'not_available_at_update',open_loop_mean=str(open_mean),open_loop_variance=str(open_var),open_loop_measurement=str(H*open_mean),persistence_measurement=str(persistence) if persistence is not None else None,filter_squared_error=str((z-measurement_pred)**2) if known else None,open_loop_squared_error=str((z-H*open_mean)**2) if known else None,persistence_squared_error=str((z-persistence)**2) if known and persistence is not None else None)
        rows.append(row);previous.append(record);origin=record['timestamp']
    branches={}
    for s in q['scenarios']:
        controls=list(map(F,s['controls']));states=[]
        for j in range(q['horizon']+1):
            m=A**j*mean+B*sum((A**(j-i)*controls[i-1] for i in range(1,j+1)),F())
            v=A**(2*j)*var+Q*sum((A**(2*i) for i in range(j)),F())
            states.append(dict(mean=str(m),variance=str(v),measurement_mean=str(H*m),measurement_variance=str(H*H*v+Rn)))
        branches[s['id']]=states
    return dict(rows=rows,final_mean=str(mean),final_variance=str(var),branches=branches)

def cases():
    good={'sequential':request(),'empty':request(()),'missing':request((2,None)),'all-missing':request((None,None)), 'single':request((2,))}
    q=request((2,));q['parameters']['R']='3';good['noisy']=q
    q=request((2,));q['parameters']['H']='2';good['scaled']=q
    q=request((2,));q['parameters']['H']='1/2';q['parameters']['R']='1/100';good['gain-over-one']=q
    q=request();q['parameters']['H']='0';good['unobservable']=q
    q=request();q['parameters']['P0']='0';good['zero-prior']=q
    q=request();q['parameters']['Q']='1';good['process-noise']=q
    q=request((4,));q['parameters'].update(A='1/2',B='1',m0='4',P0='4');q['records'][0]['control']='1';q.update(horizon=1,scenarios=[dict(id='zero',controls=['0']),dict(id='one',controls=['1']),dict(id='same',controls=['0'])],reference_scenario='zero');good['controls']=q
    q=copy.deepcopy(good['controls']);q.update(horizon=0,scenarios=[dict(id='zero',controls=[]),dict(id='same',controls=[])]);good['zero-horizon']=q
    q=copy.deepcopy(good['controls']);q.update(horizon=3,scenarios=[dict(id='zero',controls=['0']*3),dict(id='one',controls=['1','0','-1'])]);good['future-convolution']=q
    q=request((2,2,3));q['records'][0]['available_at']=stamp(2);good['delayed']=q
    q=copy.deepcopy(good['delayed']);q['records'][0]['value']='999';good['delayed-changed']=q
    q=request((2,2));q['records'][1]['available_at']=stamp(20);good['not-yet-known']=q
    q=copy.deepcopy(good['not-yet-known']);q['timeline']['evaluation_at']=stamp(25);good['later-evaluation']=q
    q=request((2,None,3));q['records'][0]['available_at']=stamp(2);good['delayed-persistence']=q
    q=request();q['mode']='archival';q['provenance']['archive_checks']={k:True for k in q['provenance']['archive_checks']};q['provenance']['rights']='permission_granted';good['declared-archival']=q
    q=request();q['provenance']['attribution']='Original Δ example ``` fenced safely';good['unicode']=q
    q=request((1,2,3));q['parameters'].update(A='-1/2',B='-2',H='-3/2',Q='1/4',R='7/5',m0='-1',P0='3/2');q['records'][0]['control']='-2';good['signed-rationals']=q
    bad={}
    def change(name,fn,base='sequential'):
        q=copy.deepcopy(good[base]);fn(q);bad[name]=q
    change('unknown',lambda q:q.update(smoothing=True));change('live',lambda q:q.update(mode='live'));change('privacy',lambda q:q.update(person_id='person'))
    change('profile',lambda q:q['profile'].update(sha256='0'*64));change('schema-bool',lambda q:q.update(schema_version=True))
    change('asset',lambda q:q['records'][0].update(asset_id='other'));change('state-unit',lambda q:q['records'][0].update(state_unit='m'));change('measurement-unit',lambda q:q['records'][0].update(measurement_unit='m'));change('version',lambda q:q['parameters'].update(version='v2'))
    for name,v in [('negative-Q','-1'),('negative-P','-1'),('zero-R','0'),('negative-R','-1'),('float',.5),('bool',True),('zero-den','1/0'),('oversize','1'+'0'*18)]:
        key='Q' if name=='negative-Q' else 'P0' if name=='negative-P' else 'R' if name in ('zero-R','negative-R') else 'A'
        change(name,lambda q,k=key,v=v:q['parameters'].update({k:v}))
    change('off-grid',lambda q:q['records'][0].update(timestamp=stamp(3)));change('tick',lambda q:q['records'][0].update(tick=0));change('duplicate-id',lambda q:q['records'][1].update(id='r1'));change('reverse',lambda q:q['records'].reverse());change('duplicate-row',lambda q:q['records'].append(copy.deepcopy(q['records'][0])))
    change('fractional-time',lambda q:q['timeline'].update(initial_at='2020-01-01T00:00:00.1Z'));change('offset',lambda q:q['timeline'].update(initial_at='2020-01-01T00:00:00+00:00'));change('early-availability',lambda q:q['records'][0].update(available_at=stamp(0)));change('missing-availability',lambda q:q['records'][0].update(available_at=None));change('null-value-time',lambda q:q['records'][0].update(value=None));change('early-evaluation',lambda q:q['timeline'].update(evaluation_at=stamp(1)));change('step-bool',lambda q:q['timeline'].update(step_seconds=True))
    change('source',lambda q:q['provenance'].update(source_ref='unknown'));change('rights',lambda q:q['provenance'].update(rights='unknown'));change('snapshot',lambda q:q['provenance'].update(snapshot='tampered'));change('archival-unchecked',lambda q:q.update(mode='archival'));change('fake-synthetic-checks',lambda q:q['provenance']['archive_checks'].update(source=True))
    change('reference',lambda q:q.update(reference_scenario='missing'),'controls');change('branch-measurement',lambda q:q['scenarios'][0].update(value='2'),'controls');change('branch-length',lambda q:q['scenarios'][0].update(controls=[]),'controls');change('duplicate-scenario',lambda q:q['scenarios'].append(copy.deepcopy(q['scenarios'][0])),'controls');change('no-scenario-horizon',lambda q:q.update(horizon=1));change('horizon-cap',lambda q:q.update(horizon=129),'controls')
    q=request(tuple(None for _ in range(257)));bad['record-cap']=q
    q=request(tuple(None for _ in range(256)));q.update(horizon=128,scenarios=[dict(id='s'+str(i),controls=['0']*128) for i in range(8)],reference_scenario='s0');bad['cell-cap']=q
    q=request(tuple(None for _ in range(100)));q['parameters'].update(A='1/999999999999999989',m0='1',P0='1');bad['bit-growth']=q
    return {**{k:(q,0) for k,q in good.items()},**{k:(q,2) for k,q in bad.items()}}

FAMILIES={'scalar-prediction':['controls'],'measurement-correction':['sequential'],'batch-precision-oracle':['sequential'],'process-variance':['process-noise'],'measurement-variance':['noisy'],'missing-observation':['missing','all-missing'],'zero-prior-variance':['zero-prior'],'scaled-observation':['scaled','gain-over-one'],'unobservable-H-zero':['unobservable'],'invalid-variance':['negative-Q','negative-P','negative-R'],'innovation-singularity-boundary':['zero-R','zero-prior'],'covariance-algebra':['sequential','signed-rationals'],'control-input':['controls'],'timestamp-grid':['off-grid','fractional-time','offset'],'observation-availability':['delayed','not-yet-known','delayed-persistence'],'future-observation-leakage':['delayed','delayed-changed','later-evaluation'],'duplicate-out-of-order':['duplicate-id','reverse','duplicate-row'],'asset-identity-units':['asset','state-unit','measurement-unit','version'],'open-loop-baseline':['sequential'],'last-observation-baseline':['sequential','empty'],'matched-preupdate-scores':['sequential','missing','delayed-persistence'],'scenario-fork-no-future-updates':['controls','future-convolution','branch-measurement'],'identical-scenario-control':['controls','zero-horizon'],'source-rights':['source','rights','snapshot'],'synthetic-live-boundary':['live','privacy','declared-archival','archival-unchecked'],'resource-bit-growth':['cell-cap','record-cap','bit-growth'],'json-markdown-hashes':['unicode','profile']}
def freeze():
    c=cases();expected={name:oracle(q) for name,(q,code) in c.items() if code==0}
    seq=expected['sequential']['rows'];assert [(r['gain'],r['posterior_mean'],r['posterior_variance']) for r in seq]==[('1/2','1','1/2'),('1/3','4/3','1/3')]
    # Independent batch Gaussian precision/information, not any recursion above.
    precision=F(1)+sum([F(1),F(1)]);information=F(0)+sum([F(2),F(2)]);assert precision==3 and information==4 and information/precision==F(seq[-1]['posterior_mean']) and 1/precision==F(seq[-1]['posterior_variance'])
    assert expected['noisy']['final_mean']=='1/2' and expected['scaled']['final_variance']=='1/5'
    assert expected['missing']['final_mean']=='1' and expected['missing']['final_variance']=='1/2'
    assert expected['controls']['final_mean']=='7/2' and expected['controls']['branches']['zero'][1]['mean']=='7/4' and expected['controls']['branches']['one'][1]['mean']=='11/4'
    assert [seq[1][k] for k in ['filter_squared_error','persistence_squared_error','open_loop_squared_error']]==['1','0','4']
    f=dict(version=1,families=FAMILIES,batch_anchor=dict(precision='3',information='4',mean='4/3',variance='1/3'),cases={name:dict(input=q,exit_code=code,expected=expected.get(name)) for name,(q,code) in c.items()})
    path=R/'tests/fixtures/digital-twin-independent-v1.json';path.write_text(json.dumps(f,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    manifest=dict(version=1,profile_sha256=digest(json.loads((R/'knowledge/digital_twin_profile_v1.json').read_text(encoding='utf-8'))),fixture_families=27,accepted=sum(code==0 for _,code in c.values()),rejected=sum(code!=0 for _,code in c.values()),normalized_lf_sha256={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in [path,Path(__file__)]})
    (R/'knowledge/digital_twin_fixture_freeze_v1.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n');print(manifest)
if __name__=='__main__':freeze()
