import copy
import math
import unittest
from pathlib import Path
from unittest.mock import patch
from future import quantum_probability_forecasting as e
from future.scrying import load_input
from scripts.verify_quantum_probability_forecasting import negative_requests,verify

class QuantumProbabilityTests(unittest.TestCase):
    def test_all_twenty_independent_families(self):self.assertEqual(len(verify()['families']),20)
    def test_immutable_request(self):
        q=e.request('compare',gates=[dict(op='h',target=0)],shots=3);old=copy.deepcopy(q);r=e.read(q);self.assertEqual(q,old);r['request']['circuit']['gates'].clear();self.assertEqual(q,old)
    def test_p_preparation(self):
        for p in (0,.001,.2,.25,.5,.99,1):
            r=e.read(e.request(gates=[dict(op='ry',target=0,angle=2*math.asin(math.sqrt(p)))]))['result'];self.assertAlmostEqual(r['event']['ideal_model_probability'],p,places=12)
    def test_assets_tamper(self):
        old=e.load_input
        def changed(path):
            x=old(path)
            if str(path).endswith('profile_v1.json'):x['version']=2
            return x
        with patch.object(e,'load_input',changed):
            with self.assertRaises(ValueError):e.read(e.request())
    def test_source_tamper(self):
        q=e.request();old=e.load_input
        def changed(path):
            x=old(path)
            if str(path).endswith('sources.json'):x[0]['author']='other'
            return x
        with patch.object(e,'load_input',changed):
            with self.assertRaises(ValueError):e.read(q)
    def test_all_event_mappings(self):
        for n in range(1,5):
            for i in range(2**n):
                gates=[dict(op='x',target=t) for t in range(n) if i&(1<<t)]
                r=e.read(e.request('compare',n,gates,17,event=dict(kind='bitstring',value=format(i,f'0{n}b'))))['result'];self.assertEqual(r['sampling']['event_count'],17);self.assertEqual(r['classical']['count'],17)
    def test_every_shared_event(self):
        for n in range(1,5):
            gs=[dict(op='ry',target=t,angle=.712+t) for t in range(n)]
            for i in range(2**n):
                r=e.read(e.request('compare',n,gs,101,event=dict(kind='bitstring',value=format(i,f'0{n}b'))))['result'];self.assertEqual(r['sampling']['event_count'],r['classical']['count'])

for c in load_input(Path('tests/fixtures/quantum_probability_forecasting_reference_v1.json'))['circuits']:
    def test(self,c=c):
        r=e.read(e.request(qubits=c['qubits'],gates=c['gates']))['result']
        for a,x in zip(r['statevector'],c['state']):self.assertLessEqual(abs(a['real']-x[0]),1e-12);self.assertLessEqual(abs(a['imag']-x[1]),1e-12)
    setattr(QuantumProbabilityTests,'test_matrix_'+c['id'].replace('-','_'),test)
for name,q in negative_requests().items():
    def test(self,q=q):
        with self.assertRaises((ValueError,TypeError,KeyError,OverflowError)):e.read(q)
    setattr(QuantumProbabilityTests,'test_reject_'+name.replace('-','_'),test)
