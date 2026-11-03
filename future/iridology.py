"""Literal historical schematic reference; never a personal iris assessment."""
import copy
import html
import json
from pathlib import Path
from .knowledge import Rule

DATA=json.loads((Path(__file__).resolve().parents[1]/'knowledge/iridology_lindlahr_v1.json').read_text(encoding='utf-8'))
PROFILE=DATA['profile']
LIMITS=[DATA['scientific_statement'],
    'Manual historical labels only;no patient images,medical histories,biometrics,health scores or personal-trait assessment.',
    '33 selected labels are supported,not the complete original chart or clinical doctrine.',
    'Source eye names describe the upright plate only;no patient,mirror,camera or image-orientation transformation.',
    'Printed perimeter numbers are not assumed unique label IDs,equal angular sectors or calibrated clock positions.',
    'Numeric radial boundaries,clock-based label inference and automatic sector recognition are unsupported.',
    'Jensen,Deck and Rayid remain separate unsupported profiles;no cross-source substitutions.',
    'Historical claims and exceptions are documentary;no disease signs,treatments or health predictions are implemented.']


def _object(value,keys,path):
    if not isinstance(value,dict) or set(value)-set(keys):
        raise ValueError(path+': unsupported fields;no patient,image,medical or trait-assessment inputs')


def _text(value,limit=100):
    return isinstance(value,str) and bool(value.strip()) and len(value)<=limit and not any(ord(c)<32 for c in value)


def validate(value):
    _object(value,['schema_version','profile','task','mode','diagram','view','selections','example_id'],'input')
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:
        raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE:
        raise ValueError('Unsupported edition/tradition;no Jensen,Deck or Rayid fallback')
    if value.get('task')!='historical_reference':
        raise ValueError('Only historical_reference;diagnosis,screening,treatment and personal assessments rejected')
    if value.get('diagram')!='frontispiece' or value.get('view')!='source_plate_upright':
        raise ValueError('Only frontispiece in source_plate_upright view;no patient or mirror transforms')
    if value.get('mode')=='source_example':
        if 'selections' in value:
            raise ValueError('Published schematic examples cannot be overridden')
        if not isinstance(value.get('example_id'),str) or value['example_id'] not in DATA['source_examples']:
            raise ValueError('Unknown published schematic example')
        return copy.deepcopy(value)
    if value.get('mode')!='manual' or 'example_id' in value:
        raise ValueError('Use manual or source_example without mixed inputs')
    rows=value.get('selections')
    if not isinstance(rows,list) or not 1<=len(rows)<=24:
        raise ValueError('Supply1-24 historical schematic selections')
    for row in rows:
        _object(row,['eye','label_id','region_id','sector_id','clock_position','radial_band','certainty'],'selection')
        if row.get('eye','unknown') not in ('right','left','unknown'):
            raise ValueError('Eye must be right,left or unknown as named in the source')
        label=row.get('label_id')
        if isinstance(label,list):
            if not 2<=len(label)<=8 or any(not _text(x) for x in label) or len(set(label))!=len(label):
                raise ValueError('Ambiguous label requires2-8 distinct identifiers')
        elif label is not None and not _text(label):
            raise ValueError('Invalid label identifier')
        for key in ['region_id','sector_id','clock_position','radial_band']:
            if key in row and row[key] is not None and not _text(row[key]):
                raise ValueError(key+' must be text or null;coordinate annotations are not metric lookup inputs')
        if row.get('certainty','selected') not in ('selected','uncertain','unknown'):
            raise ValueError('Unsupported certainty')
    return copy.deepcopy(value)


def register_knowledge(registry):
    registry.add_source(DATA['source'])
    for entry in DATA['entries'].values():
        registry.add_rule(Rule(entry['rule_id'],entry['version'],15,'historical iris-map reference',PROFILE,
            entry['source_id'],entry['locator'],entry['description'],'historical_schematic_label_lookup',
            dict(eye=entry['eye'],label_id=entry['label_id'],printed_label=entry['printed_label'],
                placement=entry['placement'],parent_label=entry['parent_label'],individual_inference=False),
            'proposed','traditional',[]))
    diagram=DATA['diagrams']['frontispiece']
    registry.add_rule(Rule('iridology.lindlahr.1922.orientation',1,15,'historical iris-map reference',PROFILE,
        DATA['source']['id'],diagram['locator'],DATA['conventions']['orientation'],'literal_plate_orientation',
        dict(orientation=diagram['orientation'],patient_transform='unsupported'),'proposed','traditional',[]))
    for key,example in DATA['source_examples'].items():
        registry.add_rule(Rule('iridology.lindlahr.1922.example.'+key,1,15,'historical iris-map reference',PROFILE,
            DATA['source']['id'],example['locator'],example['description'],'published_schematic_selection',
            dict(selections=example['selections'],individual_inference=False),'proposed','traditional',[]))


