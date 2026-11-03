import copy
import json
import tempfile
import unittest
from pathlib import Path
from future.podomancy import DATA,PROFILE,reference,markdown,load_input,register_knowledge
from future.knowledge import Registry

FIXTURE=json.loads(Path('tests/fixtures/podomancy_source_examples.json').read_text(encoding='utf-8'))


def request(rows=None,**kwargs):
    return dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',
        orientation=dict(frame='subject',view='plantar',mirrored=False),
        selections=rows if rows is not None else [dict(entry_id='sole_many_long_lines',side='left')])|kwargs


class PodomancyTests(unittest.TestCase):
    def test_independent_primary_text_entries(self):
        for key,region,view,pages,word in FIXTURE['cases']:
            r=reference(request([dict(entry_id=key,region_id=region,side='both')],orientation=dict(frame='subject',view=view,mirrored=False)))['results'][0]
            self.assertEqual(r['status'],'resolved_reference');e=r['entry']
            self.assertEqual(e['printed_page_markers'],pages);self.assertIn(word,e['source_label'])
            self.assertEqual(e['source_id'],FIXTURE['source_id'])

    def test_source_context_and_qualifications(self):
        r=reference(request());self.assertIn('Anonymous',r['source']['author'])
        self.assertIn('undated',r['source']['edition']);self.assertIn('not inspected',r['source']['verification'])
        self.assertIn('Chapter V',r['results'][0]['entry']['locator'])
        self.assertTrue(all(e['qualifications'] for e in DATA['entries'].values()))
        for key,target in FIXTURE['contrasts']:self.assertEqual(DATA['entries'][key]['cross_references'],[target])

    def test_toe_and_unknown_region_are_unsupported(self):
        for row in [dict(region_id='big_toe',side='left'),dict(entry_id='toe_2',side='right'),dict(region_id='Indian_lotus_mark')]:
            r=reference(request([row]))['results'][0];self.assertEqual(r['status'],'unsupported_reference');self.assertIsNone(r['entry'])
        self.assertEqual(reference(request())['coverage']['toe_rules'],0)

    def test_subject_sides_are_mirror_invariant(self):
        for side in ['left','right']:
            for view in ['plantar','dorsal']:
                values=[]
                for mirrored in [False,True]:
                    row=reference(request([dict(entry_id='foot_thin_lean_soft',side=side)],orientation=dict(frame='subject',view=view,mirrored=mirrored)))['results'][0]
                    self.assertEqual(row['canonical_subject_side'],side);values.append(row['entry'])
                self.assertEqual(values[0],values[1])

    def test_viewer_labels_are_not_guessed(self):
        for view in ['plantar','dorsal']:
            for mirror in [False,True,'unknown']:
                row=reference(request([dict(entry_id='foot_thin_lean_soft',side='left')],orientation=dict(frame='viewer',view=view,mirrored=mirror)))['results'][0]
                self.assertEqual(row['canonical_subject_side'],'unknown');self.assertEqual(row['status'],'partial_reference');self.assertIsNone(row['entry'])

    def test_plantar_dorsal_and_unknown_view(self):
        for view,status in [('plantar','resolved_reference'),('dorsal','view_conflict'),('unknown','partial_reference')]:
            r=reference(request(orientation=dict(frame='subject',view=view,mirrored=False)))['results'][0]
            self.assertEqual(r['status'],status)
        r=reference(request([dict(entry_id='foot_broad_thick_long',side='right')],orientation=dict(frame='subject',view='dorsal',mirrored=False)))
        self.assertEqual(r['results'][0]['status'],'resolved_reference')

    def test_missing_uncertain_and_candidate_sets(self):
        for certainty in ['uncertain','unknown']:
            r=reference(request([dict(entry_id='sole_thin_skin',side='left',certainty=certainty)]))['results'][0]
            self.assertEqual(r['status'],'partial_reference');self.assertIsNone(r['entry'])
        self.assertEqual(reference(request([dict(entry_id='sole_thin_skin')]))['results'][0]['status'],'partial_reference')
        row=reference(request([dict(candidates=['sole_thin_skin','missing'],side='both')]))['results'][0]
        self.assertEqual(row['status'],'ambiguous');self.assertEqual(row['unknown_candidate_ids'],['missing']);self.assertIsNone(row['entry'])
        self.assertEqual(reference(request([dict(region_id='sole',side='both')]))['results'][0]['status'],'ambiguous')

    def test_conflicts_and_invalid_inputs(self):
        r=reference(request([dict(entry_id='sole_thin_skin',region_id='whole_foot',side='both')]))['results'][0]
        self.assertEqual(r['status'],'conflict');self.assertIsNone(r['entry'])
        for rows in [[],[{}],[dict(entry_id=1)],[dict(candidates=['sole_thin_skin','sole_thin_skin'])],[dict(region_id='sole',side='midline')]]:
            with self.assertRaises(ValueError):reference(request(rows))
        with self.assertRaises(ValueError):reference(request(schema_version=True))

    def test_source_profile_and_examples_isolated(self):
        for p in ['Somogyi','Sheehan','Aristotle-ancient','Indian']:
            with self.assertRaises(ValueError):reference(request(profile=p))
        for key in DATA['source_examples']:
            r=reference(dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='source_example',example_id=key))
            self.assertEqual(r['results'][0]['entry']['id'],key)
        with self.assertRaises(ValueError):reference(request(mode='source_example',example_id='sole_thin_skin'))

    def test_personal_inference_and_clinical_inputs_rejected(self):
        for key,value in [('image','feet.jpg'),('measurements',dict(toe_length=3)),('person','test'),('diagnosis','test'),('shape','broad')]:
            with self.assertRaises(ValueError):reference(request()|{key:value})
        for task in ['personality','intelligence','health','criminality','future_outcomes','reflexology']:
            with self.assertRaises(ValueError):reference(request(task=task))
        with self.assertRaises(ValueError):reference(request([dict(region_id='sole',skin_thickness=3)]))

    def test_registry_provenance_and_nonempirical_status(self):
        registry=Registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            rows=[json.loads(r[0]) for r in registry.db.execute('SELECT record FROM rules')]
            self.assertEqual(len(rows),6)
            self.assertTrue(all(r['status']=='proposed' and r['evidence_kind']=='traditional' and r['source_id']==FIXTURE['source_id'] for r in rows))
            self.assertTrue(all(not r['parameters']['individual_inference'] for r in rows))
            self.assertEqual(registry.select_rules(12,'historical foot reference','Somogyi'),[])
        finally:registry.close()

    def test_reproducibility_strict_json_and_no_mutation(self):
        v=request();before=copy.deepcopy(v);a=reference(v);b=reference(v)
        self.assertEqual(v,before);self.assertEqual(a,b);self.assertEqual(markdown(a),markdown(b))
        self.assertEqual(json.loads(json.dumps(a)),a);self.assertFalse(a['inference_enabled']);self.assertIsNone(a['individual_assessment'])
        self.assertIn('No individualized',markdown(a));self.assertIn('299-300',markdown(a))
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'input.json')
            for text in ['{"profile":"one","profile":"two"}','{"n":NaN}']:
                p.write_text(text)
                with self.assertRaises(ValueError):load_input(p)
