"""Finite exact back-door diagnostics under declared synthetic causal assumptions."""
import copy,hashlib,itertools,json,math,re
from fractions import Fraction as F
from pathlib import Path
from .remote_viewing import digest,obj,identifier,integer,text
from .scrying import load_input,freeze
ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='872e27c27228050ad3a6714bc7549d5c29a98406bc4fec70ddccc99d6d7ace20'
def assets():
    p=load_input(ROOT/'knowledge/causal_ai_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned causal profile mismatch')
    for name,key in [('causal_ai_sources.json','source_manifest_sha256'),('causal_ai_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/name))!=p[key]:raise ValueError('Pinned source integrity mismatch')
    return p
DATA=freeze(assets())
def fields(v,key):obj(v,DATA['schema'][key])
def seq(v,limit):
    if not isinstance(v,list) or len(v)>limit:raise ValueError('Bounded list required')
    return v
def rational(v):
    if type(v) is int:
        if len(str(abs(v)))>18:raise ValueError('Rational component digits exceeded')
        return F(v)
    if not isinstance(v,str) or not re.fullmatch(r'-?(?:0|[1-9][0-9]{0,17})(?:/[1-9][0-9]{0,17})?',v) or v.startswith('-0'):raise ValueError('Exact bounded rational required')
    return F(v)
def operation(a,b,kind):
    an,ad=a.numerator.bit_length(),a.denominator.bit_length();bn,bd=b.numerator.bit_length(),b.denominator.bit_length()
    nb=max(an+bd,bn+ad)+1 if kind=='add' else an+bn;db=ad+bd
    if max(nb,db)>8192:raise ValueError('Intermediate rational bit reservation exceeded')
    return a+b if kind=='add' else a*b
def add(a,b):return operation(a,b,'add')
def mul(a,b):return operation(a,b,'mul')
def ratio(a,b):
    if b==0:raise ValueError('Undefined probability denominator')
    return mul(a,F(b.denominator,b.numerator))
def total(xs):
    s=F(0)
    for x in xs:s=add(s,x)
    return s
def closure(seeds,adj):
    seen=set();pending=list(seeds)
    while pending:
        n=pending.pop()
        if n not in seen:seen.add(n);pending.extend(adj[n])
    return seen
def separated(names,edges,x,y,z):
    """Direction-state active-trail traversal; independent oracle enumerates paths."""
    parents={n:set() for n in names};children={n:set() for n in names}
    for a,b in edges:parents[b].add(a);children[a].add(b)
    ancestors=closure(z,parents);known=set(z);pending=[(x,'up')];seen=set()
    while pending:
        v,direction=pending.pop()
        if (v,direction) in seen:continue
        seen.add((v,direction))
        if v==y and v not in known:return False
        if direction=='up' and v not in known:
            pending.extend((p,'up') for p in parents[v]);pending.extend((c,'down') for c in children[v])
        elif direction=='down':
            if v not in known:pending.extend((c,'down') for c in children[v])
            if v in ancestors:pending.extend((p,'up') for p in parents[v])
    return True
def backdoor(names,edges,x,y,z):
    children={n:set() for n in names}
    for a,b in edges:children[a].add(b)
    descendants=closure([x],children)-{x};forbidden=sorted(set(z)&descendants)
    return dict(valid=not forbidden and separated(names,[(a,b) for a,b in edges if a!=x],x,y,z),descendants_in_adjustment=forbidden,surgery='Remove outgoing treatment edges for back-door check; not intervention surgery')
def validate(q):
    fields(q,'root');integer(q['schema_version'],1,1);fields(q['profile'],'profile');integer(q['profile']['version'],1,1)
    if q['profile']!=dict(id=DATA['id'],version=1,sha256=PROFILE_HASH,catalog_sha256=DATA['source_manifest_sha256']):raise ValueError('Profile identity mismatch')
    nodes=seq(q['nodes'],8)
    if len(nodes)<2:raise ValueError('At least two nodes required')
    states={};observed=[]
    for n in nodes:
        fields(n,'node');identifier(n['id']);ss=seq(n['states'],3)
        if len(ss)<2 or len(set(map(identifier,ss)))!=len(ss):raise ValueError('Distinct declared states required')
        if n['id'] in states:raise ValueError('Duplicate node')
        if type(n['observed']) is not bool:raise ValueError('Exact observed boolean required')
        states[n['id']]=sorted(ss)
        if n['observed']:observed.append(n['id'])
    names=sorted(states);observed.sort();edges=[];children={n:set() for n in names};indegree={n:0 for n in names}
    for edge in seq(q['edges'],28):
        seq(edge,2)
        if len(edge)!=2:raise ValueError('Directed edge pair required')
        a,b=map(identifier,edge)
        if a not in states or b not in states or a==b:raise ValueError('Unknown endpoint or self edge')
        if (a,b) in edges:raise ValueError('Duplicate edge')
        edges.append((a,b));children[a].add(b);indegree[b]+=1
    pending=[n for n in names if not indegree[n]];ordered=[]
    while pending:
        n=pending.pop();ordered.append(n)
        for c in children[n]:
            indegree[c]-=1
            if not indegree[c]:pending.append(c)
    if len(ordered)!=len(names):raise ValueError('Cyclic graph unsupported')
    x=identifier(q['treatment']);y=identifier(q['outcome'])
    if x==y or x not in observed or y not in observed:raise ValueError('Distinct observed treatment/outcome required')
    if q['outcome_value'] not in states[y]:raise ValueError('Unknown outcome state')
    z=seq(q['adjustment'],6)
    for n in z:identifier(n)
    if len(z)!=len(set(z)) or any(n not in observed or n in (x,y) for n in z):raise ValueError('Invalid observed adjustment set')
    fields(q['assumptions'],'assumptions');assumptions=dict(causal_graph=True,consistency=True,exchangeability_under_graph=True,selection_bias=False)
    if q['assumptions']!=assumptions or any(type(v) is not bool for v in q['assumptions'].values()):raise ValueError('Explicit supported causal assumptions required')
    cells=math.prod(len(states[n]) for n in observed);strata=math.prod(len(states[n]) for n in z)
    budget=dict(joint_cells=cells,work=cells*len(names)**2*8,returned_cells=cells*len(names)+strata*len(states[x])*8)
    for key,v in budget.items():
        if v>DATA['bounds'][key]:raise ValueError('Combined '+key+' cap exceeded')
    rows=seq(q['joint'],4096)
    if len(rows)!=cells:raise ValueError('Complete observed joint rows required,including zeros')
    table={}
    for row in rows:
        fields(row,'joint_row');obj(row['assignment'],observed)
        key=tuple(row['assignment'][n] for n in observed)
        if any(a not in states[n] for n,a in zip(observed,key)):raise ValueError('Unknown joint state')
        if key in table:raise ValueError('Duplicate joint assignment')
        p=rational(row['weight'])
        if p<0:raise ValueError('Negative probability')
        table[key]=p
    if total(table.values())!=1:raise ValueError('Joint probabilities must sum exactly to one')
    p=q['provenance'];fields(p,'provenance')
    if p['synthetic'] is not True or p['rights']!='self_authored':raise ValueError('Self-authored synthetic tables required')
    if p['source_ref'] not in [s['id'] for s in load_input(ROOT/'knowledge/causal_ai_sources.json')]:raise ValueError('Unknown source')
    for key in ('attribution','snapshot'):
        if not text(p[key],4000).strip():raise ValueError('Nonempty provenance required')
    if p['snapshot_sha256']!=hashlib.sha256(p['snapshot'].encode()).hexdigest():raise ValueError('Snapshot hash mismatch')
    return names,observed,states,sorted(edges),table,budget
def compatibility(names,edges,table):
    parents={n:sorted(a for a,b in edges if b==n) for n in names};indices={n:i for i,n in enumerate(names)};den={};num={}
    for n in names:
        den[n]={};num[n]={}
        for key,p in table.items():
            pa=tuple(key[indices[a]] for a in parents[n]);v=key[indices[n]]
            den[n][pa]=add(den[n].get(pa,F(0)),p);num[n][(pa,v)]=add(num[n].get((pa,v),F(0)),p)
    mismatches=[]
    for key,p in sorted(table.items()):
        product=F(1)
        for n in names:
            pa=tuple(key[indices[a]] for a in parents[n]);d=den[n][pa]
            if not d:product=F(0);break
            product=mul(product,ratio(num[n][(pa,key[indices[n]])],d))
        if product!=p:mismatches.append(dict(assignment=dict(zip(names,key)),joint=str(p),factorized=str(product)))
    return dict(status='compatible' if not mismatches else 'incompatible',mismatch_count=len(mismatches),first_mismatch=mismatches[0] if mismatches else None,scope='Exact finite probability compatibility,not empirical causal truth')
def read(request,registry=None):
    q=copy.deepcopy(request);names,observed,states,edges,table,budget=validate(q);x=q['treatment'];y=q['outcome'];z=sorted(q['adjustment']);index={n:i for i,n in enumerate(observed)};levels=states[x];target=q['outcome_value']
    graph=backdoor(names,edges,x,y,z);latent=sorted(set(names)-set(observed));compat=dict(status='not_checked',reason='Latent graph unsupported') if latent else compatibility(names,edges,table)
    px={a:F(0) for a in levels};pyx={a:F(0) for a in levels};pz={};pxz={};pyxz={}
    for key,p in table.items():
        a=key[index[x]];zs=tuple(key[index[n]] for n in z);event=key[index[y]]==target
        px[a]=add(px[a],p);pyx[a]=add(pyx[a],p if event else F(0));pz[zs]=add(pz.get(zs,F(0)),p)
        pxz[(a,zs)]=add(pxz.get((a,zs),F(0)),p);pyxz[(a,zs)]=add(pyxz.get((a,zs),F(0)),p if event else F(0))
    obs={a:str(ratio(pyx[a],px[a])) if px[a] else None for a in levels};overlap=[dict(treatment_value=a,stratum=dict(zip(z,zs))) for zs,p in sorted(pz.items()) if p for a in levels if pxz[(a,zs)]==0]
    if latent:status='unsupported_latent_graph'
    elif not graph['valid']:status='unsupported_adjustment'
    elif compat['status']!='compatible':status='incompatible_joint_graph'
    elif overlap:status='not_estimable_positivity'
    else:status='identified_under_declared_assumptions'
    estimates=None;stratum_rows=[]
    if status=='identified_under_declared_assumptions':
        risks={a:F(0) for a in levels}
        for zs,mass in sorted(pz.items()):
            cond={a:ratio(pyxz[(a,zs)],pxz[(a,zs)]) for a in levels} if mass else None
            terms={a:mul(cond[a],mass) for a in levels} if mass else None
            if terms:
                for a in levels:risks[a]=add(risks[a],terms[a])
            stratum_rows.append(dict(assignment=dict(zip(z,zs)),mass=str(mass),skipped_zero_mass=not bool(mass),conditional=None if cond is None else {a:str(v) for a,v in cond.items()},weighted_terms=None if terms is None else {a:str(v) for a,v in terms.items()}))
        estimates=dict(risks={a:str(v) for a,v in risks.items()},contrast_first_minus_last=str(add(risks[levels[0]],-risks[levels[-1]])),contrast_last_minus_first=str(add(risks[levels[-1]],-risks[levels[0]])),level_order=levels,scope='Conditional on declared causal graph,consistency,exchangeability and absence of selection bias')
    canonical_graph=dict(nodes=sorted([dict(id=n,states=states[n],observed=n in observed) for n in names],key=lambda n:n['id']),edges=edges,query=dict(treatment=x,outcome=y,outcome_value=target,adjustment=z),assumptions=q['assumptions'])
    canonical_table=[dict(assignment=dict(zip(observed,key)),weight=str(p)) for key,p in sorted(table.items())];sources=load_input(ROOT/'knowledge/causal_ai_sources.json')
    if registry is not None:
        for source in sources:registry.add_source(source)
    result=dict(status='accepted',technique_id=56,schema_version=1,profile=q['profile'],request=q,input_sha256=digest(q),model_sha256=digest(canonical_graph),table_sha256=digest(canonical_table),source_manifest_sha256=DATA['source_manifest_sha256'],source_freeze_sha256=DATA['source_freeze_sha256'],schema_sha256=digest(dict(DATA['schema'])),code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),identification_status=status,backdoor=graph,latent_nodes=latent,compatibility=compat,positivity=dict(passed=not overlap,failures=overlap,zero_mass_strata=[dict(zip(z,k)) for k,v in sorted(pz.items()) if not v]),observational=dict(risks=obs,contrast_first_minus_last=None if obs[levels[0]] is None or obs[levels[-1]] is None else str(add(F(obs[levels[0]]),-F(obs[levels[-1]]))),contrast_last_minus_first=None if obs[levels[0]] is None or obs[levels[-1]] is None else str(add(F(obs[levels[-1]]),-F(obs[levels[0]]))),level_order=levels,scope='Association only'),interventional=estimates,strata=stratum_rows,budget=budget,sources=sources,limitations=list(DATA['configuration_matrix']['unsupported'])+['Supplied-set sufficient criterion failure does not prove general nonidentifiability.','Graph/table compatibility and synthetic arithmetic are not causal discovery or empirical validation.','Identities,rights and assumptions are declarations,not independently certified truth.'])
    result['report_sha256']=digest(result);return result
def markdown(result):
    body=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False);fence='`'*max(3,1+max([len(x) for x in re.findall(r'`+',body)]+[0]))
    return '# Causal AI — finite synthetic back-door reference\n\n'+fence+'json\n'+body+'\n'+fence+'\n'
