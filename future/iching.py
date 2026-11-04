"""Exact six-line transformations and source-bounded symbolic readings."""
import copy
from fractions import Fraction
import html
import json
from pathlib import Path
from .iching_catalog import (DATA, CONVENTIONS, PROFILE, POLICY, HEXAGRAMS, PATTERNS,
    TRIGRAMS, CATALOG_DIGEST, CONVENTION_DIGEST, hexagram, thaw, register_knowledge)
from .iching_cast import PROTOCOL, METHODS, WEIGHTS, cast
from .card_random import seed_bytes

STATES = {6: (0, True, 1, 'old_yin'), 7: (1, False, 1, 'young_yang'),
          8: (0, False, 0, 'young_yin'), 9: (1, True, 0, 'old_yang')}


def validate_lines(lines):
    if not isinstance(lines, (list, tuple)) or len(lines) != 6 or any(type(x) is not int or x not in STATES for x in lines):
        raise ValueError('Six integer states6/7/8/9 required,bottom-to-top')
    return list(lines)


def _identity(pattern):
    n = PATTERNS[tuple(pattern)]
    h = HEXAGRAMS[str(n)]
    trigrams = []
    for role, bits in [('lower', pattern[:3]), ('upper', pattern[3:])]:
        key = ''.join(map(str, bits))
        trigrams.append(dict(role=role, pattern_bottom_to_top=list(bits), **thaw(TRIGRAMS[key])))
    return dict(id=h['id'], number=n, name=h['name'], aliases=thaw(h['aliases']),
        pattern_bottom_to_top=list(pattern), trigrams=trigrams,
        diagram_top_to_bottom=['-------' if b else '--- ---' for b in reversed(pattern)])


def values_for(pattern, change_mask):
    """Inverse representation:binary pattern plus six-bit mask uniquely fixes values."""
    if not isinstance(pattern, (list, tuple)) or len(pattern) != 6 or any(type(b) is not int or b not in (0, 1) for b in pattern):
        raise ValueError('Pattern requires six integer0/1 bits,bottom-to-top')
    if type(change_mask) is not int or not 0 <= change_mask <= 63:
        raise ValueError('Change mask must be integer0..63;bit0=line1')
    return [(9 if b else 6) if change_mask & (1 << i) else (7 if b else 8) for i, b in enumerate(pattern)]


def transform(lines):
    values = validate_lines(lines)
    initial, result, moving, trace = [], [], [], []
    mask = 0
    for i, value in enumerate(values):
        before, changes, after, label = STATES[value]
        initial.append(before); result.append(after)
        if changes:
            moving.append(i + 1); mask |= 1 << i
        trace.append(dict(position=i + 1, value=value, state=label,
            initial_yang=bool(before), moving=changes, resulting_yang=bool(after)))
    return dict(line_order='bottom_to_top', values=values, change_mask=mask,
        moving_lines=moving, trace=trace, initial=_identity(initial), resulting=_identity(result))


def validate(value):
    allowed = {'schema_version', 'profile', 'reading_policy', 'task', 'mode', 'method',
               'line_order', 'lines', 'seed', 'protocol', 'question'}
    if not isinstance(value, dict) or set(value) - allowed:
        raise ValueError('Input object contains unknown/unsupported fields')
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1:
        raise ValueError('schema_version must be integer1')
    if value.get('profile') != PROFILE or value.get('reading_policy') != POLICY:
        raise ValueError('Exact Legge1882 profile and all_moving_lines_v1 policy required')
    if value.get('task') != 'symbolic_reading' or value.get('line_order') != 'bottom_to_top':
        raise ValueError('Only symbolic_reading and explicit bottom_to_top order supported')
    if 'question' in value:
        q = value['question']
        if not isinstance(q, str) or not q.strip() or len(q) > 1000 or any(ord(c) < 32 for c in q):
            raise ValueError('Question must be nonempty plain text up to1000 characters')
        try: q.encode('utf-8', errors='strict')
        except UnicodeError as exc: raise ValueError('Question must encode as UTF-8') from exc
    if value.get('mode') == 'manual':
        if value.get('method') != 'manual' or set(value) & {'seed', 'protocol'}:
            raise ValueError('Manual lines require method manual and no seed/protocol')
        validate_lines(value.get('lines'))
    elif value.get('mode') == 'seeded':
        if not isinstance(value.get('method'), str) or value['method'] not in METHODS or 'lines' in value:
            raise ValueError('Seeded mode requires supported casting method and no manual lines')
        if value.get('protocol') != PROTOCOL: raise ValueError('Exact I Ching casting protocol required')
        seed_bytes(value.get('seed'))
    else: raise ValueError('Use manual or seeded mode')
    return copy.deepcopy(value)


