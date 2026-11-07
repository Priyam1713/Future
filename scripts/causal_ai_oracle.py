"""Pre-engine structural enumeration and independent simple-path oracle."""
import copy,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def request(names=('X','Y'),edges=(('X','Y'),),adjustment=()):
    p=json.loads((R/'knowledge/causal_ai_profile_v1.json').read_text(encoding='utf-8'));snapshot='Original finite synthetic causal table; no human data.'
    return dict(schema_version=1,profile=dict(id=p['id'],version=1,sha256=digest(p),catalog_sha256=p['source_manifest_sha256']),nodes=[dict(id=n,states=['0','1'],observed=True) for n in names],edges=[list(e) for e in edges],treatment='X',outcome='Y',outcome_value='1',adjustment=list(adjustment),joint=[dict(assignment=dict(zip(names,states)),weight=str(F(1,2**len(names)))) for states in itertools.product(['0','1'],repeat=len(names))],assumptions=dict(causal_graph=True,consistency=True,exchangeability_under_graph=True,selection_bias=False),provenance=dict(synthetic=True,source_ref='causal-ai-pearl-chapter3-v1',rights='self_authored',attribution='Future self-authored finite structural model',snapshot=snapshot,snapshot_sha256=hashlib.sha256(snapshot.encode()).hexdigest()))
def structural():
    counts={states:0 for states in itertools.product(['0','1'],repeat=3)};do={0:0,1:0}
    for z,ex,ey in itertools.product(range(2),range(4),range(10)):
        x=int(ex<(1 if z==0 else 3));y=int(ey<1+2*x+4*z);counts[tuple(map(str,(z,x,y)))]+=1
        for force in [0,1]:do[force]+=int(ey<1+2*force+4*z)
    q=request(('Z','X','Y'),(('Z','X'),('Z','Y'),('X','Y')),('Z',));q['joint']=[dict(assignment=dict(zip(['Z','X','Y'],k)),weight=str(F(v,80))) for k,v in counts.items()]
    assert (F(do[0],80),F(do[1],80))==(F(3,10),F(1,2))
    return q,dict(counts={','.join(k):v for k,v in counts.items()},total=80,do_risks={str(k):str(F(v,80)) for k,v in do.items()})
def backdoor_oracle(names,edges,x,y,z):
    edges=set(map(tuple,edges));z=set(z)
    def reaches(a,b):
        pending=[a];seen=set()
        while pending:
            v=pending.pop()
            if v==b:return True
            if v in seen:continue
            seen.add(v);pending += [c for p,c in edges if p==v]
        return False
    if any(reaches(x,a) for a in z):return False
    adj={n:set() for n in names}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    def search(path):
        v=path[-1]
        if v==y:
            if (path[1],x) not in edges:return False
            for i in range(1,len(path)-1):
                a,c,b=path[i-1:i+2];collider=(a,c) in edges and (b,c) in edges
                if collider and not any(reaches(c,k) for k in z):return False
                if not collider and c in z:return False
            return True
        return any(search(path+[n]) for n in adj[v] if n not in path)
    return not search([x])
