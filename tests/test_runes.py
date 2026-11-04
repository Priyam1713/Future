import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unicodedata
import unittest
from future import runes as r
from future.card_random import Stream
from future.knowledge import Registry

ROOT=Path(__file__).resolve().parents[1]
REF=json.loads((ROOT/'tests/fixtures/runes_inventory_reference.json').read_text(encoding='utf-8'))
BASE=dict(schema_version=1,profile=r.PROFILE,task='symbolic_reading',mode='seeded',spread='three',
    protocol=r.PROTOCOL,seed='Future-Runes-v1',orientation_policy='upright_only')


def manual(ids,spread='three'):
    return {k:v for k,v in BASE.items() if k not in ('seed','protocol')}|dict(mode='manual',spread=spread,
        runes=[dict(rune_id=k) for k in ids])


class RuneTests(unittest.TestCase):
    def test_all24_identity_order_names(self):
        self.assertEqual([r.rune(k)['position'] for k in r.ORDER],REF['positions'])
        self.assertEqual([r.rune(k)['name'] for k in r.ORDER],REF['names'])
        self.assertEqual(len(set(r.ORDER)),24)
        self.assertEqual(list(r.ORDER),[f'rune-{n:02d}' for n in range(1,25)])

    def test_unicode_glyphs_and_fallbacks(self):
        for identifier,cp in zip(r.ORDER,REF['codepoints']):
            item=r.rune(identifier)
            self.assertEqual(ord(item['glyph']),int(cp,16))
            self.assertEqual(item['codepoint'],'U+'+cp)
            self.assertEqual(item['unicode_name'],unicodedata.name(item['glyph']))
            self.assertIn(identifier,item['text_fallback'])
        self.assertEqual(len({r.rune(k)['glyph'] for k in r.ORDER}),24)

    def test_transliteration_and_uncertain_sound(self):
        self.assertEqual([r.rune(k)['transliteration'] for k in r.ORDER],REF['transliterations'])
        # Page Figure1/sound qualifications: approximate sound reference, not exact phonetic reconstruction.
        self.assertEqual([r.rune(k)['phonetic_value'] for k in r.ORDER],
            ['f','u','θ','a','r','k','g','w','h','n','i','j',None,'p','z','s','t','b','e','m','l','ŋ (possibly ŋg)','o','d'])
        self.assertIsNone(r.rune('rune-13')['phonetic_value'])
        self.assertEqual(r.rune('rune-13')['phonetic_status'],'uncertain')
        self.assertEqual(r.rune('rune-03')['phonetic_value'],'θ')
        self.assertIn('possibly',r.rune('rune-22')['phonetic_value'])

    def test_names_not_attested_as_elder_labels(self):
        for item in r.RUNES.values():
            self.assertFalse(item['name_attested_as_elder_label'])
            self.assertIn(item['name_classification'],['reconstructed','reconstructed_disputed','editorial_label_for_divergent_names'])
            self.assertIn('later_language',item['related_name']['classification'])
        self.assertEqual(r.rune('rune-06')['name_classification'],'editorial_label_for_divergent_names')

    def test_historical_order_variants_not_silently_substituted(self):
        self.assertEqual([r.rune(k)['transliteration'] for k in r.ORDER[-2:]],REF['historical_variants']['selected_final'])
        self.assertNotEqual(REF['historical_variants']['kylver_final'],REF['historical_variants']['selected_final'])
        self.assertEqual([r.rune(k)['transliteration'] for k in r.ORDER[12:14]],['ï','p'])
        self.assertIn('13/14',r.DATA['historical_variants']['kylver'])

    def test_reference_coverage_and_three_layers(self):
        nonnull=0
        for item in r.RUNES.values():
            self.assertTrue(item['historical_reference']['locator'])
            self.assertTrue(item['association']['source_id'] and item['association']['locator'])
            self.assertEqual(item['association']['coverage'],'comparative_reconstructed')
            self.assertEqual(item['composition']['coverage'],'modern_editorial')
            self.assertFalse(item['composition']['ancient_rule'])
            nonnull+=int(item['association']['lexical_association'] is not None)
        self.assertEqual(nonnull,21)

    def test_independent_source_cases(self):
        for case in REF['source_cases']:
            item=r.rune(f"rune-{case['position']:02d}")
            if 'lexical' in case:self.assertEqual(item['association']['lexical_association'],case['lexical'])
            if 'phonetic' in case:self.assertEqual(item['phonetic_value'],case['phonetic'])
            if 'conflict_contains' in case:self.assertIn(case['conflict_contains'],' '.join(item['conflicts']).lower())

    def test_unknowns_preserved_in_readings(self):
        result=r.read(manual(['rune-06','rune-14','rune-15']))
        self.assertTrue(all(x['unresolved_meaning'] for x in result['readings']))
        self.assertTrue(all(x['comparative']['lexical_association'] is None for x in result['readings']))
        self.assertIn('unresolved',result['summary']['text'])
        self.assertIn('not established',result['readings'][1]['conflicts'][0])

    def test_poem_tradition_is_separate(self):
        result=r.read(manual(['rune-04','rune-15','rune-17']))
        for row in result['readings']:
            self.assertEqual(row['later_poem_accounts'][0]['tradition'],'Old English Futhorc')
            self.assertFalse(row['later_poem_accounts'][0]['translation_reproduced'])
            self.assertNotEqual(row['later_poem_accounts'][0]['source_id'],row['comparative']['source_id'])

    def test_no_blank_or_system_substitution(self):
        for name in ['blank','rune-25','younger-01','major-00','lenormand-01',None,{}]:
            with self.assertRaises(ValueError):r.rune(name)
        for profile in ['Blum25','Younger16','Futhorc',None]:
            with self.assertRaises(ValueError):r.read(BASE|dict(profile=profile))

    def test_full_draw_without_replacement_and_counts(self):
        for n in range(1,25):
            selected,pack,trace=r.draw('all-counts',n)
            self.assertEqual(selected,pack[:n]);self.assertEqual(len(set(selected)),n)
            self.assertEqual(sorted(pack),sorted(r.ORDER));self.assertEqual(trace['cuts'],[])
        for n in [0,-1,25,True,1.0,None,'3']:
            with self.assertRaises(ValueError):r.draw('x',n)

    def test_six_independent_complete_set_vectors(self):
        vectors=json.loads((ROOT/'tests/fixtures/runes_seed_vectors.json').read_text(encoding='utf-8'))['vectors']
        self.assertEqual(len(vectors),6)
        for v in vectors:
            selected,pack,_=r.draw(v['seed'],24)
            self.assertEqual([r.rune(k)['position'] for k in pack],v['permutation'])
            self.assertEqual(selected,pack)
            stream=Stream(v['seed'],'deck')
            self.assertEqual(hashlib.sha256(stream.prefix+bytes(8)).hexdigest(),v['deck_first_block'])

    def test_utf8_seed_boundaries_and_no_normalization(self):
        for seed in ['',None,True,'x'*257,'é'*129,'\ud800']:
            with self.assertRaises(ValueError):r.read(BASE|dict(seed=seed))
        for seed in ['x','x'*256,'é'*128,'\0',' seed ']:
            self.assertEqual(r.read(BASE|dict(seed=seed))['replay']['seed'],seed)
        self.assertNotEqual(r.draw('Café',24)[0],r.draw('Cafe\u0301',24)[0])

    def test_seeded_one_and_three_positions(self):
        for spread,n in [('one',1),('three',3)]:
            result=r.read(BASE|dict(spread=spread))
            self.assertEqual(len(result['readings']),n)
            self.assertEqual([x['position']['order'] for x in result['readings']],list(range(1,n+1)))
            self.assertEqual([x['rune']['id'] for x in result['readings']],result['replay']['shuffled_set'][:n])
        self.assertEqual([x['position']['label'] for x in r.read(BASE)['readings']],['Situation','Challenge','Reflection'])

    def test_manual_order_and_duplicates(self):
        ids=['rune-23','rune-01','rune-24'];result=r.read(manual(ids))
        self.assertEqual([x['rune']['id'] for x in result['readings']],ids)
        self.assertIsNone(result['replay']['protocol']);self.assertIsNone(result['replay']['shuffled_set'])
        for bad in [manual(['rune-01']*3),manual(['rune-01']),manual(ids)|dict(seed='x'),manual(ids)|dict(protocol=r.PROTOCOL)]:
            with self.assertRaises(ValueError):r.read(bad)

    def test_upright_policy_and_rotation_separation(self):
        self.assertFalse(r.read(BASE)['replay']['orientation_stream_used'])
        self.assertTrue(all(x['orientation']=='upright' for x in r.read(BASE)['readings']))
        for policy in ['explicit','reversed','seeded_reversals',None]:
            with self.assertRaises(ValueError):r.read(BASE|dict(orientation_policy=policy))
        for orientation in ['reversed','face_down','mirrored',180]:
            with self.assertRaises(ValueError):r.read(manual(['rune-01'],'one')|dict(runes=[dict(rune_id='rune-01',orientation=orientation)]))

    def test_custom_editorial_labels(self):
        labels=['Context','Tension','Consideration'];result=r.read(BASE|dict(positions=labels))
        self.assertEqual([x['position']['label'] for x in result['readings']],labels)
        self.assertTrue(all(x['position']['coverage']=='editorial_layout' for x in result['readings']))
        for p in [['x']*3,['x','y'],['x','y','\n'],['x','y','\ud800'],'abc']:
            with self.assertRaises(ValueError):r.read(BASE|dict(positions=p))
        with self.assertRaises(ValueError):r.read(BASE|dict(spread='one',positions=['Focus']))

    def test_invalid_input_fields_and_modes(self):
        bad=[None,[],BASE|dict(schema_version=True),BASE|dict(spread=[]),BASE|dict(spread='nine'),
            BASE|dict(mode='auto'),BASE|dict(task='prediction'),BASE|dict(protocol='future-cards-sha256-fy-v1'),
            BASE|dict(runes=[]),BASE|dict(question=''),BASE|dict(question='\ud800'),BASE|dict(strength=9),
            manual(['rune-01'],'one')|dict(runes=[None]),manual(['rune-01'],'one')|dict(runes=[dict(rune_id='rune-01',rotation=0)])]
        for value in bad:
            with self.assertRaises(ValueError):r.read(value)

    def test_interpretation_and_unsupported_conclusions(self):
        result=r.read(manual(['rune-01','rune-10','rune-18']))
        self.assertFalse(result['factual_prediction']);self.assertIsNone(result['outcome_probabilities'])
        self.assertIsNone(result['combinations']['universal_rule'])
        for row in result['readings']:
            self.assertIn(row['position']['label'],row['compositional']['text'])
            self.assertIn(row['rune']['composition']['theme'],row['compositional']['text'])
            self.assertTrue(row['unsupported'])

    def test_exact_json_markdown_replay_and_escaping(self):
        for request in [BASE,BASE|dict(spread='one'),manual(['rune-06','rune-14','rune-15'])]:
            result=r.read(request|dict(question='<script>|context'))
            self.assertEqual(r.read(json.loads(json.dumps(result))['replay']['request']),result)
            text=r.markdown(result);replay=json.loads(text.split('```json\n')[1].split('\n```')[0])
            self.assertEqual(r.read(replay['request']),result)
            self.assertEqual(text,r.markdown(result));self.assertIn('&lt;script&gt;',text)
            self.assertIn('Text fallback:',text)

    def test_immutable_catalog_and_request(self):
        with self.assertRaises(TypeError):r.RUNES['rune-01']['name']='changed'
        x=r.rune('rune-01');x['association']['lexical_association']='changed'
        self.assertNotEqual(r.rune('rune-01')['association']['lexical_association'],'changed')
        value=copy.deepcopy(BASE);result=r.read(value);value['seed']='new'
        self.assertEqual(result['replay']['request'],BASE)

    def test_portable_catalog_and_order_hashes(self):
        s=(ROOT/'knowledge/runes_elder24_v1.json').read_text(encoding='utf-8')
        self.assertEqual(r.digest(json.loads(s)),r.digest(json.loads(s.replace('\n','\r\n'))))
        self.assertEqual(r.digest(json.loads(s)),r.CATALOG_HASH)
        self.assertEqual(hashlib.sha256('\n'.join(r.ORDER).encode('utf-8')).hexdigest(),r.ORDER_HASH)

    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'input.json')
            for text in ['{"seed":"x","seed":"y"}','{"seed":NaN}','{"seed":Infinity}']:
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):r.load_input(p)
            p.write_text(json.dumps(BASE),encoding='utf-8-sig');self.assertEqual(r.load_input(p),BASE)

    def test_registry_and_prior_draw_isolation(self):
        registry=Registry()
        try:
            r.read(BASE,registry);r.register_knowledge(registry)
            self.assertEqual(registry.db.execute('select count(*) from rules').fetchone()[0],48)
            self.assertEqual(registry.select_rules(19,'Younger (16)',r.PROFILE),[])
        finally:registry.close()
        from future.tarot_catalog import ORDER as tarot_order
        from future.card_random import shuffle_pack
        before=shuffle_pack(tarot_order,'Future-Tarot-v1')
        r.read(BASE)
        self.assertEqual(before,shuffle_pack(tarot_order,'Future-Tarot-v1'))


if __name__=='__main__':unittest.main()
