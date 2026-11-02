from copy import deepcopy
from pathlib import Path
import json,unittest
from future.chinese import chart,STEMS,GAN,ZHI,CONVENTIONS
from future.chinese_readings import ten_god,enrich,register_knowledge,CATALOG,markdown
from future.natal import SkyfieldEphemeris
from future.__main__ import load_registry

ROOT=Path(__file__).resolve().parents[1]

class ChineseReadingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=SkyfieldEphemeris(ROOT/'data/de440s.bsp')
        cls.refs=json.loads((ROOT/'tests/fixtures/chinese_reference.json').read_text(encoding='utf-8'))
    @classmethod
    def tearDownClass(cls):cls.e.kernel.close()

    def test_all100_independent_relations_and_published_examples(self):
        for a in range(10):
            for b in range(10):
                r=ten_god(a,b)
                self.assertEqual(r['character'],self.refs['ten_gods'][GAN[a]+GAN[b]])
                self.assertEqual(r['source_id'],'chinese-tan-ten-gods-v1')
        pub=json.loads((ROOT/'tests/fixtures/chinese_published.json').read_text(encoding='utf-8'))
        for f in pub['relationships']:
            self.assertEqual(ten_god(STEMS.index(f['self']),STEMS.index(f['other']))['name'],f['label'])
        # Tan printedp79 ten explicitly listed Direct Wealth examples.
        for a,b in [(0,5),(1,4),(2,7),(3,6),(4,9),(5,8),(6,1),(7,0),(8,3),(9,2)]:
            self.assertEqual(ten_god(a,b)['name'],'Direct Wealth')
        for bad in [-1,10,True,1.5,'0']:
            with self.assertRaises(ValueError):ten_god(bad,0)

    def test_hidden_memberships_and_classical_variant_isolation(self):
        for branch,indices in zip(ZHI,CATALOG['hidden_stems']['stems_by_branch']):
            self.assertEqual({GAN[i] for i in indices},set(self.refs['hidden_stems'][branch]))
        self.assertEqual(CATALOG['hidden_stems']['profile'],'modern-fixed-sets-six-tail')
        self.assertIn('San Ming',CATALOG['hidden_stems']['exception'])
        # Modern Zi contains Gui only; San Ming seasonal allocations are not
        # unioned into it or turned into numerical percentages.
        self.assertEqual(CATALOG['hidden_stems']['stems_by_branch'][0],[9])

    def test_published_chart_context_no_mutation_and_composition(self):
        n=chart(self.e,'1918-12-01T12:30','Asia/Shanghai',0,120)
        saved=deepcopy(n);r=enrich(n)
        self.assertEqual(n,saved)
        self.assertEqual(r['pillars']['hour']['ten_god']['name'],'Indirect Wealth')
        self.assertEqual([h['ten_god']['name'] for h in r['pillars']['hour']['hidden_stems']],['Direct Wealth','Direct Officer'])
        self.assertEqual(r['reading']['day_master']['coverage'],'direct')
        self.assertTrue(all(x['coverage']=='compositional' for x in r['reading']['pillars']))
        self.assertEqual(sum(r['reading']['ten_god_occurrences']['visible_excluding_day_master'].values()),3)
        self.assertEqual(len(r['reading']['element_interactions']),12)
        self.assertEqual(r['luck_pillars']['status'],'unsupported')
        self.assertNotIn('score',r['reading'])
        self.assertEqual(r,enrich(n))
        text=markdown(r)
        self.assertIn('compositional',text);self.assertIn('printedpp73',text)
        self.assertIn('unsupported',text)
        for id in (1,2,4):
            bad=deepcopy(n);bad['technique_id']=id
            with self.assertRaises(ValueError):enrich(bad)

    def test_rule_source_locators_and_inventory_preservation(self):
        registry=load_registry()
        try:
            register_knowledge(registry);register_knowledge(registry)
            for c in CATALOG['day_master_components']+CATALOG['pillar_components']:
                self.assertTrue(c['locator'] and c['limitation'])
                self.assertIsNotNone(registry.db.execute('SELECT id FROM sources WHERE id=?',(c['source_id'],)).fetchone())
            self.assertEqual(len(CATALOG['day_master_components']),10)
            self.assertEqual(len(CATALOG['pillar_components']),4)
        finally:registry.close()
        inventory=json.loads((ROOT/'knowledge/inventory.json').read_text(encoding='utf-8'))
        variations=[r[2] for r in inventory['sheets']['Variations'] if r[0]==3]
        self.assertEqual(len(variations),5)
        self.assertIn('Zi Wei Dou Shu',variations);self.assertIn('Nine Star Ki',variations)
        release=json.loads((ROOT/'knowledge/chinese_core_v1.json').read_text(encoding='utf-8'))
        self.assertEqual(release['status'],'Core v1 Ready')
        self.assertEqual(len(release['supported']['profiles']),3)
        self.assertIn('Luck-pillar starting ages, absolute onset and personal timing forecasts',release['unsupported'])

if __name__=='__main__':unittest.main()
