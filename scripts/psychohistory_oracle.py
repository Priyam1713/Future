"""Independent pre-engine dense Fraction/set oracle and original synthetic inputs.

No production imports. The RNG uses modulo arithmetic instead of production masks.
"""
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def words(seed,count):
    out=[]
    for _ in range(count):
        seed=seed^((seed*8192)%(2**32));seed=seed^(seed//131072);seed=seed^((seed*32)%(2**32));out.append(seed)
    return out
def request(n=3,edges=None,phi='1/2',seeds=None,runs=1,cap=None,trace=True):
    p=json.loads((R/'knowledge/psychohistory_profile_v1.json').read_text(encoding='utf-8'))
    nodes=[str(i).zfill(3) for i in range(n)]
    snapshot='Original synthetic graph; no observed people or causal claims.'
    return dict(schema_version=1,profile=dict(id=p['id'],sha256=digest(p),catalog_sha256=p['source_manifest_sha256']),population=dict(size=n,nodes=nodes),runs=runs,rounds=n if cap is None else cap,trace_states=trace,rng=dict(algorithm='xorshift32-v1',seed=1),scenarios=[dict(id='base',edges=[[nodes[a],nodes[b]] for a,b in (edges if edges is not None else [(i,i+1) for i in range(n-1)])],thresholds=[dict(node=x,phi=phi) for x in nodes],initial=dict(mode='fixed',probability=None,fixed_seeds=[nodes[i] for i in (seeds if seeds is not None else [0])],run_seeds=[],overrides=[]))],reference_scenario='base',provenance=dict(synthetic=True,source_ref='psychohistory-watts-threshold-v1',rights='self_authored',attribution='Future original synthetic fixture',snapshot=snapshot,snapshot_sha256=hashlib.sha256(snapshot.encode()).hexdigest()))
def oracle(q):
    nodes=q['population']['nodes'];n=len(nodes);draws=words(q['rng']['seed'],n*q['runs']);out={}
    for s in q['scenarios']:
        matrix=[[int(sorted([a,b]) in s['edges']) if a!=b else 0 for b in nodes] for a in nodes]
        phi=[F(x['phi']) for x in s['thresholds']];rows=[]
        for run in range(q['runs']):
            init=s['initial'];mode=init['mode']
            if mode=='bernoulli':active={node for i,node in enumerate(nodes) if F(draws[run*n+i],2**32)<F(init['probability'])}
            else:active=set(init['fixed_seeds'] if mode=='fixed' else init['run_seeds'][run])
            for o in init['overrides']:
                if o['state']:active.add(o['node'])
                else:active.discard(o['node'])
            history=[['1' if node in active else '0' for node in nodes]];truncated=False
            for tick in range(q['rounds']+1):
                added=set()
                for i,node in enumerate(nodes):
                    degree=sum(matrix[i]);fraction=F(sum(matrix[i][j] for j,b in enumerate(nodes) if b in active),degree) if degree else None
                    if degree and fraction>=phi[i]:added.add(node)
                following=active|added
                if following==active:break
                if tick==q['rounds']:truncated=True;break
                active=following;history.append(['1' if node in active else '0' for node in nodes])
            states=[[int(x) for x in row] for row in history]
            rows.append(dict(states=states,counts=[sum(row) for row in states],truncated=truncated))
        out[s['id']]=rows
    return out
def stats(values):
    n=len(values);mean=sum(map(F,values),F())/n;var=sum((F(v)-mean)**2 for v in values)/n
    return dict(mean=str(mean),population_variance=str(var),sample_variance=str(var*n/(n-1)) if n>1 else None)

def cases():
    good={}
    good['path']=request()
    q=request(4,[(0,1),(0,2),(0,3)],'2/3');s=copy.deepcopy(q['scenarios'][0]);s['id']='complete';s['edges']=[[str(a).zfill(3),str(b).zfill(3)] for a,b in itertools.combinations(range(4),2)];q['scenarios'].append(s);good['topology']=q
    q=request(2,runs=4);q['scenarios'][0]['initial'].update(mode='explicit_runs',fixed_seeds=[],run_seeds=[[],['001'],['000'],['000','001']]);good['exhaustive']=q
    q=request();s=copy.deepcopy(q['scenarios'][0]);s['id']='higher';s['thresholds']=[dict(node=x,phi='2/3') for x in q['population']['nodes']];q['scenarios'].append(s);good['threshold-comparison']=q
    good['isolated']=request(3,[],phi='0')
    good['zero-threshold']=request(3,phi='0',seeds=[])
    good['zero-seed']=request(3,seeds=[])
    good['all-seed']=request(3,seeds=[0,1,2])
    good['truncated']=request(cap=1)
    good['zero-cap']=request(cap=0)
    good['complete-tie']=request(4,list(itertools.combinations(range(4),2)),phi='1/3')
    good['node-thresholds']=request();good['node-thresholds']['scenarios'][0]['thresholds'][1]['phi']='2/3'
    for name,rho in [('rho-zero','0'),('rho-one','1'),('bernoulli','1/2')]:
        q=request(4,runs=8,trace=False);q['scenarios'][0]['initial'].update(mode='bernoulli',probability=rho,fixed_seeds=[]);good[name]=q
    q=copy.deepcopy(good['bernoulli']);s=copy.deepcopy(q['scenarios'][0]);s['id']='identical';q['scenarios'].append(s);good['identical']=q
    q=copy.deepcopy(good['identical']);q['scenarios'][1]['initial']['probability']='3/4';good['paired-rho']=q
    q=copy.deepcopy(good['paired-rho']);q['scenarios'][1]['initial']['overrides']=[dict(node='000',state=0),dict(node='002',state=1)];good['overrides']=q
    good['singleton']=request(1,[],seeds=[])
    q=copy.deepcopy(good['path']);q['provenance']['attribution']='Original Δ example ``` safely fenced';good['unicode']=q
    # Relabel every node-indexed field; order reverses the physical path identities.
    q=copy.deepcopy(good['node-thresholds']);mapping={'000':'z','001':'b','002':'a'};q['population']['nodes']=sorted(mapping.values())
    for s in q['scenarios']:
        s['edges']=sorted([sorted([mapping[a],mapping[b]]) for a,b in s['edges']]);s['thresholds']=sorted([dict(node=mapping[t['node']],phi=t['phi']) for t in s['thresholds']],key=lambda x:x['node']);s['initial']['fixed_seeds']=sorted(mapping[x] for x in s['initial']['fixed_seeds'])
    good['relabelled']=q
    bad={}
    def change(name,fn,base='path'):
        q=copy.deepcopy(good[base]);fn(q);bad[name]=q
    change('unknown-field',lambda q:q.update(predicted_date='2030-01-01'))
    change('causal',lambda q:q.update(causal_effect=True))
    change('empirical',lambda q:q['provenance'].update(synthetic=False))
    change('rights',lambda q:q['provenance'].update(rights='unknown'))
    change('source',lambda q:q['provenance'].update(source_ref='unknown'))
    change('snapshot',lambda q:q['provenance'].update(snapshot='altered'))
    change('profile',lambda q:q['profile'].update(sha256='0'*64))
    change('schema',lambda q:q.update(schema_version=True))
    change('nodes',lambda q:q['population'].update(nodes=['000','000','002']))
    change('size',lambda q:q['population'].update(size=4))
    change('self-loop',lambda q:q['scenarios'][0].update(edges=[['000','000']]))
    change('duplicate-edge',lambda q:q['scenarios'][0].update(edges=[['000','001'],['000','001']]))
    change('reversed-edge',lambda q:q['scenarios'][0].update(edges=[['001','000']]))
    change('unknown-node',lambda q:q['scenarios'][0].update(edges=[['000','999']]))
    change('malformed-edge',lambda q:q['scenarios'][0].update(edges=[['000']]))
    for name,phi in [('float',0.5),('bool',True),('negative','-1/2'),('over-one','3/2'),('zero-den','1/0'),('huge','1'+'0'*32)]:change('phi-'+name,lambda q,p=phi:q['scenarios'][0]['thresholds'][0].update(phi=p))
    change('threshold-order',lambda q:q['scenarios'][0]['thresholds'].reverse())
    change('seed-duplicate',lambda q:q['scenarios'][0]['initial'].update(fixed_seeds=['000','000']))
    change('seed-unknown',lambda q:q['scenarios'][0]['initial'].update(fixed_seeds=['x']))
    change('initial-mode',lambda q:q['scenarios'][0]['initial'].update(mode='infectious'))
    change('probability-conflict',lambda q:q['scenarios'][0]['initial'].update(probability='1/2'))
    change('run-seeds-count',lambda q:q['scenarios'][0]['initial'].update(run_seeds=[[]],fixed_seeds=[],mode='explicit_runs'),'exhaustive')
    change('override-bool',lambda q:q['scenarios'][0]['initial'].update(overrides=[dict(node='000',state=True)]))
    change('override-duplicate',lambda q:q['scenarios'][0]['initial'].update(overrides=[dict(node='000',state=1),dict(node='000',state=0)]))
    change('rng-zero',lambda q:q['rng'].update(seed=0));change('rng-type',lambda q:q['rng'].update(seed=True));change('rng-algorithm',lambda q:q['rng'].update(algorithm='other'))
    change('rounds',lambda q:q.update(rounds=4));change('runs',lambda q:q.update(runs=257));change('trace-type',lambda q:q.update(trace_states=1))
    change('reference',lambda q:q.update(reference_scenario='missing'));change('duplicate-scenario',lambda q:q['scenarios'].append(copy.deepcopy(q['scenarios'][0])))
    q=request(128,runs=256,trace=False);bad['count-cap']=q
    q=request(128,runs=2,trace=True);bad['state-cap']=q
    q=request(64,list(itertools.combinations(range(64),2)),runs=64,trace=False);q['scenarios']*=8
    for i,s in enumerate(q['scenarios']):q['scenarios'][i]=copy.deepcopy(s);q['scenarios'][i]['id']='s'+str(i)
    q['reference_scenario']='s0';q['rounds']=4;bad['work-cap']=q
    q=request(65,list(itertools.combinations(range(65),2)),cap=0,trace=False);bad['edge-cap']=q
    return {**{k:(v,0) for k,v in good.items()},**{k:(v,2) for k,v in bad.items()}}

FAMILIES={
 'population-conservation':['path','bernoulli'],'one-step-transitions':['path'],'zero-probability-events':['rho-zero'],'certain-transitions':['rho-one'],
 'absorbing-states':['all-seed','truncated','zero-cap'],'isolated-nodes':['isolated','singleton'],'fully-connected':['complete-tie'],
 'seeded-event-ordering':['bernoulli','overrides'],'repeated-run-counts':['exhaustive','bernoulli'],'scenario-boundaries':['reference','duplicate-scenario'],
 'common-random-pairing':['identical','paired-rho','overrides'],'causal-claims':['causal'],'parameter-misspecification':['threshold-comparison'],
 'topology-sensitivity':['topology'],'synthetic-mode':['empirical'],'rights-source':['rights','source','snapshot'],
 'json-markdown-replay':['unicode'],'unsupported-real-world-prediction':['unknown-field'],'synchronous-asynchronous':['path'],
 'fraction-threshold-boundary':['complete-tie','node-thresholds'],'initial-seed-binomial':['exhaustive','bernoulli'],
 'finite-work-resource-caps':['count-cap','state-cap','work-cap','edge-cap'],'node-relabeling-invariance':['node-thresholds','relabelled']}

def freeze():
    assert words(1,5)==[270369,67634689,2647435461,307599695,2398689233]
    allcases=cases();expected={k:oracle(q) for k,(q,c) in allcases.items() if c==0}
    assert expected['path']['base'][0]['states']==[[1,0,0],[1,1,0],[1,1,1]]
    assert [expected['topology'][s][0]['counts'][-1] for s in ['base','complete']]==[4,1]
    final=[r['counts'][-1] for r in expected['exhaustive']['base']];assert final==[0,2,2,2]
    assert stats(final)==dict(mean='3/2',population_variance='3/4',sample_variance='1')
    gains=[r['counts'][-1]-r['counts'][0] for r in expected['exhaustive']['base']];assert stats(gains)['population_variance']=='1/4'
    fixture=dict(version=1,families=FAMILIES,prng_seed1_first5=words(1,5),cases={k:dict(input=q,exit_code=c,expected=expected.get(k)) for k,(q,c) in allcases.items()},
        literal_anchors=dict(path=[[1,0,0],[1,1,0],[1,1,1]],forward_inplace_one_sweep=[1,1,1],reverse_inplace_one_sweep=[1,1,0],two_node_final_counts=final,final_count=stats(final),final_fraction=stats([F(x,2) for x in final]),gain=stats(gains),binomial_N4_rho_quarter=dict(mean='1',variance='3/4')))
    path=R/'tests/fixtures/psychohistory-independent-v1.json';path.write_text(json.dumps(fixture,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    manifest=dict(version=1,profile_sha256=digest(json.loads((R/'knowledge/psychohistory_profile_v1.json').read_text(encoding='utf-8'))),fixture_families=len(FAMILIES),accepted=sum(c==0 for _,c in allcases.values()),rejected=sum(c!=0 for _,c in allcases.values()),normalized_lf_sha256={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in [path,Path(__file__)]})
    (R/'knowledge/psychohistory_fixture_freeze_v1.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(manifest)

if __name__=='__main__':freeze()
