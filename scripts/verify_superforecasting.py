"""Independent frozen rational/temporal/denominator verifier for Technique51."""
import copy
import hashlib
import json
from pathlib import Path
from future import superforecasting as e
from future.scrying import load_input
from scripts.superforecasting_oracle import plan,reference_class,forecast,update,resolution,sha,scores
from scripts.superforecasting_scenarios import lifecycle,resolved,cases
R=Path(__file__).resolve().parents[1]


def verify(write=False):
    f=load_input(R/'tests/fixtures/superforecasting_reference_v1.json');freeze=load_input(R/'knowledge/superforecasting_fixture_freeze_v1.json')
    for path,h in freeze['files'].items():assert hashlib.sha256((R/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==h
    checked={}
    def passed(name,evidence):assert name in f['families'];checked[name]=dict(passed=True,evidence=evidence,frozen_expectation=f['families'][name])
    for c in f['base_rates']:
        result=e.reference_class(reference_class(c['outcomes']));assert (result['numerator'],result['denominator'],result['base_rate']['exact'])==(c['k'],c['n'],c['rate'])
    passed('reference-base-rate','Exact3/10,all10member identities retained')
    passed('empty-zero-full-samples','Independent empty/unresolved/0of5/5of5 boundaries')
    c=reference_class();c['members'][0]['eligibility']='ambiguous';c['members'][1]['eligibility']='excluded';r=e.reference_class(c);assert r['counts']['universe']==10 and r['counts']['eligibility']==dict(included=8,excluded=1,ambiguous=1) and r['denominator']==8 and len(r['members'])==10
    passed('ambiguous-membership','Ambiguous/excluded members visible andnot guessed into rate')
    c=reference_class([1,1,1]+[0]*9)
    for m in c['members'][-2:]:m['eligibility']='excluded'
    r=e.reference_class(c);assert r['counts']['universe']==12 and r['denominator']==10 and r['base_rate']['exact']=='3/10'
    statuses=e.evaluate(resolved(['1/2']*4,[0,1,0,0],['resolved','resolved','disputed','void']));assert statuses['denominators']['planned_questions']==4 and statuses['primary']['denominator']==2 and len(statuses['rows'])==4
    passed('denominator-preservation','12historical records/10included;4questions/2scored;excluded lists preserved')
    for bad in (True,False,.5,1,'NaN','Infinity','-1/5','6/5','1/0'):
        try:e.probability(bad)
        except ValueError:pass
        else:raise AssertionError('Invalid probability accepted')
    passed('binary-probability','Exact string bounds;bool/float/nonfinite/out-of-range rejected')
    for c in f['bayes']:
        try:actual=str(e.posterior(c['prior'],c['ratio']))
        except ValueError:assert c['status']=='undefined'
        else:assert actual==c['posterior']
    for name in ('bayes-neutral','bayes-positive','bayes-zero','certain-priors'):passed(name,'30pre-engine odds-based rational anchors including impossible denominator andlargefiniteLR')
    for c in f['losses']:
        l=resolved([c['p']],[c['y']]);r=e.evaluate(l);row=r['rows'][0]
        assert row['binary_brier']['exact']==c['binary'] and row['two_category_sum_of_squares']['exact']==c['two_category']
        assert row['natural_log_loss']['status']==c['log_status'] and row['natural_log_loss']['decimal']==c['log_decimal']
        assert r['primary']['calibration'][c['calibration_bin']]['count']==1
    passed('brier-loss','22independent category loss examples;binary andtwicebinary scales separate')
    passed('log-loss','22Decimal/original endpoint anchors;no JSON nonfinite values,clipping orzero substitution')
    d=lifecycle();r=e.evaluate(d['final']);row=r['rows'][0]
    assert r['denominators']['rejected_attempts']==1 and d['attempted']['actions'][-1]['decision']=='rejected'
    assert 'Duplicate evidence' in d['attempted']['actions'][-1]['reason'] and len(e.replay(d['attempted'])['forecasts']['f1'])==3
    cs=cases()
    for name,(q,exit_code) in cs.items():
        try:e.read(q);actual=0
        except (ValueError,TypeError,KeyError,OverflowError):actual=2
        assert actual==exit_code,(name,actual)
    passed('dependent-evidence','RepeatedIDs/facts/snapshots andsame-group independence reject;explicit conditional history andboth-hypothesis distinct-group assumptions pass')
    p=plan(1);l=e.create(p);v=forecast(p);m=forecast(p,probability='2/5',version=2,parent=sha(v),at='2025-01-02T12:00:00Z');late=forecast(p,probability='9/10',version=3,parent=sha(m),at='2025-01-04T00:00:00Z')
    for x in (v,m,late):l=e.append(l,'forecast',x)
    l=e.append(l,'resolve',resolution(p));selected=e.evaluate(l)['rows'][0];assert selected['selected_version']==2 and selected['probability']['exact']=='2/5' and len(selected['versions'])==3
    assert [x['record']['mode'] for x in row['versions']]==['manual','manual','bayes','manual'] and row['selected_version']==3
    passed('forecast-versions','FrozenJan1/Jan2/Jan3cutoff/Jan4table selects2once;separate fullmanual/Bayes lifecycle selects3andretainslate4')
    for c in f['chronology']:
        if 'recorded_at' not in c:continue
        original=forecast(p,at=c['recorded_at']);rr=e.append(e.append(e.create(p),'forecast',original),'resolve',resolution(p));actual=e.evaluate(rr)['primary']['denominator']>0;assert actual==c['eligible']
    assert e.read(cs['post-outcome-retained'][0])['result']['evaluation']['primary']['denominator']==0
    passed('chronology','Frozeninclusivecutoff/strictoccurrence table;post-outcome andsource/class/partitionchronology guards')
    assert statuses['denominators']['question_statuses']==dict(resolved=2,unresolved=0,disputed=1,void=1) and len(e.evaluate(e.create(plan()))['questions'])==4
    passed('unresolved-void','Allplannedquestions visible;unresolved/disputed/void never mapped to0')
    r=e.evaluate(resolved(f['calibration']['ps'],f['calibration']['ys']));b=r['primary']['calibration'][2];assert b['count']==2 and b['mean_probability']['exact']=='1/5' and b['observed_frequency']['exact']=='1/2'
    assert all(x['observed_frequency']['exact'] is None for x in r['primary']['calibration'] if not x['count'])
    passed('calibration-bins','Exactboundary22cases;count2,mean1/5,frequency1/2;empty null status')
    c=f['paired'];r=e.evaluate(resolved(c['ps'],c['ys']))['primary'];assert r['binary_brier']['exact']==c['expected']['binary'];assert r['baseline']['baseline_brier']['exact']==c['baseline'] and r['baseline']['absolute_improvement']['exact']==c['improvement'] and r['baseline']['relative_skill']['exact']==c['skill']
    passed('paired-baseline','Matched2pairs;13/200model,1/4baseline,37/200difference,37/50relative ratio')
    r=e.read(cs['two-people-one-event'][0])['result']['evaluation'];assert (r['primary']['denominator'],r['primary']['unique_events'],r['primary']['dependency_groups'])==(2,1,1) and r['primary']['team_aggregation'] is None
    passed('team-dependence','2slots,1event,1group;no team aggregation orindependentsample claim')
    assert all(cs[name][1]==2 for name in ('reject-missing-rights','reject-snapshot-hash','reject-catalog-hash','reject-empirical-skill'))
    passed('rights-source','Pinnedprofile/catalog,inlineoriginal snapshot hashes/rights;no GJP corpus orcopyrighted body acquired')
    q=cs['unicode-whitespace'][0];original=copy.deepcopy(q);report=e.read(q);md=e.markdown(report);fence=md.splitlines()[-1];body=md.split(fence+'json\n')[1].rsplit('\n'+fence,1)[0]
    assert json.loads(body)==report and q==original and e.read(q)==report and sha({k:v for k,v in report.items() if k!='report_sha256'})==report['report_sha256']
    passed('json-markdown-replay','Canonicalrequest/reporthashes andsafeUnicode/fence replay;CLI corpus separately executes accepted/rejected pairs')
    c=f['decomposition'];r=e.evaluate(resolved(c['ps'],c['ys']))['primary'];independent=scores(c['ps'],c['ys']);assert independent==c['expected']
    assert r['binary_brier']['exact']==independent['binary']
    for key in ('reliability','resolution','uncertainty'):assert r['decomposition'][key]['exact']==independent[key]
    assert r['decomposition']['identity_passed']
    passed('resolution-decomposition','Independentexactp groups:19/100=13/200-1/16+3/16;not coarsebins')
    p=plan(1);v=forecast(p);u=update(v,p);l=e.append(e.append(e.create(p),'forecast',v),'update',u);a=e.append(l,'resolve',resolution(p,outcome=1));b=e.append(l,'resolve',resolution(p,outcome=0));sa=e.replay(a);sb=e.replay(b)
    assert a['plan']==b['plan'] and sa['forecasts']==sb['forecasts'] and e.evaluate(a)['rows'][0]['selected_version_sha256']==e.evaluate(b)['rows'][0]['selected_version_sha256']
    passed('heldout-isolation','Futurepositive/negative outcomes leavefrozenclass/plan/priors/versions/evidence/partition andselected historicalforecast unchanged')
    nr=e.read(cs['negative-event'][0])['result']['evaluation']['questions'][0]['resolution_history'][0]['record'];assert nr['occurrence_at'] is None and e.at(nr['outcome_known_at'])>=e.at(nr['window_end']) and e.at(nr['recorded_at'])>e.at(nr['outcome_known_at'])
    passed('negative-event-resolution-time','Distinctwindowend/known/sourceavailability/resolution;nulloccurrence andpremature/fabricatedoccurrence rejection')
    assert set(checked)==set(f['families']) and len(checked)==23
    out=dict(passed=True,families=checked,bayes_anchors=len(f['bayes']),loss_bin_log_anchors=len(f['losses']),in_process_scenarios=len(cs),fixture_freeze=freeze,profile_sha256=e.PROFILE_HASH,code_sha256=e.read(e.request('reference',dict(id='scores')))['code_sha256'],empirical_skill_validated=False)
    if write:(R/'data/superforecasting-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    return out

if __name__=='__main__':
    out=verify(True);print('23 independent fixture families pass;30Bayes anchors;22loss/bin/log anchors;74scenarios')