def build():
    path=R/'tests/fixtures/causal-ai-independent-v1.json'
    if path.exists():raise ValueError('Immutable fixture already exists')
    q,struct=structural();cases={}
    def add(name,request,status='identified_under_declared_assumptions',risks=None,obs=None):cases[name]=dict(input=request,exit_code=0 if status!='rejected' else 2,expected=dict(identification_status=status,risks=risks,observational=obs))
    add('confounding',q,risks={'0':'3/10','1':'1/2'},obs={'0':'1/5','1':'3/5'})
    x=copy.deepcopy(q);x['adjustment']=[];add('unblocked-confounding',x,'unsupported_adjustment')
    add('no-confounding',request(),risks={'0':'1/2','1':'1/2'},obs={'0':'1/2','1':'1/2'})
    x=request(('X','M','Y'),(('X','M'),('M','Y')));counts={states:0 for states in itertools.product(['0','1'],repeat=3)}
    for a,b,c in itertools.product(range(2),range(4),range(4)):
        m=a^int(b==0);y=m^int(c==0);counts[tuple(map(str,(a,m,y)))]+=1
    x['joint']=[dict(assignment=dict(zip(['X','M','Y'],k)),weight=str(F(v,32))) for k,v in counts.items()];add('mediation',x,risks={'0':'3/8','1':'5/8'})
    y=copy.deepcopy(x);y['adjustment']=['M'];add('mediator-adjusted',y,'unsupported_adjustment')
    edges=[('A','X'),('A','C'),('B','C'),('B','Y'),('C','D')]
    add('collider-closed',request(('A','B','C','D','X','Y'),edges),risks={'0':'1/2','1':'1/2'})
    add('collider-conditioned',request(('A','B','C','D','X','Y'),edges,['C']),'unsupported_adjustment')
    add('collider-descendant',request(('A','B','C','D','X','Y'),edges,['D']),'unsupported_adjustment')
    x=copy.deepcopy(q)
    for row in x['joint']:
        a=row['assignment'];row['weight']=str(F(1,4) if a['X']==a['Z'] else F(0))
    add('missing-positivity',x,'not_estimable_positivity')
    x=copy.deepcopy(q)
    for row in x['joint']:row['weight']='1/4' if row['assignment']['Z']=='0' else '0'
    add('zero-mass-stratum',x,risks={'0':'1/2','1':'1/2'})
    x=request()
    for row in x['joint']:row['weight']='1/2' if row['assignment']['X']==row['assignment']['Y'] else '0'
    add('deterministic-intervention',x,risks={'0':'0','1':'1'})
    x=request(edges=())
    for row in x['joint']:row['weight']='2/5' if row['assignment']['X']==row['assignment']['Y'] else '1/10'
    add('incompatible',x,'incompatible_joint_graph')
    x=request();x['nodes'].append(dict(id='U',states=['0','1'],observed=False));x['edges'] += [['U','X'],['U','Y']];add('latent',x,'unsupported_latent_graph')
    x=copy.deepcopy(q);x['nodes'].reverse();x['edges'].reverse();x['joint'].reverse();add('reordered',x,risks={'0':'3/10','1':'1/2'},obs={'0':'1/5','1':'3/5'})
    x=request();x['nodes'][1]['states'].append('2');x['joint']=[dict(assignment={'X':a,'Y':b},weight='1/6') for a,b in itertools.product(['0','1'],['0','1','2'])];add('categorical',x,risks={'0':'1/3','1':'1/3'})
    mut={
     'cycle':lambda x:x['edges'].append(['Y','X']),
     'unknown-edge':lambda x:x['edges'].append(['X','unknown']),
     'duplicate-edge':lambda x:x['edges'].append(['X','Y']),
     'self-edge':lambda x:x['edges'].append(['X','X']),
     'duplicate-node':lambda x:x['nodes'].append(copy.deepcopy(x['nodes'][0])),
     'duplicate-state':lambda x:x['nodes'][0]['states'].append('0'),
     'duplicate-row':lambda x:x['joint'].append(copy.deepcopy(x['joint'][0])),
     'missing-row':lambda x:x['joint'].pop(),
     'unknown-state':lambda x:x['joint'][0]['assignment'].update(X='2'),
     'negative-weight':lambda x:x['joint'][0].update(weight='-1/4'),
     'unnormalized':lambda x:x['joint'][0].update(weight='1/2'),
     'float-weight':lambda x:x['joint'][0].update(weight=0.25),
     'boolean-weight':lambda x:x['joint'][0].update(weight=True),
     'zero-denominator':lambda x:x['joint'][0].update(weight='1/0'),
     'large-rational':lambda x:x['joint'][0].update(weight=10**18),
     'bad-assumption':lambda x:x['assumptions'].update(causal_graph=False),
     'selection-bias':lambda x:x['assumptions'].update(selection_bias=True),
     'adjust-X':lambda x:x.update(adjustment=['X']),
     'unknown-adjustment':lambda x:x.update(adjustment=['unknown']),
     'unknown-outcome':lambda x:x.update(outcome_value='unknown'),
     'empirical':lambda x:x['provenance'].update(synthetic=False),
     'rights':lambda x:x['provenance'].update(rights='unknown'),
     'source':lambda x:x['provenance'].update(source_ref='unknown'),
     'snapshot':lambda x:x['provenance'].update(snapshot_sha256='0'*64),
     'profile':lambda x:x['profile'].update(sha256='0'*64),
     'extra-field':lambda x:x.update(counterfactual=True),
     'nodes-cap':lambda x:x['nodes'].extend([dict(id='n'+str(i),states=['0','1'],observed=True) for i in range(7)])}
    for name,change in mut.items():x=request();change(x);add(name,x,'rejected')
    graph_cases=[];names=['0','1','2','3'];possible=list(itertools.combinations(names,2))
    for mask in range(64):
        es=[list(e) for i,e in enumerate(possible) if mask&(1<<i)]
        for zmask in range(4):
            z=[str(i+1) for i in range(2) if zmask&(1<<i)];graph_cases.append(dict(nodes=names,edges=es,x='0',y='3',z=z,valid=backdoor_oracle(names,es,'0','3',z)))
    families={'confounding':['confounding','unblocked-confounding'],'mediation':['mediation','mediator-adjusted'],'collider-closed':['collider-closed'],'collider-conditioned':['collider-conditioned'],'collider-descendant':['collider-descendant'],'no-confounding':['no-confounding'],'descendant-adjustment':['mediator-adjusted'],'missing-positivity':['missing-positivity'],'zero-mass-stratum':['zero-mass-stratum'],'cycle-refusal':['cycle'],'unknown-edge':['unknown-edge'],'duplicate-edge':['duplicate-edge'],'exact-adjusted-risk':['confounding'],'observational-interventional-disagreement':['confounding'],'deterministic-intervention-oracle':['confounding','deterministic-intervention'],'joint-normalization':['unnormalized','missing-row','duplicate-row'],'graph-table-incompatibility':['incompatible'],'latent-graph-unsupported':['latent'],'canonical-order':['reordered'],'source-rights':['empirical','rights','source','snapshot'],'rational-bounds':['large-rational','float-weight','boolean-weight'],'json-markdown-replay':['profile','categorical']}
    out=dict(version=1,technique_id=56,profile_sha256=q['profile']['sha256'],families=families,cases=cases,graph_cases=graph_cases,structural_enumeration=struct,contrast_convention=dict(first_minus_last='-1/5',last_minus_first='1/5'),independence='Original structural exogenous enumeration for interventional answers; simple undirected path collider checks for graph cases; no production imports.')
    path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    freeze=dict(version=1,fixture_sha256=digest(out),oracle_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),fixture_families=len(families),graph_cases=len(graph_cases),accepted=sum(c['exit_code']==0 for c in cases.values()),rejected=sum(c['exit_code']==2 for c in cases.values()),structural_enumeration=struct)
    (R/'knowledge/causal_ai_fixture_freeze_v1.json').write_text(json.dumps(freeze,indent=2)+'\n',encoding='utf-8',newline='\n');print(freeze)
if __name__=='__main__':build()
