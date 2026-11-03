"""Manual, source-attributed symbolism. No personal or physical aura inference."""
import copy
import html
import json
from pathlib import Path
from .knowledge import Rule

DATA = json.loads((Path(__file__).resolve().parents[1] / 'knowledge/aura_thought_forms_v1.json').read_text(encoding='utf-8'))
PROFILE = DATA['profile']
LIMITS = [
    'Symbolic/creative reference only. No actual aura,personality,emotion,health,hidden energy,spiritual status or future outcome is inferred.',
    'Selections and subjective descriptions are user statements,not detected colors or verified observations.',
    'This historical Theosophical source is separate from Brennan,Kunz and chakra systems. No seven-layer correspondence is implemented.',
    'Color reproduction is not calibrated. No RGB,photo,camera,brightness-to-strength or spiritual-level processing.',
    'Kirlian corona-discharge photography does not establish supernatural aura detection;no optical apparatus or simulation is implemented.',
    'Historical descriptions are not scientific validation,diagnosis,healing advice or evidence of protective efficacy.',
    'Arbitrary mixtures have component coverage only;no new combined meaning is inferred.'
]


def _object(value, keys, path):
    if not isinstance(value, dict) or set(value) - set(keys):
        raise ValueError(path + ': unsupported schema; no photo,personal assessment or diagnostic inputs')


def _text(value, limit=160):
    return isinstance(value, str) and bool(value.strip()) and len(value) <= limit and not any(ord(c) < 32 for c in value)


def validate(value):
    _object(value, ['schema_version', 'profile', 'task', 'mode', 'components', 'subjective_description', 'example_id'], 'input')
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1:
        raise ValueError('schema_version must be integer 1')
    if value.get('profile') != PROFILE:
        raise ValueError('Unsupported tradition/edition; no cross-source fallback')
    if value.get('task') != 'symbolic_reference':
        raise ValueError('Only symbolic_reference; detection,personal inference and diagnosis are rejected')
    if value.get('mode') == 'source_example':
        if set(value) & {'components', 'subjective_description'}:
            raise ValueError('Source example cannot be overridden or personalized')
        if not isinstance(value.get('example_id'), str) or value['example_id'] not in DATA['source_examples']:
            raise ValueError('Unknown published example')
        return copy.deepcopy(value)
    if value.get('mode') != 'manual' or 'example_id' in value:
        raise ValueError('Use manual or source_example,without mixed inputs')
    if 'subjective_description' in value and not _text(value['subjective_description'], 1000):
        raise ValueError('subjective_description must be nonempty plain text up to1000 characters')
    rows = value.get('components')
    if not isinstance(rows, list) or not 1 <= len(rows) <= 24:
        raise ValueError('Supply1-24 manual symbolic components')
    for row in rows:
        _object(row, ['color', 'context', 'slot', 'certainty'], 'component')
        color = row.get('color', 'unknown')
        if isinstance(color, list):
            if not 2 <= len(color) <= 8 or any(not _text(c) for c in color) or len(set(color)) != len(color):
                raise ValueError('Ambiguous color requires2-8 distinct names')
        elif color is not None and not _text(color):
            raise ValueError('Color must be a name,list of alternatives,or null')
        if not _text(row.get('context', 'thought_form')) or not _text(row.get('slot', 'composition')):
            raise ValueError('Context and slot must be nonempty text')
        if row.get('certainty', 'selected') not in ('selected', 'uncertain', 'unknown'):
            raise ValueError('Unknown certainty')
    return copy.deepcopy(value)


