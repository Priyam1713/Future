"""Bounded offline CPU statevector reference. No quantum advantage or QAE."""
import copy
import hashlib
import json
import math
from pathlib import Path
from .remote_viewing import digest, obj, integer, text
from .scrying import load_input

ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='abe755a144bf38b228ebbd0e6eb313b93405ff2d90fda75e1bcb2295196852dd'
PRNG='xorshift32-v1'
LIMITS=[
    'CPU classical emulation only;no QPU,GPU,cloud,Aer execution or quantum advantage.',
    'QAE,coherent oracle construction,variational and quantum-inspired algorithms are unimplemented.',
    'Ideal model probabilities,finite simulated frequencies and unknown real-world event probabilities are distinct.',
    'Known p is available directly without sampling;shared-stream identity is by construction,not superiority.',
    'Population moments assume independent identically prepared Bernoulli trials;PRNG emulates this model. No confidence interval or financial forecasting skill certified.',
    'Float64 libm results and exact JSON replay are scoped to the recorded runtime;cross-platform comparisons use1e-12 absolute tolerance.'
]
REFERENCES={
    'born':dict(source='quantum-prob-montanaro-v1',locator='Theorem2.2 and controlled rotation mapping',rule='a=<psi|P|psi>=sum_good |amplitude|^2;coefficient sqrt(p) differs from probability p.'),
    'ry':dict(source='quantum-prob-ibm-gates-v1',locator='RYGate matrix',rule='RY(theta)|0>=[cos(theta/2),sin(theta/2)];theta=2asin(sqrt(p)) requires known p.'),
    'bell':dict(source='quantum-prob-ibm-gates-v1',locator='Editorial composition of H and CX with IBM bit order',rule='Hq0 then CX0->1 gives (00+11)/sqrt(2);q0LSB.'),
    'montanaro':dict(source='quantum-prob-montanaro-v1',locator='Sections2a–2c;Theorems2.2,2.5',rule='Requires coherent A,inverse A,good projector and reflections. Error<=2pi sqrt(a(1-a))/t+pi^2/t^2;success>=8/pi^2. Median repetition boosts confidence. Query bounds are not CPU wall time.'),
    'variance':dict(source='quantum-prob-montanaro-v1',locator='Introduction classical sample mean;editorial Bernoulli specialization',rule='E[K]=Np;VarK=Np(1-p);Varfrequency=p(1-p)/N;SE=sqrt(Varfrequency).'),
    'risk':dict(source='quantum-prob-risk-v1',locator='2019npj journal article pp1–4;separate2018preprint',rule='Sum p_i f(i) is an expectation under supplied model probabilities;not learned unknown market probabilities. VaR/CVaR unimplemented.')
}


