import unittest
import json
from pathlib import Path
from future.natal import *

class NatalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = SkyfieldEphemeris('data/de440s.bsp')

    def test_independent_swiss_reference(self):
        fixtures = json.loads(Path('tests/fixtures/swiss_reference.json').read_text())
        for f in fixtures['charts']:
            c = chart(self.e,f['local'],f['zone'],f['latitude'],f['longitude'])
            for name, expected in f['longitudes'].items():
                self.assertLess(abs(signed(c['planets'][name]['longitude']-expected)),.01,name)
                self.assertEqual(c['planets'][name]['retrograde'], f['retrograde'][name])
            for name in ('ascendant','midheaven'):
                self.assertLess(abs(signed(c['angles'][name]-f[name])),.02)
            equal=chart(self.e,f['local'],f['zone'],f['latitude'],f['longitude'],Settings(houses='equal'))
            for actual,expected in zip(equal['house_cusps'],f['equal_cusps']):
                self.assertLess(abs(signed(actual-expected)),.02)

    def test_domicile_extraction(self):
        from future.__main__ import load_registry
        from future.interpretations import explain
        r=load_registry()
        try:
            c=chart(self.e,'2000-08-01T12:00','Europe/London',51.5,0,Settings(tradition='medieval/traditional'))
            self.assertTrue(any(x['rule_id']=='traditional.domicile.sun' for x in explain(c,r)))
            c['planets']['Sun']['sign']='Virgo'
            self.assertFalse(any(x['rule_id']=='traditional.domicile.sun' for x in explain(c,r)))
            c['settings']['tradition']='Hellenistic'
            self.assertEqual(explain(c,r),[])
        finally: r.close()

    def test_dst(self):
        with self.assertRaises(ValueError): birth_utc('2024-03-10T02:30','America/New_York')
        with self.assertRaises(ValueError): birth_utc('2024-11-03T01:30','America/New_York')
        a=birth_utc('2024-11-03T01:30','America/New_York',0)
        b=birth_utc('2024-11-03T01:30','America/New_York',1)
        self.assertEqual((b-a).total_seconds(),3600)

    def test_boundaries_and_aspects(self):
        self.assertEqual(placement(360)['sign'],'Aries')
        self.assertEqual(placement(-.001)['sign'],'Pisces')
        self.assertEqual(placement(30)['sign'],'Taurus')
        self.assertEqual(len(aspects({'a':{'longitude':359},'b':{'longitude':1}},{0:2})),1)
        self.assertEqual(aspects({'a':{'longitude':359},'b':{'longitude':1}},{0:1}),[])

    def test_config_and_reproducibility(self):
        args=(self.e,'2000-01-01T12:00','Europe/London',51.4779,0)
        a=chart(*args)
        self.assertEqual(a,chart(*args))
        b=chart(*args,settings=Settings(houses='equal',tradition='Hellenistic'))
        self.assertNotEqual(a['house_cusps'],b['house_cusps'])
        self.assertEqual(len(b['planets']),7)
        for p in a['planets'].values(): self.assertTrue(1<=p['house']<=12)

    def test_documented_einstein_chart(self):
        # Astro-Databank uses local mean time, unlike Europe's later civil time.
        # Its published Sun 23 Pisces 30 and Moon 14 Sagittarius 32 are insensitive
        # to the ~13-minute distinction between Ulm LMT and Berlin historical LMT.
        c=chart(self.e,'1879-03-14T11:30','Europe/Berlin',48.4,10.)
        self.assertLess(abs(c['planets']['Sun']['longitude']-353.5),.03)
        self.assertLess(abs(c['planets']['Moon']['longitude']-254.533333),.15)

if __name__=='__main__': unittest.main()
