"""Moody1992 mirror-specific subset;user reports remain attributed,never detected."""
import copy
import html
import json
from pathlib import Path
import re
from types import MappingProxyType
from .knowledge import Rule
# Narrow pure utilities only;no Technique21 validation/read/profile substitution.
from .scrying import freeze,thaw,digest,_object,_optional_text,_timestamp,_raw,load_input

ROOT=Path(__file__).resolve().parents[1]
DATA=freeze(json.loads((ROOT/'knowledge/mirror_profile_v1.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile']
PROFILE_HASH=digest(thaw(DATA))
TYPES=DATA['experience_types']
RULES=MappingProxyType({r['id']:r for r in DATA['rules']})
STAGES=tuple(x['id'] for x in DATA['workflow'])


def validate(value):
    _object(value,['schema_version','profile','task','mode','session','stages','journal','personal_reflection'])
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE or value.get('task')!='guided_mirror_journal' or value.get('mode')!='manual':
        raise ValueError('Exact Moody1992 subset profile,guided_mirror_journal task and manual mode required')
    session=value.get('session',{})
    _object(session,['surface','view','lighting','background','intention','personal_context','timestamp','status'])
    for key,options,default in [('surface',DATA['surfaces'],'unspecified'),('view',DATA['view_options'],'unspecified')]:
        if not isinstance(session.get(key,default),str) or session.get(key,default) not in options:raise ValueError('Unsupported '+key+';use explicit unknown or unspecified')
    status=session.get('status','planned')
    if status not in ('planned','in_progress','completed','discontinued'):raise ValueError('Unknown declared session status')
    for key in ('lighting','background','intention','personal_context'):_optional_text(session,key,2000)
    _timestamp(session.get('timestamp'));_optional_text(value,'personal_reflection',10000)
    stages=value.get('stages',[])
    if not isinstance(stages,list) or len(stages)>len(STAGES):raise ValueError('Stages must be a list of up to6 declarations')
    seen=set()
    for row in stages:
        _object(row,['stage_id','status']);identifier=row.get('stage_id')
        if not isinstance(identifier,str) or identifier not in STAGES:raise ValueError('Unknown Mirror guide stage')
        if identifier in seen:raise ValueError('Duplicate or conflicting stage declarations rejected')
        seen.add(identifier)
        if row.get('status') not in ('completed','skipped'):raise ValueError('Stage status must be completed or skipped')
        if status=='planned' and row['status']=='completed':raise ValueError('Planned session conflicts with completed stage;declare session state explicitly')
    rows=value.get('journal')
    if rows is not None:
        if not isinstance(rows,list) or len(rows)>128:raise ValueError('Journal must be null or up to128 user entries')
        last=0
        for row in rows:
            _object(row,['experience_type','description','sequence','timestamp','uncertainty','associations','personal_reflection'])
            if 'experience_type' in row and (not isinstance(row['experience_type'],str) or row['experience_type'] not in TYPES):raise ValueError('Unknown user experience type;no detected spirit or generated vision category')
            for key in ('description','personal_reflection'):_optional_text(row,key,10000)
            if 'sequence' in row:
                n=row['sequence']
                if type(n) is not int or not last<n<=1000000:raise ValueError('Sequence numbers must strictly increase without reordering')
                last=n
            if 'uncertainty' in row and type(row['uncertainty']) is not bool:raise ValueError('Uncertainty must be boolean when supplied')
            _timestamp(row.get('timestamp'))
            if 'associations' in row:
                a=row['associations']
                if not isinstance(a,list) or len(a)>32 or any(not _raw(x,2000) for x in a):raise ValueError('Associations must be up to32 user-authored UTF8 strings')
    return copy.deepcopy(value)


def register_knowledge(registry):
    registry.add_source(thaw(DATA['source']))
    for r in DATA['rules']:
        registry.add_rule(Rule(r['id'],r['version'],22,'psychomanteum',PROFILE,r['source_id'],r['locator'],
            r['statement'],'mirror_procedure_reference',dict(coverage=r['coverage']),'proposed','traditional',[]))


def read(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    session=request.get('session',{});stage_map={r['stage_id']:r['status'] for r in request.get('stages',[])}
    guidance=thaw(DATA['workflow'])
    for n,step in enumerate(guidance,1):
        step.update(order=n,user_stage_status=stage_map.get(step['id'],'not_recorded'),performed_by_engine=False,
            source_components=[thaw(RULES[k]) for k in step['rule_ids']])
    journal=[];counts={k:0 for k in TYPES};counts['unclassified']=0
    for n,row in enumerate(request.get('journal') or [],1):
        kind=row.get('experience_type');counts[kind or 'unclassified']+=1;raw=row.get('description')
        state='missing' if 'description' not in row else 'null' if raw is None else 'blank' if not raw.strip() else 'text'
        conflicts=['uncertain_type_with_uncertainty_false'] if kind=='uncertain' and row.get('uncertainty') is False else []
        journal.append(dict(input_order=n,user_record=copy.deepcopy(row),experience_type=kind,
            attribution='user_reported;not engine-observed',description_state=state,
            uncertainty=dict(user_declared=row.get('uncertainty'),classification_unresolved=kind in (None,'uncertain'),
                conflicts=conflicts,physical_reality_verified=False),
            associations=dict(coverage='user_attributed',values=copy.deepcopy(row.get('associations',[])),universal_meaning=False)))
    journal_state='missing' if 'journal' not in request else 'null' if request['journal'] is None else 'empty' if not request['journal'] else 'provided'
    view=session.get('view','unspecified')
    actual=dict(coverage='user_declared_conditions',values=copy.deepcopy(session),effective_surface=session.get('surface','unspecified'),
        effective_view=view,view_relation_to_source='declared match' if view=='self_reflection_excluded' else 'declared difference' if view=='self_reflection_visible' else 'unknown',
        environment_observed_by_engine=False,source_setup_required=False)
    meaningful=any(isinstance(r['user_record'].get('description'),str) and r['user_record']['description'].strip() for r in journal)
    questions=['What details do you choose to retain from your own notes?','Which associations are personal to you?','How,if at all,do these notes relate to your intention?'] if meaningful else ['Would you like to leave this as no report or add your own words? No imagery or encounter is required.']
    summary=('You supplied '+str(len(journal))+' journal entries. '+
        ('Declared categories: '+', '.join(k+'='+str(v) for k,v in counts.items() if v)+'. ' if journal else 'No experience was recorded. ')+
        'Stage declarations and descriptions remain user reports;no person,presence or hidden meaning is identified.')
    replay=dict(request=request,profile=PROFILE,profile_sha256=PROFILE_HASH,source_id=DATA['source']['id'],
        source_snapshot_sha256=DATA['source']['snapshot_sha256'],workflow='moody1992-subset-editorial-journal-v1',
        ordering='Input list preserved;sequence annotations never sort',clock_used=False,seed_protocol=None,
        full_source_protocol_reproduced=False,contact_inferred=False)
    return dict(schema_version=1,technique_id=22,profile=PROFILE,task='guided_mirror_journal',mode='manual',
        session=actual,guidance=guidance,guidance_scope='Source-backed subset guidance;stage completion is user declared,not observed',
        adaptation=DATA['adaptation'],historical_setup=thaw(DATA['historical_setup']),
        direct=dict(coverage='source_reference',rules=thaw(DATA['rules']),edition_boundary='1992 article subset;not full1993 Reunions,Atkinson orDee/Casaubon procedure'),
        journal=journal,journal_state=journal_state,personal_reflection=request.get('personal_reflection'),
        summary=dict(coverage='neutral_editorial_summary',counts=counts,text=summary),
        editorial_reflection=dict(coverage='modern_editorial',questions=questions,symbol_dictionary_used=False),
        unsupported=['Objective deceased-person/spirit contact oridentity','Clinical/grief-treatment efficacy,diagnosis orprediction','Universal symbolism orhidden knowledge'],
        sources=[thaw(DATA['source'])],limitations=list(DATA['limits']),replay=replay,
        contact_verified=False,perception_detected=False,therapeutic_efficacy_claimed=False,factual_prediction=False,confidence_score=None)


def markdown(result):
    def safe(v):return html.escape(str(v)).replace('|','&#124;').replace('\n',' ')
    def block(v,language='text'):
        fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',v)),default=0))
        return [fence+language,v,fence]
    lines=['# Mirror Scrying — guided mirror journal','','Profile: '+result['profile'],'',safe(result['guidance_scope']),
        '',safe(result['adaptation']),'','## User-declared session','']+block(json.dumps(result['session'],indent=2),'json')
    lines+=['','## Source-specific guide']
    for step in result['guidance']:
        lines+=['',str(step['order'])+'. '+safe(step['text'])+' ['+step['coverage']+'; user status '+step['user_stage_status']+']']
        for rule in step['source_components']:lines+=['','Source: '+rule['source_id']+'; '+safe(rule['locator'])+'; '+rule['id']+'.']
    lines+=['','## Original journal','','Journal state: '+result['journal_state']+'.']
    for row in result['journal']:
        lines+=['','### Entry '+str(row['input_order']),'','Type: '+safe(row['experience_type'])+'; '+safe(row['attribution']),
            '', 'Uncertainty: '+safe(json.dumps(row['uncertainty'])),'','Original user record:','']+block(json.dumps(row['user_record'],indent=2),'json')
        if row['user_record'].get('description') is not None:lines+=['','Verbatim description:','']+block(row['user_record']['description'])
        for association in row['associations']['values']:lines+=['','User association (not universal):','']+block(association)
        if row['user_record'].get('personal_reflection') is not None:lines+=['','User personal reflection:','']+block(row['user_record']['personal_reflection'])
    if result['personal_reflection'] is not None:lines+=['','## User personal reflection','']+block(result['personal_reflection'])
    lines+=['','## Neutral summary','',safe(result['summary']['text']),'','Modern editorial questions:']
    for question in result['editorial_reflection']['questions']:lines+=['','- '+safe(question)]
    lines+=['','## Source reference and qualifications']
    for rule in result['direct']['rules']:lines+=['','- '+safe(rule['statement'])+' ['+rule['id']+'; '+safe(rule['locator'])+']']
    lines+=['','[Inspected1992 article]('+result['sources'][0]['url']+')','',safe(result['direct']['edition_boundary']),
        '', 'Historical setup facts (reference only):','']+block(json.dumps(result['historical_setup'],indent=2),'json')
    lines+=['','## Limits','',safe(' '.join(result['limitations'])),'',safe('; '.join(result['unsupported'])),
        '', '## Exact replay metadata','']+block(json.dumps(result['replay'],indent=2),'json')
    return '\n'.join(lines)+'\n'


def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),session_report=None),indent=2)
    return '# Mirror Scrying request rejected\n\n'+html.escape(str(message))+'\n'
