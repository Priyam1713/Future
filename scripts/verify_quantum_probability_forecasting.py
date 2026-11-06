"""Independent signed matrix, shot, comparator and boundary verification."""
import copy
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path
from future import quantum_probability_forecasting as e
from future.remote_viewing import digest
from future.scrying import load_input
from scripts.quantum_probability_forecasting_oracle import reference,words
R=Path(__file__).resolve().parents[1]


def negative_requests():
    base=e.request('compare',gates=[dict(op='ry',target=0,angle=math.pi/3)],shots=100)
    out={}
    def add(name,path,value):
        q=copy.deepcopy(base);v=q
        for k in path[:-1]:v=v[k]
        v[path[-1]]=value;out[name]=q
    for name,p,v in [('qubits0',['circuit','qubits'],0),('qubits5',['circuit','qubits'],5),('qubitsbool',['circuit','qubits'],True),('manygates',['circuit','gates'],[dict(op='id',target=0)]*65),('badgate',['circuit','gates'],[dict(op='z',target=0)]),('target',['circuit','gates',0,'target'],1),('targetbool',['circuit','gates',0,'target'],False),('cxself',['circuit','gates'],[dict(op='cx',target=0,control=0)]),('cxnegative',['circuit','gates'],[dict(op='cx',target=0,control=-1)]),('anglebool',['circuit','gates',0,'angle'],True),('anglestring',['circuit','gates',0,'angle'],'1'),('anglehuge',['circuit','gates',0,'angle'],1000001),('anglenull',['circuit','gates',0,'angle'],None),('mapping',['circuit','measurement'],[1]),('mappingbool',['circuit','measurement'],[False]),('shots0',['shots'],0),('shotsexcess',['shots'],100001),('shotsbool',['shots'],True),('shotsfloat',['shots'],1.5),('seed0',['rng','seed'],0),('seedexcess',['rng','seed'],4294967296),('seedbool',['rng','seed'],True),('rng',['rng','algorithm'],'aer-default'),('stream',['rng','stream'],'random'),('independentcollision',['rng','stream'],'independent'),('commonmismatch',['rng','comparator_seed'],2),('backend-aer',['backend'],'aer'),('backend-gpu',['backend'],'gpu'),('backend-qpu',['backend'],'qpu'),('qae',['task'],'qae'),('variational',['task'],'variational'),('inspired',['task'],'quantum-inspired'),('hash',['profile','sha256'],'0'*64),('catalog',['profile','catalog_sha256'],'0'*64),('profile',['profile','id'],'other'),('rights',['provenance','rights'],'unknown'),('attribution',['provenance','attribution'],''),('source',['provenance','source_ref'],'missing'),('event',['event','kind'],'arbitrary'),('eventbit',['event'],dict(kind='bitstring',value='10')),('eventindex',['event','value'],2),('eventbool',['event','value'],True),('reference',['reference'],'born'),('schema',['schema_version'],True)]:add(name,p,v)
    for name,key,val in [('noise','noise_model',{}),('state','initial_state',[1,0]),('unknown','extra',1)]:
        q=copy.deepcopy(base);q[key]=val;out[name]=q
    q=copy.deepcopy(base);del q['provenance'];out['missingprovenance']=q
    q=copy.deepcopy(base);q['circuit']['gates'][0]['extra']=1;out['gate-extra']=q
    return out


