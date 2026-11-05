import copy,json,re,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from future import bibliomancy as b
from future.__main__ import load_registry

F=json.loads(Path('tests/fixtures/bibliomancy_corpus_v1.json').read_text(encoding='utf-8'))
def q(path=None,**kw):
    return dict(schema_version=1,profile=b.PROFILE,mode='manual_coarse',corpus_id=b.DATA['corpus_id'],corpus_version=1,corpus_sha256=b.DATA['corpus_sha256'],index_id=b.DATA['index_id'],index_version=1,index_sha256=b.DATA['index_sha256'],selections=[dict(path=path or [1,1,2,1])])|kw
def h(faces=None,**kw):return dict(schema_version=1,profile=b.PROFILE,mode='homeric_index_reference',faces=faces or [1,3,6])|kw

class BibliomancyTests(unittest.TestCase):
    def reject(self,query):
        with self.assertRaises((ValueError,OSError)):b.read(query)
    def test_source_text_fixtures(self):
        for f in F['selections']:
            r=b.read(q(f['path']))['selections'][0];self.assertEqual((r['text'],r['sentence_id'],r['verse_ids']),(f['text'],f['id'],f['verses']))
    def test_full_integrity(self):self.assertTrue(b.integrity()['verified'])
    def test_first_citation(self):self.assertEqual(b.read(q())['selections'][0]['citation'],'Ruth 1:1')
    def test_last_citation(self):self.assertEqual(b.read(q([1,1,5,30]))['selections'][0]['citation'],'Ruth 4:18-22')
    def test_sentence_not_verse(self):
        a=b.read(q([1,1,2,1]))['selections'][0];c=b.read(q([1,1,2,2]))['selections'][0];self.assertEqual(a['verse_ids'],c['verse_ids']);self.assertNotEqual(a['text'],c['text'])
    def test_cross_verse(self):self.assertEqual(b.read(q([1,1,2,23]))['selections'][0]['citation'],'Ruth 1:12-13')
    def test_nested_quote(self):self.assertTrue(b.read(q([1,1,3,35]))['selections'][0]['text'].endswith('.’ ”'))
    def test_no_stray_closing_quote(self):self.assertTrue(b.read(q([1,1,3,36]))['selections'][0]['text'].startswith('Naomi'))
    def test_source_punctuation_outside_quote(self):self.assertTrue(b.read(q([1,1,5,27]))['selections'][0]['text'].endswith('Naomi”.'))
    def test_native_vs_page(self):
        s=b.read(q())['selections'][0];self.assertEqual(s['logical_page']['index'],2);self.assertEqual(s['logical_page']['native_chapter'],1);self.assertIsNone(s['logical_page']['printed_page'])
    def test_context_first_clips(self):self.assertEqual(b.read(q(context=2))['selections'][0]['context_before'],[])
    def test_context_last_clips(self):self.assertEqual(b.read(q([1,1,5,30],context=2))['selections'][0]['context_after'],[])
    def test_context_no_page_cross(self):self.assertEqual(b.read(q([1,1,2,41]))['selections'][0]['context_after'],[])
    def test_context_zero(self):
        s=b.read(q(context=0))['selections'][0];self.assertEqual(s['context_before']+s['context_after'],[])
    def test_context_previous_source(self):self.assertEqual(b.read(q([1,1,2,2]))['selections'][0]['context_before'][0]['text'],F['selections'][0]['text'])
    def test_multiple_order(self):
        paths=[[1,1,5,30],[1,1,2,1],[1,1,3,3]];r=b.read(q(selections=[dict(path=p) for p in paths]));self.assertEqual([s['path'] for s in r['selections']],paths)
    def test_repeated_preserved(self):
        r=b.read(q(selections=[dict(path=[1,1,2,1])]*2));self.assertEqual(len(r['selections']),2);self.assertEqual(r['comparison']['repeated_ids'],['RUT.1.s001'])
    def test_raw_user_text(self):
        raw='  Café Café\r\n猫\t `````json  ';r=b.read(q(question=raw,reflection=raw,notes=None));self.assertEqual(r['user_text'],dict(question=raw,reflection=raw,notes=None));self.assertEqual(r['selections'][0]['text'],F['selections'][0]['text'])
    def test_per_selection_reflection(self):
        r=b.read(q(selections=[dict(path=[1,1,2,1],reflection=' mine ')]));self.assertEqual(r['selections'][0]['user_reflection'],' mine ')
    def test_no_manual_probability(self):
        r=b.read(q());self.assertIsNone(r['selection_origin']['selection_probability']);self.assertFalse(r['selection_origin']['generated_draw']);self.assertFalse(r['replay']['rng'])
    def test_evidence_layers(self):self.assertEqual(set(b.read(q())['evidence_layers']),{'direct','editorial','user_attributed','unsupported'})
    def test_no_combined_meaning(self):self.assertIsNone(b.read(q())['comparison']['combined_meaning'])
    def test_homeric_first_last(self):self.assertEqual((b.read(h([1,1,1]))['historical_reference']['ordinal'],b.read(h([6,6,6]))['historical_reference']['ordinal']),(1,216))
    def test_homeric_historical_anchors(self):self.assertEqual((b.read(h())['historical_reference']['ordinal'],b.read(h([1,5,1]))['historical_reference']['ordinal']),(18,25))
    def test_homeric_order(self):self.assertNotEqual(b.read(h([1,3,6]))['historical_reference']['ordinal'],b.read(h([6,3,1]))['historical_reference']['ordinal'])
    def test_homeric_no_passage(self):
        r=b.read(h());self.assertIsNone(r['historical_reference']['passage']);self.assertEqual(r['selections'],[]);self.assertEqual(r['historical_reference']['verse_mapping'],'mapping unavailable')
    def test_homeric_year_distinction(self):
        x=b.read(h())['historical_reference']['context'];self.assertIn('2013',x['citation']);self.assertEqual(x['website_date'],'2014-03-28')
    def test_homeric_invalid(self):
        for faces in ([0,1,1],[7,1,1],[True,1,1],[1.0,1,1],[1,2],136):self.reject(h(faces))
    def test_all_path_levels_invalid(self):
        for level in range(4):
            for value in (0,-1,True,1.0,999,'1',None):
                p=[1,1,2,1];p[level]=value;self.reject(q(p))
    def test_empty_heading(self):self.reject(q([1,1,1,1]))
    def test_path_shape(self):
        for p in ([1,1,2],{},'1,1,2,1'):self.reject(q(selections=[dict(path=p)]))
    def test_missing_corpus_fields(self):
        for key in ('corpus_id','corpus_sha256','index_id','index_sha256','corpus_version','index_version'):
            x=q();x.pop(key);self.reject(x)
    def test_wrong_identity(self):
        for key in ('profile','corpus_id','corpus_sha256','index_id','index_sha256'):self.reject(q(**{key:'unknown'}))
    def test_edition_version(self):
        for key in ('corpus_version','index_version'):
            for version in (2,True,1.0):self.reject(q(**{key:version}))
    def test_unsupported_modes(self):
        for mode in ('fine','seeded','random','line'):self.reject(q(mode=mode))
    def test_unknown_field(self):self.reject(q(seed='x'))
    def test_unknown_sentence(self):self.reject(q(selections=[dict(path=[1,1,2,1],sentence_id='RUT.1.s002')]))
    def test_known_sentence_assertion(self):self.assertEqual(b.read(q(selections=[dict(path=[1,1,2,1],sentence_id='RUT.1.s001')]))['selections'][0]['sentence_id'],'RUT.1.s001')
    def test_selections_limits(self):
        for selections in ([],{},[dict(path=[1,1,2,1])]*33):self.reject(q(selections=selections))
    def test_context_limits(self):
        for context in (-1,3,True,1.0):self.reject(q(context=context))
    def test_raw_text_rejections(self):
        for text in ('\x00', '\ud800','x'*10001,123):self.reject(q(question=text))
    def test_schema_strict(self):
        for version in (True,1.0,2):self.reject(q(schema_version=version))
    def test_deepcopy_input_and_output(self):
        x=q();old=copy.deepcopy(x);r=b.read(x);r['replay']['request']['selections'][0]['path'][0]=99;self.assertEqual(x,old);self.assertEqual(b.read(x)['selections'][0]['path'][0],1)
    def test_exact_replay(self):
        r=b.read(q(reflection=' mine '));self.assertEqual(b.read(r['replay']['request']),r);self.assertNotEqual(r['replay']['input_sha256'],b.read(q(reflection='mine'))['replay']['input_sha256'])
    def test_markdown_replay(self):
        r=b.read(q(question=' ```json\n猫 '));m=re.search(r'(`{3,})json\n(.*?)\n\1',b.markdown(r).split('## Exact replay metadata')[1],re.S);self.assertEqual(b.read(json.loads(m[2])['request']),r)
    def test_strict_json_loader(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'q.json')
            for text in ('{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}'):
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):b.load_input(p)
    def asset_change(self,asset,change):
        import shutil
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'knowledge').mkdir();(root/'resources/corpora').mkdir(parents=True)
            for name in ('profile','corpus','index'):shutil.copyfile(b.ROOT/f'knowledge/bibliomancy_{name}_v1.json',root/f'knowledge/bibliomancy_{name}_v1.json')
            shutil.copytree(b.ROOT/'resources/corpora/webclassic-ruth-v1',root/'resources/corpora/webclassic-ruth-v1')
            change(root/asset)
            with patch.object(b,'ROOT',root):self.reject(q())
    def test_missing_corpus_asset(self):self.asset_change('knowledge/bibliomancy_corpus_v1.json',lambda p:p.unlink())
    def test_changed_corpus(self):self.asset_change('knowledge/bibliomancy_corpus_v1.json',lambda p:p.write_text('{}',encoding='utf-8'))
    def test_reordered_index(self):
        def change(p):
            x=json.loads(p.read_text(encoding='utf-8'));x['shelves'][0]['books'][0]['pages'].reverse();p.write_text(json.dumps(x),encoding='utf-8')
        self.asset_change('knowledge/bibliomancy_index_v1.json',change)
    def test_profile_tampering(self):self.asset_change('knowledge/bibliomancy_profile_v1.json',lambda p:p.write_text('{}',encoding='utf-8'))
    def test_raw_witness_change(self):self.asset_change('resources/corpora/webclassic-ruth-v1/RUT01.html',lambda p:p.write_bytes(p.read_bytes()+b' '))
    def test_registry_idempotence(self):
        r=load_registry()
        try:
            b.read(q(),r);b.read(h(),r);self.assertEqual(r.db.execute("select count(*) from rules where id like 'bibliomancy.%'").fetchone()[0],3)
        finally:r.close()
    def test_source_discrepancies_explicit(self):
        r=b.read(q());self.assertIn('08/09',r['source_discrepancies']['seventeen_books']);self.assertIn('0..18',r['source_discrepancies']['fine_word_count'])
    def test_snapshot_limitation(self):self.assertIsNone(b.read(q())['procedure_source']['snapshot_sha256'])
    def test_rights_and_single_book(self):
        r=b.read(q());self.assertIn('public domain',r['corpus']['source']['rights_note']);self.assertIn('one complete book',r['adaptation'])

if __name__=='__main__':unittest.main()
