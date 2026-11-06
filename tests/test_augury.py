import copy,json,re,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from future import augury as a
from future.__main__ import load_registry
F=json.loads(Path('tests/fixtures/augury_reference_v1.json').read_text(encoding='utf-8'))
def obs(**kw):return dict(observation_id='obs1',bird_label='crow',phenomenon='call',relative_side='left',relation='located_on_side',reference_frame='observer_relative')|kw
def q(o=None,**kw):return dict(schema_version=1,profile=a.PROFILE,mode='manual',task='observe',catalog_id=a.DATA['catalog_id'],catalog_version=1,catalog_sha256=a.CATALOG_HASH,observations=[o or obs()])|kw
def ref(ids):return {k:v for k,v in q(task='reference',reference_ids=ids).items() if k!='observations'}
def result(o=None):return a.read(q(o))['observations'][0]
class AuguryTests(unittest.TestCase):
    def reject(self,x):
        with self.assertRaises((ValueError,OSError)):a.read(x)
    def test_all_source_records(self):self.assertEqual(a.assets()[1]['records'],F['records'])
    def test_source_hashes(self):self.assertTrue(a.integrity()['verified']);self.assertEqual(len(a.assets()[1]['sources']),4)
    def test_crow_call_no_favorable(self):r=result();self.assertEqual(r['applicable_main_ids'],['call-crow-left']);self.assertEqual(r['favorable_main_source_ids'],[])
    def test_call_crow_source_conflict(self):self.assertEqual(result()['status'],'conflicting_evidence')
    def test_raven_call(self):r=result(obs(bird_label='raven',relative_side='right'));self.assertEqual(r['status'],'applicable');self.assertEqual(r['favorable_main_source_ids'],[])
    def test_crow_flight(self):r=result(obs(phenomenon='flight',relation='moving_to_side'));self.assertEqual(r['favorable_main_source_ids'],['flight-crow-left'])
    def test_raven_flight(self):self.assertEqual(result(obs(bird_label='raven',phenomenon='flight',relative_side='right',relation='moving_to_side'))['favorable_main_source_ids'],['flight-raven-right'])
    def test_no_opposite_inversion(self):r=result(obs(phenomenon='flight',relative_side='right',relation='moving_to_side'));self.assertEqual(r['status'],'not_applicable');self.assertIsNone(r['empirical_prediction'])
    def test_unknown_phenomenon(self):self.assertEqual(result(obs(phenomenon='unknown'))['status'],'insufficient_evidence')
    def test_unknown_side(self):self.assertEqual(result(obs(relative_side='unknown'))['status'],'insufficient_evidence')
    def test_unknown_bird(self):self.assertEqual(result(obs(bird_label='unknown'))['status'],'insufficient_evidence')
    def test_unrecognized_bird(self):self.assertEqual(result(obs(bird_label='sparrow'))['status'],'unsupported')
    def test_latin_not_automatic_alias(self):self.assertEqual(result(obs(bird_label='cornix'))['status'],'unsupported')
    def test_missing_frame(self):o=obs();o.pop('reference_frame');self.assertEqual(result(o)['status'],'insufficient_evidence')
    def test_no_compass_conversion(self):r=result(obs(reference_frame='cardinal',observer_facing='S'));self.assertEqual(r['status'],'unsupported');self.assertIsNone(r['cardinal_conversion'])
    def test_facing_does_not_fill_frame(self):self.assertEqual(result(obs(reference_frame='unknown',observer_facing='S'))['status'],'insufficient_evidence')
    def test_located_flight_not_moving(self):self.assertEqual(result(obs(phenomenon='flight'))['status'],'not_applicable')
    def test_departing_not_moving_to(self):self.assertEqual(result(obs(phenomenon='flight',relation='moving_from_side'))['status'],'not_applicable')
    def test_unresolved_relation(self):self.assertEqual(result(obs(relation='unresolved'))['status'],'insufficient_evidence')
    def test_structured_side_conflict(self):r=result(obs(phenomenon='flight',relation='moving_to_side',side_reports=['left','right']));self.assertTrue(r['structured_side_conflict']);self.assertEqual(r['applicable_main_ids'],[])
    def test_conflict_declared_vs_report(self):self.assertTrue(result(obs(side_reports=['right']))['structured_side_conflict'])
    def test_report_does_not_fill_missing_side(self):self.assertEqual(result(obs(relative_side='unknown',side_reports=['left']))['status'],'insufficient_evidence')
    def test_raw_prose_not_interpreted(self):self.assertFalse(result(obs(description='It was right and left.'))['structured_side_conflict'])
    def test_uncertain_each_required_field(self):
        for field in a.DATA['required_fields']:
            r=result(obs(phenomenon='flight',relation='moving_to_side',uncertain_fields=[field]));self.assertEqual(r['favorable_main_source_ids'],[])
    def test_note_right_call_distinct(self):r=result(obs(relative_side='right'));self.assertEqual(r['matched_note_ids'],['note226-crow-right']);self.assertEqual(r['applicable_main_ids'],[]);self.assertEqual(r['status'],'conflicting_evidence')
    def test_exact_initial_call_locator(self):self.assertEqual(a.lookup('call-crow-left')['locator'],'I.7.12')
    def test_main_note_layers(self):self.assertEqual(a.lookup('classes-main')['text_layer'],'main_text_dialogue');self.assertEqual(a.lookup('classes-note133')['text_layer'],'translator_note')
    def test_speakers(self):self.assertEqual(a.lookup('call-crow-left')['speaker'],'Quintus');self.assertEqual(a.lookup('direction-criticism')['speaker'],'Marcus')
    def test_cock_criticism_no_match(self):r=result(obs(bird_label='cock'));self.assertEqual(r['status'],'unsupported');self.assertIn('Democritus',a.lookup('cock-criticism')['source_account'])
    def test_public_not_authorized(self):self.assertFalse(result(obs(setting='public ceremony',origin='reported_real'))['public_auspice_authorized'])
    def test_ordinary_hypothetical_allowed(self):self.assertEqual(result(obs(setting='ordinary private observation',origin='hypothetical'))['applicable_main_ids'],['call-crow-left'])
    def test_modern_species_user_only(self):r=result(obs(modern_species='Corvus corone, my identification'));self.assertIsNone(r['modern_species_inferred']);self.assertIn('Corvus',r['declared']['modern_species'])
    def test_sequence_raw(self):self.assertEqual(result(obs(sequence=[' eventA ',' eventB ']))['declared']['sequence'],[' eventA ',' eventB '])
    def test_compare_call_flight(self):
        r=a.read(q(observations=[obs(),obs(observation_id='obs2',phenomenon='flight',relation='moving_to_side')]));self.assertEqual(r['comparisons'][0]['phenomena'],['call','flight']);self.assertIsNone(r['comparisons'][0]['combined_omen'])
    def test_order(self):r=a.read(q(observations=[obs(observation_id='b'),obs(observation_id='a')]));self.assertEqual([x['observation_id'] for x in r['observations']],['b','a'])
    def test_duplicate_observation_id(self):self.reject(q(observations=[obs(),obs()]))
    def test_reference_order(self):r=a.read(ref(['cock-criticism','public-early']));self.assertEqual([x['id'] for x in r['references']],['cock-criticism','public-early'])
    def test_catalog(self):x={k:v for k,v in q(task='catalog').items() if k!='observations'};self.assertEqual(len(a.read(x)['references']),14)
    def test_unknown_reference(self):self.reject(ref(['unknown']))
    def test_context_always_visible(self):self.assertEqual(len(a.read(q())['context_references']),9)
    def test_latin_translation_limit(self):self.assertIn('without an explicit flight verb',a.read(q())['translation_notes']['qualification'])
    def test_no_weather_transfer(self):self.assertEqual(result(obs(bird_label='heron',description='storm'))['status'],'unsupported')
    def test_no_greek_transfer(self):self.reject(q(profile='homer-murray1924-greek-omens'))
    def test_no_prediction_task(self):self.reject(q(task='predict'))
    def test_raw_unicode(self):
        raw='  Café Café\r\n猫\t `````json ';x=a.read(q(obs(reflection=raw),question=raw));self.assertEqual(x['user_text']['question'],raw);self.assertEqual(x['observations'][0]['declared']['reflection'],raw)
    def test_question_does_not_select(self):self.assertEqual(a.read(q(question='raven right?'))['observations'][0]['applicable_main_ids'],['call-crow-left'])
    def test_invalid_schema_types(self):
        for v in (True,1.0,2):self.reject(q(schema_version=v));self.reject(q(catalog_version=v))
    def test_invalid_hash_profile(self):self.reject(q(catalog_sha256='0'*64));self.reject(q(profile='unknown'))
    def test_invalid_observation_types(self):
        for key in ('phenomenon','relative_side','relation','reference_frame','origin','observer_facing'):self.reject(q(obs(**{key:True})))
    def test_invalid_bird_text(self):
        for v in (True,'','\ud800','\x00'):self.reject(q(obs(bird_label=v)))
    def test_invalid_context_text(self):self.reject(q(obs(description=12)));self.reject(q(question='x'*10001))
    def test_invalid_uncertain_fields(self):self.reject(q(obs(uncertain_fields=['species'])));self.reject(q(obs(uncertain_fields=['bird_label','bird_label'])))
    def test_invalid_sequence(self):self.reject(q(obs(sequence=[12])));self.reject(q(obs(side_reports=['east'])))
    def test_unknown_fields(self):self.reject(q(bearing=90));self.reject(q(obs(azimuth=90)))
    def test_input_limits(self):self.reject(q(observations=[]));self.reject(q(observations=[obs()]*9))
    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'q.json')
            for text in ('{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}'):
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):a.load_input(p)
    def test_exact_replay(self):r=a.read(q(notes=' x '));self.assertEqual(a.read(r['replay']['request']),r)
    def test_markdown_replay(self):
        r=a.read(q(notes='`````json 猫'));m=re.search(r'(`{3,})json\n(.*?)\n\1',a.markdown(r).split('## Exact replay metadata')[1],re.S);self.assertEqual(a.read(json.loads(m[2])['request']),r)
    def test_deepcopy(self):x=q();old=copy.deepcopy(x);r=a.read(x);r['observations'][0]['declared']['bird_label']='raven';self.assertEqual(x,old)
    def test_registry(self):
        r=load_registry()
        try:a.read(q(),r);a.read(q(),r);self.assertEqual(r.db.execute("select count(*) from rules where id like 'augury.%'").fetchone()[0],14)
        finally:r.close()
    def asset_change(self,name,change):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'knowledge').mkdir()
            for stem in ('profile','catalog'):(root/f'knowledge/augury_{stem}_v1.json').write_bytes((a.ROOT/f'knowledge/augury_{stem}_v1.json').read_bytes())
            change(root/f'knowledge/augury_{name}_v1.json')
            with patch.object(a,'ROOT',root):self.reject(q())
    def test_missing_catalog(self):self.asset_change('catalog',lambda p:p.unlink())
    def test_changed_record(self):self.asset_change('catalog',lambda p:p.write_text('{}',encoding='utf-8'))
    def test_changed_profile(self):self.asset_change('profile',lambda p:p.write_text('{}',encoding='utf-8'))

if __name__=='__main__':unittest.main()
