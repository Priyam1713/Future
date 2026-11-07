import copy,unittest
from fractions import Fraction as F
from future.brain_intention import read,checked,rational,extract,score
from scripts.verify_brain_intention import fixture,check_case,literal_checks
class BrainIntentionTests(unittest.TestCase):
    def test_literal_anchors(self):literal_checks()
    def test_test_label_isolation(self):
        f=fixture();a=read(f['cases']['worked']['input']);b=read(f['cases']['test-label-flip']['input'])
        self.assertEqual(a['model_sha256'],b['model_sha256']);self.assertEqual(a['predictions'],b['predictions']);self.assertNotEqual(a['evaluation'],b['evaluation'])
    def test_test_features_do_not_fit(self):
        q=copy.deepcopy(fixture()['cases']['worked']['input']);a=read(q);q['trials'][4]['values']=[100,100];b=read(q)
        self.assertEqual(a['model_sha256'],b['model_sha256']);self.assertNotEqual(a['predictions'],b['predictions'])
    def test_sample_population_distinction(self):
        self.assertEqual(extract([[F(-1),F(1),F(-1),F(1)]]),[0,1]);self.assertNotEqual(F(4,3),1)
    def test_absent_class(self):
        r=score(['A','A'],['A','B']);self.assertEqual(r['accuracy'],'1/2');self.assertIsNone(r['balanced_accuracy']);self.assertEqual(r['status'],'not_estimable')
    def test_bit_reservation(self):
        with self.assertRaisesRegex(ValueError,'bit reservation'):checked(F(1,2**8190),F(1,2**8190),'mul')
    def test_rational_rejections(self):
        for x in [True,1.0,'1e2','-0','01','1/-2','1/0',10**18]:
            with self.subTest(x=x),self.assertRaises(ValueError):rational(x)
    def test_raw_cap(self):
        q=copy.deepcopy(fixture()['cases']['windows']['input']);q['channels']=[dict(id='c'+str(i),unit='arbitrary_units') for i in range(8)];q['fit_at']=10**7;q['trials']=[]
        template=fixture()['cases']['windows']['input']['trials'][0]
        for i in range(128):
            t=copy.deepcopy(template);t.update(id='t'+str(i),trial_id='trial'+str(i),source_id='s'+str(i),subject='p'+str(i),start=0,end=512,available_at=600,predict_at=10**8,label_available_at=10**8+1 if i>=2 else 700,partition='TRAIN' if i<2 else 'TEST',label='A' if i%2==0 else 'B',values=[[0]*512 for _ in range(8)]);q['trials'].append(t)
        with self.assertRaisesRegex(ValueError,'raw cell cap'):read(q)
def make_case(case):
    def test(self):check_case(case)
    return test
for name,c in fixture()['cases'].items():setattr(BrainIntentionTests,'test_fixture_'+name.replace('-','_'),make_case(c))
if __name__=='__main__':unittest.main()
