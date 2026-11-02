import json,unittest,math
from pathlib import Path
from datetime import datetime
from future.natal import SkyfieldEphemeris,signed
from future.vedic import d1,nakshatra,dignity,ayanamsha,sector,graha_aspects,PROFILE,register_knowledge

class VedicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.e=SkyfieldEphemeris('data/de440s.bsp')
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()
    def test_independent_positions_ascendant_nodes_and_daynight(self):
        f=json.loads(Path('tests/fixtures/vedic_reference.json').read_text())
        states=set()
        for c in f['cases']:
            r=d1(self.e,c['local'],c['zone'],c['latitude'],c['longitude'])
            self.assertEqual(r['birth']['utc'],c['utc'])
            self.assertLess(abs(r['ayanamsha']['true_degrees']-c['ayanamsha_true'])*3600,1)
            self.assertLess(abs(signed(r['ascendant']['longitude']-c['ascendant'])),.02)
            for n,p in c['positions'].items():
                self.assertLess(abs(signed(r['planets'][n]['longitude']-p['longitude'])),.01,n)
                self.assertEqual(r['planets'][n]['retrograde'],p['retrograde'])
            self.assertAlmostEqual(abs(signed(r['planets']['Rahu']['longitude']-r['planets']['Ketu']['longitude'])),180)
            self.assertEqual(r['moon_nakshatra']['index'],c['moon_nakshatra_index'])
            self.assertEqual(r['moon_nakshatra']['pada'],c['moon_pada'])
            self.assertEqual(r['solar_horizon']['above_geometric_horizon'],c['sun_above_horizon'])
            states.add(c['sun_above_horizon'])
        self.assertEqual(states,{True,False})
    def test_published_chart1_complete_inputs(self):
        f=json.loads(Path('tests/fixtures/vedic_published.json').read_text())['chart1']
        utc=datetime.fromisoformat(f['utc'])
        r=d1(self.e,utc.replace(tzinfo=None).isoformat(),'UTC',f['latitude'],f['longitude'])
        self.assertEqual(r['ascendant']['sign_index'],int(f['ascendant']//30))
        self.assertIn('not claimed reproduced',f['ascendant_comparison'])
        self.assertGreater(abs(signed(r['ascendant']['longitude']-f['ascendant'])),.1)
        for n,p in f['longitudes'].items():self.assertLess(abs(signed(r['planets'][n]['longitude']-p)),f['tolerance_degrees'],n)
    def test_sign_nakshatra_pada_edges(self):
        for i in range(27):
            edge=i*360/27
            self.assertEqual(nakshatra(edge)['index'],i)
            self.assertEqual(nakshatra(edge)['pada'],1)
            self.assertEqual(nakshatra(edge-1e-7)['index'],(i-1)%27)
            self.assertEqual(nakshatra(edge+1e-7)['index'],i)
        self.assertEqual(nakshatra(360),nakshatra(0))
        self.assertEqual(nakshatra(-1e-7)['pada'],4)
        for i in range(108):self.assertEqual(nakshatra(i*360/108)['pada'],i%4+1)
        self.assertEqual(sector(30,12)[0],1)
        for v in (float('nan'),float('inf'),True):
            with self.assertRaises(ValueError):nakshatra(v)
    def test_dignity_and_documented_aspect_example34(self):
        self.assertIn('exaltation_sign',dignity('Jupiter',95)['flags'])
        self.assertTrue(dignity('Mercury',165)['moolatrikona'])
        self.assertFalse(dignity('Mercury',170)['moolatrikona'])
        self.assertIsInstance(dignity('Mars',1)['moolatrikona'],str)
        self.assertIn('unsupported',dignity('Rahu',1)['coverage'])
        p={n:{'sign_index':0} for n in ('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn')}
        p['Jupiter']['sign_index']=2;p['Mars']['sign_index']=4;p['Saturn']['sign_index']=8
        r=graha_aspects(p)
        self.assertEqual([x['target_sign'] for x in r if x['from']=='Jupiter'],['Libra','Sagittarius','Aquarius'])
        self.assertEqual([x['target_sign'] for x in r if x['from']=='Mars'],['Scorpio','Aquarius','Pisces'])
        self.assertEqual([x['target_sign'] for x in r if x['from']=='Saturn'],['Aquarius','Gemini','Virgo'])
    def test_anchor_input_scope_registry_and_reproducibility(self):
        a=ayanamsha(self.e.ts,self.e.ts.tt_jd(2435553.5))
        self.assertAlmostEqual(a['true_degrees'],23.25+.658/3600,places=10)
        args=(self.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209)
        self.assertEqual(d1(*args),d1(*args))
        with self.assertRaises(ValueError):d1(*args,profile='KP')
        with self.assertRaises(ValueError):d1(self.e,'2000-01-01','UTC',70,0)
        with self.assertRaises(ValueError):d1(self.e,'2024-03-10T02:30','America/New_York',40,-74)
        from future.__main__ import load_registry
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            rows=[json.loads(x[0]) for x in registry.db.execute('select record from rules')]
            self.assertEqual(sum(x['technique_id']==2 for x in rows),7)
            self.assertTrue(all(x['tradition']==PROFILE for x in rows if x['technique_id']==2))
        finally:registry.close()
