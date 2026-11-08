import copy,unittest
from fractions import Fraction as F
from unittest.mock import patch
from future.multiverse import read,assets,checked
from scripts.multiverse_oracle import node
from scripts.verify_multiverse import fixture,case,vector,atoms,canonical
class MultiverseTests(unittest.TestCase):
    def test_atoms(self):atoms()
    def test_canonical(self):canonical()
    def test_repeatability(self):
        q=fixture()['cases']['reference']['input'];self.assertEqual(read(q),read(copy.deepcopy(q)))
    def asset_change(self,name):
        import future.multiverse as m
        original=m.load_input
        def changed(path):
            x=original(path)
            if path.name==name:
                if isinstance(x,list):x[0]['author']='Changed'
                else:x['version']=2
            return x
        with patch.object(m,'load_input',side_effect=changed),self.assertRaises(ValueError):assets()
    def test_profile_tampering(self):self.asset_change('multiverse_profile_v1.json')
    def test_source_tampering(self):self.asset_change('multiverse_sources.json')
    def test_source_freeze_tampering(self):self.asset_change('multiverse_source_freeze_v1.json')
    def test_fraction_bit_guard(self):
        with self.assertRaises(ValueError):checked(F(1<<8192))
        self.assertEqual(checked(F(1<<8191)),F(1<<8191))
    def test_isolated_depth_cap(self):
        q=fixture()['cases']['depth-over']['input'];q['queries']=[]
        with self.assertRaisesRegex(ValueError,'depth'):read(q)
    def test_isolated_node_cap(self):
        q=fixture()['cases']['reference']['input'];q['nodes']=[node('R',None,'1')]+[node('n'+str(i),'R','1/256','0') for i in range(256)];q['queries']=[]
        with self.assertRaisesRegex(ValueError,'Bounded list'):read(q)
    def test_isolated_query_cap(self):
        q=fixture()['cases']['reference']['input'];q['queries']=[dict(id='q'+str(i),given='R',target='A') for i in range(257)]
        with self.assertRaisesRegex(ValueError,'Bounded list'):read(q)
    def test_registry_idempotence(self):
        from future.knowledge import Registry
        reg=Registry(':memory:')
        try:
            q=fixture()['cases']['reference']['input'];read(q,reg);read(q,reg);self.assertEqual(reg.db.execute('SELECT COUNT(*) FROM sources').fetchone()[0],5)
        finally:reg.close()
    def test_narrative_does_not_change_math(self):
        q=fixture()['cases']['reference']['input'];a=read(q);q['scenario']['description']='A different fictional narrative.';b=read(q)
        for k in ['nodes','leaves','expected_utility','queries']:self.assertEqual(a[k],b[k])
        self.assertNotEqual(a['model_sha256'],b['model_sha256'])
def case_test(name):
    def test(self):case(name)
    return test
for name in fixture()['cases']:setattr(MultiverseTests,'test_case_'+name.replace('-','_'),case_test(name))
for i in range(len(fixture()['tree_vectors'])):setattr(MultiverseTests,'test_tree_'+str(i),lambda self,i=i:vector(i))
