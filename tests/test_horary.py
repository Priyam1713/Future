import json,unittest
from pathlib import Path
from datetime import datetime,timedelta,timezone
from future.natal import SkyfieldEphemeris,signed
from future.horary import assess,classify,hour_from_events,register_knowledge,DATA,SCOPE,planetary_hour
from future.horary_motion import aspect_state,motion,ordered_candidates,contact_roots
from future.doctrines import dignity,DoctrineSettings
from future.__main__ import load_registry
from future.transits import roots

class HoraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.e=SkyfieldEphemeris('data/de440s.bsp')
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()

    def test_original_published_arithmetic_and_reception(self):
        f=json.loads(Path('tests/fixtures/horary_published.json').read_text())
        r=aspect_state({'name':'Venus','longitude':40,'speed_degrees_per_day':1},
                       {'name':'Saturn','longitude':168,'speed_degrees_per_day':.1},120)
        self.assertEqual(r['orb'],f['moiety']['deviation']);self.assertEqual(r['moiety'],9)
        self.assertTrue(r['within_orb']);self.assertEqual(r['phase'],'applying')
        settings=DoctrineSettings('lilly-ptolemaic','lilly','lilly-ca113','fixed-day-fortune','dignity-occupancy')
        for key,kind in [('domicile_pair','domicile'),('triplicity_pair_day','triplicity'),('terms_pair','bound')]:
            pair=list(f['reception'][key].items())
            self.assertEqual(dignity(pair[0][1],True,settings)[kind],pair[1][0])
            self.assertEqual(dignity(pair[1][1],True,settings)[kind],pair[0][0])
        # Cambridge is documentary evidence, explicitly not numerical validation.
        self.assertIn('1643',f['cambridge']['printed_date'])
        self.assertIn('not',f['cambridge']['source_judgment'])

    def test_original_unequal_planetary_hours_and_boundaries(self):
        f=json.loads(Path('tests/fixtures/horary_published.json').read_text())['planetary_hours']
        def t(clock):return datetime.fromisoformat('2026-11-02T'+clock+':00+00:00')
        rise,set_=t(f['sunrise']),t(f['sunset']);next_=rise+timedelta(days=1)
        for c in f['cases']:
            r=hour_from_events(rise,set_,next_,t(c['time']),0)
            self.assertEqual((r['lord'],r['hour']),(c['lord'],c['hour']))
        self.assertEqual(hour_from_events(rise,set_,next_,rise,0)['hour'],1)
        self.assertEqual(hour_from_events(rise,set_,next_,set_,0)['hour'],13)
        with self.assertRaises(ValueError):hour_from_events(rise,set_,next_,next_,0)
        with self.assertRaises(ValueError):hour_from_events(rise,set_,next_,rise,True)

    def test_no_false_certification_conflicts_or_missing_rules(self):
        pos={'id':'p','direction':'positive','value':True};neg={'id':'n','direction':'negative','value':False}
        gate={'id':'g','value':True}
        self.assertEqual(classify([pos,neg],[gate])['classification'],'supported_positive')
        self.assertEqual(classify([dict(pos,value=False),dict(neg,value=True)],[gate])['classification'],'supported_negative')
        for predicates,cautions in [([pos,dict(neg,value=True)],[gate]),([pos,neg],[dict(gate,value=None)]),
                ([pos,dict(neg,value=None)],[gate]),([dict(pos,value=False),neg],[gate]),([pos,neg],[dict(gate,value=False)])]:
            self.assertEqual(classify(predicates,cautions)['classification'],'indeterminate')

    def test_relative_application_and_sign_boundaries(self):
        def body(n,l,v):return dict(name=n,longitude=l,speed_degrees_per_day=v)
        self.assertEqual(aspect_state(body('Mercury',359,2),body('Saturn',1,0),0)['phase'],'applying')
        self.assertFalse(aspect_state(body('Mercury',359,2),body('Saturn',1,0),0)['sign_agreement'])
        self.assertEqual(aspect_state(body('Mercury',1,2),body('Saturn',0,0),0)['phase'],'separating')
        self.assertEqual(aspect_state(body('Mercury',1,-1),body('Saturn',0,0),0)['phase'],'applying')
        self.assertTrue(aspect_state(body('Mercury',.05,2),body('Saturn',0,0),0)['post_exact_within_six_arcminutes'])

    def test_reversal_double_contact_and_half_open_window(self):
        start=datetime(2026,1,1,tzinfo=timezone.utc)
        times=[start+timedelta(hours=h) for h in range(4)]
        # Known analytic roots at1.3/1.7h, both between hourly samples.
        def f(t):
            h=(t-start).total_seconds()/3600
            return ((h-1.5)**2-.04)%360
        found=contact_roots(times,[f(t) for t in times],0,f)
        self.assertEqual(len(found),2)
        for actual,h in zip(found,[1.3,1.7]):self.assertLess(abs((actual-start).total_seconds()-h*3600),.3)
        linear=lambda t:(t-start).total_seconds()/3600
        self.assertEqual(roots(times,[0,1,2,3],3,linear),[])
        self.assertEqual(roots(times,[0,1,2,3],0,linear),[start])

    def test_intervening_recipient_contact_and_station_not_certified(self):
        events=[{'type':'station','bodies':['Mercury'],'utc':'01'},
                {'type':'exact_aspect','bodies':['Mars','Jupiter'],'utc':'02','angle':0},
                {'type':'exact_aspect','bodies':['Mercury','Mars'],'utc':'03','angle':0}]
        r=ordered_candidates(events,'Mercury','Mars')
        self.assertEqual(len(r['candidates']),2)
        self.assertIn('not certified',r['status'])
        self.assertIsNone(ordered_candidates(events,'Moon','Venus')['target_contact'])

    def test_independent_all_planet_motion_and_chart(self):
        f=json.loads(Path('tests/fixtures/horary_reference.json').read_text())
        stations=ingresses=0
        for c in f['cases']:
            utc=datetime.fromisoformat(c['utc']);r=motion(self.e,utc)
            self.assertEqual(len(r['events']),len(c['events']))
            for a,b in zip(r['events'],c['events']):
                self.assertEqual((a['type'],a['bodies'],a.get('angle')),(b['type'],b['bodies'],b.get('angle')))
                self.assertLess(abs((datetime.fromisoformat(a['utc'])-utc).total_seconds()-b['seconds_from_start']),f['event_tolerance_seconds'])
                if a['type']=='exact_aspect':self.assertLess(a['residual_degrees'],.0001)
                stations+=a['type']=='station';ingresses+=a['type']=='ingress'
            a=assess(self.e,'Was this advice well intended?','advice-intent',c['utc'][:-6],'UTC',c['latitude'],c['longitude'])
            n=a['question_chart']
            for b,p in c['positions'].items():
                self.assertLess(abs(signed(n['planets'][b]['longitude']-p['longitude'])),f['longitude_tolerance_degrees'])
                self.assertEqual(n['planets'][b]['retrograde'],p['retrograde'])
            for x,y in zip(n['house_cusps'],c['cusps']):self.assertLess(abs(signed(x-y)),f['angle_tolerance_degrees'])
            self.assertEqual(a['classification'],'indeterminate')
            self.assertIn('gate.seventh_full',a['unknown_rules'])
            self.assertTrue(all(d['locator'] and d['source_id']==DATA['source']['id'] for d in a['rule_diagnostics']))
        self.assertGreater(stations,0);self.assertGreater(ingresses,0)

    def test_protocol_validation_and_isolation(self):
        args=[self.e,'Question','advice-intent','2026-11-03T12:00:00','Asia/Kolkata',28,77]
        self.assertEqual(assess(self.e,'Question','marriage','x','x',0,0)['classification'],'unsupported_question')
        for kwargs in [{'protocol':'received-question'},{'profile':'Frawley'}]:
            with self.assertRaises(ValueError):assess(*args,**kwargs)
        with self.assertRaises(ValueError):assess(self.e,'','advice-intent',*args[3:])
        with self.assertRaises(ValueError):assess(self.e,'Q','advice-intent','2024-11-03T01:30:00','America/New_York',40,-74)
        with self.assertRaises(ValueError):assess(self.e,'Q','advice-intent','2024-03-10T02:30:00','America/New_York',40,-74)
        with self.assertRaises(ValueError):motion(self.e,datetime(2026,1,1))
        with self.assertRaises(ValueError):motion(self.e,datetime(2026,1,1,tzinfo=timezone.utc),float('nan'))

    def test_registry_source_version_and_no_verified_judgment_claim(self):
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            for r in DATA['rules']:
                self.assertTrue(r['locator']);self.assertEqual(r['source_id'],DATA['source']['id'])
        finally:registry.close()

    def test_independent_sunrise_mean_node_and_source_scope(self):
        f=json.loads(Path('tests/fixtures/horary_reference.json').read_text())
        for c in f['cases']:
            utc=datetime.fromisoformat(c['utc'])
            hour=planetary_hour(self.e,utc,c['latitude'],c['longitude'])
            for key in ('sunrise','sunset','next_sunrise'):
                delta=(datetime.fromisoformat(hour[key+'_utc'])-utc).total_seconds()
                self.assertLess(abs(delta-c[key+'_seconds_from_start']),120)
            r=assess(self.e,'Question','advice-intent',c['utc'][:-6],'UTC',c['latitude'],c['longitude'])
            self.assertLess(abs(signed(r['nodes']['positions']['North Node']['longitude']-c['mean_node_longitude'])),.02)
            for reading in r['interpretations']:
                self.assertEqual(reading['coverage'],'direct');self.assertIn('Individual testimony',reading['limitation'])
        self.assertEqual(SCOPE['status'],'Developing');self.assertIn('NOT MET',SCOPE['acceptance']['core_v1'])
        pages=json.loads(Path('knowledge/horary_image_provenance.json').read_text())
        self.assertEqual(len(pages),len({p['printed_page'] for p in pages}))
        self.assertGreaterEqual(len(pages),32)
        for p in pages:self.assertRegex(p['sha256'],r'^[0-9a-f]{64}$')

    def test_explicit_fold_and_repeatability(self):
        args=[self.e,'Question','advice-intent','2024-11-03T01:30:00','America/New_York',40,-74]
        a=assess(*args,fold=0);b=assess(*args,fold=1)
        self.assertEqual((datetime.fromisoformat(b['question_chart']['birth']['utc'])-
                          datetime.fromisoformat(a['question_chart']['birth']['utc'])).total_seconds(),3600)
        again=assess(*args,fold=0)
        self.assertEqual(a,again)

    def test_targeted_caution_recheck_keeps_unknown_and_version_history(self):
        from future.horary import ATTEMPT
        self.assertIsNone(ATTEMPT['gate']['value'])
        self.assertEqual(ATTEMPT['gate']['certified_configurations'],[])
        r=assess(self.e,'Question','advice-intent','2026-11-03T12:00:00','Asia/Kolkata',28.6139,77.209)
        gate=next(d for d in r['rule_diagnostics'] if d['id']=='gate.seventh_full')
        self.assertIsNone(gate['value']);self.assertIn('seventh-cusp',gate['reason'].lower())
        self.assertEqual(gate['evidence']['rule_ref']['version'],2)
        self.assertEqual(r['classification'],'indeterminate')
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            versions=[x['version'] for x in registry.db.execute("SELECT version FROM rules WHERE id='horary.accidentals-gap' ORDER BY version")]
            self.assertEqual(versions,[1,2])
            self.assertFalse(registry.select_rules(5,'Lilly advice intent',DATA['profile']))
        finally:registry.close()

    def test_no_synthetic_or_wrong_category_published_acceptance(self):
        from future.horary import ATTEMPT
        search=ATTEMPT['validation_search']
        self.assertEqual(search['qualifying_published_examples'],[])
        self.assertTrue(all(not c['accepted'] and c['reason'] and c['locator'] for c in search['candidates']))
        conditions={r['id']:r for r in ATTEMPT['material_conditions']}
        self.assertEqual(conditions['seventh.cusp.affliction']['implementation'],'unresolved')
        self.assertIn('not established',conditions['table.accidental_debilities']['materiality'])