def _lookup(row):
    eye=row.get('eye','unknown');label=row.get('label_id');region=row.get('region_id')
    ids=label if isinstance(label,list) else [label]
    candidates=[copy.deepcopy(e) for e in DATA['entries'].values() if (eye=='unknown' or eye==e['eye']) and e['label_id'] in ids]
    selected_region=DATA['entries'].get(region) if region else None
    conflict=False
    if selected_region:
        conflict=(eye!='unknown' and eye!=selected_region['eye']) or (label is not None and selected_region['label_id'] not in ids)
        if not candidates:candidates=[copy.deepcopy(selected_region)]
        elif selected_region['id'] not in {c['id'] for c in candidates}:candidates.append(copy.deepcopy(selected_region))
    if conflict:status='conflict'
    elif row.get('certainty','selected')!='selected':status='unknown_or_uncertain'
    elif eye=='unknown':status='unknown_eye'
    elif region and not selected_region:status='unsupported_region'
    elif isinstance(label,list):status='ambiguous'
    elif selected_region:status='resolved_reference'
    elif label in (None,'unknown'):status='unsupported_sector' if row.get('sector_id') else 'unknown_or_uncertain'
    elif candidates:status='resolved_reference'
    else:status='unsupported_label_for_eye'
    reasons={
        'conflict':'Eye,label and region selections disagree;neither alternative is applied.',
        'unknown_or_uncertain':'Missing or uncertain label;no reference is selected.',
        'unknown_eye':'Source eye is unspecified;candidate labels retained without choosing an eye.',
        'unsupported_region':'Region identifier is not in the verified selected legend.',
        'ambiguous':'Alternative labels retained without choosing a reference.',
        'resolved_reference':'Literal selected label from this historical plate;not a real iris observation.',
        'unsupported_sector':'Perimeter-mark-to-label lookup is unverified;no equal-sector assumption.',
        'unsupported_label_for_eye':'No supported label for this eye in this edition subset;no cross-eye/source fallback.'}
    fact=None
    if status=='resolved_reference':
        fact=copy.deepcopy(selected_region) if selected_region else candidates[0]
    annotations={k:dict(value=row[k],status='unsupported_for_lookup',used_for_label_selection=False,
        reason='No verified metric clock/radial/perimeter-sector boundaries;annotation retained only.') for k in ['sector_id','clock_position','radial_band'] if k in row}
    return dict(selection=copy.deepcopy(row),status=status,reason=reasons[status],
        coverage='direct' if fact else 'unsupported' if status.startswith('unsupported') else 'unresolved',
        reference=fact,candidate_references=candidates if fact is None else [],annotations=annotations,
        placement_on_plate=DATA['diagrams']['frontispiece']['orientation'].get(eye),personal_inference=False)


def reference(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    example=copy.deepcopy(DATA['source_examples'][request['example_id']]) if request['mode']=='source_example' else None
    rows=example['selections'] if example else request['selections']
    results=[_lookup(row) for row in rows]
    return dict(schema_version=1,technique_id=15,profile=PROFILE,task='historical_reference',mode=request['mode'],
        diagram=copy.deepcopy(DATA['diagrams']['frontispiece']),source_example=example,selections=results,
        source=copy.deepcopy(DATA['source']),source_cautions=copy.deepcopy(DATA['source_cautions']),conventions=copy.deepcopy(DATA['conventions']),
        coverage=dict(supported_entries=len(DATA['entries']),complete_chart=False,
            resolved=sum(x['status']=='resolved_reference' for x in results),unresolved=sum(x['status']!='resolved_reference' for x in results)),
        geometry=dict(status='unsupported',reason='No exact polar or radial boundaries verified;no coordinates infer a label.',
            clock_normalization=False,left_right_transform=False,radial_boundary_lookup=False),
        scientific_validity=dict(statement=DATA['scientific_statement'],source_ids=list(DATA['scientific_sources']),
            sources=['https://pubmed.ncbi.nlm.nih.gov/480560/','https://pubmed.ncbi.nlm.nih.gov/10213874/'],diagnostic_validation=False),
        limitations=list(LIMITS),inference_enabled=False,individual_assessment=None,medical_assessment=None)


def _md(value):return html.escape(str(value),quote=False).replace('|','&#124;').replace('\n',' ')


def markdown(report):
    lines=['# Iridology — historical/educational reference','','**No personal iris analysis or medical assessment.**','',
        'Profile: '+report['profile'],'',report['source']['edition'],'',
        'Diagram: '+report['diagram']['title']+'; '+report['diagram']['credit']+'; '+report['diagram']['locator'],
        '',report['conventions']['orientation'],'','| Eye | Selected label / region | Status | Printed label |','|---|---|---|---|']
    for r in report['selections']:
        s=r['selection'];t=r['reference']
        lines.append('| '+' | '.join(_md(v) for v in [s.get('eye','unknown'),s.get('label_id') or s.get('region_id','unknown'),r['status'],t['printed_label'] if t else 'Unresolved'])+' |')
    for r in report['selections']:
        lines+=['','Diagnostic: '+r['reason']]
        for t in ([r['reference']] if r['reference'] else r['candidate_references']):
            lines+=['','## '+t['eye']+' iris — '+t['printed_label'],'',t['description'],
                'Parent label: '+str(t['parent_label'])+'; qualitative placement: '+t['placement'],
                'Source: '+t['source_id']+'; '+t['locator'],'Rule: '+t['rule_id']+' v'+str(t['version']),
                'Identifier: '+t['id']+' ('+t['identifier_kind']+'); printed number: '+str(t['printed_number'])]
            lines+=['- '+q for q in t['qualifications']]
        for k,a in r['annotations'].items():lines+=['Annotation '+k+': '+_md(a['value'])+'; '+a['status']+'; '+a['reason']]
    if report['source_example']:
        e=report['source_example'];lines+=['','Teaching selection from published schematic: '+e['description'],
            'Editorial selection of source labels,not a published historical patient case.','Source locator: '+e['locator']]
    lines+=['','## Scientific validity and limits','',report['scientific_validity']['statement']]
    lines+=['- '+x for x in report['limitations']]
    lines+=['- '+c['locator']+': '+c['description'] for c in report['source_cautions']]
    lines+=['',report['source']['rights_note'],'','[Original source]('+report['source']['url']+')',
        '[Masked diagnostic evaluation]('+report['scientific_validity']['sources'][0]+')',
        '[Scientific review]('+report['scientific_validity']['sources'][1]+')','']
    return '\n'.join(lines)


def load_input(path):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate JSON key: '+k)
            out[k]=v
        return out
    def invalid(value):raise ValueError('Nonfinite JSON: '+value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid)
