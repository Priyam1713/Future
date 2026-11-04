"""Source-layered Elder24 reference readings over the unchanged draw kernel."""
import copy
import hashlib
import html
import json
from pathlib import Path
from types import MappingProxyType
from .card_random import PROTOCOL as KERNEL, seed_bytes, shuffle_pack
from .knowledge import Rule


def freeze(value):
    if isinstance(value, dict): return MappingProxyType({k: freeze(v) for k,v in value.items()})
    if isinstance(value, list): return tuple(freeze(v) for v in value)
    return value


def thaw(value):
    if isinstance(value, (dict, MappingProxyType)): return {k: thaw(v) for k,v in value.items()}
    if isinstance(value, (list, tuple)): return [thaw(v) for v in value]
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
        ensure_ascii=False).encode('utf-8')).hexdigest()


ROOT = Path(__file__).resolve().parents[1]
DATA = freeze(json.loads((ROOT/'knowledge/runes_elder24_v1.json').read_text(encoding='utf-8')))
PROFILE = DATA['profile']
PROTOCOL = DATA['protocol']['id']
ORDER = DATA['canonical_order']
RUNES = DATA['runes']
SPREADS = MappingProxyType({'one': 1, 'three': 3})
CATALOG_HASH = digest(thaw(DATA))
ORDER_HASH = hashlib.sha256('\n'.join(ORDER).encode('utf-8')).hexdigest()
assert len(ORDER) == len(set(ORDER)) == len(RUNES) == 24


def rune(identifier):
    if not isinstance(identifier, str) or identifier not in RUNES:
        raise ValueError('Unknown rune in the named Elder24 profile;no blank/system substitution')
    return thaw(RUNES[identifier])


def register_knowledge(registry):
    for key in ['source', 'encoding_source', 'poem_source']: registry.add_source(thaw(DATA[key]))
    for r in RUNES.values():
        h, a = r['historical_reference'], r['association']
        registry.add_rule(Rule(h['rule_id'], 1, 19, 'Elder Futhark (24)', PROFILE,
            h['source_id'], h['locator'], 'Reference position'+str(r['position'])+',transliteration '+r['transliteration']+
            ',normalized display '+r['codepoint']+'. Full name is '+r['name_classification']+'.',
            'rune_historical_reference', dict(rune_id=r['id'], name_attested_as_elder_label=False),
            'proposed', 'traditional', []))
        registry.add_rule(Rule(a['rule_id'], 1, 19, 'Elder Futhark (24)', PROFILE,
            a['source_id'], a['locator'], 'Qualified lexical reference: '+str(a['lexical_association'])+
            ';status '+a['meaning_status']+'. No ancient divination rule.',
            'rune_comparative_reference', dict(rune_id=r['id'], coverage=a['coverage']),
            'proposed', 'traditional', []))


def _object(value, allowed):
    if not isinstance(value, dict) or set(value) - set(allowed):
        raise ValueError('Expected object with supported fields only')


def _text(value, limit):
    if not isinstance(value, str) or not value.strip() or len(value) > limit or any(ord(c) < 32 for c in value):
        return False
    try: value.encode('utf-8', errors='strict')
    except UnicodeError: return False
    return True


