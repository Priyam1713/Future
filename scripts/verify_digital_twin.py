"""Immutable pre-engine information-form/closed-form tables versus production."""
import copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from future.digital_twin import read,markdown
from scripts.digital_twin_oracle import digest
R=Path(__file__).resolve().parents[1]
def fixture():return json.loads((R/'tests/fixtures/digital-twin-independent-v1.json').read_text(encoding='utf-8'))
def verify_case(name,c):
    if c['exit_code']:
        try:read(c['input'])
        except (ValueError,TypeError):return None
        raise AssertionError('Invalid request accepted: '+name)
    q=c['input'];r=read(q);expected=c['expected'];assert r==read(q) and r['input_sha256']==digest(q)
    body=dict(r);h=body.pop('report_sha256');assert digest(body)==h
    assert len(r['rows'])==len(expected['rows'])
    for actual,answer in zip(r['rows'],expected['rows']):
        assert all(actual[k]==v for k,v in answer.items()),(name,actual,answer)
        assert F(actual['posterior_variance'])>=0 and F(actual['innovation_variance'])>0
        if actual['correction']=='applied':
            H=F(q['parameters']['H']);P=F(actual['prior_variance']);Rn=F(q['parameters']['R']);K=F(actual['gain'])
            # Independent Joseph identity, including non-unit/negative H and gain>1.
            assert F(actual['posterior_variance'])==(1-K*H)**2*P+K*K*Rn
    assert r['final_posterior']['mean']==expected['final_mean'] and r['final_posterior']['variance']==expected['final_variance']
    for s in r['scenarios']:
        assert len(s['trajectory'])==len(expected['branches'][s['id']])
        for a,b in zip(s['trajectory'],expected['branches'][s['id']]):assert all(a[k]==v for k,v in b.items())
        assert s['fork']==r['scenario_fork']
    if r['scenarios']:
        byid={s['id']:s for s in r['scenarios']};ref=byid[q['reference_scenario']]
        for comp in r['comparisons']:
            for diff,a,b in zip(comp['differences'],byid[comp['scenario']]['trajectory'],ref['trajectory']):
                assert F(diff['mean_difference'])==F(a['mean'])-F(b['mean']) and F(diff['variance_difference'])==F(a['variance'])-F(b['variance'])
                if comp['identical_controls']:assert diff['mean_difference']==diff['variance_difference']=='0'
    # Independently select all known targets and common three-way denominators.
    eligible=[i for i,x in enumerate(expected['rows']) if x['filter_squared_error'] is not None];matched=[i for i in eligible if expected['rows'][i]['persistence_squared_error'] is not None]
    assert r['evaluation']['eligible_target_ids']==[q['records'][i]['id'] for i in eligible]
    assert r['evaluation']['matched_target_ids']==[q['records'][i]['id'] for i in matched]
    for score,indices,key in [(r['evaluation']['filter_all'],eligible,'filter_squared_error'),(r['evaluation']['open_loop_all'],eligible,'open_loop_squared_error')]+[(r['evaluation']['three_way_matched'][key],matched,key+'_squared_error') for key in ['filter','open_loop','persistence']]:
        values=[F(expected['rows'][i][key]) for i in indices];assert score['count']==len(values)
        assert score['mean_squared_error']==(str(sum(values,F())/len(values)) if values else None)
        assert score['status']==('finite' if values else 'not_estimable')
    assert markdown(r)==markdown(read(q));return r
def run():
    f=fixture();manifest=json.loads((R/'knowledge/digital_twin_fixture_freeze_v1.json').read_text())
    for p,h in manifest['normalized_lf_sha256'].items():assert hashlib.sha256((R/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==h
    results={n:verify_case(n,c) for n,c in f['cases'].items()}
    seq=results['sequential'];anchor=f['batch_anchor'];assert seq['final_posterior']['mean']==anchor['mean'] and seq['final_posterior']['variance']==anchor['variance']
    assert seq['rows'][1]['filter_squared_error']=='1' and seq['rows'][1]['persistence_squared_error']=='0' and seq['rows'][1]['open_loop_squared_error']=='4'
    # Neither evaluation cutoff nor an unavailable measurement can change filter states.
    a=results['not-yet-known'];b=results['later-evaluation'];assert a['final_posterior']==b['final_posterior'] and a['scenario_fork']==b['scenario_fork']
    assert a['evaluation']['eligible_target_ids']!=b['evaluation']['eligible_target_ids']
    a=results['delayed'];b=results['delayed-changed'];assert a['final_posterior']==b['final_posterior'] and a['scenario_fork']==b['scenario_fork']
    assert [x['predicted_measurement'] for x in a['rows']]==[x['predicted_measurement'] for x in b['rows']]
    q=copy.deepcopy(f['cases']['controls']['input']);a=read(q);q.update(horizon=0,scenarios=[],reference_scenario=None);b=read(q);assert a['rows']==b['rows'] and a['final_posterior']==b['final_posterior']
    assert F(results['gain-over-one']['rows'][0]['gain'])>1
    for name in ['cell-cap','bit-growth']:
        try:read(f['cases'][name]['input'])
        except ValueError as e:assert ('budget' in str(e)) if name=='cell-cap' else ('bit' in str(e))
        else:raise AssertionError('Resource request accepted')
    out=dict(passed=True,fixture_families=27,families={k:dict(passed=True,cases=v) for k,v in f['families'].items()},accepted=manifest['accepted'],rejected=manifest['rejected'],profile_sha256=manifest['profile_sha256'],pre_engine_fixture_hashes_passed=True,batch_anchor=anchor,chronology_and_future_forks_passed=True,matched_preupdate_scores_passed=True,scientific_scope='Bounded exact synthetic replay correctness; not empirical accuracy, calibrated uncertainty or complete real-time twin certification')
    (R/'data/digital-twin-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('27 independent fixture families pass;22 accepted/43 rejected cases;batch,chronology,baselines,scenarios andbit bounds');return out
if __name__=='__main__':run()
