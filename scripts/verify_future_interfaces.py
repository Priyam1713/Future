"""Read-only compatibility witnesses; no adapters or unified execution framework."""
import copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from future.remote_viewing import digest
from future.scrying import load_input
R=Path(__file__).resolve().parents[1]
def fixture(stem):return load_input(R/('tests/fixtures/'+stem+'-independent-v1.json'))
def run():
    from future import superforecasting as sf,collective_intelligence as ci,prediction_markets as pm,psychohistory as ph,digital_twin as dt,agent_based as ab,chaos_theory as ct,causal_ai as ca,multiverse as mv
    from scripts.superforecasting_oracle import plan,forecast,resolution
    from scripts.superforecasting_scenarios import resolved
    groups={}
    # Compare real scoring interfaces on the same probabilities/outcomes.
    ps=['1/5','1/5','4/5','4/5'];ys=[0,1,0,1];a=sf.evaluate(resolved(ps,ys));b=ci.read(fixture('collective-intelligence')['cases']['decomposition']['input'])
    assert a['primary']['binary_brier']['exact']==b['primary']['binary_brier']=='17/50'
    assert a['primary']['two_category_sum_of_squares']['exact']==b['primary']['two_category_brier']=='17/25'
    groups['51-to-57-scoring']=dict(passed=True,binary_brier='17/50',two_category_brier='17/25',boundary='Compatible numeric scoring conventions;question identities,weights/forecast revisions remain separate schemas. No automatic adapter.')
    # Explicit offline outcome mapping is only a witness, never a live resolver.
    sf_yes=sf.evaluate(resolved(['1/2'],[1]));market=pm.read(fixture('prediction-markets')['cases']['settle-yes']['input']);assert sf_yes['questions'][0]['outcome']==1 and market['final']['winning_outcome']=='YES' and market['final']['settlements']==1
    p=plan(1);ledger=sf.create(p);ledger=sf.append(ledger,'forecast',forecast(p,at=p['questions'][0]['cutoff']));ledger=sf.append(ledger,'resolve',resolution(p));assert sf.evaluate(ledger)['rows'][0]['scored']
    cutoff=pm.read(fixture('prediction-markets')['cases']['quote-at-cutoff']['input']);assert any(x['decision']=='rejected' for x in cutoff['trace'])
    unresolved=sf.evaluate(resolved(['1/2'],[1],['void']));assert unresolved['primary']['denominator']==0
    bad=copy.deepcopy(fixture('prediction-markets')['cases']['settle-yes']['input']);bad['events'][-1]['outcome']='void'
    try:pm.read(bad)
    except ValueError:pass
    else:raise AssertionError('Void cannot map to binary market settlement')
    groups['51-to-58-resolution']=dict(passed=True,demonstrated_mapping={'1':'YES','0':'NO'},mapping_scope='Manually declared synthetic witness only; no shared identity/authentication adapter.',differences=['51allowsdispute/void andcontrolledresolutioncorrection;58settlesbinaryonce','51forecastcutoffinclusive;58quotes/tradesstrictlybeforeclose','51canresolvepositiveoccurrencebeforewindowend;58requiresmarketclose','Question/eventIDs,rule definitions,evidence anddeclaredauthority mustbe reconciled before any futureadapter.'])
    # Common hashes are provenance primitives, not permission to share RNG streams.
    p52=fixture('psychohistory')['cases']['identical']['input'];r52=ph.read(p52);assert r52==ph.read(p52) and all(c['identical_configuration'] for c in r52['comparisons']) and r52['interpretation']['causal_inference']=='unsupported'
    r60=mv.read(fixture('multiverse')['cases']['reference']['input'])
    common=['input_sha256','code_sha256','source_manifest_sha256','source_freeze_sha256']
    for r in [r52,r60]:
        for key in common:assert isinstance(r[key],str) and len(r[key])==64
        assert r['request']['provenance']['snapshot_sha256']==hashlib.sha256(r['request']['provenance']['snapshot'].encode()).hexdigest()
    groups['52-synthetic-provenance']=dict(passed=True,common_hash_fields=common,stream_sha256=r52['stream_sha256'],boundary='52finite PRNG coupled runs are correlated model samples;60exact editorial treeweights have no RNG. No empirical probability/causal transfer or stream reuse.')
    r53=dt.read(fixture('digital-twin')['cases']['delayed']['input']);changed=dt.read(fixture('digital-twin')['cases']['delayed-changed']['input']);assert [r['posterior_mean'] for r in r53['rows']]==[r['posterior_mean'] for r in changed['rows']] and r53['rows'][0]['correction']=='not_available_at_update'
    notknown=dt.read(fixture('digital-twin')['cases']['not-yet-known']['input']);assert notknown['rows'][-1]['filter_squared_error'] is None
    late=ci.read(fixture('collective-intelligence')['cases']['late-revision']['input']);assert late['status']=='accepted'
    groups['53-measurement-availability']=dict(passed=True,late_measurement_did_not_rewrite_filter=True,unknown_target_not_scored=True,boundary='Common availability chronology concept;53doesnotretroactivelyassimilatedelayedrecords,51/57selecteligibleforecastrevisions underdifferentcutoffcontracts. No automaticevaluationconnector.')
    r54=ab.read(fixture('agent-based')['cases']['full-horizon-fixed']['input']);r59=ct.read(fixture('chaos-theory')['cases']['stride']['input'])
    assert all(s['executed_ticks']==s['requested_ticks']==r54['request']['ticks'] and not s['early_stopped'] for s in r54['scenarios'])
    n=r59['request']['integration']['steps'];assert r59['diagnostics']['integrated_coarse_steps_per_trajectory']==n and r59['diagnostics']['integrated_refined_steps_per_trajectory']==2*n
    assert r59['diagnostics']['lyapunov_exponent'] is None
    groups['54-to-59-simulation-boundaries']=dict(passed=True,boundary='54exact synchronous binary B3/S23 gridticks differ from59approximate continuous Lorenz RK4 dimensionless steps. Both finish requested horizons;neither scalarcounts nor equalclocklabels make states/units comparable. No grid-to-ODE adapter.')
    causal=ca.read(fixture('causal-ai')['cases']['confounding']['input']);unsupported=ca.read(fixture('causal-ai')['cases']['latent']['input']);assert causal['observational']['risks']!=causal['interventional']['risks'] and unsupported['interventional'] is None
    groups['56-causal-versus-conditional']=dict(passed=True,observational=causal['observational']['risks'],interventional=causal['interventional']['risks'],boundary='Conditionalscenario/forecast probabilities are notinterventions.56effects dependondeclaredDAG,adjustment,compatibility andpositivity;unsupportedlatent graph hasnullinterventionalresult.')
    assert F(r60['total_leaf_mass'])==1 and sum((F(l['mass'])*F(l['utility']) for l in r60['leaves']),F(0))==F(r60['expected_utility'])==1
    assert next(l for l in r60['leaves'] if l['id']=='A1')['mass']=='1/6' and not r60['universe_observations_used'] and not r60['everett_empirically_validated']
    groups['60-generic-scenario-representation']=dict(passed=True,leaf_mass='1',expected_utility='1',path_mass='1/6',boundary='Finite exact editorial probability/utility representation only;arbitraryweights distinctfrom Bornrule amplitudes. No observational,causal ormultiverse predictive certification.')
    files=['future/'+name+'.py' for name in ['superforecasting','collective_intelligence','prediction_markets','psychohistory','digital_twin','agent_based','chaos_theory','causal_ai','multiverse']]
    out=dict(passed=True,groups=groups,group_count=len(groups),engine_code_sha256={path:hashlib.sha256((R/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for path in files},scope='Read-only compatibility/semantic-boundary witnesses; no engines changed,no production connector orneworchestrationframework.')
    (R/'data/future-interface-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(str(len(groups))+' cross-engine compatibility/boundary groups pass;no productionadapters')
if __name__=='__main__':run()