def validate(value):
    _object(value, ['schema_version','profile','task','mode','spread','protocol','seed',
                    'orientation_policy','runes','positions','question'])
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1:
        raise ValueError('schema_version must be integer1')
    if value.get('profile') != PROFILE or value.get('task') != 'symbolic_reading':
        raise ValueError('Exact Elder24 profile and symbolic_reading task required')
    if not isinstance(value.get('spread'), str) or value['spread'] not in SPREADS:
        raise ValueError('Use one or three editorial spread')
    if value.get('orientation_policy') != 'upright_only':
        raise ValueError('Upright-only application;no generic reversal,mirror or face-down interpretation')
    if 'positions' in value:
        labels = value['positions']
        if value['spread'] != 'three' or not isinstance(labels, list) or len(labels) != 3 or any(not _text(x,80) for x in labels) or len(set(labels)) != 3:
            raise ValueError('Three-rune layout requires three distinct plain-text editorial labels')
    if 'question' in value and not _text(value['question'],1000):
        raise ValueError('Question must be nonempty plain UTF-8 text up to1000 characters')
    if value.get('mode') == 'seeded':
        if 'runes' in value or value.get('protocol') != PROTOCOL:
            raise ValueError('Exact Rune draw protocol required;no mixed manual selection')
        seed_bytes(value.get('seed'))
    elif value.get('mode') == 'manual':
        if set(value) & {'seed','protocol'}: raise ValueError('Manual mode has no seed/protocol')
        rows = value.get('runes')
        if not isinstance(rows, list) or len(rows) != SPREADS[value['spread']]:
            raise ValueError('Manual rune count must match spread')
        identifiers = []
        for row in rows:
            _object(row, ['rune_id','orientation'])
            rune(row.get('rune_id'))
            if row.get('orientation','upright') != 'upright': raise ValueError('Reversed/rotated/face-down runes unsupported')
            identifiers.append(row['rune_id'])
        if len(set(identifiers)) != len(identifiers): raise ValueError('No repeated runes within a draw')
    else: raise ValueError('Use seeded or manual mode')
    return copy.deepcopy(value)


def draw(seed, count):
    """Computational draw1..24;reading layouts remain limited to1/3."""
    if type(count) is not int or not 1 <= count <= 24:
        raise ValueError('Draw count must be integer1..24')
    pack, trace = shuffle_pack(ORDER, seed, rounds=1, cut=False)
    return pack[:count], pack, trace


def read(value, registry=None):
    request = validate(value)
    if registry is not None: register_knowledge(registry)
    if request['mode'] == 'seeded':
        identifiers, pack, trace = draw(request['seed'], SPREADS[request['spread']])
    else:
        identifiers = [x['rune_id'] for x in request['runes']]
        pack, trace = None, None
    labels = ['Focus'] if request['spread'] == 'one' else request.get('positions',['Situation','Challenge','Reflection'])
    readings = []
    for number, (identifier, label) in enumerate(zip(identifiers,labels),1):
        r = rune(identifier); a = r['association']
        unresolved = a['lexical_association'] is None
        reference = 'The literal name association is unresolved.' if unresolved else 'The qualified linguistic association is '+a['lexical_association']+'.'
        reflection = ('At '+label+', consider '+r['composition']['theme']+'. '+r['composition']['reflection']+
            ' '+reference+' This application is modern editorial reflection,not an ancient rule or factual claim.')
        readings.append(dict(position=dict(order=number,label=label,coverage='editorial_layout',
            role='Apply the chosen theme to '+label+' as a reflection prompt;no event or person is inferred.'),
            rune=r, orientation='upright', direct=r['historical_reference'],
            comparative=a, later_poem_accounts=r['later_poem_accounts'],
            compositional=dict(coverage='modern_editorial',text=reflection,theme=r['composition']['theme']),
            unresolved_meaning=unresolved, conflicts=r['conflicts'], unsupported=r['unknowns']))
    threads=[r['position']['label']+': '+r['rune']['composition']['theme'] for r in readings]
    if len(readings)==1:
        summary='Use '+threads[0]+' as a focus. '+readings[0]['rune']['composition']['reflection']
    else:
        summary=('Begin with '+threads[0]+',compare it with '+threads[1]+',then use '+threads[2]+
            ' to frame a considered response. Ask how these themes support or complicate each other. This sequence is editorial composition;there is no source-published universal combination rule.')
    if any(r['unresolved_meaning'] for r in readings):
        summary+=' At least one literal name meaning is unresolved;its editorial prompt does not settle that gap.'
    replay = dict(request=request, profile=PROFILE, protocol=PROTOCOL if pack else None,
        kernel=KERNEL if pack else None, seed=request.get('seed'), canonical_order=list(ORDER),
        canonical_order_sha256=ORDER_HASH, catalog_sha256=CATALOG_HASH,
        serialization=thaw(DATA['protocol']), shuffled_set=pack, draw_count=len(identifiers),
        selected=[dict(rune_id=k,orientation='upright') for k in identifiers], shuffle=trace,
        orientation_policy='upright_only', orientation_stream_used=False, replacement=False,
        cuts=[], physical_casting_equivalence=False)
    return dict(schema_version=1, technique_id=19, profile=PROFILE, source_profile_title=DATA['title'],
        task='symbolic_reading', mode=request['mode'], spread=request['spread'], question=request.get('question'),
        readings=readings, summary=dict(coverage='modern_editorial_compositional',text=summary),
        combinations=dict(coverage='unsupported',universal_rule=None),
        historical_order_variants=thaw(DATA['historical_variants']), replay=replay,
        sources=[thaw(DATA[k]) for k in ['source','encoding_source','poem_source']],
        factual_prediction=False, outcome_probabilities=None,
        limitations=list(DATA['limits'])+['Upright-only is an application policy,not a claim that historical writing lacked reversed/inverted shapes.',
            'No blank,Younger,Futhorc,modern guidebook,reversal or physical-casting interpretation is substituted.',
            'No inferred diagnosis,personality,hidden facts,guaranteed events or rune-strength score.'])


