"""Exact finite editorial scenario trees; no quantum or universe prediction."""
import copy,hashlib,json,re
from fractions import Fraction as F
from pathlib import Path
from .remote_viewing import digest,obj,integer,identifier,text
from .scrying import load_input,freeze
ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='9f1b7221a1c5aece17521729aa61e1c280c2bb39c2639ddaea716bafc06b0506'
def assets():
    p=load_input(ROOT/'knowledge/multiverse_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned finite scenario profile mismatch')
    for name,key in [('multiverse_sources.json','source_manifest_sha256'),('multiverse_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/name))!=p[key]:raise ValueError('Pinned source integrity mismatch')
    return p
DATA=freeze(assets())
def fields(v,k):obj(v,DATA['schema'][k])
def bounded_list(v,limit):
    if not isinstance(v,list) or len(v)>limit:raise ValueError('Bounded list required')
    return v
def checked(x):
    if max(x.numerator.bit_length(),x.denominator.bit_length())>8192:raise ValueError('Exact fraction bit cap exceeded')
    return x
def rational(v):
    if not isinstance(v,str) or re.fullmatch(r'-?(?:0|[1-9][0-9]{0,8})(?:/[1-9][0-9]{0,8})?',v) is None:raise ValueError('Bounded rational string required')
    return checked(F(v))
def nonempty(v):
    if not text(v,4000).strip():raise ValueError('Nonempty bounded text required')
def validate(q):
    fields(q,'root');integer(q['schema_version'],1,1);fields(q['profile'],'profile');integer(q['profile']['version'],1,1)
    if q['profile']!=dict(id=DATA['id'],version=1,sha256=PROFILE_HASH,catalog_sha256=DATA['source_manifest_sha256']):raise ValueError('Profile identity mismatch')
    s=q['scenario'];fields(s,'scenario');identifier(s['id']);integer(s['version'],1,1);nonempty(s['description'])
    if s['kind']!='educational_editorial_weights' or s['exhaustive'] is not True:raise ValueError('Only declared exhaustive editorial scenarios supported')
    nodes=bounded_list(q['nodes'],256);queries=bounded_list(q['queries'],256)
    if not nodes:raise ValueError('At least one node required')
    budget=dict(work=len(nodes)**2+len(queries)*len(nodes),returned_cells=16*len(nodes)+8*len(queries))
    if any(v>DATA['bounds'][k] for k,v in budget.items()):raise ValueError('Combined resource cap exceeded')
    by={};weights={};utilities={}
    for n in nodes:
        fields(n,'node');identifier(n['id'])
        if n['id'] in by:raise ValueError('Duplicate node/path identity')
        if n['parent'] is not None:identifier(n['parent'])
        by[n['id']]=n;w=rational(n['weight'])
        if not 0<=w<=1:raise ValueError('Branch weight must be in[0,1]')
        weights[n['id']]=w
        if n['utility'] is not None:
            u=rational(n['utility'])
            if abs(u)>1000000:raise ValueError('Utility bound exceeded')
            utilities[n['id']]=u
    roots=[n['id'] for n in nodes if n['parent'] is None]
    if len(roots)!=1:raise ValueError('Exactly one root required')
    root=roots[0]
    if weights[root]!=1:raise ValueError('Root weight must equal1')
    children={k:[] for k in by}
    for n in nodes:
        parent=n['parent']
        if parent is not None:
            if parent not in by or parent==n['id']:raise ValueError('Unknown/self parent')
            children[parent].append(n['id'])
    for values in children.values():values.sort()
    order=[root];paths={root:[root]}
    for name in order:
        for child in children[name]:
            if child in paths:raise ValueError('Cyclic/duplicate path')
            paths[child]=paths[name]+[child]
            if len(paths[child])-1>32:raise ValueError('Tree depth cap exceeded')
            order.append(child)
    if len(order)!=len(by):raise ValueError('Cycle/disconnected component')
    for name,values in children.items():
        if values:
            if name in utilities:raise ValueError('Internal utility must be null')
            total=F(0)
            for child in values:total=checked(total+weights[child])
            if total!=1:raise ValueError('Child weights must sum exactly1')
        elif name not in utilities:raise ValueError('Explicit terminal utility required')
    seen=set()
    for x in queries:
        fields(x,'query')
        for k in ('id','given','target'):identifier(x[k])
        if x['id'] in seen:raise ValueError('Duplicate query identity')
        seen.add(x['id'])
        if x['given'] not in by or x['target'] not in by:raise ValueError('Unknown query node')
    v=q['provenance'];fields(v,'provenance')
    if v['synthetic'] is not True or v['rights']!='self_authored':raise ValueError('Self-authored synthetic scenario required')
    if v['source_ref'] not in [x['id'] for x in load_input(ROOT/'knowledge/multiverse_sources.json')]:raise ValueError('Unknown source')
    nonempty(v['attribution']);nonempty(v['snapshot'])
    if v['snapshot_sha256']!=hashlib.sha256(v['snapshot'].encode()).hexdigest():raise ValueError('Snapshot hash mismatch')
    q['nodes']=sorted(nodes,key=lambda n:n['id']);q['queries']=sorted(queries,key=lambda x:x['id'])
    return by,weights,utilities,root,children,order,paths,budget
def read(request,registry=None):
    q=copy.deepcopy(request);by,w,u,root,children,order,paths,budget=validate(q);mass={root:F(1)}
    for name in order:
        for child in children[name]:mass[child]=checked(mass[name]*w[child])
    for name in reversed(order):
        if children[name]:
            total=F(0)
            for child in children[name]:total=checked(total+checked(w[child]*u[child]))
            u[name]=total
    leaves=sorted(n for n in by if not children[n]);total=F(0)
    for leaf in leaves:total=checked(total+mass[leaf])
    if total!=1:raise ValueError('Complete modeled leaf mass must equal1')
    nodes=[dict(id=n,parent=by[n]['parent'],children=children[n],path=paths[n],depth=len(paths[n])-1,local_weight=str(w[n]),mass=str(mass[n]),terminal=not children[n],declared_utility=by[n]['utility'],conditional_expected_utility=str(u[n]) if mass[n] else None) for n in sorted(by)]
    queries=[]
    for x in q['queries']:
        g,t=x['given'],x['target'];intersection=mass[t] if g in paths[t] else mass[g] if t in paths[g] else F(0)
        queries.append(dict(**x,condition_mass=str(mass[g]),intersection_mass=str(intersection),probability=str(checked(intersection/mass[g])) if mass[g] else None,status='estimated_exact_model' if mass[g] else 'not_estimable_zero_condition'))
    sources=load_input(ROOT/'knowledge/multiverse_sources.json')
    if registry is not None:
        for source in sources:registry.add_source(source)
    r=dict(status='accepted',technique_id=60,schema_version=1,profile=q['profile'],request=q,input_sha256=digest(q),model_sha256=digest(dict(scenario=q['scenario'],nodes=q['nodes'])),schema_sha256=digest(dict(DATA['schema'])),source_manifest_sha256=DATA['source_manifest_sha256'],source_freeze_sha256=DATA['source_freeze_sha256'],code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),root=root,nodes=nodes,leaves=[dict(id=n,mass=str(mass[n]),utility=str(u[n]),weighted_utility=str(checked(mass[n]*u[n]))) for n in leaves],total_leaf_mass=str(total),expected_utility=str(u[root]),queries=queries,budget=budget,numerics=dict(DATA['numeric']),sources=sources,universe_observations_used=False,everett_empirically_validated=False,empirical_forecast_accuracy_validated=False,limitations=list(DATA['configuration_matrix']['unsupported'])+['Editorial weights are declarations,not Born-rule amplitudes or observed frequencies.','Completeness applies to the declared finite tree; externally omitted possibilities cannot be detected.','Utilities and narrative are self-authored synthetic inputs,not recommendations or other-universe predictions.'])
    r['report_sha256']=digest(r);return r
def markdown(result):
    body=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False);fence='`'*max(3,1+max([len(x) for x in re.findall(r'`+',body)]+[0]))
    return '# Multiverse — educational finite editorial scenario tree\n\n'+fence+'json\n'+body+'\n'+fence+'\n'
