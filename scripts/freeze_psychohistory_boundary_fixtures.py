"""Independent preflight-only cap and exact draw-boundary addendum."""
import copy
import hashlib
import json
from scripts.psychohistory_oracle import R,request,digest

def run():
    q=request(128,[],runs=256,cap=18,trace=False);q['scenarios']=[dict(copy.deepcopy(q['scenarios'][0]),id='s'+str(i)) for i in range(8)];q['reference_scenario']='s0'
    assert 8*256*19*128==4980736 and 8*(2*257*19+12*256+32)==102960
    cases={'count-only-cap':dict(input=q,exit_code=2,expected_budget=dict(work_units=4980736,count_cells=102960,state_cells=0))}
    for name,rho,expected in [('draw-exact-tie','270369/4294967296',0),('draw-above-tie','270370/4294967296',1)]:
        q=request(1,[],trace=True);q['scenarios'][0]['initial'].update(mode='bernoulli',probability=rho,fixed_seeds=[])
        cases[name]=dict(input=q,exit_code=0,initial_active=expected)
    path=R/'tests/fixtures/psychohistory-boundaries-v1.json';path.write_text(json.dumps(dict(version=1,cases=cases),indent=2)+'\n',encoding='utf-8',newline='\n')
    freeze=dict(version=1,reason='Separately freeze count-only preflight rejection and strict Bernoulli rational equality; no production change.',normalized_lf_sha256={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in [path,__file__ and R/'scripts/freeze_psychohistory_boundary_fixtures.py']})
    (R/'knowledge/psychohistory_boundary_fixture_freeze_v1.json').write_text(json.dumps(freeze,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Three independent boundary cases frozen')

if __name__=='__main__':run()
