"""Independent frozen-table, exhaustive composition and rational-score oracle."""
import copy,hashlib,itertools,json
from datetime import datetime,timedelta,timezone
from fractions import Fraction as Q
from pathlib import Path
from future import intuitive_prediction as engine

ROOT=Path(__file__).resolve().parents[1]
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
def sha(v):return hashlib.sha256(canonical(v)).hexdigest()
F=json.loads((ROOT/'tests/fixtures/intuitive_prediction_reference_v1.json').read_text(encoding='utf-8'))
def check(a,b):assert a==b,(a,b)
def decision(cues=None,states=None,direction='positive',tie='abstain'):
    d=copy.deepcopy(F['decision'])
    if cues is not None:d.update(profile='gigerenzer-goldstein1996-ttb-deterministic-v1',cues=copy.deepcopy(cues),recognition=states or ['recognized']*2,tie_policy=tie)
    elif states is not None:d['recognition']=states
    d['ecological_direction']=direction
    return engine.decision(d)
def build(plan=None,ff=None,rr=None):
    l=engine.create(copy.deepcopy(plan or F['plan']))
    for f in copy.deepcopy(F['forecasts'] if ff is None else ff):l=engine.append(l,'forecast',f)
    for r in copy.deepcopy(F['resolutions'] if rr is None else rr):l=engine.append(l,'resolve',r)
    return l
def reject(call):
    try:call()
    except (ValueError,TypeError,KeyError):return
    raise AssertionError('Invalid configuration accepted')
