"""CLI lifecycle and exact accepted/rejected JSON/Markdown replay."""
import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future import intuitive_prediction as p
from tests.test_intuitive_prediction import F,dec,ttb,study,tm,baseline_plan,baseline_study

ROOT=Path(__file__).resolve().parents[1]
def req(task,**kw):return dict(schema_version=1,task=task,**kw)
def examples():
    good={}
    for name,kw in [('positive',{}),('negative',dict(ecological_direction='negative')),('both',dict(recognition=['recognized']*2)),('neither',dict(recognition=['unrecognized']*2)),('unknown-recognition',dict(recognition=['recognized','unknown'])),('unknown-direction',dict(ecological_direction='unknown'))]:
        good[name]=req('recognition',decision=dec(**kw))
    for x in F['source_worked']:good[x['id']]=req('take-the-best',decision=ttb(alternatives=x['alternatives'],cues=x['cues']))
    good['early-stop']=req('take-the-best',decision=ttb())
    cues=copy.deepcopy(F['search_stop']['cues']);cues[1]['values']=['negative','unknown'];cues[2]['values']=['positive','negative']
    good['third-cue']=req('take-the-best',decision=ttb(cues=cues))
    for name,values in [('positive-unknown',['positive','unknown']),('negative-unknown',['negative','unknown'])]:
        c=copy.deepcopy(cues[:1]);c[0]['values']=values;good[name]=req('take-the-best',decision=ttb(cues=c))
    good['exhausted']=req('take-the-best',decision=ttb(cues=[]))
    tied=copy.deepcopy(cues[:2]);tied[1]['validity']=tied[0]['validity']
    good['tie-abstain']=req('take-the-best',decision=ttb(cues=tied));good['tie-frozen']=req('take-the-best',decision=ttb(cues=tied,tie_policy='frozen_order'))
    changed=dec();changed['context']['environment_changed']=True;good['nonstationary']=req('recognition',decision=changed)
    good['rpd-reference']=req('decision-reference',reference=dict(context=F['decision']['context'],rpd={k:'Human-declared contextual note' for k in ['cues_noticed','situation','expectancies','anomalies','candidate_action','mental_simulation','revision_or_alternative','feedback_history']}))
    good['exact-brier']=req('forecast-score',ledger=study());good['unresolved']=req('report',ledger=study(resolutions=[]))
    good['n0']=req('calibration',ledger=study(forecasts=[],resolutions=[]))
    rr=copy.deepcopy(F['resolutions']);rr[0].update(status='disputed',outcome=None);rr[1].update(status='void',outcome=None)
    good['disputed-void']=req('report',ledger=study(resolutions=rr))
    for name,q,y in [('zero-correct','0',0),('one-correct','1',1),('zero-wrong','0',1),('one-wrong','1',0)]:
        ff=copy.deepcopy(F['forecasts']);rr=copy.deepcopy(F['resolutions']);ff[0]['probability']=q;rr[0]['outcome']=y
        good[name]=req('report',ledger=study(forecasts=ff,resolutions=rr))
    ff=copy.deepcopy(F['forecasts']);ff[0]['probability']='0';ff[1]['probability']='1';good['bin-endpoints']=req('calibration',ledger=study(forecasts=ff))
    ff=copy.deepcopy(F['forecasts']);ff[1]['probability']='0.8';good['small-n']=req('calibration',ledger=study(forecasts=ff))
    l=study();v=copy.deepcopy(F['forecasts'][0]);v.update(parent_sha256=p.digest(v),at=tm(13),probability='1',outcome_known=True,reason='Known after outcome')
    good['late-amendment']=req('forecast-amend',ledger=l,forecast=v)
    l=study(resolutions=[]);v=copy.deepcopy(F['forecasts'][0]);v.update(parent_sha256=p.digest(v),at=tm(10,1),probability='0.9',reason='Before outcome')
    good['prospective-amendment']=req('forecast-amend',ledger=l,forecast=v)
    ff=copy.deepcopy(F['forecasts']);ff[0]['notes']='e\u0301  raw\n```<script>data</script>';good['unicode-whitespace']=req('report',ledger=study(forecasts=ff))
    good['baseline']=req('baseline-compare',ledger=baseline_study())
    pl=copy.deepcopy(F['plan']);pl['slots'][1]['event_id']='e1';pl['slots'][1]['forecaster']='person2'
    good['dependent-forecasters']=req('report',ledger=study(plan=pl))
    good['record-forecast']=req('forecast-record',ledger=p.create(F['plan']),forecast=F['forecasts'][0])
    good['record-decision']=req('decision-record',ledger=p.create(F['plan']),decision=dec())
    good['reference']=req('reference')
    bad={}
    for name,value in [('negative-probability','-0.1'),('above-one','1.1'),('boolean-probability',True),('number-probability',0.8),('bad-decimal','0e0')]:
        f=copy.deepcopy(F['forecasts'][0]);f['probability']=value;bad[name]=req('forecast-record',ledger=p.create(F['plan']),forecast=f)
    for name,key,value in [('invalid-orientation','orientation','negative'),('invalid-validity','validity','0.4'),('invalid-rank','rank',0),('missing-cue-provenance','provenance','')]:
        c=copy.deepcopy(cues);c[0][key]=value;bad[name]=req('take-the-best',decision=ttb(cues=c))
    bad['ttb-negative-import']=req('take-the-best',decision=ttb(ecological_direction='negative'))
    pl=baseline_plan();pl['baseline']['training_outcomes'][0]['event_id']='e1';bad['baseline-leak']=req('create',plan=pl)
    pl=baseline_plan();pl['baseline']['probability']='0.5';bad['hindsight-base-rate']=req('create',plan=pl)
    l=study();l['actions'][0]['payload']['notes']+='tamper';bad['mutation']=req('report',ledger=l)
    rr=copy.deepcopy(F['resolutions'][0]);rr['outcome']=True;bad['boolean-outcome']=req('resolve',ledger=study(resolutions=[]),resolution=rr)
    rr=copy.deepcopy(F['resolutions'][0]);rr['evidence']['permission']='';bad['rights']=req('resolve',ledger=study(resolutions=[]),resolution=rr)
    rr=copy.deepcopy(F['resolutions'][0]);rr['evidence']['sha256']='0'*64;bad['evidence-bytes']=req('resolve',ledger=study(resolutions=[]),resolution=rr)
    bad['unsupported-psychic']=req('predict-psychic');bad['schema']=req('reference',unknown=True)
    return good,bad

