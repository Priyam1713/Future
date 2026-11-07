"""Pre-engine leaf-parent path products and leaf-set intersections, no engine imports."""
import copy,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def save(p,x):(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def node(i,parent,weight,utility=None):return dict(id=i,parent=parent,weight=weight,utility=utility)
def request():
    p=json.loads((R/'knowledge/multiverse_profile_v1.json').read_text(encoding='utf-8'));snapshot='Self-authored finite educational editorial scenario; no universe observations.'
    return dict(schema_version=1,profile=dict(id=p['id'],version=1,sha256=digest(p),catalog_sha256=p['source_manifest_sha256']),scenario=dict(id='toy-scenario',version=1,kind='educational_editorial_weights',exhaustive=True,description='Fictional branches with declared utilities.'),nodes=[node('R',None,'1'),node('A','R','1/2'),node('B','R','1/2','2'),node('Z','R','0','99'),node('A1','A','1/3','6'),node('A2','A','2/3','-3')],queries=[dict(id='q'+str(k),given=g,target=t) for k,(g,t) in enumerate([('R','A1'),('A','A1'),('A1','A'),('A','B'),('Z','R'),('R','Z'),('R','R'),('A1','A1')])],provenance=dict(synthetic=True,source_ref='multiverse-mit-multiplication-v1',rights='self_authored',attribution='Original synthetic scenario author',snapshot=snapshot,snapshot_sha256=hashlib.sha256(snapshot.encode()).hexdigest()))
def expected(q):
    by={n['id']:n for n in q['nodes']};parents={n['parent'] for n in q['nodes'] if n['parent'] is not None};leaves=sorted(set(by)-parents);paths={};leafmasses={}
    for leaf in leaves:
        path=[];current=leaf;mass=F(1)
        while current is not None:path.append(current);mass*=F(by[current]['weight']);current=by[current]['parent']
        paths[leaf]=list(reversed(path));leafmasses[leaf]=mass
    sets={n:{leaf for leaf,path in paths.items() if n in path} for n in by};mass=lambda leaves:sum((leafmasses[n] for n in leaves),F(0))
    nodes={n:dict(mass=str(mass(leaves)),conditional_expected_utility=str(sum((leafmasses[l]*F(by[l]['utility']) for l in leaves),F(0))/mass(leaves)) if mass(leaves) else None) for n,leaves in sets.items()}
    queries={x['id']:dict(intersection_mass=str(mass(sets[x['given']]&sets[x['target']])),probability=str(mass(sets[x['given']]&sets[x['target']])/mass(sets[x['given']])) if mass(sets[x['given']]) else None,status='estimated_exact_model' if mass(sets[x['given']]) else 'not_estimable_zero_condition') for x in q['queries']}
    return dict(nodes=nodes,leaves={n:str(leafmasses[n]) for n in leaves},paths=paths,total_leaf_mass=str(sum(leafmasses.values(),F(0))),expected_utility=str(sum((leafmasses[n]*F(by[n]['utility']) for n in leaves),F(0))),queries=queries)
FAMILIES=['root-normalization','local-normalization','path-products','complete-leaf-mass','expected-utility','negative-utilities','zero-weight-branches','conditional-nested','conditional-disjoint','impossible-condition','single-root-leaf','deterministic-branches','canonical-order','unique-identities','acyclic-tree','complete-terminal-outcomes','rational-validation','unsupported-physics','depth-bounds','resource-bounds','source-rights','snapshot-binding','immutable-report','independent-atoms']
def build():
    path=R/'tests/fixtures/multiverse-independent-v1.json'
    if path.exists():raise ValueError('Immutable fixtures already exist')
    cases={}
    def add(name,q,code,family):cases[name]=dict(input=q,exit_code=code,family=family,expected=expected(q) if code==0 else None)
    q=request();add('reference',q,0,'path-products')
    q=request();q['nodes'].reverse();q['queries'].reverse();add('permuted',q,0,'canonical-order')
    q=request();q['queries']=[];add('no-queries',q,0,'resource-bounds')
    q=request();q['nodes']=[node('R',None,'1','-7')];q['queries']=[dict(id='q',given='R',target='R')];add('single-leaf',q,0,'single-root-leaf')
    q=request();q['nodes']=[node('R',None,'1'),node('yes','R','1','-4'),node('no','R','0','100')];q['queries']=[dict(id='q',given='no',target='yes')];add('deterministic',q,0,'deterministic-branches')
    q=request();q['nodes']=[node('n'+str(i),'n'+str(i-1) if i else None,'1','-1' if i==32 else None) for i in range(33)];q['queries']=[dict(id='q',given='n32',target='n0')];add('depth-limit',q,0,'depth-bounds')
    q=request();q['nodes']=[node('R',None,'1')]+[node('n'+str(i),'R','1/255',str(i-127)) for i in range(255)];q['queries']=[dict(id='q'+str(i),given='R',target='n'+str(i%255)) for i in range(256)];add('size-limit',q,0,'resource-bounds')
    q=request();q['nodes'][4]['utility']='-6';add('negative-utility',q,0,'negative-utilities')
    q=request();q['nodes'][1]['weight']='0';q['nodes'][2]['weight']='1';add('zero-parent-normalized',q,0,'zero-weight-branches')
    def bad(name,section,key,value,family):
        q=request()
        if section=='node':q['nodes'][key[0]][key[1]]=value
        elif section:q[section][key]=value
        else:q[key]=value
        add(name,q,2,family)
    for name,section,key,value,family in [('root-weight','node',(0,'weight'),'1/2','root-normalization'),('local-sum','node',(1,'weight'),'1/3','local-normalization'),('negative-weight','node',(1,'weight'),'-1/2','rational-validation'),('weight-above-one','node',(1,'weight'),'2','rational-validation'),('float-weight','node',(1,'weight'),0.5,'rational-validation'),('bool-weight','node',(1,'weight'),True,'rational-validation'),('nonfinite-weight','node',(1,'weight'),'Infinity','rational-validation'),('zero-denominator','node',(1,'weight'),'1/0','rational-validation'),('decimal-weight','node',(1,'weight'),'0.5','rational-validation'),('long-weight','node',(1,'weight'),'1'*50,'rational-validation'),('utility-large','node',(4,'utility'),'1000001','rational-validation'),('utility-missing','node',(4,'utility'),None,'complete-terminal-outcomes'),('internal-utility','node',(1,'utility'),'0','complete-terminal-outcomes'),('unknown-parent','node',(1,'parent'),'unknown','acyclic-tree'),('self-parent','node',(1,'parent'),'A','acyclic-tree'),('second-root','node',(1,'parent'),None,'acyclic-tree'),('duplicate-node','node',(2,'id'),'A','unique-identities'),('invalid-id','node',(2,'id'),'bad id','unique-identities'),('no-nodes',None,'nodes',[],'resource-bounds'),('bad-nodes',None,'nodes',{},'resource-bounds'),('kind','scenario','kind','Born_rule_amplitudes','unsupported-physics'),('not-exhaustive','scenario','exhaustive',False,'complete-terminal-outcomes'),('scenario-version','scenario','version',True,'immutable-report'),('empty-description','scenario','description','','source-rights'),('profile-hash','profile','sha256','0'*64,'immutable-report'),('catalog-hash','profile','catalog_sha256','0'*64,'source-rights'),('source','provenance','source_ref','unknown','source-rights'),('rights','provenance','rights','unknown','source-rights'),('synthetic','provenance','synthetic',False,'unsupported-physics'),('snapshot','provenance','snapshot_sha256','0'*64,'snapshot-binding'),('attribution','provenance','attribution','','source-rights'),('schema-version',None,'schema_version',True,'immutable-report'),('amplitudes',None,'amplitudes',['1','0'],'unsupported-physics')]:bad(name,section,key,value,family)
    q=request();q['queries'][0]['given']='unknown';add('unknown-given',q,2,'conditional-nested')
    q=request();q['queries'][0]['target']='unknown';add('unknown-target',q,2,'conditional-disjoint')
    q=request();q['queries'][1]['id']=q['queries'][0]['id'];add('duplicate-query',q,2,'unique-identities')
    q=request();q['nodes'][1]['parent']='A1';add('cycle',q,2,'acyclic-tree')
    q=request();q['nodes'][1]['weight']='0';q['nodes'][2]['weight']='1';q['nodes'][4]['weight']='1/2';add('zero-parent-incomplete',q,2,'local-normalization')
    q=request();q['nodes']=[node('n'+str(i),'n'+str(i-1) if i else None,'1','0' if i==33 else None) for i in range(34)];add('depth-over',q,2,'depth-bounds')
    q=request();q['nodes']*=43;add('nodes-over',q,2,'resource-bounds')
    q=request();q['queries']*=33;add('queries-over',q,2,'resource-bounds')
    vectors=[]
    for a,b,c in itertools.product([F(0),F(1,3),F(1,2),F(1)],repeat=3):
        q=request();q['nodes']=[node('R',None,'1'),node('L','R',str(a)),node('D','R',str(1-a)),node('L0','L',str(b),'-2'),node('L1','L',str(1-b),'3'),node('D0','D',str(c),'7'),node('D1','D',str(1-c),'-5')];ids=[n['id'] for n in q['nodes']];q['queries']=[dict(id=g+'_'+t,given=g,target=t) for g,t in itertools.product(ids,repeat=2)];vectors.append(dict(input=q,expected=expected(q)))
    atoms=['A1','A2','A2','B','B','B'];reference=expected(request());assert reference['leaves']==dict(A1='1/6',A2='1/3',B='1/2',Z='0') and reference['expected_utility']=='1'
    utilities={'A1':6,'A2':-3,'B':2};assert sum(utilities[a] for a in atoms)==6
    f=dict(version=1,technique_id=60,families=FAMILIES,cases=cases,tree_vectors=vectors,equiprobable_atoms=atoms,atom_utilities=utilities,literal_anchors=dict(path_mass='1/6',expected_utility='1',conditional_A1_given_A='1/3',conditional_A_given_A1='1',disjoint='0',zero_condition=None));save(path.relative_to(R),f)
    save('knowledge/multiverse_fixture_freeze_v1.json',dict(version=1,technique_id=60,fixture_sha256=digest(f),oracle_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),families=FAMILIES,production_exists=(R/'future/multiverse.py').exists(),independent_method='Exactleaf-parentproduct/leafsetintersections;independent sixequiprobableatoms;64trees/all3136nodepairqueries.'))
    print(len(cases),'cases',len(vectors),'trees',len(FAMILIES),'families')
if __name__=='__main__':build()
