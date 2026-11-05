"""Independent pre-engine source fixtures and relationship truth-table checks."""
import hashlib,itertools,json
from pathlib import Path

def verify():
    from future import osteomancy as o
    f=json.loads(Path('tests/fixtures/osteomancy_reference_v1.json').read_text(encoding='utf-8'))
    freeze=json.loads(Path('knowledge/osteomancy_source_freeze_v1.json').read_text(encoding='utf-8'))
    canonical=hashlib.sha256(json.dumps(f,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
    assert canonical==freeze['fixture_canonical_sha256'] and f['authored_before_engine']
    assert list(o.CASES)==f['case_ids'] and len(o.CASES)==13
    assert o.thaw(o.DATA['source'])==f['source']
    for c in f['cases']:
        actual=o.lookup(c['case_id']);actual.pop('source_deep_link');assert actual==c
        for k in ('prognostication','verification'):
            assert c['components'][k]['value'] is None and c['components'][k]['status']=='omitted_from_inspected_excerpt'
            assert c['components'][k]['original_inscription_status']=='not_independently_verified'
        assert all(v['status']=='not_independently_verified' and v['value'] is None for v in c['original_evidence'].values())
    expected={c['case_id']:c for c in f['cases']}
    for case_id,(label,index) in f['expected_checks']['days'].items():assert expected[case_id]['components']['day']['value']==dict(label=label,source_day_index=index)
    for case_id,c in expected.items():
        if case_id not in f['expected_checks']['days']:assert c['components']['day']['value'] is None
        assert c['components']['diviner']['value']==f['expected_checks']['diviners'].get(case_id)
        assert (c['components']['lunar_month']['value'] or {}).get('number')==f['expected_checks']['moons'].get(case_id)
    assert [i for i in f['case_ids'] if expected[i]['components']['action']['status']=='explicitly_uncertain_in_source']==['20A','20B']
    rules={frozenset(r['pair']):r for r in f['relationships']}
    checks=0
    for a,b in itertools.product(f['case_ids'],repeat=2):
        actual=o.compare(a,b);back=o.compare(b,a)
        classification='same_record' if a==b else rules[frozenset((a,b))]['classification'] if frozenset((a,b)) in rules else 'relationship_unresolved'
        assert actual['relationship']['classification']==classification
        assert actual['canonical_case_ids']==back['canonical_case_ids']
        assert actual['relationship']==back['relationship'] and actual['component_comparison']==back['component_comparison']
        for name in ('day','diviner','prognostication','verification'):
            x,y=expected[a]['components'][name],expected[b]['components'][name]
            if x['value'] is None or y['value'] is None:assert actual['component_comparison'][name]['status']=='incomparable_missing_evidence'
        checks+=1
    for relation in f['relationships']:
        assert o.compare(*relation['pair'])['relationship']==relation
        assert list(o.DATA['groups'][relation['group']])==relation['pair']
    assert o.compare('19A','19B')['component_comparison']['day']['status']=='different_source_values'
    assert o.compare('19A','19B')['component_comparison']['condition']['status']=='different_source_values'
    assert o.compare('20A','20B')['component_comparison']['action']['status']=='incomparable_uncertainty'
    assert o.compare('24A','24B')['editorial_index_comparison']['predicates']==['mobilization','enemy_disaster_agency']
    out=dict(passed=True,profile=o.PROFILE,profile_sha256=o.PROFILE_HASH,source_sha256=f['source']['snapshot_sha256'],fixture_canonical_sha256=canonical,
        source_records=13,named_relationships=5,ordered_pair_checks=checks,omitted_outcome_component_checks=26,original_evidence_checks=52,
        day_labels_checked=4,explicit_diviners_checked=4,uncertain_action_cases=['20A','20B'],
        reference='Independently authored pre-engine factual fixtures and five-rule comparison table; no expected value obtained by invoking production matcher.',
        invariants=['All13 labels and typed facts preserved','169 ordered pairs and reversal stability','No A/B suffix classification','No source day/diviner inheritance','Uncertain action in both20A/B','No original artifact assignment or fabricated outcome','Missing fields are incomparable, not shared factual negatives'],empirical_validation=False)
    Path('data/osteomancy-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(f'13 Osteomancy source records;5 named relationships;{checks} ordered pair checks;26 omitted-outcome checks;52 original-evidence checks passed')
    return out
if __name__=='__main__':verify()