def register_knowledge(registry):
    registry.add_source(DATA['source'])
    for term in DATA['terms'].values():
        registry.add_rule(Rule(term['rule_id'], term['version'], 14, 'Theosophical color layers', PROFILE,
            term['source_id'], term['locator'], term['description'], 'manual_symbolic_color_reference',
            dict(color=term['id'], qualifications=term['qualifications'], key=term['key'], individual_inference=False),
            'proposed', 'traditional', []))
    for key, context in DATA['contexts'].items():
        registry.add_rule(Rule('aura.thought_forms.context.'+key, 1, 14, 'Theosophical color layers', PROFILE,
            DATA['source']['id'], context['locator'], context['description'], 'documentary_context_reference',
            dict(context=key, anatomical_location=None, layer_number=None), 'proposed', 'traditional', []))
    for example in DATA['source_examples'].values():
        registry.add_rule(Rule(example['rule_id'], example['version'], 14, 'Theosophical color layers', PROFILE,
            example['source_id'], example['locator'], example['description'], 'published_symbolic_example',
            dict(figure=example['figure'], colors=example['colors'], individual_inference=False), 'proposed', 'traditional', []))


def reference(value, registry=None):
    request = validate(value)
    if registry is not None:
        register_knowledge(registry)
    example = copy.deepcopy(DATA['source_examples'][request['example_id']]) if request['mode'] == 'source_example' else None
    rows = [dict(color=c) for c in example['colors']] if example else request['components']
    # A slot is a user-declared single component only when explicitly supplied.
    # Multiple colors without a slot are a composition,not a contradiction.
    conflicts = []
    bad = set()
    for i, a in enumerate(rows):
        if 'slot' not in a or not isinstance(a.get('color'), str) or a.get('certainty','selected') != 'selected':
            continue
        for j, b in enumerate(rows[:i]):
            if b.get('slot') == a['slot'] and a.get('context','thought_form') == b.get('context','thought_form') and isinstance(b.get('color'),str) and b.get('certainty','selected') == 'selected' and a['color'] != b['color']:
                conflicts.append(dict(indices=[j, i], slot=a['slot'], reason='Different exclusive color labels for the same declared component;no winner selected.'))
                bad.update([i, j])
    results = []
    for i, row in enumerate(rows):
        color = row.get('color', 'unknown')
        candidates = color if isinstance(color,list) else [color]
        known = [copy.deepcopy(DATA['terms'][c]) for c in candidates if isinstance(c,str) and c in DATA['terms']]
        context = row.get('context','thought_form')
        if i in bad:
            status = 'conflict'
        elif color in (None, 'unknown') or row.get('certainty','selected') != 'selected':
            status = 'unknown_or_uncertain'
        elif isinstance(color,list):
            status = 'ambiguous'
        elif context not in DATA['contexts']:
            status = 'unsupported_context'
        elif known:
            status = 'resolved_symbol'
        else:
            status = 'unsupported_color'
        ctx = copy.deepcopy(DATA['contexts'].get(context))
        if ctx:
            ctx.update(source_id=DATA['source']['id'],rule_id='aura.thought_forms.context.'+context,version=1,
                coverage='direct_documentary_term',color_layer_assignment='unsupported')
        reason = {
            'conflict':'Different exclusive labels occupy the same declared slot;neither is applied.',
            'unknown_or_uncertain':'Missing or uncertain manual selection;no meaning is applied.',
            'ambiguous':'Alternatives are retained without selecting a shade or motif.',
            'unsupported_context':'This context has no verified rule in the selected source profile.',
            'resolved_symbol':'Exact manual vocabulary identifier;source-attributed symbolism only.',
            'unsupported_color':'No verified entry for this description;no nearest-color or inferred mapping.'
        }[status]
        results.append(dict(selection=copy.deepcopy(row),status=status,reason=reason,coverage='direct' if status=='resolved_symbol' else 'unsupported' if status.startswith('unsupported') else 'unresolved',
            reference=known[0] if status=='resolved_symbol' else None,candidate_references=known if status!='resolved_symbol' else [],context_reference=ctx))
    resolved = [r['reference'] for r in results if r['reference']]
    complete = len(resolved) == len(results)
    coverage = 'direct_published_example' if example else 'compositional' if complete and len(results)>1 else 'direct' if complete else 'partial' if resolved else 'unsupported_or_unresolved'
    motifs = [t['motif'] for t in resolved]
    summary = ('Published historical teaching example: '+example['title']+'. '+example['description']) if example else (
        'Selected creative motifs: '+'; '.join(motifs)+'. These are source-attributed symbols,not statements about a person.' if motifs else
        'No symbolic interpretation resolved. Review the explicit unknown,ambiguous,conflicting or unsupported selections.')
    if not complete:
        summary += ' Some components remain unresolved;no complete configuration interpretation is available.'
    return dict(schema_version=1,technique_id=14,profile=PROFILE,task='symbolic_reference',mode=request['mode'],source_example=example,
        components=results,conflicts=conflicts,subjective_description=dict(text=request.get('subjective_description'),status='user_statement_only',used_for_inference=False),
        configuration=dict(coverage=coverage,summary=summary,complete_component_coverage=complete,combined_rule=example['rule_id'] if example else None,
            combination_status='documented_example' if example else 'component_symbols_only_no_combined_rule',
            creative_prompt='For a fictional scene,which of the selected motifs would you contrast or develop?' if motifs else None),
        source=copy.deepcopy(DATA['source']),conventions=copy.deepcopy(DATA['conventions']),source_cautions=copy.deepcopy(DATA['source_cautions']),
        vocabulary=dict(colors=len(DATA['terms']),contexts=len(DATA['contexts']),published_examples=len(DATA['source_examples'])),
        optical=dict(status='not_implemented',source_id='aura-corona-boyers-tiller-1973-v1',distinction='Corona-discharge photographs are physical optical phenomena,not proof of supernatural aura detection.'),
        limitations=list(LIMITS),inference_enabled=False,individual_assessment=None,physical_aura_detected=False)


