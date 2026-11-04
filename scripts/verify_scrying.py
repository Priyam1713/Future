"""Independent pre-engine selected-passage and procedure-order acceptance."""
import json
from pathlib import Path
from future import scrying as s


def run():
    ref=json.loads(Path('tests/fixtures/scrying_procedure_reference.json').read_text(encoding='utf-8'))
    counts={}
    assert [r['id'].split('.')[-1] for r in s.DATA['rules']]==ref['source_rule_order']
    for case in ref['cases']:
        rule=s.RULES['scrying.atkinson.'+case['rule']]
        assert case['locator_contains'] in rule['locator'] and case['statement_contains'] in rule['statement']
    counts['independent_original_passage_cases']=len(ref['cases'])
    base=dict(schema_version=1,profile=s.PROFILE,task='guided_journal',mode='manual')
    for surface in ref['surface_ids']:
        result=s.read(base|dict(session=dict(surface=surface)))
        assert result['session']['effective_surface']==surface
        assert s.DATA['surfaces'][surface]['rule_ids']==('scrying.atkinson.surface',)
    counts['independent_surface_choices']=len(ref['surface_ids'])
    workflow=s.read(base)['guidance']
    for n,expected in enumerate(ref['workflow_order']):
        assert workflow[n]['id']==expected and workflow[n]['order']==n+1
        assert all(r['source_id'] and r['locator'] for r in workflow[n]['source_components'])
    counts['frozen_editorial_workflow_stages']=len(workflow)
    assert ref['edition']['displayed_isbn'] in s.DATA['source']['edition']
    assert not ref['edition']['loc_equivalent'] and 'not equated' in s.read(base)['direct']['edition_boundary']
    counts['edition_boundary_cases']=2
    report=dict(passed=True,checks=sum(counts.values()),counts=counts,
        assurance='Selected historical procedure fidelity and editorial workflow consistency;not clairvoyance,perception or predictive validation.',optional_seeded_prompts='Deferred;no seed protocol or vector claim')
    Path('data/scrying-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(report['checks'],'Scrying reference checks passed')


if __name__=='__main__':run()
