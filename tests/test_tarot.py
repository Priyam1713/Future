import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from future.card_random import PROTOCOL,Stream,SIZE,seed_bytes,shuffle_pack,orientations
from future.tarot_catalog import DATA,PROFILE,ORDER,CARDS,card,register_knowledge
from future.tarot import read,markdown,load_input
from future.knowledge import Registry

FIXTURE=json.loads(Path('tests/fixtures/tarot_source_examples.json').read_text(encoding='utf-8'))
VECTORS=json.loads(Path('tests/fixtures/tarot_seed_vectors.json').read_text(encoding='utf-8'))


def seeded(spread='three',**kwargs):
    return dict(schema_version=1,profile=PROFILE,task='symbolic_reading',mode='seeded',spread=spread,
        protocol=PROTOCOL,seed='Future-Tarot-v1',orientation_policy='seeded_reversals')|kwargs


def manual(ids=None,spread='one',**kwargs):
    return dict(schema_version=1,profile=PROFILE,task='symbolic_reading',mode='manual',spread=spread,
        orientation_policy='explicit',cards=ids if ids is not None else [dict(card_id='wands-four',orientation='reversed')])|kwargs


def significator(**kwargs):return dict(card_id='major-11',facing='left',basis='matter')|kwargs


class TarotTests(unittest.TestCase):
    def test_independent_canonical_card_identities(self):
        names=['The Fool','The Magician','The High Priestess','The Empress','The Emperor','The Hierophant','The Lovers','The Chariot','Strength','The Hermit',
            'Wheel of Fortune','Justice','The Hanged Man','Death','Temperance','The Devil','The Tower','The Star','The Moon','The Sun','The Last Judgment','The World']
        self.assertEqual(len(ORDER),78);self.assertEqual(len(set(ORDER)),78)
        for n,name in enumerate(names):
            c=card(f'major-{n:02d}');self.assertEqual((c['number'],c['name'],c['arcana']),(n,name,'major'))
        self.assertEqual(card('major-08')['source_name'],'Fortitude')
        ranks=['ace','two','three','four','five','six','seven','eight','nine','ten','page','knight','queen','king']
        for suit in ['wands','cups','swords','pentacles']:
            for i,rank in enumerate(ranks):
                c=card(suit+'-'+rank);self.assertEqual((c['suit'],c['rank'],c['rank_number'],c['arcana']),(suit,rank,i+1,'minor'))

    def test_independent_source_meanings_and_exceptions(self):
        for fixture in FIXTURE['meaning_cases']:
            m=card(fixture['card_id'])['meanings'][fixture['orientation']]
            self.assertEqual(m['page'],fixture['page']);self.assertEqual(m['source_id'],FIXTURE['source_id'])
            for phrase in fixture['contains']:self.assertIn(phrase,m['text'])
        m=card('cups-two')['meanings']['reversed']
        self.assertIn('section4',m['locator']);self.assertIn('primary_section_has_no_reversed_entry_explicit_section4_gap_fill',m['flags'])

    def test_complete_catalog_provenance_and_source_isolation(self):
        self.assertEqual(sum(len(c['meanings']) for c in CARDS.values()),156)
        for c in CARDS.values():
            for o in ['upright','reversed']:
                m=c['meanings'][o];self.assertTrue(m['text']);self.assertTrue(m['symbolic_focus']);self.assertTrue(m['locator']);self.assertTrue(m['rule_id'])
                self.assertEqual(m['coverage'],'direct_source_text');self.assertEqual(m['gloss_coverage'],'source_derived_editorial_keywords')
        self.assertEqual(sum(c['additional_meanings'] is not None for c in CARDS.values()),56)
        for p in ['Thoth','Marseille','Etteilla','waite-1910']:
            with self.assertRaises(ValueError):read(seeded(profile=p))

    def test_immutable_catalog_and_output_copy(self):
        with self.assertRaises(TypeError):CARDS['major-00']['name']='changed'
        with self.assertRaises(TypeError):CARDS['major-00']['meanings']['upright']['text']='changed'
        c=card('major-00');c['meanings']['upright']['text']='changed'
        self.assertNotEqual(card('major-00')['meanings']['upright']['text'],'changed')

    def test_independent_dotnet_known_answer_vectors(self):
        self.assertEqual(len(VECTORS['vectors']),6)
        for v in VECTORS['vectors']:
            s=Stream(v['seed'],'deck');words=[s.word() for _ in range(8)]
            self.assertEqual(''.join(f'{w:08x}' for w in words),v['deck_first_block'])
            o=Stream(v['seed'],'orientation');self.assertEqual(''.join(f'{o.word():08x}' for _ in range(8)),v['orientation_first_block'])
            ids=[str(i) for i in range(78) if i!=v['removed_index']]
            pack,trace=shuffle_pack(ids,v['seed'],rounds=v['rounds'],cut=v['rounds']==3)
            self.assertEqual([int(k) for k in pack],v['permutation']);self.assertEqual(trace['cuts'],v['cuts'])
            self.assertEqual([int(x=='reversed') for x in orientations(v['seed'],10,'seeded_reversals')],v['orientation_bits'])

    def test_rejection_sampling_boundaries_and_equal_residue_counts(self):
        s=Stream('x','deck');words=iter([SIZE-1,SIZE-2]);s.word=lambda:next(words)
        self.assertEqual(s.below(3),2);self.assertEqual(s.rejections,1)
        s=Stream('x','deck');words=iter([SIZE-6,SIZE-7]);s.word=lambda:next(words)
        self.assertEqual(s.below(10),9);self.assertEqual(s.rejections,1)
        s=Stream('x','deck');s.word=lambda:SIZE-1
        self.assertEqual(s.below(SIZE),SIZE-1);self.assertEqual(s.below(1),0)
        for n in [3,7,10,77,78]:
            limit=SIZE-SIZE%n;self.assertEqual(limit%n,0)
            # Every residue occurs equally often among accepted32-bit integers.
            self.assertEqual({(limit-1-r)//n+1 for r in range(n)},{limit//n})
        for n in [0,-1,True,1.5,SIZE+1]:
            with self.assertRaises(ValueError):s.below(n)

    def test_unicode_seed_encoding_and_validation(self):
        self.assertNotEqual(seed_bytes('Café'),seed_bytes('Cafe\u0301'))
        self.assertNotEqual(shuffle_pack(list(ORDER),'Café')[0],shuffle_pack(list(ORDER),'Cafe\u0301')[0])
        for v in ['',None,123,True,'é'*129,'\ud800']:
            with self.assertRaises(ValueError):seed_bytes(v)
        self.assertEqual(len(seed_bytes('é'*128)),256)
        with self.assertRaises(ValueError):Stream('x','unknown')

    def test_permutation_no_replacement_and_removed_significator(self):
        for seed in ['x','y','z','test0','test1']:
            pack,_=shuffle_pack(list(ORDER),seed);self.assertEqual(set(pack),set(ORDER));self.assertEqual(len(pack),78)
            r=read(seeded('waite_celtic',seed=seed,significator=significator()))
            self.assertNotIn('major-11',r['replay']['shuffled_pack']);self.assertEqual(len(r['replay']['shuffled_pack']),77)
            self.assertEqual(len({x['card']['id'] for x in r['readings']}),10)

    def test_orientation_stream_independence(self):
        a=read(seeded());b=read(seeded(orientation_policy='upright_only'))
        self.assertEqual(a['replay']['shuffled_pack'],b['replay']['shuffled_pack'])
        self.assertEqual([r['card']['id'] for r in a['readings']],[r['card']['id'] for r in b['readings']])
        self.assertTrue(all(r['orientation']=='upright' for r in b['readings']))

    def test_full_replay_known_protocol(self):
        for q in [seeded('one'),seeded(positions=['Situation','Challenge','Reflection']),seeded('waite_celtic',significator=significator())]:
            r=read(q);self.assertEqual(r,read(r['replay']['request']))
            self.assertEqual(r['replay']['canonical_order_sha256'],hashlib.sha256('\n'.join(ORDER).encode()).hexdigest())
        with self.assertRaises(ValueError):read(seeded(protocol='future-cards-sha256-fy-v2'))

    def test_one_three_and_manual_orientations(self):
        r=read(manual());self.assertEqual(r['readings'][0]['orientation'],'reversed')
        self.assertIn('unaltered',r['readings'][0]['direct_component']['text']);self.assertIsNotNone(r['readings'][0]['upright_reference'])
        self.assertIsNone(r['replay']['seed']);self.assertEqual(r,read(r['replay']['request']))
        r=read(manual([dict(card_id='major-00'),dict(card_id='major-08'),dict(card_id='major-11')],spread='three',orientation_policy='upright_only',positions=['A','B','C']))
        self.assertEqual([x['position']['label'] for x in r['readings']],['A','B','C'])
        self.assertTrue(all(x['position']['coverage']=='editorial_application_layout' for x in r['readings']))

    def test_historical_celtic_positions_facing_and_crosswise_orientation(self):
        a=read(seeded('waite_celtic',significator=significator()));b=read(seeded('waite_celtic',significator=significator(facing='right')))
        self.assertEqual([x['position']['id'] for x in a['readings']],FIXTURE['celtic_positions'])
        self.assertEqual([a['readings'][i]['position']['placement'] for i in [4,5]],['right','left'])
        self.assertEqual([b['readings'][i]['position']['placement'] for i in [4,5]],['left','right'])
        self.assertEqual(a['readings'][1]['position']['placement'],'crosswise_cover')
        self.assertEqual(a['readings'][1]['orientation'],a['replay']['cards'][1]['orientation'])
        self.assertEqual(a['readings'][9]['position']['placement'],'staff_right_top')
        self.assertEqual(a['replay']['shuffle']['rounds'],3);self.assertEqual(len(a['replay']['shuffle']['cuts']),3)
        self.assertEqual(a['significator']['selection']['card_id'],FIXTURE['source_example']['card_id'])

    def test_source_follow_up_option_never_auto_redraws(self):
        ids=[dict(card_id=f'major-{i:02d}',orientation='upright') for i in range(9)]+[dict(card_id='cups-queen',orientation='upright')]
        r=read(manual(ids,'waite_celtic',significator=significator()))
        self.assertTrue(r['follow_up']['option_applicable']);self.assertFalse(r['follow_up']['automatic_redraw'])
        self.assertEqual(r['follow_up']['proposed_significator'],'cups-queen');self.assertEqual(len(r['readings']),10)
        ids[-1]=dict(card_id='major-10',orientation='upright')
        r=read(manual(ids,'waite_celtic',significator=significator(),final_card_uncertain=True))
        self.assertTrue(r['follow_up']['option_applicable']);self.assertFalse(r['follow_up']['final_court_card'])

    def test_alternatives_and_composition_are_explicit(self):
        r=read(manual([dict(card_id='major-17',orientation='upright')]))
        self.assertIn('alternative_or_conflicting_source_readings',r['readings'][0]['ambiguity'])
        self.assertEqual(r['overall']['coverage'],'compositional');self.assertFalse(r['overall']['source_card_pair_rules_applied'])
        r=read(manual());self.assertFalse(r['readings'][0]['additional_account_applied'])
        self.assertIn('children',r['readings'][0]['additional_source_account']['text'])
        self.assertFalse(r['factual_prediction'])

    def test_question_is_context_not_card_or_fact_inference(self):
        a=read(seeded());b=read(seeded(question='Will I certainly win?'))
        self.assertEqual(a['readings'],b['readings']);self.assertEqual(a['overall'],b['overall'])
        self.assertIn('not used',b['question_usage'])

    def test_unknown_duplicates_and_conflicting_manual_inputs(self):
        bad=[manual([dict(card_id='unknown',orientation='upright')]),manual([dict(card_id='major-00',orientation='unknown')]),
            manual([dict(card_id='major-00',orientation='reversed')],orientation_policy='upright_only'),
            manual([dict(card_id='major-00',orientation='upright')]*3,spread='three'),manual(seed='x'),
            seeded(cards=[]),seeded('waite_celtic'),seeded('one',significator=significator()),seeded('three',positions=['A','A','B'])]
        bad += [seeded('waite_celtic',significator=significator(basis='person_manual')),
            seeded('waite_celtic',significator=significator(card_id='cups-queen',basis='matter'))]
        for value in bad:
            with self.assertRaises(ValueError):read(value)
        self.assertEqual(read(seeded('waite_celtic',significator=significator(card_id='cups-queen',basis='person_manual')))['significator']['card']['id'],'cups-queen')
        ids=[dict(card_id=k,orientation='upright') for k in list(ORDER)[2:12]]
        with self.assertRaises(ValueError):read(manual(ids,'waite_celtic',significator=significator()))

    def test_invalid_schema_and_assessment_claims(self):
        for q in [seeded(schema_version=True),seeded(task='diagnosis'),seeded(spread='thoth'),seeded(seed=5),seeded(question=''),
            seeded(photo='person.jpg'),seeded(prediction_score=0.9),seeded('waite_celtic',significator=significator(facing='automatic'))]:
            with self.assertRaises(ValueError):read(q)

    def test_invalid_sampling_settings(self):
        for pack in [[],['x','x'],['x',3]]:
            with self.assertRaises(ValueError):shuffle_pack(pack,'x')
        for kw in [dict(rounds=True),dict(rounds=2),dict(cut='yes')]:
            with self.assertRaises(ValueError):shuffle_pack(['a','b'],'x',**kw)
        with self.assertRaises(ValueError):shuffle_pack(['a'],'x',cut=True)
        with self.assertRaises(ValueError):orientations('x',-1,'seeded_reversals')
        with self.assertRaises(ValueError):orientations('x',1,'explicit')

    def test_duplicate_nonfinite_and_bom_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'input.json')
            for text in ['{"a":1,"a":2}','{"x":NaN}','{"x":Infinity}']:
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):load_input(p)
            p.write_text(json.dumps(seeded()),encoding='utf-8-sig');self.assertEqual(load_input(p),seeded())

    def test_registry_immutable_source_provenance(self):
        r=Registry()
        try:
            register_knowledge(r);register_knowledge(r)
            rows=[json.loads(x[0]) for x in r.db.execute('select record from rules')]
            self.assertEqual(len(rows),213);self.assertTrue(all(x['source_id']==FIXTURE['source_id'] and x['status']=='proposed' and x['evidence_kind']=='traditional' for x in rows))
        finally:r.close()

    def test_json_markdown_reproducibility(self):
        q=seeded(question='<script> | scene')
        a=read(q);self.assertEqual(json.dumps(a,sort_keys=True),json.dumps(read(q),sort_keys=True));self.assertEqual(markdown(a),markdown(read(q)))
        self.assertIn('&lt;script&gt; &#124;',markdown(a));self.assertIn('compositional',markdown(read(seeded('waite_celtic',significator=significator()))))


if __name__=='__main__':unittest.main()
