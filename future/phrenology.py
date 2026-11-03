"""Source-specific historical label lookup. No head data or individual inference."""
import copy
import json
from pathlib import Path
from .knowledge import Rule

DATA = json.loads((Path(__file__).resolve().parents[1] / 'knowledge/phrenology_spurzheim_v1.json').read_text(encoding='utf-8'))
PROFILE = DATA['profile']
LIMITS = [DATA['scientific_scope'],
    'Printed views do not establish anatomical left/right; no mirrored or cross-edition mapping is inferred.',
    'Locations are qualitative printed-label positions,not measured organ boundaries or modern brain anatomy.',
    'Only15 selected passage summaries are provided; other descriptions reproduce legend categories only.',
    'Gall,Combe and other editions remain unsupported. Historical racist,sexist and ability claims are not assessment rules.']


def _object(value, keys, path):
    if not isinstance(value, dict):
        raise ValueError(path + ' must be an object')
    if set(value) - set(keys):
        raise ValueError(path + ': unsupported fields; personal data,images and measurements are not accepted')


def _text(value):
    return isinstance(value, str) and 0 < len(value) <= 120 and bool(value.strip())


def validate(value):
    _object(value, ['schema_version','profile','task','schematic','selections','region_id'], 'input')
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1:
        raise ValueError('schema_version must be integer1')
    if value.get('profile') != PROFILE:
        raise ValueError('Unsupported source profile; no edition or school fallback')
    if value.get('task') != 'historical_reference':
        raise ValueError('Only historical_reference is supported; personal inference is rejected')
    if not _text(value.get('schematic')) or value['schematic'] not in DATA['schematics']:
        raise ValueError('Select a verified named schematic')
    rows = value.get('selections', [])
    if not isinstance(rows, list) or len(rows) > 37:
        raise ValueError('selections must contain at most37 references')
    if not rows and 'region_id' not in value:
        raise ValueError('Supply at least one selection or a named software browsing region')
    if 'region_id' in value and not _text(value['region_id']):
        raise ValueError('region_id must be a nonempty identifier')
    for row in rows:
        _object(row, ['label_id','name','candidates'], 'selection')
        if not row:
            raise ValueError('Empty selection')
        if 'candidates' in row:
            candidates = row['candidates']
            if len(row) != 1 or not isinstance(candidates, list) or not 2 <= len(candidates) <= 37:
                raise ValueError('Ambiguous candidates require2-37 distinct label IDs,without an asserted label/name')
            if any(not _text(x) for x in candidates) or len(set(candidates)) != len(candidates):
                raise ValueError('Invalid or duplicate candidate IDs')
        elif any(not _text(v) for v in row.values()):
            raise ValueError('Label IDs and names must be nonempty strings')
    return copy.deepcopy(value)


def register_knowledge(registry):
    registry.add_source(DATA['source'])
    for entry in DATA['entries'].values():
        registry.add_rule(Rule(entry['rule_id'], 1, 10, 'historical faculty reference', PROFILE,
            entry['source_id'], entry['legend_locator'] + ('; ' + entry['description_locator'] if 'description_locator' in entry else ''), entry['historical_description'],
            'historical_label_lookup', dict(label_id=entry['id'], individual_inference=False,
            original_name=entry['original_name'], category=entry['category'], aliases=entry['aliases'],
            diagram_locations={sid: s['locations'][entry['id']] for sid,s in DATA['schematics'].items() if entry['id'] in s['locations']},
            description_coverage=entry['description_coverage']), 'proposed', 'traditional', []))


def _names(name):
    return [key for key, entry in DATA['entries'].items()
            if name.casefold() in [x.casefold() for x in [entry['original_name'], *entry['aliases']]]]


def _fact(key, schematic):
    entry = copy.deepcopy(DATA['entries'][key])
    location = DATA['schematics'][schematic]['locations'].get(key)
    entry['location'] = copy.deepcopy(location)
    entry['location_status'] = 'verified_printed_label' if location else 'unverified_anchor' if key == 'dagger' else 'not_shown_in_selected_panel'
    entry['interpretation_type'] = 'direct_historical_reference'
    entry['applied_to_individual'] = False
    return entry


