"""Offline exact CPU baseline forecasts and retrospective rolling evaluation."""
import copy
from decimal import Decimal, localcontext, ROUND_HALF_EVEN
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re

from .remote_viewing import digest, obj, text, identifier, integer, hexhash
from .scrying import load_input, freeze, thaw

ROOT = Path(__file__).resolve().parents[1]
PROFILE_HASH = 'ed2490bf3ddc5861b3a406e2ba8aa93b3f2b2fe33e0b7917371e5c26875e7fdb'


def assets():
    p = load_input(ROOT/'knowledge/ai_predictive_modeling_profile_v1.json')
    if digest(p) != PROFILE_HASH:
        raise ValueError('Pinned forecasting profile mismatch')
    for file, key in [('knowledge/ai_predictive_modeling_sources.json','source_manifest_sha256'),
                      ('knowledge/ai_predictive_modeling_source_freeze_v1.json','source_freeze_sha256'),
                      ('resources/ai-predictive-modeling/noaa_mlo_2000_2023.json','dataset_sha256'),
                      ('data/ai-predictive-modeling-evaluation-design.json','protocol_sha256')]:
        if digest(load_input(ROOT/file)) != p[key]:
            raise ValueError('Pinned source/data/protocol mismatch')
    return p


DATA = freeze(assets())
MODELS = tuple(c['id'] for c in DATA['candidates'])
VINTAGE = 'Retrospective evaluation on a fixed revised data snapshot;historical publication vintages are unverified. Software prefix isolation does not prove as-of historical data availability.'


def decimal(v):
    if not isinstance(v, str) or len(v) > 64 or re.fullmatch(r'-?(?:0|[1-9][0-9]{0,29})(?:\.[0-9]{1,24})?', v) is None:
        raise ValueError('Bounded plain finite decimal string required')
    return Q(v)


def display(v, reason=None, sqrt=False):
    if v is None:
        return dict(exact=None, decimal=None, reason=reason or 'not_estimable')
    v = Q(v)
    with localcontext() as ctx:
        ctx.prec = 80
        d = Decimal(v.numerator)/Decimal(v.denominator)
        if sqrt: d = d.sqrt()
        d = d.quantize(Decimal('0.000000000001'), rounding=ROUND_HALF_EVEN)
    return dict(exact=('sqrt('+str(v)+')') if sqrt else str(v), decimal=format(d, 'f'), reason=None)


def month(v):
    if not isinstance(v, str) or not re.fullmatch(r'[0-9]{4}-(?:0[1-9]|1[0-2])', v) or v[:4] == '0000':
        raise ValueError('Calendar month YYYY-MM required')
    return int(v[:4])*12 + int(v[5:])-1


def add_month(v, h):
    n = month(v)+h; y, m = divmod(n, 12)
    if not 1 <= y <= 9999: raise ValueError('Calendar month outside supported range')
    return f'{y:04d}-{m+1:02d}'


def sequence(v, maximum=1200, nonempty=False):
    if not isinstance(v, list) or len(v) > maximum or nonempty and not v:
        raise ValueError('Bounded list required')


def horizons(v):
    sequence(v, 120, True)
    for h in v: integer(h, 1, 120)
    if v != sorted(set(v)): raise ValueError('Sorted distinct horizons required')


def config(model, season):
    integer(season, 1, 120); identifier(model)
    if model in MODELS:
        if model == 'seasonal_naive_m12' and season != 12: raise ValueError('Seasonal model/period mismatch')
        return dict(id=model, version=1, family='ses' if model.startswith('ses') else 'seasonal_naive' if model.startswith('seasonal') else model,
                    alpha=model.split('alpha')[1].split('_')[0] if model.startswith('ses') else None,
                    seasonal_period=season if model.startswith('seasonal') else None,
                    initialization='first observation,then consume subsequent observations' if model.startswith('ses') else None)
    m = re.fullmatch(r'seasonal_naive_m([1-9][0-9]{0,2})', model)
    if m and int(m[1]) == season and season <= 120:
        return dict(id=model, version=1, family='seasonal_naive', alpha=None, seasonal_period=season, initialization=None)
    raise ValueError('Unsupported fixed model configuration')


