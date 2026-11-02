import unittest
from future.numerology import calculate,reduce

class NumerologyTests(unittest.TestCase):
    def run_case(self,b='1998-10-15',n='Thomas Cruise Mapother',t='2026-10-12',y=''):
        return calculate(b,n,'birth',t,y)
    def test_published(self):
        r=self.run_case()
        self.assertEqual([p['result'] for p in r['life_path']['components']],[1,6,9]);self.assertEqual(r['life_path']['steps'],[16,7])
        self.assertEqual([p['result'] for p in r['expression']['components']],[22,3,6]);self.assertEqual(r['expression']['steps'],[31,4])
        r=self.run_case(n='Thomas John Hancock');self.assertEqual(r['soul_urge']['steps'],[20,2])
        self.assertEqual(r['personality']['steps'],[14,5])
        r=self.run_case(b='1990-09-12');self.assertEqual([r['cycles'][k]['result'] for k in ('sun','year','month','day')],[3,4,5,8])
    def test_independent_mapping_and_masters(self):
        groups=['AJS','BKT','CLU','DMV','ENW','FOX','GPY','HQZ','IR']
        for value,letters in enumerate(groups,1):
            for c in letters:
                r=self.run_case(n=c,y='v' if c=='Y' else '')
                self.assertEqual(r['expression']['input'],value)
        for n in range(1,1000):self.assertEqual(reduce(n,False)['result'],1+(n-1)%9)
        for n in (11,22,33):self.assertEqual(reduce(n)['result'],n)
    def test_inputs(self):
        for n in ('José','李','A2','-Anne','Anne--Marie',' A','A\tB',''):
            with self.assertRaises(ValueError):self.run_case(n=n)
        for b in ('1900-02-29','2026-13-01'):
            with self.assertRaises(ValueError):self.run_case(b=b)
        self.run_case(b='2000-02-29')
        with self.assertRaises(ValueError):self.run_case(n='Yy')
        r=self.run_case(n='Yy',y='vc');self.assertEqual(r['soul_urge']['result'],7)
        self.assertEqual(self.run_case(n="Anne-Marie O'Neil")['name']['tokens'][0]['part'],'ANNE-MARIE')
    def test_boundaries_and_reproducibility(self):
        a=self.run_case(t='2025-12-31');b=self.run_case(t='2026-01-01')
        self.assertNotEqual(a['cycles']['year']['result'],b['cycles']['year']['result'])
        self.assertEqual(self.run_case(),self.run_case())
        with self.assertRaises(ValueError):calculate('2000-01-01','A','other','2026-01-01')
