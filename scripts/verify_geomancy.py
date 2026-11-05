"""Independent source expectations, exhaustive bit oracle and algebra verification."""
import hashlib
import itertools
import json
from pathlib import Path
from scripts.geomancy_reference import encode,decode,reference

def verify():
    from future import geomancy as g
    fixture_path=Path('tests/fixtures/geomancy_reference_v1.json')
    f=json.loads(fixture_path.read_text(encoding='utf-8'))
    freeze=json.loads(Path('knowledge/geomancy_source_freeze_v1.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(fixture_path.read_bytes()).hexdigest()==freeze['fixture_sha256']
    assert f['authored_before_engine'] and g.CONVENTION==f['figure_convention']
    assert len(g.FIGURES)==16 and len({x['id'] for x in g.FIGURES.values()})==16
    alias_count=0
    for expected in f['figures']:
        actual=g.lookup(expected['pattern'])
        assert all(actual[k]==expected[k] for k in ['id','name','pattern','aliases'])
        for name in [expected['id'],expected['name'],*expected['aliases']]:
            assert g.lookup(name.upper())==actual;alias_count+=1
    assert g.lookup('Puella')['pattern']=='1211' and g.lookup('Puer')['pattern']=='1121'
    for a,b,c in f['addition_truth_table']:assert g.add(str(a)*4,str(b)*4)==str(c)*4
    for row in f['charts']:
        assert reference(row['positions'][:4])==row['positions']
        assert g.chart(row['positions'][:4])==row['positions']
    patterns=[decode(i) for i in range(16)]
    pairs=0
    for a,b in itertools.product(patterns,repeat=2):
        actual=g.add(a,b)
        assert actual==decode(encode(a)^encode(b))
        assert actual in g.FIGURES and actual==g.add(b,a)
        assert g.add(a,a)=='2222'
        pairs+=1
    associative=0
    for a,b,c in itertools.product(patterns,repeat=3):
        assert g.add(g.add(a,b),c)==g.add(a,g.add(b,c));associative+=1
    charts=0
    parent_list=[(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)]
    for m in itertools.product(patterns,repeat=4):
        expected=reference(m);actual=g.chart(m)
        assert actual==expected and g.chart(m)==actual
        assert all(p in g.FIGURES for p in actual)
        assert [''.join(d[i] for d in actual[4:8]) for i in range(4)]==list(m)
        assert all(encode(actual[i+8])==encode(actual[a-1])^encode(actual[b-1]) for i,(a,b) in enumerate(parent_list))
        assert sum(map(int,actual[14]))%2==0
        charts+=1
    assert charts==65536 and pairs==256
    report=dict(passed=True,profile=g.PROFILE,profile_sha256=g.PROFILE_HASH,source_sha256=f['source']['snapshot_sha256'],
        figure_identities=16,alias_checks=alias_count,truth_table_rows=4,independent_charts=len(f['charts']),published_charts=1,
        exhaustive_mother_combinations=charts,addition_pairs=pairs,associativity_triples=associative,
        reference='scripts/geomancy_reference.py; independent top-bit-first 1=single/0=double bit matrix and XOR; no future imports',
        fixture_sha256=freeze['fixture_sha256'],invariants=['all fifteen positions match reference','all figure identities valid','transposition reconstruction','all parent dependencies','Judge even total-point parity','determinism','closure','commutativity','associativity','self-addition'],
        empirical_validation=False)
    Path('data/geomancy-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'{charts} independent Geomancy charts, {pairs} addition pairs, {associative} associative triples, 16 identities and {len(f["charts"])} fixtures passed')
    return report

if __name__=='__main__':verify()
