import copy,json,re,tempfile,unittest
from pathlib import Path
from future import osteomancy as o
from future.__main__ import load_registry
F=json.loads(Path('tests/fixtures/osteomancy_reference_v1.json').read_text(encoding='utf-8'))
def q(**kw):return dict(schema_version=1,profile=o.PROFILE,mode='documentary',task='reference',case_ids=['8'])|kw
def select_group(group):return dict(schema_version=1,profile=o.PROFILE,mode='documentary',task='group',group=group)

class OsteomancyTests(unittest.TestCase):
    def reject(self,**kw):
        with self.assertRaises(ValueError):o.read(q(**kw))
    def test_source_identity(self):self.assertEqual(o.thaw(o.DATA['source']),F['source'])
    def test_complete_ids(self):self.assertEqual(list(o.CASES),F['case_ids']);self.assertEqual(len(o.CASES),13)
    def test_all_facts(self):
        for c in F['cases']:
            actual=o.lookup(c['case_id']);actual.pop('source_deep_link');self.assertEqual(actual,c)
    def test_attribution(self):
        r=o.read(q());self.assertIn('de Bary',r['source']['author']);self.assertIn('1999',r['source']['edition']);self.assertIn('not the cited',r['source_context'])
    def test_rights(self):self.assertIn('not a blanket',o.DATA['source']['rights_note'])
    def test_day_labels(self):
        for i,(label,index) in F['expected_checks']['days'].items():self.assertEqual(o.lookup(i)['components']['day']['value'],dict(label=label,source_day_index=index))
    def test_no_inherit_dates(self):self.assertIsNone(o.lookup('20B')['components']['day']['value']);self.assertIsNone(o.lookup('9B')['components']['diviner']['value'])
    def test_lunar_months(self):
        self.assertEqual(o.lookup('19A')['components']['lunar_month']['value']['number'],3);self.assertIsNone(o.lookup('19B')['components']['lunar_month']['value'])
    def test_diviners(self):
        for i,v in F['expected_checks']['diviners'].items():self.assertEqual(o.lookup(i)['components']['diviner']['value'],v)
    def test_no_calendar(self):self.assertFalse(o.read(q())['chronological_boundary']['calendar_conversion'])
    def test_no_outcome(self):
        for i in o.ORDER:
            for k in ('prognostication','verification'):
                c=o.lookup(i)['components'][k];self.assertIsNone(c['value']);self.assertEqual(c['status'],'omitted_from_inspected_excerpt');self.assertEqual(c['original_inscription_status'],'not_independently_verified')
    def test_original_unknown(self):
        for i in o.ORDER:self.assertTrue(all(v['status']=='not_independently_verified' for v in o.lookup(i)['original_evidence'].values()))
    def test_source_editorial_context(self):
        a=o.lookup('8');self.assertNotIn('Wu Ding',a['components']['participants']['value']);self.assertIn('Wu Ding',a['source_editorial_context']['kinship'])
    def test_both_actions_uncertain(self):
        for i in ('20A','20B'):self.assertEqual(o.lookup(i)['components']['action'],dict(status='explicitly_uncertain_in_source',value='(doing something?)',original_inscription_status='not_independently_verified'))
    def test_target_uncertainty(self):self.assertEqual(o.lookup('10')['components']['target']['value'],'(it/him)')
    def test_editorial_preface(self):self.assertEqual(o.lookup('23')['components']['preface']['value'],'[Divined:]');self.assertIsNone(o.lookup('24A')['components']['preface']['value'])
    def test_9_opposition(self):self.assertEqual(o.compare('9A','9B')['relationship']['classification'],'explicitly_contrasted_charge')
    def test_19_conditions(self):
        r=o.compare('19A','19B');self.assertEqual(r['relationship']['classification'],'differently_conditioned_charge');self.assertEqual(r['component_comparison']['condition']['status'],'different_source_values')
    def test_20_uncertainty(self):self.assertEqual(o.compare('20A','20B')['component_comparison']['action']['status'],'incomparable_uncertainty')
    def test_22_opposition(self):self.assertEqual(o.compare('22A','22B')['relationship']['opposition'],'asserted_vs_denied_named_cause')
    def test_24_distinct(self):self.assertEqual(o.compare('24A','24B')['relationship']['classification'],'distinct_propositions')
    def test_unresolved(self):self.assertEqual(o.compare('8','24B')['relationship']['classification'],'relationship_unresolved')
    def test_same_record(self):self.assertEqual(o.compare('8','8')['relationship']['classification'],'same_record')
    def test_reverse_stable(self):
        a=o.compare('19A','19B');b=o.compare('19B','19A');a.pop('requested_order');b.pop('requested_order');self.assertEqual(a,b)
    def test_missing_not_shared(self):self.assertEqual(o.compare('9A','9B')['component_comparison']['verification']['status'],'incomparable_missing_evidence')
    def test_ordered_multiple(self):self.assertEqual(o.read(q(case_ids=['24B','8','19A']))['selected_case_ids'],['24B','8','19A'])
    def test_multiple_comparison(self):self.assertEqual(len(o.read(q(task='compare',case_ids=['8','9A','9B']))['comparisons']),3)
    def test_groups(self):
        for r in F['relationships']:self.assertEqual(o.read(select_group(r['group']))['selected_case_ids'],r['pair'])
    def test_topic(self):
        v=dict(schema_version=1,profile=o.PROFILE,mode='documentary',task='topic',topic='royal_affliction');self.assertEqual(o.read(v)['selected_case_ids'],['8','9A','9B','10'])
    def test_annotations_unicode(self):
        s='  Café Café\r\n猫\t `````json ';v=q(notes=s,annotations=[dict(case_id='8',note=s,association=s)]);r=o.read(v);self.assertEqual(r['replay']['request'],v);self.assertEqual(r['user_annotations'][0]['note'],s)
    def test_no_user_override(self):self.reject(annotations=[dict(case_id='8',note='x',charge='occurred')])
    def test_copy_and_immutable(self):
        r=o.lookup('8');r['components']['day']['value']['label']='changed';self.assertEqual(o.lookup('8')['components']['day']['value']['label'],'yiwei')
        with self.assertRaises(TypeError):o.DATA['profile']='x'
    def test_replay_hash(self):
        r=o.read(q(notes='x'));self.assertEqual(o.read(r['replay']['request']),r);self.assertNotEqual(o.read(q(notes=' x'))['replay']['input_sha256'],r['replay']['input_sha256'])
    def test_markdown_replay(self):
        r=o.read(q(notes='`````json\n猫'));text=o.markdown(r);m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);self.assertEqual(o.read(json.loads(m[2])['request']),r)
    def test_registry(self):
        r=load_registry()
        try:o.register_knowledge(r);o.register_knowledge(r);self.assertEqual(r.db.execute("select count(*) from rules where id like 'osteomancy.%'").fetchone()[0],18)
        finally:r.close()
    def test_unknown_id(self):
        for i in ['99','9a',9,{},None]:self.reject(case_ids=[i])
    def test_duplicate_id(self):self.reject(case_ids=['8','8'])
    def test_wrong_selectors(self):self.reject(group='ancestor-harm')
    def test_bad_group(self):
        with self.assertRaises(ValueError):o.read(select_group('all-bones'))
    def test_bad_topic(self):
        v=dict(schema_version=1,profile=o.PROFILE,mode='documentary',task='topic',topic='spirits')
        with self.assertRaises(ValueError):o.read(v)
    def test_annotation_unselected(self):self.reject(annotations=[dict(case_id='9A',note='x')])
    def test_schema_and_mode(self):
        for k,v in [('schema_version',True),('profile','keightley'),('mode','seeded')]:self.reject(**{k:v})
    def test_unsupported(self):
        for task in ['bone_toss','crack_classification','prediction']:self.reject(task=task)
        self.reject(seed='x');self.reject(artifact_id='museum-image')
    def test_invalid_comparison(self):self.reject(task='compare')
    def test_invalid_text(self):
        for text in ['x'*10001,'\0','\ud800',3]:self.reject(notes=text)
    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'q.json')
            for t in ['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}']:
                p.write_text(t,encoding='utf-8')
                with self.assertRaises(ValueError):o.load_input(p)

if __name__=='__main__':unittest.main()
