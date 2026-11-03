import copy
import json
import tempfile
import unittest
from pathlib import Path
from future.palmistry import read,validate,markdown,load_observations,register_knowledge,PROFILE,DATA
from future.__main__ import load_registry


def observation(hand=None):
    return dict(schema_version=1,profile=PROFILE,dominance='right',hands=[dict(side='right',**(hand or {}))])


def ids(report):
    return {r['id'] for h in report['hands'] for r in h['readings']}


class PalmistryTests(unittest.TestCase):
    def test_published_illustrated_source_details(self):
        fixtures=json.loads(Path('tests/fixtures/palmistry_cheiro_examples.json').read_text())
        self.assertEqual(fixtures['scan_sha256'],DATA['source']['sha256'])
        for case in fixtures['cases']:
            with self.subTest(case=case['id']):
                r=read(observation(case['observation']))
                self.assertEqual(ids(r),set(case['expected_ids']))
                self.assertTrue(all(x['source_id']==fixtures['source_id'] and x['locator'] for x in r['hands'][0]['readings']))
                text=' '.join(x['text'].lower() for x in r['hands'][0]['readings'])
                # Independently transcribed source themes, not expectations exported by the matcher.
                terms={'cheiro-plateII':['order','method'],'cheiro-plateIII':['action','independence'],
                       'cheiro-plateV':['artistic','impuls'],'cheiro-XVIII-c':['ambition','position'],
                       'cheiro-XVI-d':['caution','sensitivity'],'cheiro-XVI-j':['sincerity','enthusiasm']}
                self.assertTrue(all(term in text for term in terms[case['id']]))

    def test_independently_transcribed_head_variations_and_exceptions(self):
        # Direct source pp88-89, not production-derived expectations.
        cases=[({'curvature':'straight','clarity':'clear','continuity':'unbroken'},'head.straight'),
               ({'curvature':'straight_then_sloping'},'head.balanced'),
               ({'curvature':'slight_slope'},'head.sloping'),({'curvature':'very_sloping'},'head.very_sloping'),
               ({'length':'short'},'head.short'),({'length':'very_long','curvature':'straight'},'head.long'),
               ({'continuity':'chained'},'head.chained'),({'branches':'upward'},'head.branches')]
        for features,expected in cases:
            r=read(observation(dict(lines=dict(head=dict(presence='present',**features)))))
            self.assertIn('palm.cheiro.'+expected,ids(r))
            self.assertTrue(r['hands'][0]['readings'][0]['exceptions'])
        # Straight by itself does not establish the source's clear/even conditions.
        r=read(observation({'lines':{'head':{'presence':'present','curvature':'straight'}}}))
        self.assertNotIn('palm.cheiro.head.straight',ids(r))

    def test_life_relations_and_no_longevity_inference(self):
        for gap in ('joined','medium','wide'):
            h=dict(head_life_gap=gap,lines=dict(head=dict(presence='present'),life=dict(presence='present',length='short',continuity='broken',depth='shallow')))
            r=read(observation(h));self.assertEqual(ids(r),{'palm.cheiro.life.gap.'+gap})
            self.assertTrue(r['hands'][0]['unsupported_observations'])
        r=read(observation(dict(lines=dict(life=dict(presence='present',origin='jupiter_base')))))
        self.assertIn('palm.cheiro.life.jupiter_origin',ids(r))

    def test_heart_variations_and_located_branches(self):
        for origin in ('jupiter','between_jupiter_saturn','saturn'):
            r=read(observation({'lines':{'heart':{'presence':'present','origin':origin}}}))
            self.assertEqual(ids(r),{'palm.cheiro.heart.origin.'+origin})
        for field,value,expected in [('continuity','broken','broken'),('continuity','chained','chained'),
            ('fork','small_jupiter','small_fork'),('fork','jupiter_and_between','balanced_fork'),('fork','jupiter_and_saturn','wide_fork')]:
            r=read(observation({'lines':{'heart':{'presence':'present',field:value}}}))
            self.assertEqual(ids(r),{'palm.cheiro.heart.'+expected})
        for direction in ('upward','downward'):
            r=read(observation({'lines':{'heart':{'presence':'present','branches':direction}}}))
            self.assertEqual(ids(r),set())
            r=read(observation({'lines':{'heart':{'presence':'present','branches':direction,'branch_position':'commencement'}}}))
            self.assertEqual(ids(r),{'palm.cheiro.heart.'+direction})

    def test_all_supported_mount_locations_and_no_inverse_meanings(self):
        for mount,location in [('venus','thumb'),('jupiter','index'),('saturn','middle'),('sun','ring'),('mercury','little'),
                               ('mars_active','Jupiter'),('mars_passive','Mercury'),('luna','Venus')]:
            self.assertIn(location,DATA['mounts'][mount]['location'])
            for prominence in ('developed','flat','excessive','unknown','uncertain'):
                r=read(observation({'mounts':{mount:{'prominence':prominence}}}))
                self.assertEqual(ids(r),{'palm.cheiro.mount.'+mount} if prominence=='developed' else set())

    def test_shapes_measurements_and_no_automatic_classification(self):
        for shape in ('square','spatulate','philosophic','conic','psychic','mixed'):
            r=read(observation(dict(shape=dict(type=shape),proportions_mm=dict(palm_length=100,palm_width=80,middle_finger_length=90))))
            self.assertIn('palm.cheiro.shape.'+shape,ids(r))
            self.assertEqual(r['hands'][0]['measurement_ratios']['palm_length_over_palm_width'],1.25)
        r=read(observation(dict(proportions_mm=dict(palm_length=100,palm_width=100))))
        self.assertEqual(ids(r),set())

    def test_left_right_dominance_and_comparison(self):
        for dominance in ('right','left','ambidextrous','unknown'):
            o=observation(dict(shape=dict(type='square')));o['dominance']=dominance
            o['hands'].append(dict(side='left',shape=dict(type='conic')))
            r=read(o)
            self.assertFalse(r['hand_use']['dominance_reversal_applied'])
            self.assertEqual(r['hands'][0]['source_role'],'natural/inherited context')
            self.assertEqual(r['hands'][1]['source_role'],'acquired/training context')
            self.assertIn(dict(path='shape.type',left='conic',right='square'),r['observed_hand_differences'])

    def test_unknown_uncertain_absent_and_missing(self):
        for presence in ('absent','unknown','uncertain'):
            r=read(observation({'lines':{'head':{'presence':presence,'curvature':'slight_slope'}}}))
            self.assertEqual(ids(r),set())
        r=read(observation());self.assertFalse(ids(r));self.assertTrue(r['hands'][0]['unknown_core_observations'])
        o=observation({'shape':{'type':'uncertain'},'mounts':{'sun':{'prominence':'uncertain'}}})
        self.assertEqual(ids(read(o)),set())

    def test_contradictions_withheld_and_symbolic_tensions_retained(self):
        r=read(observation(dict(shape=dict(type='square'),lines=dict(head=dict(presence='present',curvature='slight_slope'),
            heart=dict(presence='absent',origin='jupiter')))))
        h=r['hands'][0]
        self.assertNotIn('palm.cheiro.heart.origin.jupiter',ids(r))
        self.assertTrue(h['observation_conflicts']);self.assertTrue(h['interpretive_tensions'])
        self.assertIn('palm.cheiro.shape.square',ids(r));self.assertIn('palm.cheiro.head.sloping',ids(r))
        for line in [dict(presence='present',fork='small_jupiter',branches='none')]:
            r=read(observation(dict(lines=dict(heart=line))))
            self.assertFalse(ids(r));self.assertTrue(r['hands'][0]['observation_conflicts'])
        r=read(observation(dict(lines=dict(heart=dict(presence='present',origin='saturn',fork='small_jupiter')))))
        self.assertFalse(ids(r));self.assertTrue(r['hands'][0]['observation_conflicts'])
        r=read(observation(dict(lines=dict(life=dict(presence='present',branch_to='jupiter',branches='downward')))))
        self.assertFalse(ids(r));self.assertTrue(r['hands'][0]['observation_conflicts'])

    def test_invalid_values_and_schema_boundaries(self):
        malformed=[None,[],dict(),observation()|dict(schema_version=True),observation()|dict(profile='Benham'),
            observation()|dict(hands=[]),observation()|dict(hands=[dict(side='right'),dict(side='right')]),
            observation()|dict(hands=[dict(side='unknown')]),
            observation(dict(shape=dict(type='fire'))),observation(dict(lines=dict(head=dict(presence=True)))),
            observation(dict(mounts=dict(venus=dict(prominence=100)))),observation(dict(markings='star')),
            observation(dict(proportions_mm=dict(palm_width=0))),observation(dict(proportions_mm=dict(palm_width=float('nan')))),
            observation(dict(proportions_mm=dict(palm_width=True))),observation(dict(unknown_feature='bad'))]
        for o in malformed:
            with self.subTest(value=o),self.assertRaises(ValueError):read(o)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'bad.json')
            for text in ['{"schema_version":1,"schema_version":2}','{"x":NaN}']:
                p.write_text(text)
                with self.assertRaises(ValueError):load_observations(p)

    def test_profile_provenance_isolation_and_registry_immutability(self):
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            o=observation(dict(shape=dict(type='square')));r=read(o,registry)
            self.assertEqual(registry.select_rules(8,'Hand shape','Benham'),[])
            self.assertEqual(r['source']['id'],'palmistry-cheiro-ninth-scan-v1')
            self.assertTrue(all(x['profile']==PROFILE and x['locator'] for x in DATA['rules']))
            # Traditional symbolic rules are not computational/empirical verification claims.
            row=registry.db.execute('SELECT record FROM rules WHERE id=?',('palm.cheiro.shape.square',)).fetchone()
            self.assertEqual(json.loads(row['record'])['evidence_kind'],'traditional')
        finally:registry.close()

    def test_json_markdown_reproducibility_and_no_input_mutation(self):
        o=observation(dict(shape=dict(type='square'),markings=['unverified star']));before=copy.deepcopy(o)
        a=read(o);b=read(o)
        self.assertEqual(o,before);self.assertEqual(json.dumps(a,sort_keys=True),json.dumps(b,sort_keys=True))
        self.assertEqual(markdown(a),markdown(b));self.assertIn('Cheiro associates',markdown(a))
        self.assertIn('Unsupported marking',markdown(a));self.assertIn('palm.cheiro.shape.square',markdown(a))

if __name__=='__main__':unittest.main()
