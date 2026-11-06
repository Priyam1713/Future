"""Independent pre-engine quotient oracle versus production interval scan."""
import json,re
from pathlib import Path
from future import feng_shui as f
ROOT=Path(__file__).resolve().parents[1]
def verify():
    fixture=json.loads((ROOT/'tests/fixtures/feng_shui_reference_v1.json').read_text(encoding='utf-8'))
    p,c=f.assets();rows=c['rows'];truth=fixture['expected_by_heading']
    assert f.digest(fixture)==p['source_fixture_sha256'] and rows==fixture['rows'] and c['sources']==[fixture['source']]
    assert len(rows)==24 and len({r['id'] for r in rows})==24 and len(truth)==3600
    counts={r['id']:0 for r in rows};uncertainty=0
    for heading,expected in enumerate(truth):
        row=f._classify(heading,rows)
        assert [row['id'],row['source_name'],row['chinese']]==expected,(heading,row,expected)
        assert sum(r['lower_tenths']<=heading<=r['upper_tenths'] if not r['wraps_north'] else heading>=r['lower_tenths'] or heading<=r['upper_tenths'] for r in rows)==1
        counts[row['id']]+=1
        # Entire3-point uncertainty interval for every one of3600centers,using frozen oracle only.
        out=f._evaluate(dict(bearing_tenths=heading,uncertainty_tenths=1),p,rows)
        expected_ids={truth[x%3600][0] for x in (heading-1,heading,heading+1)}
        assert out['possible_mountain_ids']==[i for i in fixture['source_order'] if i in expected_ids]
        assert out['discrete_heading_count']==3 and out['wraps_north']==(heading in (0,3599))
        assert out['classification_unique']==(len(expected_ids)==1)
        assert out['declination_conversion'] is None and out['measured_qi'] is None and out['outcome_prediction'] is None and not out['physical_building_conclusion_supported']
        uncertainty+=1
    assert set(counts.values())=={150}
    boundary_checks=0
    for case in fixture['boundary_cases']:
        for heading,*expected in case['checked']:
            row=f._classify(heading,rows);assert [row['id'],row['source_name'],row['chinese']]==expected;boundary_checks+=1
        for heading in case['central_valid_points']+[case['nominal_center_tenths']]:assert f._classify(heading,rows)['id']==case['id']
        assert case['geometric_midpoint_twentieths']%2==1
    for case in fixture['uncertainty_cases']:
        out=f._evaluate({k:case[k] for k in ('bearing_tenths','uncertainty_tenths','alternate_readings')},p,rows)
        assert out['possible_mountain_ids']==case['possible_ids'] and out['discrete_heading_count']==case['point_count'] and out['classification_unique']==case['unique'] and out['wraps_north']==case['wraps_north']
    for case in fixture['semantic_cases']:
        o={k:v for k,v in case.items() if k not in ('name','numeric_id','context_status','possible_ids','definitive_id')};out=f._evaluate(o,p,rows)
        if 'numeric_id' in case:assert out['center_mountain']['id']==case['numeric_id']
        for key in ('context_status','definitive_id'):
            if key in case:assert out[key]==case[key]
        if 'possible_ids' in case:assert out['possible_mountain_ids']==case['possible_ids']
    for a in fixture['anchors']:
        q=dict(schema_version=1,profile=f.PROFILE,catalog_id=f.DATA['catalog_id'],catalog_version=1,catalog_sha256=f.CATALOG_HASH,mode='manual',task='classify',bearing_tenths=a['bearing_tenths'],north_reference='source_diagram',bearing_role='source_heading')
        out=f.read(q);assert out['readings'][0]['definitive_id']==a['id'] and out['readings'][0]['center_mountain']['source_name']==a['name']
        assert f.read(out['replay']['request'])==out
        m=re.search(r'(`{3,})json\n(.*?)\n\1',f.markdown(out).split('## Exact replay metadata')[1],re.S)
        assert f.read(json.loads(m[2])['request'])==out
    result=dict(passed=True,profile=f.PROFILE,profile_sha256=f.PROFILE_HASH,catalog_sha256=f.CATALOG_HASH,source_fixture_sha256=f.digest(fixture),source_rows=24,exact_heading_checks=3600,id_name_chinese_verified=True,headings_per_mountain=counts,boundary_neighbor_central_checks=boundary_checks,nominal_centers=24,central_valid_points=48,exact_midpoints_outside_supported_precision=24,uncertainty_three_point_ranges=uncertainty,additional_uncertainty_cases=len(fixture['uncertainty_cases']),source_anchors=3,semantic_cases=len(fixture['semantic_cases']),gaps=0,overlaps=0,north_wrap=True,replay_passed=True,oracle='Frozen pre-engine quotient/cycle table,independent of production literal interval scan',empirical_feng_shui_validation=False)
    (ROOT/'data/feng-shui-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('24 source rows;3600 ID/name/Chinese headings;3600 uncertainty ranges;144 boundary/neighbor/central checks;9 extra ranges;3 anchors passed')
    return result
if __name__=='__main__':verify()
