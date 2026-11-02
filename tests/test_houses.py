import json,unittest
from pathlib import Path
from datetime import datetime
from future.houses import cusps,house_for,HouseGeometryError,frame
from future.natal import SkyfieldEphemeris,chart,Settings,signed

class HouseTests(unittest.TestCase):
    def test_independent_spherical_frames(self):
        fixture=json.loads(Path('tests/fixtures/house_reference.json').read_text())
        for f in fixture['frames']:
            for name,expected in f['systems'].items():
                with self.subTest(frame=f['armc'],lat=f['latitude'],system=name):
                    actual=cusps(f['armc'],f['latitude'],f['obliquity'],name)
                    self.assertLess(max(abs(signed(a-b)) for a,b in zip(actual,expected)),1e-6)
                    for i,a in enumerate(actual):
                        self.assertEqual(house_for(a,actual),i+1)
                        self.assertEqual(house_for((a+1e-7)%360,actual),i+1)
                        self.assertEqual(house_for((a-1e-7)%360,actual),(i-1)%12+1)
    def test_independent_dates_and_chart_integration(self):
        e=SkyfieldEphemeris('data/de440s.bsp')
        self.addCleanup(e.kernel.close)
        for f in json.loads(Path('tests/fixtures/house_reference.json').read_text())['dates']:
            for name,expected in f['systems'].items():
                t=e.ts.ut1_jd(f['jd_ut1'])
                armc,eps=frame(t,f['longitude'])
                actual=cusps(armc,f['latitude'],eps,name)
                self.assertLess(max(abs(signed(a-b)) for a,b in zip(actual,expected)),.02)
        for name in ('porphyry','placidus','regiomontanus','campanus'):
            c=chart(e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,Settings(houses=name))
            self.assertAlmostEqual(c['angles']['ascendant'],c['house_cusps'][0],places=9)
            self.assertAlmostEqual(c['angles']['midheaven'],c['house_cusps'][9],places=9)
    def test_high_latitude_and_no_fallback(self):
        for name in ('porphyry','placidus','regiomontanus','campanus'):
            with self.assertRaisesRegex(HouseGeometryError,'no fallback'):cusps(45,70,23.44,name)
        self.assertEqual(len(cusps(45,80,23.44,'equal')),12)
        self.assertEqual(len(cusps(45,-80,23.44,'whole-sign')),12)

if __name__=='__main__':unittest.main()
