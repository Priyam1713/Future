import json,unittest
from pathlib import Path
from datetime import datetime
from future.natal import SkyfieldEphemeris
from future.lunar_sequence import sequence
from future.elections import REQUIREMENTS

class LunarSequenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.e=SkyfieldEphemeris('data/de440s.bsp')
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()
    def test_independent_contacts_ingresses_and_station(self):
        f=json.loads(Path('tests/fixtures/lunar_reference.json').read_text())
        stations=0
        for case in f['cases']:
            start=datetime.fromisoformat(case['start_utc']);r=sequence(self.e,start)
            self.assertEqual(len(r['events']),len(case['events']))
            for actual,expected in zip(r['events'],case['events']):
                self.assertEqual(actual['type'],expected['type'])
                self.assertEqual(actual.get('target'),expected.get('target'))
                self.assertEqual(actual.get('aspect_degrees'),expected.get('aspect_degrees'))
                self.assertLess(abs((datetime.fromisoformat(actual['utc'])-start).total_seconds()-expected['seconds_from_start']),f['tolerance_seconds'])
                if actual['type']=='exact_aspect':
                    self.assertLess(actual['residual_degrees'],.0001)
                    self.assertEqual(actual['phase_before'],'applying');self.assertEqual(actual['phase_after'],'separating')
                stations+=actual['type']=='target_station'
            for i,x in enumerate(r['contacts_before_ingress']):
                self.assertLess(x['utc'],r['next_moon_ingress_utc'])
                self.assertEqual(len(x['intervening_contacts']),i)
                self.assertIn('indeterminate',x['historical_prohibition'])
        self.assertGreater(stations,0)
    def test_scope_and_input(self):
        self.assertEqual(REQUIREMENTS['category'],'retain-received-money')
        self.assertTrue(any(r['status']=='unsupported' for r in REQUIREMENTS['rules']))
        self.assertTrue(all(r['locator'] and r['exception'] for r in REQUIREMENTS['rules']))
        with self.assertRaises(ValueError):sequence(self.e,datetime(2026,1,1))
        with self.assertRaises(ValueError):sequence(self.e,datetime.fromisoformat('2026-01-01T00:00:00+00:00'),9)
