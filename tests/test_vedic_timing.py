import json,unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path
from future.vedic import d1
from future.natal import SkyfieldEphemeris,signed
from future.vedic_timing import vimshottari,navamsa,navamsa_point,antardashas,enrich

class VedicTimingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.e=SkyfieldEphemeris('data/de440s.bsp')
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()
    def test_published_navamsa_examples_and_complete_chart54(self):
        f=json.loads(Path('tests/fixtures/vedic_published.json').read_text())
        for p in f['d9_example16']['points']:self.assertEqual(navamsa_point(p['longitude'])['sign'],p['d9_sign'])
        c=f['chart54'];n=d1(self.e,c['local'],c['zone'],c['latitude'],c['longitude']);r=navamsa(n)
        for name,expected in c['d1_longitudes'].items():
            actual=n['ascendant']['longitude'] if name=='Ascendant' else n['planets'][name]['longitude']
            self.assertLess(abs(signed(actual-expected)),c['tolerance_degrees'],name)
        for name,expected in c['d9_signs'].items():
            actual=r['ascendant']['sign'] if name=='Ascendant' else r['planets'][name]['sign']
            self.assertEqual(actual,expected,name)
        self.assertNotEqual(n['ascendant']['sign'],r['ascendant']['sign'])
        self.assertEqual(r['planets']['Sun']['house'],10)
    def test_independent_d9_and_all_rational_boundaries(self):
        f=json.loads(Path('tests/fixtures/vedic_reference.json').read_text())
        for c in f['cases']:
            n=d1(self.e,c['local'],c['zone'],c['latitude'],c['longitude']);r=navamsa(n)
            self.assertLess(abs(signed(r['ascendant']['longitude_symbolic']-c['d9_ascendant'])),.02)
            for name,expected in c['d9_longitudes'].items():
                self.assertLess(abs(signed(r['planets'][name]['longitude_symbolic']-expected)),.02,name)
        for i in range(108):
            edge=i*10/3
            self.assertEqual(navamsa_point(edge)['sign_index'],i%12)
            self.assertEqual(navamsa_point(edge-1e-7)['sign_index'],(i-1)%12)
            self.assertEqual(navamsa_point(edge+1e-7)['sign_index'],i%12)
    def test_published_fraction_and_full_parent_antardashas(self):
        f=json.loads(Path('tests/fixtures/vedic_published.json').read_text())['dasha_example50'];birth=datetime.fromisoformat(f['birth_utc'])
        r=vimshottari(birth,f['moon_longitude_rounded'],birth)
        b=r['birth_balance']
        self.assertEqual(b['lord'],f['first_lord']);self.assertEqual(r['birth_moon_nakshatra']['pada'],3)
        self.assertAlmostEqual(b['years_remaining'],2.24875,places=10)
        self.assertLess(abs((datetime.fromisoformat(b['end_exclusive_utc'])-datetime.fromisoformat('2002-07-16T23:02:00+00:00')).total_seconds()),.00001)
        # The book's civil July15 approximation is not silently forced.
        self.assertIn('inconsistent',r['limitations'][1])
        self.assertEqual(b['antardasha_at_birth']['lord'],'Ketu')
        self.assertLess(datetime.fromisoformat(b['full_md_antardashas'][0]['start_inclusive_utc']),birth)
        start=datetime(2000,1,1,tzinfo=timezone.utc);end=start+timedelta(days=7200)
        ads=antardashas('Venus',start,end)
        self.assertEqual([p['lord'] for p in ads],[p[0] for p in f['venus_antardasha_years']])
        for a,(_,years) in zip(ads,f['venus_antardasha_years']):
            days=(datetime.fromisoformat(a['end_exclusive_utc'])-datetime.fromisoformat(a['start_inclusive_utc'])).total_seconds()/86400
            self.assertAlmostEqual(days,years*360,places=8)
    def test_independent_vimshottari_both_years(self):
        f=json.loads(Path('tests/fixtures/vimshottari_reference.json').read_text())
        for c in f['cases']:
            n=d1(self.e,c['local'],c['zone'],c['latitude'],c['longitude'])
            r=vimshottari(datetime.fromisoformat(n['birth']['utc']),n['planets']['Moon']['longitude'],datetime.fromisoformat(c['target_utc']),c['year_key'])
            self.assertLess(abs(signed(n['planets']['Moon']['longitude']-c['moon_reference'])),f['moon_tolerance_degrees'])
            bound=f['moon_tolerance_degrees']*r['birth_balance']['full_md']['full_years']*r['year_days']*86400/(40/3)+.00001
            self.assertEqual(r['current']['mahadasa']['lord'],c['current_md'])
            self.assertEqual(r['current']['antardasha']['lord'],c['current_ad'])
            for actual,expected in [(r['birth_balance']['end_exclusive_utc'],c['birth_md_end_utc']),
                                    (r['current']['antardasha']['end_exclusive_utc'],c['current_ad_end_utc'])]:
                self.assertLess(abs((datetime.fromisoformat(actual)-datetime.fromisoformat(expected)).total_seconds()),bound)
    def test_exact_boundaries_reproducibility_and_invalid_scope(self):
        birth=datetime(2000,2,29,12,tzinfo=timezone.utc)
        r=vimshottari(birth,0,birth);boundary=datetime.fromisoformat(r['birth_balance']['end_exclusive_utc'])
        self.assertEqual(vimshottari(birth,0,boundary)['current']['mahadasa']['lord'],'Venus')
        self.assertEqual(vimshottari(birth,0,boundary-timedelta(microseconds=1))['current']['mahadasa']['lord'],'Ketu')
        ads=r['current_md_antardashas']
        for left,right in zip(ads,ads[1:]):
            self.assertEqual(left['end_exclusive_utc'],right['start_inclusive_utc'])
            t=datetime.fromisoformat(right['start_inclusive_utc'])
            self.assertEqual(vimshottari(birth,0,t)['current']['antardasha']['lord'],right['lord'])
        self.assertEqual(r,vimshottari(birth,0,birth))
        self.assertNotEqual(r['birth_balance']['end_exclusive_utc'],vimshottari(birth,0,birth,'solar-365.2425')['birth_balance']['end_exclusive_utc'])
        for args in [(birth,0,birth,'bad'),(birth,0,birth-timedelta(seconds=1)),(birth,0,birth.replace(tzinfo=None))]:
            with self.assertRaises(ValueError):vimshottari(*args)
        with self.assertRaises(ValueError):navamsa({'technique_id':1})
