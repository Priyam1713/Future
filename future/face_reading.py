"""Historical reference lookup and descriptive annotation; no appearance-to-trait inference."""
import copy
import hashlib
import json
import math
import re
from pathlib import Path
from .knowledge import Rule

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'knowledge/face_reading_lavater_v1.json').read_text(encoding='utf-8'))
PROFILE=DATA['profile']
UNKNOWN=('unknown','uncertain')
GEOMETRY=dict(outline=['straight','convex','concave','mixed'],relative_base=['narrow','intermediate','broad'],
              state=['at_rest','moving'])
LIMITS=[
    'Historical/symbolic reference only. Physiognomic claims about character or ability are discredited.',
    'No individual intelligence,honesty,morality,criminality,personality,health,ethnicity,protected-trait or life-outcome assessment.',
    'Historical associations are selected by region only,never by observed geometry,markings,measurements or side.',
    'Normalized points and side labels are manual annotations; no image processing or anatomical landmark detection.',
    'Observer accuracy and source fidelity are different questions; schematic transcriptions do not validate real-person judgments.',
    'Chinese Mian Xiang,five elements and12 palaces remain unsupported and are not merged with Lavater.',
    'Only the inspected Hunter1789 Volume I pages/figures are covered; no Holcroft/other-volume substitution.']


def _obj(value,keys,path):
    if not isinstance(value,dict):raise ValueError(path+' must be an object')
    if set(value)-set(keys):raise ValueError(path+': unsupported fields '+','.join(sorted(set(value)-set(keys))))


def _enum(value,choices,path):
    if not isinstance(value,str) or value not in list(choices)+list(UNKNOWN):raise ValueError('Invalid '+path)


def validate(value):
    _obj(value,['schema_version','profile','task','mode','orientation','observations','example_id'],'input')
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE:raise ValueError('Unsupported source profile; no cross-tradition fallback')
    if value.get('task')!='historical_reference':raise ValueError('Only historical_reference is supported; individual inference requests are rejected')
    if value.get('mode') not in ('manual','source_example'):raise ValueError('mode must be manual or source_example')
    if value['mode']=='source_example':
        if set(value)&{'observations','orientation'}:raise ValueError('Source examples cannot be overridden with manual observations or orientation')
        if not isinstance(value.get('example_id'),str) or value['example_id'] not in DATA['source_examples']:
            raise ValueError('Unknown source example')
        return copy.deepcopy(value)
    if 'example_id' in value:raise ValueError('Use source_example mode for a published schematic')
    orientation=value.get('orientation')
    _obj(orientation,['view','side_frame','mirrored'],'orientation')
    _enum(orientation.get('view'),['frontal','left_profile','right_profile'],'orientation.view')
    if orientation.get('side_frame') not in ('subject','viewer'):raise ValueError('Explicit subject/viewer side_frame required')
    if not (type(orientation.get('mirrored')) is bool or orientation.get('mirrored') in UNKNOWN):
        raise ValueError('mirrored must be boolean or unknown/uncertain')
    rows=value.get('observations')
    if not isinstance(rows,list) or not 1<=len(rows)<=24:raise ValueError('Supply1-24 region observations')
    for r in rows:
        _obj(r,['region_id','side','visibility','geometry','markings','point'],'observation')
        if not isinstance(r.get('region_id'),str) or not re.fullmatch('[a-z][a-z_]{0,39}',r['region_id']):
            raise ValueError('region_id must be a lowercase identifier')
        _enum(r.get('side','unknown'),['left','right','both','midline'],'side')
        _enum(r.get('visibility','unknown'),['visible','occluded'],'visibility')
        if r['region_id'] in DATA['regions']:
            side=r.get('side','unknown');paired=DATA['regions'][r['region_id']]['paired']
            if (paired and side=='midline') or (not paired and side not in ('midline',*UNKNOWN)):
                raise ValueError('Region/side mismatch; central regions require midline,paired regions use left/right/both')
        g=r.get('geometry',{})
        _obj(g,GEOMETRY,'geometry')
        for k,v in g.items():_enum(v,GEOMETRY[k],'geometry.'+k)
        marks=r.get('markings',['unknown'])
        if not isinstance(marks,list) or not 1<=len(marks)<=4 or any(not isinstance(m,str) for m in marks):raise ValueError('Invalid markings list')
        if len(set(marks))!=len(marks):raise ValueError('Duplicate marking')
        for m in marks:_enum(m,['none','line','spot','crease'],'marking')
        if len(marks)>1 and any(m in ('none',*UNKNOWN) for m in marks):raise ValueError('None/unknown/uncertain markings cannot be combined with other markings')
        if 'point' in r:
            p=r['point']
            if isinstance(p,str) and p in UNKNOWN:continue
            if not isinstance(p,list) or len(p)!=2 or any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not 0<=x<=1 for x in p):
                raise ValueError('point needs two finite normalized coordinates[0,1],or unknown/uncertain')
    return copy.deepcopy(value)


