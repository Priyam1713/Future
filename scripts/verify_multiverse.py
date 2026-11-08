"""Frozen atom/leafset oracle compared with forward/backward production traversal."""
import copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from future.remote_viewing import digest
from future.scrying import load_input
R=Path(__file__).resolve().parents[1]
def fixture():
    f=load_input(R/'tests/fixtures/multiverse-independent-v1.json');fr=load_input(R/'knowledge/multiverse_fixture_freeze_v1.json');assert digest(f)==fr['fixture_sha256'] and not fr['production_exists'];assert hashlib.sha256((R/'scripts/multiverse_oracle.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==fr['oracle_sha256'];return f
def report(r,e):
    assert r['total_leaf_mass']==e['total_leaf_mass']=='1' and r['expected_utility']==e['expected_utility']
    nodes={n['id']:n for n in r['nodes']};leaves={n['id']:n for n in r['leaves']};assert {n:x['mass'] for n,x in leaves.items()}==e['leaves']
    for n,x in e['nodes'].items():
        assert nodes[n]['mass']==x['mass'] and nodes[n]['conditional_expected_utility']==x['conditional_expected_utility']
        if nodes[n]['children']:assert sum((F(nodes[c]['local_weight']) for c in nodes[n]['children']),F(0))==1
    for n,path in e['paths'].items():assert nodes[n]['path']==path
    assert sum((F(x['mass']) for x in leaves.values()),F(0))==1
    assert sum((F(x['mass'])*F(x['utility']) for x in leaves.values()),F(0))==F(r['expected_utility'])
    queries={x['id']:x for x in r['queries']}
    for name,x in e['queries'].items():assert {k:queries[name][k] for k in x}==x
    assert not r['universe_observations_used'] and not r['everett_empirically_validated'] and not r['empirical_forecast_accuracy_validated']
    q=copy.deepcopy(r);sha=q.pop('report_sha256');assert digest(q)==sha
def case(name):
    from future.multiverse import read
    c=fixture()['cases'][name];q=copy.deepcopy(c['input'])
    if c['exit_code']:
        try:read(q)
        except (ValueError,TypeError):return
        raise AssertionError('Expected rejection '+name)
    r=read(q);assert q==c['input'];report(r,c['expected'])
def vector(i):
    from future.multiverse import read
    v=fixture()['tree_vectors'][i];report(read(v['input']),v['expected'])
def atoms():
    from future.multiverse import read
    f=fixture();r=read(f['cases']['reference']['input']);a=f['equiprobable_atoms'];u=f['atom_utilities'];leaves={x['id']:F(x['mass']) for x in r['leaves']}
    assert {k:F(a.count(k),len(a)) for k in u}=={k:leaves[k] for k in u}
    assert sum((F(u[k],len(a)) for k in a),F(0))==F(r['expected_utility'])==1
    assert leaves['A1']==F(1,6) and leaves['Z']==0
    # Incorrect equal leaf weighting must disagree, especially with impossible Z.
    wrong=sum((F(n['utility']) for n in r['leaves']),F(0))/len(r['leaves']);assert wrong==26 and wrong!=F(r['expected_utility'])
def canonical():
    from future.multiverse import read
    f=fixture();assert read(f['cases']['reference']['input'])==read(f['cases']['permuted']['input'])
def run():
    f=fixture()
    for name in f['cases']:case(name)
    for i in range(len(f['tree_vectors'])):vector(i)
    atoms();canonical()
    additional={'complete-leaf-mass':'All reports exactleafsum1','expected-utility':'All reports bottom-upEU equalsindependent weightedleafsum','conditional-nested':'3136expandednodepairqueries andliteralnestedqueries','conditional-disjoint':'3136expandednodepairqueries andliteraldisjointqueries','impossible-condition':'Zero-conditionedqueries explicitlynull;notestimable','immutable-report':'Allreporthashes;callerinputunchanged','independent-atoms':'Sixequallylikelyatoms andequal-leaf negativecontrol'}
    families={name:dict(passed=True,cases=[n for n,c in f['cases'].items() if c['family']==name],additional_check=additional.get(name)) for name in f['families']};assert all(v['cases'] or v['additional_check'] for v in families.values())
    out=dict(passed=True,fixture_families=len(families),families=families,tree_vectors=len(f['tree_vectors']),expanded_conditional_queries=sum(len(v['input']['queries']) for v in f['tree_vectors']),equiprobable_atoms=6,accepted_cases=sum(c['exit_code']==0 for c in f['cases'].values()),rejected_cases=sum(c['exit_code']!=0 for c in f['cases'].values()),literal_anchors=f['literal_anchors'],negative_control='Equalleafutilityaverage26 disagreeswithproperweightedEU1',scope='Exactfinite genericprobability/utility software;no quantum-amplitude dynamics or Everett empiricalproof.')
    (R/'data/multiverse-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(str(len(families))+' independent families pass;64trees/3136conditionalqueries;6equiprobableatoms;canonicalorder andnegativecontrol pass')
if __name__=='__main__':run()