def run(write=False):
    good,bad=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'request.json')
        def cli(name,q,fmt,rejected=False,save=True,raw=None):
            path.write_text(raw if raw is not None else json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            cp=subprocess.run([sys.executable,'-m','future','intuitive-prediction',str(path),'--format',fmt],cwd=ROOT,capture_output=True)
            assert cp.returncode==(2 if rejected else 0),(name,cp.stderr.decode(errors='replace'),cp.stdout[:200])
            actual=cp.stdout.decode('utf-8').replace('\r\n','\n').rstrip('\n')+'\n'
            if fmt=='json':value=json.loads(actual)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',actual,re.S);assert m,name;value=json.loads(m.group(2))
            if save:
                target=ROOT/f'data/intuitive-prediction-{name}.{ "json" if fmt=="json" else "md"}'
                if write:target.write_text(actual,encoding='utf-8')
                else:assert target.read_text(encoding='utf-8')==actual,('replay',name,fmt)
            cases.append(dict(name=name,format=fmt,rejected=rejected,passed=True))
            return value
        for rejected,examples_ in [(False,good),(True,bad)]:
            for name,q in examples_.items():
                target=ROOT/f'data/intuitive-prediction-{name}-input.json'
                if write:target.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                else:assert json.loads(target.read_text(encoding='utf-8'))==q
                values=[cli(name,q,fmt,rejected) for fmt in ['json','markdown']];assert values[0]==values[1]
        for name,raw in [('duplicate-json','{"schema_version":1,"task":"reference","task":"reference"}'),('nonfinite-json','{"schema_version":1,"task":"reference","x":NaN}')]:
            # Do not commit intentionally invalid JSON;literal strings live in this smoke tool.
            for fmt in ['json','markdown']:cli(name,None,fmt,True,save=False,raw=raw)
        # Actual CLI-created ledger, separately submitted decision and probabilities,then outcomes.
        value=cli('lifecycle-create',req('create',plan=F['plan']),'json',save=False);ledger=value['ledger']
        value=cli('lifecycle-decision',req('decision-record',ledger=ledger,decision=dec()),'json',save=False);ledger=value['ledger']
        for f in F['forecasts']:
            v=copy.deepcopy(f);v['decision_id']='d1'
            value=cli('lifecycle-'+v['forecast_id'],req('forecast-record',ledger=ledger,forecast=v),'json',save=False);ledger=value['ledger']
        for r in F['resolutions']:
            value=cli('lifecycle-'+r['event_id'],req('resolve',ledger=ledger,resolution=r),'json',save=False);ledger=value['ledger']
        value=cli('lifecycle-report',req('report',ledger=ledger),'json',save=False)
        assert value['result']['brier']['exact']=='5/16';assert len(value['result']['decisions'])==1
        demo=ROOT/'data/intuitive-prediction-demo.json'
        if write:demo.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        else:assert json.loads(demo.read_text(encoding='utf-8'))==value
    out=dict(passed=True,cli_cases=len(cases),accepted_pairs=len(good),rejected_pairs=len(bad),complete_cli_lifecycle=True,exact_replay=True,cases=cases)
    target=ROOT/'data/intuitive-prediction-smoke.json'
    if write:target.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==out
    print(f'{len(cases)}CLI cases;{len(good)}accepted/{len(bad)}rejected JSON/Markdown pairs;complete linked lifecycle passed')
if __name__=='__main__':run('--write' in sys.argv)
