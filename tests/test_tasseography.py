import copy,json,re,tempfile,unittest
from pathlib import Path
from future import tasseography as t
from future.__main__ import load_registry

REF=json.loads(Path('tests/fixtures/tasseography_reference_v2.json').read_text(encoding='utf-8'))
EXTRA=json.loads(Path('tests/fixtures/tasseography_context_reference.json').read_text(encoding='utf-8'))


def base(observations=None,**kwargs):
    return dict(schema_version=1,profile=t.PROFILE,task='symbolic_cup_reading',mode='manual',vessel='cup',observations=observations or [])|kwargs


def obs(symbol='anchor',**kwargs):return dict(id='o1',symbol_id=symbol)|kwargs


def selected(result):return [c['reference']['id'] for c in result['cases'] if c['status']=='applicable']


def figure(musician=True):
    rows=[]
    for i,e in enumerate(REF['figure_viii']['placements']):
        row={k:v for k,v in e.items() if k!='beside'};row['id']='o'+str(i);rows.append(row)
    rows[2]['adjacent_to']=['o1']
    return base(rows,source_example='figure_viii',context=dict(musician=musician))


class TasseographyTests(unittest.TestCase):
    def test_01_source_identity_locators(self):
        self.assertEqual(list(t.SYMBOLS),REF['symbols'])
        self.assertEqual({k:v['locator'] for k,v in t.SYMBOLS.items()},REF['locators'])
        self.assertIn('not verified print pagination',t.DATA['source']['edition'])

    def test_02_independent_zone_cases(self):
        for region,expected in REF['cup_zones']:
            z=t.zones(obs(region=region));self.assertEqual(z['qualifications'][0]['association'],expected)
            self.assertIsNone(z['calendar_date'])

    def test_03_handle_overlap_without_priority(self):
        z=t.zones(obs(region='bottom',handle_relation='under_handle'))
        self.assertEqual([x['association'] for x in z['qualifications']],['far_distant','present_immediate'])
        self.assertEqual(z['status'],'conflicting_evidence')

    def test_04_unknown_zone_not_inferred_from_prose(self):
        r=t.read(base([obs(observation='At the rim under the handle')]))
        self.assertEqual(r['observations'][0]['zones']['qualifications'],[])
        self.assertFalse(r['layout']['position_inferred'])

    def test_05_pre_engine_condition_cases(self):
        for c in REF['conditional_cases']:
            r=t.read(base([obs(c['symbol'],**c['fields'])],context=c['context']))
            self.assertEqual(selected(r['observations'][0]),c['applicable'],c)

    def test_06_adjacency_known_answers(self):
        for case in REF['adjacency_cases']:
            first=obs(case['symbols'][0],adjacent_to=['o2'],**case['fields']);second=dict(id='o2',symbol_id=case['symbols'][1])
            r=t.read(base([first,second]));self.assertEqual(selected(r['observations'][0]),case['expected'])

    def test_07_source_postal_vs_initial(self):
        a=obs('bird',motion='flying',heading='towards_handle',multiplicity='single',adjacent_to=['o2'])
        r=t.read(base([a,dict(id='o2',symbol_id='letter',mark='M')]))
        self.assertNotIn('received',selected(r['observations'][0]))
        self.assertNotEqual(t.SYMBOLS['postal_mark']['locator'],t.SYMBOLS['letter']['locator'])

    def test_08_adjacency_missing_versus_empty(self):
        a=obs('numeral',numeral=90);b=dict(id='o2',symbol_id='dots')
        self.assertEqual(t.read(base([a,b]))['observations'][0]['cases'][0]['status'],'insufficient_information')
        a['adjacent_to']=[]
        self.assertEqual(t.read(base([a,b]))['observations'][0]['cases'][0]['status'],'not_applicable')

    def test_09_contradictory_neighbor_lists(self):
        a=obs('numeral',numeral=90,adjacent_to=['o2']);b=dict(id='o2',symbol_id='dots',adjacent_to=[])
        r=t.read(base([a,b]))
        self.assertEqual(r['observations'][0]['cases'][0]['status'],'conflicting_evidence')

    def test_10_surrounding_dots_not_plain_adjacency(self):
        for case in EXTRA['dots_cases']:
            a=obs('dots',adjacent_to=['o2'])
            if 'arrangement' in case:a['arrangement']=case['arrangement']
            r=t.read(base([a,dict(id='o2',symbol_id='anchor')]))
            self.assertEqual(r['observations'][0]['cases'][0]['status'],case['status'])

    def test_11_motion_heading_conflict(self):
        r=t.read(base([obs('aircraft',motion='stationary',heading='towards_handle')]))['observations'][0]
        self.assertEqual(r['status'],'conflicting_evidence')
        self.assertEqual(r['cases'][1]['intrinsic_status'],'applicable')
        self.assertEqual(r['cases'][1]['status'],'conflicting_evidence')

    def test_12_proximity_conflict(self):
        r=t.read(base([obs('apron',proximity='far',handle_relation='near_handle')]))['observations'][0]
        self.assertEqual(r['status'],'conflicting_evidence')
        self.assertEqual(selected(r),[])

    def test_13_manual_identity_alternatives(self):
        r=t.read(base([obs('anchor',alternatives=['acorn'],uncertainty=True)]))['observations'][0]
        self.assertEqual(r['status'],'conflicting_evidence')
        self.assertEqual(r['alternative_references'][0]['id'],'acorn')
        self.assertEqual(selected(r),[])

    def test_14_competing_regions(self):
        r=t.read(base([obs('cross',region='bottom',region_alternatives=['rim'],size='small',multiplicity='single')]))['observations'][0]
        self.assertEqual(r['cases'][1]['status'],'conflicting_evidence')
        self.assertEqual(r['zones']['status'],'conflicting_evidence')

    def test_15_no_aggregation_or_numeric_several(self):
        r=t.read(base([obs('acorn'),obs('acorn',id='o2')]))
        self.assertEqual([selected(o) for o in r['observations']],[['general'],['general']])
        with self.assertRaises(ValueError):t.read(base([obs('acorn',count=3)]))

    def test_16_lone_cross_conflict(self):
        r=t.read(base([obs('cross',size='small',multiplicity='single',region='bottom'),obs('cross',id='o2')]))
        self.assertEqual(r['observations'][0]['status'],EXTRA['cross_single_conflicting_second_cross'])

    def test_17_figure_viii_original_positions(self):
        r=t.read(figure());d=r['documentary_comparison']
        self.assertTrue(all(c['status']=='declared_fields_match' for c in d['placement_checks']))
        self.assertEqual([c['status'] for c in d['cases']],['applicable']*3)
        self.assertIsNone(r['observations'][0]['zones']['calendar_date'])

    def test_18_figure_musician_and_marital_context_separate(self):
        q=figure();q['context']={};r=t.read(q)
        self.assertEqual(r['documentary_comparison']['cases'][1]['status'],'insufficient_information')
        self.assertEqual(r['documentary_comparison']['cases'][2]['status'],'applicable')
        cosy=r['observations'][4];self.assertEqual(selected(cosy),[])
        self.assertTrue(all(c['status']=='insufficient_information' for c in cosy['cases']))

    def test_19_figure_adjacency_not_inferred_from_circle(self):
        q=figure();q['observations'][2].pop('adjacent_to');d=t.read(q)['documentary_comparison']
        self.assertEqual(d['cases'][0]['status'],'insufficient_information')
        self.assertEqual(d['placement_checks'][2]['status'],'missing_or_different')

    def test_20_coal_scope_and_beetle_requirement(self):
        self.assertEqual(t.read(base([obs('coal_scoop')]))['observations'][0]['status'],'unsupported')
        q=base([obs('coal_scoop')],source_example='figure_viii')
        self.assertEqual(t.read(q)['observations'][0]['status'],'insufficient_information')

    def test_21_organ_alternatives_not_resolved(self):
        o=t.read(base([obs('organ',observation='I am a musician')]))['observations'][0]
        self.assertEqual(selected(o),[]);self.assertEqual(o['reference']['alternatives'],['Wedding','Death','Realised ambition'])
        for s in ('barrel_organ','coal_scuttle'):
            self.assertEqual(t.read(base([obs(s)]))['observations'][0]['status'],'unsupported')

    def test_22_method_isolation(self):
        for q in (base(vessel='saucer'),base(vessel='coffee'),base(profile='kent-pg6964-ordinary-cup-v1'),base(profile='nelros')):
            with self.assertRaises(ValueError):t.read(q)
        self.assertIsNone(t.read(base())['documentary_comparison'])

    def test_23_strict_schema_and_ids(self):
        for q in (base(seed=1),base(schema_version=True),base(mode='image'),base([obs(id='../bad')]),base([obs(),obs()])):
            with self.assertRaises(ValueError):t.read(q)

    def test_24_validation_categories_and_relations(self):
        for row in (obs(region='saucer_centre'),obs(adjacent_to=['missing']),obs(adjacent_to=['o1']),obs(region_alternatives=[[]]),obs(motion=1),obs(uncertainty=1)):
            with self.assertRaises(ValueError):t.read(base([row]))

    def test_25_numeric_and_mark_validation(self):
        for row in (obs('numeral',numeral=True),obs('numeral',numeral=-1),obs(numeral=90),obs(mark='M'),obs('letter',mark='\ud800'),obs('letter',mark='AB')):
            with self.assertRaises(ValueError):t.read(base([row]))
        r=t.read(base([obs('letter',mark='M',size='small')]))
        self.assertNotIn('Edwards',json.dumps(r));self.assertEqual(selected(r['observations'][0]),['small'])

    def test_26_verbatim_user_records(self):
        raw=REF['raw_text'];q=base([obs(observation=raw,association=None)],notes='',context=dict(musician=None))
        r=t.read(q);self.assertEqual(r['observations'][0]['user_record'],q['observations'][0]);self.assertEqual(r['replay']['request'],q)

    def test_27_no_factual_prediction_or_recognition(self):
        r=t.read(base([obs('acorn',region='rim')]))
        self.assertFalse(r['layout']['position_inferred']);self.assertFalse(r['replay']['generated_placements'])
        self.assertTrue(all(c['forecast'] is False for c in r['observations'][0]['cases']))
        self.assertIsNone(r['observations'][0]['zones']['calendar_date'])

    def test_28_json_markdown_replay(self):
        q=base([obs(association='```\r\n猫 ')]);r=t.read(q);md=t.markdown(r)
        m=re.search(r'(`{3,})json\n(.*?)\n\1',md.split('## Exact replay metadata')[1],re.S)
        self.assertEqual(t.read(json.loads(m[2])['request']),json.loads(json.dumps(r)))

    def test_29_immutable_and_portable_hashes(self):
        with self.assertRaises(TypeError):t.DATA['version']=3
        q=base([obs()]);r=t.read(q);q['observations'][0]['symbol_id']='acorn'
        self.assertEqual(r['replay']['request']['observations'][0]['symbol_id'],'anchor')
        self.assertEqual(t.digest({'a':1,'猫':2}),t.digest({'猫':2,'a':1}))
        self.assertEqual(t.PROFILE_HASH,t.digest(t.thaw(t.DATA)))

    def test_30_registry_source_rules(self):
        reg=load_registry()
        try:
            t.read(base(),reg);rows=reg.db.execute('SELECT record FROM rules WHERE id LIKE ?',('tasseography.kent.%',)).fetchall()
            self.assertEqual(len(rows),23)
            self.assertTrue(all(json.loads(r[0])['version']==2 and json.loads(r[0])['status']=='proposed' for r in rows))
        finally:reg.close()

    def test_31_strict_file_and_bounds(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'x.json');p.write_text('{"a":1,"a":2}',encoding='utf-8')
            with self.assertRaises(ValueError):t.load_input(p)
        with self.assertRaises(ValueError):t.read(base([obs(id='o'+str(i)) for i in range(65)]))
        with self.assertRaises(ValueError):t.read(base([obs(observation='x'*10001)]))

    def test_32_unknown_and_empty(self):
        r=t.read(base());self.assertEqual(r['observations'],[])
        o=t.read(base([obs('unknown',alternatives=['unverified'])]))['observations'][0]
        self.assertEqual(o['status'],'unsupported');self.assertIsNone(o['reference'])


if __name__=='__main__':unittest.main()