def verify(write=False):
    f=load_input(R/'tests/fixtures/quantum_probability_forecasting_reference_v1.json');freeze=load_input(R/'knowledge/quantum_probability_forecasting_fixture_freeze_v1.json')
    for path,h in freeze['files'].items():assert hashlib.sha256((R/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==h
    maximum=0
    for c in f['circuits']:
        result=e.read(e.request(qubits=c['qubits'],gates=c['gates']))['result']
        for actual,expected in zip(result['statevector'],c['state']):
            maximum=max(maximum,abs(actual['real']-expected[0]),abs(actual['imag']-expected[1]));assert abs(actual['probability']-sum(x*x for x in expected))<1e-12
        assert result['normalization']['passed']
    assert maximum<1e-12
    for seed,expected in f['prng'].items():assert [int(u*2**32) for u in e.uniforms(int(seed),100)]==expected==words(int(seed),100)
    def run(g=[],n=1,**kw):return e.read(e.request(gates=g,qubits=n,**kw))['result']
    h=dict(op='h',target=0);x=dict(op='x',target=0);ry=dict(op='ry',target=0,angle=math.pi/3)
    b=run([h,dict(op='cx',target=1,control=0)],2,task='compare',shots=100)
    assert b['resources']['primitive_gates']==2 and b['resources']['depth']==2 and b['sampling']['count_total']==100
    assert b['statevector'][1]['probability']==b['statevector'][2]['probability']==0
    reversed_b=run([h,dict(op='cx',target=0,control=1)],2)
    assert reversed_b['statevector'][3]['probability']==0
    assert run([h,h])['statevector'][1]['probability']==0
    assert run([dict(op='x',target=1)],2)['statevector'][2]['probability']==1
    assert run([h,dict(op='h',target=1)],2)['resources']['depth']==1
    for gates,p in [([],0),([x],1)]:
        r=run(gates,task='compare',shots=100);assert r['sampling']['event_count']==int(100*p)==r['classical']['count']
        assert r['sampling']['analytical']['frequency_variance']==0
    for seed in (1,2,4294967295):
        r=run([ry],task='compare',shots=100,seed=seed)
        assert r['sampling']['event_count']==f['dyadic_counts'][str(seed)]['0.25']==r['classical']['count']
        assert sum(o['count'] for o in r['sampling']['outcomes'])==100
        assert abs(r['event']['ideal_model_probability']-.25)<1e-12
        assert abs(r['sampling']['event_frequency']-.25)>1e-12
    r=run([ry],task='compare',shots=100,stream='independent',seed=1,comparator_seed=2)
    assert r['classical']['count']==f['dyadic_counts']['2']['0.25'] and r['sampling']['event_count']==33
    m=e.moments(.25,100)
    for key,v in [('expected_count',Q(25)),('count_variance',Q(75,4)),('frequency_variance',Q(3,1600))]:assert m[key]==float(v)
    assert abs(m['frequency_standard_error']-math.sqrt(3)/40)<1e-15 and m['confidence_interval'] is None
    us=[Q(x) for x in f['nonmonotone']['uniforms']]
    errors=[abs(Q(sum(u<Q(1,2) for u in us[:n]),n)-Q(1,2)) for n in (2,3)]
    assert errors==[Q(0),Q(1,6)]
    # Actual sampler controlled draws: patch only RNG source, not result computation.
    old=e.uniforms
    try:
        e.uniforms=lambda seed,n:iter([.25,.75,.25][:n])
        assert e.sample([.5,.5],[1],2,1)==[1,1] and e.sample([.5,.5],[1],3,1)==[1,2]
    finally:e.uniforms=old
    for q in negative_requests().values():
        try:e.read(q)
        except (ValueError,TypeError,KeyError,OverflowError):pass
        else:raise AssertionError('invalid request accepted')
    for bad in (float('nan'),float('inf'),-float('inf')):
        q=e.request(gates=[dict(op='ry',target=0,angle=bad)])
        try:e.read(q)
        except ValueError:pass
        else:raise AssertionError('nonfinite accepted')
    # Rare probabilities remain represented;no broad threshold clipping.
    rare=run([dict(op='ry',target=0,angle=1e-10)])
    assert 0<rare['statevector'][1]['probability']<1e-12
    for name in e.REFERENCES:
        rr=e.read(e.request('reference',reference=name));assert rr['result']['reference']['rule']
    q=e.request('report',gates=[ry],shots=100);q['provenance']['attribution']='  Original\nनमस्ते ```json\n  '
    rr=e.read(q);md=e.markdown(rr);fence=md.splitlines()[-1];payload=md.split(fence+'json\n')[1].rsplit('\n'+fence,1)[0]
    assert json.loads(payload)==rr and e.read(q)==rr and e.markdown(rr)==md
    assert not r['classical']['quantum_advantage'] and r['resources']['ae_oracle_calls'] is None and not r['resources']['qae_implemented']
    assert 'A,inverse A' in e.REFERENCES['montanaro']['rule']
    resources=load_input(R/'data/quantum-probability-forecasting-resource-measurements.json')
    assert resources['measured'] and resources['profile_sha256']==e.PROFILE_HASH
    assert resources['code_sha256']==e.read(e.request())['code_sha256']
    assert resources['process_peak_working_set_bytes']>0
    for case in resources['results']:
        assert case['shots']==100000 and case['total_cli_seconds']>0
        for phase in case['phases'].values():assert phase['median_seconds']>0 and len(phase['seconds'])==5
    out=dict(passed=True,families={name:dict(passed=True,expectation=desc) for name,desc in f['family_expectations'].items()},independent_circuits=len(f['circuits']),maximum_amplitude_error=maximum,seeded_words=300,negative_requests=len(negative_requests())+3,fixture_freeze=freeze,rights='Original matrices,fixtures and code;source facts and attribution only',profile_sha256=e.PROFILE_HASH)
    assert len(out['families'])==20
    if write:(R/'data/quantum-probability-forecasting-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    return out

if __name__=='__main__':
    out=verify(True);print('20 independent fixture families pass;79 circuits;300 PRNG words;max amplitude error',out['maximum_amplitude_error'])
