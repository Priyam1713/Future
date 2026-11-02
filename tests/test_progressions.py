import unittest,json
from pathlib import Path
from datetime import datetime,timezone
from future.natal import SkyfieldEphemeris,Settings,signed
from future.progressions import progress,Clock

class ProgressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.e=SkyfieldEphemeris('data/de440s.bsp')
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()
    def test_independent_planets_and_angle_conventions(self):
        for f in json.loads(Path('tests/fixtures/progression_reference.json').read_text())['charts']:
            for method,systems in f['angle_cusps'].items():
                for system,expected in systems.items():
                    result=progress(self.e,f['birth_utc'].split('+')[0],'UTC',f['latitude'],f['longitude'],
                        datetime.fromisoformat(f['target_utc']),Settings(houses=system),year_key=f['year_key'],
                        angle_method=method,window_days=1)
                    self.assertAlmostEqual(result['progressed_epoch']['jd_tt'],f['jd_tt'],places=8)
                    for name,ref in f['planets'].items():
                        self.assertLess(abs(signed(result['planets'][name]['longitude']-ref['longitude'])),.01)
                        self.assertEqual(result['planets'][name]['retrograde'],ref['retrograde'])
                    self.assertLess(max(abs(signed(a-b)) for a,b in zip(result['house_cusps'],expected)),.02)
                    self.assertCountEqual([[r['progressed'],r['target'],r['aspect']] for r in result['progressed_to_natal_aspects']],f['progressed_to_natal'])
                    self.assertCountEqual([[r['progressed'],r['target'],r['aspect']] for r in result['progressed_to_progressed_aspects']],f['progressed_to_progressed'])
    def test_independent_moon_ingress(self):
        f=next(f for f in json.loads(Path('tests/fixtures/progression_reference.json').read_text())['charts'] if 'moon_virgo_ingress_utc' in f)
        report=progress(self.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,datetime(2026,11,2,tzinfo=timezone.utc))
        event=next(e for e in report['upcoming']['sign_changes'] if e['planet']=='Moon')
        y,m,d,h,mi,sec=f['moon_virgo_ingress_utc']
        expected=datetime(y,m,d,h,mi,int(sec),tzinfo=timezone.utc)
        self.assertLess(abs((datetime.fromisoformat(event['real_utc'])-expected).total_seconds()),3600)
        earlier=progress(self.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,datetime(2026,7,1,tzinfo=timezone.utc))
        newmoon=next(e for e in earlier['upcoming']['progressed_lunation_boundaries'] if e['phase']=='new')
        y,m,d,h,mi,sec=f['newmoon_before_target_utc']
        expected=datetime(y,m,d,h,mi,int(sec),tzinfo=timezone.utc)
        self.assertLess(abs((datetime.fromisoformat(newmoon['real_utc'])-expected).total_seconds()),3600)
    def test_explicit_conventions_and_reproducibility(self):
        args=(self.e,'2000-02-29T12:00','UTC',-33.9,151.2,datetime(2030,2,28,tzinfo=timezone.utc))
        a=progress(*args,angle_method='none',window_days=1)
        self.assertIsNone(a['angles']);self.assertIsNone(a['house_cusps'])
        self.assertEqual(a,progress(*args,angle_method='none',window_days=1))
        b=progress(*args,year_key='julian',angle_method='none',window_days=1)
        self.assertNotEqual(a['progressed_epoch']['jd_tt'],b['progressed_epoch']['jd_tt'])
        with self.assertRaises(ValueError):Clock(self.e,datetime(2000,1,1,tzinfo=timezone.utc),'bad')
        with self.assertRaises(ValueError):progress(*args,angle_method='primary-directions',window_days=1)
        with self.assertRaises(ValueError):progress(*args,settings=Settings(houses='placidus'),window_days=0)
    def test_knowledge_registry_preserves_method_scopes(self):
        from future.__main__ import load_registry
        from future.progressions import register_knowledge
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            rows=[json.loads(r['record']) for r in registry.db.execute('SELECT record FROM rules')]
            progressed=[r for r in rows if r['variation']=='secondary progressions']
            self.assertEqual(len(progressed),6)
            self.assertEqual({r['tradition'] for r in progressed},{'modern Western','Astrodienst','Cafe Astrology'})
            self.assertTrue(all(r['source_id'] and r['locator'] and r['status']=='proposed' for r in progressed))
        finally:registry.close()

if __name__=='__main__':unittest.main()
