import copy
import json
from pathlib import Path
import tempfile
import unittest
from future.iridology import DATA,PROFILE,reference,markdown,load_input,register_knowledge
from future.knowledge import Registry

FIXTURE=json.loads(Path('tests/fixtures/iridology_source_examples.json').read_text(encoding='utf-8'))


def request(rows=None,**kwargs):
    return dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',diagram='frontispiece',view='source_plate_upright',
        selections=rows if rows is not None else [dict(eye='right',label_id='liver')])|kwargs


class IridologyTests(unittest.TestCase):
    def test_independent_original_plate_labels(self):
        for eye,label,text,parent,placement in FIXTURE['cases']:
            r=reference(request([dict(eye=eye,label_id=label)]));t=r['selections'][0]['reference']
            self.assertEqual((t['printed_label'],t['parent_label'],t['placement']),(text,parent,placement))
            self.assertEqual(t['source_id'],FIXTURE['source_id']);self.assertIsNone(t['printed_number'])
            self.assertIn('canvas',t['locator']);self.assertFalse(r['selections'][0]['personal_inference'])

    def test_original_plate_orientation_and_chapter_placements(self):
        for eye,placement in FIXTURE['orientation_cases']:
            r=reference(request([dict(eye=eye,label_id='stomach')]))
            self.assertEqual(r['selections'][0]['placement_on_plate'],placement)
        for label,placement,page in FIXTURE['chapter_cases']:
            t=reference(request([dict(eye='left',label_id=label)]))['selections'][0]['reference']
            self.assertEqual(t['placement'],placement);self.assertIn('p'+str(page),t['locator'])
        self.assertIn('Fifth edition1922',DATA['conventions']['edition'])

    def test_published_schematic_examples_not_patient_cases(self):
        for e in FIXTURE['published_examples']:
            r=reference(dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='source_example',
                diagram='frontispiece',view='source_plate_upright',example_id=e['id']))
            self.assertEqual([x['selection'] for x in r['selections']],e['selections'])
            self.assertEqual(r['coverage']['resolved'],3);self.assertIsNone(r['medical_assessment'])
            self.assertEqual(r['source_example']['example_kind'],'editorial_selection_from_published_diagram')
            self.assertFalse(r['source_example']['historical_patient_case'])
            self.assertIn('canvas6',r['source_example']['locator'])

    def test_cross_eye_asymmetric_labels(self):
        for eye,label in [('left','liver'),('right','spleen'),('right','heart')]:
            r=reference(request([dict(eye=eye,label_id=label)]))
            self.assertEqual(r['selections'][0]['status'],'unsupported_label_for_eye')
            self.assertIsNone(r['selections'][0]['reference'])
        self.assertIn('handedness',DATA['source_cautions'][1]['description'])

    def test_region_lookup_and_conflicting_selections(self):
        r=reference(request([dict(eye='right',region_id='right-liver')]))
        self.assertEqual(r['selections'][0]['reference']['printed_label'],'LIVER')
        for row in [dict(eye='left',region_id='right-liver'),dict(eye='right',label_id='kidney',region_id='right-liver')]:
            r=reference(request([row]));self.assertEqual(r['selections'][0]['status'],'conflict')
            self.assertIsNone(r['selections'][0]['reference']);self.assertTrue(r['selections'][0]['candidate_references'])
        self.assertEqual(reference(request([dict(eye='right',region_id='unverified')]))['selections'][0]['status'],'unsupported_region')

    def test_missing_ambiguous_and_uncertain_selection(self):
        rows=[{},dict(eye='right'),dict(eye='right',label_id=None),dict(eye='right',label_id=['liver','kidney']),
            dict(eye='left',label_id='heart',certainty='uncertain')]
        r=reference(request(rows))
        self.assertEqual([x['status'] for x in r['selections']],['unknown_eye','unknown_or_uncertain','unknown_or_uncertain','ambiguous','unknown_or_uncertain'])
        self.assertTrue(all(x['reference'] is None for x in r['selections']))
        r=reference(request([dict(label_id='kidney')]))
        self.assertEqual(len(r['selections'][0]['candidate_references']),2)

    def test_geometry_hints_cannot_infer_or_change_label(self):
        a=reference(request())
        for clock,band in [('0','pupil'),('3:00','skin'),('12:00','unknown'),('360','boundary')]:
            b=reference(request([dict(eye='right',label_id='liver',clock_position=clock,radial_band=band,sector_id='12R')]))
            self.assertEqual(a['selections'][0]['reference'],b['selections'][0]['reference'])
            self.assertTrue(all(not x['used_for_label_selection'] for x in b['selections'][0]['annotations'].values()))
            self.assertEqual(b['geometry']['status'],'unsupported')
        b=reference(request([dict(eye='right',sector_id='12R',clock_position='5:00')]))
        self.assertEqual(b['selections'][0]['status'],'unsupported_sector');self.assertIsNone(b['selections'][0]['reference'])
        self.assertFalse(b['geometry']['radial_boundary_lookup'])

    def test_source_edition_diagram_and_view_isolation(self):
        for profile in ['Jensen','Deck','Rayid','lindlahr-1919']:
            with self.assertRaises(ValueError):reference(request(profile=profile))
        for diagram in ['fig5','jensen-chart','unknown']:
            with self.assertRaises(ValueError):reference(request(diagram=diagram))
        for view in ['patient','mirror','camera','back_view']:
            with self.assertRaises(ValueError):reference(request(view=view))

    def test_reject_personal_iris_analysis(self):
        for key in ['photo','image','medical_history','patient','health_score','personality','biometrics']:
            with self.assertRaises(ValueError):reference(request(**{key:'sample'}))
        for task in ['diagnosis','screening','treatment','susceptibility','personality','organ_health']:
            with self.assertRaises(ValueError):reference(request(task=task))
        with self.assertRaises(ValueError):reference(request([dict(eye='right',label_id='liver',iris_mark='spot')]))
        r=reference(request());self.assertFalse(r['scientific_validity']['diagnostic_validation'])
        self.assertFalse(r['inference_enabled']);self.assertIsNone(r['individual_assessment'])

    def test_invalid_schema_and_source_override(self):
        bad=[request([]),request([{}]*25),request(schema_version=True),request(mode='automatic'),
            request([dict(eye='camera_left')]),request([dict(label_id=['liver','liver'])]),request([dict(label_id=['liver'])]),
            request([dict(label_id=1)]),request([dict(clock_position=float('nan'))]),request([dict(certainty='diagnosed')]),
            request(mode='source_example',example_id='asymmetric-organ-labels')]
        for value in bad:
            with self.assertRaises(ValueError):reference(value)

    def test_duplicate_nonfinite_and_bom_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'input.json')
            for text in ['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}']:
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):load_input(p)
            p.write_text(json.dumps(request()),encoding='utf-8-sig');self.assertEqual(load_input(p),request())

    def test_registry_provenance_and_no_mutation(self):
        r=Registry()
        try:
            register_knowledge(r);register_knowledge(r)
            rules=[json.loads(x[0]) for x in r.db.execute('select record from rules')]
            self.assertEqual(len(rules),36)
            self.assertTrue(all(x['source_id']==FIXTURE['source_id'] and x['status']=='proposed' and x['evidence_kind']=='traditional' for x in rules))
        finally:r.close()
        a=reference(request());a['selections'][0]['reference']['printed_label']='changed'
        self.assertEqual(reference(request())['selections'][0]['reference']['printed_label'],'LIVER')

    def test_json_markdown_reproducibility_and_escaping(self):
        v=request([dict(eye='right',label_id='liver',clock_position='<script> | test')]);old=copy.deepcopy(v)
        a=reference(v);b=reference(v);self.assertEqual(json.dumps(a,sort_keys=True),json.dumps(b,sort_keys=True))
        self.assertEqual(markdown(a),markdown(b));self.assertEqual(v,old)
        self.assertIn('&lt;script&gt; &#124;',markdown(a));self.assertIn('No personal iris analysis',markdown(a))
        self.assertIn('not validate',markdown(a))


if __name__=='__main__':unittest.main()
