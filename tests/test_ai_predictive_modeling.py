import copy
import json
import unittest
from unittest.mock import patch
from fractions import Fraction as Q
from future import ai_predictive_modeling as e
from future.knowledge import Registry
from scripts.verify_ai_predictive_modeling import F,req,dataset,plan,sha,run


def forecast_request(d=None,**changes):
    d=copy.deepcopy(d or dataset())
    q=req('forecast',dataset=d,dataset_sha256=sha(d),model='naive',origin='2020-03',horizons=[1,2],seasonal_period=1)
    q.update(changes);return q


def invalid_requests():
    out={}
    for name,k,v in [('profile','profile','unknown'),('version','profile_version',True),('schema','schema_version',True),('model','model','chronos-2'),
                     ('alpha','model','ses_alpha0.3_initial_y1'),('season','seasonal_period',True),('h0','horizons',[0]),('hbool','horizons',[True]),
                     ('hduplicate','horizons',[1,1]),('horder','horizons',[2,1]),('hfloat','horizons',[1.0]),('hmax','horizons',[121]),
                     ('origin','origin','2020-13'),('missing-origin','origin','2019-12'),('dataset-hash','dataset_sha256','0'*64)]:
        q=forecast_request();q[k]=v;out[name]=q
    for name,mutate in [
        ('duplicate-period',lambda d:d['series'][0]['observations'][1].update(period='2020-01')),
        ('irregular',lambda d:d['series'][0]['observations'][1].update(period='2020-03')),
        ('non-monthly',lambda d:d.update(frequency='daily')),
        ('no-rights',lambda d:d['provenance'].update(rights='unknown')),
        ('empty-source',lambda d:d['provenance'].update(source_ref='')),
        ('bad-source-hash',lambda d:d['provenance'].update(snapshot_sha256='bad')),
        ('duplicate-series',lambda d:d['series'].append(copy.deepcopy(d['series'][0]))),
        ('future-covariates',lambda d:d.update(future_covariates={'target':'future'})),
        ('missing-training',lambda d:d['series'][0]['observations'][1].update(value=None)),
        ('availability',lambda d:d['series'][0]['availability'].update(status='verified_unseen'))]:
        d=dataset();mutate(d);out[name]=forecast_request(d)
    for name,v in [('float',1.2),('bool',True),('nan','NaN'),('infinity','Infinity'),('exponent','1e3'),('leading-zero','01'),('plus','+1'),('space',' 1'),('empty',''),('too-big','9'*31),('too-precise','0.'+'1'*25)]:
        d=dataset();d['series'][0]['observations'][1]['value']=v;out['numeric-'+name]=forecast_request(d)
    q=forecast_request();q['unknown']=True;out['extra-field']=q
    q=forecast_request();q['model']='drift';q['origin']='2020-01';out['short-drift']=q
    q=forecast_request();q.update(model='seasonal_naive_m12',seasonal_period=12);out['short-seasonal']=q
    q=forecast_request();q.update(model='seasonal_naive_m4',seasonal_period=12);out['season-model-mismatch']=q
    q=req('benchmark',resource_evidence=dict(record={},sha256='0'*64));out['resource-hash']=q
    return out


