import json
import math
import unittest
from pathlib import Path
from datetime import datetime,timedelta,timezone
from future.natal import SkyfieldEphemeris,signed,birth_utc,chart,Settings
from future.astrocartography import (coordinates,generate,diagnostics,line_geometry,nearest,
                                    register_knowledge,PROFILE,markdown)
from future.__main__ import load_registry

FIXTURE=json.loads(Path('tests/fixtures/astrocartography_swiss.json').read_text())


class AstrocartographyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.e=SkyfieldEphemeris('data/de440s.bsp')
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()

    def test_independent_coordinates_and_meridians(self):
        maxima=dict(ra=0.,declination=0.,gast=0.,meridian=0.,horizon_altitude=0.,cusp=0.)
        for case in FIXTURE['cases']:
            utc=datetime.fromisoformat(case['utc']);t,positions=coordinates(self.e,utc)
            maxima['gast']=max(maxima['gast'],abs(signed(float(t.gast)*15-case['gast_degrees'])))
            for name,b in positions.items():
                r=case['planets'][name]
                maxima['ra']=max(maxima['ra'],abs(signed(b['ra_degrees']-r['ra'])))
                maxima['declination']=max(maxima['declination'],abs(b['declination_degrees']-r['dec']))
                for angle in ('MC','IC'):
                    segments,_=line_geometry(b,angle)
                    lon=segments[0][0][0]
                    residual=abs(signed(case['gast_degrees']+lon-r['ra']-(180 if angle=='IC' else 0)))
                    maxima['meridian']=max(maxima['meridian'],residual)
                    self.assertLess(residual,.012)
        self.assertLess(maxima['ra'],.001);self.assertLess(maxima['declination'],.001)
        self.assertLess(maxima['gast'],.012)

    def test_independent_horizon_roots_and_circumpolar(self):
        for case in FIXTURE['cases']:
            _,positions=coordinates(self.e,datetime.fromisoformat(case['utc']))
            for r in case['horizon_roots']:
                body=positions[r['planet']]
                if not r['roots']:
                    self.assertIn(diagnostics(body,r['latitude'],0)['horizon_status'],('always-above','always-below'))
                for root in r['roots']:
                    diag=diagnostics(body,r['latitude'],root['longitude'])
                    self.assertLess(abs(diag['geometric_altitude_degrees']),.012)
                    derivative=diag['altitude_sine_derivative_per_hour_angle_radian']
                    self.assertGreater(derivative if root['angle']=='ASC' else -derivative,0)
                    self.assertLess(nearest(body,root['angle'],r['latitude'],root['longitude'])['distance_km'],1.4)

    def test_sampled_lines_against_independent_equatorial_reference(self):
        maximum=0.
        for case in FIXTURE['cases']:
            _,positions=coordinates(self.e,datetime.fromisoformat(case['utc']))
            for name,b in positions.items():
                r=case['planets'][name]
                for angle in ('ASC','DSC'):
                    segments,_=line_geometry(b,angle,.01)
                    for segment in segments:
                        for lon,lat in segment:
                            h=(case['gast_degrees']+lon-r['ra'])*math.pi/180
                            p,d=lat*math.pi/180,r['dec']*math.pi/180
                            sine=math.sin(p)*math.sin(d)+math.cos(p)*math.cos(d)*math.cos(h)
                            altitude=math.degrees(math.asin(max(-1,min(1,sine))))
                            maximum=max(maximum,abs(altitude))
                            self.assertGreaterEqual(-math.sin(h) if angle=='ASC' else math.sin(h),-1e-4)
        self.assertLess(maximum,.012)

    def test_dateline_and_independent_interpolation_probes(self):
        for dec in (-89.9,-45,-.001,0,.001,45,89.9):
            for mc in (-180,-179,0,179):
                body=dict(mc_longitude=mc,declination_degrees=dec)
                for angle in ('ASC','DSC'):
                    segments,info=line_geometry(body,angle,.01)
                    self.assertLessEqual(info['max_probe_residual_degrees'],.008)
                    for seg in segments:
                        self.assertGreaterEqual(len(seg),2)
                        for a,b in zip(seg,seg[1:]):
                            self.assertLessEqual(abs(a[0]-b[0]),180)
                            for f in (.1,.2,.4,.6,.8,.9):
                                lon=a[0]+f*(b[0]-a[0]);lat=a[1]+f*(b[1]-a[1])
                                self.assertLess(abs(diagnostics(body,lat,lon)['geometric_altitude_degrees']),.0101)
                    for a,b in zip(segments,segments[1:]):
                        self.assertEqual(abs(a[-1][0]),180);self.assertEqual(a[-1][1],b[0][1])

    def test_hand_derived_branches_poles_and_grazing(self):
        b=dict(mc_longitude=0,declination_degrees=0)
        self.assertAlmostEqual(nearest(b,'ASC',0,-90)['distance_km'],0)
        self.assertAlmostEqual(nearest(b,'DSC',0,90)['distance_km'],0)
        self.assertAlmostEqual(nearest(b,'ASC',0,90)['central_angle_degrees'],90)
        self.assertEqual(nearest(b,'ASC',0,90)['nearest_kind'],'grazing-endpoint')
        self.assertEqual(diagnostics(b,90,0)['horizon_status'],'polar-degenerate')
        b['declination_degrees']=45
        self.assertEqual(diagnostics(b,45,180)['horizon_status'],'grazing')
        self.assertEqual(diagnostics(b,80,0)['horizon_status'],'always-above')
        self.assertEqual(diagnostics(b,-80,0)['horizon_status'],'always-below')
        self.assertAlmostEqual(diagnostics(b,0,-90)['geometric_altitude_degrees'],0)

    def test_distance_against_independent_dense_geographic_search(self):
        # Independently construct horizon roots by latitude, evaluate haversine distances.
        for angle,lon,lat in [('ASC',135,20),('DSC',-150,-40),('MC',90,50),('IC',-30,-15)]:
            b=dict(mc_longitude=15,declination_degrees=-20)
            best=180.
            limit=70 if angle in ('ASC','DSC') else 90
            for i in range(limit*200+1):
                p=-limit+i*.01
                if angle in ('ASC','DSC'):
                    h=math.degrees(math.acos(-math.tan(math.radians(p))*math.tan(math.radians(-20))))
                    l=15+(-h if angle=='ASC' else h)
                else:l=15+(180 if angle=='IC' else 0)
                a=math.sin(math.radians(p-lat)/2)**2+math.cos(math.radians(lat))*math.cos(math.radians(p))*math.sin(math.radians(l-lon)/2)**2
                distance=math.degrees(2*math.asin(math.sqrt(min(1,a))))
                best=min(best,distance)
            actual=nearest(b,angle,lat,lon)['central_angle_degrees']
            self.assertLessEqual(actual,best+1e-8)
            self.assertLess(best-actual,.011)

    def test_relocation_six_systems_against_swiss(self):
        from future.astrocartography import relocated
        systems=dict(P='placidus',R='regiomontanus',C='campanus',O='porphyry',E='equal',W='whole-sign')
        for case in FIXTURE['cases']:
            for ref in case['sites']:
                r=relocated(self.e,datetime.fromisoformat(case['utc']),dict(name='test',zone='UTC',latitude=ref['latitude'],longitude=ref['longitude']),systems[ref['system']])
                c=r['chart']
                for key in ('ascendant','midheaven'):self.assertLess(abs(signed(c['angles'][key]-ref[key])),.012)
                for a,b in zip(c['house_cusps'],ref['cusps']):self.assertLess(abs(signed(a-b)),.02)

    def test_absolute_instant_multiple_destinations_and_earlier_interface(self):
        r=generate(self.e,'1990-07-15T12:00:00','Asia/Kolkata',28.6,77.2,
            destinations=[dict(name='Sydney',latitude=-33.8688,longitude=151.2093,zone='Australia/Sydney'),
                          dict(name='Polar',latitude=80,longitude=0,zone='UTC')],query=(28.6,77.2),uncertainty_minutes=5)
        self.assertEqual(len(r['geojson']['features']),40)
        natal=r['natal_frame']['chart'];rel=r['relocated_frames'][0]['chart']
        self.assertEqual(natal['planets'].keys(),rel['planets'].keys())
        for name in natal['planets']:self.assertEqual(natal['planets'][name]['longitude'],rel['planets'][name]['longitude'])
        self.assertNotEqual(natal['angles'],rel['angles'])
        self.assertEqual(r['birth']['utc'],r['relocated_frames'][0]['utc'])
        self.assertEqual(r['relocated_frames'][1]['status'],'unsupported')
        old=chart(self.e,'1990-07-15T12:00:00','Asia/Kolkata',28.6,77.2,Settings(houses='placidus'))
        self.assertEqual(old['angles'],natal['angles']);self.assertEqual(old['technique_id'],1)
        self.assertIn('Compositional',markdown(r));self.assertEqual(len(r['query']['lines']),40)

    def test_birth_time_sensitivity_and_zone_ambiguity(self):
        r=generate(self.e,'2000-02-29T23:55:00','UTC',0,0,bodies=['Sun'],uncertainty_minutes=10)
        for row in r['birth_time_sensitivity']:
            shift=row['planets']['Sun']['mc_shift_degrees']
            self.assertAlmostEqual(shift,-row['offset_minutes']/4,delta=.002)
        with self.assertRaises(ValueError):birth_utc('2024-11-03T01:30:00','America/New_York')
        a=birth_utc('2024-11-03T01:30:00','America/New_York',0)
        b=birth_utc('2024-11-03T01:30:00','America/New_York',1)
        self.assertEqual(b-a,timedelta(hours=1))
        with self.assertRaises(ValueError):birth_utc('2024-03-10T02:30:00','America/New_York')

    def test_rule_provenance_and_unsupported_books(self):
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            rules=registry.select_rules(7,'angular lines',PROFILE)
            self.assertEqual(len(rules),1);self.assertEqual(rules[0]['fixture_ids'],['astrocartography-swiss-v1'])
            self.assertEqual(registry.select_rules(7,'angular lines','Jim Lewis'),[])
            r=generate(self.e,'2000-01-01','UTC',0,0,bodies=['Pluto'])
            for f in r['geojson']['features']:
                reading=f['properties']['interpretation']
                self.assertEqual(reading['coverage'],'compositional')
                self.assertEqual(reading['direct_book_coverage'],'unsupported')
                self.assertEqual(len(reading['sources']),2)
        finally:registry.close()

    def test_invalid_configurations(self):
        for kwargs in [dict(profile='Lewis'),dict(tolerance=float('nan')),dict(uncertainty_minutes=-1),
                       dict(bodies=[]),dict(bodies=['Sun','Sun']),dict(bodies=['Node']),dict(query=(91,0)),dict(houses='unknown')]:
            with self.assertRaises(ValueError):generate(self.e,'2000-01-01','UTC',0,0,**kwargs)
        for year in (1800,2149):
            with self.assertRaises(ValueError):generate(self.e,f'{year}-01-01','UTC',0,0)

    def test_reproducibility(self):
        args=(self.e,'2024-01-01T00:00:00','UTC',-30,150)
        a=generate(*args,bodies=['Moon']);b=generate(*args,bodies=['Moon'])
        self.assertEqual(json.dumps(a,sort_keys=True),json.dumps(b,sort_keys=True))

if __name__=='__main__':unittest.main()