def point_forecasts(values, model, hs, season):
    c = config(model, season); horizons(hs)
    if not values: raise ValueError('Insufficient history')
    if any(v is None for v in values): raise ValueError('Missing training target')
    ys = [decimal(v) for v in values]; n = len(ys)
    if c['family'] == 'seasonal_naive':
        if n < season: raise ValueError('Insufficient seasonal history')
        return [ys[n-season+(h-1)%season] for h in hs]
    if c['family'] == 'drift':
        if n < 2: raise ValueError('Insufficient drift history')
        slope = (ys[-1]-ys[0])/(n-1)
        return [ys[-1]+h*slope for h in hs]
    if c['family'] == 'mean': level = sum(ys, Q(0))/n
    elif c['family'] == 'naive': level = ys[-1]
    else:
        alpha = Q(c['alpha']); level = ys[0]
        for y in ys[1:]: level = alpha*y + (1-alpha)*level
    return [level for _ in hs]


def training_scale(values, season):
    if len(values) <= season: return None, 'insufficient_scale_history'
    if any(v is None for v in values): return None, 'missing_training_target'
    ys = [decimal(v) for v in values]
    s = sum((abs(ys[i]-ys[i-season]) for i in range(season, len(ys))), Q(0))/(len(ys)-season)
    return (s, None) if s else (None, 'zero_training_scale')


def validate_dataset(d, expected):
    obj(d, ('id','version','frequency','units','series','provenance'))
    identifier(d['id']); integer(d['version'], 1, 1)
    if d['frequency'] != 'monthly' or not text(d['units'], 200).strip(): raise ValueError('Monthly frequency/units required')
    hexhash(expected)
    if digest(d) != expected: raise ValueError('Dataset hash mismatch')
    p = d['provenance']; obj(p, ('source_ref','snapshot_sha256','rights','attribution','notes'))
    for k in ('source_ref','attribution'): 
        if not text(p[k]).strip(): raise ValueError('Source/attribution required')
    text(p['notes'])
    if p['snapshot_sha256'] is not None: hexhash(p['snapshot_sha256'])
    if p['rights'] not in ('public_domain','self_authored','permission_granted'): raise ValueError('Explicit source rights required')
    sequence(d['series'], 20, True); seen = set()
    for s in d['series']:
        obj(s, ('id','availability','observations')); identifier(s['id'])
        if s['id'] in seen: raise ValueError('Duplicate series ID')
        seen.add(s['id']); obj(s['availability'], ('status','vintage','notes'))
        if s['availability']['status'] not in ('unknown','declared_as_of'): raise ValueError('Availability status required')
        if s['availability']['vintage'] is not None: text(s['availability']['vintage'], 200)
        if s['availability']['status'] == 'declared_as_of' and not s['availability']['vintage']: raise ValueError('Declared vintage required')
        text(s['availability']['notes'])
        sequence(s['observations'], 1200, True); previous = None
        for row in s['observations']:
            obj(row, ('period','value')); now = month(row['period'])
            if previous is not None and now != previous+1: raise ValueError('Unique complete ordered monthly grid required')
            previous = now
            if row['value'] is not None: decimal(row['value'])
    return d


def noaa_dataset():
    raw = load_input(ROOT/'resources/ai-predictive-modeling/noaa_mlo_2000_2023.json')
    if digest(raw) != DATA['dataset_sha256']: raise ValueError('Pinned NOAA mismatch')
    return dict(id=raw['id'], version=1, frequency='monthly', units='ppm',
        provenance=dict(source_ref=raw['source_url'],snapshot_sha256=raw['source_file_sha256'],rights='public_domain',attribution=raw['attribution'],notes=raw['rights']),
        series=[dict(id='mlo_co2',availability=dict(status='unknown',vintage=raw['source_creation'],notes=VINTAGE),
                     observations=[dict(period=r['period'],value=r['value']) for r in raw['observations']])])


