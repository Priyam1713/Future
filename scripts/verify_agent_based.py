"""Frozen sparse-oracle boards, exhaustive local states and geometric identities."""
import copy,hashlib,json,math
from pathlib import Path
from future.agent_based import read,markdown,next_cell,transition,neighborhoods
from scripts.agent_based_oracle import digest
R=Path(__file__).resolve().parents[1]
def fixture():return json.loads((R/'tests/fixtures/agent-based-independent-v1.json').read_text(encoding='utf-8'))
def state_hash(board):return hashlib.sha256(bytes(x for row in board for x in row)).hexdigest()
def verify_case(name,c):
    if c['exit_code']:
        try:read(c['input'])
        except (ValueError,TypeError):return None
        raise AssertionError('Invalid request accepted: '+name)
    q=c['input'];r=read(q);assert r==read(q) and r['input_sha256']==digest(q);body=dict(r);sha=body.pop('report_sha256');assert digest(body)==sha
    n=q['geometry']['height']*q['geometry']['width'];expected=c['expected'];byid={s['id']:s for s in r['scenarios']}
    for s in r['scenarios']:
        e=expected[s['id']];assert s['initial_grid']==e['states'][0] and s['final_grid']==e['states'][-1]
        assert s['state_trace']==(e['states'] if q['trace_states'] else None)
        assert s['initial_state_sha256']==state_hash(e['states'][0]) and s['final_state_sha256']==state_hash(e['states'][-1])
        assert s['classification']==e['classification'] and s['truncated']==e['truncated']
        assert s['fixed_point']==(e['classification']=='fixed_point') and s['periodic_cycle']==(e['classification']=='periodic_cycle')
        assert (s['cycle_start'],s['period'],s['first_repeat_tick'])==((e['cycle']['start'],e['cycle']['period'],e['cycle']['first_repeat_tick']) if e['cycle'] else (None,None,None))
        assert s['requested_ticks']==s['executed_ticks']==q['ticks'] and not s['early_stopped'] and len(s['counts'])==q['ticks']+1
        for tick,(row,answer) in enumerate(zip(s['counts'],e['counts'])):
            assert all(row[k]==v for k,v in answer.items()) and row['state_sha256']==state_hash(e['states'][tick])
            assert row['alive']+row['dead']==n
            if tick:assert row['alive']==s['counts'][tick-1]['alive']+row['births']-row['deaths']
            else:assert row['births'] is row['deaths'] is None
    ref=expected[q['reference_scenario']]
    for comp in r['comparisons']:
        e=expected[comp['scenario']];diffs=[]
        for tick,(a,b) in enumerate(zip(e['states'],ref['states'])):
            alive_a=sum(map(sum,a));alive_b=sum(map(sum,b));hamming=sum(x!=y for ar,br in zip(a,b) for x,y in zip(ar,br));diffs.append(dict(tick=tick,alive_difference=alive_a-alive_b,hamming_distance=hamming))
        assert comp['per_tick']==diffs and comp['final_alive_difference']==diffs[-1]['alive_difference'] and comp['final_hamming_distance']==diffs[-1]['hamming_distance']
        assert comp['final_states_equal']==(e['states'][-1]==ref['states'][-1])
        if comp['identical_initial_state']:assert all(d['alive_difference']==d['hamming_distance']==0 for d in diffs)
    assert markdown(r)==markdown(read(q));return r
def verify_local(f):
    for row in f['local_truth']:assert next_cell(row['current'],row['neighbors'])==row['next']
    neighbors=neighborhoods(3,3);birth=survival=0
    for row in f['local_configurations']:
        state=bytes((row['code']>>i)&1 for i in range(9));following=transition(state,neighbors);assert following[4]==row['next']
        if not state[4]:birth+=following[4]
        else:survival+=following[4]
    assert birth==math.comb(8,3)==56 and survival==math.comb(8,2)+math.comb(8,3)==84
    assert birth+survival==140 and 512-birth-survival==372
def inplace_negative():
    board=[[0,0,0],[1,1,1],[0,0,0]]
    for r in range(3):
        for c in range(3):
            count=sum(board[x][y] for x in range(max(0,r-1),min(3,r+2)) for y in range(max(0,c-1),min(3,c+2)) if (x,y)!=(r,c))
            board[r][c]=int(count==3 or board[r][c]==1 and count==2)
            if (r,c)==(0,2):return board[r][c]
def run():
    f=fixture();manifest=json.loads((R/'knowledge/agent_based_fixture_freeze_v1.json').read_text())
    for p,h in manifest['normalized_lf_sha256'].items():assert hashlib.sha256((R/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==h
    results={n:verify_case(n,c) for n,c in f['cases'].items()};verify_local(f);assert inplace_negative()==f['inplace_negative']['row_major_inplace_next']==1
    assert results['blinker']['scenarios'][0]['state_trace'][1][0][2]==f['inplace_negative']['synchronous_next']==0
    for original,rotated,reflected in zip(results['rectangle']['scenarios'][0]['state_trace'],results['rotated']['scenarios'][0]['state_trace'],results['reflected']['scenarios'][0]['state_trace']):
        assert [list(row) for row in zip(*original[::-1])]==rotated and [row[::-1] for row in original]==reflected
    for a,b in zip(results['glider']['scenarios'][0]['state_trace'],results['translated']['scenarios'][0]['state_trace']):
        assert {(r+2,c+1) for r,row in enumerate(a) for c,x in enumerate(row) if x}=={(r,c) for r,row in enumerate(b) for c,x in enumerate(row) if x}
    eq=next(x for x in results['equal-count-different-state']['comparisons'] if x['scenario']=='vertical');assert eq['final_alive_difference']==0 and eq['final_hamming_distance']==4
    q=copy.deepcopy(f['cases']['identical']['input']);a=read(q);q['scenarios'].reverse();b=read(q);assert {s['id']:s for s in a['scenarios']}=={s['id']:s for s in b['scenarios']}
    for case,key in [('work-cap','cell_ticks'),('state-cap','returned_state_cells'),('count-cap','returned_count_cells')]:
        try:read(f['cases'][case]['input'])
        except ValueError as e:assert key in str(e)
        else:raise AssertionError('Resource cap not rejected')
    out=dict(passed=True,fixture_families=26,families={k:dict(passed=True,cases=v) for k,v in f['families'].items()},accepted=manifest['accepted'],rejected=manifest['rejected'],profile_sha256=manifest['profile_sha256'],pre_engine_hashes_passed=True,local_truth_cases=18,exhaustive_local_configurations=512,combinatorics=f['combinatorics'],block_blinker_glider_passed=True,geometric_controls_passed=True,inplace_negative_passed=True,scientific_scope='Exact bounded synthetic automaton correctness;notempirical social,clinical,LLM orcausal prediction')
    (R/'data/agent-based-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('26 independent families pass;18local cases;512configurations=56birth+84survival=140alive/372dead;block,blinker,glider andgeometry');return out
if __name__=='__main__':run()
