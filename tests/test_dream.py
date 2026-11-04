import copy
import json
from pathlib import Path
import tempfile
import unittest
from future import dream as d,mirror as m,scrying as s
from future.knowledge import Registry

ROOT=Path(__file__).resolve().parents[1]
BASE=dict(schema_version=1,profile=d.PROFILE,task='historical_reflection',mode='manual')
REF=json.loads((ROOT/'tests/fixtures/dream_source_reference.json').read_text(encoding='utf-8'))


class DreamTests(unittest.TestCase):
    def test_independent_taxonomy_terms_and_parents(self):
        self.assertEqual(list(d.CATEGORIES),REF['category_ids'])
        self.assertEqual([x['parent'] for x in d.CATEGORIES.values()],REF['parents'])
        self.assertEqual([x['greek'] for x in d.CATEGORIES.values()],REF['greek_terms'])
        self.assertIn('Present-state',d.CATEGORIES['enypnion']['definition'])
        self.assertIn('future-signifying',d.CATEGORIES['oneiros']['definition'])

    def test_nine_independent_motif_sections(self):
        self.assertEqual(len(d.MOTIFS),9)
        for key,section in REF['motif_sections'].items():
            self.assertEqual(d.MOTIFS[key]['provenance']['locator'],'Oneirocritica '+section)
            self.assertFalse(d.MOTIFS[key]['forecast'])

    def test_translation_and_rights_attribution(self):
        for key,motif in d.MOTIFS.items():
            expected='Naphtali Lewis1976' if REF['motif_sections'][key]=='1.1' else 'Robert J.White1975'
            self.assertEqual(motif['provenance']['translator'],expected)
        self.assertEqual(d.DATA['source']['ingestion'],'facts_only')
        self.assertIn('no translated passage',d.DATA['rights'])
        self.assertIn('Pack',d.DATA['greek_source']['edition'])

    def test_independent_contextual_cases(self):
        for case in REF['cases']:
            actual=d.lookup(case['motif'],case['context'])
            self.assertEqual(actual['status'],case['status'])
            self.assertEqual([x['id'] for x in actual['selected_cases']],case['selected'])

    def test_boolean_context_true_false_missing(self):
        for motif,key in [('eating','hungry'),('drinking','thirsty'),('feared_object','current_fear'),('desired_person','current_desire')]:
            self.assertEqual(d.lookup(motif,{key:True})['status'],'conditional_reference')
            self.assertEqual(d.lookup(motif,{key:False})['status'],'conditions_not_met')
            self.assertIn(key,d.lookup(motif,{})['missing_context'])
            self.assertEqual(d.lookup(motif,{key:None})['status'],'missing_context')

    def test_contextual_nose_accounts_not_universal(self):
        expected={'perfume_trade':'trade','civic_standing':'reputation','illness':'body'}
        for circumstance,case in expected.items():
            actual=d.lookup('lost_nose',dict(circumstances=[circumstance]))
            self.assertEqual([x['id'] for x in actual['selected_cases']],[case])
            self.assertFalse(actual['forecast'])
        self.assertEqual(d.lookup('lost_nose',{})['status'],'missing_context')

    def test_conflicting_staff_and_nose_references_retained(self):
        for motif,context in [('broken_staff',dict(staff_cases=['initial_account','repeat_during_paralysis'])),('lost_nose',dict(circumstances=['perfume_trade','illness']))]:
            result=d.read(BASE|dict(lookups=[motif],context=context))
            self.assertEqual(result['motif_references'][0]['status'],'conflicting_references')
            self.assertEqual(len(result['motif_references'][0]['selected_cases']),2)
            self.assertFalse(result['factual_prediction']);self.assertFalse(result['diagnosis'])

    def test_serpent_polysemy_never_ranks_a_meaning(self):
        result=d.lookup('serpent',{})
        self.assertEqual(result['status'],'polysemous_reference')
        self.assertEqual([c['id'] for c in result['selected_cases']],['kingship','time','wealth','sacred'])
        self.assertNotIn('best',result);self.assertFalse(result['forecast'])

    def test_competing_myth_versions_and_blank_context(self):
        self.assertEqual(d.lookup('myth_variants',dict(myth_versions=['a','b']))['status'],'conditional_reference')
        for versions in ([],['a'],['',' ']):
            self.assertEqual(d.lookup('myth_variants',dict(myth_versions=versions))['status'],'missing_context')

    def test_taxonomy_conditions_and_parent_structure(self):
        r=d.read(BASE|dict(lookups=['eating'],context=dict(hungry=True)))
        cats={x['category']['id']:x for x in r['historical_taxonomy']['categories']}
        self.assertEqual(cats['enypnion']['status'],'conditional_historical_comparison')
        r=d.read(BASE|dict(taxonomy_claims=['theorematic']))
        cats={x['category']['id']:x for x in r['historical_taxonomy']['categories']}
        self.assertEqual(cats['oneiros']['status'],'parent_of_selected_branch')
        self.assertTrue(cats['theorematic']['missing_context'])
        self.assertFalse(cats['oneiros']['predictive_validity_verified'])

    def test_conflicting_category_lenses_reported_not_repaired(self):
        r=d.read(BASE|dict(taxonomy_claims=['enypnion','theorematic','allegorical']))
        self.assertEqual(len(r['historical_taxonomy']['conflicts']),2)
        self.assertEqual(sum(x['user_claimed'] for x in r['historical_taxonomy']['categories']),3)
        self.assertIsNone(r['historical_taxonomy']['certainty'])

    def test_shipwreck_correspondence_is_user_report_not_prediction(self):
        r=d.read(BASE|dict(lookups=['shipwreck'],context=dict(at_sea=True,exact_correspondence_reported=True)))
        cats={x['category']['id']:x for x in r['historical_taxonomy']['categories']}
        self.assertEqual(cats['theorematic']['status'],'conditional_historical_comparison')
        self.assertFalse(cats['theorematic']['predictive_validity_verified'])
        self.assertFalse(r['factual_prediction'])

    def test_unknown_source_case_no_fallback(self):
        r=d.read(BASE|dict(lookups=['flying_universal']))
        self.assertEqual(r['motif_references'][0]['status'],'unsupported')
        self.assertEqual(r['motif_references'][0]['selected_cases'],[])

    def test_tradition_and_profile_isolation(self):
        for profile in ('Freud1913','Jung','Faraday',m.PROFILE,s.PROFILE,None):
            with self.assertRaises(ValueError):d.read(BASE|dict(profile=profile))
        self.assertTrue(all(x['provenance']['source_id']==d.DATA['source']['id'] for x in d.MOTIFS.values()))

    def test_verbatim_narrative_associations_and_entities(self):
        raw='  Café Cafe\u0301\r\n\t🐍 ``` <tag>  '
        value=BASE|dict(narrative=raw,associations=[raw,''],people=['my own label'],objects=['object'],places=['place'],events=['event'],feelings=['my feeling'],personal_reflection=raw)
        r=d.read(value);self.assertEqual(r['journal']['record'],{k:v for k,v in value.items() if k not in BASE})
        self.assertEqual(json.loads(json.dumps(r))['journal']['record']['narrative'],raw)

    def test_scene_sequences_timestamps_and_raw_records(self):
        scenes=[dict(sequence=2,description=' first ',timestamp='2024-02-29',people=['A']),{},dict(sequence=9,description='next',uncertainty=True)]
        value=BASE|dict(timestamp='2026-11-04T18:00:00+05:30',scenes=scenes)
        r=d.read(value);self.assertEqual(r['journal']['record']['scenes'],scenes)
        self.assertFalse(r['replay']['clock_used'])
        for rows in ([dict(sequence=True)],[dict(sequence=2),dict(sequence=1)],[dict(timestamp='now')]):
            with self.assertRaises(ValueError):d.read(BASE|dict(scenes=rows))

    def test_empty_fragmented_uncertain_and_no_recall(self):
        for extra,state in (({},'missing'),(dict(narrative=None),'null'),(dict(narrative='  '),'blank')):
            r=d.read(BASE|extra);self.assertEqual(r['journal']['narrative_state'],state)
            self.assertEqual(r['motif_references'],[])
        for recall in ('fragmented','uncertain','no_recall'):
            self.assertEqual(d.read(BASE|dict(recall=recall))['journal']['record']['recall'],recall)

    def test_personal_context_optional_and_never_inferred(self):
        r=d.read(BASE|dict(narrative='I was hungry and saw a serpent.'))
        self.assertNotIn('context',r['journal']['record'])
        self.assertEqual(r['motif_references'],[])
        for field in ('age','gender','health','occupation'):
            self.assertNotIn(field,r['journal']['record'])
        self.assertEqual(d.read(BASE|dict(context=dict(notes='only my voluntary words')))['journal']['record']['context']['notes'],'only my voluntary words')

    def test_manual_tag_cannot_trigger_reference(self):
        r=d.read(BASE|dict(narrative='not a serpent',annotations=[dict(motif_id='serpent')]))
        self.assertEqual(r['motif_references'],[])
        self.assertFalse(r['annotations'][0]['automatic_match'])
        self.assertFalse(r['annotations'][0]['historical_lookup_triggered'])
        self.assertFalse(r['replay']['automatic_matching'])

    def test_manual_unicode_spans_preserve_original_offsets(self):
        text=' A🐍 Café Cafe\u0301 '
        rows=[dict(motif_id='serpent',start=2,end=3),dict(motif_id='eating',start=4,end=8),dict(motif_id='drinking',start=9,end=14)]
        r=d.read(BASE|dict(narrative=text,annotations=rows))
        self.assertEqual([x['selected_text'] for x in r['annotations']],['🐍','Café','Cafe\u0301'])
        r=d.read(BASE|dict(scenes=[dict(description=text)],annotations=[dict(motif_id='serpent',target='scene',scene_index=1,start=2,end=3)]))
        self.assertEqual(r['annotations'][0]['selected_text'],'🐍')

    def test_overlaps_decisions_and_duplicate_conflicts(self):
        rows=[dict(motif_id='serpent',start=0,end=3,decision='exclude'),dict(motif_id='eating',start=1,end=4)]
        r=d.read(BASE|dict(narrative='abcd',annotations=rows))
        self.assertEqual(len(r['annotations']),2);self.assertEqual(r['annotations'][0]['decision'],'exclude')
        with self.assertRaises(ValueError):d.read(BASE|dict(narrative='abcd',annotations=[rows[0],rows[0]|dict(decision='include')]))
        for row in (dict(motif_id='serpent',start=True,end=2),dict(motif_id='serpent',start=0),dict(motif_id='serpent',start=0,end=99),dict(motif_id='serpent',target='scene',scene_index=1)):
            with self.assertRaises(ValueError):d.read(BASE|dict(narrative='abc',annotations=[row]))

    def test_user_preferences_and_historical_opt_out(self):
        r=d.read(BASE|dict(preferences=dict(historical_references=False,editorial_questions=False)))
        self.assertIsNone(r['historical_taxonomy']);self.assertEqual(r['editorial_reflection']['questions'],[])
        with self.assertRaises(ValueError):d.read(BASE|dict(lookups=['serpent'],preferences=dict(historical_references=False)))

    def test_words_cannot_alter_declared_case_evaluation(self):
        a=BASE|dict(narrative='Eating food.',lookups=['eating'],context=dict(hungry=True))
        b=a|dict(narrative='No food;this is a metaphor or translated phrase.')
        self.assertEqual(d.read(a)['motif_references'],d.read(b)['motif_references'])
        self.assertFalse(d.read(a)['diagnosis']);self.assertFalse(d.read(a)['hidden_memory_inferred'])
        self.assertIsNone(d.read(a)['confidence_score'])

    def test_strict_schema_context_and_collection_bounds(self):
        for extra in (dict(schema_version=True),dict(mode='seeded'),dict(task='diagnose'),dict(auto_tagging=True),dict(seed='x')):
            with self.assertRaises(ValueError):d.read(BASE|extra)
        for context in (None,dict(hungry='yes'),dict(circumstances=['unknown']),dict(staff_cases=['initial_account']*2),dict(myth_versions=['same']*2)):
            with self.assertRaises(ValueError):d.read(BASE|dict(context=context))
        for extra in (dict(narrative='\ud800'),dict(narrative='x'*20001),dict(scenes=[{}]*65),dict(people=[True]),dict(lookups=['eating']*2),dict(taxonomy_claims=['other'])):
            with self.assertRaises(ValueError):d.read(BASE|extra)

    def test_json_markdown_replay_and_escape(self):
        value=BASE|dict(narrative='raw\n```\ntext',lookups=['<script>'])
        r=d.read(value);md=d.markdown(r)
        self.assertIn('````text',md);self.assertIn('&lt;script&gt;',md)
        replay=json.loads(md.split('## Exact replay metadata')[1].split('```json\n')[1].split('\n```')[0])
        self.assertEqual(d.read(replay['request']),r);self.assertEqual(json.loads(json.dumps(r)),r)

    def test_strict_json_and_portable_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp,'input.json')
            for text in ('{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}'):
                path.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):d.load_input(path)
            path.write_text(json.dumps(BASE),encoding='utf-8-sig');self.assertEqual(d.load_input(path),BASE)
        raw=(ROOT/'knowledge/dream_profile_v1.json').read_text(encoding='utf-8')
        self.assertEqual(d.PROFILE_HASH,d.digest(json.loads(raw.replace('\n','\r\n'))))

    def test_immutable_catalog_request_and_registry(self):
        with self.assertRaises(TypeError):d.DATA['profile']='other'
        value=BASE|dict(narrative='raw');saved=copy.deepcopy(value);r=d.read(value)
        self.assertEqual(value,saved);r['journal']['record']['narrative']='changed'
        self.assertEqual(d.read(value)['journal']['record']['narrative'],'raw')
        registry=Registry()
        try:
            d.read(BASE,registry);d.read(BASE,registry)
            self.assertEqual(registry.db.execute('select count(*) from rules').fetchone()[0],15)
            self.assertEqual(registry.db.execute('select count(*) from sources').fetchone()[0],2)
        finally:registry.close()

    def test_pure_reuse_and_previous_saved_reports(self):
        self.assertIs(d._timestamp,s._timestamp);self.assertIs(d.load_input,s.load_input)
        for engine,prefix,names in [(s,'scrying',('guided','multiple','empty')),(m,'mirror',('guided','multiple','skipped'))]:
            for name in names:
                value=json.loads((ROOT/f'data/{prefix}-{name}-input.json').read_text(encoding='utf-8'))
                expected=json.loads((ROOT/f'data/{prefix}-{name}.json').read_text(encoding='utf-8'))
                self.assertEqual(engine.read(value),expected)


if __name__=='__main__':unittest.main()