def forecast_cells(dataset, model, origin, hs, season, partition='forecast'):
    month(origin); horizons(hs); integer(season,1,120)
    cells = []; data_hash = digest(dataset)
    try: c = config(model, season); unsupported = False
    except ValueError: c = dict(id=model,version=None); unsupported = True
    for series in dataset['series']:
        rows = series['observations']; prefix = [r for r in rows if month(r['period']) <= month(origin)]
        lookup = {r['period']:r['value'] for r in rows}
        values = [r['value'] for r in prefix]; scale, scale_reason = training_scale(values,season)
        predictions = None; reason = None
        if unsupported: status, reason = 'unsupported_configuration','unsupported_model_or_season'
        elif origin not in lookup: status, reason = 'ineligible_origin','origin_not_in_series_grid'
        else:
            try: predictions = point_forecasts(values,model,hs,season); status = 'success'
            except ValueError as e: status, reason = 'model_failure',str(e)
        train_hash = digest(dict(series_id=series['id'], observations=prefix, cutoff=origin))
        for i,h in enumerate(hs):
            target = add_month(origin,h); actual = lookup.get(target); pred = None if predictions is None else predictions[i]
            y = None if actual is None else decimal(actual); e = None if pred is None or y is None else y-pred
            state = 'missing_target' if predictions is not None and y is None else status
            r = dict(model=c,profile=DATA['id'],profile_version=1,series_id=series['id'],dataset_sha256=data_hash,
                     source_sha256=dataset['provenance']['snapshot_sha256'],training_cutoff=origin,training_rows=len(prefix),training_prefix_sha256=train_hash,
                     origin=origin,horizon=h,target_period=target,partition=partition,status=state,reason='missing_evaluation_outcome' if state=='missing_target' else reason,
                     prediction=display(pred,'forecast_unavailable'),point_functional={'mean':'training arithmetic mean','naive':'last observed value','drift':'endpoint linear extrapolation','ses':'fixed-alpha final level','seasonal_naive':'last observed seasonal value'}.get(c.get('family'),'unsupported'),
                     actual=actual,error=display(e,'unscored'),absolute_error=display(None if e is None else abs(e),'unscored'),
                     squared_error=display(None if e is None else e*e,'unscored'),training_scale=display(scale,scale_reason),
                     scaled_absolute_error=display(None if e is None or scale is None else abs(e)/scale,scale_reason or 'unscored'))
            r['sha256'] = digest(r); cells.append(r)
    return cells


def _q(field):
    return None if field['exact'] is None else Q(field['exact'])


def metrics(cells, include_smape=False):
    scored = [c for c in cells if c['status']=='success' and c['error']['exact'] is not None]
    n = len(scored); errors = [_q(c['error']) for c in scored]
    loss = sum(map(abs,errors),Q(0)); squares = sum((e*e for e in errors),Q(0))
    scaled = [_q(c['scaled_absolute_error']) for c in scored if _q(c['scaled_absolute_error']) is not None]
    actual_sum = sum((abs(decimal(c['actual'])) for c in scored),Q(0))
    smape = []
    for c in scored if include_smape and n<=20 else []:
        y, pred = decimal(c['actual']), _q(c['prediction']); den = abs(y)+abs(pred)
        smape.append(200*abs(y-pred)/den if den else Q(0))
    counts = {s:sum(c['status']==s for c in cells) for s in ('success','missing_target','ineligible_origin','unsupported_configuration','model_failure')}
    scale_reasons={c['training_scale']['reason'] for c in scored if c['training_scale']['reason'] is not None}
    undefined_scale_reason=next(iter(scale_reasons)) if len(scale_reasons)==1 else 'no_defined_training_scales'
    return dict(planned=len(cells),scored=n,status_counts=counts,planned_distinct_target_months=len({(c['series_id'],c['target_period']) for c in cells}),
                distinct_target_months=len({(c['series_id'],c['target_period']) for c in scored}),
                mae=display(loss/n if n else None,'no_scored_pairs'),mse=display(squares/n if n else None,'no_scored_pairs'),
                rmse=display(squares/n if n else None,'no_scored_pairs',sqrt=True),bias=display(sum(errors,Q(0))/n if n else None,'no_scored_pairs'),
                mase=display(sum(scaled,Q(0))/len(scaled) if scaled else None,undefined_scale_reason if n else 'no_scored_pairs'),mase_count=len(scaled),
                undefined_scale_counts={reason:sum(c['training_scale']['reason']==reason for c in scored) for reason in ('zero_training_scale','insufficient_scale_history','missing_training_target')},
                wape=display(loss/actual_sum if actual_sum else None,'zero_actual_denominator' if n else 'no_scored_pairs'),
                absolute_smape_percent=display(sum(smape,Q(0))/n if smape else None,'manual_diagnostic_only_max20_pairs' if n else 'no_scored_pairs'),
                smape_convention='Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only.')


