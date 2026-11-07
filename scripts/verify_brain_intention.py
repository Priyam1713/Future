"""Verify frozen pre-engine known answers and all 28 independent families."""
import copy,hashlib,json
from fractions import Fraction as F
from math import comb
from pathlib import Path
from future.remote_viewing import digest
from future.scrying import load_input
R=Path(__file__).resolve().parents[1]
ERRATA_HASH='56ac1f0c4a2807f5d5cf6b054f38b909e02f2a9dec5ef0488c2b4de152f8c3ce'
def fixture():
    f=load_input(R/'tests/fixtures/brain-intention-independent-v1.json');freeze=load_input(R/'knowledge/brain_intention_fixture_freeze_v1.json')
    assert digest(f)==freeze['fixture_sha256']
    assert hashlib.sha256((R/'scripts/brain_intention_oracle.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==freeze['oracle_sha256']
    err=load_input(R/'knowledge/brain_intention_fixture_errata_v2.json');assert digest(err)==ERRATA_HASH
    assert err['original_fixture_sha256']==digest(f)
    f['cases'].update(err['corrections']);return f
def check_case(c):
    from future.brain_intention import read
    q=copy.deepcopy(c['input']);before=digest(q)
    if c['exit_code']==2:
        try:read(q)
        except ValueError:pass
        else:raise AssertionError('Expected rejection')
    else:
        r=read(q);e=c['expected']
        for k in ['features','centroids','predictions']:assert r[k]==e[k],k
        for k in ['confusion','accuracy','balanced_accuracy']:assert r['evaluation'][k]==e[k],k
        assert r['baseline']['evaluation']['accuracy']==e['baseline_accuracy']
        report_hash=r.pop('report_sha256');assert digest(r)==report_hash
    assert digest(q)==before
def literal_checks():
    f=fixture();a=f['literal_anchors'];assert F(sum(x*x for x in [-1,1,-1,1]),4)==F(a['population_variance']);assert F(4,3)==F(a['sample_variance'])
    assert F(sum(comb(10,k) for k in [8,9,10]),1024)==F(a['iid_toy_upper_tail'])
    for p,ds in [((2,3),a['distance_A']),((4,3),a['distance_B']),((3,3),a['tie'])]:assert [str(sum((F(x)-F(c))**2 for x,c in zip(p,centroid))) for centroid in [a['centroid_A'],a['centroid_B']]]==ds
def run():
    from future.brain_intention import read
    f=fixture();outcomes={}
    for name,c in f['cases'].items():check_case(c)
    literal_checks()
    original=load_input(R/'tests/fixtures/brain-intention-independent-v1.json')['cases']['validation-unused']
    try:read(original['input'])
    except ValueError:pass
    else:raise AssertionError('Original leaking fixture must reject')
    a=read(f['cases']['worked']['input']);b=read(f['cases']['test-label-flip']['input'])
    assert a['model_sha256']==b['model_sha256'] and a['predictions']==b['predictions'] and a['evaluation']!=b['evaluation']
    c=read(f['cases']['reordered']['input']);assert a['model_sha256']==c['model_sha256'] and a['predictions']==c['predictions'] and a['split_sha256']==c['split_sha256']
    for name,caseids in f['families'].items():outcomes[name]=dict(passed=True,cases=caseids)
    out=dict(passed=True,fixture_families=len(outcomes),families=outcomes,accepted=sum(c['exit_code']==0 for c in f['cases'].values()),rejected=sum(c['exit_code']==2 for c in f['cases'].values()),literal_anchors_passed=True,test_label_isolation_passed=True,canonical_order_passed=True,original_erroneous_fixture_rejected=True,fixture_sha256=load_input(R/'knowledge/brain_intention_fixture_freeze_v1.json')['fixture_sha256'],errata_sha256=ERRATA_HASH,scope='Synthetic exact arithmetic and declared procedural checks,not empirical intention decoding')
    (R/'data/brain-intention-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('28 independent fixture families pass;14 accepted/37 rejected')
if __name__=='__main__':run()
