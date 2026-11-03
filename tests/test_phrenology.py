import copy
import json
import tempfile
import unittest
from pathlib import Path
from future.phrenology import DATA, PROFILE, reference, markdown, load_input, register_knowledge
from future.knowledge import Registry

FIXTURE = json.loads(Path('tests/fixtures/phrenology_spurzheim_examples.json').read_text(encoding='utf-8'))


def request(schematic='frontis-frontal', **kwargs):
    return dict(schema_version=1,profile=PROFILE,task='historical_reference',schematic=schematic) | kwargs


def lookup(label, schematic='frontis-frontal'):
    return reference(request(schematic,selections=[dict(label_id=label)]))['results'][0]['entry']


class PhrenologyTests(unittest.TestCase):
    def test_original_legend_and_count(self):
        for key,name in FIXTURE['legend_pairs']:
            e=lookup(key)
            self.assertEqual(e['original_name'],name)
            self.assertEqual(e['number'],int(key) if key.isdigit() else None)
        self.assertEqual(DATA['inventory_count'],dict(numbered=35,unnumbered=2,total=37))
        self.assertNotIn('36',DATA['entries'])

    def test_independent_printed_panel_positions(self):
        for panel,key,name,terms in FIXTURE['diagram_cases']:
            e=lookup(key,panel)
            self.assertEqual(e['original_name'],name)
            self.assertEqual(e['location_status'],'verified_printed_label')
            for word in terms:self.assertIn(word,e['location']['description'])

    def test_panel_absences_and_unverified_anchor(self):
        for panel,key in FIXTURE['panel_absences']:
            e=lookup(key,panel)
            self.assertIsNone(e['location'])
            self.assertNotEqual(e['location_status'],'verified_printed_label')
        for panel in DATA['schematics']:
            self.assertEqual(lookup('dagger',panel)['location_status'],'unverified_anchor')

    def test_orientation_and_edition_isolation(self):
        for panel in DATA['schematics']:
            r=reference(request(panel,selections=[dict(label_id='1')]))
            self.assertIn('unspecified',r['schematic']['orientation'])
        for profile in ['Combe','Gall','spurzheim-1833','spurzheim-1908']:
            with self.assertRaises(ValueError):reference(request(profile=profile,selections=[dict(label_id='1')]))

    def test_documented_names_and_aliases(self):
        for name,key in [('Weight','25'),('COMPARISON','34'),('Vitativeness','dagger'),('*','star')]:
            r=reference(request(selections=[dict(name=name)]))['results'][0]
            self.assertEqual(r['entry']['id'],key)
        self.assertEqual(lookup('25')['original_name'],'Weight and Resistance')

    def test_unknown_ambiguous_and_missing(self):
        r=reference(request(selections=[dict(label_id='36'),dict(name='Conditionality'),dict(candidates=['31','32','unknown'])]))
        self.assertEqual([x['status'] for x in r['results']],['unknown_label','unknown_name','ambiguous'])
        self.assertTrue(all(x['entry'] is None for x in r['results']))
        self.assertEqual(len(r['results'][2]['candidate_references']),2)
        with self.assertRaises(ValueError):reference(request())
        with self.assertRaises(ValueError):reference(request(selections=[{}]))

    def test_conflicting_identifiers_never_choose_winner(self):
        for row in [dict(label_id='23',name='Size'),dict(label_id='unknown',name='Size')]:
            r=reference(request(selections=[row]))['results'][0]
            self.assertEqual(r['status'],'conflict')
            self.assertIsNone(r['entry'])
        r=reference(request(selections=[dict(label_id='24',name='Size')]))
        self.assertEqual(r['results'][0]['status'],'resolved')

    def test_region_browsing_conflicts_and_unknowns(self):
        r=reference(request(region_id='frontal-central-column'))
        self.assertEqual([x['entry']['id'] for x in r['results']],['14','13','34','30','22'])
        self.assertEqual(r['selection_mode'],'browse_software_group')
        r=reference(request('frontis-profile',region_id='frontal-central-column',selections=[dict(label_id='14')]))
        self.assertEqual(r['region_status'],'schematic_conflict')
        self.assertEqual(r['results'][0]['status'],'conflict')
        self.assertEqual(reference(request(region_id='new-region'))['region_status'],'unknown_region')

    def test_personal_inference_and_geometry_rejected(self):
        base=request(selections=[dict(label_id='1')])
        for field,value in [('image','head.jpg'),('measurements',{'width':12}),('person','test'),('geometry',{}),('point',[0.2,0.5])]:
            with self.assertRaises(ValueError):reference(base|{field:value})
        for task in ['personality','intelligence','health','criminality']:
            with self.assertRaises(ValueError):reference(base|dict(task=task))
        with self.assertRaises(ValueError):reference(request(selections=[dict(label_id='1',strength=9)]))

    def test_registry_provenance_and_description_limits(self):
        reg=Registry()
        try:
            register_knowledge(reg);register_knowledge(reg)
            rows=reg.db.execute('SELECT record FROM rules').fetchall()
            self.assertEqual(len(rows),37)
            self.assertTrue(all(json.loads(x[0])['source_id']==FIXTURE['source_id'] for x in rows))
            self.assertEqual(reg.select_rules(10,'historical faculty reference','Combe'),[])
            self.assertEqual(reg.select_rules(10,'historical faculty reference',PROFILE),[])
        finally:reg.close()
        self.assertEqual(sum(e['description_coverage']=='direct_selected_passage_paraphrase' for e in DATA['entries'].values()),15)
        self.assertEqual(lookup('2')['description_coverage'],'legend_category_only')

    def test_strict_input_and_json(self):
        for row in [dict(label_id=1),dict(candidates=['1','1']),dict(name=''),dict(label_id=True)]:
            with self.assertRaises(ValueError):reference(request(selections=[row]))
        for value in [request(selections=[dict(label_id='1')])|dict(schema_version=True),request([],selections=[dict(label_id='1')])]:
            with self.assertRaises(ValueError):reference(value)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'input.json')
            for text in ['{"profile":"one","profile":"two"}','{"value":NaN}']:
                p.write_text(text)
                with self.assertRaises(ValueError):load_input(p)

    def test_json_markdown_reproducibility_and_no_mutation(self):
        v=request(selections=[dict(label_id='34'),dict(candidates=['31','32'])]);original=copy.deepcopy(v)
        first=reference(v);second=reference(v)
        self.assertEqual(first,second);self.assertEqual(v,original)
        self.assertEqual(markdown(first),markdown(second))
        self.assertEqual(json.loads(json.dumps(first)),first)
        self.assertFalse(first['inference_enabled']);self.assertIsNone(first['individual_assessment'])
        self.assertIn('canvas5',markdown(first));self.assertIn('Scientifically discredited',markdown(first))
        self.assertTrue(all(not x['applied_to_individual'] for x in [first['results'][0]['entry'],*first['results'][1]['candidate_references']]))
