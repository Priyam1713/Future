"""Documentary foot/sole references,never appearance-to-person assessment."""
import copy
import json
from pathlib import Path
from .knowledge import Rule

DATA=json.loads((Path(__file__).resolve().parents[1]/'knowledge/podomancy_reference_v1.json').read_text(encoding='utf-8'))
PROFILE=DATA['profile']
LIMITS=[DATA['scientific_scope'],
    'Only six source descriptions in two regions; no verified individual toe names/order or toe-shape method.',
    'Anonymous undated Booksellers edition in Gutenberg67858; exact print year and matching original page images remain unverified.',
    'Source descriptions are qualitative phrases,not measurable diagnostic categories or classification thresholds.',
    'Somogyi,Sheehan,Indian traditions and other editions remain unsupported and separate.',
    'No personal photographs,measurements,medical observations,reflexology recommendations or individual assessment.',
    'Historical fidelity does not establish scientific or predictive validity.']


def _object(value,keys,path):
    if not isinstance(value,dict):raise ValueError(path+' must be an object')
    if set(value)-set(keys):raise ValueError(path+': unsupported fields; no personal images,measurements or medical input')


def _id(value):
    return isinstance(value,str) and 0<len(value)<=80 and value.isascii() and all(c.isalnum() or c in '_-' for c in value)


def validate(value):
    _object(value,['schema_version','profile','task','mode','schematic_id','orientation','selections','example_id'],'input')
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE:raise ValueError('Unsupported profile; no cross-source fallback')
    if value.get('task')!='historical_reference':raise ValueError('Only historical_reference supported; personal or medical inference rejected')
    if value.get('schematic_id',DATA['schematic']['id'])!=DATA['schematic']['id']:raise ValueError('Unknown teaching index; no original diagram mapping claimed')
    if value.get('mode')=='source_example':
        if set(value)&{'selections','orientation'}:raise ValueError('Source example cannot be overridden')
        if not isinstance(value.get('example_id'),str) or value['example_id'] not in DATA['source_examples']:raise ValueError('Unknown source example')
        return copy.deepcopy(value)
    if value.get('mode')!='manual' or 'example_id' in value:raise ValueError('Use manual or source_example without mixed inputs')
    orientation=value.get('orientation')
    _object(orientation,['frame','view','mirrored'],'orientation')
    if orientation.get('frame') not in ('subject','viewer') or orientation.get('view') not in ('dorsal','plantar','unknown'):
        raise ValueError('Explicit subject/viewer frame and dorsal/plantar/unknown view required')
    if not(type(orientation.get('mirrored')) is bool or orientation.get('mirrored')=='unknown'):raise ValueError('Explicit boolean or unknown mirroring required')
    rows=value.get('selections')
    if not isinstance(rows,list) or not 1<=len(rows)<=24:raise ValueError('Supply1-24 historical reference selections')
    for row in rows:
        _object(row,['entry_id','region_id','side','certainty','candidates'],'selection')
        if not set(row)&{'entry_id','region_id','candidates'}:raise ValueError('Select entry,region or ambiguous candidate IDs')
        for field in ('entry_id','region_id'):
            if field in row and not _id(row[field]):raise ValueError('Invalid '+field)
        if row.get('side','unknown') not in ('left','right','both','unknown'):raise ValueError('side must be subject left/right,both or unknown')
        if row.get('certainty','certain') not in ('certain','uncertain','unknown'):raise ValueError('Invalid certainty label')
        if 'candidates' in row:
            c=row['candidates']
            if 'entry_id' in row or not isinstance(c,list) or not 2<=len(c)<=12 or any(not _id(k) for k in c) or len(set(c))!=len(c):
                raise ValueError('Use2-12 distinct candidate IDs without an asserted entry')
    return copy.deepcopy(value)


def register_knowledge(registry):
    registry.add_source(DATA['source'])
    for e in DATA['entries'].values():
        registry.add_rule(Rule(e['rule_id'],e['version'],12,'historical foot reference',PROFILE,e['source_id'],e['locator'],
            e['historical_association'],'historical_foot_entry_lookup',dict(entry_id=e['id'],region_id=e['region_id'],
            view_requirement=e['view_requirement'],qualifications=e['qualifications'],individual_inference=False),
            'proposed','traditional',[]))


def _fact(key):
    e=copy.deepcopy(DATA['entries'][key]);e['applied_to_individual']=False
    return e


