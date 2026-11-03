"""Independent primary-text transcription comparisons,not empirical validation."""
import json
from pathlib import Path
from future.podomancy import PROFILE,reference


def run():
    fixture=json.loads(Path('tests/fixtures/podomancy_source_examples.json').read_text(encoding='utf-8'));cases=[]
    for key,region,view,pages,word in fixture['cases']:
        r=reference(dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',
            orientation=dict(frame='subject',view=view,mirrored=False),selections=[dict(entry_id=key,region_id=region,side='both')]))['results'][0]
        e=r['entry'];assert r['status']=='resolved_reference' and e['printed_page_markers']==pages and word in e['source_label']
        assert e['source_id']==fixture['source_id'] and not e['applied_to_individual']
        cases.append(dict(entry_id=key,region_id=region,expected_page_markers=pages,expected_label_fragment=word,actual_locator=e['locator'],passed=True))
    Path('data/podomancy-verification.json').write_text(json.dumps(dict(profile=PROFILE,source_id=fixture['source_id'],method=fixture['method'],
        cases=cases,passed=True,limits=fixture['limits'],empirical_accuracy_validated=False),indent=2)+'\n',encoding='utf-8')
    print(len(cases),'independent primary-text reference cases passed')


if __name__=='__main__':run()
