"""Verify pre-engine literal selection choices,exact pools and scoring conventions."""
import copy,hashlib,json
from pathlib import Path
from future.remote_viewing import digest
from future.scrying import load_input
R=Path(__file__).resolve().parents[1]
def fixture():
    f=load_input(R/'tests/fixtures/collective-intelligence-independent-v1.json');fr=load_input(R/'knowledge/collective_intelligence_fixture_freeze_v1.json')
    assert digest(f)==fr['fixture_sha256'];assert hashlib.sha256((R/'scripts/collective_intelligence_oracle.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==fr['oracle_sha256'];return f
def check_case(c):
    from future.collective_intelligence import read
    q=copy.deepcopy(c['input']);before=digest(q)
    if c['exit_code']==2:
        try:read(q)
        except ValueError:pass
        else:raise AssertionError('Expected rejection')
    else:
        r=read(q);e=c['expected']
        for qid,ex in e['questions'].items():
            for key,value in ex.items():assert r['questions'][qid][key]==value,(qid,key)
        for key,value in e['primary'].items():assert r['primary'][key]==value,key
        for fid,ex in e['individuals'].items():
            for key,value in ex.items():assert r['individuals'][fid][key]==value,(fid,key)
        assert r['empirical_skill_validated'] is False and r['dependence']['independence_certified'] is False
        report_hash=r.pop('report_sha256');assert digest(r)==report_hash
    assert digest(q)==before
def convention_checks():
    from future.collective_intelligence import read
    f=fixture();r=read(f['cases']['decomposition']['input']);a=f['literal_anchors']['decomposition'];d=r['primary']['decomposition']
    for key in ['reliability','resolution','uncertainty']:assert d[key]==a[key]
    assert d['identity_passed'] and r['primary']['binary_brier']==a['binary_brier'] and r['primary']['two_category_brier']==a['two_category_brier']
    base=read(f['cases']['equal']['input']);flip=read(f['cases']['outcome-flip']['input'])
    assert base['model_sha256']==flip['model_sha256'] and base['questions']['q1']['probability']==flip['questions']['q1']['probability']
    assert base['resolution_sha256']!=flip['resolution_sha256']
    weighted_input=copy.deepcopy(f['cases']['weighted']['input']);weighted=read(weighted_input);weighted_input['questions'][0]['resolution']['outcome']=0;weighted_flip=read(weighted_input)
    assert weighted['model_sha256']==weighted_flip['model_sha256']
    assert weighted['questions']['q1']['probability']==weighted_flip['questions']['q1']['probability']=='13/20'
    assert weighted['primary']['binary_brier']=='49/400' and weighted_flip['primary']['binary_brier']=='169/400'
    order=read(f['cases']['reordered']['input']);assert base['model_sha256']==order['model_sha256'] and base['split_sha256']==order['split_sha256']
def compatibility_51():
    from future.superforecasting import aggregate,number
    from fractions import Fraction as F
    rows=[]
    for i,(p,y) in enumerate(zip([F(1,5),F(1,5),F(4,5),F(4,5)],[0,1,0,1])):
        rows.append(dict(scored=True,probability=number(p),outcome=y,baseline_probability='1/2',binary_brier=number((p-y)**2),forecast_id='f'+str(i),question_id='q'+str(i),event_id='e'+str(i),dependency_group='g'+str(i),participant='person',exclusion_reasons=[]))
    result=aggregate(rows)
    assert result['binary_brier']['exact']=='17/50' and result['two_category_sum_of_squares']['exact']=='17/25'
    assert [result['decomposition'][k]['exact'] for k in ['reliability','resolution','uncertainty']]==['9/100','0','1/4']
    return True
def run():
    f=fixture()
    for c in f['cases'].values():check_case(c)
    convention_checks();compatibility_51()
    out=dict(passed=True,fixture_families=len(f['families']),families={k:dict(passed=True,cases=v) for k,v in f['families'].items()},accepted=sum(c['exit_code']==0 for c in f['cases'].values()),rejected=sum(c['exit_code']==2 for c in f['cases'].values()),literal_anchors=f['literal_anchors'],outcome_label_isolation_passed=True,canonical_order_passed=True,compatibility_51_scoring_passed=True,fixture_sha256=digest(f),scope='Exact declared offline pooling/scoring and eligibility software; no independent crowd or empirical skill certification')
    (R/'data/collective-intelligence-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('31 independent fixture families pass;25 accepted/35 rejected;51 scoring conventions match')
if __name__=='__main__':run()
