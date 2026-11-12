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
