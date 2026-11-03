"""Fontaine documentary lookup,independent of any real person's skin."""
import copy
import json
from pathlib import Path
from .knowledge import Rule

DATA = json.loads((Path(__file__).resolve().parents[1]/'knowledge/moleosophy_fontaine_v1.json').read_text(encoding='utf-8'))
PROFILE = DATA['profile']
LIMITS = [
    'Historical/symbolic reference only. Mole-based character and future-outcome claims are not scientifically validated.',
    'No individual character,intelligence,criminality,health,longevity,personality or future-outcome conclusions.',
    'No personal photographs,measurements,medical observations,diagnosis or skin-cancer screening.',
    'Only27 selected documentary summaries across19 regions; not a complete edition or prognostic system.',
    'Chinese,Indian and other Western editions are unsupported; no tradition blending.',
    'Source examples are textual teaching selections,not real-person observations or original numbered mole diagrams.',
    'A correct historical transcription does not establish empirical validity.']


def _object(value, keys, path):
    if not isinstance(value,dict):
        raise ValueError(path+' must be an object')
    if set(value)-set(keys):
        raise ValueError(path+': unsupported fields; no personal images,skin observations or inference inputs')


def _identifier(value):
    return isinstance(value,str) and 0 < len(value) <= 80 and value.isascii() and all(c.isalnum() or c in '_-' for c in value)


def validate(value):
    _object(value,['schema_version','profile','task','mode','schematic_id','orientation','selections','example_id'],'input')
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:
        raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE:
        raise ValueError('Unsupported source profile; no cross-school or edition fallback')
    if value.get('task')!='historical_reference':
        raise ValueError('Only historical_reference is supported; personalized or medical inference is rejected')
    if value.get('schematic_id',DATA['schematic']['id'])!=DATA['schematic']['id']:
        raise ValueError('Unsupported schematic; only the named textual teaching index is available')
    if value.get('mode')=='source_example':
        if set(value)&{'orientation','selections'}:
            raise ValueError('Source examples cannot be overridden with manual selections or orientation')
        if not isinstance(value.get('example_id'),str) or value['example_id'] not in DATA['source_examples']:
            raise ValueError('Unknown source example')
        return copy.deepcopy(value)
    if value.get('mode')!='manual' or 'example_id' in value:
        raise ValueError('Select manual or source_example mode without mixed inputs')
    orientation=value.get('orientation')
    _object(orientation,['frame','view','mirrored'],'orientation')
    if orientation.get('frame') not in ('subject','viewer') or orientation.get('view') not in ('frontal','posterior','unknown'):
        raise ValueError('Explicit subject/viewer frame and frontal/posterior/unknown view required')
    if not (type(orientation.get('mirrored')) is bool or orientation.get('mirrored')=='unknown'):
        raise ValueError('Explicit boolean or unknown mirroring required')
    selections=value.get('selections')
    if not isinstance(selections,list) or not 1<=len(selections)<=32:
        raise ValueError('Supply1-32 historical reference selections')
    for row in selections:
        _object(row,['entry_id','region_id','side','location_id'],'selection')
        if not set(row)&{'entry_id','region_id'}:
            raise ValueError('Select an entry or region')
        for key in ('entry_id','region_id','location_id'):
            if key in row and not _identifier(row[key]):
                raise ValueError('Invalid '+key+'; use exact string identifiers')
        if 'side' in row and row['side'] not in ('left','right','midline','unknown'):
            raise ValueError('side must be left,right,midline or unknown')
    return copy.deepcopy(value)


def normalize_side(side, orientation):
    if orientation['frame']=='subject' or side in ('midline','unknown'):
        return side,[]
    if orientation['view']!='frontal' or type(orientation['mirrored']) is not bool:
        return 'unknown',['Viewer side is unresolved; only known frontal mirroring can transform side labels.']
    return (side if orientation['mirrored'] else 'right' if side=='left' else 'left'),[]


def register_knowledge(registry):
    registry.add_source(DATA['source'])
    for key,entry in DATA['entries'].items():
        registry.add_rule(Rule(entry['rule_id'],entry['version'],11,'historical mole reference',PROFILE,entry['source_id'],
            entry['locator'],entry['historical_association'],'historical_region_entry_lookup',
            dict(entry_id=key,region_id=entry['region_id'],source_side=entry['source_side'],location_id=entry['location_id'],
                 qualifications=entry['qualifications'],individual_inference=False), 'proposed','traditional',[]))


def _fact(key):
    value=copy.deepcopy(DATA['entries'][key])
    value['applied_to_individual']=False
    return value


def _matches(entry,side,location):
    # Unknown constraints retain candidates; no most-likely or closest-location guessing.
    return (side=='unknown' or entry['source_side'] in ('either','unspecified',side)) and (location=='unknown' or location==entry['location_id'])


