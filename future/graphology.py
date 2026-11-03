"""Schooling1892 manual descriptive references; never a writer assessment."""
import copy
import json
from pathlib import Path
from .knowledge import Rule
from .graphology_geometry import measure

DATA=json.loads((Path(__file__).resolve().parents[1]/'knowledge/graphology_schooling_v1.json').read_text(encoding='utf-8'))
PROFILE=DATA['profile']
FEATURES=sorted({f for t in DATA['terms'].values() for f in t['features']})
OPPOSITES=[{'ascending','descending'},{'rectilinear','serpentine'},{'vertical','reversed'},{'vertical','inclined'},
    {'reversed','inclined'},{'large','very_small'},{'regular','irregular'},{'crowded','spaced_out'},
    {'clear','confused'},{'light','muddy_heavy'},{'diminishing','enlarging'}]
LIMITS=['Historical/descriptive reference only; graphology is not a reliable personality or employment assessment.',
    'No writer intelligence,personality,mental health,criminality,honesty,employment suitability or other personal-trait classification.',
    'Manual labels are not independently recognized. No image input,OCR,signature authentication or forensic authorship determination.',
    'Geometry measures supplied vectors/dimensions only; no source size/spacing thresholds or personal interpretations derived.',
    'True pen pressure cannot be inferred from image darkness; calibrated physical/dynamic pressure processing is not implemented.',
    'Only the adapted1892 Schooling edition is supported; ABC,Saudek,German holistic,American applied and other scripts remain separate.',
    'Twenty selected ordinary-column labels are documentary context; complex combinations and writer-state selection are unsupported.']


def _object(value,keys,path):
    if not isinstance(value,dict):raise ValueError(path+' must be an object')
    if set(value)-set(keys):raise ValueError(path+': unsupported fields; no image,identity or personal assessment inputs')


def _id(value):
    return isinstance(value,str) and 0<len(value)<=80 and value.isascii() and all(c.isalnum() or c in '_-' for c in value)


def validate(value):
    _object(value,['schema_version','profile','task','mode','script','writing_direction','observations','geometry','pressure_evidence','example_id'],'input')
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE:raise ValueError('Unsupported source/edition; no cross-tradition fallback')
    if value.get('task')!='historical_reference':raise ValueError('Personal,clinical,criminality and employment assessment tasks are rejected')
    if value.get('mode')=='source_example':
        if set(value)&{'script','writing_direction','observations','geometry','pressure_evidence'}:raise ValueError('Source examples cannot be overridden')
        if not isinstance(value.get('example_id'),str) or value['example_id'] not in DATA['source_examples']:raise ValueError('Unknown source example')
        return copy.deepcopy(value)
    if value.get('mode')!='manual' or 'example_id' in value:raise ValueError('Use manual or source_example without mixed inputs')
    if not _id(value.get('script')) or value.get('writing_direction') not in ('ltr','rtl','unknown'):raise ValueError('Explicit script and writing_direction required')
    rows=value.get('observations',[])
    if not isinstance(rows,list) or len(rows)>40 or (not rows and 'geometry' not in value):raise ValueError('Supply1-40 observations or independent geometry')
    for row in rows:
        _object(row,['feature','category','scope','certainty'],'observation')
        if not _id(row.get('feature')) or not _id(row.get('scope','whole_sample')):raise ValueError('Feature and scope require identifiers')
        cats=row.get('category','unknown')
        if isinstance(cats,list):
            if not 2<=len(cats)<=8 or any(not _id(k) for k in cats) or len(set(cats))!=len(cats):raise ValueError('Ambiguous category set requires2-8 distinct identifiers')
        elif not _id(cats):raise ValueError('Invalid category')
        if row.get('certainty','certain') not in ('certain','uncertain','unknown'):raise ValueError('Invalid certainty')
    if value.get('pressure_evidence','not_supplied') not in ('not_supplied','image_darkness','physical_dynamic'):
        raise ValueError('Unsupported pressure evidence label')
    if 'geometry' in value:measure(value['geometry'])
    return copy.deepcopy(value)


def register_knowledge(registry):
    registry.add_source(DATA['source'])
    for t in DATA['terms'].values():
        registry.add_rule(Rule(t['rule_id'],t['version'],13,'historical descriptive terminology',PROFILE,t['source_id'],
            t['locator'],t['definition'],'historical_graphology_term_lookup',dict(category=t['id'],features=t['features'],
            exceptions=t['exceptions'],historical_context=t['historical_context'],interpretation_locator=t['interpretation_locator'],
            interpretation_coverage=t['interpretation_coverage'],individual_inference=False),'proposed','traditional',[]))


def _fact(key):
    t=copy.deepcopy(DATA['terms'][key]);t['coverage']='direct_descriptive_reference';t['applied_to_writer']=False
    return t


