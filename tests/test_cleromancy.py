import copy,json,re,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from future import cleromancy as e,cleromancy_catalog as c
from future.__main__ import load_registry
F=json.loads(Path('tests/fixtures/cleromancy_reference_v1.json').read_text(encoding='utf-8'))
def q(**kw):return dict(schema_version=1,profile=c.PROFILE,mode='manual',task='reading',catalog_id=c.DATA['catalog_id'],catalog_version=1,catalog_sha256=c.CATALOG_HASH,mark='gao-alpha')|kw
def cat(**kw):return {k:v for k,v in q(task='catalog').items() if k!='mark'}|kw

class CleromancyTests(unittest.TestCase):
    def reject(self,query):
        with self.assertRaises((ValueError,OSError)):e.read(query)
    def test_complete_catalog(self):self.assertEqual(c.catalog(),F['marks'])
    def test_all_source_accounts(self):
        for r in F['marks']:self.assertEqual(e.read(q(mark=r['id']))['selected_mark'],r)
    def test_all_aliases(self):
        for raw,expected in F['aliases'].items():self.assertEqual(c.identify(raw)['canonical_id'],expected)
    def test_order(self):self.assertEqual([x['order'] for x in c.catalog()],list(range(1,25)))
    def test_alpha(self):self.assertEqual(e.read(q(mark='Α'))['selected_mark']['account_tag'],'apollo_success')
    def test_omega(self):self.assertEqual(e.read(q(mark='ω'))['selected_mark']['account_tag'],'harsh_harvest')
    def test_epsilon_not_prediction(self):self.assertIn('descriptive',e.read(q(mark='epsilon'))['selected_mark']['lexical_qualification'])
    def test_eta_not_automatic_protection(self):self.assertIn('further commentary',e.read(q(mark='eta'))['selected_mark']['lexical_qualification'])
    def test_lambda_not_augury(self):self.assertIn('observer orientation',e.read(q(mark='lambda'))['selected_mark']['lexical_qualification'])
    def test_chi_khi(self):self.assertEqual(c.lookup('Chi')['record'],c.lookup('Khi')['record']);self.assertEqual(c.lookup('chi')['record']['source_display'],'Khi')
    def test_all_greek_lowercase(self):
        for r in F['marks']:self.assertEqual(c.lookup(r['lowercase'])['record']['glyph'],r['glyph'])
    def test_final_sigma(self):self.assertEqual(c.lookup('ς')['record']['id'],'gao-sigma')
    def test_ascii_case_trim(self):self.assertEqual(c.identify(' \tGAO-ALPHA\r\n')['canonical_id'],'gao-alpha')
    def test_no_confusable_folding(self):
        for mark in F['rejected_aliases']:self.reject(q(mark=mark))
    def test_accented_and_compatibility_rejected(self):
        for mark in ('α\u0301','ϐ','Ａ','𝐀','Ϲ'):self.reject(q(mark=mark))
    def test_invalid_unicode(self):
        for mark in ('\ud800','\x00','x'*81):self.reject(q(mark=mark))
    def test_invalid_mark_types(self):
        for mark in (None,True,1,1.0,[],{}):self.reject(q(mark=mark))
    def test_missing_mark(self):x=q();x.pop('mark');self.reject(x)
    def test_raw_mark_trace(self):self.assertEqual(e.read(q(mark=' Alpha '))['selection']['normalization']['raw'],' Alpha ')
    def test_ambiguous_alias_table(self):
        p,table=c.assets();table['aliases']['ALPHA']='gao-beta'
        with self.assertRaisesRegex(ValueError,'Ambiguous'):c.alias_index(table)
    def test_unknown_alias_target(self):
        p,table=c.assets();table['aliases']['test']='unknown'
        with self.assertRaises(ValueError):c.alias_index(table)
    def test_catalog_task(self):
        r=e.read(cat());self.assertEqual(len(r['catalog_records']),24);self.assertIsNone(r['selection']);self.assertIsNone(r['selected_mark'])
    def test_catalog_cannot_select(self):self.reject(cat(mark='alpha'))
    def test_lookup(self):self.assertEqual(e.read(q(task='lookup'))['selected_mark']['id'],'gao-alpha')
    def test_origin_default_unknown(self):self.assertEqual(e.read(q())['selection']['observation_origin'],'unknown')
    def test_origins(self):
        for origin in ('reported_real','hypothetical','unknown'):self.assertEqual(e.read(q(observation_origin=origin))['selection']['observation_origin'],origin)
    def test_invalid_origin(self):
        for origin in ('verified',None,True,[]):self.reject(q(observation_origin=origin))
    def test_no_generated_probability(self):
        x=e.read(q(observation_origin='reported_real'))['selection'];self.assertFalse(x['generated']);self.assertFalse(x['physical_selection_verified']);self.assertIsNone(x['probability'])
    def test_raw_context(self):
        raw='  Café Café\r\n猫\t `````json ';r=e.read(q(question=raw,association=raw,reflection=raw,notes=None,uncertainty=' unsure '));self.assertEqual(r['user_text']['question'],raw);self.assertEqual(r['user_text']['association'],raw);self.assertIsNone(r['user_text']['notes'])
    def test_invalid_user_text(self):
        for value in (123,'\ud800','\x00','x'*10001):self.reject(q(question=value))
    def test_question_cannot_select(self):self.assertEqual(e.read(q(question='Omega?'))['selected_mark']['id'],'gao-alpha')
    def test_same_mark_different_questions(self):
        a=e.read(q(question='A'));b=e.read(q(question='B'));self.assertEqual(a['selected_mark'],b['selected_mark']);self.assertNotEqual(a['replay']['input_sha256'],b['replay']['input_sha256'])
    def test_no_user_application(self):self.assertIsNone(e.read(q())['source_interpretation']['user_application'])
    def test_observation_uncertainty_does_not_change_meaning(self):self.assertEqual(e.read(q(uncertainty='guess'))['selected_mark'],e.read(q())['selected_mark'])
    def test_invalid_profile(self):self.reject(q(profile='generic-greek'))
    def test_hash_mismatch(self):self.reject(q(catalog_sha256='0'*64))
    def test_unknown_catalog(self):self.reject(q(catalog_id='unknown'))
    def test_version_types(self):
        for value in (True,1.0,2):self.reject(q(catalog_version=value));self.reject(q(schema_version=value))
    def test_missing_identity(self):
        for key in ('catalog_id','catalog_version','catalog_sha256'):
            x=q();x.pop(key);self.reject(x)
    def test_numeric_and_seeded_unsupported(self):
        for mode in ('five_astragaloi','five_d6','homeric','seeded'):self.reject(q(mode=mode))
    def test_prediction_rejected(self):self.reject(q(task='predict'))
    def test_multi_draw_rejected(self):self.reject(q(marks=['alpha','beta']))
    def test_numeric_fields_rejected(self):self.reject(q(faces=[6,5,3,6,6]))
    def test_unsupported_seed(self):self.reject(q(seed='x'))
    def test_exact_replay(self):
        r=e.read(q(notes=' x '));self.assertEqual(e.read(r['replay']['request']),r)
    def test_markdown_replay(self):
        r=e.read(q(notes='`````json 猫'));m=re.search(r'(`{3,})json\n(.*?)\n\1',e.markdown(r).split('## Exact replay metadata')[1],re.S);self.assertEqual(e.read(json.loads(m[2])['request']),r)
    def test_deep_copy(self):
        x=q();saved=copy.deepcopy(x);r=e.read(x);r['selected_mark']['name']='changed';r['replay']['request']['mark']='omega';self.assertEqual(x,saved);self.assertEqual(e.read(x)['selected_mark']['name'],'Alpha')
    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'q.json')
            for text in ('{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}'):
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):e.load_input(p)
    def test_registry_idempotence(self):
        r=load_registry()
        try:e.read(q(),r);e.read(cat(),r);self.assertEqual(r.db.execute("select count(*) from rules where id like 'cleromancy.%'").fetchone()[0],25)
        finally:r.close()
    def test_source_snapshot_unavailable(self):self.assertIsNone(e.read(q())['replay']['source_html_sha256']);self.assertIn('certificate',e.read(q())['source']['access'])
    def test_historical_attribution(self):self.assertIn('not independently',e.read(q())['selected_mark']['historical_attribution'])
    def test_evidence_layers(self):self.assertEqual(set(e.read(q())['evidence_matrix']),{'direct','compositional','user_attributed','unsupported'})
    def test_impossible_example_not_corrected(self):
        d=e.read(q())['numeric_discrepancies']['impossible_face'];self.assertEqual(d['faces'],[6,5,3,6,6]);self.assertEqual(d['source_sum'],26);self.assertFalse(d['accepted_vector'])
    def test_column_conflict_retained(self):self.assertIn('reverses',e.read(q())['numeric_discrepancies']['columns'])
    def test_rights_not_translation_corpus(self):self.assertIn('no complete',e.read(q())['rights'])
    def asset_change(self,name,mutate):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'knowledge').mkdir()
            for stem in ('profile','catalog'):
                p=root/f'knowledge/cleromancy_{stem}_v1.json';p.write_bytes((c.ROOT/f'knowledge/cleromancy_{stem}_v1.json').read_bytes())
            mutate(root/f'knowledge/cleromancy_{name}_v1.json')
            with patch.object(c,'ROOT',root):self.reject(q())
    def test_missing_catalog(self):self.asset_change('catalog',lambda p:p.unlink())
    def test_reordered_catalog(self):
        def change(p):
            x=json.loads(p.read_text(encoding='utf-8'));x['marks'].reverse();p.write_text(json.dumps(x),encoding='utf-8')
        self.asset_change('catalog',change)
    def test_changed_meaning(self):
        def change(p):
            x=json.loads(p.read_text(encoding='utf-8'));x['marks'][0]['source_account']='fabricated';p.write_text(json.dumps(x),encoding='utf-8')
        self.asset_change('catalog',change)
    def test_profile_tamper(self):self.asset_change('profile',lambda p:p.write_text('{}',encoding='utf-8'))

if __name__=='__main__':unittest.main()
