"""Independent frozen numerical, all-cell and procedural forecasting verifier."""
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from future import ai_predictive_modeling as e
from .ai_predictive_modeling_oracle import sha

ROOT=Path(__file__).resolve().parents[1]
F=json.loads((ROOT/'tests/fixtures/ai_predictive_modeling_reference_v1.json').read_text())


def req(task,**kw):
    return dict(schema_version=1,profile=e.DATA['id'],profile_version=1,task=task,**kw)


def dataset(values=None,season=1):
    values=values if values is not None else ['1','2','3','4','5','6','7','8']
    return dict(id='synthetic',version=1,frequency='monthly',units='original units',
        provenance=dict(source_ref='original-synthetic',snapshot_sha256=None,rights='self_authored',attribution='Original synthetic numerical demonstration',notes='Unicode note  \n'),
        series=[dict(id='synthetic1',availability=dict(status='unknown',vintage=None,notes='No independent availability witness'),
                     observations=[dict(period=f'2020-{i+1:02d}',value=v) for i,v in enumerate(values)])])


def plan(models=None,season=1):
    return dict(models=models if models is not None else ['naive','mean','drift','ses_alpha0.2_initial_y1'],
                validation_origins=['2020-02','2020-03'],test_origins=['2020-04','2020-05'],horizons=[1],seasonal_period=season,selection='validation_macro_mae_then_order')


def reject(fn):
    try:fn()
    except (ValueError,KeyError,TypeError):return
    raise AssertionError('Invalid configuration accepted')


def eq(a,b):
    assert a==b,(a,b)