def markdown(result):
    def safe(x): return html.escape(str(x)).replace('|','&#124;').replace('\n',' ')
    lines=['# Rune Casting — historical/symbolic reading','', '**Profile:** '+safe(result['profile']),
        '', 'Mode: '+safe(result['mode'])+'; spread: '+safe(result['spread'])+'; upright only.',
        '', safe(result['summary']['text'])]
    if result['question']: lines+=['','Question context: '+safe(result['question'])]
    for reading in result['readings']:
        r=reading['rune']; a=reading['comparative']; h=reading['direct']
        lines+=['','## '+str(reading['position']['order'])+'. '+safe(reading['position']['label'])+
            ' — '+safe(r['name'])+' '+r['glyph'],'', 'Text fallback: '+safe(r['text_fallback'])+'; '+r['codepoint'],
            '', 'Direct reference: position '+str(r['position'])+'; transliteration '+safe(r['transliteration'])+
            '; approximate sound '+safe(r['phonetic_value'])+'; name class '+safe(r['name_classification'])+'.',
            '', 'Source: '+safe(h['source_id'])+'; '+safe(h['locator'])+'; '+safe(h['rule_id']),
            '', 'Comparative/reconstructed association: '+safe(a['lexical_association'] if a['lexical_association'] is not None else 'UNRESOLVED')+'.',
            '', 'Source: '+safe(a['source_id'])+'; '+safe(a['locator'])+'; '+safe(a['rule_id'])]
        for account in reading['later_poem_accounts']:
            lines+=['','Separate '+safe(account['tradition'])+' context: '+safe(account['context']),
                '', 'Source: '+safe(account['source_id'])+'; '+safe(account['locator'])]
        lines+=['','Modern editorial composition: '+safe(reading['compositional']['text'])]
        if reading['conflicts']: lines+=['','Conflicts/uncertainty: '+safe(' '.join(reading['conflicts']))]
        lines+=['','Unsupported: '+safe('; '.join(reading['unsupported']))]
    lines+=['','## Limits','',safe(' '.join(result['limitations'])),'',
        'Glyphs are normalized Unicode display characters;no font or artwork is bundled.','',
        '[Inspected scholarly source]('+result['sources'][0]['url']+')','',
        '## Exact replay metadata','','```json',json.dumps(result['replay'],ensure_ascii=True,indent=2),'```','']
    return '\n'.join(lines)


def load_input(path):
    def pairs(items):
        result={}
        for k,v in items:
            if k in result: raise ValueError('Duplicate JSON key: '+k)
            result[k]=v
        return result
    def invalid(value): raise ValueError('Nonfinite JSON: '+value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid)