def normalize(row,orientation):
    side=row.get('side','unknown');point=row.get('point','unknown');issues=[]
    view=orientation['view'];frame=orientation['side_frame'];mirrored=orientation['mirrored']
    canonical=side
    if frame=='viewer' and side in ('left','right'):
        if view!='frontal' or type(mirrored) is not bool:
            canonical='unknown';issues.append('Viewer side cannot be resolved without a known frontal mirroring convention.')
        elif not mirrored:canonical='right' if side=='left' else 'left'
    p=None
    if isinstance(point,list):
        if view=='frontal' and (frame=='subject' or type(mirrored) is bool):
            p=list(point)
            if frame=='viewer' and not mirrored:p[0]=1-p[0]
        else:issues.append('Point retained in input frame; profile/unknown projection is not converted into a frontal subject coordinate.')
    if view in ('unknown','uncertain'):issues.append('View is unknown; no visible-side assumption made.')
    return dict(canonical_subject_side=canonical,canonical_subject_point=p,ambiguities=issues)


def register_knowledge(registry):
    registry.add_source(DATA['source'])
    for key,r in DATA['regions'].items():
        registry.add_rule(Rule(r['rule_id'],r['version'],9,'historical region reference',PROFILE,r['source_id'],r['locator'],
            r['historical_association'],'historical_region_lookup',dict(region_id=key,individual_inference=False),
            'proposed','traditional',[]))
    for t in DATA['terms']:
        registry.add_rule(Rule(t['id'],t['version'],9,'historical terminology',PROFILE,DATA['source']['id'],t['locator'],
            t['description'],'historical_terminology',dict(term=t['term'],individual_inference=False),'proposed','traditional',[]))


def _known(x):
    return x is not None and not (isinstance(x,str) and x in UNKNOWN)


def _overlap(a,b):
    sides=dict(left={'left'},right={'right'},both={'left','right'},midline={'midline'},unknown=set(),uncertain=set())
    return bool(sides[a]&sides[b])


def reference(value,registry=None):
    value=validate(value)
    if registry is not None:register_knowledge(registry)
    example=None
    if value['mode']=='source_example':
        example=copy.deepcopy(DATA['source_examples'][value['example_id']])
        observations=[{k:copy.deepcopy(example[k]) for k in ('region_id','side','visibility','geometry')}]
        orientation=dict(view='schematic',side_frame='subject',mirrored=False)
    else:observations=value['observations'];orientation=value['orientation']
    rows=[];conflicts=[]
    for i,raw in enumerate(observations):
        normalized=normalize(raw,orientation)
        region=DATA['regions'].get(raw['region_id']);g=raw.get('geometry',{})
        if raw.get('visibility')=='occluded' and (any(_known(x) for x in g.values()) or isinstance(raw.get('point'),list) or raw.get('markings',['unknown']) not in (['unknown'],['uncertain'])):
            conflicts.append(dict(indices=[i],reason='Occluded region has confirmed geometry,point or marking observations.'))
        side=normalized['canonical_subject_side']
        if raw.get('visibility')=='visible' and orientation['view'] in ('left_profile','right_profile'):
            visible_side=orientation['view'].split('_')[0]
            if side in ('left','right','both') and side!=visible_side:
                conflicts.append(dict(indices=[i],reason='Visible paired region conflicts with declared anatomical profile view.'))
        rows.append(dict(index=i,region_id=raw['region_id'],observation=copy.deepcopy(raw),**normalized,
            region_definition=region['region_description'] if region else None,
            historical_reference=copy.deepcopy(region),
            rule_trace=dict(rule_id=region['rule_id'] if region else None,version=region['version'] if region else None,
                lookup_key=raw['region_id'],method='region_reference_only',geometry_used_for_association=False,
                source_id=region['source_id'] if region else None,locator=region['locator'] if region else None),
            coverage='unsupported_region' if region is None else 'historical_reference_available',
            observation_status='recorded',individual_assessment=None,association_applied_to_individual=False,
            unknown_fields=[k for k,v in [('side',raw.get('side','unknown')),('visibility',raw.get('visibility','unknown'))]+
                            [('geometry.'+k,g.get(k,'unknown')) for k in GEOMETRY] if not _known(v)]))
    for i,a in enumerate(rows):
        for j in range(i):
            b=rows[j]
            if a['region_id']!=b['region_id'] or not _overlap(a['canonical_subject_side'],b['canonical_subject_side']):continue
            av,bv=a['observation'],b['observation'];differ=[]
            for key in ('outline','relative_base','state'):
                x,y=av.get('geometry',{}).get(key),bv.get('geometry',{}).get(key)
                if _known(x) and _known(y) and x!=y:differ.append('geometry.'+key)
            if _known(av.get('visibility')) and _known(bv.get('visibility')) and av['visibility']!=bv['visibility']:differ.append('visibility')
            ma,mb=av.get('markings',['unknown']),bv.get('markings',['unknown'])
            if not any(m in UNKNOWN for m in ma+mb) and set(ma)!=set(mb):differ.append('markings')
            if differ:conflicts.append(dict(indices=[j,i],reason='Overlapping region annotations disagree on '+','.join(differ)))
            elif av==bv:a.setdefault('duplicate_of',j)
    for row in rows:
        affected=[c for c in conflicts if row['index'] in c['indices']]
        row['observation_conflicts']=affected
        row['observation_status']=('conflicting' if affected else 'ambiguous' if row['ambiguities'] else
            'partial' if row['unknown_fields'] else 'recorded')
    release=ROOT/'knowledge/face_reading_core_v1.json'
    return dict(technique_id=9,profile=PROFILE,tradition=DATA['tradition'],mode=value['mode'],task='historical_reference',
        release_status=json.loads(release.read_text())['status'] if release.exists() else 'Developing',
        input=value,orientation=orientation,orientation_convention=DATA['conventions']['orientation'],
        regions=rows,source_example=example,terminology=DATA['terms'],observation_conflicts=conflicts,
        missing_regions=[k for k in DATA['regions'] if k not in {r['region_id'] for r in rows}],
        tradition_ambiguities=['Chinese five-element/12-palace mappings are unverified and excluded.',
            'Hunter spelling/translation is preserved separately from Holcroft and other editions.'],
        summary=f"{len(rows)} annotations; {sum(r['historical_reference'] is not None for r in rows)} region-reference lookups; {len(conflicts)} observation conflicts; zero personal assessments.",
        individual_assessment=None,inference_enabled=False,source=DATA['source'],limits=LIMITS,
        reproducibility=dict(profile_version=1,input_sha256=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            source_profile_sha256=hashlib.sha256(json.dumps(DATA,sort_keys=True).encode()).hexdigest()))