def _md(value):
    return html.escape(str(value),quote=False).replace('|','&#124;').replace('\n',' ')


def markdown(report):
    lines = ['# Aura — symbolic/creative reference','', '**No personal assessment or physical aura detection.**','',
        'Profile: '+report['profile'],'',report['configuration']['summary'],'',
        'Configuration coverage: '+report['configuration']['coverage'],'',
        '| Selected color | Context | Status | Historical motif |','|---|---|---|---|']
    for row in report['components']:
        s=row['selection'];t=row['reference']
        lines.append('| '+' | '.join(_md(v) for v in [s.get('color','unknown'),s.get('context','thought_form'),row['status'],t['motif'] if t else 'Unresolved'])+' |')
    for row in report['components']:
        lines += ['', 'Selection diagnostic: '+row['reason']]
        for t in ([row['reference']] if row['reference'] else row['candidate_references']):
            lines += ['', '## '+t['color']+' — '+row['status'],'',t['description'],
                'Source: '+t['source_id']+'; '+t['locator'],'Rule: '+t['rule_id']+' v'+str(t['version'])]
            lines += ['- '+q for q in t['qualifications']]
        if row['context_reference']:
            c=row['context_reference'];lines += ['', 'Context: '+c['description'],'Locator: '+c['locator']+'; '+c['rule_id']+' v1. Color-to-layer assignment remains unsupported.']
    if report['source_example']:
        e=report['source_example'];lines += ['','Published example: '+e['title']+'; '+e['locator']+'; '+e['rule_id']+' v1']
    lines += ['', '## Uncertainty and composition','']
    lines += ['- '+_md(c['reason'])+' Slot: '+_md(c['slot']) for c in report['conflicts']]
    lines += ['Combined rule: '+str(report['configuration']['combined_rule'])+'; '+report['configuration']['combination_status']]
    if report['configuration']['creative_prompt']:
        lines += [report['configuration']['creative_prompt']]
    if report['subjective_description']['text']:
        lines += ['', 'User statement only (unused for inference): '+_md(report['subjective_description']['text'])]
    lines += ['', '## Provenance and limitations','',report['source']['edition'],report['source']['rights_note']]
    lines += ['- '+k+': '+v for k,v in report['conventions'].items()]
    lines += ['- '+v for v in report['source_cautions']+report['limitations']]
    lines += ['', '[Primary source]('+report['source']['url']+')','']
    return '\n'.join(lines)


def load_input(path):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:
                raise ValueError('Duplicate JSON key: '+k)
            out[k]=v
        return out
    def invalid(value):
        raise ValueError('Nonfinite JSON: '+value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid)
