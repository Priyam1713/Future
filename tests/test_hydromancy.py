import copy,hashlib,json,re,tempfile,unittest
from pathlib import Path
from future import hydromancy as h
from future.knowledge import Registry
F=json.loads(Path('tests/fixtures/hydromancy_reference_v1.json').read_text(encoding='utf-8'))
W=dict(medium='water',container='dark_bowl',rainwater=True,gaze='soft')
def base(rows=None,**kw):return dict(schema_version=1,profile=h.PROFILE,task='water_observation_reference',mode='manual',session=copy.deepcopy(W),observations=rows or [])|kw
def obs(category='perceived_fogginess',**kw):return dict(id='o1',sequence=1,category=category,basis='subjective')|kw
def case(r,name):return next(x for x in r if x['id']==name)

class HydromancyTests(unittest.TestCase):
 def test_attribution(self):
  self.assertIn(F['excerpt_author'],h.DATA['attribution']);self.assertIn(F['article_author'],h.DATA['attribution']);self.assertIn('Not Donald Tyson',h.DATA['attribution'])
 def test_source_hashes(self):self.assertEqual({s['id']:s['snapshot_sha256'] for s in h.DATA['sources']},F['source_hashes'])
 def test_source_rights(self):
  for s in h.DATA['sources']:self.assertEqual(s['ingestion'],'facts_only');self.assertIn('separate rights',s['rights_note'])
 def test_independent_context_cases(self):
  for name,session,key,state in F['cases']:
   with self.subTest(name=name):self.assertEqual(case(h.read(base(session=session))['session_evaluation'],key)['status'],state)
 def test_independent_observation_cases(self):
  for category,basis,state in F['observations']:
   with self.subTest(category=category,basis=basis):self.assertEqual(h.read(base([obs(category,basis=basis)]))['observations'][0]['status'],state)
 def test_moving_water_not_prohibited(self):
  r=h.read(base(session=W|dict(surface_motion='ripples',observer_undisturbed=True,surface_visible=True)))
  self.assertEqual(case(r['session_evaluation'],'position')['status'],'source_supported')
 def test_oil_not_water(self):
  r=h.read(base([obs()],session=W|dict(medium='oil_on_water')));self.assertEqual(r['observations'][0]['status'],'context_mismatch')
 def test_unknown_not_default(self):self.assertEqual(h.water_context({}),'insufficient_information')
 def test_intense_gaze(self):self.assertEqual(case(h.read(base(session=W|dict(gaze='intense')))['session_evaluation'],'gaze')['status'],'context_mismatch')
 def test_missing_gaze(self):self.assertEqual(h.read(base([obs()],session={k:v for k,v in W.items() if k!='gaze'}))['observations'][0]['status'],'insufficient_information')
 def test_rain_false(self):self.assertEqual(case(h.read(base(session=W|dict(rainwater=False)))['session_evaluation'],'dark_bowl')['status'],'context_mismatch')
 def test_observation_context_override(self):
  r=h.read(base([obs(context=dict(medium='oil_only'))]));self.assertEqual(r['observations'][0]['effective_context']['medium'],'oil_only');self.assertEqual(r['session']['medium'],'water')
 def test_physical_mist_not_fog(self):self.assertEqual(h.read(base([obs('physical_mist',basis='physical')]))['observations'][0]['cases'],[])
 def test_imagination_not_reflection(self):self.assertEqual(h.read(base([obs('reflection',basis='imagined')]))['observations'][0]['status'],'conflicting_evidence')
 def test_no_imagery_valid(self):self.assertEqual(h.read(base([obs('no_imagery',basis='unknown')]))['observations'][0]['status'],'unsupported')
 def test_empty_valid(self):self.assertEqual(h.read(base())['observations'],[])
 def test_uncertainty(self):self.assertEqual(h.read(base([obs(uncertainty=True)]))['observations'][0]['status'],'insufficient_information')
 def test_category_alternatives(self):self.assertEqual(h.read(base([obs(alternatives=['physical_mist'])]))['observations'][0]['status'],'conflicting_evidence')
 def test_unknown_basis(self):self.assertEqual(h.read(base([obs(basis=None)]))['observations'][0]['status'],'insufficient_information')
 def test_no_omens(self):
  r=h.read(base([obs('oil_drops',basis='physical',drop_count=3,color='blue')]))['observations'][0]
  self.assertEqual(r['status'],'unsupported');self.assertFalse(r['physical_or_extraordinary_cause_verified'])
 def test_raw_text_not_classified(self):self.assertEqual(h.read(base([obs('unknown',basis='unknown',description='I see fog with spirits')]))['observations'][0]['status'],'unsupported')
 def test_documentary_requested_only(self):
  self.assertIsNone(h.read(base())['documentary_comparison']);r=h.read(base(documentary_comparison=True))
  self.assertEqual(r['documentary_comparison']['coptic'],F['documentary']);self.assertFalse(r['documentary_reference']['executable'])
 def test_discontinued(self):
  r=h.read(base([obs()],session=W|dict(status='discontinued')));self.assertIsNone(r['editorial_reflection']);self.assertIsNone(r['observations'][0]['cases'][0]['account'])
 def test_discomfort(self):self.assertTrue(h.read(base([obs(discomfort=True)]))['continuation']['display_held'])
 def test_origin_and_order(self):
  r=h.read(base([obs(id='z'),obs(id='a',sequence=3,origin='synthetic')],origin='hypothetical'));self.assertEqual([o['id'] for o in r['observations']],['z','a']);self.assertEqual(r['observations'][1]['origin'],'synthetic')
 def test_timestamp_no_clock(self):
  q=base(session=W|dict(timestamp='2026-11-05T12:00:00+05:30'));self.assertEqual(h.read(q)['session']['timestamp'],q['session']['timestamp'])
 def test_raw_unicode(self):
  text='  Café Café 猫 🌊\r\n\t `````json  ';q=base([obs(description=text,association=text)],notes=text)
  self.assertEqual(h.read(q)['replay']['request'],q)
 def test_hash_portable(self):
  q=base();r=h.read(q);self.assertEqual(r['replay']['input_sha256'],hashlib.sha256(json.dumps(q,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest())
 def test_markdown_replay(self):
  q=base(notes='```json\n 🌊  ');r=h.read(q);m=re.search(r'(`{3,})json\n(.*?)\n\1',h.markdown(r).split('## Exact replay metadata')[1],re.S);self.assertEqual(h.read(json.loads(m[2])['request']),r)
 def test_no_mutation(self):
  q=base([obs()]);before=copy.deepcopy(q);r=h.read(q);r['replay']['request']['observations'].clear();self.assertEqual(q,before)
  with self.assertRaises(TypeError):h.DATA['version']=2
 def test_evidence_layers(self):self.assertEqual(set(h.read(base())['provenance_matrix']),{'direct_source','user_attributed','editorial','unsupported'})
 def test_registry(self):
  r=Registry()
  try:h.register_knowledge(r);h.register_knowledge(r);self.assertEqual(r.db.execute('select count(*) from rules').fetchone()[0],8)
  finally:r.close()
 def test_invalid(self):
  bad=[base(schema_version=True),base(mode='photo'),base(seed=1),base(profile='atkinson-pg43954-guided-journal-v1'),base([obs(sequence=True)]),base([obs(),obs()]),base([obs(basis='spiritual')]),base([obs(drop_count=True)]),base([obs(description='\x00')]),base([obs(uncertainty=1)]),base([obs(context=dict(medium='tea'))]),base(session=W|dict(timestamp='yesterday')),base(session=W|dict(rainwater=1)),base(documentary_comparison='yes'),base(notes='x'*10001)]
  for q in bad:
   with self.assertRaises(ValueError):h.read(q)
 def test_json_loader(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d,'q.json')
   for s in ['{"x":NaN}','{"x":1,"x":2}']:
    p.write_text(s)
    with self.assertRaises(ValueError):h.load_input(p)

if __name__=='__main__':unittest.main()
