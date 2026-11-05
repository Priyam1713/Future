import copy,hashlib,json,re,tempfile,unittest
from pathlib import Path
from future import pyromancy as p
from future.knowledge import Registry

FIXTURE=json.loads(Path('tests/fixtures/pyromancy_reference_v1.json').read_text(encoding='utf-8'))
def obs(phenomenon='flame',**kw):return dict(id='o1',phenomenon=phenomenon)|kw
def base(rows=None,**kw):return dict(schema_version=1,profile=p.PROFILE,task='symbolic_candle_observation',mode='manual',observations=rows or [])|kw
def selected(row):return [r['id'] for r in row['cases'] if r['status']=='applicable']
def result(row,**kw):return p.read(base([row],**kw))['observations'][0]
def fixture_row(name):
    f=next(c for c in FIXTURE['cases'] if c['name']==name)
    return obs(f['phenomenon'],attributes=copy.deepcopy(f['attributes']),physical=copy.deepcopy(f['physical']))


class PyromancyTests(unittest.TestCase):
    def test_public_dates_and_witnesses(self):
        for source,f in zip(p.DATA['sources'],FIXTURE['source_witnesses']):
            self.assertEqual(source['published_on'],FIXTURE['publication_date'])
            self.assertEqual(source['snapshot_sha256'],f['sha256']);self.assertEqual(source['snapshot_bytes'],f['bytes'])
            self.assertIn('not verified2020',source['witness'])
    def test_rights_and_locators(self):
        for source in p.DATA['sources']:self.assertEqual(source['ingestion'],'facts_only');self.assertIn('separate rights',source['rights_note'])
        for rule in p.RULES:self.assertEqual(rule['locator'],FIXTURE['source_locators'][rule['case']])
    def test_independent_pre_engine_cases(self):
        for f in FIXTURE['cases']:
            with self.subTest(name=f['name']):self.assertEqual(selected(result(fixture_row(f['name']))),f['expected'])
    def test_missing_source_conditions(self):
        for f in FIXTURE['missing']:
            row=result(obs(f['phenomenon'],attributes=f['attributes'],physical=f['physical']))
            self.assertEqual(next(c for c in row['cases'] if c['id']==f['case'])['status'],'insufficient_evidence')
    def test_conflicts(self):
        for f in FIXTURE['conflicts']:
            self.assertEqual(result(obs(f['phenomenon'],attributes=f['attributes'],physical=f['physical']))['status'],'conflicting_evidence')
    def test_known_cause_prevents_symbolic_application(self):
        row=result(fixture_row('high_known_cause'));self.assertEqual(row['physical_assessment']['status'],'not_applicable');self.assertEqual(selected(row),[])
    def test_possible_cause_prevents_application(self):
        self.assertEqual(result(fixture_row('high_possible_cause'))['status'],'not_applicable')
    def test_no_cause_noticed_not_absence(self):
        row=result(fixture_row('high_no_cause_noticed'));self.assertEqual(row['physical_assessment']['status'],'insufficient_evidence');self.assertFalse(row['physical_assessment']['cause_verified'])
    def test_tall_needs_correction(self):
        row=fixture_row('high_after_correction');row['physical']=dict(explanation='checked_no_issue',correction='not_needed_after_check')
        self.assertEqual(selected(result(row)),[])
    def test_low_sound_no_correction_needed(self):
        self.assertEqual(selected(result(fixture_row('low_sound_no_correction_needed'))),['low_persistent'])
    def test_improvement_different_from_persistence(self):
        self.assertEqual(selected(result(fixture_row('low_improved'))),[])
        self.assertEqual(selected(result(fixture_row('low_after_correction'))),['low_persistent'])
    def test_missing_followup(self):
        row=fixture_row('high_after_correction');row['physical'].pop('after_correction')
        self.assertEqual(result(row)['status'],'insufficient_evidence')
    def test_conflicting_correction(self):
        row=fixture_row('high_after_correction');row['physical']['correction']=['none','reported_completed']
        self.assertEqual(result(row)['status'],'conflicting_evidence')
    def test_summary_does_not_clear_details(self):
        for detail in [dict(wick='carbonized'),dict(draft=True),dict(dressing='excess'),dict(construction='concern')]:
            row=fixture_row('low_sound_no_correction_needed');row['physical'].update(detail)
            self.assertEqual(result(row)['status'],'conflicting_evidence')
    def test_correction_sequence_contradiction(self):
        row=fixture_row('low_sound_no_correction_needed');row['physical']['after_correction']='persisted'
        self.assertEqual(result(row)['status'],'conflicting_evidence')
    def test_upper_vs_full_jar(self):
        self.assertEqual(selected(result(fixture_row('upper_dense'))),['upper_clearing','upper_dense'])
        self.assertEqual(selected(result(fixture_row('full_jar'))),['full_jar_dense'])
    def test_density_unknown_not_invented(self):
        r=result(fixture_row('upper_black'));self.assertEqual(selected(r),['upper_clearing'])
        self.assertEqual(next(c for c in r['cases'] if c['id']=='upper_dense')['status'],'insufficient_evidence')
        self.assertEqual(selected(result(fixture_row('full_unknown_density'))),[])
    def test_light_haze_requires_light_through(self):
        row=fixture_row('upper_light');row['attributes'].pop('light_through_deposit')
        self.assertEqual(selected(result(row)),[])
    def test_upper_clear_required(self):
        self.assertEqual(selected(result(fixture_row('upper_not_clear'))),[])
        row=fixture_row('upper_black');row['attributes'].pop('lower_glass_clear')
        self.assertEqual(result(row)['status'],'insufficient_evidence')
    def test_jar_substrate_required(self):
        self.assertEqual(result(fixture_row('soot_no_jar'))['status'],'insufficient_evidence')
    def test_smoke_ember_lamp_unsupported(self):
        for phenomenon in ('smoke','ember','lamp','flame_color','other','unknown'):
            self.assertEqual(result(obs(phenomenon))['status'],'unsupported')
    def test_flame_and_wax_colors_separate(self):
        row=fixture_row('low_sound_no_correction_needed')|dict(flame_color='blue',wax_color='red')
        r=result(row);self.assertIsNone(r['color_correspondences']);self.assertEqual(r['declared']['wax_color'],'red');self.assertEqual(r['unsupported_symbolic_fields'],['flame_color','wax_color'])
    def test_lamp_documentary_only(self):
        r=p.read(base([obs('lamp')],documentary_reference='pgm_iv_52_87'))
        for k,v in FIXTURE['historical_lamp'].items():self.assertEqual(r['documentary_lamp'][k],v)
        self.assertTrue(r['documentary_lamp']['requested']);self.assertFalse(r['documentary_lamp']['betz_original_checked'])
    def test_safety_hold_all_hazards(self):
        for hazard in FIXTURE['safety']:
            r=p.read(base([fixture_row('high_after_correction')],safety=hazard))
            self.assertTrue(r['safety']['symbolic_hold']);self.assertEqual(r['editorial_synthesis'][0]['accounts'],[]);self.assertIsNone(r['editorial_synthesis'][0]['reflection'])
            self.assertTrue(all(c['displayed_account'] is None for c in r['observations'][0]['cases']))
    def test_row_hazard_holds_whole_session(self):
        a=fixture_row('upper_dense');b=obs('other',id='hazard',safety=dict(overheating=True))
        r=p.read(base([a,b]));self.assertTrue(r['safety']['symbolic_hold']);self.assertEqual(selected(r['observations'][0]),[])
    def test_stopped_no_relighting(self):
        r=p.read(base(safety=dict(stopped=True,unsafe_burning=True)))
        self.assertIn('Keep the reported activity stopped',r['safety']['message'])
    def test_unknown_safety_not_clearance(self):
        r=p.read(base());self.assertFalse(r['safety']['physically_verified']);self.assertIn('not physical verification',r['safety']['message'])
    def test_origins_order_and_sequence(self):
        rows=[obs(id='second',sequence=2),obs('soot',id='fifth',sequence=5,origin='synthetic')]
        r=p.read(base(rows,origin='hypothetical'));self.assertEqual([o['id'] for o in r['observations']],['second','fifth']);self.assertEqual([o['origin'] for o in r['observations']],['hypothetical','synthetic'])
    def test_uncertainty_and_identification_alternatives(self):
        for extra,state in [(dict(uncertainty=True),'insufficient_evidence'),(dict(alternatives=['smoke']),'conflicting_evidence')]:
            row=fixture_row('low_sound_no_correction_needed')|extra;self.assertEqual(result(row)['status'],state)
    def test_verbatim_unicode_whitespace(self):
        text='  Café Café 猫 🕯\r\n\t `````json\n  '
        q=base([obs(observation=text,association=text)],notes=text,context=text)
        r=p.read(q);self.assertEqual(r['replay']['request'],q);self.assertEqual(r['user_notes'],text)
    def test_no_prose_inference(self):
        r=result(obs(observation='high flame after wick correction persisted;no problems'))
        self.assertEqual(r['status'],'insufficient_evidence');self.assertFalse(r['physical_assessment']['cause_verified'])
    def test_empty_missing_and_nulls(self):
        self.assertEqual(p.read(base())['summary']['observations'],0)
        row=obs(attributes=dict(height=None),physical=dict(explanation=None));self.assertEqual(result(row)['status'],'insufficient_evidence')
    def test_no_mutation_profile_immutable(self):
        q=base([fixture_row('upper_dense')]);before=copy.deepcopy(q);r=p.read(q);r['replay']['request']['observations'].clear();self.assertEqual(q,before)
        with self.assertRaises(TypeError):p.DATA['version']=3
    def test_portable_hashes(self):
        q=base();r=p.read(q)
        h=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        self.assertEqual(r['replay']['input_sha256'],h(q));self.assertEqual(r['replay']['profile_sha256'],h(json.loads(Path('knowledge/pyromancy_profile_v1.json').read_text(encoding='utf-8'))))
    def test_markdown_replay_fences(self):
        q=base(notes='```json\n ``` 猫  ');r=p.read(q);m=p.markdown(r)
        match=re.search(r'(`{3,})json\n(.*?)\n\1',m.split('## Exact replay metadata')[1],re.S)
        self.assertEqual(p.read(json.loads(match[2])['request']),r)
    def test_four_evidence_layers_and_offline(self):
        r=p.read(base([fixture_row('upper_dense')]))
        self.assertEqual(set(r['provenance_matrix']),{'direct','user_attributed','editorial','unsupported'})
        self.assertFalse(r['replay']['external_calls']);self.assertFalse(r['replay']['rng']);self.assertFalse(r['replay']['generated_observations'])
    def test_registry_idempotence(self):
        r=Registry()
        try:
            p.register_knowledge(r);p.register_knowledge(r);self.assertEqual(r.db.execute('select count(*) from rules').fetchone()[0],6)
            self.assertEqual({json.loads(x[0])['status'] for x in r.db.execute('select record from rules')},{'proposed'})
        finally:r.close()
    def test_invalid_configurations(self):
        invalid=[base(schema_version=True),base(profile='pamita-book2020'),base(mode='video'),base(seed=1),base(temperature=500),base(origin=[]),
            base([obs(phenomenon='made_up')]),base([obs(id='bad id')]),base([obs(),obs()]),base([obs(sequence=True)]),
            base([obs(sequence=2),obs(id='o2',sequence=1)]),base([obs(attributes=dict(height='very_tall'))]),
            base([obs(physical=dict(draft=1))]),base([obs(physical=dict(explanation=['known','known']))]),base([obs(safety=dict(active_hazard='no'))]),
            base([obs(uncertainty=1)]),base([obs(alternatives=['made_up'])]),base([obs(observation='\x00')]),base(notes='x'*10001),
            base([obs(flame_color='x'*81)]),base(observations=[obs()]*65),base(documentary_reference='perform_rite')]
        for q in invalid:
            with self.subTest(q=q):
                with self.assertRaises(ValueError):p.read(q)
    def test_strict_json_loader(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d,'q.json')
            for text in ['{"x":1,"x":2}','{"x":Infinity}']:
                f.write_text(text)
                with self.assertRaises(ValueError):p.load_input(f)


if __name__=='__main__':unittest.main()
