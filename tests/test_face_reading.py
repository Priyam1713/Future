import copy
import json
import tempfile
import unittest
from pathlib import Path
from future.face_reading import reference,normalize,load_input,markdown,register_knowledge,DATA,PROFILE
from future.__main__ import load_registry


def manual(rows=None,**orientation):
    return dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',
        orientation=dict(view='frontal',side_frame='subject',mirrored=False)|orientation,
        observations=rows if rows is not None else [dict(region_id='forehead',side='midline',visibility='unknown')])


def example(id):
    return dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='source_example',example_id=id)


class FaceReferenceTests(unittest.TestCase):
    def test_independently_transcribed_region_labels(self):
        fixture=json.loads(Path('tests/fixtures/face_reading_lavater_examples.json').read_text())
        for case in fixture['region_cases']:
            region=case['region_id'];side='both' if region in ('eyes','cheeks') else 'midline'
            r=reference(manual([dict(region_id=region,side=side,visibility='visible')]))
            ref=r['regions'][0]['historical_reference']
            self.assertEqual(ref['historical_term'],case['expected_term'])
            self.assertEqual(ref['locator'],case['expected_locator'])
            self.assertEqual(ref['source_id'],fixture['source_id'])
        self.assertEqual(DATA['regions']['eyes']['source_label'],'eye')
        self.assertIn('eyebrows',DATA['regions']['forehead']['region_description'])

    def test_original_three_labeled_diagrams(self):
        fixture=json.loads(Path('tests/fixtures/face_reading_lavater_examples.json').read_text())
        for case in fixture['illustration_cases']:
            r=reference(example(case['example_id']));e=r['source_example']
            self.assertEqual(e['figure_number'],case['expected_figure'])
            self.assertEqual(e['region_id'],case['expected_region'])
            self.assertEqual(e['geometry']['outline'],case['expected_outline'])
            self.assertEqual(e['geometry']['relative_base'],case['expected_relative_base'])
            self.assertIn(case['expected_page'],e['locator'])
            self.assertTrue(e['reference_only']);self.assertFalse(r['inference_enabled'])
            self.assertIsNone(r['individual_assessment'])

    def test_frontal_viewer_left_right_and_mirroring(self):
        raw=dict(region_id='eyes',side='left',visibility='visible',point=[.2,.4])
        r=reference(manual([raw],side_frame='viewer'))['regions'][0]
        self.assertEqual(r['canonical_subject_side'],'right')
        self.assertAlmostEqual(r['canonical_subject_point'][0],.8)
        r=reference(manual([raw],side_frame='viewer',mirrored=True))['regions'][0]
        self.assertEqual(r['canonical_subject_side'],'left')
        self.assertEqual(r['canonical_subject_point'],[.2,.4])
        for side,mirrored,expected in [('right',False,'left'),('right',True,'right')]:
            row=raw|dict(side=side)
            self.assertEqual(reference(manual([row],side_frame='viewer',mirrored=mirrored))['regions'][0]['canonical_subject_side'],expected)

    def test_subject_frame_and_unknown_mirror_are_not_guessed(self):
        raw=dict(region_id='cheeks',side='left',point=[.1,.7])
        r=reference(manual([raw],mirrored=True))['regions'][0]
        self.assertEqual(r['canonical_subject_side'],'left');self.assertEqual(r['canonical_subject_point'],[.1,.7])
        r=reference(manual([raw],side_frame='viewer',mirrored='unknown'))['regions'][0]
        self.assertEqual(r['canonical_subject_side'],'unknown');self.assertIsNone(r['canonical_subject_point']);self.assertTrue(r['ambiguities'])

    def test_profile_visibility_and_no_frontal_projection(self):
        raw=dict(region_id='eyes',side='right',visibility='visible',point=[.6,.4])
        r=reference(manual([raw],view='left_profile'))
        self.assertTrue(r['observation_conflicts']);self.assertIsNone(r['regions'][0]['canonical_subject_point'])
        r=reference(manual([raw],view='right_profile'))
        self.assertFalse(r['observation_conflicts'])
        r=reference(manual([raw],view='right_profile',side_frame='viewer'))
        self.assertEqual(r['regions'][0]['canonical_subject_side'],'unknown')

    def test_unknown_missing_and_unsupported_regions(self):
        r=reference(manual())
        self.assertEqual(r['regions'][0]['observation_status'],'partial')
        self.assertEqual(len(r['missing_regions']),5)
        r=reference(manual([dict(region_id='ear',side='unknown',visibility='uncertain',geometry=dict(outline='uncertain'))]))
        self.assertEqual(r['regions'][0]['coverage'],'unsupported_region')
        self.assertIsNone(r['regions'][0]['historical_reference'])
        self.assertTrue(r['regions'][0]['unknown_fields'])

    def test_contradictory_and_duplicate_annotations(self):
        a=dict(region_id='cheeks',side='both',visibility='visible',geometry=dict(outline='convex'))
        b=dict(region_id='cheeks',side='left',visibility='visible',geometry=dict(outline='concave'))
        r=reference(manual([a,b]));self.assertTrue(r['observation_conflicts'])
        self.assertTrue(all(x['observation_status']=='conflicting' for x in r['regions']))
        r=reference(manual([a,copy.deepcopy(a)]));self.assertEqual(r['regions'][1]['duplicate_of'],0)
        r=reference(manual([dict(region_id='nose',side='midline',visibility='occluded',markings=['spot'])]))
        self.assertTrue(r['observation_conflicts'])

    def test_observation_variations_cannot_produce_personal_judgments(self):
        refs=[]
        for outline,base,marks in [('straight','narrow',['none']),('convex','broad',['spot']),('concave','intermediate',['crease','line'])]:
            r=reference(manual([dict(region_id='forehead',side='midline',visibility='visible',geometry=dict(outline=outline,relative_base=base),markings=marks)]))
            row=r['regions'][0];refs.append(row['historical_reference'])
            self.assertFalse(row['rule_trace']['geometry_used_for_association'])
            self.assertFalse(row['association_applied_to_individual']);self.assertIsNone(row['individual_assessment'])
        self.assertEqual(refs[0],refs[1]);self.assertEqual(refs[1],refs[2])

    def test_rejects_inference_requests_and_school_mixing(self):
        for task in ('intelligence','honesty','morality','criminality','personality','diagnosis','ethnicity','employment','life_outcomes'):
            with self.subTest(task=task),self.assertRaises(ValueError):reference(manual()|dict(task=task))
        for key in ('personality_score','medical_diagnosis','requested_inference','image_path','person_name'):
            with self.assertRaises(ValueError):reference(manual()|{key:'not allowed'})
        for profile in ('Yap','Bridges','Holcroft','five-elements','12-palaces'):
            with self.assertRaises(ValueError):reference(manual()|dict(profile=profile))

    def test_schema_boundaries_and_strict_json(self):
        rows=[None,{},manual()|dict(schema_version=True),manual()|dict(observations=[]),
              manual()|dict(observations=[dict(region_id='eyes',side='midline')]),
              manual()|dict(observations=[dict(region_id='chin',side='left')]),
              manual([dict(region_id='nose',side='midline',point=[float('nan'),0])]),
              manual([dict(region_id='nose',side='midline',point=[1.01,.5])]),
              manual([dict(region_id='nose',side='midline',point=[True,.5])]),
              manual([dict(region_id='nose',side='midline',markings=['none','spot'])]),
              manual([dict(region_id='nose',side='midline',geometry=dict(intelligence='high'))]),
              example('unknown'),example('lavater-v1-p265-figure-1')|dict(observations=[])]
        for value in rows:
            with self.subTest(value=value),self.assertRaises(ValueError):reference(value)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'input.json')
            for text in ['{"task":"historical_reference","task":"personality"}','{"point":NaN}']:
                p.write_text(text)
                with self.assertRaises(ValueError):load_input(p)

    def test_registry_provenance_and_no_empirical_claim(self):
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            reference(manual(),registry)
            row=registry.db.execute('SELECT record FROM rules WHERE id=?',('face.lavater.region.forehead',)).fetchone()
            r=json.loads(row['record']);self.assertEqual(r['evidence_kind'],'traditional');self.assertFalse(r['parameters']['individual_inference'])
            self.assertEqual(registry.select_rules(9,'historical region reference','Chinese Mian Xiang'),[])
        finally:registry.close()

    def test_reports_reproducibility_and_no_mutation(self):
        o=manual([dict(region_id='nose',side='midline',geometry=dict(outline='convex'))]);before=copy.deepcopy(o)
        a=reference(o);b=reference(o)
        self.assertEqual(o,before);self.assertEqual(json.dumps(a,sort_keys=True),json.dumps(b,sort_keys=True))
        text=markdown(a);self.assertEqual(text,markdown(b))
        self.assertIn('independent of the observed geometry',text)
        self.assertIn('Volume I,Fragment II,p18',text);self.assertIn('face.lavater.region.nose',text)
        self.assertIn('physiognomy',text);self.assertIn('pathognomy',text)

if __name__=='__main__':unittest.main()
