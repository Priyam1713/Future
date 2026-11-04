"""Edition-bounded guidance and faithful user journaling;no perception inference."""
import copy
from datetime import date,datetime
import hashlib
import html
import json
from pathlib import Path
import re
from types import MappingProxyType
from .knowledge import Rule


def freeze(v):
    if isinstance(v,dict):return MappingProxyType({k:freeze(x) for k,x in v.items()})
    if isinstance(v,list):return tuple(freeze(x) for x in v)
    return v


def thaw(v):
    if isinstance(v,(dict,MappingProxyType)):return {k:thaw(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [thaw(x) for x in v]
    return v


def digest(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()


ROOT=Path(__file__).resolve().parents[1]
DATA=freeze(json.loads((ROOT/'knowledge/scrying_profile_v1.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile']
PROFILE_HASH=digest(thaw(DATA))
TYPES=DATA['experience_types']
RULES=MappingProxyType({r['id']:r for r in DATA['rules']})


def _object(v,fields):
    if not isinstance(v,dict) or set(v)-set(fields):raise ValueError('Expected object with supported fields only')


def _raw(v,limit):
    if not isinstance(v,str) or len(v)>limit or any(ord(c)<32 and c not in '\r\n\t' for c in v):return False
    try:v.encode('utf-8',errors='strict')
    except UnicodeError:return False
    return True


def _optional_text(obj,key,limit):
    if key in obj and obj[key] is not None and not _raw(obj[key],limit):raise ValueError(key+' must be UTF8 text or null within its length bound')


def _timestamp(value):
    if value is None:return
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:[0-5]\d)?)?',value):
        raise ValueError('Timestamp must be ISO date or dateTtime with seconds and optional offset;no automatic clock')
    try:
        if 'T' in value:datetime.fromisoformat(value.replace('Z','+00:00'))
        else:date.fromisoformat(value)
    except ValueError as exc:raise ValueError('Invalid calendar date/time') from exc


def validate(value):
    _object(value,['schema_version','profile','task','mode','session','journal','personal_reflection'])
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE or value.get('task')!='guided_journal' or value.get('mode')!='manual':
        raise ValueError('Exact Atkinson digital profile,guided_journal task and manual mode required')
    session=value.get('session',{})
    _object(session,['surface','lighting','background','intention','timestamp','practice','visualization_subject','status'])
    surface=session.get('surface','unspecified');practice=session.get('practice','gazing')
    if not isinstance(surface,str) or surface not in DATA['surfaces']:raise ValueError('Unknown reflective surface;use explicit unknown or unspecified')
    if not isinstance(practice,str) or practice not in DATA['practices']:raise ValueError('Unknown practice;no altered-state procedure')
    if session.get('status','planned') not in ('planned','completed','discontinued'):raise ValueError('Unknown declared session status')
    for key,limit in [('lighting',2000),('background',2000),('intention',2000),('visualization_subject',2000)]:_optional_text(session,key,limit)
    if 'visualization_subject' in session and practice!='familiar_visualization':raise ValueError('Visualization subject belongs only to optional familiar_visualization practice')
    _timestamp(session.get('timestamp'))
    _optional_text(value,'personal_reflection',10000)
    rows=value.get('journal')
    if rows is not None:
        if not isinstance(rows,list) or len(rows)>128:raise ValueError('Journal must be null or a list of up to128 user entries')
        last=0
        for row in rows:
            _object(row,['experience_type','description','sequence','timestamp','uncertainty','associations','personal_reflection'])
            if 'experience_type' in row and (not isinstance(row['experience_type'],str) or row['experience_type'] not in TYPES):
                raise ValueError('Use a user experience category;generated prompts are not user observations')
            for key in ('description','personal_reflection'):_optional_text(row,key,10000)
            if 'sequence' in row:
                number=row['sequence']
                if type(number) is not int or not last<number<=1000000:raise ValueError('Explicit sequence numbers must strictly increase;input order is preserved')
                last=number
            if 'uncertainty' in row and type(row['uncertainty']) is not bool:raise ValueError('Uncertainty must be an explicit boolean when supplied')
            _timestamp(row.get('timestamp'))
            if 'associations' in row:
                a=row['associations']
                if not isinstance(a,list) or len(a)>32 or any(not _raw(x,2000) for x in a):raise ValueError('Associations must be up to32 user-authored UTF8 strings')
    return copy.deepcopy(value)


def register_knowledge(registry):
    registry.add_source(thaw(DATA['source']))
    for r in DATA['rules']:
        registry.add_rule(Rule(r['id'],r['version'],21,'Crystal gazing',PROFILE,r['source_id'],r['locator'],
            r['statement'],'scrying_procedure_reference',dict(coverage=r['coverage']),'proposed','traditional',[]))


def read(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    session=request.get('session',{})
    surface=session.get('surface','unspecified');practice=session.get('practice','gazing')
    workflow=thaw(DATA['workflow'])
    if practice=='familiar_visualization':
        workflow[2]['rule_ids'].append('scrying.atkinson.visualize')
        workflow[2]['optional_visualization']='If you choose to picture a familiar subject,record that deliberate image as imagined imagery;it is not evidence of external perception.'
    for n,step in enumerate(workflow,1):
        step['order']=n;step['source_components']=[thaw(RULES[k]) for k in step['rule_ids']]
        step['performed_by_engine']=False
    journal=[];counts={k:0 for k in TYPES};counts['unclassified']=0
    for n,row in enumerate(request.get('journal') or [],1):
        kind=row.get('experience_type');counts[kind or 'unclassified']+=1
        raw=row.get('description');state='missing' if 'description' not in row else 'null' if raw is None else 'blank' if not raw.strip() else 'text'
        conflicts=['uncertain_type_with_uncertainty_false'] if kind=='uncertain' and row.get('uncertainty') is False else []
        journal.append(dict(input_order=n,user_record=copy.deepcopy(row),experience_type=kind,
            attribution='user_reported;not engine-observed',description_state=state,
            uncertainty=dict(user_declared=row.get('uncertainty'),classification_unresolved=kind in (None,'uncertain'),
                conflicts=conflicts,physical_reality_verified=False),
            associations=dict(coverage='user_attributed',values=copy.deepcopy(row.get('associations',[])),universal_meaning=False)))
    journal_state='missing' if 'journal' not in request else 'null' if request['journal'] is None else 'empty' if not request['journal'] else 'provided'
    meaningful=any(isinstance(x['user_record'].get('description'),str) and x['user_record']['description'].strip() for x in journal)
    text=('You supplied '+str(len(journal))+' journal entries. '+
        ('Declared categories: '+', '.join(k+'='+str(v) for k,v in counts.items() if v)+'. ' if journal else 'No experience was recorded. ')+
        'Descriptions and personal associations remain user-attributed;no hidden meaning or event is inferred.')
    questions=(['Which details in your own notes stood out?','What associations do you personally choose to make?',
        'How,if at all,do your notes relate to your stated intention?'] if meaningful else
        ['Would you like to leave the journal as it is or add your own notes? No imagery is required.'])
    actual=dict(coverage='user_declared_conditions',values=copy.deepcopy(session),
        effective_surface=surface,surface_defaulted='surface' not in session,practice=practice,practice_defaulted='practice' not in session,
        lighting_state='unspecified' if 'lighting' not in session else 'unknown' if session['lighting'] is None else 'user_reported',
        background_state='unspecified' if 'background' not in session else 'unknown' if session['background'] is None else 'user_reported',
        environment_observed_by_engine=False)
    replay=dict(request=request,profile=PROFILE,profile_sha256=PROFILE_HASH,source_id=DATA['source']['id'],
        source_snapshot_sha256=DATA['source']['snapshot_sha256'],workflow='editorial-guided-journal-v1',
        ordering='input list;explicit sequence annotations never sort',clock_used=False,seed_protocol=None,
        generated_creative_prompts=False,perception_inferred=False)
    return dict(schema_version=1,technique_id=21,profile=PROFILE,task='guided_journal',mode='manual',
        session=actual,guidance=workflow,guidance_scope='Reference guidance,not a record that steps were performed',
        stop_policy='May discontinue at any point;no required imagery,prolonged stare or altered state',
        direct=dict(coverage='source_reference',rules=thaw(DATA['rules']),edition_boundary='PG displayed reprint is not equated with LOC1908 facsimile'),
        historical_beliefs=dict(coverage='historical_author_claims',descriptions=[thaw(RULES['scrying.atkinson.reported_imagery'])],
            scientific_validation=False,expected_imagery_required=False),
        journal=journal,journal_state=journal_state,personal_reflection=request.get('personal_reflection'),
        summary=dict(coverage='neutral_editorial_summary',counts=counts,text=text),
        editorial_reflection=dict(coverage='modern_editorial',questions=questions,symbol_dictionary_used=False),
        creative_prompts=[],creative_prompt_system=thaw(DATA['generated_creative_prompt']),
        unsupported=['Universal symbolic meanings','Entity,spirit,hidden-memory or emotion detection','Factual prediction or diagnosis'],
        sources=[thaw(DATA['source'])],limitations=list(DATA['limits']),replay=replay,
        factual_prediction=False,perception_detected=False,confidence_score=None)


def markdown(result):
    def safe(v):return html.escape(str(v)).replace('|','&#124;').replace('\n',' ')
    def block(v,language='text'):
        fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',v)),default=0))
        return [fence+language,v,fence]
    lines=['# Scrying — guided symbolic journal','','Profile: '+result['profile'],'',safe(result['guidance_scope']),
        '',safe(result['stop_policy']),'','## User-declared session','']
    lines+=block(json.dumps(result['session'],ensure_ascii=True,indent=2),'json')
    lines+=['','## Guided procedure']
    for step in result['guidance']:
        lines+=['',str(step['order'])+'. '+safe(step['text'])+' ['+step['coverage']+']']
        if 'optional_visualization' in step:lines+=['',safe(step['optional_visualization'])]
        for rule in step['source_components']:
            lines+=['','Source: '+rule['source_id']+'; '+safe(rule['locator'])+'; '+rule['id']+'.']
    lines+=['','## Original journal','','Journal state: '+result['journal_state']+'.']
    for row in result['journal']:
        lines+=['','### Entry '+str(row['input_order']),'',
            'Type: '+safe(row['experience_type'])+'; '+safe(row['attribution'])+'; description state: '+row['description_state']+'.',
            '', 'Uncertainty: '+safe(json.dumps(row['uncertainty'])),'','Original user record:','']
        lines+=block(json.dumps(row['user_record'],ensure_ascii=True,indent=2),'json')
        raw=row['user_record'].get('description')
        if raw is not None:lines+=['','Verbatim description:','']+block(raw)
        for association in row['associations']['values']:
            lines+=['','User-authored association (no universal meaning):','']+block(association)
        reflection=row['user_record'].get('personal_reflection')
        if reflection is not None:lines+=['','User personal reflection:','']+block(reflection)
    if result['personal_reflection'] is not None:lines+=['','## User personal reflection','']+block(result['personal_reflection'])
    lines+=['','## Neutral summary','',safe(result['summary']['text']),'','Modern editorial questions:']
    for question in result['editorial_reflection']['questions']:lines+=['','- '+safe(question)]
    lines+=['','## Direct source reference']
    for rule in result['direct']['rules']:
        lines+=['','- '+safe(rule['statement'])+' ['+rule['id']+'; '+safe(rule['locator'])+']']
    lines+=['','[Selected historical digital text]('+result['sources'][0]['url']+')','',
        safe(result['direct']['edition_boundary']), '', 'Historical beliefs are not scientific validation;reported mist/pictures are not required.',
        '', '## Limits','',safe(' '.join(result['limitations'])),'','## Exact replay metadata','']
    lines+=block(json.dumps(result['replay'],ensure_ascii=True,indent=2),'json')
    return '\n'.join(lines)+'\n'


def load_input(path):
    def pairs(items):
        result={}
        for k,v in items:
            if k in result:raise ValueError('Duplicate JSON key: '+k)
            result[k]=v
        return result
    def invalid(v):raise ValueError('Nonfinite JSON: '+v)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid)


def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),session_report=None),indent=2)
    return '# Scrying request rejected\n\n'+html.escape(str(message))+'\n'
