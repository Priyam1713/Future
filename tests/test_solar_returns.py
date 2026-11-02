import unittest,json
from pathlib import Path
from datetime import datetime
from future.natal import SkyfieldEphemeris,chart,Settings,signed
from future.solar_returns import solar_return

class SolarReturnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.e=SkyfieldEphemeris('data/de440s.bsp')
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()
    def test_independent_years_positions_and_cusps(self):
        for f in json.loads(Path('tests/fixtures/solar_return_reference.json').read_text())['cases']:
            y,m,d,h=f['birth']
            n=chart(self.e,f'{y:04d}-{m:02d}-{d:02d}T{h:02d}:00:00','UTC',f['latitude'],f['longitude'])
            r=solar_return(self.e,n,f['year'],f['latitude'],f['longitude'])
            jd=float(self.e.ts.from_datetime(datetime.fromisoformat(r['exact_utc'])).tt)
            self.assertLess(abs(jd-f['jd_tt'])*86400,120)
            self.assertLess(r['solar_residual_degrees'],1e-5)
            for p,expected in zip(r['return_chart']['planets'].values(),f['longitudes']):
                self.assertLess(abs(signed(p['longitude']-expected)),.01)
            self.assertLess(max(abs(signed(a-b)) for a,b in zip(r['return_chart']['house_cusps'],f['placidus_cusps'])),.05)
    def test_relocation_and_calendar_validation(self):
        n=chart(self.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209)
        a=solar_return(self.e,n,2026,28.6139,77.209)
        b=solar_return(self.e,n,2026,-33.9,151.2,'regiomontanus')
        self.assertEqual(a['exact_utc'],b['exact_utc'])
        self.assertEqual([p['longitude'] for p in a['return_chart']['planets'].values()],
                         [p['longitude'] for p in b['return_chart']['planets'].values()])
        self.assertNotEqual(a['return_chart']['house_cusps'],b['return_chart']['house_cusps'])
        self.assertIn('unsupported',b['interpretation']['coverage'])
        for bad in (1849,2149,True):
            with self.assertRaises(ValueError):solar_return(self.e,n,bad,28,77)

if __name__=='__main__':unittest.main()
