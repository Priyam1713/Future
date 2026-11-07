"""Compare production to immutable pre-engine tables and independent algebra."""
import copy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from future.psychohistory import read,words,markdown,validate
from scripts.psychohistory_oracle import stats,digest

R=Path(__file__).resolve().parents[1]
def fixture():return json.loads((R/'tests/fixtures/psychohistory-independent-v1.json').read_text(encoding='utf-8'))
def verify_case(name,c):
    if c['exit_code']:
        try:read(c['input'])
        except (ValueError,TypeError):return None
        raise AssertionError('Invalid request accepted: '+name)
    report=read(c['input']);q=c['input'];n=q['population']['size'];byid={s['id']:s for s in report['scenarios']}
    assert report==read(q) and digest(q)==report['input_sha256']
    body=dict(report);h=body.pop('report_sha256');assert digest(body)==h
    for sid,expected in c['expected'].items():
        actual=byid[sid];initial=[];final=[];gains=[]
        for row,answer in zip(actual['rows'],expected):
            counts=answer['counts'];assert row['active_counts']==counts and row['inactive_counts']==[n-x for x in counts]
            assert counts==sorted(counts) and all(0<=x<=n for x in counts)
            assert row['states']==(answer['states'] if q['trace_states'] else None)
            assert row['initial_state_sha256']==digest(answer['states'][0]) and row['final_state_sha256']==digest(answer['states'][-1])
            assert row['truncated']==answer['truncated'] and row['converged']!=row['truncated']
            assert row['executed_rounds']==len(counts)-1 and row['persistence_final_active']==counts[0]
            assert row['initial_active']==counts[0] and row['final_active']==counts[-1]
            initial.append(counts[0]);final.append(counts[-1]);gains.append(counts[-1]-counts[0])
        for key,values in [('initial_count',initial),('final_count',final),('initial_fraction',[F(x,n) for x in initial]),('final_fraction',[F(x,n) for x in final])]:
            expected_stats=stats(values)
            assert all(actual[key][k]==v for k,v in expected_stats.items()),(name,key)
            assert actual[key]['population_denominator']==len(values)
            assert actual[key]['sample_denominator']==(len(values)-1 if len(values)>1 else None)
        assert all(actual['persistence_baseline']['gain'][k]==v for k,v in stats(gains).items())
        for t in range(q['rounds']+1):
            mean=sum(F(r['counts'][min(t,len(r['counts'])-1)]) for r in expected)/q['runs']
            assert actual['per_round_mean_active'][t]==str(mean) and actual['per_round_mean_inactive'][t]==str(n-mean)
    ref=byid[q['reference_scenario']]
    for row in report['comparisons']:
        diff=[a['final_active']-b['final_active'] for a,b in zip(byid[row['scenario']]['rows'],ref['rows'])]
        assert row['paired_final_differences']==diff and all(row['statistics'][k]==v for k,v in stats(diff).items())
        if row['identical_configuration']:assert set(diff)=={0}
        assert row['pairing_stream_sha256']==report['stream_sha256']
    assert markdown(report)==markdown(read(q))
    return report

def run():
    f=fixture();freeze=json.loads((R/'knowledge/psychohistory_fixture_freeze_v1.json').read_text())
    for name,h in freeze['normalized_lf_sha256'].items():assert hashlib.sha256((R/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==h
    results={name:verify_case(name,c) for name,c in f['cases'].items()}
    assert words(1,5)==f['prng_seed1_first5']
    assert results['path']['scenarios'][0]['rows'][0]['states']==f['literal_anchors']['path']
    assert f['literal_anchors']['path'][1]!=f['literal_anchors']['forward_inplace_one_sweep']
    exact=results['exhaustive']['scenarios'][0]
    assert exact['final_count']['mean']=='3/2' and exact['final_count']['population_variance']=='3/4'
    assert exact['final_fraction']['mean']=='3/4' and exact['final_fraction']['population_variance']=='3/16'
    assert exact['persistence_baseline']['gain']['mean']=='1/2' and exact['persistence_baseline']['gain']['population_variance']=='1/4'
    assert results['node-thresholds']['scenarios'][0]['rows'][0]['active_counts']==results['relabelled']['scenarios'][0]['rows'][0]['active_counts']
    # Shared draws are invariant under scenario order, graphs and fixed overrides.
    q=copy.deepcopy(f['cases']['overrides']['input']);a=read(q);q['scenarios'].reverse();b=read(q)
    assert a['stream_sha256']==b['stream_sha256'] and {s['id']:s['rows'] for s in a['scenarios']}=={s['id']:s['rows'] for s in b['scenarios']}
    for s in a['scenarios']:assert [r['draw_row_sha256'] for r in s['rows']]==[r['draw_row_sha256'] for r in a['scenarios'][0]['rows']]
    # Literal ideal binomial versus correlated final population variance.
    assert F(4)*F(1,4)==F(f['literal_anchors']['binomial_N4_rho_quarter']['mean'])
    assert F(4)*F(1,4)*F(3,4)==F('3/4')
    for name in ['rho-zero','rho-one','bernoulli','overrides']:
        for s in results[name]['scenarios']:
            spec=next(x for x in f['cases'][name]['input']['scenarios'] if x['id']==s['id']);rho=F(spec['initial']['probability']);free=4-len(spec['initial']['overrides']);fixed=sum(o['state'] for o in spec['initial']['overrides'])
            assert s['ideal_initial_moments']['mean']==str(fixed+free*rho) and s['ideal_initial_moments']['variance']==str(free*rho*(1-rho))
    # Target-specific budget refusals; work-case output remains within its caps.
    for name,kind in [('state-cap','state_cells'),('work-cap','work_units'),('count-cap','work_units')]:
        try:validate(f['cases'][name]['input'])
        except ValueError as e:assert kind in str(e),(name,str(e))
        else:raise AssertionError('Cap not rejected')
    out=dict(passed=True,profile_sha256=freeze['profile_sha256'],families={k:dict(passed=True,cases=v) for k,v in f['families'].items()},fixture_families=len(f['families']),accepted=freeze['accepted'],rejected=freeze['rejected'],literal_anchors=f['literal_anchors'],prng_vectors_passed=True,pairing_and_order_passed=True,pre_engine_fixture_hashes_passed=True,scientific_scope='Independent synthetic software correctness only; no empirical validation')
    (R/'data/psychohistory-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('23 independent fixture families pass;21 accepted/41 rejected cases;exact algebra,PRNG,pairing and conservation')
    return out

if __name__=='__main__':run()
