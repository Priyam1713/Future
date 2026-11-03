"""Immutable source catalog,independent of shuffling and layout composition."""
import json
from pathlib import Path
from types import MappingProxyType
from .knowledge import Rule


def freeze(value):
    if isinstance(value,dict):return MappingProxyType({k:freeze(v) for k,v in value.items()})
    if isinstance(value,list):return tuple(freeze(x) for x in value)
    return value


def thaw(value):
    if isinstance(value,(dict,MappingProxyType)):return {k:thaw(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [thaw(x) for x in value]
    return value


DATA=freeze(json.loads((Path(__file__).resolve().parents[1]/'knowledge/tarot_waite_v1.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile']
ORDER=DATA['canonical_order']
CARDS=DATA['cards']
assert len(ORDER)==len(set(ORDER))==len(CARDS)==78


def card(identifier):
    if not isinstance(identifier,str) or identifier not in CARDS:raise ValueError('Unknown card in Waite1922 profile: '+str(identifier))
    return thaw(CARDS[identifier])


def register_knowledge(registry):
    registry.add_source(thaw(DATA['source']))
    for c in CARDS.values():
        for orientation,m in c['meanings'].items():
            registry.add_rule(Rule(m['rule_id'],m['version'],16,'Rider–Waite–Smith',PROFILE,m['source_id'],m['locator'],m['text'],
                'tarot_source_meaning',dict(card_id=c['id'],orientation=orientation,flags=thaw(m['flags']),
                    source_gloss=m['symbolic_focus'],gloss_coverage=m['gloss_coverage']), 'proposed','traditional',[]))
        if c['additional_meanings']:
            a=c['additional_meanings']
            registry.add_rule(Rule('tarot.waite1922.'+c['id']+'.additional',1,16,'Rider–Waite–Smith',PROFILE,DATA['source']['id'],a['locator'],a['text'],
                'tarot_source_alternative',dict(card_id=c['id'],automatically_merged=False),'proposed','traditional',[]))
    s=DATA['celtic']
    registry.add_rule(Rule(s['rule_id'],s['version'],16,'spreads',PROFILE,s['source_id'],s['locator'],s['significator'],
        'waite_celtic_positions',dict(positions=thaw(s['positions']),facing=s['facing'],exceptions=thaw(s['exceptions'])),'proposed','traditional',[]))
