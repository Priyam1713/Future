"""Pre-engine sparse Counter/set oracle; no production imports."""
from collections import Counter
import copy,hashlib,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def grid(h,w,live=()):return [[int((r,c) in live) for c in range(w)] for r in range(h)]
def request(board=None,ticks=2,trace=True):
    board=board if board is not None else [[0,0,0],[1,1,1],[0,0,0]];p=json.loads((R/'knowledge/agent_based_profile_v1.json').read_text(encoding='utf-8'));snapshot='Original explicit synthetic binary board; no observed people or assets.'
    return dict(schema_version=1,profile=dict(id=p['id'],version=1,sha256=digest(p),catalog_sha256=p['source_manifest_sha256']),model=dict(p['model']),geometry=dict(height=len(board),width=len(board[0])),ticks=ticks,trace_states=trace,scenarios=[dict(id='base',initial_grid=board)],reference_scenario='base',provenance=dict(synthetic=True,source_ref='agent-based-mesa-life-agents-v1',rights='self_authored',attribution='Future original synthetic Life fixture',snapshot=snapshot,snapshot_sha256=hashlib.sha256(snapshot.encode()).hexdigest()))
def oracle(q):
    h,w=q['geometry']['height'],q['geometry']['width'];out={}
    for s in q['scenarios']:
        live={(r,c) for r in range(h) for c in range(w) if s['initial_grid'][r][c]};states=[grid(h,w,live)];rows=[dict(alive=len(live),dead=h*w-len(live),births=None,deaths=None)];cycle=None
        for tick in range(1,q['ticks']+1):
            counts=Counter()
            for r,c in live:
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if (dr or dc) and 0<=r+dr<h and 0<=c+dc<w:counts[r+dr,c+dc]+=1
            following={position for position,n in counts.items() if n==3 or n==2 and position in live};state=grid(h,w,following)
            if cycle is None and state in states:
                start=states.index(state);cycle=dict(start=start,period=tick-start,first_repeat_tick=tick)
            rows.append(dict(alive=len(following),dead=h*w-len(following),births=len(following-live),deaths=len(live-following)));states.append(state);live=following
        out[s['id']]=dict(states=states,counts=rows,classification='unclassified' if cycle is None else 'fixed_point' if cycle['period']==1 else 'periodic_cycle',cycle=cycle,truncated=cycle is None)
    return out
def cases():
    good={'blinker':request(),'empty':request(grid(3,3),3),'single':request(grid(3,3,[(1,1)]),2),'block':request(grid(4,4,[(1,1),(1,2),(2,1),(2,2)]),3),'blinker-odd':request(ticks=5),'blinker-one':request(ticks=1),'zero-tick':request(ticks=0),'zero-tick-no-trace':request(ticks=0,trace=False),'tiny-one':request([[1]],2),'tiny-line':request([[1,1,1]],3),'tiny-two':request([[1,1],[1,0]],2),'clipped-corners':request([[1,0,1],[0,0,0],[1,0,0]],2)}
    glider={(1,2),(2,3),(3,1),(3,2),(3,3)};good['glider']=request(grid(7,7,glider),4);good['glider-no-trace']=request(grid(7,7,glider),4,False)
    good['translated']=request(grid(11,9,{(r+2,c+1) for r,c in glider}),4)
    board=grid(5,7,{(1,2),(2,3),(3,1),(3,2),(3,3)});good['rectangle']=request(board,3);good['rotated']=request([list(row) for row in zip(*board[::-1])],3);good['reflected']=request([row[::-1] for row in board],3)
    q=request();q['scenarios'].append(dict(id='vertical',initial_grid=[[0,1,0],[0,1,0],[0,1,0]]));good['equal-count-different-state']=q
    q=request(trace=False);q['scenarios'].append(dict(id='same',initial_grid=copy.deepcopy(q['scenarios'][0]['initial_grid'])));good['identical']=q
    q=request();q['scenarios'].append(dict(id='block',initial_grid=[[1,1,0],[1,1,0],[0,0,0]]));good['scenario-comparison']=q
    good['full-horizon-fixed']=request(grid(4,4,[(1,1),(1,2),(2,1),(2,2)]),256,False)
    q=request();q['provenance']['attribution']='Original Δ board ``` safe fence';good['unicode']=q
    bad={}
    def change(name,fn,base='blinker'):
        q=copy.deepcopy(good[base]);fn(q);bad[name]=q
    change('torus',lambda q:q['model'].update(boundary='toroidal'));change('wrap',lambda q:q['model'].update(boundary='wraparound'));change('schedule',lambda q:q['model'].update(scheduler='row-major-in-place'));change('other-rule',lambda q:q['model'].update(rule='B36/S23'));change('neighborhood',lambda q:q['model'].update(neighborhood='von-neumann'))
    change('variation',lambda q:q.update(variation='Schelling segregation'));change('rng',lambda q:q.update(rng=1));change('early-stop',lambda q:q.update(early_stop=True))
    change('profile',lambda q:q['profile'].update(sha256='0'*64));change('version',lambda q:q['profile'].update(version=True));change('schema',lambda q:q.update(schema_version=True));change('source',lambda q:q['provenance'].update(source_ref='unknown'));change('rights',lambda q:q['provenance'].update(rights='unknown'));change('snapshot',lambda q:q['provenance'].update(snapshot='changed'));change('empirical',lambda q:q['provenance'].update(synthetic=False))
    for name,value in [('negative',-1),('over',257),('bool',True),('float',1.0)]:change('ticks-'+name,lambda q,v=value:q.update(ticks=v))
    for name,value in [('zero',0),('over',65),('bool',True),('float',3.0)]:change('height-'+name,lambda q,v=value:q['geometry'].update(height=v))
    change('width-zero',lambda q:q['geometry'].update(width=0));change('wrong-height',lambda q:q['geometry'].update(height=2));change('wrong-width',lambda q:q['geometry'].update(width=2));change('ragged',lambda q:q['scenarios'][0]['initial_grid'][0].pop());change('row-string',lambda q:q['scenarios'][0]['initial_grid'].__setitem__(0,'000'))
    for name,value in [('bool',True),('float',1.0),('negative',-1),('two',2),('string','1')]:change('binary-'+name,lambda q,v=value:q['scenarios'][0]['initial_grid'][0].__setitem__(0,v))
    change('trace-type',lambda q:q.update(trace_states=1));change('empty-scenarios',lambda q:q.update(scenarios=[]));change('reference',lambda q:q.update(reference_scenario='missing'));change('duplicate-scenario',lambda q:q['scenarios'].append(copy.deepcopy(q['scenarios'][0])));change('scenario-geometry',lambda q:q['scenarios'][0].update(geometry=dict(height=3,width=3)))
    q=request(grid(64,64),256,False);bad['work-cap']=q
    q=request(grid(64,64),24,True);bad['state-cap']=q
    q=request([[0]],256,False);q['scenarios']=[dict(id='s'+str(i),initial_grid=[[0]]) for i in range(8)];q['reference_scenario']='s0';bad['count-cap']=q
    q=request();q['scenarios']=[dict(id='s'+str(i),initial_grid=copy.deepcopy(q['scenarios'][0]['initial_grid'])) for i in range(9)];q['reference_scenario']='s0';bad['scenario-cap']=q
    return {**{k:(q,0) for k,q in good.items()},**{k:(q,2) for k,q in bad.items()}}

