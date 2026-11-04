import copy
import json
from pathlib import Path
import tempfile
import unittest
from future import scrying as s
from future.knowledge import Registry

ROOT=Path(__file__).resolve().parents[1]
BASE=dict(schema_version=1,profile=s.PROFILE,task='guided_journal',mode='manual')
REF=json.loads((ROOT/'tests/fixtures/scrying_procedure_reference.json').read_text(encoding='utf-8'))


class ScryingTests(unittest.TestCase):
    def test_independent_original_procedure_fixture(self):
        self.assertEqual([r['id'].split('.')[-1] for r in s.DATA['rules']],REF['source_rule_order'])
        for case in REF['cases']:
            rule=s.RULES['scrying.atkinson.'+case['rule']]
            self.assertIn(case['locator_contains'],rule['locator'])
            self.assertIn(case['statement_contains'],rule['statement'])

    def test_edition_provenance_and_source_isolation(self):
        source=s.DATA['source']
        self.assertIn('updated2024-10-23',source['edition'])
        self.assertIn(REF['edition']['displayed_isbn'],source['edition'])
        self.assertEqual(len(source['snapshot_sha256']),64)
        self.assertIn('not equated',s.read(BASE)['direct']['edition_boundary'])
        for profile in ('Thomas1905','Atkinson1908facsimile','Moody',None):
            with self.assertRaises(ValueError):s.read(BASE|dict(profile=profile))

    def test_eight_source_supported_surfaces(self):
        for surface in REF['surface_ids']:
            r=s.read(BASE|dict(session=dict(surface=surface)))
            self.assertEqual(r['session']['effective_surface'],surface)
            self.assertEqual(s.DATA['surfaces'][surface]['rule_ids'],('scrying.atkinson.surface',))
        self.assertEqual(len(REF['surface_ids']),8)
        for surface in ('camera','flame','blood',[],None):
            with self.assertRaises(ValueError):s.read(BASE|dict(session=dict(surface=surface)))

    def test_declared_environment_separate_from_recommendation(self):
        value=BASE|dict(session=dict(surface='glass',lighting='  light in FRONT\nnot behind ',background='white table'))
        r=s.read(value)
        self.assertEqual(r['session']['values'],value['session'])
        self.assertFalse(r['session']['environment_observed_by_engine'])
        self.assertIn('back toward',s.RULES['scrying.atkinson.lighting']['statement'])

    def test_unknown_unspecified_and_null_conditions(self):
        r=s.read(BASE)
        self.assertEqual(r['session']['effective_surface'],'unspecified')
        self.assertEqual(r['session']['lighting_state'],'unspecified')
        r=s.read(BASE|dict(session=dict(surface='unknown',lighting=None,background=None)))
        self.assertEqual(r['session']['lighting_state'],'unknown')
        self.assertEqual(r['session']['background_state'],'unknown')
        self.assertIsNone(r['session']['values']['lighting'])

    def test_guided_order_and_rule_locators(self):
        r=s.read(BASE)
        self.assertEqual([x['id'] for x in r['guidance']],REF['workflow_order'])
        self.assertEqual([x['order'] for x in r['guidance']],list(range(1,7)))
        for step in r['guidance']:
            self.assertFalse(step['performed_by_engine'])
            self.assertTrue(all(rule['source_id'] and rule['locator'] for rule in step['source_components']))
        self.assertEqual(r['guidance'][3]['coverage'],'editorial_journaling')

    def test_no_required_imagery_or_prolonged_stare(self):
        r=s.read(BASE|dict(session=dict(status='discontinued')))
        self.assertIn('discontinue',r['stop_policy'])
        self.assertIn('blink',r['guidance'][2]['text'])
        self.assertFalse(r['historical_beliefs']['expected_imagery_required'])
        self.assertEqual(r['session']['values']['status'],'discontinued')

    def test_optional_visualization_remains_imagined(self):
        value=BASE|dict(session=dict(practice='familiar_visualization',visualization_subject='my familiar chair'),
            journal=[dict(experience_type='imagined_imagery',description='A chair I deliberately pictured.')])
        r=s.read(value)
        self.assertIn('scrying.atkinson.visualize',r['guidance'][2]['rule_ids'])
        self.assertIn('imagined imagery',r['guidance'][2]['optional_visualization'])
        self.assertEqual(r['journal'][0]['experience_type'],'imagined_imagery')
        with self.assertRaises(ValueError):s.read(BASE|dict(session=dict(visualization_subject='chair')))

    def test_raw_description_association_and_reflection_preservation(self):
        raw='  Café Cafe\u0301\r\n\t"image" <tag> ```  '
        row=dict(experience_type='subjective_imagery',description=raw,associations=[raw,''],personal_reflection=raw)
        value=BASE|dict(journal=[row],personal_reflection=raw)
        r=s.read(value)
        self.assertEqual(r['journal'][0]['user_record'],row)
        self.assertEqual(r['journal'][0]['associations']['values'],[raw,''])
        self.assertEqual(r['personal_reflection'],raw)
        self.assertEqual(json.loads(json.dumps(r))['journal'][0]['user_record']['description'],raw)

    def test_five_experience_types_remain_user_attributed(self):
        rows=[dict(experience_type=k,description='same words') for k in s.TYPES]
        r=s.read(BASE|dict(journal=rows))
        self.assertEqual([x['experience_type'] for x in r['journal']],list(s.TYPES))
        self.assertTrue(all(x['attribution'].startswith('user_reported') for x in r['journal']))
        self.assertFalse(r['perception_detected'])

    def test_generated_prompt_never_accepted_as_observation(self):
        with self.assertRaises(ValueError):s.read(BASE|dict(journal=[dict(experience_type='generated_creative_prompt',description='orb')]))
        for extra in (dict(seed='x'),dict(prompts=['orb']),dict(mode='seeded')):
            with self.assertRaises(ValueError):s.read(BASE|extra)
        r=s.read(BASE);self.assertEqual(r['creative_prompts'],[])
        self.assertFalse(r['creative_prompt_system']['supported'])

    def test_missing_null_empty_and_unclassified_journals(self):
        for extra,state in (({},'missing'),(dict(journal=None),'null'),(dict(journal=[]),'empty')):
            r=s.read(BASE|extra)
            self.assertEqual(r['journal_state'],state);self.assertEqual(r['journal'],[])
        r=s.read(BASE|dict(journal=[{},dict(description=''),dict(description=None),dict(description='  ')]))
        self.assertEqual([x['description_state'] for x in r['journal']],['missing','blank','null','blank'])
        self.assertEqual(r['summary']['counts']['unclassified'],4)
        self.assertTrue(all(x['uncertainty']['classification_unresolved'] for x in r['journal']))

    def test_no_imagery_is_valid_and_no_symbolism_created(self):
        r=s.read(BASE|dict(journal=[dict(experience_type='no_imagery')]))
        self.assertEqual(r['summary']['counts']['no_imagery'],1)
        self.assertFalse(r['editorial_reflection']['symbol_dictionary_used'])
        self.assertEqual(len(r['editorial_reflection']['questions']),1)
        self.assertIsNone(r['confidence_score'])

    def test_uncertainty_and_structural_conflict_retained(self):
        r=s.read(BASE|dict(journal=[dict(experience_type='uncertain',uncertainty=False,description='not sure')]))
        u=r['journal'][0]['uncertainty']
        self.assertFalse(u['user_declared']);self.assertTrue(u['classification_unresolved'])
        self.assertIn('uncertain_type_with_uncertainty_false',u['conflicts'])
        self.assertFalse(u['physical_reality_verified'])

    def test_user_symbolism_never_source_or_universal(self):
        row=dict(experience_type='subjective_imagery',description='red circle',associations=['To me,this means a fresh start.'])
        r=s.read(BASE|dict(journal=[row]))
        self.assertEqual(r['journal'][0]['associations']['coverage'],'user_attributed')
        self.assertFalse(r['journal'][0]['associations']['universal_meaning'])
        self.assertFalse(r['editorial_reflection']['symbol_dictionary_used'])
        self.assertNotIn('fresh start',json.dumps(r['direct']))
        for extra in (dict(symbol_dictionary='aura'),dict(universal_meaning='anger'),dict(prediction=True)):
            with self.assertRaises(ValueError):s.read(BASE|extra)

    def test_input_order_and_explicit_sequences(self):
        rows=[dict(sequence=2,description='first'),{},dict(sequence=9,description='third')]
        r=s.read(BASE|dict(journal=rows))
        self.assertEqual([x['user_record'] for x in r['journal']],rows)
        for sequence in ([2,2],[3,1],[True,2],[0,2],[1000001]):
            with self.assertRaises(ValueError):s.read(BASE|dict(journal=[dict(sequence=n) for n in sequence]))

    def test_user_timestamps_not_current_clock(self):
        for timestamp in ('2024-02-29','2026-11-04T17:02:03+05:30','2026-11-04T11:00:00Z','2026-11-04T11:00:00',None):
            r=s.read(BASE|dict(session=dict(timestamp=timestamp),journal=[dict(timestamp=timestamp)]))
            self.assertEqual(r['session']['values']['timestamp'],timestamp)
            self.assertFalse(r['replay']['clock_used'])
        for timestamp in ('2025-02-29','2026-13-01','now','2026-11-04T25:00:00','2026-11-04T12:00:00+05:99',True):
            with self.assertRaises(ValueError):s.read(BASE|dict(session=dict(timestamp=timestamp)))

    def test_strict_schema_and_unknown_fields(self):
        for extra in (dict(schema_version=True),dict(task='clairvoyance'),dict(mode='camera'),dict(sensor=[])):
            with self.assertRaises(ValueError):s.read(BASE|extra)
        for value in (None,[],True):
            with self.assertRaises(ValueError):s.read(value)
        for session in (None,[],dict(camera=True),dict(practice='trance'),dict(status='verified')):
            with self.assertRaises(ValueError):s.read(BASE|dict(session=session))
        for row in (None,[],dict(unseen_entity='yes'),dict(experience_type=None),dict(uncertainty='yes')):
            with self.assertRaises(ValueError):s.read(BASE|dict(journal=[row]))

    def test_text_and_collection_bounds(self):
        for desc in ('\ud800','\0','x'*10001,True):
            with self.assertRaises(ValueError):s.read(BASE|dict(journal=[dict(description=desc)]))
        for rows in ({},True,[{}]*129):
            with self.assertRaises(ValueError):s.read(BASE|dict(journal=rows))
        for associations in (None,{},[True],['x']*33,['x'*2001]):
            with self.assertRaises(ValueError):s.read(BASE|dict(journal=[dict(associations=associations)]))
        self.assertEqual(len(s.read(BASE|dict(journal=[{}]*128))['journal']),128)

    def test_neutral_summary_without_claims_or_material(self):
        r=s.read(BASE|dict(session=dict(intention='Will I win?')))
        self.assertIn('No experience was recorded',r['summary']['text'])
        self.assertEqual(sum(r['summary']['counts'].values()),0)
        self.assertFalse(r['factual_prediction']);self.assertIsNone(r['confidence_score'])
        self.assertIn('no hidden meaning',r['summary']['text'])

    def test_json_markdown_replay_and_fence_preservation(self):
        value=BASE|dict(journal=[dict(description='literal\n```\ntext\r\n  ',associations=['own association'])])
        r=s.read(value);md=s.markdown(r)
        self.assertIn('````text',md)
        self.assertEqual(json.loads(json.dumps(r)),r)
        replay=json.loads(md.split('## Exact replay metadata')[1].split('```json\n')[1].split('\n```')[0])
        self.assertEqual(s.read(replay['request']),r)
        self.assertEqual(replay['request'],value)

    def test_strict_json_duplicate_keys_nonfinite_and_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp,'input.json')
            for text in ('{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}'):
                path.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):s.load_input(path)
            path.write_text(json.dumps(BASE),encoding='utf-8-sig')
            self.assertEqual(s.load_input(path),BASE)

    def test_immutable_catalog_request_and_portable_hash(self):
        with self.assertRaises(TypeError):s.DATA['profile']='other'
        value=BASE|dict(journal=[dict(description='my words')]);saved=copy.deepcopy(value)
        r=s.read(value);self.assertEqual(value,saved)
        r['sources'][0]['url']='mutated';r['journal'][0]['user_record']['description']='mutated'
        self.assertNotEqual(s.read(value)['sources'],r['sources'])
        raw=(ROOT/'knowledge/scrying_profile_v1.json').read_text(encoding='utf-8')
        self.assertEqual(s.PROFILE_HASH,s.digest(json.loads(raw.replace('\n','\r\n'))))

    def test_registry_rules_idempotence_and_rejections(self):
        registry=Registry()
        try:
            s.read(BASE,registry);s.read(BASE,registry)
            self.assertEqual(registry.db.execute('select count(*) from rules').fetchone()[0],8)
            self.assertEqual(registry.db.execute('select count(*) from sources').fetchone()[0],1)
        finally:registry.close()
        self.assertIsNone(json.loads(s.rejection('Invalid input','json'))['session_report'])
        self.assertNotIn('<script>',s.rejection('<script>','markdown'))


if __name__=='__main__':unittest.main()
