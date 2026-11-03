"""Original-page transcriptions and separate constructed Euclidean fixtures."""
import json
from pathlib import Path
from future.graphology import PROFILE,reference
from future.graphology_geometry import measure


def run():
    f=json.loads(Path('tests/fixtures/graphology_source_examples.json').read_text(encoding='utf-8'));source_cases=[]
    for feature,category,name,page,figure in f['term_cases']:
        r=reference(dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',script='latin',writing_direction='ltr',
            observations=[dict(feature=feature,category=category)]))['observations'][0]['reference']
        assert (r['term'],r['definition_page'],r['figure'])==(name,page,figure) and r['source_id']==f['source_id']
        source_cases.append(dict(kind='original definition',category=category,expected_term=name,expected_page=page,expected_figure=figure,actual_locator=r['locator'],passed=True))
    for key,figure,category,page in f['caption_cases']:
        r=reference(dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='source_example',example_id=key))
        assert r['source_example']['figure']==figure and r['observations'][0]['reference']['id']==category
        assert 'p'+str(page)+',' in r['source_example']['locator']
        source_cases.append(dict(kind='original facsimile caption',example_id=key,expected_figure=figure,expected_category=category,expected_page=page,passed=True))
    g=json.loads(Path('tests/fixtures/graphology_geometry_examples.json').read_text(encoding='utf-8'));geometry_cases=[]
    for c in g['angle_cases']:
        actual=measure(dict(coordinate_system='cartesian_y_up',units='mm',baseline=c['baseline'],upstroke=c['upstroke']))
        assert abs(actual['baseline_angle']-c['baseline_angle'])<1e-10 and abs(actual['slant_from_baseline_normal']-c['slant'])<1e-10
        geometry_cases.append(dict(expected=c,actual=actual,passed=True))
    c=g['ratio_case'];a=measure(dict(coordinate_system='cartesian_y_up',units='mm',spacing={k:c[k] for k in ['x_height','word_gap','letter_gap','line_gap']}))
    assert [a['ratios'][k+'_over_x_height'] for k in ['word_gap','letter_gap','line_gap']]==c['expected']
    geometry_cases.append(dict(expected=c,actual=a,passed=True))
    Path('data/graphology-verification.json').write_text(json.dumps(dict(profile=PROFILE,source_id=f['source_id'],source_method=f['method'],source_cases=source_cases,
        geometry_method=g['method'],geometry_cases=geometry_cases,passed=True,limits=[f['limits'],g['limits']],personal_or_psychometric_validity_demonstrated=False),indent=2)+'\n',encoding='utf-8')
    print(len(source_cases),'independent source cases and',len(geometry_cases),'separate Euclidean geometry cases passed')


if __name__=='__main__':run()