def paired(cells, reference):
    key = lambda c:(c['series_id'],c['origin'],c['horizon'])
    refs = {key(c):c for c in reference if c['status']=='success'}
    pairs = [(c,refs[key(c)]) for c in cells if c['status']=='success' and key(c) in refs]
    n = len(pairs)
    a = sum((_q(c['absolute_error']) for c,_ in pairs),Q(0))/n if n else None
    b = sum((_q(r['absolute_error']) for _,r in pairs),Q(0))/n if n else None
    return dict(common_scored=n,candidate_mae=display(a,'no_common_pairs'),reference_mae=display(b,'no_common_pairs'),
                candidate_minus_reference_mae=display(None if n==0 else a-b,'no_common_pairs'),
                ratio=display(a/b if n and b else None,'zero_reference_error' if n else 'no_common_pairs'),reference_model='seasonal_naive',
                direction='Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells.')


def validate_plan(p):
    obj(p, ('models','validation_origins','test_origins','horizons','seasonal_period','selection'))
    sequence(p['models'],20,True)
    for m in p['models']: identifier(m)
    if len(set(p['models'])) != len(p['models']): raise ValueError('Duplicate model candidate')
    integer(p['seasonal_period'],1,120); horizons(p['horizons'])
    for name in ('validation_origins','test_origins'):
        sequence(p[name],100,True); ids=[month(v) for v in p[name]]
        if ids != list(range(ids[0],ids[0]+len(ids))): raise ValueError('Ordered monthly origin schedule required')
    if month(p['validation_origins'][-1])+max(p['horizons']) > month(p['test_origins'][0]):
        raise ValueError('Validation targets unavailable at first test origin')
    if p['selection'] != 'validation_macro_mae_then_order': raise ValueError('Unsupported selection rule')


def evaluate(dataset,p):
    validate_plan(p)
    if len(dataset['series'])*len(p['models'])*(len(p['validation_origins'])+len(p['test_origins']))*len(p['horizons']) > 100000:
        raise ValueError('Evaluation cell budget exceeded')
    ledger = {}; summary = {}; selection = []
    for partition in ('validation','test'):
        ledger[partition] = []; summary[partition] = []
        for model in p['models']:
            cells = [c for origin in p[partition+'_origins'] for c in forecast_cells(dataset,model,origin,p['horizons'],p['seasonal_period'],partition)]
            ledger[partition].extend(cells)
            by_series = {s['id']:metrics([c for c in cells if c['series_id']==s['id']]) for s in dataset['series']}
            valid = [Q(m['mae']['exact']) for m in by_series.values() if m['mae']['exact'] is not None]
            macro = sum(valid,Q(0))/len(valid) if len(valid)==len(by_series) else None
            aggregate = metrics(cells)
            summary[partition].append(dict(model=model,aggregate=aggregate,by_series=by_series,macro_mae=display(macro,'series_without_scored_pairs'),
                by_horizon={str(h):metrics([c for c in cells if c['horizon']==h]) for h in p['horizons']}))
            if partition == 'validation':
                failures = sum(c['status'] not in ('success','missing_target') for c in cells)
                selection.append(dict(model=model,validation_macro_mae=display(macro,'series_without_scored_pairs'),eligible=macro is not None and failures==0,
                                      reason='forecast_failure_or_empty_series' if failures or macro is None else None))
        if partition == 'validation':
            eligible = [s for s in selection if s['eligible']]
            selected = min(eligible,key=lambda s:(Q(s['validation_macro_mae']['exact']),p['models'].index(s['model'])))['model'] if eligible else None
            selection_commitment = dict(selected=selected,candidates=copy.deepcopy(selection),tie_order=copy.deepcopy(p['models']),
                                        rule='Validation per-series macro MAE only;complete forecast coverage required. Test diagnostics never select.')
            selection_commitment['sha256'] = digest(selection_commitment)
        reference = [c for origin in p[partition+'_origins'] for c in forecast_cells(dataset,'seasonal_naive_m'+str(p['seasonal_period']),origin,p['horizons'],p['seasonal_period'],partition)]
        for row in summary[partition]:
            row['paired_seasonal_naive'] = paired([c for c in ledger[partition] if c['model']['id']==row['model']],reference)
    primary = next((r for r in summary['test'] if r['model']==selected),None)
    return dict(plan=copy.deepcopy(p),plan_sha256=digest(p),selection=selection_commitment,summary=summary,cells=ledger,primary_selected_test=copy.deepcopy(primary),
                test_all_candidates_role='Diagnostic reporting only;not a second selection stage.',
                weighting='Macro weights series equally;micro weights scored cells equally. With one series they coincide. MASE uses per-origin scales.',
                dependence='Forecast windows overlap;300cells/model/partition represent36distinct NOAA target months,not300independent trials. No naive significance tests.',vintage=VINTAGE)


