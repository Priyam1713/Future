"""Original-image transcriptions verify historical fidelity,not scientific validity."""
import json
from pathlib import Path
from future.phrenology import reference, PROFILE


def run():
    fixture=json.loads(Path('tests/fixtures/phrenology_spurzheim_examples.json').read_text(encoding='utf-8'))
    cases=[]
    def read(panel,key):
        return reference(dict(schema_version=1,profile=PROFILE,task='historical_reference',schematic=panel,
            selections=[dict(label_id=key)]))['results'][0]['entry']
    for key,name in fixture['legend_pairs']:
        actual=read('frontis-frontal',key)
        assert actual['original_name']==name
        cases.append(dict(kind='original legend',label_id=key,expected=name,actual=actual['original_name'],passed=True))
    for panel,key,name,terms in fixture['diagram_cases']:
        actual=read(panel,key)
        assert actual['original_name']==name and all(t in actual['location']['description'] for t in terms)
        cases.append(dict(kind='original panel position',schematic=panel,label_id=key,expected_terms=terms,actual=actual['location'],passed=True))
    for panel,key in fixture['panel_absences']:
        assert read(panel,key)['location'] is None
        cases.append(dict(kind='absent/unverified anchor',schematic=panel,label_id=key,passed=True))
    report=dict(profile=PROFILE,source_id=fixture['source_id'],method=fixture['method'],cases=cases,passed=True,
        limits=fixture['limits'],individual_inference_validated=False)
    Path('data/phrenology-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'independent original legend/panel/absence cases passed')


if __name__=='__main__':run()
