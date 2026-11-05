"""Source-bounded Shang translated-charge references; no casting or prophecy."""
import copy,html,itertools,json,re
from pathlib import Path
from types import MappingProxyType
from urllib.parse import quote
from .knowledge import Rule
from .scrying import freeze,thaw,digest,_object,_optional_text,load_input

ROOT=Path(__file__).resolve().parents[1]
DATA=freeze(json.loads((ROOT/'knowledge/osteomancy_profile_v1.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile'];PROFILE_HASH=digest(thaw(DATA))
CASES=MappingProxyType({c['case_id']:c for c in DATA['cases']})
ORDER=tuple(CASES);INDEX=MappingProxyType({i:n for n,i in enumerate(ORDER)})
RELATIONSHIPS=MappingProxyType({frozenset(r['pair']):r for r in DATA['relationships']})
PRESENT='present_in_inspected_excerpt';UNCERTAIN='explicitly_uncertain_in_source'


def lookup(case_id):
    if not isinstance(case_id,str) or case_id not in CASES:raise ValueError('Unknown exact AFE case ID')
    result=thaw(CASES[case_id])
    result['source_deep_link']=DATA['source']['url']+'#:~:text='+quote(case_id+'.',safe='')
    return result


def _selection(q):
    if q['task']=='group':return list(DATA['groups'][q['group']])
    if q['task']=='topic':return [c for c in ORDER if q['topic'] in CASES[c]['editorial_topics']]
    return q['case_ids'].copy()


def validate(value):
    _object(value,['schema_version','profile','mode','task','case_ids','group','topic','research_id','notes','research_question','annotations'])
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE or value.get('mode')!='documentary':raise ValueError('Exact AFE documentary profile and documentary mode required')
    task=value.get('task');selectors=set(value)&{'case_ids','group','topic'}
    if task in ('reference','compare'):
        if selectors!={'case_ids'}:raise ValueError('Reference/compare requires case_ids only; selectors cannot be mixed')
        ids=value['case_ids'];minimum=2 if task=='compare' else 1
        if not isinstance(ids,list) or not minimum<=len(ids)<=13:raise ValueError(f'{task} requires {minimum}–13 ordered exact case IDs')
        for i in ids:lookup(i)
        if len(set(ids))!=len(ids):raise ValueError('Duplicate selected case IDs rejected')
    elif task=='group':
        if selectors!={'group'} or not isinstance(value['group'],str) or value['group'] not in DATA['groups']:raise ValueError('Exact supported group required without other selectors')
    elif task=='topic':
        if selectors!={'topic'} or not isinstance(value['topic'],str) or value['topic'] not in DATA['topics']:raise ValueError('Exact editorial topic required without other selectors')
    else:raise ValueError('Supported documentary tasks: reference, compare, group, topic; modern tosses and crack classification unsupported')
    if 'research_id' in value and (not isinstance(value['research_id'],str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',value['research_id'])):raise ValueError('Bounded plain research_id required')
    for k in ('notes','research_question'):_optional_text(value,k,10000)
    annotations=value.get('annotations',[])
    if not isinstance(annotations,list) or len(annotations)>13:raise ValueError('At most13 user annotations allowed')
    selected=set(_selection(value));seen=set()
    for a in annotations:
        _object(a,['case_id','note','association'])
        identifier=a.get('case_id');lookup(identifier)
        if identifier not in selected or identifier in seen:raise ValueError('Annotations require distinct selected case IDs')
        seen.add(identifier)
        if not set(a)&{'note','association'}:raise ValueError('Annotation requires a user note or association')
        for k in ('note','association'):_optional_text(a,k,10000)
    return copy.deepcopy(value)


def compare(a,b):
    lookup(a);lookup(b)
    ids=sorted([a,b],key=INDEX.__getitem__);left,right=[CASES[i] for i in ids]
    if a==b:
        relationship=dict(pair=ids,classification='same_record',opposition='not_applicable',scope='Same exact source label, not a second independent inscription.')
    elif frozenset(ids) in RELATIONSHIPS:
        relationship=thaw(RELATIONSHIPS[frozenset(ids)])
    else:
        relationship=dict(pair=ids,classification='relationship_unresolved',opposition='not_independently_verified',scope='No independently frozen relationship for this pair; shared tags or A/B labels do not establish opposition.')
    fields={}
    for name in DATA['comparison_components']:
        x,y=left['components'][name],right['components'][name]
        if UNCERTAIN in (x['status'],y['status']):status='incomparable_uncertainty'
        elif x['status']!=PRESENT or y['status']!=PRESENT:status='incomparable_missing_evidence'
        else:status='shared_source_value' if x['value']==y['value'] else 'different_source_values'
        fields[name]=dict(status=status,left=thaw(x),right=thaw(y))
    return dict(requested_order=[a,b],canonical_case_ids=ids,relationship=relationship,component_comparison=fields,
        editorial_index_comparison=dict(shared_topics=[t for t in DATA['topics'] if t in left['editorial_topics'] and t in right['editorial_topics']],
            predicates=[left['charge_formulation']['predicate'],right['charge_formulation']['predicate']],
            polarities=[left['charge_formulation']['polarity'],right['charge_formulation']['polarity']],policy=DATA['index_policy']),
        uncertainty_by_case={i:thaw(CASES[i]['translation_qualifications']) for i in dict.fromkeys(ids)},
        original_artifact_relationship='not_independently_verified; labels are excerpt identifiers, not artifact IDs',
        qualification='Source-attributed charges and editorial comparisons; no prognostication or actual outcome inferred.')


def register_knowledge(registry):
    registry.add_source(thaw(DATA['source']))
    for c in DATA['cases']:
        registry.add_rule(Rule('osteomancy.case.'+c['case_id'],1,35,'Shang oracle bones',PROFILE,DATA['source']['id'],c['locator'],
            c['components']['charge']['value'],'osteomancy_documentary_reference',dict(case_id=c['case_id']),'proposed','traditional',[]))
    for r in DATA['relationships']:
        registry.add_rule(Rule('osteomancy.relationship.'+r['group'],1,35,'Shang oracle bones',PROFILE,DATA['source']['id'],r['locator'],
            r['scope'],'osteomancy_source_comparison',dict(pair=thaw(r['pair']),classification=r['classification']),'proposed','traditional',[]))


def read(value,registry=None):
    q=validate(value)
    if registry is not None:register_knowledge(registry)
    ids=_selection(q)
    comparisons=[compare(a,b) for a,b in itertools.combinations(ids,2)] if q['task'] in ('compare','group') else []
    records=[lookup(i) for i in ids]
    return dict(schema_version=1,technique_id=35,profile=PROFILE,mode='documentary',task=q['task'],selected_case_ids=ids,
        source=thaw(DATA['source']),source_context=DATA['source_context'],records=records,comparisons=comparisons,
        structure_summary={k:{state:sum(c['components'][k]['status']==state for c in records) for state in DATA['evidence_states']} for k in DATA['comparison_components']},
        evidence_states=thaw(DATA['evidence_states']),comparison_policy=DATA['comparison_policy'],
        available_groups=thaw(DATA['groups']),editorial_topics=thaw(DATA['topics']),
        user_annotations=copy.deepcopy(q.get('annotations',[])),user_text={k:q[k] for k in ('research_id','notes','research_question') if k in q},
        chronological_boundary=dict(absolute_date=None,calendar_conversion=False,policy='Partial source day/moon labels retained. No date inheritance or Gregorian conversion; indices49/50 alone do not establish an absolute elapsed interval.'),
        provenance_matrix=dict(direct='Independently checked source-record facts and exact attribution/locators; short original factual annotations, not copied translations',editorial='Typed structural/topic indexing and only independently frozen pair relationships',user_attributed='Raw user research questions, notes and associations; never replacements for historical evidence',unsupported='Generated archaeological evidence, original-text decipherment, modern casting, spirit contact, future prediction or supernatural accuracy'),
        limitations=thaw(DATA['unsupported']),qualification='Historical translated-charge reference only. A charge is not evidence that its proposition occurred; excerpt omission is not original-inscription absence.',
        replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,source_sha256=DATA['source']['snapshot_sha256'],
            serialization='SHA256 canonical UTF8 sorted-key compact JSON, unescaped Unicode, no terminal LF; raw user whitespace preserved',external_calls=False,rng=False,generated_historical_records=False))


def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2);fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Osteomancy: Shang inscription reference and comparison','',html.escape(result['qualification']),
        '',f'Profile: {PROFILE}','','## Selected source records','','| Label | Factual annotation | Source |','| --- | --- | --- |']
    for c in result['records']:lines.append(f'| {c["label"]} | {c["components"]["charge"]["value"]} | [AFE label {c["label"]}]({c["source_deep_link"]}) |')
    for title,key in [('Source attribution and rights','source'),('Historical source context','source_context'),('Typed source records','records'),
        ('Structured comparisons','comparisons'),('Component availability','structure_summary'),('Evidence-state definitions','evidence_states'),
        ('Comparison limits','comparison_policy'),('Verified groups','available_groups'),('Editorial topic index','editorial_topics'),
        ('Raw user annotations','user_annotations'),('Raw research notes','user_text'),('Partial-date boundary','chronological_boundary'),
        ('Evidence layers','provenance_matrix'),('Unsupported coverage','limitations'),('Exact replay metadata','replay')]:
        lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'


def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),osteomancy_report=None),indent=2)
    return '# Osteomancy request rejected\n\n'+html.escape(str(message))+'\n'
