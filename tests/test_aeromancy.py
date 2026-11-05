import copy,hashlib,json,re,tempfile,unittest
from pathlib import Path
from future import aeromancy as a
from future.knowledge import Registry
F=json.loads(Path('tests/fixtures/aeromancy_reference_v1.json').read_text(encoding='utf-8'))
def obs(phenomenon='smoke',**kw):return dict(id='o1',phenomenon=phenomenon)|kw
def base(rows=None,**kw):return dict(schema_version=1,profile=a.PROFILE,task='atmospheric_lore_comparison',mode='manual',observations=rows or [])|kw
def selected(row):return [c['id'] for c in row['cases'] if c['observational_status']=='applicable']
def result(row,**kw):return a.read(base([row],**kw))['observations'][0]
def case(row,name):return next(c for c in row['cases'] if c['id']==name)
def texas(days=5):return dict(named_wind_direction='south',wind_direction_convention='from',dry_weather=True,wind_strength='light',light_wind_duration_days=days,prior_wind_direction='south',prior_wind_strength='strong')

class AeromancyTests(unittest.TestCase):
 def test_edition_hash(self):
  self.assertEqual(a.DATA['source']['snapshot_sha256'],F['sha256'])
  for term in F['edition']:self.assertIn(term,a.DATA['source']['edition'])
 def test_locators(self):
  for key,value in F['locators'].items():self.assertEqual(next(c for c in a.CASES if c['case']==key)['locator'],value)
 def test_attributions(self):
  for key,value in F['attributions'].items():self.assertEqual(next(c for c in a.CASES if c['case']==key)['attribution'],value)
 def test_pre_engine_cases(self):
  for phenomenon,features,expected in F['cases']:
   with self.subTest(features=features):self.assertEqual(selected(result(obs(phenomenon,features=features))),expected)
 def test_regions(self):
  for source,declared,state in F['regions']:self.assertEqual(a.regional(source,declared)['status'],state)
 def test_unknown_region_not_scotland(self):
  r=result(obs(features=dict(smoke_drift_towards='east')))
  self.assertEqual(r['status'],'insufficient_evidence');self.assertTrue(case(r,'smoke_east')['retrieved_by_observations']);self.assertEqual(r['historical_accounts'][0]['regional_status'],'insufficient_evidence')
 def test_region_mismatch_retains_reference(self):
  r=result(obs(features=dict(smoke_drift_towards='east')),region='texas')
  self.assertEqual(r['status'],'not_applicable');self.assertEqual(r['historical_accounts'][0]['attribution'],'Scotland')
 def test_row_region_override(self):self.assertEqual(result(obs(region='scotland',features=dict(smoke_drift_towards='east')),region='texas')['status'],'applicable')
 def test_unknown_source_region_not_worldwide(self):
  r=result(obs('wind',features=dict(named_wind_direction='south',wind_direction_convention='from',wind_continuity='considerable_time')))
  self.assertEqual(case(r,'wing_south')['regional_context']['status'],'source_unspecified');self.assertEqual(case(r,'wing_south')['empirical_validity'],'not_established')
 def test_wind_not_smoke(self):self.assertEqual(selected(result(obs(features=dict(named_wind_direction='east',wind_direction_convention='from')))),[])
 def test_cloud_axis_not_motion(self):self.assertEqual(selected(result(obs('cloud',features=dict(cloud_appearance='hake_shaped',named_wind_direction='south',cloud_motion='rapid')))),[])
 def test_hake_axes(self):
  for axis,key in [('east_west','hake_ew'),('north_south','hake_ns')]:self.assertEqual(selected(result(obs('cloud',features=dict(cloud_appearance='hake_shaped',cloud_axis=axis)))),[key])
 def test_explicit_wind_convention(self):
  features=texas();features.pop('wind_direction_convention');self.assertEqual(case(result(obs('wind',features=features)),'texas_sequence')['observational_status'],'insufficient_evidence')
 def test_texas_duration_not_delay(self):
  self.assertEqual(selected(result(obs('wind',features=texas(5)))),['texas_sequence'])
  self.assertEqual(selected(result(obs('wind',features=texas(6)))),['texas_sequence'])
  self.assertEqual(selected(result(obs('wind',features=texas(4)))),[])
 def test_texas_material_conditions(self):
  for key in ('dry_weather','wind_strength','prior_wind_direction','prior_wind_strength','light_wind_duration_days'):
   f=texas();f.pop(key);self.assertEqual(case(result(obs('wind',features=f)),'texas_sequence')['observational_status'],'insufficient_evidence')
 def test_wing_continuity(self):
  f=dict(named_wind_direction='south',wind_direction_convention='from');self.assertEqual(selected(result(obs('wind',features=f))),[])
  f['wind_continuity']='considerable_time';self.assertEqual(selected(result(obs('wind',features=f))),['wing_south'])
 def test_fleecy_all_conditions(self):
  f=copy.deepcopy(F['cases'][6][1])
  for key in f:
   missing=f.copy();missing.pop(key);self.assertEqual(case(result(obs('cloud',features=missing)),'fleecy_compound')['observational_status'],'insufficient_evidence')
 def test_negation_distinct_missing(self):
  missing=case(result(obs('cloud',features=dict(mackerel_sky=True))),'mackerel_mares');negative=case(result(obs('cloud',features=dict(mackerel_sky=True,mares_tails=False))),'mackerel_mares')
  self.assertEqual(missing['observational_status'],'insufficient_evidence');self.assertEqual(negative['observational_status'],'not_applicable')
 def test_compound_mackerel(self):self.assertIn('mackerel_mares',selected(result(obs('cloud',features=dict(mackerel_sky=True,mares_tails=True)))))
 def test_mackerel_accounts_separate(self):
  r=result(obs('cloud',features=dict(mackerel_sky=True)));self.assertEqual(len(r['competing_accounts']),5);self.assertEqual(len(r['historical_accounts']),5)
  for c in r['cases']:self.assertIsNone(c['calendar_forecast'])
 def test_horizons(self):
  for key,value in F['horizons'].items():self.assertEqual(next(c for c in a.CASES if c['case']==key)['horizon'],value)
 def test_feature_conflict(self):self.assertEqual(result(obs(features=dict(smoke_drift_towards=['east','west'])),region='scotland')['status'],'conflicting_evidence')
 def test_regional_conflict(self):self.assertEqual(result(obs(features=dict(smoke_drift_towards='east')),region=['scotland','texas'])['status'],'conflicting_evidence')
 def test_unknown_alternative(self):self.assertEqual(case(result(obs(features=dict(smoke_drift_towards=['east',None]))),'smoke_east')['observational_status'],'insufficient_evidence')
 def test_uncertainty(self):self.assertEqual(selected(result(obs(features=dict(smoke_drift_towards='east'),uncertainty=True))),[])
 def test_identification_alternatives(self):self.assertEqual(result(obs('cloud',features=dict(mackerel_sky=True),alternatives=['other_shape']))['status'],'conflicting_evidence')
 def test_unsupported(self):self.assertEqual(result(obs('other',description='dragon spirit in a cloud'))['status'],'unsupported')
 def test_no_text_inference(self):self.assertEqual(selected(result(obs(description='Scotland east smoke'))),[])
 def test_reference_only(self):
  r=a.read(base(include_reference_catalog=True));self.assertEqual(len(r['reference_catalog']),13);self.assertEqual(r['observations'],[])
 def test_origin_order_timestamp(self):
  q=base([obs(id='z',sequence=2),obs('wind',id='a',sequence=4,origin='synthetic')],origin='hypothetical',timestamp='2026-11-05')
  r=a.read(q);self.assertEqual([o['id'] for o in r['observations']],['z','a']);self.assertEqual(r['observations'][1]['origin'],'synthetic');self.assertEqual(r['declared_context']['timestamp'],'2026-11-05')
 def test_raw_unicode(self):
  text='  Café Café 猫 ☁\r\n\t `````json  ';q=base([obs(description=text,association=text)],notes=text);self.assertEqual(a.read(q)['replay']['request'],q)
 def test_hash_and_immutability(self):
  q=base();r=a.read(q);self.assertEqual(r['replay']['input_sha256'],hashlib.sha256(json.dumps(q,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest())
  with self.assertRaises(TypeError):a.DATA['version']=3
 def test_no_input_mutation(self):
  q=base([obs(features=dict(smoke_drift_towards=['east','west']))]);before=copy.deepcopy(q);r=a.read(q);r['replay']['request']['observations'].clear();self.assertEqual(q,before)
 def test_markdown_replay(self):
  q=base(notes='```json\n 猫  ');r=a.read(q);m=re.search(r'(`{3,})json\n(.*?)\n\1',a.markdown(r).split('## Exact replay metadata')[1],re.S);self.assertEqual(a.read(json.loads(m[2])['request']),r)
 def test_registry(self):
  r=Registry()
  try:a.register_knowledge(r);a.register_knowledge(r);self.assertEqual(r.db.execute('select count(*) from rules').fetchone()[0],13)
  finally:r.close()
 def test_layers_and_no_forecast(self):
  r=a.read(base());self.assertEqual(set(r['provenance_matrix']),{'direct','user_attributed','editorial','unsupported'});self.assertFalse(r['replay']['rng']);self.assertFalse(r['replay']['external_calls']);self.assertIn('Historical reference only',r['non_forecast'])
 def test_validation(self):
  bad=[base(schema_version=True),base(mode='image'),base(profile='generic_weather'),base(seed=1),base(latitude=5),base([obs(),obs()]),base([obs(sequence=True)]),base([obs(features=dict(wind_direction_convention='to'))]),base([obs(features=dict(light_wind_duration_days=True))]),base([obs(features=dict(elapsed_since_prior_days=5))]),base([obs(features=dict(mackerel_sky=1))]),base([obs(uncertainty=1)]),base([obs(description='\x00')]),base(region='British'),base(timestamp='today'),base(notes='x'*10001),base(include_reference_catalog=1)]
  for q in bad:
   with self.assertRaises(ValueError):a.read(q)
 def test_strict_json(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d,'q.json')
   for text in ['{"x":NaN}','{"x":1,"x":2}']:
    p.write_text(text)
    with self.assertRaises(ValueError):a.load_input(p)

if __name__=='__main__':unittest.main()
