import copy
import hashlib
import json
from pathlib import Path
import unittest
import tempfile
from future import oracle as o
from future.card_random import PROTOCOL
from future.knowledge import Registry

ROOT = Path(__file__).resolve().parents[1]
BASE = dict(schema_version=1, profile=o.PROFILE, task='symbolic_reading', mode='seeded',
    spread='three', seed='Future-Lenormand-v1', protocol=PROTOCOL, orientation_policy='upright_only')


def manual(numbers, **kwargs):
    return {k: v for k, v in BASE.items() if k not in ('seed', 'protocol')} | dict(
        mode='manual', cards=[dict(card_id=f'lenormand-{n:02d}') for n in numbers]) | kwargs


class OracleTests(unittest.TestCase):
    def test_36_inventory_transcription(self):
        f=json.loads((ROOT/'tests/fixtures/oracle_source_examples.json').read_text())
        self.assertEqual([o.card(k)['number'] for k in o.ORDER], f['numbers'])
        self.assertEqual([o.card(k)['name'] for k in o.ORDER], f['names'])
        self.assertEqual(len(set(o.ORDER)),36)

    def test_meaning_coverage(self):
        for n,k in enumerate(o.ORDER,1):
            m=o.card(k)['meaning']
            self.assertTrue(m['text'] and m['context'] and m['source_id'])
            self.assertEqual(m['locator'],f'Signification of the Cards,No.{n}')
            self.assertEqual(m['coverage'],'direct_source_paraphrase')

    def test_historical_meanings_not_modern_substitution(self):
        f=json.loads((ROOT/'tests/fixtures/oracle_source_examples.json').read_text())
        for c in f['cases']:
            m=o.card(f"lenormand-{c['number']:02d}")['meaning']
            text=(m['text']+' '+m['context']).lower()
            for word in c['motifs']: self.assertIn(word.lower(),text)

    def test_historical_example_transcription_and_discrepancy(self):
        f=json.loads((ROOT/'tests/fixtures/oracle_source_examples.json').read_text())['example']
        audit=json.loads((ROOT/'knowledge/oracle_pass1_findings.json').read_text())['source_example']
        self.assertEqual(sum(f['rows'],[]),audit['order'])
        self.assertEqual(sorted(sum(f['rows'],[])),list(range(1,37)))
        self.assertEqual(f['rows'][0][4],f['above'])
        self.assertEqual(f['rows'][2][4],f['below'])
        self.assertEqual(f['rows'][1][4],f['person'])
        self.assertLess(f['rows'][1].index(28),f['rows'][1].index(29))
        self.assertIn('right',audit['discrepancy'])

    def test_independent_full_pack_vectors(self):
        vectors=json.loads((ROOT/'tests/fixtures/oracle_seed_vectors.json').read_text(encoding='utf-8'))['vectors']
        for v in vectors:
            ids,pack,trace=o.draw(v['seed'],36)
            self.assertEqual([o.card(k)['number'] for k in pack],v['permutation'])
            self.assertEqual(ids,pack)
            self.assertEqual(sorted(pack),sorted(o.ORDER))
            self.assertEqual(trace['cuts'],[])
        self.assertNotEqual(vectors[2]['permutation'],vectors[3]['permutation'])

    def test_draw_sizes(self):
        for n in range(1,37):
            ids,pack,_=o.draw('all-counts',n)
            self.assertEqual(ids,pack[:n]);self.assertEqual(len(set(ids)),n)
        for n in [0,-1,37,True,3.0,None,'3']:
            with self.assertRaises(ValueError): o.draw('x',n)

    def test_manual_spreads(self):
        for spread,nums in [('one',[13]),('three',[28,25,9]),('five',[6,16,25,29,24])]:
            r=o.read(manual(nums,spread=spread))
            self.assertEqual([x['card']['number'] for x in r['readings']],nums)
            self.assertEqual(len(r['combinations']),len(nums)-1)
            self.assertIsNone(r['replay']['shuffled_pack'])

    def test_all_seeded_spreads(self):
        for s,n in o.SPREADS.items():
            r=o.read(BASE|dict(spread=s))
            self.assertEqual(len(r['readings']),n)
            self.assertEqual([x['position'] for x in r['readings']],list(range(1,n+1)))
            self.assertTrue(all(x['orientation']=='upright' for x in r['readings']))
            self.assertFalse(r['replay']['orientation_stream_used'])

    def test_adjacent_order(self):
        r=o.read(manual([1,3,4]))
        self.assertEqual([p['card_ids'] for p in r['combinations']],
            [['lenormand-01','lenormand-03'],['lenormand-03','lenormand-04']])
        self.assertNotEqual(o.combine('lenormand-01','lenormand-03')['text'],
            o.combine('lenormand-03','lenormand-01')['text'])

    def test_source_cloud_condition_is_not_certified_pair(self):
        for pair in [(6,16),(16,6)]:
            p=o.combine(*(f'lenormand-{n:02d}' for n in pair))
            self.assertEqual(p['direct_conditions'][0]['rule_id'],'oracle.ew1903.star-clouds')
            self.assertFalse(p['direct_conditions'][0]['condition_verified'])
            self.assertEqual(p['direct_pair']['coverage'],'unsupported')

    def test_ring_direction_and_unresolved_distance(self):
        for person in [28,29]:
            a=o.combine(f'lenormand-{person}','lenormand-25')['direct_conditions'][0]
            b=o.combine('lenormand-25',f'lenormand-{person}')['direct_conditions'][0]
            self.assertEqual(a['application'],'experimental_page_right')
            self.assertEqual(b['application'],'unsupported_distance')
            self.assertFalse(a['condition_verified']);self.assertFalse(b['condition_verified'])

    def test_unsupported_pair_and_profiles(self):
        p=o.combine('lenormand-01','lenormand-36')
        self.assertEqual(p['direct_conditions'],[])
        self.assertEqual(p['coverage'],'compositional')
        for profile in ['Rana40','Kipper','Belline','waite-1922-text-v1',None]:
            with self.assertRaises(ValueError):o.read(BASE|dict(profile=profile))
        for k in ['major-00','lenormand-37',{},None]:
            with self.assertRaises(ValueError):o.card(k)

    def test_invalid_input(self):
        bad=[BASE|dict(schema_version=True),BASE|dict(spread=[]),BASE|dict(spread='nine'),
            BASE|dict(orientation_policy='seeded_reversals'),BASE|dict(seed=''),
            BASE|dict(protocol='v2'),BASE|dict(task='prediction'),BASE|dict(cuts=[1]),
            BASE|dict(cards=[]),BASE|dict(question='\n'),BASE|dict(question='\ud800'),
            manual([1,1,2]),manual([1]),manual([1,2,3],seed='x'),
            manual([1,2,3],cards=[dict(card_id='lenormand-01',orientation='reversed')]*3),
            manual([1,2,3],cards=[None]*3)]
        for value in bad:
            with self.subTest(value=repr(value)):
                with self.assertRaises(ValueError):o.read(value)

    def test_immutable_catalog_and_request(self):
        with self.assertRaises(TypeError):o.CARDS['lenormand-01']['number']=2
        c=o.card('lenormand-01');c['meaning']['text']='changed'
        self.assertNotEqual(o.card('lenormand-01')['meaning']['text'],'changed')
        value=copy.deepcopy(BASE);r=o.read(value);value['seed']='mutated'
        self.assertEqual(r['replay']['request'],BASE)

    def test_exact_replay_and_hashes(self):
        for value in [BASE,manual([28,25,9])]:
            r=o.read(value)
            self.assertEqual(o.read(r['replay']['request']),r)
            self.assertEqual(o.read(json.loads(json.dumps(r))['replay']['request']),r)
            self.assertEqual(r['replay']['canonical_order_sha256'],
                hashlib.sha256('\n'.join(o.ORDER).encode()).hexdigest())
            self.assertEqual(r['replay']['catalog_sha256'],hashlib.sha256(o._PATH.read_bytes()).hexdigest())

    def test_markdown_replay(self):
        r=o.read(BASE|dict(question='<script> | symbolic context'))
        text=o.markdown(r)
        replay=json.loads(text.split('```json\n')[1].split('\n```')[0])
        self.assertEqual(o.read(replay['request']),r)
        self.assertIn('&lt;script&gt;',text)
        self.assertEqual(text,o.markdown(r))
        self.assertIn('Context:',text);self.assertIn('Source:',text)

    def test_registry_isolation(self):
        with_registry=Registry()
        try:
            o.read(BASE,with_registry);o.register_knowledge(with_registry)
            records=with_registry.select_rules(17,'Lenormand 36',o.PROFILE)
            # Rules stay proposed;source transcription is not empirical certification.
            self.assertEqual(records,[])
            self.assertGreaterEqual(with_registry.db.execute('select count(*) from rules').fetchone()[0],36)
        finally:with_registry.close()

    def test_no_tarot_mutation(self):
        from future.tarot_catalog import ORDER as tarot_order
        from future.card_random import shuffle_pack
        before=shuffle_pack(tarot_order,'Future-Tarot-v1')
        o.read(BASE)
        self.assertEqual(before,shuffle_pack(tarot_order,'Future-Tarot-v1'))

    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp,'input.json')
            for text in ['{"seed":"a","seed":"b"}','{"seed":NaN}','{"seed":Infinity}']:
                path.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):o.load_input(path)
            path.write_text(json.dumps(BASE),encoding='utf-8-sig')
            self.assertEqual(o.load_input(path),BASE)


if __name__=='__main__':unittest.main()
