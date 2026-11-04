"""Acceptance against independent pre-engine historical/context fixtures."""
import json
from pathlib import Path
from future import dream as d


def run():
    ref=json.loads(Path('tests/fixtures/dream_source_reference.json').read_text(encoding='utf-8'))
    counts={}
    for n,key in enumerate(ref['category_ids']):
        item=d.CATEGORIES[key]
        assert (item['greek'],item['parent'])==(ref['greek_terms'][n],ref['parents'][n])
    counts['independent_category_terms_and_relations']=4
    for key,section in ref['motif_sections'].items():
        motif=d.MOTIFS[key]
        assert motif['provenance']['locator']=='Oneirocritica '+section and not motif['forecast']
    counts['independent_motif_locators']=9
    for case in ref['cases']:
        actual=d.lookup(case['motif'],case['context'])
        assert actual['status']==case['status'] and [x['id'] for x in actual['selected_cases']]==case['selected']
    counts['independent_contextual_cases']=len(ref['cases'])
    for rule,section in zip(d.DATA['context_rules'],['1.8','1.9']):assert rule['locator']=='Oneirocritica '+section
    counts['context_qualifications']=2
    assert all(d.MOTIFS[k]['provenance']['translator']=='Naphtali Lewis1976' for k in ['eating','drinking','feared_object','desired_person'])
    assert all(d.MOTIFS[k]['provenance']['translator']=='Robert J.White1975' for k in ['shipwreck','serpent','lost_nose','broken_staff','myth_variants'])
    counts['translation_partitions']=2
    report=dict(passed=True,checks=sum(counts.values()),counts=counts,
        assurance='Bounded historical source fidelity andexplicit contextual comparison only;synthetic application fixtures,not empirical omen orclinical validation.',automatic_tagger='Deferred;manual annotations never trigger source interpretations')
    Path('data/dream-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(report['checks'],'Dream reference checks passed')


if __name__=='__main__':run()
