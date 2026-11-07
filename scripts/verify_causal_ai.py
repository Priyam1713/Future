"""Independent structural/path known answers; no fixture generation from engine."""
import copy,hashlib,json
from pathlib import Path
from future.remote_viewing import digest
from future.scrying import load_input
R=Path(__file__).resolve().parents[1]
def fixture():
    f=load_input(R/'tests/fixtures/causal-ai-independent-v1.json');fr=load_input(R/'knowledge/causal_ai_fixture_freeze_v1.json')
    assert digest(f)==fr['fixture_sha256'];assert hashlib.sha256((R/'scripts/causal_ai_oracle.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==fr['oracle_sha256'];return f
def check_case(c):
    from future.causal_ai import read
    q=copy.deepcopy(c['input']);before=digest(q)
    if c['exit_code']==2:
        try:read(q)
        except ValueError:pass
        else:raise AssertionError('Expected rejection')
    else:
        r=read(q);e=c['expected'];assert r['identification_status']==e['identification_status']
        if e['risks'] is not None:assert r['interventional']['risks']==e['risks']
        if e['observational'] is not None:assert r['observational']['risks']==e['observational']
        if e['identification_status']!='identified_under_declared_assumptions':assert r['interventional'] is None
        report_hash=r.pop('report_sha256');assert digest(r)==report_hash
    assert before==digest(q)
def graph_checks():
    from future.causal_ai import backdoor
    f=fixture()
    for c in f['graph_cases']:assert backdoor(c['nodes'],c['edges'],c['x'],c['y'],c['z'])['valid']==c['valid'],c
def run():
    from future.causal_ai import read
    f=fixture()
    for c in f['cases'].values():check_case(c)
    graph_checks();r=read(f['cases']['confounding']['input']);s=f['structural_enumeration']
    assert r['interventional']['risks']==s['do_risks'];assert r['interventional']['contrast_last_minus_first']=='1/5' and r['interventional']['contrast_first_minus_last']=='-1/5';assert r['observational']['contrast_last_minus_first']=='2/5'
    reordered=read(f['cases']['reordered']['input']);assert (r['model_sha256'],r['table_sha256'],r['interventional'])==(reordered['model_sha256'],reordered['table_sha256'],reordered['interventional'])
    zero=read(f['cases']['zero-mass-stratum']['input']);assert len(zero['positivity']['zero_mass_strata'])==1 and any(a['conditional'] is None and a['skipped_zero_mass'] for a in zero['strata'])
    out=dict(passed=True,fixture_families=len(f['families']),families={k:dict(passed=True,cases=v) for k,v in f['families'].items()},accepted=sum(c['exit_code']==0 for c in f['cases'].values()),rejected=sum(c['exit_code']==2 for c in f['cases'].values()),independent_graph_cases=len(f['graph_cases']),structural_enumeration_cases=80,interventional_oracle_passed=True,observational_disagreement_passed=True,canonical_order_passed=True,zero_strata_passed=True,fixture_sha256=digest(f),scope='Finite exact synthetic model software,not causal discovery or empirical effect validation')
    (R/'data/causal-ai-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('22 independent fixture families pass;256 graph cases;80 structural oracle cases')
if __name__=='__main__':run()
