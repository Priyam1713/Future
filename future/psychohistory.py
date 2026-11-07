"""Exact synthetic synchronous threshold dynamics; no real-world prediction."""
import copy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re
from .remote_viewing import digest,obj,integer,identifier,text
from .scrying import load_input,freeze

ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='b7e9f2d27994be3e89ac0bba0e2066bbc19bd89241e01e4b0989621de061988f'

def assets():
    p=load_input(ROOT/'knowledge/psychohistory_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned Psychohistory profile mismatch')
    for file,key in [('psychohistory_sources.json','source_manifest_sha256'),('psychohistory_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/file))!=p[key]:raise ValueError('Pinned source integrity mismatch')
    return p

DATA=freeze(assets())
def fields(v,key):obj(v,DATA['schema'][key])
def sequence(v,limit):
    if not isinstance(v,list) or len(v)>limit:raise ValueError('Bounded list required')
    return v
def probability(v):
    if not isinstance(v,str) or re.fullmatch(r'(?:0|[1-9][0-9]{0,31})(?:/[1-9][0-9]{0,31})?',v) is None:raise ValueError('Exact bounded rational probability string required')
    p=Q(v)
    if not 0<=p<=1:raise ValueError('Probability outside0..1')
    return p
def ordered_ids(v,nodes):
    sequence(v,len(nodes))
    for node in v:
        identifier(node)
        if node not in nodes:raise ValueError('Unknown node identity')
    if v!=sorted(set(v)):raise ValueError('Sorted unique node IDs required')
    return v
def nonempty(v):
    if not text(v,4000).strip():raise ValueError('Nonempty text required')
    return v

def validate(q):
    fields(q,'root');integer(q['schema_version'],1,1);fields(q['profile'],'profile')
    if q['profile']!=dict(id=DATA['id'],sha256=PROFILE_HASH,catalog_sha256=DATA['source_manifest_sha256']):raise ValueError('Profile identity mismatch')
    pop=q['population'];fields(pop,'population');n=integer(pop['size'],1,128);nodes=sequence(pop['nodes'],128)
    if len(nodes)!=n:raise ValueError('Population size mismatch')
    ordered_ids(nodes,nodes)
    runs=integer(q['runs'],1,256);cap=integer(q['rounds'],0,n)
    if type(q['trace_states']) is not bool:raise ValueError('Exact trace boolean required')
    fields(q['rng'],'rng')
    if q['rng']['algorithm']!='xorshift32-v1':raise ValueError('Unsupported random generator')
    integer(q['rng']['seed'],1,2**32-1)
    scenarios=sequence(q['scenarios'],8)
    if not scenarios:raise ValueError('At least one scenario required')
    ids=[];work=0
    for s in scenarios:
        fields(s,'scenario');identifier(s['id']);ids.append(s['id']);edges=sequence(s['edges'],2048)
        for edge in edges:
            if not isinstance(edge,list) or len(edge)!=2:raise ValueError('Two-ID edge required')
            ordered_ids(edge,nodes)
            if len(set(edge))!=2:raise ValueError('Self-loop rejected')
        if edges!=sorted(edges) or len({tuple(e) for e in edges})!=len(edges):raise ValueError('Canonical unique edges required')
        thresholds=sequence(s['thresholds'],128)
        for t in thresholds:fields(t,'threshold');identifier(t['node']);probability(t['phi'])
        if [t['node'] for t in thresholds]!=nodes:raise ValueError('Ordered complete thresholds required')
        init=s['initial'];fields(init,'initial');mode=init['mode']
        if mode not in ('fixed','bernoulli','explicit_runs'):raise ValueError('Unsupported initialization')
        ordered_ids(init['fixed_seeds'],nodes);sequence(init['run_seeds'],runs)
        for row in init['run_seeds']:ordered_ids(row,nodes)
        if mode=='bernoulli':probability(init['probability'])
        elif init['probability'] is not None:raise ValueError('Unexpected probability')
        if mode!='fixed' and init['fixed_seeds']:raise ValueError('Unexpected fixed seeds')
        if mode=='explicit_runs':
            if len(init['run_seeds'])!=runs:raise ValueError('Run seeds count mismatch')
        elif init['run_seeds']:raise ValueError('Unexpected run seeds')
        overrides=sequence(init['overrides'],n)
        for o in overrides:fields(o,'override');identifier(o['node']);integer(o['state'],0,1)
        ordered_ids([o['node'] for o in overrides],nodes)
        work+=runs*(cap+1)*(n+2*len(edges))
    if len(set(ids))!=len(ids):raise ValueError('Duplicate scenario ID')
    identifier(q['reference_scenario'])
    if q['reference_scenario'] not in ids:raise ValueError('Unknown reference scenario')
    p=q['provenance'];fields(p,'provenance')
    if p['synthetic'] is not True:raise ValueError('Synthetic data required')
    if p['source_ref'] not in [s['id'] for s in load_input(ROOT/'knowledge/psychohistory_sources.json')]:raise ValueError('Unknown source')
    if p['rights'] not in ('self_authored','permission_granted'):raise ValueError('Declared synthetic rights required')
    nonempty(p['attribution']);nonempty(p['snapshot'])
    if p['snapshot_sha256']!=hashlib.sha256(p['snapshot'].encode('utf-8')).hexdigest():raise ValueError('Snapshot hash mismatch')
    budget=dict(work_units=work,count_cells=len(scenarios)*(2*(runs+1)*(cap+1)+12*runs+32),state_cells=int(q['trace_states'])*len(scenarios)*runs*(cap+1)*n)
    for name,value in budget.items():
        if value>DATA['bounds'][name]:raise ValueError('Combined '+name+' budget exceeded')
    return budget

def words(seed,count):
    result=[]
    for _ in range(count):
        seed^=(seed<<13)&0xffffffff;seed^=seed>>17;seed^=(seed<<5)&0xffffffff;seed&=0xffffffff;result.append(seed)
    return result

def statistics(values):
    size=len(values);mean=sum(map(Q,values),Q())/size;var=sum((Q(v)-mean)**2 for v in values)/size
    return dict(runs=size,mean=str(mean),population_variance=str(var),population_denominator=size,
                sample_variance=str(var*size/(size-1)) if size>1 else None,sample_denominator=size-1 if size>1 else None,sample_status='estimable' if size>1 else 'not_estimable')

def evolve(initial,adj,thresholds,cap):
    state=initial[:];states=[state];truncated=False
    for tick in range(cap+1):
        following=[int(state[i] or bool(neighbors) and sum(state[j] for j in neighbors)*thresholds[i].denominator>=len(neighbors)*thresholds[i].numerator) for i,neighbors in enumerate(adj)]
        if following==state:break
        if tick==cap:truncated=True;break
        state=following;states.append(state)
    return states,truncated

def read(q,registry=None):
    # No PRNG or transition work occurs until the complete request passes preflight.
    budget=validate(q);q=copy.deepcopy(q);nodes=q['population']['nodes'];n=len(nodes);runs=q['runs'];cap=q['rounds'];index={node:i for i,node in enumerate(nodes)}
    draws=words(q['rng']['seed'],runs*n)
    stream=dict(algorithm=q['rng']['algorithm'],seed=q['rng']['seed'],nodes=nodes,runs=runs,words=draws)
    stream_hash=digest(stream);scenarios=[]
    for s in q['scenarios']:
        adj=[[] for _ in nodes]
        for a,b in s['edges']:adj[index[a]].append(index[b]);adj[index[b]].append(index[a])
        thresholds=[probability(t['phi']) for t in s['thresholds']];init=s['initial'];rho=probability(init['probability']) if init['mode']=='bernoulli' else None;rows=[]
        for run in range(runs):
            seeds=init['fixed_seeds'] if init['mode']=='fixed' else init['run_seeds'][run] if init['mode']=='explicit_runs' else []
            state=[int(node in seeds) if rho is None else int(draws[run*n+i]*rho.denominator<2**32*rho.numerator) for i,node in enumerate(nodes)]
            for o in init['overrides']:state[index[o['node']]]=o['state']
            states,truncated=evolve(state,adj,thresholds,cap);counts=[sum(row) for row in states]
            rows.append(dict(run=run,initial_active=counts[0],final_active=counts[-1],initial_fraction=str(Q(counts[0],n)),final_fraction=str(Q(counts[-1],n)),
                active_counts=counts,inactive_counts=[n-x for x in counts],states=states if q['trace_states'] else None,initial_state_sha256=digest(states[0]),final_state_sha256=digest(states[-1]),
                draw_row_sha256=digest(draws[run*n:(run+1)*n]),converged=not truncated,truncated=truncated,executed_rounds=len(states)-1,
                persistence_final_active=counts[0],paired_gain=counts[-1]-counts[0]))
        initial=[r['initial_active'] for r in rows];final=[r['final_active'] for r in rows]
        means=[sum(Q(r['active_counts'][min(t,len(r['active_counts'])-1)]) for r in rows)/runs for t in range(cap+1)]
        moments=dict(status='not_applicable',reason='Not an iid Bernoulli initialization',mean=None,variance=None)
        if rho is not None:
            free=n-len(init['overrides']);fixed=sum(o['state'] for o in init['overrides'])
            moments=dict(status='ideal_iid_initial_only',mean=str(fixed+free*rho),variance=str(free*rho*(1-rho)),free_nodes=free,fixed_active=fixed)
        scenarios.append(dict(id=s['id'],graph_sha256=digest(dict(nodes=nodes,edges=s['edges'])),thresholds_sha256=digest(s['thresholds']),initial_spec_sha256=digest(init),model_sha256=digest(dict(profile=PROFILE_HASH,nodes=nodes,edges=s['edges'],thresholds=s['thresholds'],initial=init)),
            initialization_design=init['mode'],rows=rows,initial_count=statistics(initial),final_count=statistics(final),initial_fraction=statistics([Q(x,n) for x in initial]),final_fraction=statistics([Q(x,n) for x in final]),
            per_round_mean_active=[str(x) for x in means],per_round_mean_inactive=[str(n-x) for x in means],ideal_initial_moments=moments,
            persistence_baseline=dict(name='no-influence persistence; same initial states',final_count=statistics(initial),paired_gains=[r['paired_gain'] for r in rows],gain=statistics([r['paired_gain'] for r in rows])),
            converged_runs=sum(r['converged'] for r in rows),truncated_runs=sum(r['truncated'] for r in rows)))
    ref=next(s for s in scenarios if s['id']==q['reference_scenario']);refspec=next(s for s in q['scenarios'] if s['id']==ref['id']);comparisons=[]
    for s,spec in zip(scenarios,q['scenarios']):
        diff=[a['final_active']-b['final_active'] for a,b in zip(s['rows'],ref['rows'])];changed=[k for k in ('edges','thresholds','initial') if spec[k]!=refspec[k]]
        comparisons.append(dict(scenario=s['id'],reference=ref['id'],changed_parameters=changed,identical_configuration=not changed,paired_final_differences=diff,statistics=statistics(diff),pairing_stream_sha256=stream_hash))
    sources=load_input(ROOT/'knowledge/psychohistory_sources.json')
    if registry is not None:
        for source in sources:registry.add_source(source)
    result=dict(status='accepted',technique_id=52,profile=dict(q['profile']),schema_version=1,request=q,input_sha256=digest(q),
        code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),source_manifest_sha256=DATA['source_manifest_sha256'],source_freeze_sha256=DATA['source_freeze_sha256'],
        source_snapshot_sha256=q['provenance']['snapshot_sha256'],stream_sha256=stream_hash,draw_count=len(draws),budget=budget,scenarios=scenarios,comparisons=comparisons,sources=sources,
        interpretation=dict(fictional_inspiration='Asimov; fictional premise',simulation='Original synthetic editorial synchronous finite-graph model',scenario_differences='Hypothetical model sensitivity only',empirical_calibration='unsupported',held_out_validation='unsupported',causal_inference='unsupported',rounds='Dimensionless steps; not dates',statistics='Exact deterministic finite-PRNG sample summaries; correlated cascade outcomes; no confidence interval or guaranteed CRN variance reduction'),limits=list(DATA['unsupported']))
    result['report_sha256']=digest(result);return result

def markdown(report):
    body=json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False);fence='`'*max(3,1+max([len(x) for x in re.findall(r'`+',body)]+[0]))
    return '# Psychohistory — synthetic threshold dynamics\n\n'+fence+'json\n'+body+'\n'+fence+'\n'
