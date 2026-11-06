import copy,json,re,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from future import feng_shui as f
from future.__main__ import load_registry
F=json.loads(Path('tests/fixtures/feng_shui_reference_v1.json').read_text(encoding='utf-8'))
def reading(h=920,**kw):return dict(reading_id='r1',bearing_tenths=h,north_reference='source_diagram',bearing_role='source_heading')|kw
def q(h=920,**kw):return dict(schema_version=1,profile=f.PROFILE,catalog_id=f.DATA['catalog_id'],catalog_version=1,catalog_sha256=f.CATALOG_HASH,mode='manual',task='classify',bearing_tenths=h,north_reference='source_diagram',bearing_role='source_heading')|kw
def compare(a=None,b=None,**kw):return {k:v for k,v in q(**(dict(task='compare',readings=[a or reading(),b or reading(1800,reading_id='r2')])|kw)).items() if k not in f.READING_FIELDS}
def ref(ids):return {k:v for k,v in q(task='reference',reference_ids=ids).items() if k not in f.READING_FIELDS}
def result(h=920,**kw):return f.read(q(h,**kw))['readings'][0]
class FengShuiTests(unittest.TestCase):
    def reject(self,x):
        with self.assertRaises((ValueError,OSError)):f.read(x)
    def test_source_rows(self):self.assertEqual(f.assets()[1]['rows'],F['rows'])
    def test_integrity(self):self.assertTrue(f.integrity()['verified']);self.assertEqual(f.integrity()['rows'],24)
    def test_source_identity(self):s=f.assets()[1]['sources'][0];self.assertEqual(s['snapshot_sha256'],'ef6a47bbb7da8a2b0a1483ed56783a123626b9f82d0614784d6346fb382cec3a');self.assertIsNone(s['rank'])
    def test_anchor92(self):r=result();self.assertEqual(r['definitive_id'],'E2');self.assertEqual(r['center_mountain']['source_label'],'Mao 卯')
    def test_upper75(self):self.assertEqual(result(75)['definitive_id'],'N2')
    def test_lower76(self):self.assertEqual(result(76)['definitive_id'],'N3')
    def test_zero(self):self.assertEqual(result(0)['definitive_id'],'N2')
    def test_last(self):self.assertEqual(result(3599)['definitive_id'],'N2')
    def test_cardinals(self):
        for h,id in [(0,'N2'),(900,'E2'),(1800,'S2'),(2700,'W2')]:self.assertEqual(result(h)['definitive_id'],id)
    def test_all_endpoints(self):
        for r in F['rows']:
            for h in (r['lower_tenths'],r['upper_tenths']):self.assertEqual(f.classify(h)['id'],r['id'])
    def test_both_central_points(self):
        for r in F['boundary_cases']:
            for h in r['central_valid_points']:self.assertEqual(f.classify(h)['id'],r['id'])
    def test_printed_bounds(self):self.assertEqual(f.lookup('N2')['lower_display_degrees'],'352.6');self.assertEqual(f.lookup('N2')['upper_display_degrees'],'7.5')
    def test_neighbor_cycle(self):self.assertEqual(f.lookup('S1')['previous_id'],'SE3');self.assertEqual(f.lookup('SE3')['next_id'],'S1')
    def test_reference_name(self):self.assertEqual(f.lookup('Zi')['id'],'N2')
    def test_reference_chinese(self):self.assertEqual(f.lookup('酉')['id'],'W2')
    def test_reference_full_label(self):self.assertEqual(f.lookup('Mao 卯')['id'],'E2')
    def test_reference_no_bearing(self):r=f.read(ref(['N2','N3']));self.assertEqual(r['readings'],[]);self.assertEqual([x['id'] for x in r['references']],['N2','N3'])
    def test_catalog_source_order(self):r=f.read({k:v for k,v in ref([]).items() if k!='reference_ids'}|dict(task='catalog'));self.assertEqual([x['id'] for x in r['references']],F['source_order'])
    def test_exact_has_one_point(self):r=result();self.assertTrue(r['classification_unique']);self.assertEqual(r['discrete_heading_count'],1)
    def test_boundary_uncertainty(self):r=result(75,uncertainty_tenths=1);self.assertEqual(r['possible_mountain_ids'],['N2','N3']);self.assertIsNone(r['definitive_id']);self.assertTrue(r['uncertainty_crosses_boundary']);self.assertEqual(r['status'],'ambiguous')
    def test_north_wrap_unique(self):r=result(0,uncertainty_tenths=1);self.assertTrue(r['wraps_north']);self.assertEqual(r['possible_mountain_ids'],['N2']);self.assertEqual(r['discrete_heading_count'],3)
    def test_wide_north_range(self):r=result(3599,uncertainty_tenths=100);self.assertEqual(r['possible_mountain_ids'],['N1','N2','N3']);self.assertEqual(r['discrete_heading_count'],201)
    def test_whole_domain(self):r=result(920,uncertainty_tenths=1800);self.assertEqual(r['discrete_heading_count'],3600);self.assertEqual(set(r['heading_counts_by_mountain'].values()),{150});self.assertEqual(len(r['possible_mountains']),24)
    def test_alternate_disagreement(self):r=result(75,alternate_readings=[76]);self.assertEqual(r['possible_mountain_ids'],['N2','N3']);self.assertTrue(r['candidate_readings_disagree']);self.assertFalse(r['uncertainty_crosses_boundary'])
    def test_same_sector_alternates(self):r=result(920,alternate_readings=[930]);self.assertTrue(r['classification_unique']);self.assertEqual(r['discrete_heading_count'],2)
    def test_uncertainty_every_alternate(self):r=result(75,uncertainty_tenths=1,alternate_readings=[3525]);self.assertEqual(r['possible_mountain_ids'],['N1','N2','N3']);self.assertEqual(r['discrete_heading_count'],6)
    def test_range_union_deduplicates(self):r=result(75,uncertainty_tenths=1,alternate_readings=[76]);self.assertEqual(r['discrete_heading_count'],4)
    def test_missing_frame(self):x=q();x.pop('north_reference');r=f.read(x)['readings'][0];self.assertEqual(r['context_status'],'insufficient_evidence');self.assertEqual(r['definitive_id'],'E2');self.assertNotIn('north_reference',r['declared'])
    def test_missing_role(self):x=q();x.pop('bearing_role');r=f.read(x)['readings'][0];self.assertEqual(r['bearing_role'],'unknown');self.assertEqual(r['context_status'],'insufficient_evidence')
    def test_explicit_unknown(self):r=result(north_reference='unknown',bearing_role='unknown');self.assertEqual(r['context_status'],'insufficient_evidence');self.assertEqual(r['definitive_id'],'E2')
    def test_source_frame(self):self.assertEqual(result()['context_status'],'source_diagram')
    def test_magnetic_no_conversion(self):r=result(north_reference='magnetic',bearing_role='building_facing');self.assertEqual(r['context_status'],'declared_only_no_conversion');self.assertIsNone(r['declination_conversion'])
    def test_true_no_conversion(self):r=result(north_reference='true',bearing_role='building_sitting');self.assertEqual(r['north_reference'],'true');self.assertIsNone(r['declination_conversion'])
    def test_source_diagram_physical_role(self):self.assertEqual(result(bearing_role='door')['context_status'],'unsupported_physical_frame')
    def test_door_is_not_facing(self):r=result(north_reference='magnetic',bearing_role='door',raw_observation='main facade');self.assertEqual(r['bearing_role'],'door');self.assertIsNone(r['independent_declarations']['generated_opposite'])
    def test_observer_role(self):self.assertEqual(result(bearing_role='observer')['bearing_role'],'observer')
    def test_frame_contradiction(self):r=result(north_reference='magnetic',contradictory_assertions={'north_reference':['true']});self.assertEqual(r['status'],'conflicting_evidence');self.assertIsNone(r['definitive_id'])
    def test_role_contradiction(self):r=result(contradictory_assertions={'bearing_role':['door']});self.assertEqual(r['structured_conflicts'],['bearing_role'])
    def test_bearing_contradiction(self):r=result(contradictory_assertions={'bearing_tenths':[1800]});self.assertEqual(r['possible_mountain_ids'],['S2','E2']);self.assertIsNone(r['definitive_id'])
    def test_assertion_does_not_fill_unknown(self):r=result(north_reference='unknown',contradictory_assertions={'north_reference':['magnetic']});self.assertEqual(r['north_reference'],'unknown');self.assertEqual(r['context_status'],'insufficient_evidence')
    def test_known_assertions_conflict_without_declaration(self):r=result(north_reference='unknown',contradictory_assertions={'north_reference':['magnetic','true']});self.assertIn('north_reference',r['structured_conflicts'])
    def test_independent_opposites(self):r=result(1800,north_reference='magnetic',bearing_role='building_facing',declared_facing_tenths=1800,declared_sitting_tenths=0);self.assertEqual(r['structured_conflicts'],[])
    def test_independent_nonopposites(self):r=result(1800,declared_facing_tenths=1800,declared_sitting_tenths=10);self.assertIn('independent_facing_sitting_not_opposite',r['structured_conflicts'])
    def test_primary_facing_mismatch(self):r=result(1800,bearing_role='building_facing',declared_facing_tenths=1700);self.assertIn('primary_vs_declared_facing',r['structured_conflicts'])
    def test_primary_sitting_mismatch(self):r=result(0,bearing_role='building_sitting',declared_sitting_tenths=10);self.assertIn('primary_vs_declared_sitting',r['structured_conflicts'])
    def test_no_generated_opposite(self):self.assertIsNone(result(declared_facing_tenths=1800)['independent_declarations']['sitting_tenths'])
    def test_no_shared_building_inferred(self):r=f.read(compare());self.assertFalse(r['comparisons'][0]['same_declared_building'])
    def test_explicit_shared_building(self):r=f.read(compare(reading(0,building_id='house'),reading(1800,reading_id='r2',building_id='house')));self.assertTrue(r['comparisons'][0]['same_declared_building']);self.assertTrue(r['comparisons'][0]['centers_opposite'])
    def test_comparison_distinct_roles(self):r=f.read(compare(reading(bearing_role='door'),reading(1800,reading_id='r2',bearing_role='building_facing')));self.assertEqual(r['comparisons'][0]['roles'],['door','building_facing'])
    def test_comparison_different_frames(self):r=f.read(compare(reading(north_reference='magnetic'),reading(1800,reading_id='r2',north_reference='true')));self.assertIsNone(r['comparisons'][0]['clockwise_delta_tenths'])
    def test_comparison_unknown_frame(self):r=f.read(compare(reading(north_reference='unknown'),reading(1800,reading_id='r2',north_reference='unknown')));self.assertIsNone(r['comparisons'][0]['centers_opposite'])
    def test_no_outcome_score(self):r=result();self.assertIsNone(r['outcome_prediction']);self.assertIsNone(r['measured_qi']);self.assertFalse(r['physical_building_conclusion_supported'])
    def test_precision_display(self):self.assertEqual(result(1)['bearing_degrees_display'],'0.1')
    def test_invalid_numeric_fixture(self):
        for case in F['invalid_numeric_cases']:self.reject(q(case['bearing_tenths']))
    def test_missing_bearing(self):x=q();x.pop('bearing_tenths');self.reject(x)
    def test_invalid_uncertainty(self):
        for v in (-1,1801,1.0,True,'1'):self.reject(q(uncertainty_tenths=v))
    def test_invalid_alternates(self):self.reject(q(alternate_readings=[True]));self.reject(q(alternate_readings=[1,1]));self.reject(q(alternate_readings=list(range(13))))
    def test_invalid_enum(self):self.reject(q(north_reference='north'));self.reject(q(bearing_role='facade'));self.reject(q(bearing_role=True))
    def test_invalid_independent_declarations(self):self.reject(q(declared_sitting_tenths=3600));self.reject(q(declared_facing_tenths=True))
    def test_invalid_assertions(self):self.reject(q(contradictory_assertions={'bearing_tenths':[7.55]}));self.reject(q(contradictory_assertions={'north_reference':['other']}));self.reject(q(contradictory_assertions={'bearing_role':[]}))
    def test_strict_schema_version(self):
        for v in (True,1.0,2):self.reject(q(schema_version=v));self.reject(q(catalog_version=v))
    def test_wrong_hash_profile(self):self.reject(q(catalog_sha256='0'*64));self.reject(q(profile='unknown'));self.reject(q(catalog_id='eight-mansions'))
    def test_other_tasks(self):self.reject(q(task='predict'));self.reject(q(task='flying-stars'))
    def test_unknown_fields(self):self.reject(q(bearing_degrees=7.55));self.reject(q(declination=2))
    def test_reference_validation(self):self.reject(ref([]));self.reject(ref(['N2','Zi']));self.reject(ref(['unknown']));self.reject(ref([12]))
    def test_compare_limits(self):self.reject(compare(reading(),reading(reading_id='r1')));self.reject(compare(readings=[]));self.reject(compare(readings=[reading(reading_id='a'+str(i)) for i in range(9)]))
    def test_identifier_validation(self):self.reject(q(reading_id='a b'));self.reject(q(building_id='猫'));self.reject(compare(reading(reading_id=''),reading(reading_id='x')))
    def test_raw_unicode(self):raw='  Café Café\r\n猫\t `````json ';r=f.read(q(question=raw,reflection=raw,raw_observation=raw));self.assertEqual(r['user_text']['question'],raw);self.assertEqual(r['readings'][0]['declared']['raw_observation'],raw)
    def test_raw_invalid(self):
        for v in (12,'\ud800','\x00','x'*10001):self.reject(q(notes=v))
    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'q.json')
            for text in F['raw_json_failures']:
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):f.load_input(p)
    def test_replay(self):r=f.read(q(notes=' x '));self.assertEqual(f.read(r['replay']['request']),r)
    def test_markdown_replay(self):r=f.read(q(notes='`````json 猫'));m=re.search(r'(`{3,})json\n(.*?)\n\1',f.markdown(r).split('## Exact replay metadata')[1],re.S);self.assertEqual(f.read(json.loads(m[2])['request']),r)
    def test_deepcopy(self):x=q();old=copy.deepcopy(x);r=f.read(x);r['readings'][0]['declared']['bearing_tenths']=0;self.assertEqual(x,old)
    def test_registry(self):
        r=load_registry()
        try:
            f.read(q(),r);f.read(q(),r);records=[json.loads(x[0]) for x in r.db.execute("select record from rules where id like 'feng-shui.%'")];self.assertEqual(len(records),24);self.assertTrue(all(x['status']=='verified' and x['evidence_kind']=='computational' for x in records))
        finally:r.close()
    def test_asset_tampering(self):
        for name in ('catalog','profile'):
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);(root/'knowledge').mkdir()
                for stem in ('catalog','profile'):(root/f'knowledge/feng_shui_{stem}_v1.json').write_bytes((f.ROOT/f'knowledge/feng_shui_{stem}_v1.json').read_bytes())
                (root/f'knowledge/feng_shui_{name}_v1.json').write_text('{}',encoding='utf-8')
                with patch.object(f,'ROOT',root):self.reject(q())
    def test_missing_asset(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(f,'ROOT',Path(d)):self.reject(q())
if __name__=='__main__':unittest.main()