def read(value, registry=None):
    request = validate(value)
    if registry is not None: register_knowledge(registry)
    if request['mode'] == 'seeded':
        lines, casting = cast(request['seed'], request['method'])
        weights = WEIGHTS[request['method']]; denominator = sum(weights)
        probability = Fraction(1)
        for state in lines: probability *= Fraction(weights[state - 6], denominator)
        probabilities = dict(single_line={str(v): dict(numerator=weights[v - 6], denominator=denominator)
            for v in range(6, 10)}, exact_value_sequence=dict(numerator=probability.numerator, denominator=probability.denominator),
            scope='Digital casting probabilities only;no outcome or predictive probability',
            physical_stalk_simulation=False, conventional_residue_assumptions=request['method'] == 'yarrow-marginal')
    else:
        lines = list(request['lines'])
        casting = dict(method='manual', protocol=None, raw=None, line_order='bottom_to_top')
        probabilities = None
    calculation = transform(lines)
    a = hexagram(calculation['initial']['number']); b = hexagram(calculation['resulting']['number'])
    calculation['initial']['judgment'] = a['judgment']
    calculation['resulting']['judgment'] = b['judgment']
    moving = [dict(position=i, **a['lines'][i - 1]) for i in calculation['moving_lines']]
    special = a['special_all_changing'] if len(moving) == 6 else None
    summary = (f"Begin with {a['number']} {a['name']}: " + a['judgment']['text'] + ' ')
    if moving:
        summary += ('Read the changing positions ' + ', '.join(str(x['position']) for x in moving) +
            f" as qualified perspectives on that situation,then compare {b['number']} {b['name']}: " + b['judgment']['text'] +
            ' The relating figure is a second symbolic context,not an assured future event.No moving line overrides the others.')
    else:
        summary += 'There are no moving lines;the relating figure is identical.Use the judgment as a single reflection context.'
    replay = dict(request=request, protocol=casting['protocol'], profile=PROFILE, reading_policy=POLICY,
        catalog_sha256=CATALOG_DIGEST, convention_sha256=CONVENTION_DIGEST,
        serialization=thaw(CONVENTIONS['protocol']['hashes']), casting=casting,
        values=list(lines), change_mask=calculation['change_mask'],
        initial_number=a['number'], resulting_number=b['number'])
    return dict(schema_version=1, technique_id=18, profile=PROFILE, reading_policy=thaw(CONVENTIONS['reading_policy']),
        task='symbolic_reading', mode=request['mode'], method=request['method'], question=request.get('question'),
        calculation=calculation, changing_line_texts=moving, special_all_changing=special,
        variants=a['variants'] + ([] if a['number'] == b['number'] else b['variants']),
        summary=dict(coverage='compositional', text=summary), probabilities=probabilities, replay=replay,
        source=thaw(DATA['source']), procedural_sources=list(CONVENTIONS['sources'])[1:], factual_prediction=False,
        limitations=['Source text,editorial composition and unsupported interpretations remain distinct.',
            'No universal moving-line priority,no prediction certainty or empirical accuracy claim.',
            'Historical language about gender,health,law or morals is source text,not factual assessment of a person.',
            'Transcription uses original-scan OCR with recorded normalization and selected independent scan checks;full diplomatic collation remainsP1.',
            'Yarrow marginal method samples conventional1/5/7/3 weights;it does not simulate49-stalk physical partitions.',
            'Wilhelm/Baynes,Mei Hua and Wen Wang Gua interpretations are not substituted.'])


def markdown(result):
    def safe(x): return html.escape(str(x)).replace('|', '&#124;').replace('\n', ' ')
    c = result['calculation']
    lines = ['# I Ching — symbolic reading', '', '**Profile:** ' + safe(result['profile']),
        '', 'Method: ' + safe(result['method']) + '; values bottom to top: ' + str(c['values']),
        '', 'Moving lines: ' + str(c['moving_lines']) + '; mask: ' + str(c['change_mask']) +
        ' (bit0 = line1).', '', safe(result['summary']['text'])]
    if result['question']: lines += ['', 'Question context: ' + safe(result['question'])]
    for label in ['initial', 'resulting']:
        h = c[label]; j = h['judgment']
        lines += ['', '## ' + label.title() + ': ' + str(h['number']) + ' — ' + safe(h['name']),
            '', '```text', '\n'.join(h['diagram_top_to_bottom']), '```',
            '', 'Diagram displayed top to bottom;data/casting order is bottom to top.',
            '', '; '.join(safe(t['role'] + ': ' + t['symbol'] + ' (' + t['name'] + ')') for t in h['trigrams']),
            '', safe(j['text']), '', 'Source: ' + safe(j['source_id']) + '; ' + safe(j['locator']) + '; ' + safe(j['rule_id'])]
    for item in result['changing_line_texts']:
        lines += ['', '## Changing line ' + str(item['position']), '', safe(item['text']),
                  '', 'Source: ' + safe(item['locator']) + '; ' + safe(item['rule_id'])]
    if result['special_all_changing']:
        item = result['special_all_changing']
        lines += ['', '## Additional all-changing passage', '', safe(item['text']), '', 'Source: ' + safe(item['locator'])]
    for item in result['variants']:
        lines += ['', '## Unresolved textual variant', '', safe(item['text']), '', 'Source: ' + safe(item['locator'])]
    if result['probabilities']:
        lines += ['', '## Casting probabilities', '', 'Exact digital single-line weights: ' +
            safe(json.dumps(result['probabilities']['single_line'])) + '. No predictive probabilities.']
    lines += ['', '## Limits', '', safe(' '.join(result['limitations'])), '',
        '[Original1882 scan](' + result['source']['url'] + ')', '', '## Exact replay', '',
        '```json', json.dumps(result['replay'], ensure_ascii=True, indent=2), '```', '']
    return '\n'.join(lines)


def load_input(path):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result: raise ValueError('Duplicate JSON key: ' + k)
            result[k] = v
        return result
    def invalid(value): raise ValueError('Nonfinite JSON: ' + value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs, parse_constant=invalid)
