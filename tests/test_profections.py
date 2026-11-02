import unittest
from datetime import datetime,timezone,timedelta
from future.natal import SkyfieldEphemeris,chart,Settings
from future.profections import annual,context,anniversary,register_knowledge

class ProfectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=SkyfieldEphemeris('data/de440s.bsp')
        cls.n=chart(cls.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,Settings(tradition='Hellenistic'))
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()
    def test_documented_cycles_and_boundaries(self):
        for age,house in [(0,1),(1,2),(11,12),(12,1),(24,1),(36,1),(38,3)]:
            t=datetime(1990+age,7,15,9,tzinfo=timezone.utc)
            r=annual(self.n,t)
            self.assertEqual((r['completed_age'],r['activated_house']),(age,house))
            if age:
                before=annual(self.n,t-timedelta(microseconds=1))
                self.assertEqual(before['completed_age'],age-1)
        r=context(self.e,self.n,datetime(2026,11,2,tzinfo=timezone.utc))
        self.assertEqual((r['activated_sign'],r['lord_of_year']),('Scorpio','Mars'))
        self.assertEqual(r['lord_natal_context']['conditions']['sect_affiliation'],'night')
        self.assertEqual(annual(self.n,datetime(2027,7,15,9,tzinfo=timezone.utc))['lord_of_year'],'Jupiter')
    def test_leap_year_policy_and_midnight(self):
        n=chart(self.e,'2000-02-29T12:00','UTC',-33.9,151.2,Settings(tradition='Hellenistic'))
        t=datetime(2001,2,28,12,tzinfo=timezone.utc)
        self.assertEqual(annual(n,t,leap_day='march-1')['completed_age'],0)
        self.assertEqual(annual(n,t,leap_day='february-28')['completed_age'],1)
        self.assertEqual(annual(n,datetime(2001,3,1,12,tzinfo=timezone.utc))['completed_age'],1)
        t=datetime(2004,2,29,0,tzinfo=timezone.utc)
        self.assertEqual(annual(n,t,boundary='midnight')['completed_age'],4)
        self.assertEqual(annual(n,t,boundary='birth-time')['completed_age'],3)
    def test_house_system_separation_and_input_validation(self):
        quadrant=chart(self.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,Settings(houses='placidus'))
        t=datetime(2026,11,2,tzinfo=timezone.utc)
        a,b=annual(self.n,t),annual(quadrant,t)
        self.assertEqual((a['activated_house'],a['activated_sign'],a['lord_of_year']),
                         (b['activated_house'],b['activated_sign'],b['lord_of_year']))
        self.assertEqual(b['conventions']['natal_house_system'],'placidus')
        with self.assertRaises(ValueError):annual(self.n,datetime(2026,1,1))
        with self.assertRaises(ValueError):annual(self.n,datetime(1980,1,1,tzinfo=timezone.utc))
        with self.assertRaises(ValueError):anniversary(self.n,2026,boundary='solar-return')
    def test_anniversary_dst_requires_explicit_resolution(self):
        n=chart(self.e,'2000-10-29T01:30','America/New_York',40.7,-74,Settings(tradition='Hellenistic'),fold=0)
        with self.assertRaises(ValueError):anniversary(n,2006)
        self.assertEqual((anniversary(n,2006,anniversary_fold=1)-anniversary(n,2006,anniversary_fold=0)).total_seconds(),3600)
    def test_registry_is_idempotent(self):
        from future.__main__ import load_registry
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            count=registry.db.execute("SELECT count(*) FROM rules WHERE id LIKE 'profection.%'").fetchone()[0]
            self.assertEqual(count,2)
        finally:registry.close()

if __name__=='__main__':unittest.main()
