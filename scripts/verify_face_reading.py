"""Independent source-transcription checks; never validates physiognomic inference."""
from pathlib import Path
import json
from future.face_reading import reference,PROFILE


def run():
    fixture=json.loads(Path('tests/fixtures/face_reading_lavater_examples.json').read_text())
    cases=[]
    for c in fixture['region_cases']:
        region=c['region_id'];side='both' if region in ('eyes','cheeks') else 'midline'
        request=dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',
            orientation=dict(view='frontal',side_frame='subject',mirrored=False),observations=[dict(region_id=region,side=side)])
        r=reference(request);actual=r['regions'][0]['historical_reference']
        assert actual['historical_term']==c['expected_term'] and actual['locator']==c['expected_locator']
        assert not r['inference_enabled']
        cases.append(dict(kind='printed region terminology',input_region=region,expected_term=c['expected_term'],
                          actual_term=actual['historical_term'],locator=actual['locator'],passed=True))
    for c in fixture['illustration_cases']:
        r=reference(dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='source_example',example_id=c['example_id']))
        e=r['source_example']
        assert (e['figure_number'],e['region_id'],e['geometry']['outline'],e['geometry']['relative_base'])==(c['expected_figure'],c['expected_region'],c['expected_outline'],c['expected_relative_base'])
        assert not r['inference_enabled'] and r['individual_assessment'] is None
        cases.append(dict(kind='published labeled schematic',example_id=c['example_id'],figure_number=e['figure_number'],
                          region_id=e['region_id'],geometry=e['geometry'],locator=e['locator'],passed=True))
    report=dict(profile=PROFILE,source_id=fixture['source_id'],verification_scope=fixture['method'],cases=cases,
        evidence=fixture['evidence'],passed=True,limits=fixture['limits'],individual_inference_validated=False)
    Path('data/face-reference-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(len(cases),'independently transcribed region/illustration cases passed')

if __name__=='__main__':run()
