"""Exact integer-tenth classification of a named24-mountain source table."""
import copy
import html
import itertools
import json
import re
from pathlib import Path
from .knowledge import Rule
from .scrying import freeze,digest,_object,_optional_text,load_input

ROOT=Path(__file__).resolve().parents[1]
PROFILE='yap2024-manual-24-mountain-tenths-v1'
PROFILE_HASH='ebdebdce355ed61aa2a1f14e6993f928e0baf0302ae21e79947461fc4e85323b'
DATA=freeze(load_input(ROOT/'knowledge/feng_shui_profile_v1.json'))
CATALOG_HASH=DATA['catalog_sha256']
READING_FIELDS=['reading_id','bearing_tenths','north_reference','bearing_role','uncertainty_tenths','alternate_readings','declared_facing_tenths','declared_sitting_tenths','building_id','contradictory_assertions','raw_observation','reflection']

def assets():
    p=load_input(ROOT/'knowledge/feng_shui_profile_v1.json');c=load_input(ROOT/'knowledge/feng_shui_catalog_v1.json')
    if digest(p)!=PROFILE_HASH or digest(c)!=CATALOG_HASH:raise ValueError('Pinned Feng Shui profile/catalog integrity mismatch')
    if digest(c['sources'])!=p['source_manifest_sha256']:raise ValueError('Pinned source manifest mismatch')
    return p,c

def integrity():
    p,c=assets()
    return dict(verified=True,profile_sha256=PROFILE_HASH,catalog_sha256=CATALOG_HASH,source_manifest_sha256=p['source_manifest_sha256'],rows=len(c['rows']))

def _integer(value,maximum,label):
    if type(value) is not int or not 0<=value<=maximum:raise ValueError(label+' must be an exact integer0..'+str(maximum)+';no rounding or input normalization')
    return value

