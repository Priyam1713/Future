import json,unittest
from pathlib import Path
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo
from future.natal import SkyfieldEphemeris,signed
from future.mundane import ingresses,ingress_instants,conjunctions,register_knowledge,DATA,PROFILE,readings,historical_duration,_event_chart,_conditions,aspect_geometry
from future.__main__ import load_registry

class MundaneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.e=SkyfieldEphemeris('data/de440s.bsp')
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()

    def test_all_four_published_usno_2026_instants(self):
        f=json.loads(Path('tests/fixtures/mundane_usno.json').read_text())
        r=ingresses(self.e,2026,'Europe/London',51.5,0)
        for a,b in zip(r['events'],f['response_selected_seasons']['data']):
            published=datetime(b['year'],b['month'],b['day'],int(b['time'][:2]),int(b['time'][3:]),tzinfo=timezone.utc)
            self.assertLess(abs((datetime.fromisoformat(a['utc'])-published).total_seconds()),f['tolerance_seconds'])
            self.assertEqual(a['target_longitude'],b['target'])
            self.assertEqual(a['chart']['planets']['Sun']['sign'],a['sign'])
            self.assertLess(a['residual_degrees'],1e-6);self.assertLessEqual(a['bracket_seconds'],.001)
            before=datetime.fromisoformat(a['bracket_utc'][0])
            self.assertLess(signed(float(self.e.longitudes('Sun',[before])[0])-b['target']),0)
            self.assertGreaterEqual(signed(a['solar_longitude']-b['target']),0)

    def test_independent_swiss_positions_houses_and_two_sites(self):
        f=json.loads(Path('tests/fixtures/mundane_swiss.json').read_text());tol=f['tolerances']
        for year in f['years']:
            results=[ingresses(self.e,year['year'],'UTC',51.5,0),ingresses(self.e,year['year'],'UTC',-33.8688,151.2093)]
            for i,ref in enumerate(year['events']):
                self.assertEqual(results[0]['events'][i]['utc'],results[1]['events'][i]['utc'])
                self.assertNotEqual(results[0]['events'][i]['chart']['angles']['ascendant'],results[1]['events'][i]['chart']['angles']['ascendant'])
                for j,result in enumerate(results):
                    a=result['events'][i];n=a['chart'];site=ref['sites'][j]
                    self.assertLess(abs((datetime.fromisoformat(a['utc'])-datetime.fromisoformat(ref['utc'])).total_seconds()),tol['ingress_seconds'])
                    self.assertEqual(len(n['planets']),9);self.assertNotIn('Pluto',n['planets'])
                    for body,p in ref['positions'].items():
                        self.assertLess(abs(signed(n['planets'][body]['longitude']-p['longitude'])),tol['planet_degrees'])
                        self.assertEqual(n['planets'][body]['retrograde'],p['retrograde'])
                    for x,y in zip(n['house_cusps'],site['cusps']):self.assertLess(abs(signed(x-y)),tol['cusp_degrees'])
                    for k in ('ascendant','midheaven'):self.assertLess(abs(signed(n['angles'][k]-site[k])),tol['cusp_degrees'])

    def test_independent_repeated_conjunctions_stations_and_ingresses(self):
        f=json.loads(Path('tests/fixtures/mundane_swiss.json').read_text())
        for i,c in enumerate(f['cycles']):
            r=conjunctions(self.e,datetime.fromisoformat(c['start']),datetime.fromisoformat(c['end']),'Europe/London',51.5,0)
            actual=[{'type':'conjunction','utc':x['utc']} for x in r['events']]+r['motion_changes']
            actual.sort(key=lambda x:(x['utc'],x.get('body',''),x['type']))
            self.assertEqual(len(actual),len(c['events']))
            for a,b in zip(actual,c['events']):
                self.assertEqual((a['type'],a.get('body'),a.get('target_longitude')),(b['type'],b.get('body'),b.get('target_longitude')))
                seconds=abs((datetime.fromisoformat(a['utc'])-datetime.fromisoformat(b['utc'])).total_seconds())
                if a['type']=='conjunction':
                    # Independent oracle instant and coordinate-error allowance,
                    # not a changed expected root or an arbitrary extra minute.
                    _,p=self.e.positions(datetime.fromisoformat(b['utc']))
                    error=abs(signed(p['Jupiter']['longitude']-p['Saturn']['longitude']))
                    speed=abs(p['Jupiter']['speed_degrees_per_day']-p['Saturn']['speed_degrees_per_day'])
                    self.assertLess(error,f['tolerances']['conjunction_angle_degrees'])
                    self.assertLess(seconds,f['tolerances']['conjunction_angle_degrees']/speed*86400+1)
                else:self.assertLess(seconds,f['tolerances']['cycle_event_seconds'])
            self.assertEqual(len(r['events']),1 if i==0 else 3)
            for x in r['events']:
                self.assertEqual(x['phase_before'],'applying');self.assertEqual(x['phase_after'],'separating')
                self.assertLess(x['residual_degrees'],.0001)
                self.assertEqual(x['pair_interpretation']['coverage'],'compositional')

    def test_timezones_dst_folds_and_explicit_location(self):
        ny=ingresses(self.e,2024,'America/New_York',40.7,-74)
        self.assertTrue(ny['events'][0]['chart']['epoch']['local'].endswith('-04:00'))
        self.assertTrue(ny['events'][3]['chart']['epoch']['local'].endswith('-05:00'))
        syd=ingresses(self.e,2024,'Australia/Sydney',-33.8688,151.2093)
        self.assertTrue(syd['events'][0]['chart']['epoch']['local'].endswith('+11:00'))
        self.assertTrue(syd['events'][1]['chart']['epoch']['local'].endswith('+10:00'))
        for utc,fold in [('2024-11-03T05:30:00+00:00',0),('2024-11-03T06:30:00+00:00',1)]:
            n=_event_chart(self.e,datetime.fromisoformat(utc),ZoneInfo('America/New_York'),40.7,-74)
            self.assertEqual(n['epoch']['fold'],fold);self.assertIn('T01:30:',n['epoch']['local'])
        east=ingresses(self.e,2026,'Pacific/Kiritimati',0,180)
        west=ingresses(self.e,2026,'Pacific/Honolulu',0,-180)
        self.assertEqual([x['utc'] for x in east['events']],[x['utc'] for x in west['events']])
        self.assertNotEqual(east['events'][0]['chart']['epoch']['local'],west['events'][0]['chart']['epoch']['local'])

    def test_utc_year_domain_leap_and_half_open_cycle_boundary(self):
        for year in (1851,2000,2148):
            events=ingress_instants(self.e,year)
            self.assertEqual(len(events),4)
            self.assertTrue(all(datetime.fromisoformat(x['utc']).year==year for x in events))
        f=json.loads(Path('tests/fixtures/mundane_swiss.json').read_text())['cycles'][0]
        r=conjunctions(self.e,datetime.fromisoformat(f['start']),datetime.fromisoformat(f['end']),'UTC',0,0)
        instant=datetime.fromisoformat(r['events'][0]['utc'])
        # Leave a one-second margin around the numeric root: before/after
        # windows demonstrate that a contact is neither lost nor duplicated.
        a=conjunctions(self.e,instant-timedelta(minutes=2),instant-timedelta(seconds=1),'UTC',0,0)
        b=conjunctions(self.e,instant-timedelta(seconds=1),instant+timedelta(minutes=2),'UTC',0,0)
        self.assertEqual(len(a['events']),0);self.assertEqual(len(b['events']),1)

    def test_named_profile_and_invalid_inputs(self):
        for year in (True,2026.,1850,2149):
            with self.assertRaises(ValueError):ingresses(self.e,year,'UTC',0,0)
        for lat,lon in [(60,0),(-60,0),(float('nan'),0),(0,181),(True,0)]:
            with self.assertRaises(ValueError):ingresses(self.e,2026,'UTC',lat,lon)
        for p in ('Lilly','Raphael','Campion'):
            with self.assertRaises(ValueError):ingresses(self.e,2026,'UTC',0,0,p)
        with self.assertRaises(ValueError):ingresses(self.e,2026,'UTC',0,0,historical_duration_option=1)
        for start,end in [(datetime(2026,1,1),datetime(2026,2,1)),
                (datetime(2026,1,1,tzinfo=timezone.utc),datetime(2026,1,1,tzinfo=timezone.utc)),
                (datetime(2024,1,1,tzinfo=timezone.utc),datetime(2026,1,1,tzinfo=timezone.utc))]:
            with self.assertRaises(ValueError):conjunctions(self.e,start,end,'UTC',0,0)

    def test_source_rules_conditions_and_qualified_duration(self):
        for sign in range(12):
            d=historical_duration(sign*30+.01,True)
            self.assertEqual(d['symbolic_months'],(3,12,6)[sign%3])
            self.assertIn('insufficient',d['rule']['exceptions'][0])
            self.assertFalse(historical_duration(sign*30,True,False)['applicable'])
        self.assertNotIn('symbolic_months',historical_duration(0,False))
        r=ingresses(self.e,2026,'UTC',51.5,0,historical_duration_option=True)
        n=r['events'][0]['chart'];reading=readings(n)
        self.assertEqual(n['conditions']['Sun']['own_dignities'],['exaltation'])
        self.assertEqual(n['conditions']['Neptune']['dignity_coverage'],'unsupported')
        self.assertTrue(all(x['within_orb'] is None for x in n['aspect_geometry']))
        self.assertTrue(any(p['coverage']=='compositional' for p in reading['placements']))
        self.assertTrue(any(p['coverage']=='unsupported' for p in reading['placements']))
        for p in reading['placements']:
            self.assertTrue(all(c['source_id']==DATA['source']['id'] and c['locator'] for c in p['components']))
        self.assertTrue(r['events'][0]['optional_duration']['applicable'])
        self.assertTrue(all(not x['optional_duration']['applicable'] for x in r['events'][1:]))
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            self.assertFalse(registry.select_rules(6,'ingresses and selected conjunctions','Raphael'))
            self.assertEqual(len(DATA['rules']),34)
        finally:registry.close()

    def test_published_chart_comparison_preserves_discrepancy(self):
        f=json.loads(Path('tests/fixtures/mundane_green_published.json').read_text())
        r=ingresses(self.e,1899,'Europe/London',51.5,0)['events'][0]
        errors={b:abs(signed(r['chart']['planets'][b]['longitude']-v)) for b,v in f['longitudes'].items()}
        for b,delta in errors.items():
            if b!='Saturn':self.assertLess(delta,.02)
        # Re-inspected original p115 prints22°33 Sagittarius. Do not rewrite
        # it to23°33 to force a match; this is a source discrepancy, not a pass.
        self.assertGreater(errors['Saturn'],.9)
        self.assertEqual(f['longitudes']['Saturn'],262.55)
        self.assertIn('Saturn',f['source_discrepancy'])

    def test_reproducibility_and_no_natal_interface_mutation(self):
        a=ingresses(self.e,2026,'Europe/London',51.5,0)
        b=ingresses(self.e,2026,'Europe/London',51.5,0)
        self.assertEqual(a,b)
        self.assertEqual(a['release_status'],'Core v1 Ready')
        self.assertTrue(all('epoch' in e['chart'] and 'birth' not in e['chart'] for e in a['events']))
        from future.natal import chart
        n=chart(self.e,'2026-03-20T14:45:00','UTC',51.5,0)
        self.assertEqual(n['technique_id'],1);self.assertEqual(n['settings']['application'],'natal')
        self.assertIn('Pluto',n['planets']);self.assertIn('birth',n)
