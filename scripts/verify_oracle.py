"""Check independent historical transcription and .NET permutation evidence."""
import json
from pathlib import Path
from future.oracle import ORDER, PROFILE, card, draw


def run():
    f=json.loads(Path('tests/fixtures/oracle_source_examples.json').read_text(encoding='utf-8'))
    vectors=json.loads(Path('tests/fixtures/oracle_seed_vectors.json').read_text(encoding='utf-8'))['vectors']
    checks=[]
    for n,name in zip(f['numbers'],f['names']):
        c=card(ORDER[n-1]);assert c['number']==n and c['name']==name
        assert c['meaning']['locator'] and c['meaning']['source_id']==f['source_id']
        checks.append(dict(kind='inventory_and_locator',number=n,passed=True))
    for c in f['cases']:
        m=card(ORDER[c['number']-1])['meaning'];text=(m['text']+' '+m['context']).lower()
        assert all(t.lower() in text for t in c['motifs'])
        checks.append(dict(kind='independent_source_motifs',number=c['number'],passed=True))
    frozen=json.loads(Path('knowledge/oracle_pass1_findings.json').read_text(encoding='utf-8'))
    assert sum(f['example']['rows'],[])==frozen['source_example']['order']
    assert f['example']['rows'][0][4]==31 and f['example']['rows'][2][4]==33
    checks.append(dict(kind='historical_example_transcription',passed=True,perspective_discrepancy_preserved=True))
    for v in vectors:
        ids,pack,trace=draw(v['seed'],36)
        assert [card(k)['number'] for k in pack]==v['permutation']
        assert sorted(ids)==sorted(ORDER) and trace['cuts']==[]
        checks.append(dict(kind='independent_dotnet_full_deck',seed=v['seed'],passed=True))
    result=dict(profile=PROFILE,cards=36,source_backed_meanings=36,independent_full_deck_vectors=len(vectors),
        historical_motif_cases=len(f['cases']),historical_example_cases=1,passed=len(checks),checks=checks,
        predictive_validation=False,limits='Source and replay checks do not validate predictions.Near/far and perspective ambiguity remain unresolved;small layouts are editorial.')
    Path('data/oracle-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(len(checks),'Oracle verification checks passed')


if __name__=='__main__':run()