class Forecasting(unittest.TestCase):
    def test_independent_preengine_oracle(self):self.assertTrue(run()['numerical_checks_passed'])

    def test_no_network(self):
        with patch('socket.socket.connect',side_effect=AssertionError('Network forbidden')):
            self.assertEqual(e.read(forecast_request())['result']['cells'][0]['prediction']['exact'],'3')

    def test_registry_idempotence(self):
        r=Registry(':memory:')
        try:
            for _ in range(2):e.read(req('reference'),r)
        finally:r.close()

    def test_arbitrary_unicode_provenance_replay(self):
        d=dataset();d['provenance']['notes']='  Cafe\u0301 \n`````json\n<script>raw</script> 🪁'
        q=forecast_request(d);r=e.read(q)
        self.assertEqual(r['result']['dataset']['provenance']['notes'],d['provenance']['notes'])
        self.assertIn('``````json',e.markdown(r))

    def test_failed_candidates_retained(self):
        p=plan(['seasonal_naive_m12','naive','unknown'],12);r=e.evaluate(dataset(),p)
        self.assertEqual(len(r['cells']['validation']),6)
        self.assertEqual(r['selection']['selected'],'naive')
        self.assertEqual([s['eligible'] for s in r['selection']['candidates']],[False,True,False])

    def test_missing_outcome_counts(self):
        d=dataset(['1','2','3',None,'5','6']);r=e.evaluate(d,plan(['naive']))
        self.assertEqual(r['summary']['validation'][0]['aggregate']['status_counts']['missing_target'],1)
        self.assertEqual(r['summary']['test'][0]['aggregate']['scored'],0)

    def test_empty_metrics(self):
        r=e.manual_metrics(dict(training=[],actual=[],predictions=[],seasonal_period=1))
        self.assertEqual(r['mae']['decimal'],None);self.assertEqual(r['rmse']['reason'],'no_scored_pairs')

    def test_manual_smape_scope(self):
        r=e.manual_metrics(dict(training=['1','2'],actual=['2']*21,predictions=['1']*21,seasonal_period=1))
        self.assertEqual(r['absolute_smape_percent']['reason'],'manual_diagnostic_only_max20_pairs')
        self.assertEqual(r['mae']['exact'],'1')

    def test_all_zero_scale_not_perfect(self):
        r=e.manual_metrics(dict(training=['0','0'],actual=['0'],predictions=['1'],seasonal_period=1))
        self.assertEqual(r['mase']['reason'],'zero_training_scale');self.assertEqual(r['wape']['reason'],'zero_actual_denominator')
        self.assertEqual(r['mae']['exact'],'1')

    def test_mismatched_manual_lengths(self):
        with self.assertRaises(ValueError):e.manual_metrics(dict(training=['1'],actual=['1'],predictions=[],seasonal_period=1))

    def test_invalid_manual_training_even_short(self):
        with self.assertRaises(ValueError):e.manual_metrics(dict(training=['NaN'],actual=['1'],predictions=['1'],seasonal_period=12))

    def test_test_selection_is_frozen(self):
        d=dataset();p=plan();r=e.evaluate(d,p);changed=copy.deepcopy(d)
        for row in changed['series'][0]['observations']:
            if row['period']>='2020-05':row['value']='-100000'
        self.assertEqual(e.evaluate(changed,p)['selection'],r['selection'])

    def test_validation_targets_must_resolve_before_test(self):
        p=plan();p['horizons']=[1,2]
        with self.assertRaises(ValueError):e.validate_plan(p)

    def test_no_future_grid_in_single_training(self):
        d=dataset(['1','2','3']);r=e.read(forecast_request(d,horizons=[1,12,13]))
        self.assertEqual([c['status'] for c in r['result']['cells']],['missing_target']*3)
        self.assertEqual([c['prediction']['exact'] for c in r['result']['cells']],['3']*3)

    def test_benchmark_counts(self):
        r=e.evaluate(e.noaa_dataset(),e.benchmark_plan())
        self.assertEqual(sum(len(v) for v in r['cells'].values()),4200)
        self.assertEqual(r['selection']['selected'],'drift')
        self.assertEqual(r['primary_selected_test']['model'],'drift')

    def test_signed_negative_series_allowed(self):
        self.assertEqual(e.point_forecasts(['-1','-2'],'mean',[1],1),[Q('-1.5')])

    def test_manual_distribution_reject_nonfinite(self):
        with self.assertRaises(ValueError):e.distribution_score(dict(actual='NaN',quantiles=[],intervals=[]))


for item in F['forecasts']:
    def test(self,item=item):
        self.assertEqual(list(map(str,e.point_forecasts(item['train'],item['model'],item['horizons'],item['season']))),item['expected'])
    setattr(Forecasting,'test_frozen_'+item['id'].replace('.','_'),test)

for name,q in invalid_requests().items():
    def test(self,q=q):
        with self.assertRaises((ValueError,TypeError,KeyError)):e.read(q)
    setattr(Forecasting,'test_reject_'+name.replace('-','_'),test)


if __name__=='__main__':unittest.main()
