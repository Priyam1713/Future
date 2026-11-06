"""Independent pre-engine finite truth matrix and source cases;no expected production calls."""
import json
from pathlib import Path
from future import augury as a
ROOT=Path(__file__).resolve().parents[1]
def verify():
    f=json.loads((ROOT/'tests/fixtures/augury_reference_v1.json').read_text(encoding='utf-8'));p,c=a.assets()
    assert a.digest(f)==p['source_fixture_sha256'] and c['records']==f['records'] and c['sources']==f['sources']
    ids=list(f['domains']);checks=0
    for row in f['matrix']:
        o=dict(observation_id='fixture')|dict(zip(ids,row['values']));r=a.evaluate(o)
        assert [x['rule_id'] for x in r['evaluations']]==f['condition_rule_order']
        assert [x['status'] for x in r['evaluations']]==row['statuses'],o
        assert r['status']==row['overall'],o
        assert r['cardinal_conversion'] is None and r['modern_species_inferred'] is None and r['empirical_prediction'] is None
        assert all(x in ('flight-crow-left','flight-raven-right') for x in r['favorable_main_source_ids'])
        checks+=5
    for x in f['extra_cases']:
        o=dict(observation_id=x['name'])|x['observation'];r=a.evaluate(o)
        assert r['applicable_main_ids']==x['applicable'] and r['status']==x['overall'] and r['favorable_main_source_ids']==x['favorable']
    for key in p['required_fields']:
        o=dict(observation_id='uncertain',**f['extra_cases'][2]['observation'],uncertain_fields=[key]);r=a.evaluate(o);assert not r['favorable_main_source_ids']
    o=dict(observation_id='conflict',**f['extra_cases'][2]['observation'],side_reports=['left','right']);r=a.evaluate(o);assert r['status']=='conflicting_evidence' and not r['applicable_main_ids']
    assert a.lookup('call-crow-left')['locator']=='I.7.12' and a.lookup('call-crow-left')['polarity']=='not_stated'
    assert a.lookup('classes-note133')['text_layer']=='translator_note' and a.lookup('direction-criticism')['speaker']=='Marcus'
    assert a.lookup('note226-crow-right')['conditions']['relative_side']=='right'
    out=dict(passed=True,profile=a.PROFILE,profile_sha256=a.PROFILE_HASH,catalog_sha256=a.CATALOG_HASH,source_records=14,main_condition_accounts=4,conflicting_note_conditions=1,context_references=9,finite_observations=len(f['matrix']),individual_condition_checks=checks,hand_authored_cases=4,required_field_uncertainty_cases=5,structured_conflict_cases=1,reference='Independent pre-engine14 source records,four manually authored outcomes and864 finite truth-matrix combinations. No expected result obtained from production matcher.',compass_conversion=False,greek_runtime=False,empirical_validation=False)
    (ROOT/'data/augury-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('14 Augury source records;864 finite observations;4320 condition checks;4 known answers;5 uncertain-field and1 structured conflict cases passed')
    return out
if __name__=='__main__':verify()
