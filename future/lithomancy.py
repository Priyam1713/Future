"""Source-specific manual stone reading with exact, explicitly editorial geometry."""
import copy
import html
import json
from pathlib import Path
import re
from types import MappingProxyType
from .knowledge import Rule
from .scrying import freeze,thaw,digest,_object,_optional_text,load_input

ROOT=Path(__file__).resolve().parents[1]
DATA=freeze(json.loads((ROOT/'knowledge/lithomancy_profile_v1.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile'];PROFILE_HASH=digest(thaw(DATA))
ROLES=MappingProxyType({r['role_id']:r for r in DATA['roles']})
FRAMES=DATA['spatial_contract']['frames']
LIMIT=1000000


def _id(v):
    return isinstance(v,str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',v) is not None


def point(v):
    if v is None:return None
    _object(v,['x','y'])
    if set(v)!={'x','y'} or any(type(n) is not int or not -LIMIT<=n<=LIMIT for n in v.values()):
        raise ValueError('Position must be null/unknown or exact x/y integers in -1000000..1000000; booleans rejected')
    return dict(v)


def distance_squared(a,b):
    a,b=point(a),point(b)
    if a is None or b is None:return None
    return (a['x']-b['x'])**2+(a['y']-b['y'])**2


def directions(a,b,frame):
    if frame not in FRAMES:raise ValueError('Unknown coordinate frame')
    a,b=point(a),point(b)
    if a is None or b is None:return None
    dx,dy=a['x']-b['x'],a['y']-b['y']
    if frame.endswith('y-down-v1'):dy=-dy
    return ['left' if dx<0 else 'right' if dx>0 else 'same_x',
            'below' if dy<0 else 'above' if dy>0 else 'same_y']


def geometry(points,anchor,frame):
    """Exact relative ranks. This function assigns no symbolic meanings."""
    if frame not in FRAMES:raise ValueError('Unknown coordinate frame')
    anchor=point(anchor)
    rows=[]
    for identifier,p in points.items():
        p=point(p);d=distance_squared(p,anchor)
        rows.append(dict(id=identifier,position=p,distance_squared=d,
                         delta=dict(x=p['x']-anchor['x'],y=p['y']-anchor['y']) if p is not None and anchor is not None else None,
                         direction=directions(p,anchor,frame)))
    distances=sorted({r['distance_squared'] for r in rows if r['distance_squared'] is not None})
    groups=[dict(distance_squared=d,ids=sorted(r['id'] for r in rows if r['distance_squared']==d)) for d in distances]
    return dict(distances=rows,ordered_distance_groups=groups,
        nearest_known=groups[0]['ids'] if groups else [],farthest_known=groups[-1]['ids'] if groups else [],
        unknown_positions=[r['id'] for r in rows if r['position'] is None],anchor_position_known=anchor is not None,
        tie_policy='All equal distances share priority; ID ordering serializes ties only.')


def validate(value):
    _object(value,['schema_version','profile','task','mode','reading_id','frame','coverage','origin',
                   'stones','anchor','groups','relations','question','intention','commentary','uncertainty'])
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:
        raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE or value.get('mode')!='manual' or value.get('task')!='manual_spatial_reading':
        raise ValueError('Exact Howard general-set profile, manual mode and manual_spatial_reading task required')
    if not _id(value.get('reading_id')):raise ValueError('Explicit bounded reading_id required')
    if value.get('frame') not in FRAMES:raise ValueError('Explicit supported coordinate frame required')
    if value.get('coverage') not in ('full_example','subset'):raise ValueError('Declare full_example or subset coverage')
    if value.get('origin','unknown') not in ('reported_real','hypothetical','synthetic','unknown'):raise ValueError('Unknown origin')
    for key in ('question','intention','commentary'):_optional_text(value,key,10000)
    if 'uncertainty' in value and type(value['uncertainty']) is not bool:raise ValueError('Uncertainty must be boolean')
    rows=value.get('stones')
    if not isinstance(rows,list) or not 1<=len(rows)<=12:raise ValueError('Exactly1–12 manually declared stone instances required')
    ids=set();roles=set()
    for row in rows:
        _object(row,['id','role_id','position','association','commentary','uncertainty'])
        if not _id(row.get('id')) or row['id'] in ids:raise ValueError('Unique bounded stone IDs required')
        role=row.get('role_id')
        if not isinstance(role,str) or role not in ROLES or role in roles:raise ValueError('Unique Howard example role IDs required; mixed-author and unknown roles unsupported')
        ids.add(row['id']);roles.add(role);point(row.get('position'))
        for k in ('association','commentary'):_optional_text(row,k,10000)
        if 'uncertainty' in row and type(row['uncertainty']) is not bool:raise ValueError('Stone uncertainty must be boolean')
    if value['coverage']=='full_example' and roles!=set(ROLES):raise ValueError('full_example requires all twelve distinct roles; declare subset for incomplete cast')
    anchor=value.get('anchor')
    if anchor is not None:
        _object(anchor,['kind','stone_id','position'])
        if anchor.get('kind')=='personal_stone':
            if set(anchor)!={'kind','stone_id'} or not _id(anchor.get('stone_id')) or anchor['stone_id'] not in ids:
                raise ValueError('Personal anchor must explicitly reference one present stone, without a reader position')
        elif anchor.get('kind')=='reader':
            if set(anchor)!={'kind','position'}:raise ValueError('Reader anchor requires explicit position or null, without personal stone ID')
            point(anchor['position'])
        else:raise ValueError('Anchor kind must be personal_stone or reader')
    groups=value.get('groups',[])
    if not isinstance(groups,list) or len(groups)>12:raise ValueError('At most12 user-declared groups allowed')
    group_ids=set()
    for group in groups:
        _object(group,['id','members','association'])
        if not _id(group.get('id')) or group['id'] in group_ids:raise ValueError('Unique bounded group IDs required')
        group_ids.add(group['id']);members=group.get('members')
        if not isinstance(members,list) or not 2<=len(members)<=12 or any(not _id(i) or i not in ids for i in members) or len(set(members))!=len(members):
            raise ValueError('Group requires2–12 distinct present stone IDs')
        _optional_text(group,'association',10000)
    relations=value.get('relations',[])
    if not isinstance(relations,list) or len(relations)>64:raise ValueError('At most64 declared qualitative relations allowed')
    for relation in relations:
        _object(relation,['from','to','relation','association'])
        if any(not _id(relation.get(k)) or relation[k] not in ids for k in ('from','to')) or relation['from']==relation['to']:
            raise ValueError('Relation requires two distinct present stone IDs')
        if relation.get('relation') not in ('left','right','above','below','coincident','near','far','unknown'):raise ValueError('Unknown qualitative relation')
        _optional_text(relation,'association',10000)
    return copy.deepcopy(value)


def _relation_checks(q,points):
    result=[]
    for row in q.get('relations',[]):
        a,b=points[row['from']],points[row['to']];relation=row['relation']
        if relation in ('near','far','unknown'):
            state='unquantified_user_declaration'
        elif a is None or b is None:state='insufficient_evidence'
        else:
            expected=distance_squared(a,b)==0 if relation=='coincident' else relation in directions(a,b,q['frame'])
            state='consistent' if expected else 'conflicting_evidence'
        result.append(dict(declaration=copy.deepcopy(row),status=state,
                           qualification='User-attributed relationship; no source-backed threshold or symbolic direction inferred.'))
    return result


def register_knowledge(registry):
    registry.add_source(thaw(DATA['source']))
    for role in DATA['roles']:
        registry.add_rule(Rule('lithomancy.role.'+role['role_id'],1,34,'Symbolic gem sets',PROFILE,
            DATA['source']['id'],role['locator'],role['association'],'lithomancy_source_association',
            dict(role_id=role['role_id']),'proposed','traditional',[]))
    for kind in ('personal_stone','reader'):
        registry.add_rule(Rule('lithomancy.priority.'+kind,1,34,'Positional readings',PROFILE,
            DATA['source']['id'],DATA['priority_locator'],'Nearest objects receive reading priority; distant objects may still matter',
            'lithomancy_nearest_priority',dict(anchor=kind),'proposed','traditional',[]))


def read(value,registry=None):
    q=validate(value)
    if registry is not None:register_knowledge(registry)
    byid={s['id']:s for s in q['stones']};points={s['id']:point(s.get('position')) for s in q['stones']}
    anchor=q.get('anchor');selected=None;anchor_position=None
    if anchor is not None:
        if anchor['kind']=='personal_stone':selected=anchor['stone_id'];anchor_position=points[selected]
        else:anchor_position=anchor['position']
    eligible={i:p for i,p in points.items() if i!=selected}
    spatial=geometry(eligible,anchor_position,q['frame'])
    checks=_relation_checks(q,points)
    uncertain=bool(q.get('uncertainty') or any(s.get('uncertainty') for s in q['stones']))
    conflicts=any(c['status']=='conflicting_evidence' for c in checks)
    if not spatial['ordered_distance_groups']:status='insufficient_evidence'
    elif conflicts:status='conflicting_evidence'
    elif uncertain:status='uncertain_evidence'
    elif spatial['unknown_positions']:status='partial_evidence'
    else:status='applicable'
    issues=[]
    if anchor is None:issues.append('No anchor selected; reader position and personal stone are never inferred.')
    elif anchor_position is None:issues.append('Selected anchor position is unknown.')
    if not eligible:issues.append('No non-anchor objects eligible for comparison.')
    if spatial['unknown_positions']:issues.append('Unknown eligible positions may change the nearest/farthest result; priority is among known positions only.')
    if uncertain:issues.append('Reported uncertainty qualifies the interpretation; no confidence score inferred.')
    if conflicts:issues.append('Declared qualitative relations conflict with supplied coordinates; neither is silently rewritten.')
    if len(spatial['nearest_known'])>1:issues.append('Nearest known objects tie; no unique interpretive winner established.')
    def meanings(ids):
        return [dict(id=i,role_id=byid[i]['role_id'],source_association=thaw(ROLES[byid[i]['role_id']])) for i in ids]
    pairs=[dict(ids=[a,b],distance_squared=distance_squared(points[a],points[b])) for j,a in enumerate(points) for b in list(points)[j+1:]]
    return dict(schema_version=1,technique_id=34,profile=PROFILE,source=thaw(DATA['source']),
        author_identity=thaw(DATA['author_identity']),reading_id=q['reading_id'],task=q['task'],mode='manual',origin=q.get('origin','unknown'),
        set_coverage=dict(declared=q['coverage'],kind=DATA['source_policy']['set_kind'],present_roles=[s['role_id'] for s in q['stones']],
            missing_roles=[r for r in ROLES if r not in {s['role_id'] for s in q['stones']}],total_catalog_roles=12,generated_missing_objects=False),
        source_policy=thaw(DATA['source_policy']),frame=dict(name=q['frame'],contract=thaw(DATA['spatial_contract'])),
        placements=[dict(declaration=copy.deepcopy(s),source_role=thaw(ROLES[s['role_id']]),position_known=points[s['id']] is not None) for s in q['stones']],
        anchor=dict(declaration=copy.deepcopy(anchor),position=copy.deepcopy(anchor_position),excluded_instance_id=selected,
                    source_locator=DATA['priority_locator'],selection='Explicit user designation only; source example self-marker is Lodestone, not an automatic anchor.'),
        spatial=spatial,pairwise_distances=pairs,coincident_centers=[p['ids'] for p in pairs if p['distance_squared']==0],
        source_priority=dict(status=status,scope='all_eligible' if status=='applicable' else 'known_positions_only' if spatial['nearest_known'] else 'unavailable',
            nearest_known=meanings(spatial['nearest_known']),ordered_groups=[dict(**group,source_meanings=meanings(group['ids'])) for group in spatial['ordered_distance_groups']],
            source_id=DATA['source']['id'],locator=DATA['priority_locator'],
            qualification='Read nearest known objects first under the source guidance, retaining all ties and unknown qualifications. Numeric ordering is editorial geometry, not a validated future outcome. Distant objects are not automatically discarded.'),
        declared_groups=[dict(declaration=copy.deepcopy(group),source_meanings=meanings(group['members']),interpretation='User-declared grouping; combined outcome unsupported.') for group in q.get('groups',[])],
        declared_relation_checks=checks,user_text={k:q[k] for k in ('question','intention','commentary') if k in q},issues=issues,
        editorial_synthesis=dict(priority_ids=spatial['nearest_known'],unresolved=issues,combined_fortune=None,
            statement='Source associations are retrieved for the exact proximity groups. Group membership, distance and direction add no new symbolic meaning.'),
        provenance_matrix=dict(direct='Howard web example identities, concise associations and nearest-first guidance',compositional='Exact squared distances, descriptive directions, ties and user-selected group comparisons under editorial conventions',user_attributed='Raw placements, selected anchor, question, personal associations, qualitative relations and uncertainty',unsupported='Objective prediction, diagnosis, hidden knowledge, spirit/personality inference or universal lithomancy certification'),
        limitations=thaw(DATA['unsupported']),qualification='Source-specific symbolic comparison only; exact geometry does not establish divinatory accuracy.',
        replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,source_sha256=DATA['source']['snapshot_sha256'],
            serialization='SHA256 canonical UTF8 sorted-key compact JSON, unescaped Unicode, no terminal LF; raw field whitespace preserved',external_calls=False,rng=False,generated_placements=False))


def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2);fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Lithomancy source-specific stone reading','',html.escape(result['qualification']),'',f'Profile: {PROFILE}',
        '', '## Relative proximity','', '| Stone ID | Squared distance | Direction |','| --- | --- | --- |']
    for row in result['spatial']['distances']:
        lines.append(f'| {row["id"]} | {row["distance_squared"] if row["distance_squared"] is not None else "unknown"} | {row["direction"]} |')
    for title,key in [('Source and rights','source'),('Author witness','author_identity'),('Example-set coverage','set_coverage'),
        ('Source guidance and exceptions','source_policy'),('Coordinate convention','frame'),('Original placements and source roles','placements'),
        ('Selected anchor','anchor'),('Exact spatial comparison','spatial'),('Pairwise distances','pairwise_distances'),('Coincident centers','coincident_centers'),
        ('Source-linked reading priority','source_priority'),('User-declared groups','declared_groups'),('User-declared relation checks','declared_relation_checks'),
        ('Raw user text','user_text'),('Unknown and conflicting evidence','issues'),('Editorial synthesis','editorial_synthesis'),
        ('Evidence layers','provenance_matrix'),('Unsupported coverage','limitations'),('Exact replay metadata','replay')]:
        lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'


def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),lithomancy_report=None),indent=2)
    return '# Lithomancy request rejected\n\n'+html.escape(str(message))+'\n'
