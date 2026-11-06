"""Pre-production independent closed-form rational oracle. No engine imports."""
from fractions import Fraction as Q
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def value(history, model, horizon, season=12):
    # Closed-form weight expansion is independent of production SES recursion.
    n = len(history)
    if model.startswith('ses_alpha'):
        a = Q(model.split('alpha')[1].split('_')[0]); b = 1-a
        return b**(n-1)*history[0] + sum((a*b**(n-1-i)*history[i] for i in range(1, n)), Q(0))
    if model.startswith('seasonal_naive'):
        return (history[-season:]*((horizon+season-1)//season))[horizon-1]
    if model == 'drift':
        return history[-1] + Q(horizon, n-1)*(history[-1]-history[0])
    if model == 'mean':
        return sum(history, Q(0))/n
    if model == 'naive':
        return history[-1]
    raise ValueError('Unknown reference model')


def origins(first_year):
    return [f'{first_year}-12'] + [f'{y}-{m:02d}' for y in (first_year+1, first_year+2) for m in range(1, 13)]


def benchmark():
    d = json.loads((ROOT/'resources/ai-predictive-modeling/noaa_mlo_2000_2023.json').read_text(encoding='utf-8'))
    models = json.loads((ROOT/'data/ai-predictive-modeling-evaluation-design.json').read_text(encoding='utf-8'))['candidate_order']
    months = [r['period'] for r in d['observations']]; ys = [Q(r['value']) for r in d['observations']]
    out = {}
    for partition, year in [('validation', 2017), ('test', 2020)]:
        out[partition] = {}
        for model in models:
            predictions = []; errors = []; scaled = []; actuals = []; per_h = {h: [] for h in range(1, 13)}
            for origin in origins(year):
                n = months.index(origin)+1; prefix = ys[:n]
                scale = sum((abs(prefix[i]-prefix[i-12]) for i in range(12, n)), Q(0))/(n-12)
                # Compute flat SES/mean once; unlike the engine this uses direct weights.
                flat = value(prefix, model, 1) if model.startswith('ses') or model == 'mean' else None
                for h in range(1, 13):
                    pred = flat if flat is not None else value(prefix, model, h)
                    predictions.append([origin, h, months[n+h-1], str(pred)])
                    e = ys[n+h-1]-pred; errors.append(e); scaled.append(abs(e)/scale); actuals.append(ys[n+h-1]); per_h[h].append(e)
            count = len(errors)
            out[partition][model] = dict(prediction_sha256=sha(predictions), count=count,
                mae=str(sum(map(abs, errors), Q(0))/count), mse=str(sum((e*e for e in errors), Q(0))/count),
                bias=str(sum(errors, Q(0))/count), mase=str(sum(scaled, Q(0))/count),
                wape=str(sum(map(abs, errors), Q(0))/sum(map(abs, actuals), Q(0))),
                horizon_mae={str(h): str(sum(map(abs, es), Q(0))/len(es)) for h, es in per_h.items()})
    selected = min(models, key=lambda m: (Q(out['validation'][m]['mae']), models.index(m)))
    return dict(scores=out, selected=selected, methods='Independent geometric SES expansion,endpoint drift,cycle replication and rational arithmetic;full4200prediction commitments frozen before production.')


def freeze():
    a = json.loads((ROOT/'knowledge/ai_predictive_modeling_resource_audit.json').read_text(encoding='utf-8'))
    profile = json.loads((ROOT/'knowledge/ai_predictive_modeling_profile_v1.json').read_text(encoding='utf-8'))
    f = dict(version=1, profile_sha256=sha(profile), families=[r['id'] for r in a['independent_fixture_plan']],
        forecasts=[dict(id='seasonal', train=['10','20','30','40','11','21','31','41'], model='seasonal_naive_m4', season=4, horizons=[1,2,3,4,5,6], expected=['11','21','31','41','11','21']),
                   dict(id='drift', train=['2','4','6','8'], model='drift', season=1, horizons=[1,2,3], expected=['10','12','14']),
                   dict(id='mean', train=['1','3','2','8'], model='mean', season=1, horizons=[1,2,3], expected=['7/2']*3),
                   dict(id='naive', train=['1','3','2','8'], model='naive', season=1, horizons=[1,2,3], expected=['8']*3),
                   *[dict(id='ses'+alpha, train=['1','3','2','8'], model='ses_alpha'+alpha+'_initial_y1', season=1, horizons=[1,2,3], expected=[answer]*3) for alpha, answer in [('0.2','352/125'),('0.5','5'),('0.8','853/125')]]] ,
        metrics=dict(train=['1','2','3'], actual=['2','2'], predictions=['1','4'], season=1, expected=dict(mae='3/2',mse='5/2',mase='3/2',bias='-1/2',wape='3/4',smape='200/3',scale='1',rmse='1.581138830084')),
        source_scoring=dict(p='0.1',q='744.54',actual='741.84',twice_pinball='243/50',lower='744.54',upper='773.22',alpha='0.2',interval_score='1392/25'),
        month_examples=[['2019-12',1,'2020-01'],['2020-02',12,'2021-02'],['2022-12',12,'2023-12']],
        validation_origins=origins(2017), test_origins=origins(2020),
        edge_expectations=dict(n0='null:no_scored_pairs',zero_scale='null:zero_training_scale',zero_wape='null:zero_actual_denominator',zero_reference='null:zero_reference_error',missing_target='missing_target',missing_training='model_failure',unsupported='unsupported_configuration',ineligible='ineligible_origin',invalid_quantiles='reject',invalid_interval='reject',endpoint_coverage=True),
        benchmark=benchmark(), provenance='Original synthetic cases and independent closed-form NOAA arithmetic. Source examples are arithmetic checks,not forecast-quality claims.')
    path = ROOT/'tests/fixtures/ai_predictive_modeling_reference_v1.json'
    path.write_text(json.dumps(f, indent=2)+'\n', encoding='utf-8')
    freeze = dict(fixture_sha256=sha(f), oracle_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), profile_sha256=sha(profile),
                  families=f['families'], cells=4200, selected_reference=f['benchmark']['selected'], production_written=False)
    (ROOT/'data/ai-predictive-modeling-fixture-freeze.json').write_text(json.dumps(freeze, indent=2)+'\n', encoding='utf-8')
    return freeze


if __name__ == '__main__':
    print(json.dumps(freeze(), indent=2))
