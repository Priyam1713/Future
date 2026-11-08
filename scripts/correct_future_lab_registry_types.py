"""Explicit metadata revision; preserve v1 and all pre-production math/native anchors."""
import copy,hashlib,json
from pathlib import Path
from future.remote_viewing import digest
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
def save(p,x):(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def run():
    if (R/'knowledge/future_lab_registry_freeze_v2.json').exists():raise ValueError('Metadata revision already frozen')
    original=load('data/future-lab-capability-registry.json');oldhash=digest(original);assert oldhash==load('knowledge/future_lab_registry_freeze_v1.json')['registry_sha256'];(R/'data/future-lab-capability-registry-v1.json').write_bytes((R/'data/future-lab-capability-registry.json').read_bytes())
    registry=copy.deepcopy(original);changes={4:'deterministic_symbolic_numerology',43:'offline_blinded_target_protocol_and_scoring',44:'prospective_dream_event_ledger_and_bounded_comparison',45:'explicit_heuristic_decision_and_binary_scoring',46:'dream_record_provenance_and_phenomenology_annotation',50:'cpu_emulated_small_quantum_circuit_reference',52:'synthetic_population_threshold_simulation',53:'offline_scalar_state_space_replay_and_scenarios',54:'exact_synchronous_binary_grid_simulation'}
    corrections=[]
    for e in registry['entries']:
        if e['technique_id'] in changes:
            c=load(e['core_record']);assert digest(c)==e['core_sha256'];corrections.append(dict(technique_id=e['technique_id'],before=e['capability_type'],after=changes[e['technique_id']],evidence_record=e['core_record'],release_status=c['status']));e['capability_type']=changes[e['technique_id']]
    registry.update(id='future-lab-capability-registry-v2',metadata_revision=2,supersedes_registry_sha256=oldhash);newhash=digest(registry);save('data/future-lab-capability-registry.json',registry);save('knowledge/future_lab_registry_freeze_v2.json',dict(version=2,registry_sha256=newhash,original_registry_sha256=oldhash,original_registry_path='data/future-lab-capability-registry-v1.json',corrections=corrections,scope='Classification labels only. No nativeoperation,profile,source,input/outputcontract,evaluationadmission ormathchanges.'))
    p=load('knowledge/future_lab_profile_v1.json');p.update(id='future-lab-offline-experiments-v2',version=2,registry_sha256=newhash,supersedes_profile_sha256=digest(load('knowledge/future_lab_profile_v1.json')),revision_reason='Registry classification correction only; all experiment/scoring rules unchanged.');save('knowledge/future_lab_profile_v2.json',p)
    f=load('tests/fixtures/future-lab-independent-v1.json');original_fixture_hash=digest(f);f['demo_plan']['registry_sha256']=newhash;f.update(metadata_revision=2,supersedes_fixture_sha256=original_fixture_hash);save('tests/fixtures/future-lab-independent-v2.json',f);save('knowledge/future_lab_fixture_freeze_v2.json',dict(version=2,fixture_sha256=digest(f),original_fixture_sha256=original_fixture_hash,original_fixture_freeze='knowledge/future_lab_fixture_freeze_v1.json',original_oracle_sha256=load('knowledge/future_lab_fixture_freeze_v1.json')['oracle_sha256'],metadata_transform_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),metadata_correction_after_production=True,numeric_and_native_expectations_unchanged=True,scope='Onlydemo registrybinding andexplicitrevisionmetadata changed; all54nativeoutputs andindependentnumericanswers remain frompreproductionv1.'))
    print('Registry',newhash,'Profile',digest(p),'Fixture',digest(f))
if __name__=='__main__':run()