def _identifier(value):return isinstance(value,str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',value) is not None

def _lookup(identifier,rows):
    if not isinstance(identifier,str):raise ValueError('Exact mountain ID or source label required')
    found=[r for r in rows if identifier in (r['id'],r['source_name'],r['chinese'],r['source_label'])]
    if len(found)!=1:raise ValueError('Unknown or ambiguous source mountain reference')
    r=copy.deepcopy(found[0]);i=rows.index(found[0]);r['previous_id']=rows[(i-1)%24]['id'];r['next_id']=rows[(i+1)%24]['id']
    return r

def lookup(identifier):return _lookup(identifier,assets()[1]['rows'])

def _reading(o,require_id=False):
    _object(o,READING_FIELDS)
    _integer(o.get('bearing_tenths'),3599,'bearing_tenths')
    _integer(o.get('uncertainty_tenths',0),1800,'uncertainty_tenths')
    if require_id or 'reading_id' in o:
        if not _identifier(o.get('reading_id')):raise ValueError('Bounded ASCII reading_id required')
    for key,domain in [('north_reference',DATA['north_references']),('bearing_role',DATA['bearing_roles'])]:
        if key in o and (not isinstance(o[key],str) or o[key] not in domain):raise ValueError('Unsupported '+key)
    for key in ('declared_facing_tenths','declared_sitting_tenths'):
        if key in o:_integer(o[key],3599,key)
    if 'building_id' in o and not _identifier(o['building_id']):raise ValueError('Bounded ASCII building_id required')
    for key in ('raw_observation','reflection'):_optional_text(o,key,10000)
    alternatives=o.get('alternate_readings',[])
    if not isinstance(alternatives,list) or len(alternatives)>12:raise ValueError('Up to12 alternate readings required')
    for x in alternatives:_integer(x,3599,'alternate reading')
    if len(alternatives)!=len(set(alternatives)):raise ValueError('Duplicate alternate readings rejected')
    assertions=o.get('contradictory_assertions',{})
    _object(assertions,['north_reference','bearing_role','bearing_tenths'])
    for key,values in assertions.items():
        if not isinstance(values,list) or not 1<=len(values)<=12:raise ValueError('Bounded nonempty assertion list required')
        for x in values:
            if key=='bearing_tenths':_integer(x,3599,'asserted bearing')
            elif not isinstance(x,str) or x not in DATA['north_references' if key=='north_reference' else 'bearing_roles']:raise ValueError('Unsupported asserted '+key)

def validate(value):
    if not isinstance(value,dict):raise ValueError('Expected request object')
    task=value.get('task')
    selector=READING_FIELDS if task=='classify' else ['readings'] if task=='compare' else ['reference_ids'] if task=='reference' else []
    common=['schema_version','profile','catalog_id','catalog_version','catalog_sha256','mode','task','question','notes']
    # Root reflection is available for every task;classify also preserves it as a reading declaration.
    _object(value,common+['reflection']+selector)
    if type(value.get('schema_version')) is not int or value['schema_version']!=1 or value.get('profile')!=PROFILE or value.get('mode')!='manual':raise ValueError('Exact profile,manual mode and integer schema_version1 required')
    if value.get('catalog_id')!=DATA['catalog_id'] or type(value.get('catalog_version')) is not int or value['catalog_version']!=1 or value.get('catalog_sha256')!=CATALOG_HASH:raise ValueError('Exact catalog ID,integer version1 and pinned hash required')
    if task not in DATA['tasks']:raise ValueError('Supported tasks:classify,reference,compare,catalog;other schools and outcome prediction unsupported')
    for k in ('question','notes','reflection'):_optional_text(value,k,10000)
    if task=='classify':_reading({k:value[k] for k in READING_FIELDS if k in value})
    elif task=='compare':
        rows=value.get('readings')
        if not isinstance(rows,list) or not 2<=len(rows)<=8:raise ValueError('Two to8 separately declared readings required')
        ids=[]
        for o in rows:_reading(o,True);ids.append(o['reading_id'])
        if len(ids)!=len(set(ids)):raise ValueError('Duplicate reading IDs rejected')
    elif task=='reference':
        ids=value.get('reference_ids')
        if not isinstance(ids,list) or not 1<=len(ids)<=24:raise ValueError('One to24 exact mountain references required')
        found=[lookup(x)['id'] for x in ids]
        if len(found)!=len(set(found)):raise ValueError('Duplicate mountain references or aliases rejected')
    return copy.deepcopy(value)

def _classify(heading,rows):
    # Literal source-interval scan is independent of the fixture's quotient oracle.
    matches=[r for r in rows if (r['lower_tenths']<=heading<=r['upper_tenths'] if not r['wraps_north'] else heading>=r['lower_tenths'] or heading<=r['upper_tenths'])]
    if len(matches)!=1:raise ValueError('Source catalog does not classify exactly once')
    return matches[0]

def classify(heading):
    _integer(heading,3599,'bearing_tenths')
    return copy.deepcopy(_classify(heading,assets()[1]['rows']))

def _evaluate(o,p,rows):
    heading=o['bearing_tenths'];radius=o.get('uncertainty_tenths',0)
    frame=o.get('north_reference','unknown');role=o.get('bearing_role','unknown')
    assertions=o.get('contradictory_assertions',{});conflicts=[]
    for key,values in assertions.items():
        known=set(values+[o.get(key,'unknown')])-{'unknown'}
        if len(known)>1:conflicts.append(key)
    facing=o.get('declared_facing_tenths');sitting=o.get('declared_sitting_tenths')
    if facing is not None and sitting is not None and (facing-sitting)%3600!=1800:conflicts.append('independent_facing_sitting_not_opposite')
    if role=='building_facing' and facing is not None and heading!=facing:conflicts.append('primary_vs_declared_facing')
    if role=='building_sitting' and sitting is not None and heading!=sitting:conflicts.append('primary_vs_declared_sitting')
    candidates=list(dict.fromkeys([heading]+o.get('alternate_readings',[])+assertions.get('bearing_tenths',[])))
    points=set();windows=[]
    for center in candidates:
        window={(center+d)%3600 for d in range(-radius,radius+1)};points.update(window)
        ids={_classify(h,rows)['id'] for h in window}
        windows.append(dict(center_tenths=center,lower_unwrapped_tenths=center-radius,upper_unwrapped_tenths=center+radius,point_count=len(window),possible_ids=[r['id'] for r in rows if r['id'] in ids],wraps_north=center-radius<0 or center+radius>=3600))
    counts={r['id']:0 for r in rows}
    for h in points:counts[_classify(h,rows)['id']]+=1
    possible=[copy.deepcopy(r) for r in rows if counts[r['id']]]
    unique=len(possible)==1
    issues=[]
    if frame=='unknown':issues.append('North reference missing or explicitly unknown')
    if role=='unknown':issues.append('Heading role missing or explicitly unknown')
    if frame=='source_diagram' and role not in ('source_heading','unknown'):issues.append('Source-diagram heading does not establish a physical role')
    if frame in ('magnetic','true'):issues.append('Declared physical north reference is not converted or calibrated against the source diagram')
    context='conflicting_evidence' if conflicts else 'insufficient_evidence' if frame=='unknown' or role=='unknown' else 'source_diagram' if frame=='source_diagram' and role=='source_heading' else 'unsupported_physical_frame' if frame=='source_diagram' else 'declared_only_no_conversion'
    return dict(reading_id=o.get('reading_id','heading'),declared=copy.deepcopy(o),bearing_tenths=heading,bearing_degrees_display=f'{heading//10}.{heading%10}',north_reference=frame,bearing_role=role,center_mountain=copy.deepcopy(_classify(heading,rows)),
        status='conflicting_evidence' if conflicts else 'classified' if unique else 'ambiguous',classification_unique=unique,definitive_id=possible[0]['id'] if unique and not conflicts else None,
        possible_mountain_ids=[r['id'] for r in possible],possible_mountains=possible,discrete_heading_count=len(points),heading_counts_by_mountain={i:n for i,n in counts.items() if n},
        uncertainty_tenths=radius,uncertainty_windows=windows,uncertainty_crosses_boundary=any(len(w['possible_ids'])>1 for w in windows),wraps_north=any(w['wraps_north'] for w in windows),candidate_readings_disagree=len({_classify(x,rows)['id'] for x in candidates})>1,
        structured_conflicts=conflicts,context_status=context,frame_issues=issues,precision_policy=p['numeric_policy'],match_explanation='Exact integer-tenth membership in inclusive printed intervals;N2 crosses0. No input rounding or normalization.',
        independent_declarations=dict(facing_tenths=facing,sitting_tenths=sitting,generated_opposite=None),physical_building_conclusion_supported=False,declination_conversion=None,measured_qi=None,outcome_prediction=None)

def register_knowledge(registry):
    _,c=assets()
    for s in c['sources']:registry.add_source(s)
    for r in c['rows']:
        registry.add_rule(Rule('feng-shui.'+r['id'],1,40,'Compass / Luo Pan',PROFILE,r['source_id'],r['source_locator'],'Exact source interval membership for '+r['source_label'],'integer_tenth_interval_membership',dict(lower=r['lower_tenths'],upper=r['upper_tenths'],wrap=r['wraps_north']),'verified','computational',['tests/fixtures/feng_shui_reference_v1.json:expected_by_heading']))

def read(value,registry=None):
    p,c=assets();q=validate(value)
    if registry is not None:register_knowledge(registry)
    declarations=[{k:q[k] for k in READING_FIELDS if k in q}] if q['task']=='classify' else q.get('readings',[])
    readings=[_evaluate(o,p,c['rows']) for o in declarations]
    references=[_lookup(x,c['rows']) for x in q['reference_ids']] if q['task']=='reference' else [_lookup(r['id'],c['rows']) for r in c['rows']] if q['task']=='catalog' else []
    comparisons=[]
    for a,b in itertools.combinations(readings,2):
        same_frame=a['north_reference']==b['north_reference'] and a['north_reference']!='unknown' and not a['structured_conflicts'] and not b['structured_conflicts']
        same_building=bool(a['declared'].get('building_id')) and a['declared'].get('building_id')==b['declared'].get('building_id')
        comparisons.append(dict(reading_ids=[a['reading_id'],b['reading_id']],roles=[a['bearing_role'],b['bearing_role']],north_references=[a['north_reference'],b['north_reference']],possible_ids=[a['possible_mountain_ids'],b['possible_mountain_ids']],same_declared_building=same_building,clockwise_delta_tenths=(b['bearing_tenths']-a['bearing_tenths'])%3600 if same_frame else None,centers_opposite=(b['bearing_tenths']-a['bearing_tenths'])%3600==1800 if same_frame else None,qualification='Editorial numerical comparison only;no shared physical building inferred without matching explicit building_id',combined_outcome=None))
    return dict(schema_version=1,technique_id=40,profile=PROFILE,catalog_id=p['catalog_id'],catalog_version=1,mode='manual',task=q['task'],sources=c['sources'],readings=readings,references=references,comparisons=comparisons,numeric_policy=p['numeric_policy'],frame_policy=p['frame_policy'],conflict_policy=p['conflict_policy'],comparison_policy=p['comparison_policy'],source_conventions=c['source_conventions'],
        user_text={k:q[k] for k in ('question','notes','reflection') if k in q},evidence_matrix=dict(direct='Source-located factual names and printed degree intervals',user_attributed='Manual bearings,north/role/building declarations,uncertainty and raw text',editorial='Exact discrete interval scan,uncertainty enumeration,conflict handling and comparison',unsupported='MeasuredQi,physical compass calibration,health/wealth/prosperity,safety or interpersonal outcome claims'),
        variation_matrix=dict(supported=p['supported'],experimental=p['experimental'],unsupported=p['unsupported']),qualification=p['qualification'],rights=p['rights'],
        replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,catalog_sha256=CATALOG_HASH,source_manifest_sha256=p['source_manifest_sha256'],source_snapshot_sha256={s['id']:s['snapshot_sha256'] for s in c['sources']},serialization='Canonical sorted-key compact UTF8 JSON,unescapedUnicode,no terminalLF;raw user text preserved',external_calls=False,rng=False,integrity_checked=True))

