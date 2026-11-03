import copy
import json
from pathlib import Path
import tempfile
import unittest
from future.aura import DATA, PROFILE, reference, markdown, load_input, register_knowledge
from future.knowledge import Registry

FIXTURE=json.loads(Path('tests/fixtures/aura_source_examples.json').read_text(encoding='utf-8'))


def request(components=None, **kwargs):
    return dict(schema_version=1,profile=PROFILE,task='symbolic_reference',mode='manual',
        components=components if components is not None else [dict(color='pale_rose')])|kwargs


class AuraTests(unittest.TestCase):
    def test_original_color_key_coordinates_and_labels(self):
        for color,row,col,label in FIXTURE['key_cases']:
            r=reference(request([dict(color=color)]));t=r['components'][0]['reference']
            self.assertEqual(t['key'],dict(row=row,column=col,label=label))
            self.assertEqual(t['source_id'],FIXTURE['source_id'])
            self.assertTrue(t['locator']);self.assertTrue(t['qualifications'])

    def test_independently_transcribed_published_examples(self):
        for key,fig,title,colors,section in FIXTURE['figure_cases']:
            r=reference(dict(schema_version=1,profile=PROFILE,task='symbolic_reference',mode='source_example',example_id=key))
            e=r['source_example'];self.assertEqual((e['figure'],e['title'],e['colors']),(fig,title,colors))
            self.assertIn(section,e['locator']);self.assertIn('Fig'+str(fig),e['locator'])
            self.assertEqual(r['configuration']['coverage'],'direct_published_example')
        r=reference(dict(schema_version=1,profile=PROFILE,task='symbolic_reference',mode='source_example',example_id='figure-9'))
        self.assertIn('selfish affection',r['configuration']['summary'])

    def test_shade_and_mixture_qualifications(self):
        r=reference(request([dict(color=c) for c in ['pale_rose','crimson_brown_grey','deep_grey','pale_grey']]))
        self.assertEqual([x['reference']['motif'] for x in r['components']],
            ['unselfish affection','selfish or grasping affection','the historical motif called depression','fear'])
        self.assertIn('not clinical',r['components'][2]['reference']['qualifications'][0])
        self.assertIsNone(r['individual_assessment'])

    def test_composition_never_fabricates_combined_meaning(self):
        r=reference(request([dict(color='pale_rose'),dict(color='primrose')]))
        self.assertEqual(r['configuration']['coverage'],'compositional')
        self.assertIsNone(r['configuration']['combined_rule'])
        self.assertEqual(r['configuration']['combination_status'],'component_symbols_only_no_combined_rule')
        # Even the same color components as a published illustration do not infer its shape/narrative.
        r=reference(request([dict(color='carmine'),dict(color='brown_grey')]))
        self.assertEqual(r['configuration']['coverage'],'compositional');self.assertIsNone(r['source_example'])

    def test_unknown_ambiguous_and_uncertain_values(self):
        r=reference(request([{},dict(color=None),dict(color=['blue','violet']),dict(color='green',certainty='uncertain'),dict(color='lavender')]))
        self.assertEqual([x['status'] for x in r['components']],['unknown_or_uncertain','unknown_or_uncertain','ambiguous','unknown_or_uncertain','unsupported_color'])
        self.assertTrue(all(x['reference'] is None for x in r['components']))
        r=reference(request([dict(color='black'),dict(color='missing')]))
        self.assertEqual(r['configuration']['coverage'],'partial');self.assertFalse(r['configuration']['complete_component_coverage'])

    def test_exclusive_slot_conflicts_and_multicolor_composition(self):
        r=reference(request([dict(color='pale_rose',slot='center'),dict(color='brown',slot='center')]))
        self.assertEqual(len(r['conflicts']),1);self.assertTrue(all(x['status']=='conflict' for x in r['components']))
        r=reference(request([dict(color='pale_rose',slot='center'),dict(color='brown',slot='edge')]))
        self.assertFalse(r['conflicts']);self.assertEqual(r['configuration']['coverage'],'compositional')

    def test_documentary_contexts_not_layer_or_chakra_mapping(self):
        for context in ['thought_form','mental_body','desire_body']:
            r=reference(request([dict(color='violet',context=context)]));c=r['components'][0]['context_reference']
            self.assertEqual(c['color_layer_assignment'],'unsupported');self.assertTrue(c['locator']);self.assertTrue(c['rule_id'])
        for context in ['crown_chakra','layer_7','Brennan_etheric']:
            r=reference(request([dict(color='violet',context=context)]))
            self.assertEqual(r['components'][0]['status'],'unsupported_context');self.assertIsNone(r['components'][0]['reference'])

    def test_tradition_and_edition_isolation(self):
        for profile in ['brennan','kunz','chakra-colors','leadbeater-1901-calibrated']:
            with self.assertRaises(ValueError):reference(request(profile=profile))
        with self.assertRaises(ValueError):reference(request(mode='source_example',example_id='figure-8'))
        with self.assertRaises(ValueError):reference(dict(schema_version=1,profile=PROFILE,task='symbolic_reference',mode='source_example',example_id='figure-999'))

    def test_subjective_text_does_not_select_or_modify_symbols(self):
        a=reference(request());b=reference(request(subjective_description='I feel blue and fear a diagnosis'))
        self.assertEqual(a['components'],b['components']);self.assertEqual(a['configuration'],b['configuration'])
        self.assertFalse(b['subjective_description']['used_for_inference']);self.assertFalse(b['inference_enabled'])
        self.assertFalse(b['physical_aura_detected']);self.assertIsNone(b['individual_assessment'])

    def test_reject_photos_diagnosis_and_strength(self):
        for field in ['image','photo','rgb','person','aura_strength','spiritual_level','camera','diagnosis']:
            with self.assertRaises(ValueError):reference(request(**{field:'data'}))
        for task in ['aura_detection','personality','health','prediction','healing','spiritual_rank']:
            with self.assertRaises(ValueError):reference(request(task=task))
        with self.assertRaises(ValueError):reference(request([dict(color='violet',brightness=1)]))

    def test_invalid_schema_limits(self):
        bad=[request(components=[]),request(components=[{}]*25),request(schema_version=True),request(mode='automatic'),
            request([dict(color=['blue','blue'])]),request([dict(color=['blue'])]),request([dict(color=3)]),
            request([dict(context=[]) ]),request(subjective_description=''),request([dict(certainty='detected')])]
        for v in bad:
            with self.assertRaises(ValueError):reference(v)

    def test_duplicate_nonfinite_json_and_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'input.json')
            for text in ['{"a":1,"a":2}','{"x":NaN}','{"x":Infinity}']:
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):load_input(p)
            p.write_text(json.dumps(request()),encoding='utf-8-sig');self.assertEqual(load_input(p),request())

    def test_registry_provenance_and_reproducibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Registry(str(Path(tmp,'registry.sqlite')))
            try:
                register_knowledge(r);register_knowledge(r)
                records=[json.loads(x[0]) for x in r.db.execute('SELECT record FROM rules')]
                self.assertEqual(len(records),28);self.assertTrue(all(x['source_id']==FIXTURE['source_id'] for x in records))
                self.assertTrue(all(x['status']=='proposed' and x['evidence_kind']=='traditional' for x in records))
            finally:r.close()
        a=reference(request());a['components'][0]['reference']['motif']='tampered'
        self.assertEqual(reference(request())['components'][0]['reference']['motif'],'unselfish affection')
        v=request(subjective_description='<script>bad</script> | note');v0=copy.deepcopy(v)
        self.assertEqual(markdown(reference(v)),markdown(reference(v)));self.assertEqual(v,v0)
        self.assertIn('&lt;script&gt;',markdown(reference(v)));self.assertIn('&#124;',markdown(reference(v)))
        self.assertIn('No personal assessment',markdown(reference(v)))


if __name__=='__main__':unittest.main()
