"""Bounded historical taxonomy and explicit contextual reference,never prediction."""
import copy
import html
import json
from pathlib import Path
import re
from .knowledge import Rule
from .scrying import freeze,thaw,digest,_object,_raw,_optional_text,_timestamp,load_input

ROOT=Path(__file__).resolve().parents[1]
DATA=freeze(json.loads((ROOT/'knowledge/dream_profile_v1.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile'];PROFILE_HASH=digest(thaw(DATA))
MOTIFS=DATA['motifs'];CATEGORIES=DATA['categories']
BOOL_CONTEXT=('hungry','thirsty','current_fear','current_desire','at_sea','exact_correspondence_reported')
LIST_FIELDS=('people','objects','places','events','feelings','associations')
RECALL=('complete','fragmented','uncertain','no_recall')


def _strings(value,limit=32,length=2000):
    return isinstance(value,list) and len(value)<=limit and all(_raw(x,length) for x in value)


def validate(value):
    _object(value,['schema_version','profile','task','mode','narrative','timestamp','recall','scenes',*LIST_FIELDS,
        'context','taxonomy_claims','lookups','annotations','preferences','personal_reflection'])
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE or value.get('task')!='historical_reflection' or value.get('mode')!='manual':
        raise ValueError('Exact Artemidorus profile,historical_reflection task andmanual mode required')
    _optional_text(value,'narrative',20000);_optional_text(value,'personal_reflection',10000);_timestamp(value.get('timestamp'))
    if 'recall' in value and value['recall'] not in RECALL:raise ValueError('Unknown declared recall state')
    for field in LIST_FIELDS:
        if field in value and not _strings(value[field]):raise ValueError('Use optional user-authored text lists for '+field)
    scenes=value.get('scenes',[])
    if not isinstance(scenes,list) or len(scenes)>64:raise ValueError('Scenes must be a list of up to64 records')
    last=0
    for row in scenes:
        _object(row,['description','timestamp','sequence','uncertainty','recall',*LIST_FIELDS])
        _optional_text(row,'description',10000);_timestamp(row.get('timestamp'))
        if 'sequence' in row:
            n=row['sequence']
            if type(n) is not int or not last<n<=1000000:raise ValueError('Scene sequences must strictly increase without sorting')
            last=n
        if 'uncertainty' in row and type(row['uncertainty']) is not bool:raise ValueError('Scene uncertainty must be boolean')
        if 'recall' in row and row['recall'] not in RECALL:raise ValueError('Unknown scene recall state')
        for field in LIST_FIELDS:
            if field in row and not _strings(row[field]):raise ValueError('Scene '+field+' must be a user-authored text list')
    context=value.get('context',{})
    _object(context,[*BOOL_CONTEXT,'circumstances','staff_cases','myth_versions','cultural_context','situational_context','notes'])
    for field in BOOL_CONTEXT:
        if field in context and context[field] is not None and type(context[field]) is not bool:raise ValueError('Context '+field+' must be boolean ornull')
    for field,allowed in [('circumstances',('perfume_trade','civic_standing','illness')),('staff_cases',('initial_account','repeat_during_paralysis'))]:
        if field in context:
            rows=context[field]
            if not isinstance(rows,list) or len(rows)>len(allowed) or any(not isinstance(x,str) or x not in allowed for x in rows) or len(set(rows))!=len(rows):raise ValueError('Unsupported orduplicate historical context selector: '+field)
    if 'myth_versions' in context and (not _strings(context['myth_versions'],8) or len(set(context['myth_versions']))!=len(context['myth_versions'])):raise ValueError('Myth versions must be distinct user-authored strings')
    for field in ('cultural_context','situational_context','notes'):_optional_text(context,field,2000)
    for field in ('taxonomy_claims','lookups'):
        rows=value.get(field,[])
        if not isinstance(rows,list) or len(rows)>32 or any(not _raw(x,80) or not x.strip() for x in rows) or len(set(rows))!=len(rows):raise ValueError('Use distinct plain identifiers for '+field)
        if field=='taxonomy_claims' and any(x not in CATEGORIES for x in rows):raise ValueError('Unknown historical taxonomy category')
    prefs=value.get('preferences',{});_object(prefs,['historical_references','editorial_questions'])
    if any(type(x) is not bool for x in prefs.values()):raise ValueError('Interpretation preferences must be boolean')
    if prefs.get('historical_references') is False and (value.get('lookups') or value.get('taxonomy_claims')):raise ValueError('Historical-reference opt-out conflicts withexplicit historical requests')
    annotations=value.get('annotations',[])
    if not isinstance(annotations,list) or len(annotations)>128:raise ValueError('Use up to128 manual motif annotations')
    seen=set()
    for row in annotations:
        _object(row,['motif_id','target','scene_index','start','end','decision'])
        motif=row.get('motif_id');target=row.get('target','narrative')
        if not isinstance(motif,str) or motif not in MOTIFS:raise ValueError('Unknown manual motif tag')
        if target not in ('narrative','scene') or row.get('decision','include') not in ('include','exclude'):raise ValueError('Unsupported annotation target/decision')
        if target=='scene':
            n=row.get('scene_index')
            if type(n) is not int or not 1<=n<=len(scenes):raise ValueError('Scene annotation index must reference an existing1-based scene')
            text=scenes[n-1].get('description')
        else:
            if 'scene_index' in row:raise ValueError('Narrative annotation cannot include a scene index')
            text=value.get('narrative')
        if ('start' in row)!=('end' in row):raise ValueError('Annotation start/end must be supplied together')
        if 'start' in row and (not isinstance(text,str) or type(row['start']) is not int or type(row['end']) is not int or not 0<=row['start']<row['end']<=len(text)):raise ValueError('Annotation spans are half-open Unicode code-point offsets into original text')
        key=(motif,target,row.get('scene_index'),row.get('start'),row.get('end'))
        if key in seen:raise ValueError('Duplicate/conflicting annotation rejected')
        seen.add(key)
    return copy.deepcopy(value)


def lookup(identifier,context):
    if identifier not in MOTIFS:return dict(motif_id=identifier,status='unsupported',selected_cases=[],missing_context=['verified source rule'],not_met=[],forecast=False)
    motif=thaw(MOTIFS[identifier]);kind=motif['condition_kind'];selected=[];missing=[];not_met=[]
    for case in motif['cases']:
        success=True
        for key,expected in case['requires'].items():
            actual=context.get(key)
            if actual is None or actual==[]:missing.append(key);success=False
            elif kind=='boolean' and actual is not expected:not_met.append(key);success=False
            elif kind in ('circumstances','staff_cases') and expected not in actual:success=False
            elif kind=='myth_versions' and len([v for v in actual if v.strip()])<expected:missing.append('at least2 nonblank myth_versions');success=False
        if success:selected.append(case)
    if kind=='polysemy':status='polysemous_reference'
    elif len(selected)>1:status='conflicting_references'
    elif selected:status='conditional_reference'
    elif missing:status='missing_context'
    else:status='conditions_not_met'
    keys={k for case in motif['cases'] for k in case['requires']}
    return dict(motif_id=identifier,status=status,reference=motif,selected_cases=selected,
        provided_context={k:copy.deepcopy(context[k]) for k in sorted(keys) if k in context},missing_context=sorted(set(missing)),not_met=sorted(set(not_met)),
        rule_id='dream.artemidorus.motif.'+identifier,interpretation_scope='Author-attributed historical reference only;not an event forecast ordiagnosis',forecast=False)


def taxonomy(claims,lookups,context):
    supported=set();evidence={}
    for result in lookups:
        if result['status']=='conditional_reference':
            for case in result['selected_cases']:
                if case.get('category'):
                    supported.add(case['category']);evidence.setdefault(case['category'],[]).append(result['motif_id'])
    chosen=set(claims);all_ids=chosen|supported
    if all_ids&{'theorematic','allegorical'}:all_ids.add('oneiros')
    conflicts=[]
    if 'enypnion' in all_ids and all_ids&{'oneiros','theorematic','allegorical'}:conflicts.append('present_state_and_future_signifying_lenses_for_same_record')
    if {'theorematic','allegorical'}<=all_ids:conflicts.append('direct_and_allegorical_lenses_for_same_record')
    results=[]
    for key,item in CATEGORIES.items():
        missing=[]
        if key=='enypnion' and key not in supported:missing=['explicit motif withdeclared present-state condition']
        if key=='theorematic' and context.get('exact_correspondence_reported') is not True:missing=['user-reported exact correspondence;not independently verified']
        if key=='allegorical' and key in chosen:missing=['independently verified referent;not supplied by a symbol dictionary']
        if key=='oneiros':missing=['predictive significance cannot be established by this application']
        status='conditional_historical_comparison' if key in supported else 'user_selected_lens' if key in chosen else 'parent_of_selected_branch' if key in all_ids else 'undetermined'
        results.append(dict(category=thaw(item),status=status,user_claimed=key in chosen,evidence_motifs=evidence.get(key,[]),missing_context=missing,
            rule_id='dream.artemidorus.category.'+key,predictive_validity_verified=False))
    return dict(coverage='historical_taxonomy_comparison',categories=results,conflicts=conflicts,certainty=None)


def register_knowledge(registry):
    registry.add_source(thaw(DATA['source']));registry.add_source(thaw(DATA['greek_source']))
    for group,items in [('category',CATEGORIES),('motif',MOTIFS)]:
        for key,item in items.items():
            p=item['provenance']
            registry.add_rule(Rule('dream.artemidorus.'+group+'.'+key,1,23,'Artemidorus omens',PROFILE,p['source_id'],p['locator'],
                item.get('definition','Historical reference'),'dream_historical_reference',dict(kind=group),'proposed','traditional',[]))
    for r in DATA['context_rules']:
        registry.add_rule(Rule(r['rule_id'],1,23,'Artemidorus omens',PROFILE,r['source_id'],r['locator'],r['statement'],'dream_context_reference',{},'proposed','traditional',[]))


def read(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    historical=request.get('preferences',{}).get('historical_references',True);context=request.get('context',{})
    lookups=[lookup(k,context) for k in request.get('lookups',[])] if historical else []
    comparison=taxonomy(request.get('taxonomy_claims',[]),lookups,context) if historical else None
    annotations=[]
    for row in request.get('annotations',[]):
        text=(request.get('narrative') if row.get('target','narrative')=='narrative' else request['scenes'][row['scene_index']-1].get('description'))
        annotations.append(dict(user_record=copy.deepcopy(row),coverage='user_selected_annotation',selected_text=text[row['start']:row['end']] if 'start' in row else None,
            decision=row.get('decision','include'),automatic_match=False,historical_lookup_triggered=False))
    record_fields=('narrative','timestamp','recall','scenes',*LIST_FIELDS,'context','personal_reflection')
    journal={k:copy.deepcopy(request[k]) for k in record_fields if k in request}
    narrative=request.get('narrative');state='missing' if 'narrative' not in request else 'null' if narrative is None else 'blank' if not narrative.strip() else 'text'
    counts={status:sum(x['status']==status for x in lookups) for status in ('conditional_reference','conflicting_references','polysemous_reference','missing_context','conditions_not_met','unsupported')}
    questions=[]
    if request.get('preferences',{}).get('editorial_questions',True):
        for r in lookups:
            if r['missing_context']:questions.append('If you choose,clarify '+', '.join(r['missing_context'])+' for the '+r['motif_id']+' reference;leaving it unknown is valid.')
            if r['status'] in ('conflicting_references','polysemous_reference'):questions.append('Which personal associations,if any,differ from the competing '+r['motif_id']+' accounts? No account is selected as fact.')
        questions+=['What meanings do you personally give your recorded details?','Which details remain uncertain or incomplete?']
    return dict(schema_version=1,technique_id=23,profile=PROFILE,task='historical_reflection',mode='manual',
        journal=dict(coverage='user_attributed',record=journal,narrative_state=state,scene_order='input list;never sorted'),
        annotations=annotations,annotation_policy=DATA['annotations'],historical_taxonomy=comparison,motif_references=lookups,
        context_guidance=thaw(DATA['context_rules']) if historical else [],
        summary=dict(coverage='neutral_editorial_comparison',scene_count=len(request.get('scenes',[])),reference_counts=counts,
            text=str(len(lookups))+' explicit historical lookups;'+str(counts['conditional_reference'])+' fit declared case conditions,'+str(counts['missing_context'])+' lack context. These are source comparisons,not forecasts. User associations remain separate.'),
        editorial_reflection=dict(coverage='modern_editorial',questions=questions),
        sources=[thaw(DATA['source']),thaw(DATA['greek_source'])],terminology=DATA['terminology'],
        limitations=list(DATA['limits']),unsupported=['Objective omen fulfilment','Mental-health diagnosis orrepressed-memory inference','Universal orcross-tradition symbolism'],
        replay=dict(request=request,profile=PROFILE,profile_sha256=PROFILE_HASH,source_snapshot_sha256=DATA['source']['snapshot_sha256'],
            policy='artemidorus-explicit-context-v1',annotations='manual-codepoint-spans-v1',clock_used=False,automatic_matching=False,external_calls=False),
        factual_prediction=False,diagnosis=False,hidden_memory_inferred=False,confidence_score=None)


def markdown(result):
    def safe(v):return html.escape(str(v)).replace('|','&#124;').replace('\n',' ')
    def block(v,language='text'):
        fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',v)),default=0));return [fence+language,v,fence]
    lines=['# Dream — historical andreflective interpretation','','Profile: '+result['profile'],'',
        'Historical accounts below are attributed references,not predictions ordiagnoses.','', '## Original user record','']
    lines+=block(json.dumps(result['journal'],indent=2),'json')
    record=result['journal']['record']
    if record.get('narrative') is not None:lines+=['','Verbatim narrative:','']+block(record['narrative'])
    for n,scene in enumerate(record.get('scenes',[]),1):
        if scene.get('description') is not None:lines+=['','Scene '+str(n)+' verbatim:','']+block(scene['description'])
    lines+=['','## Historical taxonomy','',safe(result['terminology'])]
    if result['historical_taxonomy']:
        for row in result['historical_taxonomy']['categories']:
            c=row['category'];p=c['provenance']
            lines+=['','- '+c['id']+' '+c['greek']+': '+safe(c['definition'])+' Status: '+row['status']+'.',
                '', 'Source: '+p['source_id']+'; '+p['locator']+'; '+p['translator']+'; '+row['rule_id']+'.',
                '', 'Missing/limits: '+safe('; '.join(row['missing_context']) or 'No additional selected-case condition;predictive validity remains unverified')]
        lines+=['','Classification conflicts: '+safe(', '.join(result['historical_taxonomy']['conflicts']) or 'none')]
    else:lines+=['','Historical references disabled by user preference.']
    lines+=['','## Historical context qualifications']
    for rule in result['context_guidance']:
        lines+=['','- '+safe(rule['statement'])+' ['+rule['source_id']+'; '+rule['locator']+'; '+rule['rule_id']+']']
    lines+=['','## Explicit motif references']
    for row in result['motif_references']:
        lines+=['','### '+safe(row['motif_id'])+' — '+row['status']]
        if 'reference' in row:
            p=row['reference']['provenance'];lines+=['',safe(row['reference']['definition']),'', 'Source: '+p['source_id']+'; '+p['locator']+'; '+p['translator']+'; '+row['rule_id']+'.']
            for case in row['selected_cases']:lines+=['','Historical case '+case['id']+': '+safe(case['historical_account'])]
            lines+=['','Case conditions anduser evidence:','']+block(json.dumps(row,indent=2),'json')
        else:lines+=['','Unsupported source case;no substitute meaning supplied.']
    lines+=['','## Manual annotations','']+block(json.dumps(result['annotations'],indent=2),'json')
    lines+=['','## Editorial comparison','',safe(result['summary']['text'])]
    for question in result['editorial_reflection']['questions']:lines+=['','- '+safe(question)]
    lines+=['','## Source scope andlimits','',safe(' '.join(result['limitations'])),
        '', '[Selected historical excerpts]('+result['sources'][0]['url']+')',
        '', '[Greek terminology witness]('+result['sources'][1]['url']+')',
        '',safe(result['sources'][0]['rights_note']),'', '## Exact replay metadata','']
    lines+=block(json.dumps(result['replay'],indent=2),'json')
    return '\n'.join(lines)+'\n'


def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),dream_report=None),indent=2)
    return '# Dream request rejected\n\n'+html.escape(str(message))+'\n'
