"""Edition-bounded practitioner references and voluntary reflection; no archive retrieval."""
import copy
from datetime import datetime
import html
import json
from pathlib import Path
import re
from .knowledge import Rule
from .scrying import freeze, thaw, digest, _object, _raw, _optional_text, _timestamp, load_input

ROOT = Path(__file__).resolve().parents[1]
DATA = freeze(json.loads((ROOT/'knowledge/akashic_profile_v1.json').read_text(encoding='utf-8')))
PROFILE = DATA['profile']; PROFILE_HASH = digest(thaw(DATA)); CONCEPTS = DATA['concepts']
PURPOSES = ('personal_reflection', 'historical_research', 'creative_imagination', 'factual_prediction',
            'medical_clinical', 'unspecified', 'unknown')
FORMS = ('open', 'yes_no', 'time_based', 'unspecified')
STATES = ('prepared', 'in_progress', 'completed', 'discontinued')
REFRAMES = {'open_reflection': 'What choices, uncertainties and personal values would I like to explore?',
            'source_research': 'What does this named source claim, and what evidence or context remains unavailable?'}


def _id(v):
    return isinstance(v, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}', v) is not None


def _ids(value, limit=32):
    return isinstance(value, list) and len(value) <= limit and all(_id(x) for x in value) and len(set(value)) == len(value)


def validate(value):
    _object(value, ['schema_version','profile','task','mode','question','concept_ids','background','focus',
                    'intention','unknowns','reframe','editorial_questions','session','notes','comparisons'])
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1:
        raise ValueError('schema_version must be integer1')
    if value.get('profile', PROFILE) != PROFILE or value.get('task') != 'reference_reflection' or value.get('mode') != 'manual':
        raise ValueError('Use the named Howe public profile, reference_reflection task and manual mode')
    question = value.get('question', {})
    _object(question, ['text','purpose','form'])
    _optional_text(question, 'text', 20000)
    if question.get('purpose', 'unspecified') not in PURPOSES or question.get('form','unspecified') not in FORMS:
        raise ValueError('Use an explicit supported question purpose and form')
    for field in ('concept_ids','comparisons'):
        if field in value and not _ids(value[field]):raise ValueError(field+' requires distinct plain identifiers, up to32')
    for field in ('background','focus','intention'):_optional_text(value, field, 10000)
    if 'unknowns' in value and (not isinstance(value['unknowns'],list) or len(value['unknowns'])>32 or any(not _raw(x,2000) for x in value['unknowns'])):
        raise ValueError('unknowns must be up to32 raw user text entries')
    if value.get('reframe','none') not in ('none','open_reflection','source_research'):
        raise ValueError('Unknown editorial reframe choice')
    if 'editorial_questions' in value and type(value['editorial_questions']) is not bool:
        raise ValueError('editorial_questions must be boolean')
    session=value.get('session',{})
    _object(session,['id','state','timestamp','stages'])
    if 'id' in session and not _id(session['id']):raise ValueError('Session id must be a bounded plain identifier')
    state=session.get('state','prepared')
    if state not in STATES:raise ValueError('Unsupported declared session state')
    _timestamp(session.get('timestamp'))
    stages=session.get('stages',[])
    if not isinstance(stages,list) or len(stages)>len(DATA['stages']):raise ValueError('Use up to7 ordered stage declarations')
    last=-1;seen={};clocks={True:None,False:None}
    for stage in stages:
        _object(stage,['id','status','timestamp','comment'])
        identifier=stage.get('id')
        if identifier not in DATA['stages']:raise ValueError('Unknown application stage')
        index=DATA['stages'].index(identifier)
        if index<=last:raise ValueError('Stage IDs must follow frozen order without duplicates or sorting')
        last=index;status=stage.get('status','pending')
        if status not in ('pending','completed','skipped'):raise ValueError('Unknown stage status')
        seen[identifier]=status
        _optional_text(stage,'comment',2000);_timestamp(stage.get('timestamp'))
        stamp=stage.get('timestamp')
        if isinstance(stamp,str) and 'T' in stamp:
            moment=datetime.fromisoformat(stamp.replace('Z','+00:00'));aware=moment.tzinfo is not None
            if clocks[aware] is not None and moment<clocks[aware]:raise ValueError('Comparable stage timestamps cannot decrease')
            clocks[aware]=moment
    if state=='prepared' and 'completed' in seen.values():raise ValueError('Prepared session cannot contain completed stages')
    if state=='completed' and (seen.get('finish') not in ('completed','skipped') or 'pending' in seen.values()):
        raise ValueError('Completed session requires an explicit finished/skipped finish stage and no pending recorded stages')
    notes=value.get('notes',[])
    if not isinstance(notes,list) or len(notes)>64:raise ValueError('Use up to64 voluntary notes')
    note_ids=set()
    for note in notes:
        _object(note,['id','text','kind','timestamp','uncertainty','concept_ids'])
        if not _id(note.get('id')) or note['id'] in note_ids:raise ValueError('Note IDs must be unique')
        note_ids.add(note['id']);_optional_text(note,'text',20000);_timestamp(note.get('timestamp'))
        if note.get('kind','reflection') not in ('reflection','association','imagined_scene','unanswered'):
            raise ValueError('Unsupported user-attributed note kind')
        if 'uncertainty' in note and type(note['uncertainty']) is not bool:raise ValueError('Uncertainty must be boolean')
        if 'concept_ids' in note and not _ids(note['concept_ids'],16):raise ValueError('Note concepts must be distinct bounded identifiers')
    return copy.deepcopy(value)


