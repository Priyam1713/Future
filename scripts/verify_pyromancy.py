"""Independent pre-engine source and manual-condition witness comparisons."""
import json
from pathlib import Path
from future import pyromancy as p
from tests.test_pyromancy import base,obs,selected,FIXTURE,fixture_row


def run():
    f=FIXTURE;counts={}
    for s,w in zip(p.DATA['sources'],f['source_witnesses']):
        assert s['published_on']==f['publication_date'] and s['id']==w['id'] and s['snapshot_sha256']==w['sha256'] and s['snapshot_bytes']==w['bytes']
        assert s['ingestion']=='facts_only' and 'not verified2020' in s['witness']
    counts['source_date_identity_hash_rights_separation']=18
    for r in p.RULES:assert r['locator']==f['source_locators'][r['case']]
    counts['source_locators']=6
    for c in f['cases']:assert selected(p.read(base([fixture_row(c['name'])]))['observations'][0])==c['expected'],c['name']
    counts['pre_engine_conditions']=len(f['cases'])
    for c in f['missing']:
        r=p.read(base([obs(c['phenomenon'],attributes=c['attributes'],physical=c['physical'])]))['observations'][0]
        assert next(x for x in r['cases'] if x['id']==c['case'])['status']=='insufficient_evidence'
    counts['missing']=len(f['missing'])
    for c in f['conflicts']:
        assert p.read(base([obs(c['phenomenon'],attributes=c['attributes'],physical=c['physical'])]))['observations'][0]['status']=='conflicting_evidence'
    counts['conflicts']=len(f['conflicts'])
    for hazard in f['safety']:
        r=p.read(base([fixture_row('high_after_correction')],safety=hazard));assert r['safety']['symbolic_hold'] and not r['editorial_synthesis'][0]['accounts']
    counts['safety_hold']=len(f['safety'])
    r=p.read(base(documentary_reference='pgm_iv_52_87'))
    for k,v in f['historical_lamp'].items():assert r['documentary_lamp'][k]==v
    counts['historical_isolation']=len(f['historical_lamp'])
    result=dict(passed=True,checks=sum(counts.values()),counts=counts,assurance='Source fidelity and independently authored manual-condition expectations,not combustion measurement,diagnosis or predictive validation.')
    Path('data/pyromancy-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['checks'],'Pyromancy independent source/condition checks passed')


if __name__=='__main__':run()
