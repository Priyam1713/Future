import unittest
from copy import deepcopy
from datetime import datetime,timezone
from future.natal import SkyfieldEphemeris,chart,Settings
from future.core_readings import placements,progression_context,return_context,register_knowledge,DATA
from future.__main__ import load_registry

class CoreReadingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=SkyfieldEphemeris('data/de440s.bsp')
        cls.n=chart(cls.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209)
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()
    def test_natal_components_follow_computed_house_and_school(self):
        registry=load_registry()
        try:
            r=placements(self.n,registry)
            sun=next(p for p in r['placements'] if p['planet']=='Sun')
            self.assertEqual(sun['house'],self.n['planets']['Sun']['house'])
            self.assertEqual(sun['coverage'],'compositional')
            self.assertTrue(any(p['id']=='core.modern.symbol.sun' for p in sun['components']))
            self.assertTrue(any(p['id']==f"core.modern.house.{sun['house']}" for p in sun['components']))
            self.assertTrue(all(p['tradition']=='modern psychological' and p['url'] and p['locator'] for p in sun['components']))
            self.assertTrue(all(a['direct_pair_coverage']=='unsupported' for a in r['aspects']))
            traditional=chart(self.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,Settings(tradition='medieval/traditional'))
            r=placements(traditional,registry)
            self.assertTrue(any(p['components'] for p in r['placements']))
            self.assertFalse(any(x['id'].startswith('core.modern') for p in r['placements'] for x in p['components']))
            h=deepcopy(traditional);h['settings']['tradition']='Hellenistic'
            self.assertTrue(all(p['coverage']=='unsupported' for p in placements(h,registry)['placements']))
        finally:registry.close()
    def test_progressed_phase_and_house_not_transit_pair(self):
        p={'Moon':{'natal_house':4}}
        r=progression_context(self.n,p,'first quarter')
        self.assertEqual({c['id'] for c in r['components']},{'core.progression.phase.first-quarter','core.modern.house.4'})
        self.assertIn('construction',r['components'][1]['text'])
        for phase in ('new','crescent','first quarter','gibbous','full','disseminating','last quarter','balsamic'):
            self.assertEqual(sum(c['id'].startswith('core.progression.phase') for c in progression_context(self.n,p,phase)['components']),1)
        n=deepcopy(self.n);n['settings']['tradition']='Hellenistic'
        self.assertEqual(progression_context(n,p,'full')['coverage'],'unsupported')
    def test_return_retrograde_conditions_and_house_profile(self):
        n=deepcopy(self.n);n['settings']['houses']='placidus'
        n['planets']['Mercury']['retrograde']=True
        r=return_context(n)
        mercury=next(x for x in r['placements'] if x['planet']=='Mercury')
        self.assertEqual(mercury['retrograde_reading'][0]['id'],'core.return.retrograde.mercury')
        self.assertFalse(next(x for x in r['placements'] if x['planet']=='Pluto')['retrograde_reading'])
        n['planets']['Mercury']['retrograde']=False
        self.assertFalse(next(x for x in return_context(n)['placements'] if x['planet']=='Mercury')['retrograde_reading'])
        n['settings']['houses']='equal'
        self.assertEqual(return_context(n)['coverage'],'unsupported')
    def test_registry_provenance_immutable_and_no_missing_context(self):
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            for r in DATA['records']:
                self.assertTrue(r['source_id'] and r['locator'] and r['exceptions'])
            self.assertEqual(registry.db.execute("select count(*) from rules where id like 'core.%'").fetchone()[0],27)
        finally:registry.close()