def load_input(path):
    def unique(pairs):
        result={}
        for k,v in pairs:
            if k in result:raise ValueError('Duplicate JSON key: '+k)
            result[k]=v
        return result
    def reject(x):raise ValueError('Non-finite JSON constant '+x)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=unique,parse_constant=reject)


def markdown(r):
    out=['# Historical face-reading reference',r['release_status']+' | '+r['profile'],r['summary'],
        'Historical claims below describe Lavater\'s text. No observation is used to assess a person.',
        'Source: ['+r['source']['edition']+']('+r['source']['url']+')',
        '\n## Orientation',json.dumps(r['orientation']),r['orientation_convention']]
    if r['source_example']:
        e=r['source_example'];out.extend(['\n## Published schematic',e['label']+'; '+e['locator'],e['description'],e['historical_context'],
            'Original illustration: '+r['source']['manifest']+' (canvas339).'])
    for row in r['regions']:
        out.extend(['\n## '+row['region_id']+' — '+row['canonical_subject_side'],
            'Observation status: '+row['observation_status']+'; coverage: '+row['coverage'],
            '```json',json.dumps(row['observation'],indent=2),'```'])
        if row['canonical_subject_point'] is not None:out.append('Canonical subject point: '+json.dumps(row['canonical_subject_point']))
        ref=row['historical_reference']
        if ref:
            out.extend([ref['region_description'],'**Historical context, independent of the observed geometry:** '+ref['historical_association'],
                        f"Rule {ref['rule_id']} v{ref['version']}; {ref['locator']}; {ref['source_id']}.",ref['limitations']])
        else:out.append('No inspected regional reference; no substitute association supplied.')
        out.extend('- Ambiguity: '+x for x in row['ambiguities'])
        out.extend('- Conflict: '+x['reason']+' Observations retained without reconciliation.' for x in row['observation_conflicts'])
        if row['unknown_fields']:out.append('Unknown/uncertain: '+', '.join(row['unknown_fields']))
    out.extend(['\n## Historical terminology']+[t['term']+': '+t['description']+' ('+t['locator']+').' for t in r['terminology']])
    out.extend(['\n## Coverage and limits','Missing regions: '+(', '.join(r['missing_regions']) or 'none')]+['- '+x for x in r['limits']])
    return '\n'.join(out)+'\n'