def run(write=False,resource_required=False):
    frozen=json.loads((ROOT/'data/ai-predictive-modeling-fixture-freeze.json').read_text())
    eq(sha(F),frozen['fixture_sha256']);eq(e.PROFILE_HASH,F['profile_sha256'])
    eq(hashlib.sha256((ROOT/'scripts/ai_predictive_modeling_oracle.py').read_bytes()).hexdigest(),frozen['oracle_sha256'])
    families={}
    for x in F['forecasts']:
        eq(list(map(str,e.point_forecasts(x['train'],x['model'],x['horizons'],x['season']))),x['expected'])
    families['seasonal-naive']=6;families['trend']=3
    for model in e.MODELS:
        eq(e.point_forecasts(['5']*12,model,[1,12,13,25],12),[Q(5)]*4)
    families['constant']=28
    for origin,h,target in F['month_examples']:eq(e.add_month(origin,h),target)
    families['horizon-indexing']=3
    m=F['metrics'];r=e.manual_metrics(dict(training=m['train'],actual=m['actual'],predictions=m['predictions'],seasonal_period=1))
    for key in ('mae','mse','mase','bias','wape'):eq(r[key]['exact'],m['expected'][key])
    eq(r['rmse']['decimal'],m['expected']['rmse']);eq(r['absolute_smape_percent']['exact'],m['expected']['smape'])
    families['deterministic-metrics']=7
    eq(e.training_scale(['1','2','3'],1)[0],Q(1));eq(e.training_scale(['1','10','3','12'],2)[0],Q(2))
    families['mase-scale']=2
    for ys,actual,pred,key in [(['0']*4,['0'],['0'],'mase'),(['1','2'],['0'],['1'],'wape')]:
        rr=e.manual_metrics(dict(training=ys,actual=actual,predictions=pred,seasonal_period=1));eq(rr[key]['exact'],None)
    eq(e.manual_metrics(dict(training=[],actual=[],predictions=[],seasonal_period=1))['mae']['reason'],'no_scored_pairs')
    families['zero-denominators']=3
    source=F['source_scoring'];q=dict(actual=source['actual'],quantiles=[dict(p=source['p'],forecast=source['q'])],intervals=[{k:source[k] for k in ('alpha','lower','upper')}])
    rr=e.distribution_score(q);eq(rr['quantiles'][0]['fpp3_twice_pinball']['exact'],source['twice_pinball']);eq(rr['intervals'][0]['score']['exact'],source['interval_score'])
    for y in ('744.54','773.22'):
        qq=copy.deepcopy(q);qq['actual']=y;eq(e.distribution_score(qq)['intervals'][0]['covered'],True)
    bad=copy.deepcopy(q);bad['intervals'][0].update(lower='800',upper='700');reject(lambda:e.distribution_score(bad))
    families['interval-ordering']=4
    bad=copy.deepcopy(q);bad['quantiles']=[dict(p='0.1',forecast='4'),dict(p='0.9',forecast='3')];reject(lambda:e.distribution_score(bad))
    bad=copy.deepcopy(q);bad['quantiles'][0]['p']='1';reject(lambda:e.distribution_score(bad))
    families['quantile-monotonicity']=3
    d=e.noaa_dataset();p=e.benchmark_plan();eq(len(d['series'][0]['observations']),288)
    e.validate_dataset(d,sha(d));reject(lambda:e.validate_dataset(d,'0'*64))
    bad=copy.deepcopy(d);bad['provenance']['rights']='unknown';reject(lambda:e.validate_dataset(bad,sha(bad)))
    families['dataset-rights-hashes']=3
    eq(p['validation_origins'],F['validation_origins']);eq(p['test_origins'],F['test_origins']);eq(len(p['horizons']),12)
    result=e.evaluate(d,p);eq(result['selection']['selected'],F['benchmark']['selected'])
    # Check all 4200 cell forecasts and each independent aggregate/horizon expectation.
    count=0
    for partition in ('validation','test'):
        eq(len(result['cells'][partition]),2100)
        for row in result['summary'][partition]:
            model=row['model'];expected=F['benchmark']['scores'][partition][model]
            cells=[c for c in result['cells'][partition] if c['model']['id']==model]
            eq(sha([[c['origin'],c['horizon'],c['target_period'],c['prediction']['exact']] for c in cells]),expected['prediction_sha256'])
            eq(row['aggregate']['scored'],300);eq(row['aggregate']['distinct_target_months'],36)
            for key in ('mae','mse','mase','bias','wape'):eq(row['aggregate'][key]['exact'],expected[key])
            for h,v in expected['horizon_mae'].items():eq(row['by_horizon'][h]['mae']['exact'],v)
            for c in cells:
                eq(c['sha256'],sha({k:v for k,v in c.items() if k!='sha256'}));assert c['training_cutoff']==c['origin'] and c['training_cutoff']<c['target_period'];count+=1
    families['fold-boundaries']=count
    for origin in ('2017-12','2019-12','2020-12','2022-12'):
        changed=copy.deepcopy(d)
        for r in changed['series'][0]['observations']:
            if r['period']>origin:r['value']='999999999999'
        for model in e.MODELS:
            before=e.forecast_cells(d,model,origin,list(range(1,25)),12)
            after=e.forecast_cells(changed,model,origin,list(range(1,25)),12)
            eq([r['prediction'] for r in before],[r['prediction'] for r in after])
            eq([r['training_prefix_sha256'] for r in before],[r['training_prefix_sha256'] for r in after])
    families['training-test-isolation']=4*7*24
    raw=dataset();bad=copy.deepcopy(raw);bad['future_covariates']={'target':['999']};reject(lambda:e.validate_dataset(bad,sha(bad)))
    families['future-covariates']=1
    dd=dataset(['1','2','3',None,'5','6']);r=e.evaluate(dd,plan())
    assert any(c['status']=='missing_target' for c in r['cells']['validation']);assert any(c['status']=='model_failure' for c in r['cells']['test'])
    families['missing-observations']=2
    for change in ('duplicate','irregular'):
        bad=dataset();bad['series'][0]['observations'][2]['period']='2020-02' if change=='duplicate' else '2020-04'
        reject(lambda:e.validate_dataset(bad,sha(bad)))
    families['irregular-timestamps']=2
    multi=dataset();s=copy.deepcopy(multi['series'][0]);s['id']='synthetic2'
    for r in s['observations']:r['value']=str(Q(r['value'])*10)
    multi['series'].append(s);e.validate_dataset(multi,sha(multi));r=e.evaluate(multi,plan())
    eq(len(r['cells']['validation']),16);eq(set(r['summary']['test'][0]['by_series']),{'synthetic1','synthetic2'})
    bad=copy.deepcopy(multi);bad['series'][1]['id']='synthetic1';reject(lambda:e.validate_dataset(bad,sha(bad)))
    families['multiple-series']=3
    zero=e.evaluate(dataset(['0']*8),plan(['naive','mean'],1));eq(zero['selection']['selected'],'naive')
    eq(zero['summary']['test'][0]['paired_seasonal_naive']['ratio']['reason'],'zero_reference_error')
    test_changed=copy.deepcopy(d)
    for r in test_changed['series'][0]['observations']:
        if r['period']>='2021-01':r['value']='100'
    eq(e.evaluate(test_changed,p)['selection'],result['selection'])
    families['baseline-comparisons']=3
    broken=dataset(['1','1','1','100','100','100']);r=e.forecast_cells(broken,'naive','2020-03',[1],1)[0]
    eq(r['prediction']['exact'],'1');eq(r['absolute_error']['exact'],'99');families['structural-break']=2
    q=req('forecast',dataset=raw,dataset_sha256=sha(raw),model='naive',origin='2020-03',horizons=[1,2],seasonal_period=1)
    report=e.read(q);eq(report,e.read(q));eq(report,e.read(req('report',request=q)))
    eq(report['report_sha256'],sha({k:v for k,v in report.items() if k!='report_sha256'}));families['exact-replay']=3
    for model in ('chronos-2','ses_alpha0.3_initial_y1','ARIMA'):
        reject(lambda:e.point_forecasts(['1','2'],model,[1],1))
    bad=copy.deepcopy(q);bad['model']='chronos-2';reject(lambda:e.read(bad))
    retained=e.evaluate(raw,plan(['naive','chronos-2']));eq(retained['summary']['test'][1]['aggregate']['status_counts']['unsupported_configuration'],2)
    families['unsupported-configurations']=5
    path=ROOT/'data/ai-predictive-modeling-resource-measurements.json'
    if path.exists():
        rr=json.loads(path.read_text());assert rr['profile_sha256']==e.PROFILE_HASH and rr['warm_model_seconds']>0 and rr['peak_process_bytes']>0
        assert rr['code_sha256']==hashlib.sha256((ROOT/'future/ai_predictive_modeling.py').read_bytes()).hexdigest();families['resource-benchmarks']=3
    elif resource_required:raise AssertionError('Measured resource evidence required for acceptance')
    else:families['resource-benchmarks']=0
    eq(set(families),set(F['families']))
    out=dict(passed=all(families.values()),numerical_checks_passed=True,profile_sha256=e.PROFILE_HASH,fixture_sha256=sha(F),
             independent_oracle_commit='1d5ed6a',cells_checked=count,sentinel_predictions=672,
             families=[dict(id=k,passed=bool(families[k]),checks=families[k]) for k in F['families']],selected_reference=F['benchmark']['selected'],
             source_vintage_certified=False,method='Pre-engine rational prediction commitments,independent geometric SES oracle,manual constants and untouched input prefixes;no expected output derived from production.')
    if write:(ROOT/'data/ai-predictive-modeling-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    return out


if __name__=='__main__':
    out=run(write=True,resource_required=True);print('21 forecasting families;4200 independent cells;672 sentinel predictions;source metrics and complete candidate ledger passed')
