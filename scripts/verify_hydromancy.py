import json
from pathlib import Path
from future import hydromancy as h
from tests.test_hydromancy import F,W,base,obs,case
def run():
 counts={}
 for name,session,key,state in F['cases']:assert case(h.read(base(session=session))['session_evaluation'],key)['status']==state
 counts['pre_engine_contexts']=len(F['cases'])
 for category,basis,state in F['observations']:assert h.read(base([obs(category,basis=basis)]))['observations'][0]['status']==state
 counts['pre_engine_classifications']=len(F['observations'])
 assert {s['id']:s['snapshot_sha256'] for s in h.DATA['sources']}==F['source_hashes'];counts['source_witnesses']=3
 assert F['article_author'] in h.DATA['attribution'] and F['excerpt_author'] in h.DATA['attribution'] and 'Not Donald Tyson' in h.DATA['attribution'];counts['attribution']=3
 assert h.thaw(h.DATA['documentary'])==F['documentary'];counts['documentary_identity_limits']=8
 r=h.read(base(session=W|dict(surface_motion='moving',observer_undisturbed=True,surface_visible=True)));assert case(r['session_evaluation'],'position')['status']=='source_supported';counts['observer_not_surface_stillness']=1
 assert h.read(base(documentary_comparison=True))['documentary_comparison']['coptic']['catalog_date']==[901,1100];counts['separate_coptic_date']=1
 result=dict(passed=True,checks=sum(counts.values()),counts=counts,assurance='Independent pre-engine source/context/classification expectations,not physical,psychological orpredictive validation.')
 Path('data/hydromancy-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(result['checks'],'Hydromancy independent reference checks passed')
if __name__=='__main__':run()
