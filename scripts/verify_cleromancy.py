"""Pre-engine source known answers and polynomial reference versus independent enumeration."""
import hashlib,itertools,json,math,sys
from collections import Counter
from pathlib import Path
from future import cleromancy_catalog as c
ROOT=Path(__file__).resolve().parents[1]
def get(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))

def reference():
    f=get('tests/fixtures/cleromancy_reference_v1.json');p,cat=c.assets()
    assert c.digest(f)==p['source_fixture_sha256']
    assert cat['marks']==f['marks'] and cat['aliases']==f['aliases']
    assert len(cat['marks'])==24 and c.integrity()['verified']
    for r in f['marks']:
        assert c.lookup(r['id'])['record']==r
        assert c.lookup(r['glyph'])['record']['glyph']==r['glyph']
        assert r['source_account'] and r['account_tag'] and r['lexical_qualification'] and r['locator']
    for raw,expected in f['aliases'].items():assert c.identify(raw)['canonical_id']==expected
    for x in f['normalized_cases']:assert c.identify(x['raw'])['canonical_id']==x['id']
    for raw in f['rejected_aliases']:
        try:c.identify(raw)
        except ValueError:pass
        else:raise AssertionError('Unexpected alias accepted: '+raw)
    ordered=0;spaces={}
    for row in f['numeric']:
        tuples=list(itertools.product(row['faces'],repeat=row['draws']))
        counts=Counter(map(sum,tuples));multisets=Counter(tuple(sorted(t)) for t in tuples)
        assert len(tuples)==row['ordered_count'] and len(multisets)==row['multiset_count']
        assert {str(k):counts[k] for k in sorted(counts)}==row['sum_counts']
        for key,multiplicity in multisets.items():
            assert multiplicity==math.factorial(len(key))//math.prod(math.factorial(n) for n in Counter(key).values())
        spaces[row['name']]=dict(ordered=len(tuples),unordered=len(multisets),sums=len(counts),distinct_sum_values=sorted(counts),multiplicities=sorted(set(multisets.values())))
        ordered+=len(tuples)
    bad=f['impossible_source_example'];assert sum(bad['faces'])==26 and set(bad['faces'])-{1,3,4,6}=={5} and not bad['accepted_vector']
    assert [x for x in range(5,31) if x not in spaces['five_astragaloi']['distinct_sum_values']]==[6,29]
    assert p['numeric_discrepancies']['unmapped_dice_sums']==[25,13] and 'caption' in p['numeric_discrepancies']['columns']
    return f,spaces,ordered

def verify():
    f,spaces,ordered=reference()
    from future import cleromancy as engine
    for r in f['marks']:
        q=dict(schema_version=1,profile=c.PROFILE,mode='manual',task='reading',catalog_id=c.DATA['catalog_id'],catalog_version=1,catalog_sha256=c.CATALOG_HASH,mark=r['id'],observation_origin='hypothetical')
        result=engine.read(q);assert result['selected_mark']==r and result['selection']['generated'] is False and result['selection']['probability'] is None
        assert engine.read(result['replay']['request'])==result
    out=dict(passed=True,profile=c.PROFILE,profile_sha256=c.PROFILE_HASH,catalog_sha256=c.CATALOG_HASH,source_record_sha256=c.DATA['source_record_sha256'],source_html_sha256=None,marks=24,source_accounts=24,alias_keys=len(f['aliases']),extra_normalization_cases=len(f['normalized_cases']),rejected_aliases=len(f['rejected_aliases']),spaces=spaces,ordered_research_tuples=ordered,impossible_face_example_preserved=True,numeric_mode_supported=False,reference='Pre-engine all24 source known answers; polynomial-convolution/binomial expectations checked by separate exhaustive tuple/multiset enumeration and multinomial multiplicities. No production sampler or meaning generator.',empirical_validation=False)
    (ROOT/'data/cleromancy-verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('24 Cleromancy source accounts;98 alias keys;9016 numerical research tuples;source discrepancies and exact replay passed')
    return out
if __name__=='__main__':
    if '--catalog-only' in sys.argv:
        f,s,n=reference();print('Standalone catalog passed:24 accounts,98 aliases,9016 mathematical tuples;no reading engine invoked')
    else:verify()
