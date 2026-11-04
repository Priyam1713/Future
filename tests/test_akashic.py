import copy
import json
from pathlib import Path
import re
import tempfile
import unittest
from future import akashic as a
from future.__main__ import load_registry

REF=json.loads(Path('tests/fixtures/akashic_reference.json').read_text(encoding='utf-8'))


def base(**kwargs):
    return dict(schema_version=1,profile=a.PROFILE,task='reference_reflection',mode='manual')|kwargs


class AkashicTests(unittest.TestCase):
    def test_01_independent_concept_locations(self):
        for key,row in REF['source_locations'].items():
            p=a.lookup(key)['reference']['provenance']
            self.assertEqual(p['locator'],row['locator'])
            self.assertEqual(p['source_id'],'akashic-howe-public-'+row['source_key']+'-facts-v2')

    def test_02_independent_definitions(self):
        self.assertEqual({k:v['description'] for k,v in a.CONCEPTS.items()},REF['definitions'])

    def test_03_procedure_structure(self):
        p=a.read(base())['guidance']['procedure']
        self.assertEqual(p['opening']['silent_stanza_repetitions'],2)
        self.assertEqual(p['closing']['declaration_repetitions'],3)
        self.assertFalse(p['prayer_reproduced'])
        self.assertEqual(p['url'],'https://lindahowe.com/ppp/')

    def test_04_purpose_known_answers(self):
        for row in REF['purposes']:
            r=a.read(base(question=dict(text='Unchanged?',purpose=row['purpose'])))
            self.assertEqual(r['question']['status'],row['status'])
            self.assertEqual(r['guidance']['purpose_reference_ids'],row['reference_ids'])
            self.assertIsNone(r['question']['answer'])

    def test_05_explicit_form_guidance(self):
        for form,expected in REF['question_forms'].items():
            r=a.read(base(question=dict(text='A phrase',form=form)))
            self.assertEqual(r['question']['form_guidance'],expected)

    def test_06_no_text_intent_inference(self):
        r=a.read(base(question=dict(text='Will I die tomorrow? What illness do I have?')))
        self.assertEqual(r['question']['effective_purpose'],'unspecified')
        self.assertEqual(r['concept_references'],[])
        self.assertFalse(r['question']['intent_inferred'])

    def test_07_source_concepts_really_return_content(self):
        r=a.read(base(concept_ids=['closing']))
        self.assertIn('three',r['concept_references'][0]['reference']['description'])
        self.assertEqual(r['concept_references'][0]['selection_reasons'],['explicit_concept_selection'])

    def test_08_unknown_concepts_no_fallback(self):
        for key in REF['unsupported_concepts']:
            r=a.lookup(key);self.assertEqual(r['status'],'unsupported_concept')
            self.assertIsNone(r['reference']);self.assertFalse(r['fallback_used'])

    def test_09_explicit_reframe(self):
        q=base(question=dict(text=REF['raw']['question'],purpose='factual_prediction'),reframe='open_reflection')
        r=a.read(q);self.assertEqual(r['question']['status'],'unsupported_request')
        self.assertEqual(r['question']['user_record']['text'],REF['raw']['question'])
        self.assertFalse(r['editorial_reframe']['original_question_replaced'])
        self.assertFalse(r['editorial_reframe']['source_quote'])

    def test_10_reframe_is_optional(self):
        self.assertIsNone(a.read(base())['editorial_reframe'])
        self.assertIsNone(a.read(base(reframe='none'))['editorial_reframe'])
        self.assertIn('source claim',a.read(base(reframe='source_research'))['editorial_reframe']['text'])

    def test_11_prediction_and_clinical_unsupported(self):
        for purpose in ('factual_prediction','medical_clinical'):
            r=a.read(base(question=dict(purpose=purpose)))
            self.assertEqual(r['question']['status'],'unsupported_request')
            self.assertIsNone(r['question']['answer'])

    def test_12_profile_isolation(self):
        for profile in REF['unsupported_profiles']:
            with self.assertRaises(ValueError):a.read(base(profile=profile))
        r=a.read(base(comparisons=REF['unsupported_profiles']))
        self.assertTrue(all(x['status']=='unsupported_comparison' and x['reference'] is None for x in r['comparisons']))

    def test_13_empty_and_null_content(self):
        for q in (base(),base(question={}),base(question=dict(text=None)),base(question=dict(text=''))):
            r=a.read(q);self.assertEqual(r['question']['status'],'purpose_unspecified')
            self.assertTrue(r['unknowns']['application_observations'])

    def test_14_raw_unicode_and_uncertainty(self):
        q=base(question=dict(text=REF['raw']['question']),notes=[dict(id='n1',text=REF['raw']['note'],kind='imagined_scene',uncertainty=True)],unknowns=REF['raw']['unknowns'])
        r=a.read(q);self.assertEqual(r['notes'][0]['user_record'],q['notes'][0])
        self.assertEqual(r['question']['user_record'],q['question'])
        self.assertEqual(r['unknowns']['user_declared'],REF['raw']['unknowns'])
        self.assertFalse(r['notes'][0]['historical_record_retrieved'])

    def test_15_valid_pre_engine_stage_sequences(self):
        for ids in REF['stage_sequences']['valid']:
            q=base(session=dict(state='in_progress',stages=[dict(id=k,status='skipped') for k in ids]))
            self.assertEqual([s['user_declaration']['id'] for s in a.read(q)['session']['stage_reports']],ids)

    def test_16_invalid_stage_sequences(self):
        for ids in REF['stage_sequences']['invalid']:
            with self.assertRaises(ValueError):a.read(base(session=dict(stages=[dict(id=k) for k in ids])))

    def test_17_completion_and_discontinuation(self):
        q=base(session=dict(state='completed',stages=[dict(id='finish',status='skipped')]))
        self.assertEqual(a.read(q)['session']['effective_state'],'completed')
        self.assertEqual(a.read(base(session=dict(state='discontinued')))['session']['effective_state'],'discontinued')
        with self.assertRaises(ValueError):a.read(base(session=dict(state='completed')))
        with self.assertRaises(ValueError):a.read(base(session=dict(stages=[dict(id='question',status='completed')])))

    def test_18_stage_source_origin(self):
        r=a.read(base(session=dict(state='in_progress',stages=[dict(id='preparation',status='completed'),dict(id='finish',status='skipped')])))
        self.assertTrue(all(s['provenance']=='editorial_application_tracking' for s in r['session']['stage_reports']))
        self.assertFalse(r['session']['spiritual_records_opened'])
        self.assertFalse(r['session']['spiritual_records_closed_verified'])

    def test_19_stage_clock_order(self):
        stages=[dict(id='question',timestamp='2026-11-04T10:00:10Z'),dict(id='finish',timestamp='2026-11-04T10:00:00Z')]
        with self.assertRaises(ValueError):a.read(base(session=dict(stages=stages)))
        stages[1]['timestamp']='2026-11-04T10:00:00'
        self.assertEqual(len(a.read(base(session=dict(stages=stages)))['session']['stage_reports']),2)

    def test_20_invalid_timestamps(self):
        for stamp in ('now','2026-02-30','2026-11-04T10:00:00+99:00'):
            with self.assertRaises(ValueError):a.read(base(session=dict(timestamp=stamp)))

    def test_21_note_reference_isolation(self):
        r=a.read(base(notes=[dict(id='n1',concept_ids=['records','spirit_message'])]))
        self.assertEqual(r['notes'][0]['references'][1]['status'],'unsupported_concept')
        self.assertEqual(r['concept_references'],[])

    def test_22_no_required_identity(self):
        r=a.read(base(background=None,focus='',intention=None,unknowns=[]))
        self.assertEqual(r['user_context'],dict(background=None,focus='',intention=None,unknowns=[]))
        with self.assertRaises(ValueError):a.read(base(legal_name='Someone'))

    def test_23_strict_schema_and_ids(self):
        for q in (base(seed=0),base(mode='llm'),base(schema_version=True),base(concept_ids=['records']*2),base(question=dict(purpose='psychic')),base(concept_ids=['../file']),base(profile=[])):
            with self.assertRaises(ValueError):a.read(q)

    def test_24_raw_limits_and_utf8(self):
        for text in ('x'*20001,'bad\x00','\ud800'):
            with self.assertRaises(ValueError):a.read(base(question=dict(text=text)))
        with self.assertRaises(ValueError):a.read(base(notes=[dict(id='n')]*2))
        with self.assertRaises(ValueError):a.read(base(notes=[dict(id='n',uncertainty=1)]))

    def test_25_evidence_and_no_prayer_copy(self):
        r=a.read(base(concept_ids=list(a.CONCEPTS)))
        self.assertEqual(set(r['provenance_matrix']),{'direct','user_attributed','editorial','unsupported'})
        self.assertFalse(r['guidance']['procedure']['prayer_reproduced'])
        self.assertNotIn('Opening Prayer\nAnd so',json.dumps(r))
        self.assertFalse(r['replay']['generated_narrative'])

    def test_26_registry_and_rights(self):
        reg=load_registry()
        try:
            a.read(base(),reg)
            rows=reg.db.execute('SELECT record FROM rules WHERE id LIKE ?',('akashic.howe.%',)).fetchall()
            self.assertEqual(len(rows),10)
            self.assertTrue(all(json.loads(r[0])['status']=='proposed' for r in rows))
            self.assertTrue(all(s['ingestion']=='facts_only' for s in a.DATA['sources']))
        finally:reg.close()

    def test_27_immutable_profile_and_request(self):
        with self.assertRaises(TypeError):a.DATA['version']=2
        q=base(question=dict(text='Original'),notes=[dict(id='n',text='Note')]);snapshot=copy.deepcopy(q);r=a.read(q)
        q['question']['text']='Changed';r['notes'][0]['user_record']['text']='Other'
        self.assertEqual(r['question']['user_record']['text'],'Original')
        self.assertEqual(r['replay']['request'],snapshot)

    def test_28_portable_replay_and_markdown(self):
        q=base(question=dict(text='```\r\n猫 Café '),concept_ids=['records']);r=a.read(q);md=a.markdown(r)
        m=re.search(r'(`{3,})json\n(.*?)\n\1',md.split('## Exact replay metadata')[1],re.S)
        replay=json.loads(m[2]);self.assertEqual(a.read(replay['request']),json.loads(json.dumps(r)))
        self.assertEqual(a.PROFILE_HASH,a.digest(a.thaw(a.DATA)))
        self.assertEqual(a.digest(dict(b=1,a='猫')),a.digest(dict(a='猫',b=1)))

    def test_29_default_profile_and_disabled_questions(self):
        q=base(editorial_questions=False);q.pop('profile');r=a.read(q)
        self.assertEqual(r['profile'],a.PROFILE);self.assertEqual(r['editorial_questions'],[])
        self.assertNotIn('profile',r['replay']['request'])

    def test_30_strict_file_and_bounds(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'x.json');p.write_text('{"a":1,"a":2}',encoding='utf-8')
            with self.assertRaises(ValueError):a.load_input(p)
        with self.assertRaises(ValueError):a.read(base(notes=[dict(id='n'+str(i)) for i in range(65)]))
        self.assertEqual(a.read(base(question=dict(purpose='unknown')))['question']['effective_purpose'],'unspecified')


if __name__=='__main__':unittest.main()