def lookup(identifier):
    if identifier not in CONCEPTS:
        return dict(id=identifier,status='unsupported_concept',reference=None,answer=None,
                    missing=['Verified concept in this source profile'],fallback_used=False)
    return dict(id=identifier,status='source_reference',reference=thaw(CONCEPTS[identifier]),
                rule_id='akashic.howe.'+identifier,answer=None,coverage='Practitioner attribution only;not supernatural verification')


def register_knowledge(registry):
    for source in DATA['sources']:registry.add_source(thaw(source))
    for identifier,concept in CONCEPTS.items():
        p=concept['provenance']
        registry.add_rule(Rule('akashic.howe.'+identifier,1,26,'Linda Howe Pathway Prayer',PROFILE,
            p['source_id'],p['locator'],concept['description'],'akashic_source_reference',{},'proposed','traditional',[]))


def read(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    question=request.get('question',{});declared=question.get('purpose','unspecified')
    purpose='unspecified' if declared=='unknown' else declared;form=question.get('form','unspecified')
    statuses=dict(personal_reflection='reflective_reference',historical_research='historical_reference',
        creative_imagination='user_imagination',factual_prediction='unsupported_request',
        medical_clinical='unsupported_request',unspecified='purpose_unspecified')
    guidance_ids=list(DATA['guidance_map'][purpose]);form_ids=['question_framing'] if form in ('yes_no','time_based') else []
    references=[]
    for identifier in dict.fromkeys(request.get('concept_ids',[])+guidance_ids+form_ids):
        result=lookup(identifier)
        result['selection_reasons']=(['explicit_concept_selection'] if identifier in request.get('concept_ids',[]) else [])+(['editorial_mapping_of_declared_purpose'] if identifier in guidance_ids else [])+(['editorial_mapping_of_declared_form'] if identifier in form_ids else [])
        references.append(result)
    text=question.get('text');missing=[]
    if text is None or not text.strip():missing.append('No nonblank question supplied;reference lookup remains available')
    if purpose=='unspecified':missing.append('Question purpose unspecified;no intent inferred from words')
    for key in ('background','focus'):
        if request.get(key) is None:missing.append('Optional '+key+' not supplied')
    if any(r['status']=='unsupported_concept' for r in references):missing.append('One or more selected source concepts are unsupported')
    session=copy.deepcopy(request.get('session',{}));stages=session.get('stages',[])
    stage_reports=[]
    for stage in stages:
        links={'source_review':['records','pathway'],'preparation':['opening','conscious'],'question':['question_framing'],
               'notes':['describe'],'concept_review':[],'finish':['closing'],'reflection':['describe']}[stage['id']]
        stage_reports.append(dict(user_declaration=stage,provenance='editorial_application_tracking',
                                  source_reference_ids=links,supernatural_compliance_verified=False))
    reframing=request.get('reframe','none')
    reframe=None if reframing=='none' else dict(choice=reframing,text=REFRAMES[reframing],
        evidence='editorial_software_guidance',source_quote=False,original_question_replaced=False,original_purpose_changed=False)
    notes=[dict(user_record=copy.deepcopy(note),coverage='user_attributed_'+note.get('kind','reflection'),
                references=[lookup(k) for k in note.get('concept_ids',[])],historical_record_retrieved=False) for note in request.get('notes',[])]
    return dict(schema_version=1,technique_id=26,profile=PROFILE,mode='manual',task='reference_reflection',
        sources=thaw(DATA['sources']),edition_boundary=DATA['edition_boundary'],
        question=dict(user_record=copy.deepcopy(question),effective_purpose=purpose,status=statuses[purpose],answer=None,
                      intent_inferred=False,form_guidance='source_discouraged' if form in ('yes_no','time_based') else 'not_assessed'),
        concept_references=references,
        guidance=dict(evidence='editorial_selection_of_source_references',purpose_reference_ids=guidance_ids,form_reference_ids=form_ids,
            procedure=thaw(DATA['procedure']),note='These references describe source claims. They are not answers retrieved for the user;practitioner question restrictions do not establish supernatural access.'),
        editorial_reframe=reframe,
        session=dict(user_record=session,effective_state=session.get('state','prepared'),stage_reports=stage_reports,
                     unrecorded_stages=[s for s in DATA['stages'] if s not in {row['id'] for row in stages}],
                     stage_origin=DATA['stage_origin'],spiritual_records_opened=False,spiritual_records_closed_verified=False),
        user_context={k:copy.deepcopy(request[k]) for k in ('background','focus','intention','unknowns') if k in request},
        notes=notes,unknowns=dict(application_observations=missing,user_declared=copy.deepcopy(request.get('unknowns',[])),
            permanent_limits=['No independent verification of metaphysical records or source abilities','Book/page procedure differences and other traditions remain incomplete']),
        comparisons=[dict(profile=k,status='unsupported_comparison',reference=None,
            reason='Only the named Howe public profile is executable;independent documentary comparisons deferred. No cross-source synthesis.') for k in request.get('comparisons',[])],
        editorial_questions=['What do I know from my own experience, and what remains uncertain?',
                             'Which personal associations differ from the selected source description?'] if request.get('editorial_questions',True) else [],
        provenance_matrix=dict(direct='Ten source-located practitioner concepts and public procedure structural facts only',
            user_attributed='Original question,background,focus,intention,notes,associations,imagined scenes and declared stages',
            editorial='Purpose/form mapping,reframing,stage tracking,missing-field observations and reflective questions',
            unsupported='Metaphysical access,hidden histories,verified past lives,predictions,deceased contact,clinical conclusions'),
        limitations=thaw(DATA['unsupported'])+['Source-backed means the author made the claim,not that the claimed archive exists.',
            'No prayer copied or invented;no legal name,religious commitment,altered state or experience required.'],
        replay=dict(request=request,input_sha256=digest(request),profile_sha256=PROFILE_HASH,
                    source_sha256={s['id']:s['snapshot_sha256'] for s in DATA['sources']},
                    serialization='Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no final LF;raw text preserved with exact content line endings',
                    external_calls=False,generated_narrative=False,rng=False))


def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2)
        fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Akashic source reference and reflection','','Profile: '+PROFILE,'',html.escape(result['edition_boundary']),
           '', '## Source identity and rights','',block(result['sources']), '', '## User question and scope','',block(result['question']),
           '', '## Source-located concepts']
    for row in result['concept_references']:
        lines+=['','### '+html.escape(row['id'])+' — '+row['status'],'',block(row)]
    for title,key in [('Source-aware question guidance','guidance'),('Optional editorial reframing','editorial_reframe'),
        ('Declared session stages','session'),('User-supplied context','user_context'),('User-attributed notes','notes'),
        ('Unknowns and missing information','unknowns'),('Documentary comparison coverage','comparisons'),
        ('Editorial reflection questions','editorial_questions'),('Provenance matrix','provenance_matrix'),('Limits','limitations'),('Exact replay metadata','replay')]:
        lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'


def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),akashic_report=None),indent=2)
    return '# Akashic request rejected\n\n'+html.escape(str(message))+'\n'
