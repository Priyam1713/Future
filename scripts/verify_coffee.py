"""Checks against the independently frozen pre-engine source/condition witness."""
import json
from pathlib import Path
from future import coffee as c
from tests.test_coffee import base,obs,selected


def run():
    f=json.loads(Path('tests/fixtures/coffee_reference_v1.json').read_text(encoding='utf-8'));counts={}
    e=c.DATA['source_edition']
    assert [e['author'],e['translator'],e['first_edition'],e['isbn']]==f['edition'];counts['edition']=4
    assert list(c.SYMBOLS)==f['symbols'];counts['identities']=7
    for cases in c.SYMBOLS.values():
        for case in cases:assert case['locator']==f['locator'] and case['source_id']==c.DATA['source']['id']
    counts['source_locators']=8
    for row in f['cases']:
        r=c.read(base([obs(row['symbol'],attributes=row['attributes'])],vessel=row.get('vessel','cup')))
        assert selected(r['observations'][0])==row['expected']
    counts['source_condition_cases']=len(f['cases'])
    for symbol,attrs,state in f['missing']:
        assert c.read(base([obs(symbol,attributes=attrs)]))['observations'][0]['status']==state
    counts['missing']=len(f['missing'])
    for symbol,attrs in f['conflicting']:
        assert c.read(base([obs(symbol,attributes=attrs)]))['observations'][0]['status']=='conflicting_evidence'
    counts['contradictions']=len(f['conflicting'])
    for half,association in f['orientation']:
        assert c.read(base([obs(half=half)]))['observations'][0]['orientation']['source_association']==association
    counts['half_mapping']=4
    for direction,intent in f['rotation']:
        assert c.rotation(base(rotation=direction,intention=intent))['status']=='applicable'
    counts['rotation']=2
    t=c.read(base([obs('line',attributes=dict(shape='flat',dots=3,dot_arrangement='at_line_end'))]))['observations'][0]['cases'][0]['timing']
    assert t['units']==f['time_units'] and t['periods']==3 and t['selected_unit'] is None and t['calendar_date'] is None
    counts['timing_alternatives_and_no_date']=6
    r=c.read(base(f['documentary_comparison']['observations'],source_example='p104_narrative'))
    assert [selected(o)[0] for o in r['observations']]==f['documentary_comparison']['expected'];counts['documentary_narrative_cases']=3
    for symbol in ('horse','fish','camel','bird','line','adhered_grounds'):
        assert c.read(base([obs(symbol)],vessel='saucer'))['observations'][0]['status']=='unsupported'
    counts['saucer_scope']=6
    assert c.DATA['source']['snapshot_sha256']==f['source_sha256'];counts['source_snapshot']=1
    data=dict(passed=True,checks=sum(counts.values()),counts=counts,assurance='Independent pre-engine source fidelity and manual-condition comparisons,not empirical prediction or image recognition.')
    Path('data/coffee-verification.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(data['checks'],'Coffee independent source/condition checks passed')


if __name__=='__main__':run()