def reference(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    example=None
    if request['mode']=='source_example':
        example=copy.deepcopy(DATA['source_examples'][request['example_id']]);script='latin';direction='ltr'
        rows=[dict(feature=example['feature'],category=example['category'],scope='published_figure')]
    else:script=request['script'];direction=request['writing_direction'];rows=request.get('observations',[])
    applicable=script=='latin' and direction=='ltr';conflicts=[];bad=set()
    for i,a in enumerate(rows):
        ca=a.get('category','unknown')
        if not isinstance(ca,str) or ca not in DATA['terms'] or a['feature'] not in DATA['terms'][ca]['features'] or a.get('certainty','certain')!='certain':continue
        for j,b in enumerate(rows[:i]):
            cb=b.get('category','unknown')
            if (a['feature'],a.get('scope','whole_sample'))!=(b['feature'],b.get('scope','whole_sample')):continue
            if isinstance(cb,str) and cb in DATA['terms'] and b['feature'] in DATA['terms'][cb]['features'] and b.get('certainty','certain')=='certain' and any({ca,cb}==p for p in OPPOSITES):
                conflicts.append(dict(indices=[j,i],feature=a['feature'],scope=a.get('scope','whole_sample'),reason='Opposing uniform labels in same declared scope; retain both without choosing a winner.'));bad.update([j,i])
    results=[]
    for i,row in enumerate(rows):
        feature=row['feature'];cat=row.get('category','unknown');cats=cat if isinstance(cat,list) else [cat]
        known=[k for k in cats if k in DATA['terms'] and feature in DATA['terms'][k]['features']]
        if not applicable:status='unsupported_script_direction'
        elif i in bad:status='conflict'
        elif row.get('certainty','certain')!='certain' or cat=='unknown':status='unknown_or_uncertain'
        elif isinstance(cat,list):status='ambiguous'
        elif known:status='resolved_reference'
        else:status='unsupported_category'
        results.append(dict(observation=copy.deepcopy(row),scope=row.get('scope','whole_sample'),status=status,
            reference=_fact(known[0]) if status=='resolved_reference' else None,
            candidate_references=[_fact(k) for k in known] if status!='resolved_reference' else [],
            coverage='direct' if status=='resolved_reference' else 'unsupported' if status.startswith('unsupported') else 'unresolved'))
    geometry=measure(request['geometry']) if 'geometry' in request else None
    return dict(schema_version=1,technique_id=13,profile=PROFILE,task='historical_reference',script=script,writing_direction=direction,
        source_example=example,observations=results,conflicts=conflicts,geometry=geometry,
        geometry_reference_link='Independent numerical description; measurements never select historical terms or writer traits.',
        pressure=dict(evidence=request.get('pressure_evidence','not_supplied'),status='unsupported',reason='No calibrated force procedure implemented; neither image darkness nor coarse strokes establishes true pressure.'),
        source=copy.deepcopy(DATA['source']),source_cautions=copy.deepcopy(DATA['source_cautions']),conventions=copy.deepcopy(DATA['conventions']),
        coverage=dict(terms=23,features=len(FEATURES),published_examples=7,compositional_interpretation='unsupported'),
        limitations=list(LIMITS),inference_enabled=False,individual_assessment=None)


def markdown(report):
    lines=['# Graphology — historical/descriptive reference','','**No personal-trait,medical or employment assessment. Historical claims are documentary.**','',
        'Profile: '+report['profile'],'',report['source']['edition'],'',
        '| Feature | Manual category | Status | Source term |','|---|---|---|---|']
    for row in report['observations']:
        o=row['observation'];lines.append('| '+o['feature']+' | '+json.dumps(o.get('category','unknown'))+' | '+row['status']+' | '+(row['reference']['term'] if row['reference'] else 'Unresolved')+' |')
    for row in report['observations']:
        for t in ([row['reference']] if row['reference'] else row['candidate_references']):
            lines+=['','## '+t['term']+' ('+row['status']+')','',t['definition'],'',t['historical_context'],
                'Source: '+t['source_id']+'; '+t['locator'],'Rule: '+t['rule_id']+' v'+str(t['version']),
                'Interpretation coverage: '+t['interpretation_coverage']]
            if t['interpretation_locator']:lines+=['Historical context locator: '+t['interpretation_locator']]
            lines+=['- '+x for x in t['exceptions']]
    lines+=['','## Independent geometry and diagnostics','',json.dumps(report['geometry'],indent=2),report['geometry_reference_link'],
        'Pressure: '+report['pressure']['status']+'; '+report['pressure']['reason']]
    for c in report['conflicts']:lines+=['Conflict: '+json.dumps(c)]
    lines+=['','## Source conventions and limitations','']+['- '+c['locator']+': '+c['description'] for c in report['source_cautions']]
    lines+=['- '+x for x in report['limitations']]+['','[Original digitization]('+report['source']['url']+')','']
    return '\n'.join(lines)


def load_input(path):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate JSON key: '+k)
            out[k]=v
        return out
    def invalid(v):raise ValueError('Nonfinite JSON: '+v)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid)