FAMILIES={'local-rule-18-cases':['local_truth'],'local-512-combinatorial-oracle':['local_configurations'],'synchronous-inplace-negative':['blinker'],'clipped-edge-neighbors':['clipped-corners'],'toroidal-alias-refusal':['torus','wrap'],'center-exclusion':['tiny-one','single'],'distinct-neighbor-positions':['tiny-line','tiny-two'],'empty-board':['empty'],'single-cell-death':['single'],'block-fixed-point':['block'],'blinker-period-two':['blinker','blinker-odd'],'glider-translation-plan':['glider','glider-no-trace'],'birth-death-count-balance':['scenario-comparison'],'active-plus-dead-cells':['scenario-comparison'],'fixed-point-detection':['block','full-horizon-fixed'],'period-versus-fixed':['blinker','blinker-one'],'zero-steps':['zero-tick','zero-tick-no-trace'],'cap-truncation':['blinker-one','glider'],'interior-translation':['glider','translated'],'rotation-reflection':['rectangle','rotated','reflected'],'identical-scenario-control':['identical','equal-count-different-state'],'strict-binary-grid':['ragged','binary-bool','binary-two','row-string'],'unsupported-variation-rejection':['variation','rng','other-rule'],'source-rights-and-data':['source','rights','snapshot','empirical'],'combined-resource-caps':['work-cap','state-cap','count-cap'],'raw-json-markdown-hashes':['unicode','profile']}
def freeze():
    truth=[dict(current=a,neighbors=n,next=v) for a,values in [(0,[0,0,0,1,0,0,0,0,0]),(1,[0,0,1,1,0,0,0,0,0])] for n,v in enumerate(values)]
    table={(r['current'],r['neighbors']):r['next'] for r in truth};local=[]
    for code in range(512):
        current=(code>>4)&1;neighbors=code.bit_count()-current;local.append(dict(code=code,current=current,neighbors=neighbors,next=table[current,neighbors]))
    births=sum(r['next'] for r in local if not r['current']);survivals=sum(r['next'] for r in local if r['current']);assert (births,survivals)==(math.comb(8,3),math.comb(8,2)+math.comb(8,3))==(56,84)
    c=cases();expected={n:oracle(q) for n,(q,code) in c.items() if code==0}
    assert expected['blinker']['base']['states']==[[[0,0,0],[1,1,1],[0,0,0]],[[0,1,0],[0,1,0],[0,1,0]],[[0,0,0],[1,1,1],[0,0,0]]]
    assert expected['block']['base']['cycle']==dict(start=0,period=1,first_repeat_tick=1)
    final=expected['glider']['base']['states'][4];assert {(r,c) for r in range(7) for c in range(7) if final[r][c]}=={(2,3),(3,4),(4,2),(4,3),(4,4)}
    f=dict(version=1,families=FAMILIES,local_truth=truth,local_configurations=local,combinatorics=dict(configurations=512,births=56,survivals=84,next_alive=140,next_dead=372,exact_fraction='35/128'),inplace_negative=dict(cell=[0,2],synchronous_next=0,row_major_inplace_next=1),cases={n:dict(input=q,exit_code=code,expected=expected.get(n)) for n,(q,code) in c.items()})
    path=R/'tests/fixtures/agent-based-independent-v1.json';path.write_text(json.dumps(f,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    manifest=dict(version=1,profile_sha256=digest(json.loads((R/'knowledge/agent_based_profile_v1.json').read_text(encoding='utf-8'))),fixture_families=26,accepted=sum(code==0 for _,code in c.values()),rejected=sum(code!=0 for _,code in c.values()),local_truth_cases=18,local_configurations=512,normalized_lf_sha256={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in [path,Path(__file__)]})
    (R/'knowledge/agent_based_fixture_freeze_v1.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n');print(manifest)
if __name__=='__main__':freeze()
