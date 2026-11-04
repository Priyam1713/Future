"""Independent original-page setup/procedure fixtures frozen before engine."""
import json
from pathlib import Path
from future import mirror as m


def run():
    ref=json.loads(Path('tests/fixtures/mirror_procedure_reference.json').read_text(encoding='utf-8'))
    counts={}
    assert [r['id'].split('.')[-1] for r in m.DATA['rules']]==ref['source_order']
    for case in ref['cases']:
        rule=m.RULES['mirror.moody1992.'+case['rule']]
        assert 'Printedp'+str(case['page']) in rule['locator'] and case['contains'] in rule['statement']
    counts['independent_original_passage_cases']=len(ref['cases'])
    for key,value in ref['setup'].items():assert m.DATA['historical_setup'][key]==value
    counts['independent_setup_facts']=len(ref['setup'])
    base=dict(schema_version=1,profile=m.PROFILE,task='guided_mirror_journal',mode='manual')
    for n,expected in enumerate(ref['workflow_order']):
        step=m.read(base)['guidance'][n]
        assert (step['id'],step['order'])==(expected,n+1)
        assert all(r['locator'] and r['source_id'] for r in step['source_components'])
    counts['frozen_subset_workflow_stages']=len(ref['workflow_order'])
    assert 'Winter1992' in m.DATA['source']['edition'] and 'not full1993' in m.read(base)['direct']['edition_boundary']
    assert m.DATA['source']['ingestion']=='facts_only' and 'Human Sciences Press' in m.DATA['rights']
    counts['edition_rights_boundaries']=2
    report=dict(passed=True,checks=sum(counts.values()),counts=counts,
        assurance='Selected source procedure fidelity andqualified subset/journal behavior;not contact,predictive orclinical validation.')
    Path('data/mirror-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(report['checks'],'Mirror reference checks passed')


if __name__=='__main__':run()
