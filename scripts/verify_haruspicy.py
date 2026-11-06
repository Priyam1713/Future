"""Pre-engine source fixtures and finite truth expectations, independent of matcher."""
import json
from pathlib import Path
from future import haruspicy as h
ROOT=Path(__file__).resolve().parents[1]

def verify():
    f=json.loads((ROOT/'tests/fixtures/haruspicy_reference_v1.json').read_text(encoding='utf-8'))
    p,c=h.assets()
    assert h.digest(f)==p['source_fixture_sha256']
    assert c['records']==f['records'] and c['sources']==f['sources'] and c['translation_notes']==f['translation_notes']
    heart=f['known_answers'][7]['observations'][0]
    fields=list(f['domains']);checked=0
    for values,statuses,overall in f['matrix']:
        x=dict(zip(fields,values));o={k:v for k,v in x.items() if k not in ('uncertain_presence','contradiction')}
        o.update(observation_id='matrix',tradition='roman',animal='votive_ox',setting_id='golden_throne_purple_robe',warning_attribution='spurinna',prior_observation_id='heart1')
        if x['uncertain_presence']:o['uncertain_fields']=['presence']
        if x['contradiction']:o['presence_reports']=['present','absent']
        r=h.evaluate_all([heart,o])[1]
        assert [a['rule_id'] for a in r['evaluations']]==f['source_case_order']
        assert [a['status'] for a in r['evaluations']]==statuses,(x,r)
        assert r['status']==overall,x
        assert r['empirical_prediction'] is None and r['anatomical_diagnosis'] is None and not r['ritual_authority']
        checked+=4
    for case in f['known_answers']:
        out=h.evaluate_all(case['observations'])
        assert [o['applicable_ids'] for o in out]==case['applicable'],case['name']
        if 'target' in case:
            r=out[case.get('target_index',0)]
            assert next(x for x in r['evaluations'] if x['rule_id']==case['target'])['status']==case['status'],case['name']
    assert h.lookup('lung-cleft')['native']==dict(book=1,chapter=39,section_start=85,section_end=85,note=None)
    assert h.lookup('liver-head-absent')['speaker']=='Marcus'
    assert h.lookup('caesar-heart')['conditions']['warning_attribution']=='spurinna'
    assert all(r['text_layer']=='main_text_dialogue' for r in c['records'])
    out=dict(passed=True,profile=h.PROFILE,profile_sha256=h.PROFILE_HASH,catalog_sha256=h.CATALOG_HASH,source_records=9,condition_accounts=4,context_references=5,finite_observations=len(f['matrix']),individual_condition_checks=checked,hand_authored_cases=len(f['known_answers']),source_fixture_sha256=h.digest(f),expected_origin='Literal independently specified pre-engine predicates and14 hand-authored cases;no expected production calls',empirical_validation=False)
    (ROOT/'data/haruspicy-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(f'9 Haruspicy source records;{len(f["matrix"])} finite observations;{checked} condition checks;14 known answers passed')
    return out
if __name__=='__main__':verify()
