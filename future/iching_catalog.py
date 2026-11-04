"""Immutable Legge1882 source text and explicit King Wen pattern inventory."""
import hashlib
import json
from pathlib import Path
from types import MappingProxyType
from .knowledge import Rule


def freeze(x):
    if isinstance(x, dict): return MappingProxyType({k: freeze(v) for k, v in x.items()})
    if isinstance(x, list): return tuple(freeze(v) for v in x)
    return x


def thaw(x):
    if isinstance(x, (dict, MappingProxyType)): return {k: thaw(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [thaw(v) for v in x]
    return x


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(',', ':')).encode('utf-8')).hexdigest()


ROOT = Path(__file__).resolve().parents[1]
DATA = freeze(json.loads((ROOT/'knowledge/iching_legge1882_v1.json').read_text(encoding='utf-8')))
CONVENTIONS = freeze(json.loads((ROOT/'knowledge/iching_conventions_v1.json').read_text(encoding='utf-8')))
PROFILE = DATA['profile']
POLICY = CONVENTIONS['reading_policy']['id']
HEXAGRAMS = DATA['hexagrams']
PATTERNS = MappingProxyType({tuple(h['pattern_bottom_to_top']): h['number'] for h in HEXAGRAMS.values()})
TRIGRAMS = DATA['trigrams']
CATALOG_DIGEST = digest(thaw(DATA))
CONVENTION_DIGEST = digest(thaw(CONVENTIONS))
assert len(HEXAGRAMS) == len(PATTERNS) == 64 and len(TRIGRAMS) == 8


def hexagram(number):
    if type(number) is not int or not 1 <= number <= 64:
        raise ValueError('King Wen number must be integer1..64')
    return thaw(HEXAGRAMS[str(number)])


def register_knowledge(registry):
    sources = json.loads((ROOT/'knowledge/iching_sources.json').read_text(encoding='utf-8'))
    for source in sources: registry.add_source(source)
    for h in HEXAGRAMS.values():
        for item in [h['judgment'], *h['lines'], *([h['special_all_changing']] if h['special_all_changing'] else [])]:
            registry.add_rule(Rule(item['rule_id'], 1, 18, 'King Wen hexagrams', PROFILE,
                item['source_id'], item['locator'], item['text'], 'iching_historical_text',
                dict(hexagram=h['number'], reading_policy=POLICY), 'proposed', 'traditional', []))
