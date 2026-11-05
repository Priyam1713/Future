import json
from pathlib import Path
from future import aeromancy as a
from tests.test_aeromancy import F,base,obs,result,selected,case,texas
def run():
 counts={}
 for phenomenon,features,expected in F['cases']:assert selected(result(obs(phenomenon,features=features)))==expected
 counts['pre_engine_conditions']=len(F['cases'])
 for source,declared,state in F['regions']:assert a.regional(source,declared)['status']==state
 counts['regional_qualification']=len(F['regions'])
 for key,value in F['attributions'].items():assert next(c for c in a.CASES if c['case']==key)['attribution']==value
 counts['individual_regional_attributions']=len(F['attributions'])
 for key,value in F['locators'].items():assert next(c for c in a.CASES if c['case']==key)['locator']==value
 counts['printed_locators']=len(F['locators'])
 for key,value in F['horizons'].items():assert next(c for c in a.CASES if c['case']==key)['horizon']==value
 counts['independent_horizon_wording']=len(F['horizons'])
 assert a.DATA['source']['snapshot_sha256']==F['sha256'];counts['source_witness']=1
 for key in texas():
  f=texas();f.pop(key);assert case(result(obs('wind',features=f)),'texas_sequence')['observational_status']=='insufficient_evidence'
 counts['texas_all_material_conditions']=len(texas())
 for key in F['cases'][6][1]:
  f=F['cases'][6][1].copy();f.pop(key);assert case(result(obs('cloud',features=f)),'fleecy_compound')['observational_status']=='insufficient_evidence'
 counts['fleecy_all_material_conditions']=len(F['cases'][6][1])
 assert len(result(obs('cloud',features=dict(mackerel_sky=True)))['competing_accounts'])==5;counts['separate_mackerel_accounts']=5
 result_data=dict(passed=True,checks=sum(counts.values()),counts=counts,assurance='Independent pre-engine historical source/condition expectations,not weather backtesting orforecast validation.')
 Path('data/aeromancy-verification.json').write_text(json.dumps(result_data,indent=2)+'\n',encoding='utf-8');print(result_data['checks'],'Aeromancy independent reference checks passed')
if __name__=='__main__':run()