def benchmark_plan():
    p = load_input(ROOT/'data/ai-predictive-modeling-evaluation-design.json')
    def origins(pair):
        return [add_month(pair[0],i) for i in range(month(pair[1])-month(pair[0])+1)]
    return dict(models=p['candidate_order'],validation_origins=origins(p['validation']['origins']),test_origins=origins(p['test']['origins']),
                horizons=p['horizons'],seasonal_period=12,selection='validation_macro_mae_then_order')


def distribution_score(v):
    obj(v, ('actual','quantiles','intervals')); y=decimal(v['actual']); sequence(v['quantiles'],100); sequence(v['intervals'],100)
    qs=[]; previous_p=Q(0); previous_q=None
    for r in v['quantiles']:
        obj(r,('p','forecast')); p=decimal(r['p']); q=decimal(r['forecast'])
        if not previous_p < p < 1 or previous_q is not None and q < previous_q: raise ValueError('Invalid/crossing quantiles')
        loss=(1-p)*(q-y) if y<q else p*(y-q)
        qs.append(dict(p=r['p'],forecast=r['forecast'],pinball=display(loss),fpp3_twice_pinball=display(2*loss)))
        previous_p,previous_q=p,q
    intervals=[]
    for r in v['intervals']:
        obj(r,('alpha','lower','upper')); alpha=decimal(r['alpha']); lo=decimal(r['lower']); hi=decimal(r['upper'])
        if not 0<alpha<1 or lo>hi: raise ValueError('Invalid interval')
        score=hi-lo+2/alpha*(lo-y if y<lo else y-hi if y>hi else 0)
        intervals.append(dict(declaration=copy.deepcopy(r),covered=lo<=y<=hi,score=display(score)))
    return dict(quantiles=qs,intervals=intervals,qualification='Manual reference scoring only;no point-model predictive distribution generated.')


def manual_metrics(v):
    obj(v,('training','actual','predictions','seasonal_period')); integer(v['seasonal_period'],1,120)
    for name in ('training','actual','predictions'): sequence(v[name])
    for x in v['training']:
        if x is not None: decimal(x)
    if len(v['actual'])!=len(v['predictions']): raise ValueError('Mismatched scoring lengths')
    scale,reason=training_scale(v['training'],v['seasonal_period']); cells=[]
    for i,(y,p) in enumerate(zip(v['actual'],v['predictions'])):
        a=None if y is None else decimal(y); b=None if p is None else decimal(p); e=None if a is None or b is None else a-b
        cells.append(dict(series_id='manual',target_period=str(i),status='success' if e is not None else 'missing_target',actual=y,
            prediction=display(b),error=display(e),absolute_error=display(None if e is None else abs(e)),squared_error=display(None if e is None else e*e),
            training_scale=display(scale,reason),scaled_absolute_error=display(None if e is None or scale is None else abs(e)/scale,reason)))
    return metrics(cells,include_smape=True)