def reference(value, registry=None):
    request=validate(value)
    if registry is not None:
        register_knowledge(registry)
    example=None
    if request['mode']=='source_example':
        example=copy.deepcopy(DATA['source_examples'][request['example_id']])
        selections=[{k:example[k] for k in ('region_id','side','location_id')}]
        orientation=dict(frame='subject',view='unknown',mirrored=False)
    else:
        selections=request['selections'];orientation=request['orientation']
    results=[]
    for row in selections:
        side,issues=normalize_side(row.get('side','unknown'),orientation)
        raw_region=row.get('region_id');region=DATA['aliases'].get(raw_region,raw_region)
        location=row.get('location_id','unknown')
        asserted=row.get('entry_id')
        keys=[key for key,entry in DATA['entries'].items() if (region is None or entry['region_id']==region) and _matches(entry,side,location)]
        candidate_keys=keys
        if asserted is not None:
            if asserted not in DATA['entries']:
                status='conflict' if raw_region is not None and keys else 'unknown_entry'
                candidate_keys=keys if raw_region is not None else []
            elif asserted not in keys:
                status='conflict';candidate_keys=list(dict.fromkeys([asserted]+keys))
            elif issues and DATA['entries'][asserted]['source_side'] in ('left','right'):
                status='orientation_unresolved';candidate_keys=[asserted]
            else:
                status='resolved';candidate_keys=[asserted]
        elif not keys:
            status='unsupported_reference'
        elif issues and any(DATA['entries'][key]['source_side'] in ('left','right') for key in keys):
            status='orientation_unresolved'
        elif len(keys)==1:
            status='resolved'
        else:
            status='ambiguous'
        # Contradictions never select an entry. Candidate facts are documentary alternatives only.
        results.append(dict(selection=copy.deepcopy(row),canonical_subject_side=side,canonical_region_id=region,
            alias_locator='Mouth cross-reference,printed p118/PDF128 -> Lips,p117/PDF127' if raw_region=='mouth' else None,
            status=status,issues=issues,entry=_fact(candidate_keys[0]) if status=='resolved' else None,
            candidate_references=[_fact(k) for k in candidate_keys] if status!='resolved' else [],
            reason='Exact source constraints; unresolved constraints and conflicts are not automatically cleared.'))
    return dict(schema_version=1,technique_id=11,profile=PROFILE,task='historical_reference',mode=request['mode'],
        schematic=copy.deepcopy(DATA['schematic']),orientation=copy.deepcopy(orientation),source_example=example,
        results=results,source=copy.deepcopy(DATA['source']),conventions=copy.deepcopy(DATA['conventions']),
        general_qualifications=copy.deepcopy(DATA['general_qualifications']),terminology_conflicts=list(DATA['terminology_conflicts']),
        coverage=dict(entries=len(DATA['entries']),regions=len({e['region_id'] for e in DATA['entries'].values()}),
            description_type='selected attributed documentary summaries; no individualized interpretations'),
        limitations=list(LIMITS),inference_enabled=False,individual_assessment=None)


def _escape(value):
    return str(value).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('|','\\|').replace('\n',' ')


def markdown(report):
    lines=['# Moleosophy — historical/symbolic reference','','**No individual assessment or medical interpretation. Historical claims are not scientifically validated.**','',
        'Profile: '+report['profile'],'',report['source']['edition'],'',
        'Teaching index: '+report['schematic']['id']+' — '+report['schematic']['kind'],'',
        '| Historical selection | Status | Subject side | Entry |','|---|---|---|---|']
    for row in report['results']:
        lines.append('| '+' | '.join(_escape(x) for x in [json.dumps(row['selection']),row['status'],row['canonical_subject_side'],
            row['entry']['original_label'] if row['entry'] else 'Unresolved'])+' |')
    for i,row in enumerate(report['results'],1):
        lines+=['',f'## Selection {i}: {row["status"]}','',row['reason']]
        lines+=['- '+x for x in row['issues']]
        if row['alias_locator']:lines+=['Alias source: '+row['alias_locator']]
        for entry in ([row['entry']] if row['entry'] else row['candidate_references']):
            lines+=['',('Reference: ' if row['entry'] else 'Unresolved candidate: ')+entry['id']+' — '+entry['original_label'],'',
                entry['historical_association'],'',
                'Source region/side/location: '+entry['region_id']+' / '+entry['source_side']+' / '+entry['location_id'],
                'Source: '+entry['source_id']+'; '+entry['locator'],
                'Rule: '+entry['rule_id']+' v'+str(entry['version'])+'; '+entry['interpretation_type']+'; '+entry['coverage']]
            lines+=['- '+q for q in entry['qualifications']]
            if entry.get('cross_references'):lines+=['Related source entries: '+', '.join(entry['cross_references'])]
    lines+=['','## Qualifications and limitations','',report['general_qualifications']['description'],
        'Source: '+report['general_qualifications']['locator'],'']
    lines+=['- '+x for x in report['terminology_conflicts']+report['limitations']]
    lines+=['','[Original containing work]('+report['source']['url']+')','']
    return '\n'.join(lines)


def load_input(path):
    def pairs(items):
        value={}
        for k,v in items:
            if k in value:raise ValueError('Duplicate JSON key: '+k)
            value[k]=v
        return value
    def invalid(value):
        raise ValueError('Nonfinite JSON value: '+value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid)