def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2);fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Feng Shui:24 Mountains source reference','',result['qualification'],'','Profile: '+PROFILE]
    for r in result['readings']:
        labels=', '.join(x['id']+' / '+x['source_label'] for x in r['possible_mountains'])
        lines+=['',f'## {r["reading_id"]}: {r["bearing_degrees_display"]}° — {r["status"]}','','Possible mountains: '+labels,'','North reference: '+r['north_reference']+';role: '+r['bearing_role']+'.', '',block(dict(center_mountain=r['center_mountain'],possible_mountain_ids=r['possible_mountain_ids'],classification_unique=r['classification_unique'],definitive_id=r['definitive_id'],context_status=r['context_status'],frame_issues=r['frame_issues']))]
    for title,key in [('Source identity and rights','sources'),('Complete declared readings and numeric evaluation','readings'),('Selected source references and neighbors','references'),('Side-by-side numerical comparisons','comparisons'),('Discrete precision and uncertainty','numeric_policy'),('Frame policy','frame_policy'),('Conflict policy','conflict_policy'),('Comparison policy','comparison_policy'),('Source conventions','source_conventions'),('Raw user text','user_text'),('Evidence layers','evidence_matrix'),('Variation support','variation_matrix'),('Rights review','rights'),('Exact replay metadata','replay')]:lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'

def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),feng_shui_report=None),indent=2)
    return '# Feng Shui request rejected\n\n'+html.escape(str(message))+'\n'
