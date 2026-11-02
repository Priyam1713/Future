import unittest,json
from pathlib import Path
from datetime import datetime,timezone,timedelta
from future.natal import SkyfieldEphemeris
from future.elections import search,evaluate,profile_for,CATALOG,register_knowledge

class ElectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=SkyfieldEphemeris('data/de440s.bsp')
        cls.f=json.loads(Path('tests/fixtures/election_reference.json').read_text())
        cls.a=datetime.fromisoformat(cls.f['start_utc']);cls.b=datetime.fromisoformat(cls.f['end_exclusive_utc'])
        cls.report=search(cls.e,'retain-received-money',cls.a,cls.b,cls.f['latitude'],cls.f['longitude'])
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()
    def test_independent_minute_grid_completeness(self):
        windows=[(datetime.fromisoformat(c['start_inclusive_utc']),datetime.fromisoformat(c['end_exclusive_utc'])) for c in self.report['candidates']]
        self.assertTrue(windows)
        for i in range(self.f['minute_samples']):
            t=self.a+timedelta(seconds=30+60*i)
            actual=any(a<=t<b for a,b in windows)
            expected=any(a<=i<b for a,b in self.f['true_index_runs'])
            self.assertEqual(actual,expected,f'Independent minute sample {i}')
        for i,(a,b) in enumerate(windows):
            self.assertLess(a,b)
            if i:self.assertLessEqual(windows[i-1][1],a)
        for c in self.report['candidates']:
            self.assertTrue(all(r['status']=='satisfied' for r in c['rule_trace']['rules'] if r['required']))
            self.assertTrue(c['diagnostics']['source_rules'])
            self.assertTrue(c['diagnostics']['sect'])
            self.assertTrue(self.report['unknown_criteria'])
    def test_profiles_source_rules_and_conflicts(self):
        fixed=profile_for('ramesey-retain-money','retain-received-money')
        fast=profile_for('ramesey-rapid-use-money','rapid-use-received-money')
        signs={n:4 for n in ('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn')}
        speeds={n:1 for n in signs}
        self.assertTrue(evaluate(signs,speeds,30,120,60,fixed)['passes_selected_rules'])
        self.assertFalse(evaluate(signs,speeds,30,120,60,fast)['passes_selected_rules'])
        speeds['Venus']=-.1
        self.assertFalse(evaluate(signs,speeds,30,120,60,fixed)['passes_selected_rules'])
        with self.assertRaises(ValueError):profile_for('ramesey-retain-money','rapid-use-received-money')
        with self.assertRaises(ValueError):profile_for('ramesey-retain-money','retain-received-money','Dorotheus')
        r=search(self.e,'retain-received-money',self.a,self.a+timedelta(hours=3),28.6139,77.209,ascendant_signs=[0,3,6,9])
        self.assertTrue(r['conflicts']);self.assertFalse(r['candidates'])
    def test_resolution_reproducibility_and_constraints(self):
        again=search(self.e,'retain-received-money',self.a,self.b,28.6139,77.209,angle_step_minutes=5)
        a=self.report['candidates'];b=again['candidates']
        self.assertEqual(len(a),len(b))
        for x,y in zip(a,b):
            for key in ('start_inclusive_utc','end_exclusive_utc'):
                self.assertLess(abs((datetime.fromisoformat(x[key])-datetime.fromisoformat(y[key])).total_seconds()),.5)
        filtered=search(self.e,'retain-received-money',self.a,self.b,28.6139,77.209,utc_hours=(18,19))
        for c in filtered['candidates']:
            start=datetime.fromisoformat(c['start_inclusive_utc']);end=datetime.fromisoformat(c['end_exclusive_utc'])
            self.assertGreaterEqual(start,start.replace(hour=18,minute=0,second=0,microsecond=0))
            self.assertLessEqual(end,start.replace(hour=19,minute=0,second=0,microsecond=0))
        with self.assertRaises(ValueError):search(self.e,'retain-received-money',self.a,self.b,70,0)
        with self.assertRaises(ValueError):search(self.e,'retain-received-money',self.a,self.b,28,77,required=['invented-score'])
    def test_registry_and_pattern_geometry(self):
        from future.__main__ import load_registry
        from future.solar_returns import aspect_patterns
        r=load_registry()
        try:register_knowledge(r);register_knowledge(r)
        finally:r.close()
        pattern=aspect_patterns([{'bodies':['A','B'],'angle':180},{'bodies':['A','C'],'angle':90},{'bodies':['B','C'],'angle':90}])
        self.assertEqual(pattern['geometric_patterns'][0]['type'],'T-square')

if __name__=='__main__':unittest.main()
