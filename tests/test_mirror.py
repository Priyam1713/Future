import copy
import json
from pathlib import Path
import tempfile
import unittest
from future import mirror as m,scrying as s
from future.knowledge import Registry

ROOT=Path(__file__).resolve().parents[1]
BASE=dict(schema_version=1,profile=m.PROFILE,task='guided_mirror_journal',mode='manual')
REF=json.loads((ROOT/'tests/fixtures/mirror_procedure_reference.json').read_text(encoding='utf-8'))


class MirrorTests(unittest.TestCase):
    def test_independent_original_procedure_cases(self):
        self.assertEqual([r['id'].split('.')[-1] for r in m.DATA['rules']],REF['source_order'])
        for case in REF['cases']:
            rule=m.RULES['mirror.moody1992.'+case['rule']]
            self.assertIn('Printedp'+str(case['page']),rule['locator'])
            self.assertIn(case['contains'],rule['statement'])

    def test_verified_setup_values_no_invented_angle(self):
        actual=m.read(BASE)['historical_setup']
        for key,value in REF['setup'].items():self.assertEqual(actual[key],value)
        self.assertEqual(actual['lamp_watts'],25)
        self.assertIsNone(actual['mirror_angle_degrees'])
        self.assertFalse(m.read(BASE)['session']['source_setup_required'])

    def test_exact_edition_rights_and_source_scope(self):
        source=m.DATA['source']
        self.assertIn('Winter1992',source['edition'])
        self.assertIn('Human Sciences Press',source['rights_note'])
        self.assertEqual(source['ingestion'],'facts_only')
        self.assertEqual(len(source['snapshot_sha256']),64)
        self.assertIn('not full1993',m.read(BASE)['direct']['edition_boundary'])

    def test_source_isolation_from_atkinson_dee_and_book(self):
        for profile in (s.PROFILE,'Dee1659','Reunions1993','obsidian',None):
            with self.assertRaises(ValueError):m.read(BASE|dict(profile=profile))
        with self.assertRaises(ValueError):s.read(dict(schema_version=1,profile=m.PROFILE,task='guided_journal',mode='manual'))
        self.assertTrue(all(r['source_id']==m.DATA['source']['id'] for r in m.DATA['rules']))

    def test_supported_mirror_configuration(self):
        for surface in ('ordinary_mirror','unknown','unspecified'):
            self.assertEqual(m.read(BASE|dict(session=dict(surface=surface)))['session']['effective_surface'],surface)
        for surface in ('obsidian','black_mirror','crystal','camera',None,[]):
            with self.assertRaises(ValueError):m.read(BASE|dict(session=dict(surface=surface)))
        with self.assertRaises(ValueError):m.read(BASE|dict(session=dict(mirror_angle_degrees=45)))

    def test_view_and_actual_environment_not_inferred(self):
        for view,relation in [('self_reflection_excluded','declared match'),('self_reflection_visible','declared difference'),('unknown','unknown'),('unspecified','unknown')]:
            value=BASE|dict(session=dict(view=view,lighting='Bright room\nuser words',background=None))
            r=m.read(value)
            self.assertEqual(r['session']['values'],value['session'])
            self.assertEqual(r['session']['view_relation_to_source'],relation)
            self.assertFalse(r['session']['environment_observed_by_engine'])

    def test_source_specific_workflow_order_and_locators(self):
        r=m.read(BASE)
        self.assertEqual([x['id'] for x in r['guidance']],REF['workflow_order'])
        self.assertEqual([x['order'] for x in r['guidance']],list(range(1,7)))
        for step in r['guidance']:
            self.assertTrue(all(x['locator'] and x['source_id'] for x in step['source_components']))
            self.assertFalse(step['performed_by_engine'])
        self.assertEqual(r['guidance'][4]['coverage'],'editorial_journal_adaptation')

    def test_subset_omissions_and_no_required_encounter(self):
        r=m.read(BASE)
        self.assertIn('not complete',r['adaptation'])
        self.assertIn('no pressure',r['guidance'][1]['text'])
        self.assertIn('blink normally',r['guidance'][2]['text'])
        self.assertIn('no historical duration',r['guidance'][3]['text'])
        self.assertFalse(r['replay']['full_source_protocol_reproduced'])

    def test_skip_stages_and_discontinue(self):
        value=BASE|dict(session=dict(status='discontinued'),stages=[dict(stage_id='gaze',status='skipped')])
        r=m.read(value)
        self.assertEqual(r['guidance'][2]['user_stage_status'],'skipped')
        self.assertEqual(r['guidance'][0]['user_stage_status'],'not_recorded')
        self.assertEqual(r['session']['values']['status'],'discontinued')
        self.assertEqual(r['journal'],[])

    def test_conflicting_stage_configuration_rejected(self):
        for stages in ([dict(stage_id='gaze',status='skipped'),dict(stage_id='gaze',status='completed')],
            [dict(stage_id='gaze',status='completed')],[dict(stage_id='other',status='skipped')],
            [dict(stage_id='gaze',status='verified')],None):
            with self.assertRaises(ValueError):m.read(BASE|dict(stages=stages))
        r=m.read(BASE|dict(session=dict(status='completed'),stages=[dict(stage_id='gaze',status='completed')]))
        self.assertEqual(r['guidance'][2]['user_stage_status'],'completed')

    def test_raw_unicode_whitespace_and_omissions(self):
        raw='  Café Cafe\u0301\r\n\ttext ``` <tag>  '
        row=dict(description=raw,associations=[raw,''],personal_reflection=raw)
        r=m.read(BASE|dict(journal=[{},row],personal_reflection=raw))
        self.assertEqual(r['journal'][0]['user_record'],{})
        self.assertEqual(r['journal'][1]['user_record'],row)
        self.assertEqual(r['personal_reflection'],raw)
        self.assertEqual(json.loads(json.dumps(r))['journal'][1]['user_record'],row)

    def test_experience_categories_stay_user_attributed(self):
        rows=[dict(experience_type=k,description='a figure') for k in m.TYPES]
        r=m.read(BASE|dict(journal=rows))
        self.assertEqual([x['experience_type'] for x in r['journal']],list(m.TYPES))
        self.assertTrue(all(x['attribution']=='user_reported;not engine-observed' for x in r['journal']))
        self.assertFalse(r['perception_detected'])

    def test_subjective_memory_or_presence_not_identified(self):
        row=dict(experience_type='subjective_imagery',description='I felt my mother was present.',associations=['My own memory.'])
        r=m.read(BASE|dict(journal=[row]))
        self.assertEqual(r['journal'][0]['user_record'],row)
        self.assertFalse(r['contact_verified']);self.assertFalse(r['therapeutic_efficacy_claimed'])
        self.assertFalse(r['factual_prediction']);self.assertIsNone(r['confidence_score'])
        self.assertNotIn('mother',r['summary']['text'])

    def test_missing_null_empty_and_no_imagery(self):
        for extra,state in (({},'missing'),(dict(journal=None),'null'),(dict(journal=[]),'empty')):
            r=m.read(BASE|extra);self.assertEqual(r['journal_state'],state);self.assertEqual(r['journal'],[])
        r=m.read(BASE|dict(journal=[dict(experience_type='no_imagery')]))
        self.assertEqual(r['summary']['counts']['no_imagery'],1)
        self.assertEqual(len(r['editorial_reflection']['questions']),1)
        self.assertFalse(r['contact_verified'])

    def test_uncertain_or_unclassified_records(self):
        r=m.read(BASE|dict(journal=[{},dict(description=''),dict(experience_type='uncertain',uncertainty=False)]))
        self.assertEqual(r['journal'][0]['description_state'],'missing')
        self.assertEqual(r['journal'][1]['description_state'],'blank')
        self.assertEqual(r['summary']['counts']['unclassified'],2)
        self.assertIn('uncertain_type_with_uncertainty_false',r['journal'][2]['uncertainty']['conflicts'])

    def test_user_meaning_and_no_dictionary(self):
        r=m.read(BASE|dict(journal=[dict(description='circle',associations=['To me: a fresh start.'])]))
        self.assertEqual(r['journal'][0]['associations']['coverage'],'user_attributed')
        self.assertFalse(r['journal'][0]['associations']['universal_meaning'])
        self.assertFalse(r['editorial_reflection']['symbol_dictionary_used'])
        with self.assertRaises(ValueError):m.read(BASE|dict(symbol_dictionary='universal'))

    def test_narrow_pure_reuse_and_scrying_golden_compatibility(self):
        self.assertIs(m._timestamp,s._timestamp);self.assertIs(m._raw,s._raw)
        self.assertIs(m.load_input,s.load_input)
        for name in ('guided','dark','associations','no-imagery','uncertain','multiple','visualization','empty'):
            value=json.loads((ROOT/f'data/scrying-{name}-input.json').read_text(encoding='utf-8'))
            expected=json.loads((ROOT/f'data/scrying-{name}.json').read_text(encoding='utf-8'))
            self.assertEqual(s.read(value),expected)

    def test_sequence_and_timestamp_declarations(self):
        value=BASE|dict(session=dict(timestamp='2026-11-04T17:00:00+05:30'),journal=[dict(sequence=2,timestamp='2024-02-29'),{},dict(sequence=7)])
        r=m.read(value)
        self.assertEqual([x['user_record'] for x in r['journal']],value['journal'])
        self.assertFalse(r['replay']['clock_used'])
        for extra in (dict(session=dict(timestamp='now')),dict(journal=[dict(sequence=True)]),dict(journal=[dict(sequence=2),dict(sequence=1)])):
            with self.assertRaises(ValueError):m.read(BASE|extra)

    def test_strict_root_and_session_schema(self):
        for extra in (dict(schema_version=True),dict(mode='seeded'),dict(task='contact'),dict(seed='vision'),dict(camera=True)):
            with self.assertRaises(ValueError):m.read(BASE|extra)
        for session in (None,[],dict(surface=[]),dict(view='tilt45'),dict(status='certified')):
            with self.assertRaises(ValueError):m.read(BASE|dict(session=session))

    def test_journal_validation_and_bounds(self):
        for row in (None,dict(experience_type='verified_spirit'),dict(description='\ud800'),dict(description='\0'),dict(uncertainty='yes'),dict(associations=[True]),dict(description='x'*10001)):
            with self.assertRaises(ValueError):m.read(BASE|dict(journal=[row]))
        with self.assertRaises(ValueError):m.read(BASE|dict(journal=[{}]*129))
        self.assertEqual(len(m.read(BASE|dict(journal=[{}]*128))['journal']),128)

    def test_json_markdown_replay_and_fences(self):
        value=BASE|dict(journal=[dict(description='literal\n```\ntext\r\n  ')])
        r=m.read(value);md=m.markdown(r)
        self.assertIn('````text',md)
        replay=json.loads(md.split('## Exact replay metadata')[1].split('```json\n')[1].split('\n```')[0])
        self.assertEqual(replay['request'],value);self.assertEqual(m.read(replay['request']),r)
        self.assertEqual(json.loads(json.dumps(r)),r)

    def test_portable_hash_and_immutable_catalog_request(self):
        raw=(ROOT/'knowledge/mirror_profile_v1.json').read_text(encoding='utf-8')
        self.assertEqual(m.PROFILE_HASH,m.digest(json.loads(raw.replace('\n','\r\n'))))
        with self.assertRaises(TypeError):m.DATA['profile']='other'
        value=BASE|dict(journal=[dict(description='mine')]);saved=copy.deepcopy(value);r=m.read(value)
        self.assertEqual(value,saved);r['journal'][0]['user_record']['description']='changed'
        self.assertEqual(m.read(value)['journal'][0]['user_record']['description'],'mine')

    def test_strict_json_bom_and_rejections(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp,'input.json')
            for text in ('{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}'):
                path.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):m.load_input(path)
            path.write_text(json.dumps(BASE),encoding='utf-8-sig');self.assertEqual(m.load_input(path),BASE)
        self.assertIsNone(json.loads(m.rejection('Invalid','json'))['session_report'])

    def test_registry_source_rules_idempotent(self):
        r=Registry()
        try:
            m.read(BASE,r);m.read(BASE,r)
            self.assertEqual(r.db.execute('select count(*) from rules').fetchone()[0],9)
            self.assertEqual(r.db.execute('select count(*) from sources').fetchone()[0],1)
        finally:r.close()


if __name__=='__main__':unittest.main()
