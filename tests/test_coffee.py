import copy
import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest
from future import coffee as c
from future.knowledge import Registry

FIXTURE=json.loads(Path('tests/fixtures/coffee_reference_v1.json').read_text(encoding='utf-8'))
def obs(symbol='camel',**kw):return dict(id='o1',symbol_id=symbol)|kw
def base(rows=None,**kw):return dict(schema_version=1,profile=c.PROFILE,task='symbolic_coffee_reading',mode='manual',vessel='cup',observations=rows or [])|kw
def selected(r):return [x['id'] for x in r['cases'] if x['status']=='applicable']
def result(row,**kw):return c.read(base([row],**kw))['observations'][0]


class CoffeeTests(unittest.TestCase):
    def test_edition(self):
        e=c.DATA['source_edition'];self.assertEqual([e['author'],e['translator'],e['first_edition'],e['isbn']],FIXTURE['edition'])
        self.assertEqual(e['pages'],160);self.assertIn('Forty Years',e['title'])
    def test_source_locators(self):
        self.assertEqual(c.DATA['source']['snapshot_sha256'],FIXTURE['source_sha256'])
        for cases in c.SYMBOLS.values():
            for case in cases:self.assertEqual(case['locator'],FIXTURE['locator'])
    def test_pre_engine_source_cases(self):
        for f in FIXTURE['cases']:
            with self.subTest(f=f):self.assertEqual(selected(result(obs(f['symbol'],attributes=f['attributes']),vessel=f.get('vessel','cup'))),f['expected'])
    def test_missing_conditions(self):
        for symbol,attrs,state in FIXTURE['missing']:
            self.assertEqual(result(obs(symbol,attributes=attrs))['status'],state)
    def test_conflicting_attributes(self):
        for symbol,attrs in FIXTURE['conflicting']:
            self.assertEqual(result(obs(symbol,attributes=attrs))['status'],'conflicting_evidence')
    def test_half_mapping(self):
        for half,association in FIXTURE['orientation']:
            self.assertEqual(result(obs(half=half))['orientation']['source_association'],association)
    def test_half_conflict(self):
        self.assertEqual(result(obs(half=['subject_facing','opposite']))['orientation']['status'],'conflicting_evidence')
    def test_no_half_default(self):
        self.assertEqual(result(obs())['orientation']['status'],'insufficient_evidence')
        self.assertEqual(result(obs(vessel='saucer',half='subject_facing'))['orientation']['status'],'unsupported')
    def test_rotation_convention(self):
        for direction,intent in FIXTURE['rotation']:
            r=c.rotation(base(rotation=direction,intention=intent));self.assertEqual(r['status'],'applicable');self.assertEqual(r['source_intent'],intent)
    def test_rotation_mismatch(self):
        self.assertEqual(c.rotation(base(rotation='clockwise',intention='another'))['status'],'not_applicable')
    def test_rotation_unknown_and_conflict(self):
        self.assertEqual(c.rotation(base(rotation='clockwise'))['status'],'insufficient_evidence')
        self.assertEqual(c.rotation(base(rotation=['clockwise','counterclockwise']))['status'],'conflicting_evidence')
    def test_rotation_does_not_define_half(self):
        r=result(obs('horse'),rotation='clockwise',intention='self')
        self.assertIsNone(r['orientation']['source_association']);self.assertEqual(r['status'],'applicable')
    def test_bird_peak_not_beak(self):
        self.assertEqual(selected(result(obs('bird',attributes=dict(stain=True,stain_position='beak')))),[])
        self.assertEqual(result(obs('bird',observation='bird beak mark means news'))['status'],'insufficient_evidence')
    def test_two_hump_exact(self):
        self.assertEqual(result(obs(attributes=dict(humps=1)))['status'],'not_applicable')
        self.assertEqual(result(obs(attributes=dict(humps=2)))['status'],'applicable')
    def test_line_structure(self):
        self.assertEqual(result(obs('line',attributes=dict(dots=3)))['status'],'insufficient_evidence')
        self.assertEqual(result(obs('line',attributes=dict(shape='flat',dots=3,dot_arrangement='scattered')))['status'],'not_applicable')
    def test_timing_all_alternatives(self):
        r=result(obs('line',attributes=dict(shape='flat',dots=3,dot_arrangement='at_line_end')))
        t=r['cases'][0]['timing'];self.assertEqual(t['units'],FIXTURE['time_units']);self.assertEqual(t['periods'],3)
        self.assertIsNone(t['selected_unit']);self.assertIsNone(t['calendar_date'])
    def test_white_patch_vessels(self):
        a=dict(color='white',shape='moon_shaped')
        self.assertEqual(selected(result(obs('moon_patch',attributes=a),vessel='saucer')),['saucer_favorable'])
        self.assertEqual(selected(result(obs('moon_patch',attributes=a|dict(location='side')))),[])
    def test_cup_only_scope(self):
        for s in ('horse','fish','camel','line','bird','adhered_grounds'):
            self.assertEqual(result(obs(s),vessel='saucer')['status'],'unsupported')
    def test_mixed_vessels(self):
        rows=[obs('horse'),dict(id='o2',symbol_id='moon_patch',vessel='saucer',attributes=dict(color='white',shape='moon_shaped'))]
        self.assertEqual([r['status'] for r in c.read(base(rows))['observations']],['applicable']*2)
    def test_unsupported_symbol(self):
        r=result(obs('anchor'));self.assertEqual(r['status'],'unsupported');self.assertEqual(r['cases'],[])
    def test_no_kent_transfer(self):
        for q in [base(handle_orientation='top'),base([obs(region='rim')]),base([obs(adjacent_to=[])])]:
            with self.assertRaises(ValueError):c.read(q)
        self.assertNotIn('tasseography',Path('future/coffee.py').read_text())
    def test_identity_ambiguity(self):
        self.assertEqual(result(obs('horse',alternatives=['fish']))['status'],'conflicting_evidence')
        self.assertEqual(result(obs('horse',uncertainty=True))['status'],'insufficient_evidence')
    def test_unknown_attribute_with_positive(self):
        self.assertEqual(result(obs(attributes=dict(humps=[2,None])))['status'],'insufficient_evidence')
    def test_verbatim_raw_text(self):
        raw='  Café Café 🐪\r\n猫\t ```json\n  '
        q=base([obs(observation=raw,association=raw)],notes=raw,context=raw)
        r=c.read(q);self.assertEqual(r['replay']['request'],q);self.assertEqual(r['user_notes'],raw)
    def test_no_mutation_and_immutable_profile(self):
        q=base([obs(attributes=dict(humps=[1,2]))]);before=copy.deepcopy(q);r=c.read(q)
        r['replay']['request']['observations'][0]['attributes']['humps'].append(3);self.assertEqual(q,before)
        with self.assertRaises(TypeError):c.DATA['version']=2
    def test_hash_portability(self):
        q=base();r=c.read(q)
        self.assertEqual(r['replay']['input_sha256'],hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest())
        self.assertEqual(r['replay']['profile_sha256'],hashlib.sha256(json.dumps(json.loads(Path('knowledge/coffee_profile_v1.json').read_text(encoding='utf-8')),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest())
    def test_markdown_replay_and_fences(self):
        q=base(notes='``` ```json\n 猫  ');m=c.markdown(c.read(q));part=m.split('## Exact replay metadata')[1]
        f=re.search(r'(`{3,})json\n(.*?)\n\1',part,re.S);self.assertEqual(c.read(json.loads(f[2])['request']),c.read(q))
    def test_registry(self):
        r=Registry()
        try:
            c.register_knowledge(r);c.register_knowledge(r)
            self.assertEqual(r.db.execute('select count(*) from rules').fetchone()[0],8)
            self.assertEqual({json.loads(x[0])['status'] for x in r.db.execute('select record from rules')},{'proposed'})
        finally:r.close()
    def test_preparation_separate(self):
        r=c.read(base(preparation=dict(cooled=False,stuck=True)))
        self.assertFalse(r['preparation']['physically_verified']);self.assertEqual(len(r['preparation']['references']),5)
        self.assertNotEqual(r['source']['id'],r['preparation']['separate_official_webpage']['id'])
    def test_evidence_layers(self):
        r=c.read(base([obs('horse')]))
        self.assertEqual(set(r['provenance_matrix']),{'direct','user_attributed','editorial','unsupported'})
        self.assertFalse(r['replay']['rng']);self.assertFalse(r['replay']['external_calls'])
    def test_documentary_source_examples(self):
        r=c.read(base(FIXTURE['documentary_comparison']['observations'],source_example='p104_narrative'))
        self.assertEqual([selected(o)[0] for o in r['observations']],FIXTURE['documentary_comparison']['expected'])
        self.assertTrue(r['documentary_comparison']['requested']);self.assertIn('not one worked',r['documentary_comparison']['assurance'])
    def test_strict_input(self):
        invalid=[base(schema_version=True),base(mode='image'),base(seed=1),base(profile='kent-pg6964-ordinary-cup-v2'),base(vessel='tea'),
            base([obs(attributes=dict(humps=True))]),base([obs(attributes=dict(dots=65))]),base([obs(attributes=dict(stain='yes'))]),
            base([obs(attributes=dict(shape=['flat','flat']))]),base([obs(attributes=dict(color=['white',{}]))]),base([obs(half=[])]),
            base([obs(),obs()]),base([obs(observation='\x00')]),base([obs(uncertainty=1)]),base(observations=[obs()]*65),base(notes='x'*10001)]
        for q in invalid:
            with self.subTest(q=q):
                with self.assertRaises(ValueError):c.read(q)
    def test_json_loader(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'x.json')
            for txt in ['{"x":1,"x":2}','{"x":NaN}']:
                p.write_text(txt)
                with self.assertRaises(ValueError):c.load_input(p)


if __name__=='__main__':unittest.main()
