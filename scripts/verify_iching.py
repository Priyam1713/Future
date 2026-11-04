"""Independent-reference acceptance checks;no production-generated expectations."""
import itertools
import json
from pathlib import Path
from future.iching import transform, values_for
from future.iching_cast import cast, coin_line, yarrow_value
from future.iching_catalog import PROFILE, hexagram, TRIGRAMS


def run():
    def load(name):return json.loads(Path('tests/fixtures',name).read_text(encoding='utf-8'))
    ref=load('iching_structure_reference.json');patterns=ref['patterns_by_king_wen']
    lookup={p:n for n,p in enumerate(patterns,1)}
    assert len(lookup)==64
    counts={}
    for n,p in enumerate(patterns,1):assert hexagram(n)['pattern_bottom_to_top']==list(map(int,p))
    counts['independent_king_wen_patterns']=64
    for p,name in ref['trigrams'].items():assert TRIGRAMS[p]['name']==name
    counts['independent_trigrams']=8
    checked=0
    for state in itertools.product([6,7,8,9],repeat=6):
        before=''.join(str(int(v in (7,9))) for v in state)
        after=''.join(str(int(v in (6,7))) for v in state)
        moving=[p for p,v in enumerate(state,1) if v%3==0]
        actual=transform(state)
        assert (actual['initial']['number'],actual['resulting']['number'])==(lookup[before],lookup[after])
        assert actual['moving_lines']==moving
        assert [t['resulting_yang'] for t in actual['trace']]==[v in (6,7) for v in state]
        checked+=1
    counts['exhaustive_six_value_states']=checked
    checked=0
    for n,p in enumerate(patterns,1):
        for mask in range(64):
            change=f'{mask:06b}'[::-1]
            expected=''.join('1' if a!=b else '0' for a,b in zip(p,change))
            actual=transform(values_for(list(map(int,p)),mask))
            assert actual['initial']['number']==n and actual['resulting']['number']==lookup[expected]
            checked+=1
    counts['exhaustive_pattern_change_masks']=checked
    outcomes=[coin_line(bits) for bits in itertools.product((0,1),repeat=3)]
    assert [outcomes.count(v) for v in [6,7,8,9]]==[1,3,3,1]
    counts['coin_equiprobable_outcomes']=8
    yarrow=[yarrow_value(index) for index in range(16)]
    assert [yarrow.count(v) for v in [6,7,8,9]]==[1,5,7,3]
    counts['yarrow_marginal_equiprobable_indices']=16
    vectors=load('iching_seed_vectors.json')['vectors']
    for v in vectors:
        values,trace=cast(v['seed'],v['method']);assert values==v['lines'] and trace['raw']==v['raw']
    counts['independent_dotnet_vectors']=len(vectors)
    coverage=0
    for n in range(1,65):
        h=hexagram(n)
        for text in [h['judgment'],*h['lines'],*([h['special_all_changing']] if n<3 else [])]:
            assert text['text'] and text['locator'] and text['source_id'] and text['pdf_pages'];coverage+=1
    counts['source_located_text_entries']=coverage
    source=load('iching_source_examples.json')
    for c in source['cases']:
        h=hexagram(c['number'])
        item=h['judgment'] if c['part']=='judgment' else h['special_all_changing'] if c['part']=='special' else h['lines'][c['part']-1]
        assert all(phrase in item['text'] for phrase in c['contains'])
        assert c['page']+36 in item['pdf_pages']
    counts['independent_scan_text_fixtures']=len(source['cases'])
    published=source['published_transformation'];r=transform([9]*6)
    assert r['initial']['number']==published['initial'] and r['resulting']['number']==published['result']
    counts['published_transformations']=1
    result=dict(profile=PROFILE,passed=True,checks=sum(counts.values()),counts=counts,
        judgments=64,ordinary_line_entries=384,special_entries=2,
        coin_weights=dict(zip(map(str,[6,7,8,9]),[1,3,3,1])),coin_denominator=8,
        yarrow_marginal_weights=dict(zip(map(str,[6,7,8,9]),[1,5,7,3])),yarrow_denominator=16,
        predictive_validation=False,limits='Independent visual pattern table,selected primary-scan text fixtures and .NET vectors;exhaustive mathematics,not full diplomatic text collation or empirical prediction validation.Physical stalk partitions not simulated.')
    Path('data/iching-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(sum(counts.values()),'I Ching verification checks passed')


if __name__=='__main__':run()
