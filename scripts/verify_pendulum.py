"""Independent pre-engine procedural fixtures and .NET categorical vectors."""
import hashlib
import json
from pathlib import Path
from future import pendulum as p


def run():
    counts={}
    cases=json.loads(Path('tests/fixtures/pendulum_source_cases.json').read_text(encoding='utf-8'))['cases']
    for case in cases:
        value=dict(schema_version=1,profile=p.PROFILE,task='symbolic_response',mode='manual',
            calibration=[dict(signal=s,response=r) for s,r in case['calibration']],
            observations=[dict(signal=case['signal'],quality=case.get('quality','full'))])
        assert p.read(value)['outcome']['symbolic_response']==case['expected']
    counts['independent_procedural_cases']=len(cases)
    vectors=json.loads(Path('tests/fixtures/pendulum_seed_vectors.json').read_text(encoding='utf-8'))['vectors']
    for v in vectors:
        stream=p.SymbolicStream(v['seed']);indices=[stream.below(5) for _ in range(32)]
        assert indices==v['indices'] and [p.category(n) for n in indices]==v['categories']
        assert hashlib.sha256(stream.prefix+bytes(8)).hexdigest()==v['first_block']
        assert (stream.counter,stream.rejections)==(v['blocks'],v['rejected_words'])
    counts['independent_seed_draws']=len(vectors)*32
    assert [p.category(n) for n in range(5)]==['yes','yes','no','no','unresolved']
    counts['exact_categorical_slots']=5
    class Forced(p.SymbolicStream):
        def __init__(self):super().__init__('forced');self.values=iter([4294967295,4294967294])
        def word(self):return next(self.values)
    stream=Forced();assert stream.below(5)==4 and stream.rejections==1
    counts['forced_rejection_boundary']=1
    report=dict(passed=True,checks=sum(counts.values()),counts=counts,independent_seed_vectors=len(vectors),
        assurance='Source-specific symbolic mapping and digital repeatability only;synthetic sessions,not predictive or physical-motion validation.')
    Path('data/pendulum-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(report['checks'],'Pendulum reference checks passed')


if __name__=='__main__':run()
