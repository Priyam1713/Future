import unittest
from workbench.dedicated import build
from future.face_reading import reference
class DedicatedTests(unittest.TestCase):
 def test_face_user_observation(self):
  request=build(9,dict(region='eyes',view='frontal',frame='viewer',mirrored='no',side='left',visibility='visible',outline='convex'))
  result=reference(request['input'])
  self.assertEqual(result['regions'][0]['canonical_subject_side'],'right')
  self.assertEqual(result['regions'][0]['observation']['geometry']['outline'],'convex')
  self.assertFalse(result['inference_enabled'])
 def test_face_invalid_side(self):
  with self.assertRaises(ValueError):build(9,dict(region='forehead',side='left'))
 def test_phrenology_selected_label(self):
  from future.phrenology import reference
  request=build(10,dict(schematic='frontis-profile',label='2'))
  result=reference(request['input'])
  self.assertIn('Amativeness',str(result));self.assertEqual(request['input']['selections'],[{'label_id':'2'}])
 def test_moleosophy_region_filter(self):
  from future.moleosophy import reference
  request=build(11,dict(region='ear',side='right'))
  result=reference(request['input'])
  self.assertEqual(request['input']['selections'],[{'region_id':'ear','side':'right'}]);self.assertIn('ear',str(result))
 def test_foot_selection_preserves_uncertainty(self):
  from future import podomancy
  entry=next(iter(podomancy.DATA['entries']))
  request=build(12,dict(entry=entry,side='left',view='plantar',certainty='uncertain'))
  result=podomancy.reference(request['input'])
  self.assertEqual(request['input']['selections'][0]['certainty'],'uncertain');self.assertIn('uncertain',str(result))
 def test_handwriting_slant(self):
  from future import graphology
  result=graphology.reference(build(13,dict(direction='ltr',slant='inclined'))['input'])
  row=next(r for r in result['observations'] if r['observation']['feature']=='slant')
  self.assertEqual(row['status'],'resolved_reference');self.assertEqual(row['observation']['category'],'inclined')
 def test_aura_color_selection(self):
  from future import aura
  color=next(iter(aura.DATA['terms']));context=next(iter(aura.DATA['contexts']))
  request=build(14,dict(color=color,context=context,certainty='selected'))
  result=aura.reference(request['input']);self.assertIn(color,str(result));self.assertEqual(request['input']['components'][0]['color'],color)
