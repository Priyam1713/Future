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
 def test_organ_source_conditions(self):
  from future import haruspicy
  q=build(39,dict(tradition='roman',organ='liver',feature='liver_head',presence='absent',other_vitals='sound'))
  haruspicy.validate(q['input']);self.assertEqual(q['input']['observations'][0]['presence'],'absent');self.assertTrue(haruspicy.evaluate_all(q['input']['observations']))
 def test_bearing_exact_tenths(self):
  a=dict(degrees='7.5',north='source_diagram',role='source_heading',alternates='7.6')
  q=build(40,a);self.assertEqual(q['input']['bearing_tenths'],75);self.assertEqual(q['input']['alternate_readings'],[76])
  a['degrees']='7.55'
  with self.assertRaises(ValueError):build(40,a)
 def test_remote_training_record_and_rank(self):
  import base64
  from pathlib import Path
  from workbench.remote_intake import ACTIONS
  from future import remote_viewing as rv
  a=dict(study='user-study',trial='user-trial',tasker='tasker',viewer='viewer',judge='judge',holder='Test author',source='Repository-authored test fixtures',permission='yes',target='3',transcript='A shape with lines',report='Candidate three is closest',created='2026-11-13T10:00:00Z',images=[base64.b64encode(Path(f'data/remote-viewing-assets/t{i}.png').read_bytes()).decode() for i in range(1,6)])
  a.update({f'rank{i}':str(v) for i,v in enumerate([2,3,1,4,5],1)})
  a.update({action+'_at':f'2026-11-13T10:{i:02d}:00Z' for i,action in enumerate(ACTIONS,1)})
  q=build(43,a);r=rv.report(q['input']['trial']);self.assertEqual(r['judge_results'][0]['actual_target_rank'],1);self.assertFalse(r['eligible_blinded_scoring'])
 def test_dream_event_ledger(self):
  from workbench.dream_intake import ACTIONS,engine
  a=dict(study='study',participant='person',coordinator='coord',collector='collector',judge='judge',rule='One predefined event record',feature='Observed object',narrative='A red object',detail='red object',event_text='A red sign was reported',evidence='Independent test evidence',holder='Test author',source='Self-authored fixture',reason='Shared color only',permission='yes',known='no',common='no',coverage='complete',rating='match')
  times={'created':0,'slot_open':1,'slot_due':3,'collection_start':0,'collection_end':59,'window_start':4,'window_end':59,'event_start':5,'event_end':5,'discovery':5}
  a.update({k:f'2026-11-13T10:{v:02d}:00Z' for k,v in times.items()})
  a.update({k+'_at':f'2026-11-13T10:{v:02d}:00Z' for k,v in zip(ACTIONS,[2,4,6,7,8,9,10,11,12])})
  q=build(44,a);r=engine.report(q['input']['ledger']);self.assertEqual(r['state'],'reported');self.assertEqual(r['pair_counts']['total'],1);self.assertFalse(r['declared_blind_judging'])
 def test_ordered_cue_decision(self):
  from future import intuitive_prediction as engine
  a=dict(first='a',second='b',criterion='Magnitude',domain='User test',observed='2026-11-13T10:00:00Z',provenance='Declared prior measurements',training='Prior period',cues='cue1, positive, negative, 0.8',practice='User declaration',recognition1='recognized',recognition2='recognized',changed='no')
  q=build(45,a);self.assertEqual(engine.decision(q['input']['decision'])['selected'],'a')
 def test_deja_reve_record_hash_and_compatibility(self):
  from future import deja_reve
  a=dict(pseudonym='p1',source='My journal',narrative='A familiar dream scene',start='2026-11-13T10:00:00Z',end='2026-11-13T10:01:00Z',recorded='2026-11-13T10:02:00Z',locked='2026-11-13T10:03:00Z',reviewer='r1',confidence='Unsure',permission='yes')
  q=build(46,a);r=deja_reve.read(q['input']);self.assertEqual(r['result']['compatibility']['status'],'review_required');self.assertEqual(q['input']['record']['original']['narrative'],a['narrative'])

 def test_quantum_bell_user_circuit(self):
  from future import quantum_probability_forecasting as quantum
  a=dict(qubits='2',gates='h,0\ncx,1,0',event_kind='bitstring',event_value='11',attribution='My circuit')
  q=build(50,a)['input'];r=quantum.read(q)
  self.assertAlmostEqual(r['result']['event']['ideal_model_probability'],0.5)
  a.update(task='sample',shots='1000',seed='123')
  q=build(50,a)['input'];self.assertEqual(quantum.read(q),quantum.read(q))
  a['gates']='cx,0,0'
  with self.assertRaises(ValueError):build(50,a)

 def test_network_user_thresholds(self):
  from future import psychohistory
  a=dict(nodes='a,1/2\nb,1/2\nc,1/2',edges='a,b\nb,c',active='a',rounds='3',snapshot='Hypothetical chain',attribution='My model',synthetic='yes')
  q=build(52,a)['input'];r=psychohistory.read(q)
  self.assertEqual(r['scenarios'][0]['rows'][0]['active_counts'],[1,2,3])
  a['edges']='a,a'
  with self.assertRaises(ValueError):build(52,a)

 def test_twin_user_measurement(self):
  from future import digital_twin
  a=dict(mode='synthetic',asset='motor',state_unit='rpm',measurement_unit='rpm',version='v1',A='1',B='0',H='1',Q='0',R='1',m0='0',P0='1',initial='2026-01-01T00:00:00Z',step='1',evaluation='2026-01-01T00:00:01Z',records='2026-01-01T00:00:01Z,2,0,2026-01-01T00:00:01Z',snapshot='Synthetic test',attribution='My model')
  q=build(53,a)['input'];r=digital_twin.read(q)
  self.assertIn('posterior_mean',str(r));self.assertEqual(digital_twin.predict(0,1,1,0,0,0),(0,1))
  self.assertIn("'posterior_mean': '1'",str(r))
  a['mode']='archival'
  with self.assertRaises(ValueError):build(53,a)

 def test_agent_grid_blinker(self):
  from future import agent_based
  a=dict(grid='00000\n00100\n00100\n00100\n00000',ticks='2',snapshot='My synthetic blinker',attribution='My configuration')
  r=agent_based.read(build(54,a)['input'])['scenarios'][0]
  self.assertEqual(r['period'],2);self.assertEqual(r['initial_grid'],r['final_grid'])
  a['grid']='01\n1'
  with self.assertRaises(ValueError):build(54,a)

 def test_user_feature_classifier(self):
  from future import brain_intention
  a=dict(channels='c1',fit='5',snapshot='Synthetic feature comparison',attribution='My data',synthetic='yes',trials='a,s1,r1,f1,t1,0,1,1,2,2,TRAIN,A,0,0\nb,s1,r1,f1,t2,2,3,3,4,4,TRAIN,B,10,0\nc,s2,r2,f2,t3,6,7,7,8,9,TEST,B,9,0')
  r=brain_intention.read(build(55,a)['input']);self.assertEqual(r['predictions'][0]['prediction'],'B');self.assertEqual(r['evaluation']['accuracy'],'1')
  a['trials']=a['trials'].replace('c,s2,r2','c,s1,r2')
  with self.assertRaises(ValueError):build(55,a)

 def test_user_causal_table(self):
  from future import causal_ai
  a=dict(nodes='X,no,yes\nY,no,yes',edges='X,Y',joint='X,Y,weight\nno,no,3/8\nno,yes,1/8\nyes,no,1/8\nyes,yes,3/8',treatment='X',outcome='Y',value='yes',snapshot='Synthetic intervention model',attribution='My table',assumptions='yes',synthetic='yes')
  r=causal_ai.read(build(56,a)['input']);self.assertEqual(r['interventional']['risks'],{'no':'1/4','yes':'3/4'})
  a['joint']=a['joint'].replace('3/8','1/8')
  with self.assertRaises(ValueError):build(56,a)

 def test_user_forecast_pool(self):
  from future import collective_intelligence as c
  a=dict(question='Will the delivery arrive?',positive='Delivered by deadline',negative='Not delivered by deadline',created='2026-01-01T00:00:00Z',locked='2026-01-01T01:00:00Z',frozen='2026-01-01T02:00:00Z',weights_at='2026-01-01T01:00:00Z',cutoff='2026-01-02T00:00:00Z',end='2026-01-03T00:00:00Z',forecasts='a,g1,1,1/4,2026-01-01T03:00:00Z,2026-01-01T03:00:00Z\nb,g2,1,3/4,2026-01-01T03:00:00Z,2026-01-01T03:00:00Z',snapshot='My elicited forecasts',attribution='Participants with permission',clarity='yes')
  r=c.read(build(57,a)['input']);self.assertIn("'probability': '1/2'",str(r['questions']))
  a['forecasts']=a['forecasts'].replace('1/4','5/4')
  with self.assertRaises(ValueError):build(57,a)

 def test_user_play_market(self):
  from future import prediction_markets as m
  a=dict(question='Will the synthetic event happen?',positive='Event occurs',negative='Event absent',created='2026-01-01T00:00:00Z',close='2026-01-03T00:00:00Z',resolver='judge',liquidity='10',accounts='alice,100',trades='2026-01-02T00:00:00Z,alice,YES,2',snapshot='My play market',attribution='My simulation',synthetic='yes')
  r=m.read(build(58,a)['input']);self.assertEqual(r['counters']['executed_trades'],1);self.assertTrue(r['invariants']['cash_conservation'])
  a['trades']=a['trades'].replace('YES,2','YES,200')
  r=m.read(build(58,a)['input']);self.assertEqual(r['counters']['executed_trades'],0);self.assertGreater(r['counters']['rejected_actions'],0)

 def test_user_lorenz_initial_states(self):
  from future import chaos_theory as c
  a=dict(sigma='10',rho='28',beta='8/3',initial='0,0,0',perturbed='0,0,0',dt='1/100',steps='10',stride='1',snapshot='Equilibrium check',attribution='My conditions')
  r=c.read(build(59,a)['input']);self.assertEqual(r['rows'][-1]['coarse_base'],[0,0,0]);self.assertIsNone(r['diagnostics']['final_refined_amplification'])
  a['dt']='1'
  with self.assertRaises(ValueError):build(59,a)
