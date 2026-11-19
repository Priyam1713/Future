"""Project versioned chamber sources from local, rights-reviewed native catalogs."""
import json

from future import chinese, chinese_readings, iching_catalog, runes, vedic, vedic_timing
from future.natal import SIGNS
from .western import ROOT

OUT = ROOT / 'fate/web/src/chambers'


def build():
    hexagrams = [iching_catalog.hexagram(n) for n in range(1, 65)]
    stones = [runes.rune(key) for key in runes.ORDER]
    bazi = chinese_readings.CATALOG
    validation = dict(
        patterns=[h['pattern_bottom_to_top'] for h in hexagrams],
        runeIds=list(runes.ORDER),
        lords=list(dict.fromkeys(vedic_timing.ORDER)),
        profiles={str(n): p for n, p in [(2, vedic.PROFILE), (3, list(chinese.PROFILES)),
                                        (18, iching_catalog.PROFILE), (19, runes.PROFILE)]},
    )
    reference = dict(
        vedic=dict(signs=list(SIGNS), grahas=[*vedic.CLASSICAL, 'Rahu', 'Ketu'],
                   mansions=vedic.TABLES['nakshatras'], lords=vedic.TABLES['nakshatra_lords'],
                   sources=vedic.CONVENTIONS['sources'], rules=vedic.CONVENTIONS['rules']),
        bazi=dict(pairs=[chinese.pillar(i % 10, i % 12) for i in range(60)],
                  stems=[chinese.stem(i) for i in range(10)],
                  relations=[[chinese_readings.ten_god(i, j) for j in range(10)] for i in range(10)],
                  hidden=bazi['hidden_stems'], masters=bazi['day_master_components'],
                  topics=bazi['pillar_components'],
                  sources=json.loads((ROOT/'knowledge/chinese_sources.json').read_text(encoding='utf-8'))),
        iching=dict(figures=hexagrams, source=iching_catalog.thaw(iching_catalog.DATA['source'])),
        runes=dict(stones=stones, sources=[runes.thaw(runes.DATA[k]) for k in ('source', 'encoding_source', 'poem_source')]),
    )
    return validation, reference


if __name__ == '__main__':
    for name, value in zip(('edition-v1.json', 'reference-v1.json'), build()):
        output = json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n'
        path = OUT / name
        if path.exists() and path.read_text(encoding='utf-8') != output:
            raise SystemExit(f'{name} already exists with different contents. Create a new edition.')
        path.write_text(output, encoding='utf-8')
