"""Acceptance against pre-engine historical fixtures and independent .NET vectors."""
import hashlib
import json
from pathlib import Path
import unicodedata
from future import runes as r
from future.card_random import Stream


def run():
    ref=json.loads(Path('tests/fixtures/runes_inventory_reference.json').read_text(encoding='utf-8'))
    counts={}
    for n,k in enumerate(r.ORDER):
        item=r.rune(k)
        assert (item['position'],item['name'],item['transliteration'])==(ref['positions'][n],ref['names'][n],ref['transliterations'][n])
        assert ord(item['glyph'])==int(ref['codepoints'][n],16)
        assert item['unicode_name']==unicodedata.name(item['glyph'])
    counts['independent_inventory_entries']=24
    for k in r.ORDER:
        item=r.rune(k)
        assert item['historical_reference']['locator'] and item['association']['locator']
        assert not item['name_attested_as_elder_label']
        assert item['composition']['coverage']=='modern_editorial' and not item['composition']['ancient_rule']
    counts['source_layer_entries']=24
    assert sum(r.rune(k)['association']['lexical_association'] is not None for k in r.ORDER)==21
    for case in ref['source_cases']:
        item=r.rune(f"rune-{case['position']:02d}")
        if 'lexical' in case:assert item['association']['lexical_association']==case['lexical']
        if 'phonetic' in case:assert item['phonetic_value']==case['phonetic']
        if 'conflict_contains' in case:assert case['conflict_contains'] in ' '.join(item['conflicts']).lower()
    counts['independent_source_cases']=len(ref['source_cases'])
    vectors=json.loads(Path('tests/fixtures/runes_seed_vectors.json').read_text(encoding='utf-8'))['vectors']
    for v in vectors:
        selected,pack,_=r.draw(v['seed'],24)
        assert selected==pack and [r.rune(k)['position'] for k in pack]==v['permutation']
        assert hashlib.sha256(Stream(v['seed'],'deck').prefix+bytes(8)).hexdigest()==v['deck_first_block']
    counts['independent_full_set_vectors']=len(vectors)
    for n in range(1,25):
        selected,pack,_=r.draw('all-counts',n)
        assert len(set(selected))==n and selected==pack[:n]
    counts['draw_counts_without_replacement']=24
    report=dict(passed=True,checks=sum(counts.values()),counts=counts,
        assurance='Source fidelity and digital replay only;no published ancient divination examples or predictive validation claimed.')
    Path('data/runes-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(report['checks'],'rune reference checks passed')


if __name__=='__main__':run()
