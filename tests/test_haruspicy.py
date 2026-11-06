import copy,json,re,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from future import haruspicy as h
from future.__main__ import load_registry
F=json.loads(Path('tests/fixtures/haruspicy_reference_v1.json').read_text(encoding='utf-8'))
def obs(**kw):return dict(observation_id='o',tradition='roman',organ='lung',feature='cleft',presence='present',other_vitals='sound')|kw
def q(o=None,**kw):return dict(schema_version=1,profile=h.PROFILE,mode='manual',task='compare',catalog_id=h.DATA['catalog_id'],catalog_version=1,catalog_sha256=h.CATALOG_HASH,observations=[o or obs()])|kw
def ref(ids):return {k:v for k,v in q(task='reference',reference_ids=ids).items() if k!='observations'}
def result(o=None):return h.read(q(o))['observations'][0]
def heart(**kw):return copy.deepcopy(F['known_answers'][7]['observations'][0])|kw
def liver(**kw):return copy.deepcopy(F['known_answers'][8]['observations'][1])|kw
def target(o,id,**kw):return next(x for x in h.read(q(o,**kw))['observations'][-1]['evaluations'] if x['rule_id']==id)
class HaruspicyTests(unittest.TestCase):
    def reject(self,x):
        with self.assertRaises((ValueError,OSError)):h.read(x)
    def test_source_records(self):self.assertEqual(h.assets()[1]['records'],F['records'])
    def test_integrity(self):self.assertTrue(h.integrity()['verified']);self.assertEqual(h.integrity()['records'],9)
    def test_lung_compound(self):self.assertEqual(result()['applicable_ids'],['lung-cleft'])
    def test_other_vitals_unknown(self):self.assertEqual(target(obs(other_vitals='unknown'),'lung-cleft')['status'],'insufficient_evidence')
    def test_other_vitals_not_sound(self):self.assertEqual(target(obs(other_vitals='not_sound'),'lung-cleft')['status'],'not_applicable')
    def test_other_vitals_missing(self):o=obs();o.pop('other_vitals');self.assertEqual(target(o,'lung-cleft')['status'],'insufficient_evidence')
    def test_liver_is_not_lung(self):self.assertEqual(target(obs(organ='liver'),'lung-cleft')['status'],'not_applicable')
    def test_absent_cleft_not_inverted(self):r=result(obs(presence='absent'));self.assertEqual(r['applicable_ids'],[]);self.assertEqual(r['historical_polarities'],[])
    def test_absent_head(self):self.assertEqual(result(liver(narrative_context='none'))['applicable_ids'],['liver-head-absent'])
    def test_present_head_no_favorable(self):self.assertEqual(result(liver(presence='present'))['historical_polarities'],[])
    def test_unknown_head(self):self.assertEqual(target(liver(presence='unknown'),'liver-head-absent')['status'],'insufficient_evidence')
    def test_omitted_presence(self):o=liver();o.pop('presence');self.assertEqual(target(o,'liver-head-absent')['status'],'insufficient_evidence')
    def test_head_attribution(self):self.assertIn('Practitioners',h.lookup('liver-head-absent')['attribution']);self.assertEqual(h.lookup('liver-head-absent')['speaker'],'Marcus')
    def test_standalone_heart(self):self.assertEqual(result(heart(narrative_context='none'))['applicable_ids'],[])
    def test_caesar_first(self):self.assertEqual(result(heart())['applicable_ids'],['caesar-heart'])
    def test_caesar_first_requires_all_context(self):
        for key in ('narrative_context','event_phase','animal','setting_id','warning_attribution'):
            self.assertEqual(target(heart(**{key:'unknown'}),'caesar-heart')['status'],'insufficient_evidence')
    def test_wrong_setting(self):self.assertEqual(target(heart(setting_id='other'),'caesar-heart')['status'],'not_applicable')
    def test_spurinna_not_inferred(self):self.assertEqual(target(heart(warning_attribution='unknown',raw_observation='Spurinna'),'caesar-heart')['status'],'insufficient_evidence')
    def test_sequence_complete(self):r=h.read(q(observations=[heart(),liver()]))['observations'][1];self.assertTrue(r['documentary_sequence_complete']);self.assertEqual(r['applicable_ids'],['liver-head-absent','caesar-liver-next-day'])
    def test_sequence_reversed(self):r=h.read(q(observations=[liver(),heart()]))['observations'][0];self.assertFalse(r['documentary_sequence_complete'])
    def test_sequence_missing(self):self.assertEqual(target(liver(),'caesar-liver-next-day')['status'],'insufficient_evidence')
    def test_sequence_self(self):self.assertEqual(target(liver(prior_observation_id='liver2'),'caesar-liver-next-day')['status'],'not_applicable')
    def test_sequence_wrong_predecessor(self):r=target(liver(),'caesar-liver-next-day',observations=[obs(observation_id='heart1'),liver()]);self.assertEqual(r['status'],'not_applicable')
    def test_sequence_unknown_predecessor(self):r=target(liver(),'caesar-liver-next-day',observations=[heart(uncertain_fields=['presence']),liver()]);self.assertEqual(r['status'],'insufficient_evidence')
    def test_sequence_conflicting_predecessor(self):r=target(liver(),'caesar-liver-next-day',observations=[heart(presence_reports=['present','absent']),liver()]);self.assertEqual(r['status'],'conflicting_evidence')
    def test_sequence_uncertain_link(self):r=target(liver(),'caesar-liver-next-day',observations=[heart(),liver(uncertain_fields=['prior_observation_id'])]);self.assertEqual(r['status'],'insufficient_evidence')
    def test_first_day_is_not_following(self):r=target(liver(),'caesar-liver-next-day',observations=[heart(),liver(event_phase='first_day')]);self.assertEqual(r['status'],'not_applicable')
    def test_sequence_raw_does_not_fill(self):self.assertFalse(result(liver(sequence=['heart first day','liver following day']))['documentary_sequence_complete'])
    def test_presence_contradiction(self):r=result(obs(presence_reports=['present','absent']));self.assertEqual(r['status'],'conflicting_evidence');self.assertEqual(r['applicable_ids'],[])
    def test_declared_contradiction(self):self.assertEqual(result(obs(presence_reports=['absent']))['status'],'conflicting_evidence')
    def test_vitals_contradiction(self):self.assertEqual(target(obs(other_vitals_reports=['sound','not_sound']),'lung-cleft')['status'],'conflicting_evidence')
    def test_structured_organ_contradiction(self):self.assertEqual(target(obs(contradictory_assertions={'organ':['lung','liver']}),'lung-cleft')['status'],'conflicting_evidence')
    def test_report_does_not_fill_unknown(self):self.assertEqual(target(obs(presence='unknown',presence_reports=['present']),'lung-cleft')['status'],'insufficient_evidence')
    def test_raw_not_parsed(self):self.assertEqual(result(obs(raw_observation='liver absent'))['applicable_ids'],['lung-cleft'])
    def test_uncertain_each_lung_predicate(self):
        for field in ('organ','feature','presence','other_vitals','tradition'):self.assertEqual(target(obs(uncertain_fields=[field]),'lung-cleft')['status'],'insufficient_evidence')
    def test_etruscan(self):self.assertEqual(result(obs(tradition='etruscan'))['status'],'unsupported')
    def test_mesopotamian(self):self.assertEqual(result(obs(tradition='mesopotamian'))['status'],'unsupported')
    def test_unknown_tradition(self):self.assertEqual(result(obs(tradition='unknown'))['status'],'insufficient_evidence')
    def test_other_feature_negative(self):self.assertEqual(result(obs(feature='other'))['status'],'not_applicable')
    def test_other_organ_negative(self):self.assertEqual(result(obs(organ='other'))['status'],'not_applicable')
    def test_unknown_feature(self):self.assertEqual(target(obs(feature='unknown'),'lung-cleft')['status'],'insufficient_evidence')
    def test_unknown_organ(self):self.assertEqual(target(obs(organ='unknown'),'lung-cleft')['status'],'insufficient_evidence')
    def test_reference_no_observations(self):r=h.read(ref(['heart-criticism','caesar-heart']));self.assertEqual(r['observations'],[]);self.assertEqual([x['id'] for x in r['references']],['heart-criticism','caesar-heart'])
    def test_reference_comparison(self):self.assertIsNone(h.read(ref(['lung-cleft','liver-head-absent']))['comparisons'][0]['combined_omen'])
    def test_catalog(self):x={k:v for k,v in q(task='catalog').items() if k!='observations'};self.assertEqual(len(h.read(x)['references']),9)
    def test_context_always_visible(self):self.assertEqual(len(h.read(q())['context_references']),5)
    def test_critical_heart(self):self.assertEqual(h.lookup('heart-criticism')['speaker'],'Marcus');self.assertIn('ancient speculation',h.lookup('heart-criticism')['source_account'])
    def test_source_terms(self):self.assertEqual(h.lookup('lung-cleft')['latin_terms'],['pulmo incisus']);self.assertIn('modern anatomical',h.lookup('liver-head-absent')['qualification'])
    def test_no_prediction_diagnosis_authority(self):r=result();self.assertIsNone(r['empirical_prediction']);self.assertIsNone(r['anatomical_diagnosis']);self.assertFalse(r['ritual_authority'])
    def test_user_origin(self):self.assertEqual(result(obs(origin='hypothetical'))['declared']['origin'],'hypothetical')
    def test_raw_unicode(self):raw='  Café Café\r\n猫\t `````json ';r=h.read(q(obs(user_association=raw),question=raw));self.assertEqual(r['user_text']['question'],raw);self.assertEqual(r['observations'][0]['declared']['user_association'],raw)
    def test_order(self):r=h.read(q(observations=[obs(observation_id='z'),obs(observation_id='a')]));self.assertEqual([x['observation_id'] for x in r['observations']],['z','a']);self.assertIsNone(r['comparisons'][0]['score'])
    def test_wrong_profile_hash(self):self.reject(q(profile='unknown'));self.reject(q(catalog_sha256='0'*64))
    def test_foreign_catalog(self):self.reject(q(catalog_id='piacenza-v1'));self.reject(q(catalog_id='barutu-v1'))
    def test_schema_types(self):
        for v in (True,1.0,2):self.reject(q(schema_version=v));self.reject(q(catalog_version=v))
    def test_no_prediction_task(self):self.reject(q(task='predict'));self.reject(q(task='diagnose'))
    def test_no_ritual_fields(self):self.reject(q(procedure='sacrifice'));self.reject(q(obs(preparation='unknown')))
    def test_invalid_enum(self):
        for k in h.DATA['domains']:self.reject(q(obs(**{k:'invalid'})));self.reject(q(obs(**{k:True})))
    def test_unknown_fields(self):self.reject(q(extra=1));self.reject(q(obs(zone_id=1)))
    def test_duplicate_ids(self):self.reject(q(observations=[obs(),obs()]))
    def test_bad_ids(self):
        for v in ('','猫','a b',True,'x'*81):self.reject(q(obs(observation_id=v)))
    def test_bad_link(self):self.reject(q(obs(prior_observation_id=True)))
    def test_observation_limits(self):self.reject(q(observations=[]));self.reject(q(observations=[obs()]*9))
    def test_reference_validation(self):self.reject(ref([]));self.reject(ref(['missing']));self.reject(ref(['lung-cleft']*2));self.reject(ref([True]))
    def test_invalid_raw(self):
        for v in (12,'\ud800','\x00','x'*10001):self.reject(q(question=v))
    def test_invalid_lists(self):self.reject(q(obs(sequence=[None])));self.reject(q(obs(presence_reports=['missing'])));self.reject(q(obs(uncertain_fields=['presence','presence'])));self.reject(q(obs(contradictory_assertions={'organ':'lung'})))
    def test_json_loader(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'q.json')
            for text in ('{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}'):
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):h.load_input(p)
    def test_replay(self):r=h.read(q(notes=' x '));self.assertEqual(h.read(r['replay']['request']),r)
    def test_markdown(self):r=h.read(q(notes='`````json 猫'));m=re.search(r'(`{3,})json\n(.*?)\n\1',h.markdown(r).split('## Exact replay metadata')[1],re.S);self.assertEqual(h.read(json.loads(m[2])['request']),r)
    def test_deepcopy(self):x=q();old=copy.deepcopy(x);r=h.read(x);r['observations'][0]['declared']['organ']='heart';self.assertEqual(x,old)
    def test_registry(self):
        r=load_registry()
        try:h.read(q(),r);h.read(q(),r);self.assertEqual(r.db.execute("select count(*) from rules where id like 'haruspicy.%'").fetchone()[0],9)
        finally:r.close()
    def test_asset_tamper(self):
        for name in ('catalog','roman_profile'):
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);(root/'knowledge').mkdir()
                for stem in ('catalog','roman_profile'):(root/f'knowledge/haruspicy_{stem}_v1.json').write_bytes((h.ROOT/f'knowledge/haruspicy_{stem}_v1.json').read_bytes())
                (root/f'knowledge/haruspicy_{name}_v1.json').write_text('{}',encoding='utf-8')
                with patch.object(h,'ROOT',root):self.reject(q())
    def test_known_answers(self):
        for case in F['known_answers']:self.assertEqual([x['applicable_ids'] for x in h.evaluate_all(case['observations'])],case['applicable'])
if __name__=='__main__':unittest.main()
