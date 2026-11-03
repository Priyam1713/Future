import json
from pathlib import Path
from future.tarot_catalog import PROFILE,ORDER,card
from future.tarot import read
from future.card_random import PROTOCOL,shuffle_pack,orientations


def run():
    f=json.loads(Path('tests/fixtures/tarot_source_examples.json').read_text(encoding='utf-8'))
    vectors=json.loads(Path('tests/fixtures/tarot_seed_vectors.json').read_text(encoding='utf-8'))
    cases=[]
    for c in f['meaning_cases']:
        m=card(c['card_id'])['meanings'][c['orientation']]
        assert m['page']==c['page'] and all(t in m['text'] for t in c['contains'])
        cases.append(dict(kind='source_transcription',case=c['card_id']+'-'+c['orientation'],page=c['page'],phrases=c['contains'],passed=True))
    for i,v in enumerate(vectors['vectors']):
        pack,trace=shuffle_pack([str(n) for n in range(78) if n!=v['removed_index']],v['seed'],rounds=v['rounds'],cut=v['rounds']==3)
        assert list(map(int,pack))==v['permutation'] and trace['cuts']==v['cuts']
        assert [int(o=='reversed') for o in orientations(v['seed'],10,'seeded_reversals')]==v['orientation_bits']
        cases.append(dict(kind='independent_dotnet_vector',case=i,seed=v['seed'],rounds=v['rounds'],complete_permutation=True,cuts=trace['cuts'],passed=True))
    r=read(dict(schema_version=1,profile=PROFILE,task='symbolic_reading',mode='seeded',spread='waite_celtic',
        protocol=PROTOCOL,seed='Future-Tarot-v1',orientation_policy='seeded_reversals',significator=dict(card_id='major-11',facing='left',basis='matter')))
    for i,position in enumerate(f['celtic_positions']):
        assert r['readings'][i]['position']['id']==position
        cases.append(dict(kind='source_layout',case=i+1,position=position,passed=True))
    for number,side in f['facing_left_sides'].items():
        assert r['readings'][int(number)-1]['position']['placement']==side
        cases.append(dict(kind='source_layout',case='facing-left-'+number,side=side,passed=True))
    result=dict(profile=PROFILE,catalog_cards=78,orientation_meanings=156,source_checks=12,layout_checks=12,independent_seed_vectors=6,
        passed=len(cases),cases=cases,predictive_validation=False,
        limitations='Selected source fixtures independently transcribed from primary pages;source coverage is not predictive evidence. Digital protocol validated against separate .NET reference,not a claim of physical ritual equivalence.')
    Path('data/tarot-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Tarot source/layout/independent protocol checks passed')


if __name__=='__main__':run()
