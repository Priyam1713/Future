"""Accepted/rejected CLI cases and exact JSON/Markdown replay."""
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from tests.test_ai_predictive_modeling import forecast_request,invalid_requests
from scripts.verify_ai_predictive_modeling import req,dataset,plan,sha,F

ROOT=Path(__file__).resolve().parents[1]


def examples():
    good={'reference':req('reference')}
    for x in F['forecasts']:
        d=dataset(x['train']);good[x['id']]=forecast_request(d,model=x['model'],origin=d['series'][0]['observations'][-1]['period'],horizons=x['horizons'],seasonal_period=x['season'])
    good['constant']=forecast_request(dataset(['5']*8),model='seasonal_naive_m4',seasonal_period=4,origin='2020-08',horizons=[1,4,5,13])
    good['missing-outcome']=forecast_request(dataset(['1','2','3']),horizons=[1,12,13])
    good['structural-break']=forecast_request(dataset(['1','1','1','100','100','100']),horizons=[1,2,3])
    d=dataset();good['prefix-original']=forecast_request(d,horizons=[1,2,3])
    changed=copy.deepcopy(d)
    for row in changed['series'][0]['observations']:
        if row['period']>'2020-03':row['value']='99999999'
    good['future-sentinel']=forecast_request(changed,horizons=[1,2,3])
    good['rolling']=req('evaluate',dataset=d,dataset_sha256=sha(d),plan=plan())
    missing=dataset(['1','2','3',None,'5','6'])
    good['missing-evaluation-target']=req('evaluate',dataset=missing,dataset_sha256=sha(missing),plan=plan())
    good['failed-candidates']=req('evaluate',dataset=d,dataset_sha256=sha(d),plan=plan(['seasonal_naive_m12','naive','unknown'],12))
    p=plan(['naive','mean']);p['validation_origins']=['2019-12','2020-01'];p['test_origins']=['2020-02','2020-03']
    good['ineligible-origin']=req('evaluate',dataset=d,dataset_sha256=sha(d),plan=p)
    zeros=dataset(['0']*8)
    good['zero-reference-tie']=req('evaluate',dataset=zeros,dataset_sha256=sha(zeros),plan=plan(['mean','naive']))
    multi=copy.deepcopy(d);s=copy.deepcopy(multi['series'][0]);s['id']='synthetic2'
    for row in s['observations']:row['value']=str(int(row['value'])*10)
    multi['series'].append(s);good['multiple-series']=req('evaluate',dataset=multi,dataset_sha256=sha(multi),plan=plan())
    for name,training,actual,pred in [('metric-known',['1','2','3'],['2','2'],['1','4']),('n0',[],[],[]),
                                    ('zero-scale',['0','0'],['1'],['0']),('zero-wape',['1','2'],['0'],['1']),
                                    ('partial-metrics',['1','2'],['2',None],['1','3'])]:
        good[name]=req('metrics',scoring=dict(training=training,actual=actual,predictions=pred,seasonal_period=1))
    source=F['source_scoring'];scoring=dict(actual=source['actual'],quantiles=[dict(p=source['p'],forecast=source['q'])],intervals=[{k:source[k] for k in ('alpha','lower','upper')}])
    good['source-distribution-score']=req('score-distribution',scoring=scoring)
    for name,y in [('lower-endpoint',source['lower']),('upper-endpoint',source['upper'])]:
        s=copy.deepcopy(scoring);s['actual']=y;good[name]=req('score-distribution',scoring=s)
    unicode=copy.deepcopy(d);unicode['provenance']['notes']='  Cafe\u0301 🪁\t\n`````json\n<script>raw</script>'
    good['unicode-whitespace']=forecast_request(unicode)
    good['report-replay']=req('report',request=good['metric-known'])
    good['noaa-benchmark']=json.loads((ROOT/'data/ai-predictive-modeling-noaa-benchmark-input.json').read_text(encoding='utf-8'))
    bad=invalid_requests()
    s=copy.deepcopy(scoring);s['quantiles']=[dict(p='0.1',forecast='4'),dict(p='0.9',forecast='3')];bad['crossing-quantiles']=req('score-distribution',scoring=s)
    s=copy.deepcopy(scoring);s['quantiles'][0]['p']='0';bad['invalid-quantile-level']=req('score-distribution',scoring=s)
    s=copy.deepcopy(scoring);s['intervals'][0].update(lower='800',upper='700');bad['reversed-interval']=req('score-distribution',scoring=s)
    s=copy.deepcopy(scoring);s['intervals'][0]['alpha']='1';bad['invalid-interval-alpha']=req('score-distribution',scoring=s)
    p=plan();p['horizons']=[1,2];bad['validation-label-leak']=req('evaluate',dataset=d,dataset_sha256=sha(d),plan=p)
    p=plan();p['models']*=2;bad['duplicate-candidate']=req('evaluate',dataset=d,dataset_sha256=sha(d),plan=p)
    bad['no-local-weights']=forecast_request(model='chronos-2',weights_path='not-acquired')
    bad['quantum-unsupported']=req('quantum-predict')
    return good,bad


def run(write=False):
    good,bad=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'request.json')
        for rejected,rows in [(False,good),(True,bad)]:
            for name,q in rows.items():
                raw=json.dumps(q,ensure_ascii=False,indent=2)+'\n';input_path=ROOT/f'data/ai-predictive-modeling-{name}-input.json'
                if write:input_path.write_text(raw,encoding='utf-8')
                else:assert input_path.read_text(encoding='utf-8')==raw,name
                path.write_text(raw,encoding='utf-8');values=[]
                for fmt in ('json','markdown'):
                    cp=subprocess.run([sys.executable,'-m','future','ai-predictive-modeling',str(path),'--format',fmt],cwd=ROOT,capture_output=True)
                    assert cp.returncode==(2 if rejected else 0),(name,cp.stderr.decode(errors='replace'))
                    out=cp.stdout.decode('utf-8').replace('\r\n','\n').rstrip('\n')+'\n'
                    value=json.loads(out) if fmt=='json' else json.loads(re.search(r'(`{3,})json\n(.*?)\n\1',out,re.S)[2]);values.append(value)
                    target=ROOT/f'data/ai-predictive-modeling-{name}.{ "json" if fmt=="json" else "md"}'
                    if write:target.write_text(out,encoding='utf-8')
                    else:assert target.read_text(encoding='utf-8')==out,('replay',name,fmt)
                    cases.append(dict(name=name,format=fmt,rejected=rejected,passed=True))
                assert values[0]==values[1]
        for raw in ('{"schema_version":1,"schema_version":1}', '{"schema_version":1,"task":NaN}'):
            path.write_text(raw,encoding='utf-8')
            for fmt in ('json','markdown'):
                cp=subprocess.run([sys.executable,'-m','future','ai-predictive-modeling',str(path),'--format',fmt],cwd=ROOT,capture_output=True)
                assert cp.returncode==2
                cases.append(dict(name='strict-json',format=fmt,rejected=True,passed=True))
    out=dict(passed=True,count=len(cases),accepted_pairs=len(good),rejected_pairs=len(bad),exact_replay=True,cases=cases)
    if write:(ROOT/'data/ai-predictive-modeling-cli-smoke.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(f'{len(cases)} AI Predictive Modeling CLI cases passed;{len(good)}accepted/{len(bad)}rejected JSON/Markdown pairs;full NOAA ledger replayed')
    return out


if __name__=='__main__':run('--write' in sys.argv)
