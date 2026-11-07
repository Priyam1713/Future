import copy,unittest
from unittest.mock import patch
from future.chaos_theory import read,assets,guard,rational
from scripts.verify_chaos_theory import fixture,case,vector,local_reference,stride_check
class ChaosTheoryTests(unittest.TestCase):
    def test_local_taylor_convergence(self):local_reference()
    def test_stride_preserves_integration(self):stride_check()
    def test_profile_tampering(self):
        import future.chaos_theory as m
        original=m.load_input
        def changed(path):
            x=original(path)
            if path.name=='chaos_theory_profile_v1.json':x['version']=2
            return x
        with patch.object(m,'load_input',side_effect=changed),self.assertRaises(ValueError):assets()
    def test_source_tampering(self):
        import future.chaos_theory as m
        original=m.load_input
        def changed(path):
            x=original(path)
            if path.name=='chaos_theory_sources.json':x[0]['author']='Changed'
            return x
        with patch.object(m,'load_input',side_effect=changed),self.assertRaises(ValueError):assets()
    def test_source_freeze_tampering(self):
        import future.chaos_theory as m
        original=m.load_input
        def changed(path):
            x=original(path)
            if path.name=='chaos_theory_source_freeze_v1.json':x['version']=2
            return x
        with patch.object(m,'load_input',side_effect=changed),self.assertRaises(ValueError):assets()
    def test_guard_nonfinite(self):
        for value in [float('nan'),float('inf'),-float('inf'),1000001]:
            with self.subTest(value=value),self.assertRaises(ValueError):guard((value,0.,0.))
    def test_repeatability(self):
        q=fixture()['cases']['one-step']['input'];self.assertEqual(read(q),read(copy.deepcopy(q)))
    def test_registry_idempotence(self):
        from future.knowledge import Registry
        registry=Registry(':memory:')
        try:
            q=fixture()['cases']['one-step']['input'];read(q,registry);n=registry.db.execute('SELECT COUNT(*) FROM sources').fetchone()[0];read(q,registry);self.assertEqual(n,5);self.assertEqual(registry.db.execute('SELECT COUNT(*) FROM sources').fetchone()[0],n)
        finally:registry.close()
def case_test(name):
    def test(self):case(name)
    return test
for name in fixture()['cases']:
    setattr(ChaosTheoryTests,'test_case_'+name.replace('-','_'),case_test(name))
for index,v in enumerate(fixture()['numerical_vectors']):
    setattr(ChaosTheoryTests,'test_vector_'+str(index),lambda self,v=v:vector(v))