def read(q, registry=None):
    assets()
    if not isinstance(q,dict) or type(q.get('schema_version')) is not int or q.get('schema_version')!=1:
        raise ValueError('Schema version1 required')
    tasks={'reference':(), 'forecast':('dataset','dataset_sha256','model','origin','horizons','seasonal_period'),
           'evaluate':('dataset','dataset_sha256','plan'), 'benchmark':(), 'metrics':('scoring',), 'score-distribution':('scoring',), 'report':('request',)}
    task=q.get('task')
    if task not in tasks: raise ValueError('Unsupported forecasting task')
    obj(q,('schema_version','task','profile','profile_version',*tasks[task]),('resource_evidence',))
    if q['profile']!=DATA['id'] or type(q['profile_version']) is not int or q['profile_version']!=1: raise ValueError('Unsupported profile/version')
    if registry is not None:
        for s in load_input(ROOT/'knowledge/ai_predictive_modeling_sources.json'): registry.add_source(s)
    if task=='report':
        if q['request'].get('task') not in ('forecast','evaluate','benchmark','metrics','score-distribution','reference'): raise ValueError('Nested replay unsupported')
        return read(q['request'],registry)
    if task=='reference': value=thaw(DATA)
    elif task in ('forecast','evaluate'):
        d=validate_dataset(q['dataset'],q['dataset_sha256'])
        if task=='forecast':
            config(q['model'],q['seasonal_period'])
            cells=forecast_cells(d,q['model'],q['origin'],q['horizons'],q['seasonal_period'])
            if any(c['status'] in ('model_failure','ineligible_origin') for c in cells): raise ValueError('Invalid forecast origin/training history')
            value=dict(cells=cells,dataset=copy.deepcopy(d),dataset_sha256=digest(d))
        else: value=dict(evaluation=evaluate(d,q['plan']),dataset=copy.deepcopy(d),dataset_sha256=digest(d))
    elif task=='benchmark':
        d=noaa_dataset(); validate_dataset(d,digest(d))
        value=dict(evaluation=evaluate(d,benchmark_plan()),dataset=copy.deepcopy(d),dataset_sha256=digest(d),
                   pinned_noaa_asset_sha256=DATA['dataset_sha256'],audit_protocol_sha256=DATA['protocol_sha256'])
    elif task=='metrics': value=manual_metrics(q['scoring'])
    else: value=distribution_score(q['scoring'])
    resource=q.get('resource_evidence')
    if resource is not None:
        obj(resource,('record','sha256'))
        if digest(resource['record'])!=resource['sha256']: raise ValueError('Resource evidence hash mismatch')
        if resource['record'].get('profile_sha256')!=PROFILE_HASH or resource['record'].get('code_sha256')!=hashlib.sha256(Path(__file__).read_bytes()).hexdigest():
            raise ValueError('Resource evidence profile/code mismatch')
    result=dict(status='accepted',task=task,profile=dict(id=DATA['id'],version=1,sha256=PROFILE_HASH),request_sha256=digest(q),
                source=load_input(ROOT/'knowledge/ai_predictive_modeling_source_freeze_v1.json'),result=value,
                code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),resource_evidence=copy.deepcopy(resource),
                resource_policy='Measured separately and frozen by hash;pure deterministic forecasts contain no fabricated runtime measurements.',vintage=VINTAGE,
                limits=['Fixed SES conventions are not optimized ETS','No ARIMA/trees/neural/Chronos operation or downloaded assets','No generated prediction intervals or guaranteed accuracy','All-candidate test scores are diagnostic;selection uses validation only','Exact absolute-sMAPE is a manual diagnostic for at most20scored pairs;omitted from benchmark aggregates to avoid impractical rational denominator growth'])
    result['report_sha256']=digest(result)
    return result


def markdown(r):
    raw=json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)
    fence='`'*max(3,max((len(x)+1 for x in re.findall(r'`+',raw)),default=0))
    lines=['# CPU forecasting workbench','',VINTAGE,'']
    e=r.get('result',{}).get('evaluation') if isinstance(r.get('result'),dict) else None
    if e:
        lines += ['Validation-selected model: '+str(e['selection']['selected']),'',
                  '| Candidate | Validation MAE | Test MAE | Test RMSE | Test MASE |','|---|---:|---:|---:|---:|']
        for v,t in zip(e['summary']['validation'],e['summary']['test']):
            lines.append('| '+v['model']+' | '+' | '.join(str(x) for x in [v['macro_mae']['decimal'],t['aggregate']['mae']['decimal'],t['aggregate']['rmse']['decimal'],t['aggregate']['mase']['decimal']])+' |')
        lines += ['',e['dependence'],'','All cells,failures,horizon scores and paired comparisons follow.','']
    return '\n'.join(lines+[fence+'json',raw,fence,''])
