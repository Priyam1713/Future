"""Frozen original-source/independent pre-engine conditional and zone checks."""
import json
from pathlib import Path
from future import tasseography as t
from tests.test_tasseography import base,obs,selected,figure


def run():
    f=json.loads(Path('tests/fixtures/tasseography_reference_v2.json').read_text(encoding='utf-8'))
    extra=json.loads(Path('tests/fixtures/tasseography_context_reference.json').read_text(encoding='utf-8'));counts={}
    assert list(t.SYMBOLS)==f['symbols'];counts['identities']=len(f['symbols'])
    for k,v in f['locators'].items():assert t.SYMBOLS[k]['locator']==v and t.SYMBOLS[k]['source_id']==f['source_id']
    counts['source_locators']=len(f['locators'])
    for region,association in f['cup_zones']:assert t.zones(obs(region=region))['qualifications'][0]['association']==association
    counts['independent_cup_zones']=len(f['cup_zones'])
    z=t.zones(obs(region='bottom',handle_relation='under_handle'));assert [x['association'] for x in z['qualifications']]==['far_distant',f['handle_timing']]
    assert z['status']=='conflicting_evidence' and z['calendar_date'] is None;counts['overlapping_qualifications']=1
    for c in f['conditional_cases']:
        assert selected(t.read(base([obs(c['symbol'],**c['fields'])],context=c['context']))['observations'][0])==c['applicable']
    counts['pre_engine_conditional_cases']=len(f['conditional_cases'])
    for c in f['adjacency_cases']:
        q=base([obs(c['symbols'][0],adjacent_to=['o2'],**c['fields']),dict(id='o2',symbol_id=c['symbols'][1])])
        assert selected(t.read(q)['observations'][0])==c['expected']
    counts['pre_engine_adjacency_cases']=len(f['adjacency_cases'])
    for c in extra['dots_cases']:
        row=obs('dots',adjacent_to=['o2'])
        if 'arrangement' in c:row['arrangement']=c['arrangement']
        assert t.read(base([row,dict(id='o2',symbol_id='anchor')]))['observations'][0]['cases'][0]['status']==c['status']
    counts['surrounding_not_plain_adjacency']=len(extra['dots_cases'])
    r=t.read(figure());d=r['documentary_comparison']
    assert all(x['status']=='declared_fields_match' for x in d['placement_checks']);counts['original_figure_placements']=5
    assert [c['status'] for c in d['cases']]==['applicable']*3;counts['documentary_cases']=3
    q=figure();q['context']={};assert t.read(q)['documentary_comparison']['cases'][1]['status']=='insufficient_information'
    q['observations'][2].pop('adjacent_to');assert t.read(q)['documentary_comparison']['cases'][0]['status']=='insufficient_information'
    counts['original_example_missing_conditions']=2
    for vessel in ('saucer','nelros','coffee'):
        try:t.read(base(vessel=vessel))
        except ValueError:pass
        else:raise AssertionError('Distinct method accepted')
    counts['method_isolation']=3
    assert 'PG6964' in t.DATA['source']['edition'] and t.DATA['source']['ingestion']=='facts_only'
    assert not t.read(base())['replay']['rng'];counts['edition_rights_no_seed']=3
    result=dict(passed=True,checks=sum(counts.values()),counts=counts,
        assurance='Source-located historical fidelity and synthetic manual-condition fixtures;FigureVIII text/diagram inspected in source pass,not image-recognition or empirical outcome validation.')
    Path('data/tasseography-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['checks'],'Tasseography independent reference checks passed')


if __name__=='__main__':run()
