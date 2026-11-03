import copy
import json
import tempfile
import unittest
from pathlib import Path
from future.moleosophy import DATA,PROFILE,reference,markdown,load_input,register_knowledge
from future.knowledge import Registry

FIXTURE=json.loads(Path('tests/fixtures/moleosophy_fontaine_examples.json').read_text(encoding='utf-8'))


def request(selections=None, **kwargs):
    base=dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',
        schematic_id=DATA['schematic']['id'],orientation=dict(frame='subject',view='frontal',mirrored=False),
        selections=selections if selections is not None else [dict(region_id='cheek',side='left')])
    return base|kwargs


def lookup(**row):
    return reference(request([row]))['results'][0]


class MoleosophyTests(unittest.TestCase):
    def test_independent_original_region_entries(self):
        for region,side,location,key,label,pages in FIXTURE['cases']:
            r=lookup(region_id=region,side=side,location_id=location)
            self.assertEqual(r['status'],'resolved')
            self.assertEqual((r['entry']['id'],r['entry']['original_label'],r['entry']['printed_pages']),(key,label,pages))
            self.assertEqual(r['entry']['pdf_pages'],[p+10 for p in pages])

    def test_original_qualifications_and_locators(self):
        for c in FIXTURE['source_assertions']:
            e=lookup(entry_id=c['entry_id'])['entry']
            self.assertIn(c['page'],e['printed_pages'])
            self.assertIn(c['term'],json.dumps(e))
        report=reference(request())
        self.assertIn('p114',report['general_qualifications']['locator'])
        self.assertFalse(report['general_qualifications']['operational'])
        self.assertIn('p115',report['terminology_conflicts'][1])
        self.assertIn('PDF pages',lookup(entry_id='wrist')['entry']['locator'])
        # Front/back is a location distinction,not an original midline-only rule.
        self.assertEqual(lookup(region_id='neck',side='left',location_id='front')['entry']['id'],'neck_front')
        self.assertEqual(lookup(entry_id='neck_back')['entry']['source_side'],'unspecified')
        self.assertEqual(lookup(entry_id='neck_front')['entry']['version'],2)

    def test_left_right_distinctions_not_universal_polarity(self):
        for region in ['eyebrow','knee','shoulder','temple']:
            left=lookup(region_id=region,side='left')['entry'];right=lookup(region_id=region,side='right')['entry']
            self.assertNotEqual(left['id'],right['id'])
        self.assertEqual(lookup(region_id='cheek',side='left')['entry']['id'],lookup(region_id='cheek',side='right')['entry']['id'])
        self.assertIn('mixed',lookup(entry_id='knee_left')['entry']['historical_association'])

    def test_viewer_mirroring_known_frontal_only(self):
        for mirrored,key in [(False,'eyebrow_right'),(True,'eyebrow_left')]:
            r=reference(request([dict(region_id='eyebrow',side='left')],orientation=dict(frame='viewer',view='frontal',mirrored=mirrored)))
            self.assertEqual(r['results'][0]['entry']['id'],key)
        for view,mirror in [('frontal','unknown'),('posterior',False),('unknown',True)]:
            r=reference(request([dict(region_id='eyebrow',side='left')],orientation=dict(frame='viewer',view=view,mirrored=mirror)))['results'][0]
            self.assertEqual(r['status'],'orientation_unresolved');self.assertIsNone(r['entry'])
            self.assertEqual(len(r['candidate_references']),2)

    def test_unknowns_and_missing_location_do_not_guess(self):
        for row,status in [(dict(region_id='new_region'),'unsupported_reference'),(dict(entry_id='new_id'),'unknown_entry'),
            (dict(region_id='eyebrow',side='unknown'),'ambiguous'),(dict(region_id='ear'),'ambiguous'),
            (dict(region_id='eye',location_id='general'),'unsupported_reference')]:
            r=lookup(**row);self.assertEqual(r['status'],status);self.assertIsNone(r['entry'])
        self.assertEqual(lookup(region_id='ear',location_id='lower_tip')['entry']['id'],'ear_lower_tip')

    def test_conflicting_assertions_never_clear_unknowns(self):
        for row in [dict(entry_id='eyebrow_left',region_id='eyebrow',side='right'),dict(entry_id='nose',region_id='chin'),
                    dict(entry_id='new_id',region_id='chin'),dict(entry_id='hand_except_fingers',location_id='finger')]:
            r=lookup(**row);self.assertEqual(r['status'],'conflict');self.assertIsNone(r['entry'])
        r=reference(request([dict(entry_id='eyebrow_right',side='left')],orientation=dict(frame='viewer',view='frontal',mirrored='unknown')))['results'][0]
        self.assertEqual(r['status'],'orientation_unresolved')

    def test_source_cross_references_and_exclusions(self):
        ear=lookup(entry_id='ear_general')['entry'];self.assertEqual(ear['cross_references'],['ear_lower_tip'])
        self.assertIn('exception',ear['qualifications'][0])
        self.assertEqual(lookup(entry_id='forehead_left')['entry']['cross_references'],['eyebrow_left'])
        mouth=lookup(region_id='mouth');self.assertEqual(mouth['entry']['id'],'lips');self.assertIn('p118',mouth['alias_locator'])
        self.assertEqual(lookup(region_id='finger')['status'],'unsupported_reference')
        self.assertIn('overlap',lookup(entry_id='wrist')['entry']['qualifications'][0])

    def test_profile_isolation_and_source_examples(self):
        for profile in ['Yap','Indian','fontaine-gutenberg','fontaine-1862']:
            with self.assertRaises(ValueError):reference(request(profile=profile))
        for key,example in DATA['source_examples'].items():
            r=reference(dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='source_example',example_id=key))
            self.assertEqual(r['results'][0]['entry']['id'],example['entry_id'])
            self.assertEqual(r['source_example'],example)
        with self.assertRaises(ValueError):reference(request(mode='source_example',example_id='original-right-eyebrow'))
        with self.assertRaises(ValueError):reference(request(schematic_id='Chinese-numbered-face'))

    def test_personal_and_medical_inference_rejected(self):
        for key,value in [('image','skin.jpg'),('person','test'),('measurements',dict(size=4)),('diagnosis','melanoma'),('medical_observations',{})]:
            with self.assertRaises(ValueError):reference(request()|{key:value})
        for task in ['medical','character','intelligence','criminality','health','longevity','future_outcomes']:
            with self.assertRaises(ValueError):reference(request(task=task))
        with self.assertRaises(ValueError):reference(request([dict(region_id='cheek',color='dark')]))

    def test_registry_rule_provenance(self):
        r=Registry()
        try:
            register_knowledge(r);register_knowledge(r)
            rows=[json.loads(x[0]) for x in r.db.execute('SELECT record FROM rules')]
            self.assertEqual(len(rows),27)
            self.assertTrue(all(x['source_id']==FIXTURE['source_id'] and x['evidence_kind']=='traditional' and x['status']=='proposed' for x in rows))
            self.assertTrue(all(not x['parameters']['individual_inference'] for x in rows))
            self.assertEqual(r.select_rules(11,'historical mole reference','Yap'),[])
        finally:r.close()

    def test_strict_schema_and_json(self):
        for row in [{},dict(entry_id=1),dict(region_id=True),dict(region_id='cheek',side='viewer_left')]:
            with self.assertRaises(ValueError):reference(request([row]))
        with self.assertRaises(ValueError):reference(request(schema_version=True))
        with self.assertRaises(ValueError):reference(request(orientation=dict(frame='subject',view='frontal',mirrored=1)))
        with self.assertRaises(ValueError):reference(request([]))
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'input.json')
            for text in ['{"profile":"one","profile":"two"}','{"side":NaN}']:
                p.write_text(text)
                with self.assertRaises(ValueError):load_input(p)

    def test_reproducible_json_markdown_without_individual_application(self):
        value=request([dict(entry_id='ear_general'),dict(region_id='eyebrow',side='unknown')]);before=copy.deepcopy(value)
        first=reference(value);second=reference(value)
        self.assertEqual(value,before);self.assertEqual(first,second)
        self.assertEqual(json.loads(json.dumps(first)),first);self.assertEqual(markdown(first),markdown(second))
        self.assertIsNone(first['individual_assessment']);self.assertFalse(first['inference_enabled'])
        self.assertIn('No individual assessment',markdown(first));self.assertIn('printed pp116',markdown(first))
        self.assertTrue(all(not e['applied_to_individual'] for e in [first['results'][0]['entry'],*first['results'][1]['candidate_references']]))