def reference(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    example=None
    if request['mode']=='source_example':
        example=copy.deepcopy(DATA['source_examples'][request['example_id']])
        orientation=dict(frame='subject',view=example['view'],mirrored=False)
        rows=[{k:example[k] for k in ('entry_id','region_id','side')}]
    else:orientation=request['orientation'];rows=request['selections']
    results=[]
    for row in rows:
        issues=[];side=row.get('side','unknown')
        if orientation['frame']=='viewer' and side in ('left','right'):
            side='unknown';issues.append('No verified viewer-to-subject foot layout; viewer side remains unknown regardless of mirrored flag.')
        if side=='unknown':issues.append('Subject side missing or unknown; source has no side-specific rule.')
        if row.get('certainty','certain')!='certain':issues.append('Selection is '+row['certainty']+'; no automatic certainty promotion.')
        if orientation['mirrored']=='unknown':issues.append('Mirroring unknown; no geometry or anatomical orientation inferred.')
        keys=[k for k,e in DATA['entries'].items() if 'region_id' not in row or e['region_id']==row['region_id']]
        if 'candidates' in row:
            # Retain the supplied ambiguity,including unknown IDs; never pick a remaining known entry.
            candidates=[k for k in row['candidates'] if k in DATA['entries']]
            status='conflict' if any(k not in keys for k in candidates) else 'ambiguous'
        elif 'entry_id' in row:
            key=row['entry_id'];candidates=[key] if key in DATA['entries'] else []
            status='unsupported_reference' if not candidates else 'conflict' if key not in keys else 'resolved_reference'
        else:
            candidates=keys;status='ambiguous' if keys else 'unsupported_reference'
        if status=='resolved_reference':
            e=DATA['entries'][candidates[0]]
            if e['view_requirement']=='plantar' and orientation['view']=='dorsal':
                status='view_conflict';issues.append('A dorsal view cannot establish a sole reference; documentary text remains available as a candidate.')
            elif e['view_requirement']=='plantar' and orientation['view']=='unknown':
                issues.append('Sole reference requires plantar context; view unknown.')
            if status=='resolved_reference' and issues:status='partial_reference'
        results.append(dict(selection=copy.deepcopy(row),canonical_subject_side=side,status=status,issues=issues,
            entry=_fact(candidates[0]) if status=='resolved_reference' else None,
            candidate_references=[_fact(k) for k in candidates] if status!='resolved_reference' else [],
            unknown_candidate_ids=[k for k in row.get('candidates',[]) if k not in DATA['entries']],
            reason='Documentary identifier lookup only; no foot appearance is measured or converted into a person judgment.'))
    return dict(schema_version=1,technique_id=12,profile=PROFILE,task='historical_reference',mode=request['mode'],
        orientation=copy.deepcopy(orientation),source_example=example,schematic=copy.deepcopy(DATA['schematic']),results=results,
        source=copy.deepcopy(DATA['source']),coverage=dict(entries=6,regions=2,toe_rules=0,description_type='direct documentary paraphrases'),
        conventions=copy.deepcopy(DATA['conventions']),source_conflicts=list(DATA['conflicts']),limitations=list(LIMITS),
        inference_enabled=False,individual_assessment=None)


def markdown(report):
    lines=['# Podomancy — historical reference','','**No individualized trait,health or life-outcome assessment. Historical claims are not scientifically validated.**','',
        'Profile: '+report['profile'],'','Source author: '+report['source']['author'],report['source']['edition'],'',
        '| Selection | Status | Subject side | Historical entry |','|---|---|---|---|']
    for row in report['results']:
        lines.append('| '+json.dumps(row['selection'])+' | '+row['status']+' | '+row['canonical_subject_side']+' | '+(row['entry']['source_label'] if row['entry'] else 'Unresolved')+' |')
    for i,row in enumerate(report['results'],1):
        lines+=['',f'## Selection {i}: {row["status"]}','',row['reason']]+['- '+x for x in row['issues']]
        for e in ([row['entry']] if row['entry'] else row['candidate_references']):
            lines+=['',('Reference: ' if row['entry'] else 'Unresolved candidate: ')+e['id'],'',e['historical_association'],'',
                'Source: '+e['source_id']+'; '+e['locator'],'Rule: '+e['rule_id']+' v'+str(e['version'])+'; '+e['coverage']]
            lines+=['- '+x for x in e['qualifications']]
        if row['unknown_candidate_ids']:lines+=['Unknown candidate IDs: '+', '.join(row['unknown_candidate_ids'])]
    lines+=['','## Source conflicts and limitations','']+['- '+x for x in report['source_conflicts']+report['limitations']]
    lines+=['','[Primary-text transcription]('+report['source']['url']+')','']
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
