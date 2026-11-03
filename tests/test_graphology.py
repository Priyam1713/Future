import copy
import json
import tempfile
import unittest
from pathlib import Path
from future.graphology import DATA,PROFILE,reference,markdown,load_input,register_knowledge
from future.graphology_geometry import measure
from future.knowledge import Registry

FIXTURE=json.loads(Path('tests/fixtures/graphology_source_examples.json').read_text(encoding='utf-8'))
GEOMETRY=json.loads(Path('tests/fixtures/graphology_geometry_examples.json').read_text(encoding='utf-8'))


def request(rows=None,**kwargs):
    return dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',script='latin',writing_direction='ltr',
        observations=rows if rows is not None else [dict(feature='slant',category='inclined')])|kwargs


def geometry(**kwargs):return dict(coordinate_system='cartesian_y_up',units='mm')|kwargs


class GraphologyTests(unittest.TestCase):
    def test_independent_original_definitions(self):
        for feature,category,name,page,fig in FIXTURE['term_cases']:
            row=reference(request([dict(feature=feature,category=category)]))['observations'][0]
            self.assertEqual(row['status'],'resolved_reference');t=row['reference']
            self.assertEqual((t['term'],t['definition_page'],t['figure']),(name,page,fig))
            self.assertEqual(t['source_id'],FIXTURE['source_id']);self.assertFalse(t['applied_to_writer'])

    def test_published_facsimile_captions(self):
        for key,figure,category,page in FIXTURE['caption_cases']:
            r=reference(dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='source_example',example_id=key))
            self.assertEqual(r['source_example']['figure'],figure)
            self.assertEqual(r['observations'][0]['reference']['id'],category)
            self.assertIn('p'+str(page)+',',r['source_example']['locator'])

    def test_context_and_incomplete_interpretations(self):
        r=reference(request([dict(feature='connection',category='juxtaposed')]))
        self.assertEqual(r['observations'][0]['coverage'],'direct')
        self.assertEqual(r['observations'][0]['reference']['interpretation_coverage'],'unsupported')
        self.assertEqual(sum(t['interpretation_coverage']=='direct_selected_ordinary_column' for t in DATA['terms'].values()),20)
        self.assertIn('ABC',r['conventions']['edition'])
        self.assertIn('absence',r['source_cautions'][2]['description'])
        self.assertTrue(all(t['exceptions'] for t in DATA['terms'].values()))

    def test_contradictions_respect_scope(self):
        rows=[dict(feature='slant',category='inclined'),dict(feature='slant',category='reversed')]
        r=reference(request(rows));self.assertEqual(len(r['conflicts']),1)
        self.assertTrue(all(x['status']=='conflict' and x['reference'] is None for x in r['observations']))
        rows[1]['scope']='second_word';self.assertFalse(reference(request(rows))['conflicts'])
        # Rising direction can have a straight path; clear line spacing can coexist with crowded word spacing.
        rows=[dict(feature='baseline_direction',category='ascending'),dict(feature='baseline_path',category='rectilinear'),
              dict(feature='line_spacing',category='clear'),dict(feature='word_spacing',category='crowded')]
        self.assertFalse(reference(request(rows))['conflicts'])

    def test_unknown_and_ambiguous_observations(self):
        rows=[dict(feature='slant'),dict(feature='slant',category=['inclined','missing']),
              dict(feature='shape',category='rounded',certainty='uncertain'),dict(feature='shape',category='vertical'),
              dict(feature='speed',category='fast')]
        r=reference(request(rows));self.assertEqual([x['status'] for x in r['observations']],
            ['unknown_or_uncertain','ambiguous','unknown_or_uncertain','unsupported_category','unsupported_category'])
        self.assertTrue(all(x['reference'] is None for x in r['observations']))

    def test_source_and_script_isolation(self):
        for profile in ['ABC-1929','Saudek','Amend-Ruiz','German-holistic']:
            with self.assertRaises(ValueError):reference(request(profile=profile))
        for script,direction in [('arabic','rtl'),('latin','rtl'),('unknown','unknown')]:
            r=reference(request(script=script,writing_direction=direction))
            self.assertEqual(r['observations'][0]['status'],'unsupported_script_direction')
            self.assertIsNone(r['observations'][0]['reference'])
        with self.assertRaises(ValueError):reference(request(mode='source_example',example_id='figure-18'))

    def test_true_pressure_never_from_appearance(self):
        for evidence in ['not_supplied','image_darkness','physical_dynamic']:
            r=reference(request([dict(feature='stroke_appearance',category='muddy_heavy'),dict(feature='pressure',category='heavy')],pressure_evidence=evidence))
            self.assertEqual(r['pressure']['status'],'unsupported')
            self.assertEqual(r['observations'][0]['status'],'resolved_reference')
            self.assertEqual(r['observations'][1]['status'],'unsupported_category')

    def test_independent_angle_fixtures(self):
        for c in GEOMETRY['angle_cases']:
            r=measure(geometry(baseline=c['baseline'],upstroke=c['upstroke']))
            self.assertAlmostEqual(r['baseline_angle'],c['baseline_angle'],places=10)
            self.assertAlmostEqual(r['slant_from_baseline_normal'],c['slant'],places=10)
            self.assertFalse(r['interpretation_applied'])

    def test_normalized_spacing_and_proportions(self):
        c=GEOMETRY['ratio_case'];r=measure(geometry(spacing={k:c[k] for k in ['x_height','word_gap','letter_gap','line_gap']},
            proportions=dict(x_height=2,ascender_height=4,descender_depth=1)))
        self.assertEqual([r['ratios'][k+'_over_x_height'] for k in ['word_gap','letter_gap','line_gap']],c['expected'])
        self.assertEqual(r['ratios']['ascender_height_over_x_height'],2)
        self.assertEqual(r['ratios']['descender_depth_over_x_height'],0.5)
        self.assertIsNone(r['baseline_angle'])

    def test_geometry_translation_scale_and_invalid_data(self):
        a=measure(geometry(baseline=[[0,0],[4,3]],upstroke=[[0,0],[-3,4]]))
        b=measure(geometry(baseline=[[10,20],[18,26]],upstroke=[[30,40],[24,48]]))
        self.assertEqual(a['baseline_angle'],b['baseline_angle']);self.assertEqual(a['slant_from_baseline_normal'],b['slant_from_baseline_normal'])
        for v in [geometry(baseline=[[0,0],[0,0]]),geometry(baseline=[[0,0],[-1,0]]),geometry(baseline=[[0,0],[1,0]],upstroke=[[0,0],[0,-1]]),
                  geometry(spacing=dict(x_height=0,word_gap=2)),geometry(spacing=dict(x_height=1,word_gap=-1)),
                  geometry(baseline=[[0,0],[float('inf'),1]]),geometry(baseline=[[0,0],[True,1]]),
                  geometry(upstroke=[[0,0],[1,1]]),geometry(baseline=[[0,0],[1,0]],coordinate_system='screen_y_down')]:
            with self.assertRaises(ValueError):measure(v)

    def test_geometry_does_not_select_interpretations(self):
        value=request(geometry=geometry(baseline=[[0,0],[1,0]],upstroke=[[0,0],[1,1]]))
        a=reference(value);value['geometry']['upstroke']=[[0,0],[-1,1]];b=reference(value)
        self.assertEqual(a['observations'],b['observations']);self.assertNotEqual(a['geometry'],b['geometry'])
        self.assertEqual(reference(request([],geometry=geometry(baseline=[[0,0],[1,1]])))['observations'],[])

    def test_personal_medical_employment_and_images_rejected(self):
        for task in ['personality','intelligence','mental_health','criminality','honesty','employment','signature_authentication']:
            with self.assertRaises(ValueError):reference(request(task=task))
        for field,value in [('image','handwriting.png'),('writer','test'),('diagnosis','test'),('employment_role','test')]:
            with self.assertRaises(ValueError):reference(request()|{field:value})
        with self.assertRaises(ValueError):reference(request([dict(feature='slant',category='inclined',personality='test')]))

    def test_registry_provenance_and_no_empirical_validation(self):
        registry=Registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            rows=[json.loads(x[0]) for x in registry.db.execute('SELECT record FROM rules')]
            self.assertEqual(len(rows),23)
            self.assertTrue(all(r['source_id']==FIXTURE['source_id'] and r['status']=='proposed' and r['evidence_kind']=='traditional' for r in rows))
            self.assertEqual(registry.select_rules(13,'historical descriptive terminology','German'),[])
        finally:registry.close()

    def test_strict_json_reproducibility_and_no_mutation(self):
        v=request();before=copy.deepcopy(v);a=reference(v);b=reference(v)
        self.assertEqual(a,b);self.assertEqual(v,before);self.assertEqual(markdown(a),markdown(b));self.assertEqual(json.loads(json.dumps(a)),a)
        self.assertFalse(a['inference_enabled']);self.assertIsNone(a['individual_assessment'])
        self.assertIn('No personal-trait',markdown(a));self.assertIn('canvas84',markdown(a))
        for rows in [[dict(feature='slant',category=['inclined','inclined'])],[dict(feature='slant',category=True)],[]]:
            with self.assertRaises(ValueError):reference(request(rows))
        with self.assertRaises(ValueError):reference(request(schema_version=True))
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'input.json')
            for text in ['{"profile":"a","profile":"b"}','{"x":NaN}']:
                p.write_text(text)
                with self.assertRaises(ValueError):load_input(p)
