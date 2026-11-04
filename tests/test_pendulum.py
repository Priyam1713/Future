import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from future import pendulum as p
from future.card_random import Stream
from future.knowledge import Registry

ROOT=Path(__file__).resolve().parents[1]
MANUAL=dict(schema_version=1,profile=p.PROFILE,task='symbolic_response',mode='manual',
    calibration=[dict(signal='clockwise',response='yes'),dict(signal='counterclockwise',response='no')],
    observations=[dict(signal='clockwise')])
SEEDED={k:v for k,v in MANUAL.items() if k not in ('calibration','observations')}|dict(mode='seeded',
    seed='Future-Pendulum-v1',protocol=p.PROTOCOL,distribution=p.DISTRIBUTION)


class PendulumTests(unittest.TestCase):
    def test_source_profile_and_procedure_rules(self):
        self.assertEqual(p.PROFILE,'lonegren-web-symbolic-response-v1')
        self.assertEqual(len(p.DATA['rules']),6)
        self.assertTrue(all(x['locator'] and x['statement'] for x in p.DATA['rules']))
        self.assertIn('not print Kit',p.read(MANUAL)['procedure']['source_scope'])
        for profile in ['Kit19','Lethbridge1976','Olson2017',None]:
            with self.assertRaises(ValueError):p.read(MANUAL|dict(profile=profile))

    def test_independent_source_cases(self):
        cases=json.loads((ROOT/'tests/fixtures/pendulum_source_cases.json').read_text(encoding='utf-8'))['cases']
        for case in cases:
            value=MANUAL|dict(calibration=[dict(signal=s,response=r) for s,r in case['calibration']],
                observations=[dict(signal=case['signal'],quality=case.get('quality','full'))])
            self.assertEqual(p.read(value)['outcome']['symbolic_response'],case['expected'],case['name'])

    def test_multiple_calibration_conventions(self):
        for signals in [('clockwise','counterclockwise'),('counterclockwise','clockwise'),('vertical','horizontal'),('horizontal','vertical')]:
            config=[dict(signal=signals[0],response='yes'),dict(signal=signals[1],response='no')]
            for n,expected in enumerate(('yes','no')):
                self.assertEqual(p.read(MANUAL|dict(calibration=config,observations=[dict(signal=signals[n])]))['outcome']['symbolic_response'],expected)

    def test_duplicate_and_contradictory_mappings_rejected(self):
        for response in ('yes','no'):
            with self.assertRaisesRegex(ValueError,'Duplicate or contradictory'):
                p.read(MANUAL|dict(calibration=MANUAL['calibration']+[dict(signal='clockwise',response=response)]))
        for signal in ('searching','still','partial','conflicting','unknown','diagonal'):
            with self.assertRaises(ValueError):p.calibration([dict(signal=signal,response='yes')])
        with self.assertRaises(ValueError):p.calibration([dict(signal='irregular',response='no')])

    def test_incomplete_calibration_preserved(self):
        for config in ([],[dict(signal='clockwise',response='yes')],[dict(signal='clockwise',response='no')]):
            result=p.read(MANUAL|dict(calibration=config))
            self.assertFalse(result['configuration']['complete'])
            self.assertFalse(result['outcome']['resolved'])
            self.assertIn('incomplete_calibration',result['outcome']['reasons'])

    def test_search_still_irregular_and_unknown(self):
        for signal in ('searching','still','irregular','partial','conflicting','unknown'):
            result=p.read(MANUAL|dict(observations=[dict(signal=signal)]))
            self.assertEqual(result['outcome']['symbolic_response'],'unresolved')
            self.assertEqual(result['observations'][0]['signal'],signal)

    def test_unrecognized_signal_does_not_default(self):
        result=p.read(MANUAL|dict(observations=[dict(signal='diagonal-to-left')]))
        self.assertEqual(result['outcome']['symbolic_response'],'unresolved')
        self.assertIn('unrecognized_signal',result['outcome']['reasons'])
        self.assertEqual(result['observations'][0]['signal'],'diagonal-to-left')

    def test_partial_conflicting_and_unknown_quality(self):
        for quality in ('partial','conflicting','unknown'):
            result=p.read(MANUAL|dict(observations=[dict(signal='clockwise',quality=quality)]))
            self.assertEqual(result['observations'][0]['calibrated_response'],'yes')
            self.assertEqual(result['outcome']['symbolic_response'],'unresolved')
        with self.assertRaises(ValueError):p.read(MANUAL|dict(observations=[dict(signal='clockwise',quality='strong')]))

    def test_repeated_unanimous_full_responses(self):
        value=MANUAL|dict(observations=[dict(signal='clockwise')]*64)
        result=p.read(value)
        self.assertTrue(result['outcome']['resolved'])
        self.assertEqual(len(result['observations']),64)
        self.assertIsNone(result['truth_confidence'])

    def test_repeated_conflict_or_neutral_never_votes(self):
        for final in ('counterclockwise','still','unknown'):
            result=p.read(MANUAL|dict(observations=[dict(signal='clockwise')]*10+[dict(signal=final)]))
            self.assertFalse(result['outcome']['resolved'])
            self.assertEqual(result['outcome']['conflicting'],final=='counterclockwise')

    def test_declared_search_and_rethink_mapping(self):
        for response in ('search','rethink','unresolved'):
            result=p.read(MANUAL|dict(calibration=MANUAL['calibration']+[dict(signal='vertical',response=response)],observations=[dict(signal='vertical')]))
            self.assertEqual(result['observations'][0]['calibrated_response'],response)
            self.assertEqual(result['outcome']['symbolic_response'],'unresolved')

    def test_manual_and_seeded_isolation(self):
        for extra in (dict(seed='x'),dict(protocol=p.PROTOCOL),dict(distribution=p.DISTRIBUTION)):
            with self.assertRaises(ValueError):p.read(MANUAL|extra)
        for extra in (dict(calibration=[]),dict(observations=[])):
            with self.assertRaises(ValueError):p.read(SEEDED|extra)
        manual=p.read(MANUAL);digital=p.read(SEEDED)
        self.assertIsNone(manual['generated_response']);self.assertIsNone(manual['replay']['simulation'])
        self.assertEqual(digital['observations'],[]);self.assertIsNone(digital['generated_signal'])

    def test_strict_schema_and_fields(self):
        for extra in (dict(schema_version=True),dict(schema_version=2),dict(task='prediction'),dict(mode='camera'),dict(truth=True)):
            with self.assertRaises(ValueError):p.read(MANUAL|extra)
        for value in (None,[],True):
            with self.assertRaises(ValueError):p.read(value)
        for row in (dict(signal='clockwise',amplitude=10),dict(signal=None),dict(signal=True),{}):
            with self.assertRaises(ValueError):p.read(MANUAL|dict(observations=[row]))

    def test_observation_and_calibration_bounds(self):
        for rows in ([],[dict(signal='clockwise')]*65,None,{}):
            with self.assertRaises(ValueError):p.read(MANUAL|dict(observations=rows))
        for config in (None,{},[dict(signal='clockwise',response='maybe')],[dict(signal='clockwise',response='yes',extra=1)]):
            with self.assertRaises(ValueError):p.read(MANUAL|dict(calibration=config))

    def test_seeded_exact_profile_protocol_distribution(self):
        for extra in (dict(protocol='future-cards-sha256-fy-v1'),dict(distribution='historical'),dict(weights=[1,1,1])):
            with self.assertRaises(ValueError):p.read(SEEDED|extra)
        self.assertFalse(p.read(SEEDED)['replay']['physical_motion_generated'])

    def test_exact_categorical_distribution(self):
        outcomes=[p.category(n) for n in range(5)]
        self.assertEqual([outcomes.count(x) for x in ('yes','no','unresolved')],[2,2,1])
        self.assertEqual(list(p.WEIGHTS),[2,2,1])
        for value in (-1,5,True,1.0,None):
            with self.assertRaises(ValueError):p.category(value)

    def test_rejection_boundary_without_modulo_bias(self):
        class Boundary(p.SymbolicStream):
            def __init__(self):super().__init__('boundary');self.test_words=iter([4294967295,4294967294])
            def word(self):return next(self.test_words)
        stream=Boundary()
        self.assertEqual(stream.below(5),4)
        self.assertEqual(stream.rejections,1)

    def test_six_independent_dotnet_32_draw_vectors(self):
        vectors=json.loads((ROOT/'tests/fixtures/pendulum_seed_vectors.json').read_text(encoding='utf-8'))['vectors']
        self.assertEqual(len(vectors),6)
        for v in vectors:
            stream=p.SymbolicStream(v['seed']);indices=[stream.below(5) for _ in range(32)]
            self.assertEqual(indices,v['indices']);self.assertEqual([p.category(n) for n in indices],v['categories'])
            self.assertEqual(hashlib.sha256(stream.prefix+bytes(8)).hexdigest(),v['first_block'])
            self.assertEqual((stream.counter,stream.rejections),(v['blocks'],v['rejected_words']))

    def test_domain_and_seed_framing(self):
        stream=p.SymbolicStream('é')
        self.assertEqual(stream.prefix,b'FuturePendulum\0v1\0symbolic-response\0\0\0\0\x02\xc3\xa9')
        self.assertNotEqual(stream.word(),Stream('é','deck').word())
        self.assertIs(p.SymbolicStream.word,Stream.word)
        self.assertIs(p.SymbolicStream.below,Stream.below)

    def test_utf8_seed_boundaries_no_normalization(self):
        for seed in ('',True,None,'x'*257,'é'*129,'\ud800'):
            with self.assertRaises(ValueError):p.read(SEEDED|dict(seed=seed))
        for seed in ('x','x'*256,'é'*128,'\0',' seed '):
            self.assertEqual(p.read(SEEDED|dict(seed=seed))['replay']['seed'],seed)
        self.assertNotEqual(p.simulate('Café')[1]['first_block'],p.simulate('Cafe\u0301')[1]['first_block'])

    def test_question_never_affects_random_or_truth(self):
        base=p.read(SEEDED)
        for question in ('Will I get the job?','Is this diagnosis true?','What could I reflect on?'):
            result=p.read(SEEDED|dict(question=question))
            self.assertEqual(result['outcome'],base['outcome'])
            self.assertEqual(result['replay']['simulation'],base['replay']['simulation'])
            self.assertFalse(result['factual_prediction']);self.assertIsNone(result['truth_confidence'])
        for q in ('',None,'a\nb','x'*1001,'\ud800'):
            with self.assertRaises(ValueError):p.read(SEEDED|dict(question=q))

    def test_complete_json_and_markdown_replay(self):
        for value in (MANUAL,SEEDED):
            result=p.read(value)
            self.assertEqual(json.loads(json.dumps(result)),result)
            replay=json.loads(p.markdown(result).split('## Exact replay metadata')[1].split('```json\n')[1].split('\n```')[0])
            self.assertEqual(p.read(replay['request']),result)
            self.assertEqual(replay['profile_sha256'],p.PROFILE_HASH)

    def test_markdown_escaping_and_explicit_layers(self):
        report=p.markdown(p.read(MANUAL|dict(question='<script>|hello')))
        self.assertNotIn('<script>',report.split('## Exact replay metadata')[0])
        self.assertIn('&lt;script&gt;',report)
        self.assertIn('Modern editorial reflection',report)
        self.assertIn('source',report.lower());self.assertIn('calibrated',report)

    def test_strict_json_duplicate_and_nonfinite_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp,'input.json')
            for text in ('{"mode":1,"mode":2}','{"value":NaN}','{"value":Infinity}'):
                path.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):p.load_input(path)
            path.write_text(json.dumps(MANUAL),encoding='utf-8-sig')
            self.assertEqual(p.load_input(path),MANUAL)

    def test_registry_source_rules_and_idempotence(self):
        registry=Registry()
        try:
            p.read(MANUAL,registry);p.read(SEEDED,registry)
            self.assertEqual(registry.db.execute('select count(*) from rules').fetchone()[0],6)
            self.assertEqual(registry.db.execute('select count(*) from sources').fetchone()[0],1)
        finally:registry.close()

    def test_immutable_catalog_and_request(self):
        with self.assertRaises(TypeError):p.DATA['profile']='other'
        with self.assertRaises(TypeError):p.DATA['signals']['still']='yes'
        value=copy.deepcopy(MANUAL);original=copy.deepcopy(value);result=p.read(value)
        self.assertEqual(value,original)
        result['sources'][0]['url']='mutated';result['procedure']['rules'][0]['statement']='mutated'
        self.assertNotEqual(p.read(value)['sources'],result['sources'])

    def test_portable_profile_hash_and_rejection_reports(self):
        raw=(ROOT/'knowledge/pendulum_profile_v1.json').read_text(encoding='utf-8')
        self.assertEqual(p.PROFILE_HASH,p.digest(json.loads(raw.replace('\n','\r\n'))))
        self.assertEqual(json.loads(p.rejection('Contradictory calibration','json'))['status'],'rejected')
        self.assertNotIn('<script>',p.rejection('<script>','markdown'))


if __name__=='__main__':unittest.main()
