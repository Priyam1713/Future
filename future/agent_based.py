"""Exact finite zero-exterior synchronous B3/S23; synthetic model only."""
import copy,hashlib,json,re
from pathlib import Path
from .remote_viewing import digest,obj,identifier,integer,text
from .scrying import load_input,freeze

ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='e6d0487cf23393a1262efb227ef912542f38ae6cb9232358a6bbc34c9053a62b'
def assets():
    p=load_input(ROOT/'knowledge/agent_based_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned Agent-Based profile mismatch')
    for file,key in [('agent_based_sources.json','source_manifest_sha256'),('agent_based_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/file))!=p[key]:raise ValueError('Pinned source integrity mismatch')
    return p
_PROFILE=assets();DATA=freeze(_PROFILE);SCHEMA_HASH=digest(_PROFILE['schema']);RULE_HASH=digest(dict(rule='B3/S23',birth=[3],survival=[2,3]))
def fields(v,name):obj(v,DATA['schema'][name])
def sequence(v,limit):
    if not isinstance(v,list) or len(v)>limit:raise ValueError('Bounded list required')
    return v
def nonempty(v):
    if not text(v,4000).strip():raise ValueError('Nonempty text required')
    return v
def validate(q):
    fields(q,'root');integer(q['schema_version'],1,1);fields(q['profile'],'profile')
    if q['profile']!=dict(id=DATA['id'],version=1,sha256=PROFILE_HASH,catalog_sha256=DATA['source_manifest_sha256']):raise ValueError('Profile identity mismatch')
    integer(q['profile']['version'],1,1);fields(q['model'],'model')
    if q['model']!=dict(DATA['model']):raise ValueError('Only synchronous B3/S23,Moore radius1 andfinite-zero-exterior supported')
    fields(q['geometry'],'geometry');h=integer(q['geometry']['height'],1,64);w=integer(q['geometry']['width'],1,64);n=h*w
    if n>4096:raise ValueError('Cell limit exceeded')
    ticks=integer(q['ticks'],0,256)
    if type(q['trace_states']) is not bool:raise ValueError('Exact trace boolean required')
    scenarios=sequence(q['scenarios'],8)
    if not scenarios:raise ValueError('At least one scenario required')
    ids=[]
    for s in scenarios:
        fields(s,'scenario');identifier(s['id']);ids.append(s['id']);board=sequence(s['initial_grid'],64)
        if len(board)!=h:raise ValueError('Grid height mismatch')
        for row in board:
            sequence(row,64)
            if len(row)!=w:raise ValueError('Grid width mismatch')
            for cell in row:integer(cell,0,1)
    if len(set(ids))!=len(ids):raise ValueError('Duplicate scenario ID')
    identifier(q['reference_scenario'])
    if q['reference_scenario'] not in ids:raise ValueError('Unknown reference scenario')
    p=q['provenance'];fields(p,'provenance')
    if p['synthetic'] is not True:raise ValueError('Original synthetic configurations required')
    if p['source_ref'] not in [s['id'] for s in load_input(ROOT/'knowledge/agent_based_sources.json')]:raise ValueError('Unknown source')
    if p['rights'] not in ('self_authored','permission_granted','public_domain','cc_by'):raise ValueError('Declared snapshot rights required')
    nonempty(p['attribution']);nonempty(p['snapshot'])
    if p['snapshot_sha256']!=hashlib.sha256(p['snapshot'].encode('utf-8')).hexdigest():raise ValueError('Snapshot hash mismatch')
    budget=dict(cell_ticks=n*ticks*len(scenarios),neighbor_cell_work=9*n*ticks*len(scenarios),returned_state_cells=len(scenarios)*n*(2+(ticks+1 if q['trace_states'] else 0)),returned_count_cells=len(scenarios)*(10*(ticks+1)+32))
    for key,value in budget.items():
        if value>DATA['bounds'][key]:raise ValueError('Combined '+key+' budget exceeded')
    return budget

def next_cell(current,neighbors):
    integer(current,0,1);integer(neighbors,0,8)
    return int(neighbors==3 or current==1 and neighbors==2)
def neighborhoods(h,w):
    return [tuple((r+dr)*w+c+dc for dr in (-1,0,1) for dc in (-1,0,1) if (dr or dc) and 0<=r+dr<h and 0<=c+dc<w) for r in range(h) for c in range(w)]
def transition(state,neighbors):
    following=bytearray(len(state))
    for i,adj in enumerate(neighbors):following[i]=next_cell(state[i],sum(state[j] for j in adj))
    return bytes(following)
def board(state,w):return [list(state[i:i+w]) for i in range(0,len(state),w)]
def state_hash(state):return hashlib.sha256(state).hexdigest()

def read(q,registry=None):
    assets();budget=validate(q);q=copy.deepcopy(q);h=q['geometry']['height'];w=q['geometry']['width'];n=h*w;neighbors=neighborhoods(h,w);results=[];histories={}
    model_hash=digest(dict(profile=PROFILE_HASH,model=q['model'],geometry=q['geometry']))
    for s in q['scenarios']:
        initial=bytes(cell for row in s['initial_grid'] for cell in row);state=initial;states=[state];seen={state:0};cycle=None;alive=sum(state)
        counts=[dict(tick=0,alive=alive,dead=n-alive,births=None,deaths=None,state_sha256=state_hash(state))]
        for tick in range(1,q['ticks']+1):
            following=transition(state,neighbors);births=sum(a==0 and b==1 for a,b in zip(state,following));deaths=sum(a==1 and b==0 for a,b in zip(state,following));alive=sum(following)
            if cycle is None and following in seen:cycle=dict(start=seen[following],period=tick-seen[following],first_repeat_tick=tick)
            if following not in seen:seen[following]=tick
            states.append(following);counts.append(dict(tick=tick,alive=alive,dead=n-alive,births=births,deaths=deaths,state_sha256=state_hash(following)));state=following
        classification='unclassified' if cycle is None else 'fixed_point' if cycle['period']==1 else 'periodic_cycle'
        results.append(dict(id=s['id'],initial_grid=board(initial,w),final_grid=board(state,w),initial_state_sha256=state_hash(initial),final_state_sha256=state_hash(state),scenario_sha256=digest(s),model_sha256=model_hash,
            initial_alive=counts[0]['alive'],initial_dead=counts[0]['dead'],final_alive=counts[-1]['alive'],final_dead=counts[-1]['dead'],counts=counts,state_trace=[board(x,w) for x in states] if q['trace_states'] else None,
            classification=classification,fixed_point=classification=='fixed_point',periodic_cycle=classification=='periodic_cycle',cycle_start=cycle['start'] if cycle else None,period=cycle['period'] if cycle else None,first_repeat_tick=cycle['first_repeat_tick'] if cycle else None,
            requested_ticks=q['ticks'],executed_ticks=q['ticks'],early_stopped=False,truncated=cycle is None))
        histories[s['id']]=states
    reference=next(s for s in results if s['id']==q['reference_scenario']);comparisons=[]
    for s in results:
        diffs=[dict(tick=t,alive_difference=s['counts'][t]['alive']-reference['counts'][t]['alive'],hamming_distance=sum(a!=b for a,b in zip(state,ref))) for t,(state,ref) in enumerate(zip(histories[s['id']],histories[reference['id']]))]
        comparisons.append(dict(scenario=s['id'],reference=reference['id'],identical_initial_state=histories[s['id']][0]==histories[reference['id']][0],per_tick=diffs,final_alive_difference=diffs[-1]['alive_difference'],final_hamming_distance=diffs[-1]['hamming_distance'],final_states_equal=histories[s['id']][-1]==histories[reference['id']][-1],interpretation='Conditional synthetic initial-state sensitivity;notreal-world causal effects'))
    sources=load_input(ROOT/'knowledge/agent_based_sources.json')
    if registry is not None:
        for source in sources:registry.add_source(source)
    result=dict(status='accepted',technique_id=54,schema_version=1,profile=dict(q['profile']),schema_sha256=SCHEMA_HASH,request=q,input_sha256=digest(q),model_sha256=model_hash,geometry_sha256=digest(q['geometry']),rule_sha256=RULE_HASH,source_manifest_sha256=DATA['source_manifest_sha256'],source_freeze_sha256=DATA['source_freeze_sha256'],snapshot_sha256=q['provenance']['snapshot_sha256'],code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),state_hash_convention='SHA256 ofraw row-majorbinarybytes0/1;dimensions boundbymodel/geometry hashes',budget=budget,scenarios=results,comparisons=comparisons,sources=sources,
        scope=dict(execution='Verified bounded exact B3/S23 withfinite-zero-exterior synchronous updates',scenarios='Synthetic initial-state sensitivity andmodel patterns',empirical_calibration='unsupported',real_world_social_forecasting='unsupported',epidemiological_prediction='unsupported',LLM_behavior_simulation='unsupported',Schelling='unsupported',Sugarscape='unsupported',time='Ticks aremodel updates,notreal-world time units',source_comparison='Editorial finite-boundary/explicit-input variant;notexactreproduction ofpinnedMesa toroidal/random-initial model',rights='Source/snapshot declarations andhashes arenotindependent truth orrights certification'),limits=list(DATA['configuration_matrix']['unsupported']))
    result['report_sha256']=digest(result);return result

def markdown(result):
    body=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False);fence='`'*max(3,1+max([len(x) for x in re.findall(r'`+',body)]+[0]))
    return '# Agent-Based Simulation — finite-grid B3/S23\n\n'+fence+'json\n'+body+'\n'+fence+'\n'