def run():
    frozen=json.loads((ROOT/'data/intuitive-prediction-fixture-freeze.json').read_text())
    check(sha(F),frozen['fixture_sha256']);check(engine.PROFILE_HASH,F['profile_sha256'])
    check(sha(F['plan']),F['expected_plan_sha256'])
    check([sha(x) for x in F['forecasts']],F['expected_original_sha256'])
    families={}
    # Independent recognized-state truth cases, separate from engine branch logic.
    choices=[(['recognized','unrecognized'],'positive','A'),(['recognized','unrecognized'],'negative','B'),
             (['unrecognized','recognized'],'positive','B'),(['unrecognized','recognized'],'negative','A'),
             (['recognized']*2,'positive',None),(['unrecognized']*2,'positive',None),(['unknown','recognized'],'positive',None),(['recognized','unknown'],'positive',None)]
    for states,direction,expected in choices:check(decision(states=states,direction=direction)['selected'],expected)
    families['recognition-choice']=len(choices)
    for case in F['source_worked']:
        d=copy.deepcopy(F['decision']);d.update(profile='gigerenzer-goldstein1996-ttb-deterministic-v1',alternatives=case['alternatives'],recognition=['recognized']*2,cues=case['cues'])
        r=engine.decision(d);check(r['selected'],case['selected']);check([c['cue']['cue_id'] for c in r['inspected']],case['inspected'])
    families['source-worked-ttb']=2
    table={(x,y):winner for x,y,winner in F['cue_pairs']}
    check(sum(v is not None for v in table.values()),4)
    template=copy.deepcopy(F['search_stop']['cues'])
    for x,y,winner in F['cue_pairs']:
        c=copy.deepcopy(template[0]);c['values']=[x,y];check(decision([c])['selected'],winner)
    families['missing-cues']=9
    # All 9^3 ordered three-cue cases: expected choice and exact visited prefix
    # composed only from the frozen nine-entry truth table, not production outputs.
    exhaustive=0
    for pairs in itertools.product(list(table),repeat=3):
        cues=copy.deepcopy(template)
        for c,pair in zip(cues,pairs):c['values']=list(pair)
        expected=None;prefix=[]
        for i,pair in enumerate(pairs):
            prefix.append('c'+str(i+1))
            if table[pair] is not None:expected=table[pair];break
        r=decision(cues);check(r['selected'],expected);check([c['cue']['cue_id'] for c in r['inspected']],prefix);exhaustive+=1
    families['search-stop']=exhaustive
    tied=copy.deepcopy(template[:2]);tied[1]['validity']=tied[0]['validity']
    check(decision(tied)['reason'],'ambiguous_validity_tie');check(decision(tied,tie='frozen_order')['selected'],'B');check(decision([])['selected'],None)
    families['ties-abstention']=3
    reject(lambda:decision(template,direction='negative'))
    for key,value in [('validity','0.4'),('orientation','negative'),('provenance','')]:
        invalid=copy.deepcopy(template);invalid[0][key]=value;reject(lambda:decision(invalid))
    families['invalid-direction']=4
    for value in ['NaN','Infinity','-0.1','1.1',True,False,0.5,'1e-1',' 0.1']:
        ff=copy.deepcopy(F['forecasts']);ff[0]['probability']=value;reject(lambda:build(ff=ff))
    # Exercise actual ledger scorer for every frozen rational case.
    for case in F['rational_grid']:
        pl=copy.deepcopy(F['plan']);pl['slots']=pl['slots'][:1];pl['events']=pl['events'][:1]
        ff=copy.deepcopy(F['forecasts'][:1]);ff[0]['probability']=case['probability']
        rr=copy.deepcopy(F['resolutions'][:1]);rr[0]['outcome']=case['outcome']
        check(engine.evaluate(build(pl,ff,rr))['brier']['exact'],case['loss'])
    families['probability-boundaries']=len(F['rational_grid'])+9
    r=engine.evaluate(build());check(r['brier']['exact'],F['brier']['mean']);check(r['two_category_positive_quadratic']['exact'],F['brier']['two_category_mean'])
    check([x['loss']['exact'] for x in r['forecasts']],F['brier']['losses']);families['exact-brier']=6
    rr=copy.deepcopy(F['resolutions'])
    rr[0].update(status='unresolved',outcome=None);rr[1].update(status='disputed',outcome=None);rr[2].update(status='void',outcome=None);rr[3]['evidence']=None
    r=engine.evaluate(build(rr=rr));check(r['brier'],None);check(r['denominators']['excluded'],4);check(len(r['forecasts']),4)
    families['unresolved-denominator']=3
    l=build();v=copy.deepcopy(F['forecasts'][0]);v.update(parent_sha256=sha(v),at='2026-11-13T00:00:00Z',probability='1',outcome_known=True,reason='After outcome')
    r=engine.evaluate(engine.append(l,'forecast',v));check(r['brier']['exact'],'5/16');check(r['forecasts'][0]['selected_version_sha256'],F['expected_original_sha256'][0]);check(r['denominators']['versions'],5)
    temporal=0
    for case in F['chronology_cases']:
        ff=copy.deepcopy(F['forecasts'][:1]);rr=copy.deepcopy(F['resolutions'][:1]);pl=copy.deepcopy(F['plan']);pl['slots']=pl['slots'][:1];pl['events']=pl['events'][:1]
        pl['events'][0]['cutoff']='2026-11-11T00:00:01Z'
        base=datetime(2026,11,11,tzinfo=timezone.utc)
        ff[0]['at']=(base+timedelta(seconds=case['offset_seconds'])).isoformat()
        result=engine.evaluate(build(pl,ff,rr));check(result['forecasts'][0]['scored'],case['eligible']);temporal+=1
    families['forecast-versions']=3+temporal
    # N=2 versus N=20 retain identical averages but distinct denominators.
    for n in [2,20]:
        pl=copy.deepcopy(F['plan']);pl['events']=[];pl['slots']=[];ff=[];rr=[]
        for i in range(n):
            eid='event'+str(i);fid='forecast'+str(i)
            e=copy.deepcopy(F['plan']['events'][0]);e['event_id']=eid;e['dependency_group']=eid;pl['events'].append(e)
            pl['slots'].append(dict(forecast_id=fid,forecaster='person1',event_id=eid))
            f=copy.deepcopy(F['forecasts'][0]);f.update(forecast_id=fid,probability='0.8');ff.append(f)
            r=copy.deepcopy(F['resolutions'][0]);r.update(event_id=eid,outcome=i%2);rr.append(r)
        result=engine.evaluate(build(pl,ff,rr));b=result['calibration'][8]
        check((b['count'],b['events'],b['mean_probability']['exact'],b['observed_frequency']['exact']),(n,n//2,'4/5','1/2'));check(result['calibration'][0]['observed_frequency'],None)
    families['calibration-small-N']=4
    pl=copy.deepcopy(F['plan']);pl['events']=pl['events'][:2];pl['slots']=pl['slots'][:2]
    pl['baseline']=dict(probability='0.25',frozen_at='2026-11-08T00:00:00Z',domain=pl['domain'],horizon=pl['horizon'],event_definition=pl['event_definition'],
        training_start='2026-11-01T00:00:00Z',training_end='2026-11-07T00:00:00Z',training_outcomes=[dict(event_id='train'+str(i),outcome=y) for i,y in enumerate([0,0,0,1])],evidence=F['evidence'])
    ff=copy.deepcopy(F['forecasts'][:2]);rr=copy.deepcopy(F['resolutions'][:2])
    for f,q in zip(ff,['0.1','0.9']):f['probability']=q
    for r,y in zip(rr,[0,1]):r['outcome']=y
    result=engine.evaluate(build(pl,ff,rr));check(result['baseline']['brier']['exact'],'5/16');check(result['brier']['exact'],'1/100');check(result['baseline']['paired_absolute_improvement']['exact'],'121/400')
    bad=copy.deepcopy(pl);bad['baseline']['training_outcomes'][0]['event_id']='e1';reject(lambda:engine.create(bad))
    # Zero-loss reference stays a paired loss; no division-based BSS is emitted.
    zero=copy.deepcopy(pl);zero['baseline']['probability']='0'
    for t in zero['baseline']['training_outcomes']:t['outcome']=0
    rz=copy.deepcopy(rr)
    for x in rz:x['outcome']=0
    check(engine.evaluate(build(zero,ff,rz))['baseline']['brier']['exact'],'0')
    families['baseline-heldout']=5
    check(decision()['probability_generated'],False)
    ff=copy.deepcopy(F['forecasts']);ff[0].update(probability='0',confidence='Certain!')
    result=engine.evaluate(build(ff=ff));check(result['forecasts'][0]['loss']['exact'],'1');families['confidence-performance']=2
    d=copy.deepcopy(F['decision']);d['context']['environment_changed']=True
    review=engine.decision(d)['domain_review'];check(review['expert_certified'],False);assert any('environment_changed' in x for x in review['warnings'])
    families['nonstationary-domain']=2
    l=build();bad=copy.deepcopy(l);bad['actions'][0]['payload']['notes']+='x';reject(lambda:engine.evaluate(bad))
    badr=copy.deepcopy(F['resolutions']);badr[0]['evidence']['permission']='';reject(lambda:build(rr=badr))
    q=dict(schema_version=1,task='report',ledger=l);check(engine.read(q),engine.read(q));assert 'json\n' in engine.markdown(engine.read(q))
    families['replay-rights-separation']=4
    check(set(families),set(F['families']))
    out=dict(passed=True,profile_sha256=F['profile_sha256'],fixture_sha256=sha(F),fixture_commit='d212583',
        families=[dict(id=k,passed=True,checks=families[k]) for k in F['families']],ordered_cue_pairs=9,discriminating_pairs=4,exhaustive_three_cue_cases=exhaustive,
        frozen_rational_ledger_scores=42,chronology_cases=temporal,source_worked_examples=2,original_hashes=4,
        baseline_known_answer='121/400',empirical_human_validation=False,method='Frozen pre-engine tables/rational constants;independent SHA/Fraction arithmetic;production only supplies actual results,never expected values.')
    (ROOT/'data/intuitive-prediction-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('15independent families;9cue pairs;729three-cue traces;42actual-ledger rational scores;chronology and baseline known answers passed')
if __name__=='__main__':run()
