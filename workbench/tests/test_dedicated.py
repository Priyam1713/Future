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
 def test_iris_source_label(self):
  from future import iridology
  request=build(15,dict(entry='right-stomach',certainty='selected'))
  result=iridology.reference(request['input']);self.assertIn('STOMACH',str(result));self.assertEqual(request['input']['selections'][0]['eye'],'right')
 def test_oracle_question_and_draw(self):
  from future import oracle
  request=build(17,dict(question='How shall I organize my project?',spread='three'))
  oracle.validate(request['input']);cards,_,_=oracle.draw(request['input']['seed'],3)
  self.assertEqual(len(set(cards)),3);self.assertEqual(request['input']['question'],'How shall I organize my project?')
 def test_iching_six_user_lines(self):
  from future import iching
  a=dict(question='What should I consider?',**{'line'+str(i):'9' for i in range(1,7)})
  result=iching.read(build(18,a)['input'])
  self.assertEqual(result['calculation']['initial']['number'],1);self.assertEqual(result['calculation']['resulting']['number'],2)
 def test_rune_draw_replays(self):
  from future import runes
  q=build(19,dict(question='What resources can I consider?',spread='three'))['input']
  runes.validate(q);a=runes.draw(q['seed'],3);self.assertEqual(a,runes.draw(q['seed'],3));self.assertEqual(len(set(a[0])),3)
 def test_pendulum_rejects_duplicate_calibration(self):
  with self.assertRaises(ValueError):build(20,dict(question='Test question',yes='clockwise',no='clockwise',signal='clockwise',quality='full'))
  q=build(20,dict(question='Test question',yes='clockwise',no='counterclockwise',signal='clockwise',quality='full'))
  from future.pendulum import calibration,interpret_observation
  self.assertEqual(interpret_observation(q['input']['observations'][0],calibration(q['input']['calibration']))['symbolic_response'],'yes')

 def test_scrying_preserves_description(self):
  from future import scrying
  q=build(21,dict(surface='crystal',lighting='Daylight',intention='Observe',kind='subjective_imagery',description='  A pale circle, perhaps reflection.  ',uncertain='yes'))
  self.assertEqual(q['input']['journal'][0]['description'],'  A pale circle, perhaps reflection.  ');self.assertIn('pale circle',str(scrying.read(q['input'])))
 def test_mirror_journal(self):
  from future import mirror
  q=build(22,dict(surface='ordinary_mirror',view='self_reflection_visible',lighting='Daylight',intention='Record notes',kind='subjective_imagery',description='A vague outline',uncertain='yes'))
  r=mirror.read(q['input']);self.assertEqual(r['journal'][0]['user_record']['description'],'A vague outline');self.assertFalse(r['contact_verified'])
 def test_dream_unknown_context_not_invented(self):
  from future import dream
  q=build(23,dict(narrative='I saw a serpent.',motif='serpent'))
  dream.validate(q['input']);self.assertEqual(q['input']['context'],{});self.assertEqual(q['input']['lookups'],['serpent'])
 def test_writing_time_order_and_original(self):
  a=dict(intention='Write freely',writing='The blue door opens.',start='2026-11-12T10:00:00Z',stop='2026-11-12T10:02:00Z',review='yes')
  q=build(24,a);self.assertEqual(q['input']['events'][1]['segment']['text'],a['writing'])
  a['stop']='2026-11-12T09:00:00Z'
  with self.assertRaises(ValueError):build(24,a)
 def test_akashic_explicit_purpose(self):
  from future import akashic
  concept=next(iter(akashic.CONCEPTS));q=build(26,dict(question='What does this source say?',purpose='historical_research',concept=concept))
  akashic.validate(q['input']);self.assertEqual(q['input']['question']['purpose'],'historical_research');self.assertEqual(akashic.lookup(concept)['status'],'source_reference')
 def test_tea_adjacency(self):
  from future import tasseography
  q=build(28,dict(symbol='bird',motion='flying',heading='towards_handle',adjacent='postal_mark',uncertain='no'))
  tasseography.validate(q['input']);self.assertEqual(q['input']['observations'][0]['adjacent_to'],['adjacent']);self.assertEqual(q['input']['observations'][1]['symbol_id'],'postal_mark')
 def test_coffee_typed_attributes(self):
  from future import coffee
  q=build(29,dict(vessel='cup',symbol=next(iter(coffee.SYMBOLS)),dots='3',stain='no'))
  coffee.validate(q['input']);a=q['input']['observations'][0]['attributes'];self.assertEqual(a['dots'],3);self.assertIs(a['stain'],False);self.assertNotIn('humps',a)
 def test_fire_known_physical_conditions(self):
  from future import pyromancy
  q=build(30,{'origin':'reported_real','phenomenon':'flame','attributes.height':'high','physical.draft':'yes','safety.active_hazard':'no'})
  pyromancy.validate(q['input']);row=q['input']['observations'][0];self.assertIs(row['physical']['draft'],True);self.assertIs(row['safety']['active_hazard'],False)
 def test_water_observation_basis(self):
  from future import hydromancy
  q=build(31,dict(origin='reported_real',category='physical_ripples',basis='physical',description='Three ripples',medium='water',container='dark_bowl',rainwater='yes'))
  hydromancy.validate(q['input']);self.assertIs(q['input']['session']['rainwater'],True);self.assertEqual(q['input']['observations'][0]['basis'],'physical')
 def test_air_direction_and_duration(self):
  from future import aeromancy
  q=build(32,dict(origin='reported_real',phenomenon='wind',region='scotland',named_wind_direction='north',light_wind_duration_days='3'))
  aeromancy.validate(q['input']);self.assertEqual(q['input']['observations'][0]['features']['light_wind_duration_days'],3)
 def test_geomancy_user_mothers(self):
  from future import geomancy
  q=build(33,dict(origin='reported_real',mother1='1111',mother2='2222',mother3='1212',mother4='2121'))
  self.assertEqual(q['input']['mothers'],['1111','2222','1212','2121']);self.assertEqual(len(geomancy.chart(q['input']['mothers'])),15)
 def test_stone_exact_geometry(self):
  from future import lithomancy
  q=build(34,dict(stones='lodestone, 0, 0\nonyx, 3, 4',frame='integer-centers-x-right-y-up-v1',origin='reported_real',anchor_x='0',anchor_y='0'))
  self.assertEqual(lithomancy.distance_squared(q['input']['stones'][1]['position'],q['input']['anchor']['position']),25)
 def test_bone_comparison_selection(self):
  from future import osteomancy
  q=build(35,dict(case='9A',second='9B'))
  self.assertEqual(q['input']['task'],'compare');self.assertEqual(osteomancy.compare('9A','9B')['requested_order'],['9A','9B'])
  with self.assertRaises(ValueError):build(35,dict(case='9A',second='9A'))
 def test_bibliomancy_pinned_passage(self):
  from future import bibliomancy
  q=build(36,dict(path='1,1,2,1',radius='0'))
  r=bibliomancy.read(q['input']);self.assertEqual(r['selections'][0]['path'],[1,1,2,1]);self.assertTrue(r['selections'][0]['text']);self.assertEqual(r['selections'][0]['context_after'],[])

 def test_lot_selection(self):
  from future import cleromancy
  q=build(37,dict(mark='gao-alpha',origin='reported_real'))
  r=cleromancy.read(q['input']);self.assertEqual(r['selection']['canonical_id'],'gao-alpha');self.assertFalse(r['selection']['generated'])
 def test_bird_unknowns_preserved(self):
  from future import augury
  q=build(38,dict(bird_label='raven',phenomenon='call'))
  augury.validate(q['input']);r=augury.evaluate(q['input']['observations'][0]);self.assertIsNone(r['empirical_prediction']);self.assertEqual(r['effective_fields']['relative_side'],'unknown')
