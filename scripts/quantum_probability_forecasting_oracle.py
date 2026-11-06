"""Independent pre-engine dense-matrix oracle. No Future engine imports."""
import math
import json
from pathlib import Path


def reference(n, gates):
    # Full matrix element construction, independently of production pair updates.
    d=2**n; state=[complex(i==0) for i in range(d)]
    for g in gates:
        t=g['target']; op=g['op']; matrix=[[0j]*d for _ in range(d)]
        if op=='cx':
            for j in range(d):
                bits=list(format(j,f'0{n}b'))
                if bits[n-1-g['control']]=='1': bits[n-1-t]='1' if bits[n-1-t]=='0' else '0'
                matrix[int(''.join(bits),2)][j]=1
        else:
            c=math.cos(g.get('angle',0)/2); s=math.sin(g.get('angle',0)/2)
            m={'id':[[1,0],[0,1]],'x':[[0,1],[1,0]],'h':[[2**-.5,2**-.5],[2**-.5,-2**-.5]],'ry':[[c,-s],[s,c]]}[op]
            for i in range(d):
                for j in range(d):
                    a=format(i,f'0{n}b'); b=format(j,f'0{n}b')
                    if all(a[k]==b[k] for k in range(n) if k!=n-1-t):matrix[i][j]=m[int(a[n-1-t])][int(b[n-1-t])]
        state=[sum(matrix[i][j]*state[j] for j in range(d)) for i in range(d)]
    return [[z.real,z.imag] for z in state]


def words(seed, count):
    # Masking follows each elementary unsigned operation; no library PRNG.
    out=[]
    for _ in range(count):
        seed=(seed ^ (seed*8192)%4294967296)%4294967296
        seed=seed ^ (seed//131072)
        seed=(seed ^ (seed*32)%4294967296)%4294967296
        out.append(seed)
    return out


def build():
    cases=[]
    def add(name,n,g,expected=None):
        state=reference(n,g)
        if expected is not None:assert all(abs(a-b)<1e-14 for x,y in zip(state,expected) for a,b in zip(x,y))
        cases.append(dict(id=name,qubits=n,gates=g,state=expected if expected is not None else state,provenance='original algebraic anchor' if expected is not None else 'independent full dense matrix multiplication frozen before engine'))
    gate=lambda op,t=0,**kw:dict(op=op,target=t,**kw)
    add('zero',1,[],[[1,0],[0,0]])
    add('identity',1,[gate('id')],[[1,0],[0,0]])
    add('one',1,[gate('x')],[[0,0],[1,0]])
    add('xx',1,[gate('x'),gate('x')],[[1,0],[0,0]])
    r=math.sqrt(.5)
    add('h0',1,[gate('h')],[[r,0],[r,0]])
    add('h1',1,[gate('x'),gate('h')],[[r,0],[-r,0]])
    add('hh',1,[gate('h'),gate('h')],[[1,0],[0,0]])
    for name,a,ex in [('ry0',0,[[1,0],[0,0]]),('rythird',math.pi/3,[[math.sqrt(3)/2,0],[.5,0]]),('ryhalf',math.pi/2,[[r,0],[r,0]]),('rypi',math.pi,[[0,0],[1,0]]),('rynegative',-math.pi/3,[[math.sqrt(3)/2,0],[-.5,0]])]:add(name,1,[gate('ry',angle=a)],ex)
    add('bell',2,[gate('h'),gate('cx',1,control=0)],[[r,0],[0,0],[0,0],[r,0]])
    add('reversed-bell',2,[gate('h'),gate('cx',0,control=1)],[[r,0],[r,0],[0,0],[0,0]])
    add('endian',2,[gate('x',1)],[[0,0],[0,0],[1,0],[0,0]])
    for n in range(1,5):
        for t in range(n):
            for op in ('id','x','h','ry'):
                gs=[gate('x',t),gate(op,t,**({'angle':.731} if op=='ry' else {}))]
                add(f'primitive-{n}-{t}-{op}',n,gs)
        if n>1:
            for c in range(n):
                for t in range(n):
                    if c!=t:add(f'cx-{n}-{c}-{t}',n,[gate('x',c),gate('cx',t,control=c)])
        gs=[]
        for k in range(64):
            t=k%n;op=('h','ry','x','id')[k%4]
            gs.append(gate(op,t,**({'angle':(-1)**k*.13*k} if op=='ry' else {})))
        if n>1:gs[-1]=gate('cx',n-1,control=0)
        add(f'composition64-{n}',n,gs)
    assert words(1,5)==[270369,67634689,2647435461,307599695,2398689233]
    return dict(version=1,oracle='pre-production dense matrices and symbolic anchors;no engine invocation',circuits=cases,prng={str(s):words(s,100) for s in (1,2,4294967295)},dyadic_counts={str(s):{str(p):sum(w<int(p*2**32) for w in words(s,100)) for p in (0,.25,.5,1)} for s in (1,2,4294967295)},binomial=dict(p='1/4',shots=100,expected_count='25',count_variance='75/4',frequency_variance='3/1600',standard_error='sqrt(3)/40'),nonmonotone=dict(uniforms=['1/4','3/4','1/4'],p='1/2',counts=[1,2],shots=[2,3],errors=['0','1/6']),family_expectations={name:desc for name,desc in zip(json.loads(Path('knowledge/quantum_probability_forecasting_profile_v1.json').read_text())['fixture_families'],['algebraic basis and X twice','signed H0/H1','RY symbolic anchors and negative sign','norm1 through64gates','exact X/identity shot endpoints','exact independent100word seeds','exact rational binomial moments','controlled uniforms worsen2to3','ideal values distinct from observed','Bell2gates depth2;parallel gates depth1','reject bool/nonfinite/oversize angles','reject Aer/GPU/QPU','Xq1 index2','same p,N;shared identity;distinct streams','iid assumption;CI null','no advantage claim;AE absent','reject missing rights/hash;reference assumptions','CLI saved JSON/MD with Unicode raw hash','HH identity probability-only negative control','Bell and reversed control signed matrices'])})

if __name__=='__main__':
    path=Path('tests/fixtures/quantum_probability_forecasting_reference_v1.json')
    path.write_text(json.dumps(build(),indent=2)+'\n',encoding='utf-8',newline='\n')
    print('independent circuits',len(build()['circuits']))