def assets():
    p=load_input(ROOT/'knowledge/quantum_probability_forecasting_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Profile integrity')
    for filename,key in [('quantum_probability_forecasting_sources.json','source_manifest_sha256'),('quantum_probability_forecasting_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/filename))!=p[key]:raise ValueError('Source integrity')
    return p


def request(task='simulate',qubits=1,gates=None,shots=None,seed=1,event=None,stream='common',comparator_seed=None,reference=None):
    """Construct a complete editable request;read still validates every field."""
    p=assets()
    return dict(schema_version=1,profile=dict(id=p['id'],sha256=PROFILE_HASH,catalog_sha256=p['source_manifest_sha256']),task=task,backend='standalone_cpu',circuit=dict(qubits=qubits,gates=gates or [],measurement=list(range(qubits))),shots=shots,rng=None if shots is None else dict(algorithm=PRNG,seed=seed,comparator_seed=seed if comparator_seed is None else comparator_seed,stream=stream),event=event or dict(kind='qubit_one',value=0),reference=reference,provenance=dict(source_ref='quantum-prob-ibm-gates-v1',rights='self_authored',attribution='Original user-supplied circuit;IBM gate conventions.'))


def validate(q,p):
    obj(q,p['schema']['root']);integer(q['schema_version'],1,1)
    obj(q['profile'],('id','sha256','catalog_sha256'))
    if q['profile']!=dict(id=p['id'],sha256=PROFILE_HASH,catalog_sha256=p['source_manifest_sha256']):raise ValueError('Identity mismatch')
    if q['backend']!='standalone_cpu' or q['task'] not in p['schema']['tasks']:raise ValueError('Unsupported capability')
    c=q['circuit'];obj(c,('qubits','gates','measurement'));n=integer(c['qubits'],1,4)
    if not isinstance(c['measurement'],list) or any(type(x) is not int for x in c['measurement']) or c['measurement']!=list(range(n)):raise ValueError('Measurement mapping')
    if not isinstance(c['gates'],list) or len(c['gates'])>64:raise ValueError('Gate count')
    for g in c['gates']:
        if not isinstance(g,dict) or g.get('op') not in p['gate_allowlist']:raise ValueError('Unsupported gate')
        op=g['op'];obj(g,('op','target','angle') if op=='ry' else ('op','target','control') if op=='cx' else ('op','target'))
        integer(g['target'],0,n-1)
        if op=='cx' and integer(g['control'],0,n-1)==g['target']:raise ValueError('CX identical wires')
        if op=='ry' and (type(g['angle']) not in (int,float) or not math.isfinite(g['angle']) or abs(g['angle'])>1000000):raise ValueError('Angle')
    e=q['event'];obj(e,('kind','value'))
    if e['kind']=='qubit_one':integer(e['value'],0,n-1)
    elif e['kind']=='bitstring':
        if not isinstance(e['value'],str) or len(e['value'])!=n or set(e['value'])-{'0','1'}:raise ValueError('Event bitstring')
    else:raise ValueError('Event kind')
    if q['task'] in ('simulate','reference') and q['shots'] is not None:raise ValueError('Unexpected shots')
    if q['task'] in ('sample','compare') and q['shots'] is None:raise ValueError('Shots required')
    if q['shots'] is None:
        if q['rng'] is not None:raise ValueError('Unexpected RNG')
    else:
        integer(q['shots'],1,100000);r=q['rng'];obj(r,('algorithm','seed','comparator_seed','stream'))
        if r['algorithm']!=PRNG or r['stream'] not in ('common','independent'):raise ValueError('RNG policy')
        integer(r['seed'],1,4294967295);integer(r['comparator_seed'],1,4294967295)
        if (r['seed']==r['comparator_seed'])!=(r['stream']=='common'):raise ValueError('Stream identity')
    if q['task']=='reference':
        if q['reference'] not in REFERENCES:raise ValueError('Reference ID')
    elif q['reference'] is not None:raise ValueError('Unexpected reference')
    v=q['provenance'];obj(v,('source_ref','rights','attribution'))
    sources=load_input(ROOT/'knowledge/quantum_probability_forecasting_sources.json')
    if v['source_ref'] not in [s['id'] for s in sources] or v['rights'] not in ('self_authored','permission_granted') or not text(v['attribution'],2000).strip():raise ValueError('Rights/provenance required')


def evolve(n,gates):
    """Complex amplitude pair updates;callers supply a validated circuit."""
    a=[0j]*(1<<n);a[0]=1+0j;depth=[0]*n;counts={op:0 for op in ('id','x','h','ry','cx')};trace=[]
    for g in gates:
        op=g['op'];t=g['target'];bit=1<<t;counts[op]+=1
        wires=[t,g['control']] if op=='cx' else [t];d=max(depth[w] for w in wires)+1
        for w in wires:depth[w]=d
        if op=='cx':
            ctrl=1<<g['control']
            for i in range(len(a)):
                if i&ctrl and not i&bit:a[i],a[i|bit]=a[i|bit],a[i]
        elif op!='id':
            if op=='x':m=(0,1,1,0)
            elif op=='h':h=1/math.sqrt(2);m=(h,h,h,-h)
            else:c=math.cos(g['angle']/2);s=math.sin(g['angle']/2);m=(c,-s,s,c)
            for i in range(len(a)):
                if not i&bit:
                    x,y=a[i],a[i|bit];a[i]=m[0]*x+m[1]*y;a[i|bit]=m[2]*x+m[3]*y
        norm=math.fsum(z.real*z.real+z.imag*z.imag for z in a)
        if abs(norm-1)>1e-12:raise ValueError('State normalization')
        trace.append(dict(gate=copy.deepcopy(g),depth=d,norm=norm))
    return a,dict(qubits=n,dimension=len(a),primitive_gates=len(gates),depth=max(depth),gate_counts=counts,measurement=list(range(n)),precision='complex binary64',statevector_payload_bytes=16*len(a),python_overhead_excluded=True,ae_oracle_calls=None,qae_implemented=False,runtime_memory_measurement='Separate resource measurements artifact;no variable timing in deterministic report.'),trace


def uniforms(seed,count):
    for _ in range(count):
        seed^=(seed<<13)&0xffffffff;seed^=seed>>17;seed^=(seed<<5)&0xffffffff;seed&=0xffffffff
        yield seed/4294967296.0


def indices(n,e):
    return [i for i in range(1<<n) if (i&(1<<e['value'])!=0 if e['kind']=='qubit_one' else format(i,f'0{n}b')==e['value'])]


def sample(prob,good,shots,seed):
    norm=math.fsum(prob);order=good+[i for i in range(len(prob)) if i not in good]
    # fsum prefixes fixes the event boundary identically to Bernoulli p.
    cdf=[math.fsum(prob[j] for j in order[:k+1])/norm for k in range(len(order))]
    last=next(i for i in reversed(order) if prob[i]>0);counts=[0]*len(prob)
    for u in uniforms(seed,shots):
        selected=last
        for i,bound in zip(order,cdf):
            if u<bound:selected=i;break
        counts[selected]+=1
    return counts


def bernoulli(p,shots,seed):return sum(u<p for u in uniforms(seed,shots))


def moments(p,n):
    return dict(expected_count=n*p,count_variance=n*p*(1-p),frequency_variance=p*(1-p)/n,frequency_standard_error=math.sqrt(p*(1-p)/n),confidence_interval=None,assumptions='iid identical preparations under ideal supplied model;population moments,not observed uncertainty validation')


def read(q,registry=None):
    p=assets();validate(q,p);q=copy.deepcopy(q)
    sources=load_input(ROOT/'knowledge/quantum_probability_forecasting_sources.json')
    if registry is not None:
        for s in sources:registry.add_source(s)
    n=q['circuit']['qubits'];a,res,trace=evolve(n,q['circuit']['gates']);probs=[z.real*z.real+z.imag*z.imag for z in a];norm=math.fsum(probs);good=indices(n,q['event']);event_p=math.fsum(probs[i] for i in good)/norm
    result=dict(statevector=[dict(index=i,bitstring=format(i,f'0{n}b'),real=z.real,imag=z.imag,probability=probs[i]) for i,z in enumerate(a)],normalization=dict(norm=norm,error=abs(norm-1),tolerance=1e-12,passed=abs(norm-1)<=1e-12,sampling_norm_divisor=norm),event=dict(predicate=q['event'],indices=good,ideal_model_probability=event_p),trace=trace,resources=res,sampling=None,classical=None,reference=copy.deepcopy(REFERENCES[q['reference']]) if q['task']=='reference' else None)
    if q['shots'] is not None:
        shots=q['shots'];r=q['rng'];cs=sample(probs,good,shots,r['seed']);k=sum(cs[i] for i in good)
        result['sampling']=dict(shots=shots,rng=r,count_total=sum(cs),outcomes=[dict(index=i,bitstring=format(i,f'0{n}b'),count=v,frequency=v/shots,absolute_error=abs(v/shots-probs[i]/norm)) for i,v in enumerate(cs)],event_count=k,event_frequency=k/shots,event_absolute_error=abs(k/shots-event_p),analytical=moments(event_p,shots))
        if q['task'] in ('compare','report'):
            b=bernoulli(event_p,shots,r['comparator_seed'])
            result['classical']=dict(known_p=event_p,known_p_exact_model_answer_available_without_sampling=True,shots=shots,count=b,frequency=b/shots,absolute_error=abs(b/shots-event_p),rng_algorithm=PRNG,seed=r['comparator_seed'],stream=r['stream'],shared_identity_by_construction=r['stream']=='common',quantum_advantage=False,analytical=moments(event_p,shots))
    out=dict(status='accepted',task=q['task'],profile=q['profile'],request=q,request_sha256=digest(q),sources=sources,source_freeze_sha256=p['source_freeze_sha256'],bit_order=p['indexing'],result=result,code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),limits=list(LIMITS))
    out['report_sha256']=digest(out);return out


def markdown(r):
    payload=json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)
    fence='`'*max(3,max((len(x) for x in __import__('re').findall(r'`+',payload)),default=0)+1)
    lines=['# Quantum Probability Reference', '', 'Status: '+r['status'], '']
    if r['status']=='accepted':
        lines+=['| Basis | Amplitude (real, imaginary) | Ideal probability |','|---|---|---|']+[f"| {s['bitstring']} | ({s['real']}, {s['imag']}) | {s['probability']} |" for s in r['result']['statevector']]
        lines+=['',*r['limits'],'']
    return '\n'.join(lines+[fence+'json',payload,fence,''])