def reference(value, registry=None):
    request = validate(value)
    if registry is not None:
        register_knowledge(registry)
    sid = request['schematic']
    region_id = request.get('region_id')
    region = DATA['regions'].get(region_id)
    region_status = ('not_selected' if region_id is None else 'unknown_region' if region is None
                     else 'schematic_conflict' if region['schematic'] != sid else 'verified_software_group')
    selections = request.get('selections', [])
    browsing = not selections and region_status == 'verified_software_group'
    if browsing:
        selections = [dict(label_id=k) for k in region['labels']]
    rows = []
    for selection in selections:
        keys = []
        if 'candidates' in selection:
            status = 'ambiguous'
            keys = [x for x in selection['candidates'] if x in DATA['entries']]
            reason = 'Candidate set retained; no automatic disambiguation or anatomical inference.'
        else:
            label = selection.get('label_id')
            names = _names(selection['name']) if 'name' in selection else []
            if label is not None and 'name' in selection:
                if label in DATA['entries'] and names == [label]:
                    keys, status = [label], 'resolved'
                else:
                    keys = list(dict.fromkeys(([label] if label in DATA['entries'] else []) + names))
                    status = 'conflict'
            elif label is not None:
                keys = [label] if label in DATA['entries'] else []
                status = 'resolved' if keys else 'unknown_label'
            else:
                keys = names
                status = 'resolved' if len(keys) == 1 else 'ambiguous' if keys else 'unknown_name'
            reason = 'Exact source lookup; no fuzzy or cross-edition fallback.'
        if status == 'resolved' and region_id is not None:
            if region_status != 'verified_software_group' or keys[0] not in region['labels']:
                status = 'conflict'
                reason = 'Label cannot be resolved consistently with selected region/schematic.'
        rows.append(dict(selection=selection, status=status, reason=reason,
            entry=_fact(keys[0],sid) if status == 'resolved' else None,
            candidate_references=[_fact(k,sid) for k in keys] if status != 'resolved' else []))
    return dict(schema_version=1, technique_id=10, profile=PROFILE, task='historical_reference',
        schematic={k:copy.deepcopy(v) for k,v in DATA['schematics'][sid].items() if k != 'locations'},
        region_id=region_id, region_status=region_status, region=copy.deepcopy(region),
        selection_mode='browse_software_group' if browsing else 'explicit_lookup', results=rows,
        inventory_count=copy.deepcopy(DATA['inventory_count']), source=copy.deepcopy(DATA['source']),
        conventions=copy.deepcopy(DATA['conventions']), terminology_conflicts=list(DATA['terminology_conflicts']),
        limitations=list(LIMITS), inference_enabled=False, individual_assessment=None)


def _escape(text):
    return str(text).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('|','\\|').replace('\n',' ')


def markdown(report):
    lines = ['# Phrenology — historical reference', '',
        '**Scientifically discredited doctrine. No individual assessment.**', '',
        'Profile: ' + report['profile'], '',
        report['schematic']['label'] + ': ' + report['schematic']['orientation'], '',
        'Region status: ' + report['region_status'], '',
        '| Selection | Status | Historical label | Printed location |',
        '|---|---|---|---|']
    for row in report['results']:
        entry = row['entry']
        lines.append('| ' + ' | '.join(_escape(x) for x in [json.dumps(row['selection'],ensure_ascii=False),row['status'],
            entry['original_name'] if entry else 'Unresolved',
            entry['location']['description'] if entry and entry['location'] else entry['location_status'] if entry else row['reason']]) + ' |')
    for index,row in enumerate(report['results'],1):
        for entry in ([row['entry']] if row['entry'] else row['candidate_references']):
            lines += ['', f"## Reference {index}: {entry['id']} — {entry['original_name']}", '',
                entry['historical_description'], '', 'Coverage: ' + entry['description_coverage'], '',
                'Source: ' + entry['source_id'] + '; ' + entry['legend_locator'] + '; ' + entry.get('description_locator',entry['chapter_locator']),
                'Rule: ' + entry['rule_id'] + ' v1; historical documentary reference,not empirical validation.']
            if entry['location']:
                lines += ['Location source: ' + entry['location']['locator']]
    lines += ['', '## Terminology and limitations', '']
    lines += ['- ' + x for x in report['terminology_conflicts'] + report['limitations']]
    lines += ['', '[Original source and rights metadata](' + report['source']['url'] + ')', '']
    return '\n'.join(lines)


def load_input(path):
    def pairs(items):
        result = {}
        for key,value in items:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('Nonfinite JSON value: ' + value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid)
