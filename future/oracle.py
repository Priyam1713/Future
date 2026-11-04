"""Named historical Lenormand symbols and replayable editorial line readings."""
import copy
import hashlib
import html
import json
from pathlib import Path
from types import MappingProxyType
from .card_random import PROTOCOL, shuffle_pack, seed_bytes
from .knowledge import Rule


def _freeze(x):
    if isinstance(x, dict): return MappingProxyType({k: _freeze(v) for k, v in x.items()})
    if isinstance(x, list): return tuple(_freeze(v) for v in x)
    return x


def _thaw(x):
    if isinstance(x, (dict, MappingProxyType)): return {k: _thaw(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [_thaw(v) for v in x]
    return x


_PATH = Path(__file__).resolve().parents[1] / 'knowledge/oracle_lenormand_v1.json'
_RAW = _PATH.read_bytes()
DATA = _freeze(json.loads(_RAW))
PROFILE = DATA['profile']
ORDER = DATA['canonical_order']
CARDS = DATA['cards']
CATALOG_SHA256 = hashlib.sha256(_RAW).hexdigest()
ORDER_SHA256 = hashlib.sha256('\n'.join(ORDER).encode('utf-8')).hexdigest()
SPREADS = MappingProxyType({'one': 1, 'three': 3, 'five': 5})
assert len(ORDER) == len(set(ORDER)) == len(CARDS) == 36


def card(identifier):
    if not isinstance(identifier, str) or identifier not in CARDS:
        raise ValueError('Unknown card in the named Lenormand1903 profile')
    return _thaw(CARDS[identifier])


def register_knowledge(registry):
    registry.add_source(_thaw(DATA['source']))
    for c in CARDS.values():
        m = c['meaning']
        registry.add_rule(Rule(m['rule_id'], 1, 17, 'Lenormand 36', PROFILE,
            m['source_id'], m['locator'], m['text'] + ' ' + m['context'],
            'oracle_source_meaning', {'card_id': c['id'], 'orientation': 'upright'},
            'proposed', 'traditional', []))
    for c in DATA['source_conditions']:
        registry.add_rule(Rule('oracle.ew1903.' + c['id'], 1, 17, 'Lenormand 36', PROFILE,
            DATA['source']['id'], c['locator'], c['effect'], 'oracle_source_condition',
            dict(relation=c['relation'], automatic_judgment=False), 'proposed', 'traditional', []))


def _object(x, keys):
    if not isinstance(x, dict) or set(x) - set(keys):
        raise ValueError('Expected object with supported fields only')


def validate(value):
    _object(value, ['schema_version', 'profile', 'task', 'mode', 'spread', 'seed',
                   'protocol', 'orientation_policy', 'cards', 'question'])
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1:
        raise ValueError('schema_version must be integer1')
    if value.get('profile') != PROFILE or value.get('task') != 'symbolic_reading':
        raise ValueError('Exact Lenormand profile and symbolic_reading task required')
    if not isinstance(value.get('spread'), str) or value['spread'] not in SPREADS:
        raise ValueError('Supported editorial spreads:one,three,five')
    if value.get('orientation_policy') != 'upright_only':
        raise ValueError('This profile supports upright_only;no reversed meanings')
    if 'question' in value:
        q = value['question']
        if not isinstance(q, str) or not q.strip() or len(q) > 1000 or any(ord(c) < 32 for c in q):
            raise ValueError('Question must be nonempty plain text up to1000 characters')
        try: q.encode('utf-8', errors='strict')
        except UnicodeError as exc: raise ValueError('Invalid question encoding') from exc
    if value.get('mode') == 'seeded':
        if 'cards' in value or value.get('protocol') != PROTOCOL:
            raise ValueError('Exact shuffle protocol required;no mixed manual cards')
        seed_bytes(value.get('seed'))
    elif value.get('mode') == 'manual':
        if set(value) & {'seed', 'protocol'}: raise ValueError('Manual mode has no seed/protocol')
        rows = value.get('cards')
        if not isinstance(rows, list) or len(rows) != SPREADS[value['spread']]:
            raise ValueError('Manual count must match spread')
        ids = []
        for r in rows:
            _object(r, ['card_id', 'orientation'])
            card(r.get('card_id'))
            if r.get('orientation', 'upright') != 'upright': raise ValueError('Reversals unsupported')
            ids.append(r['card_id'])
        if len(set(ids)) != len(ids): raise ValueError('Draw without replacement;duplicate card')
    else: raise ValueError('Use seeded or manual mode')
    return copy.deepcopy(value)


def draw(seed, count):
    """Public bounded draw,independent of the reading layouts."""
    if type(count) is not int or not 1 <= count <= 36:
        raise ValueError('Draw count must be integer1..36')
    pack, trace = shuffle_pack(ORDER, seed)
    return pack[:count], pack, trace


def combine(left, right):
    """Keep published conditions separate from editorial application and synthesis."""
    a, b = card(left), card(right)
    if left == right: raise ValueError('Pair requires distinct cards')
    n, m = a['number'], b['number']
    direct = []
    unknown = ['No source-published exact ordered pair interpretation;no universal pair dictionary.']
    if {n, m} == {6, 16}:
        direct.append(dict(source_id=DATA['source']['id'], locator='Signification of the Cards,No.16',
            rule_id='oracle.ew1903.star-clouds', condition='Star near Clouds',
            text='The source qualifies enterprise luck with a prolonged series of adverse incidents.',
            application='experimental_adjacency_as_near', condition_verified=False))
        unknown.append('Adjacency is an editorial near convention;the source supplies no distance threshold.')
    if 25 in (n, m) and ({n, m} & {28, 29}):
        right_of_person = m == 25
        direct.append(dict(source_id=DATA['source']['id'], locator='Signification of the Cards,No.25',
            rule_id='oracle.ew1903.ring-direction', condition='Ring right of person;or left AND distant',
            text='Right:happy prosperous marriage motif;left and distant:separation motif.',
            application='experimental_page_right' if right_of_person else 'unsupported_distance',
            condition_verified=False))
        unknown.append('Page-right adaptation only;source example uses mirrored right/left language.Near-left does not imply separation;distance and person reference are unresolved.')
    composition = (a['name'] + ' (' + a['meaning']['text'] + ') followed by ' +
                   b['name'] + ' (' + b['meaning']['text'] + '). Reflect on how the second motif qualifies the first, while retaining both source contexts.')
    return dict(card_ids=[left, right], coverage='compositional',
        convention='editorial_ordered_juxtaposition_v1', direct_conditions=direct,
        direct_pair=dict(coverage='unsupported', text=None), text=composition,
        unsupported=unknown, contexts=[a['meaning']['context'], b['meaning']['context']])


def read(value, registry=None):
    request = validate(value)
    if registry is not None: register_knowledge(registry)
    count = SPREADS[request['spread']]
    if request['mode'] == 'seeded':
        ids, pack, trace = draw(request['seed'], count)
    else:
        ids = [r['card_id'] for r in request['cards']]
        pack, trace = None, None
    replay = dict(request=request, profile=PROFILE, catalog_sha256=CATALOG_SHA256,
        canonical_order=list(ORDER), canonical_order_sha256=ORDER_SHA256,
        serialization='UTF-8 IDs joined by LF,no terminal LF for order hash;catalog hash uses exact file bytes',
        protocol=PROTOCOL if pack else None, seed=request.get('seed'), shuffled_pack=pack,
        draw_count=count, cards=[dict(card_id=k, orientation='upright') for k in ids],
        shuffle=trace, orientation_policy='upright_only', deck_domain='deck', orientation_stream_used=False,
        cuts=[], physical_ritual_verified=False)
    readings = [dict(position=i + 1, card=card(k), orientation='upright',
        coverage='direct_source_paraphrase', condition_status='not_adjudicated') for i, k in enumerate(ids)]
    pairs = [combine(a, b) for a, b in zip(ids, ids[1:])]
    overview = 'Read this symbolic sequence in order: ' + ' → '.join(
        card(k)['name'] + ' (' + card(k)['meaning']['text'].rstrip('.') + ')' for k in ids) + '. '
    overview += ('Use the source motifs as a reflection focus.' if count == 1 else
                 'Each adjacent pair carries the narrative forward;compare its two motifs and retain the stated alternatives.This is editorial synthesis,not a published combined forecast.')
    return dict(schema_version=1, technique_id=17, profile=PROFILE, deck_identity=DATA['source']['edition'],
        task='symbolic_reading', mode=request['mode'], spread=request['spread'],
        layout=dict(coverage='editorial_adaptation', order='left_to_right',
            source_historical_layout='Four rows of8 left-to-right,then4 centered;not implemented as a judgment engine'),
        question=request.get('question'), readings=readings, combinations=pairs,
        summary=dict(coverage='compositional', text=overview), replay=replay,
        sources=[_thaw(DATA['source'])], factual_prediction=False,
        limitations=list(DATA['unknowns']) + ['Historical health,wealth,marriage and moral language is symbolism;no facts about people or outcomes are inferred.',
            'No source distance,cloud facing,lucky/unlucky classification or significator conditions automatically judged.'])


def markdown(result):
    def safe(x): return html.escape(str(x)).replace('|', '&#124;').replace('\n', ' ')
    lines = ['# Oracle — Lenormand symbolic reading', '', '**Profile:** ' + safe(result['profile']),
             '', safe(result['deck_identity']), '', 'Layout: editorial ' + safe(result['spread']) +
             ' line,left to right;upright only.', '', safe(result['summary']['text'])]
    if result['question']: lines += ['', 'Question context: ' + safe(result['question'])]
    for r in result['readings']:
        c = r['card']; m = c['meaning']
        lines += ['', '## ' + str(r['position']) + '. ' + str(c['number']) + ' — ' + safe(c['name']),
                  '', safe(m['text']), '', 'Context: ' + safe(m['context']),
                  '', 'Source: ' + safe(m['source_id']) + '; ' + safe(m['locator']) + '; ' + safe(m['rule_id'])]
    for p in result['combinations']:
        lines += ['', '### Adjacent pair — compositional', '', safe(p['text'])]
        for d in p['direct_conditions']:
            lines += ['', 'Published condition: ' + safe(d['text']) + ' [' + safe(d['locator']) +
                      ']. Application: ' + safe(d['application']) + ';condition unresolved.']
        lines += ['', 'Unsupported: ' + safe(' '.join(p['unsupported']))]
    lines += ['', '## Limits', '', safe(' '.join(result['limitations'])), '',
              '[Historical source scan](' + result['sources'][0]['url'] + ')', '',
              '## Exact replay metadata', '', '```json', json.dumps(result['replay'], ensure_ascii=True, indent=2), '```', '']
    return '\n'.join(lines)


def load_input(path):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result: raise ValueError('Duplicate JSON key: ' + k)
            result[k] = v
        return result
    def invalid(value): raise ValueError('Nonfinite JSON: ' + value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),
                      object_pairs_hook=pairs, parse_constant=invalid)
