"""Manual public-source candle comparisons; no combustion or personal inference."""
import copy
import html
import json
from pathlib import Path
import re
from .knowledge import Rule
from .scrying import freeze,thaw,digest,_object,_optional_text,load_input

ROOT=Path(__file__).resolve().parents[1]
DATA=freeze(json.loads((ROOT/'knowledge/pyromancy_profile_v1.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile'];PROFILE_HASH=digest(thaw(DATA));RULES=DATA['rules']
STATES=('applicable','not_applicable','insufficient_evidence','conflicting_evidence','unsupported')
UNKNOWN=(None,'unknown','ambiguous')
ORIGINS=('reported_real','hypothetical','synthetic','unknown')
PHENOMENA=('flame','soot','smoke','ember','lamp','flame_color','other','unknown')
ATTRIBUTES={
    'substrate':('candle_flame','glass_jar','lamp_flame','other','unknown','ambiguous'),
    'height':('high','low','normal','unknown','ambiguous'),
    'stability':('steady','erratic','unknown','ambiguous'),
    'persistence':('persistent','transient','unknown','ambiguous'),
    'soot_location':('upper','bottom','top_to_bottom','other','unknown','ambiguous'),
    'soot_extent':('upper_only','full_jar','partial','unknown','ambiguous'),
    'soot_density':('light','dense','unknown','ambiguous'),
    'soot_color':('black','grey','other','unknown','ambiguous'),
    'lower_glass_clear':'bool','light_through_deposit':'bool'}
PHYSICAL={
    'explanation':('known','possible','not_noticed','checked_no_issue','addressed','unknown','ambiguous'),
    'correction':('none','reported_completed','not_needed_after_check','unknown','ambiguous'),
    'after_correction':('persisted','improved','changed','unknown','ambiguous'),
    'wick':('normal','long','short','clogged','drowned','carbonized','undersized','buried','unknown','ambiguous'),
    'draft':'bool','dressing':('clear','excess','debris','unknown','ambiguous'),
    'construction':('suitable','concern','unknown','ambiguous')}
SAFETY_FIELDS=('unsafe_burning','overheating','active_hazard','stopped')


def _values(v):return v if isinstance(v,list) else [v]


def _id(v):return isinstance(v,str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',v) is not None


def _choice(v,allowed,name):
    vals=_values(v)
    if not vals or len(vals)>4:raise ValueError(name+' needs one value or up to four alternatives')
    for x in vals:
        if x is None:continue
        if allowed=='bool':valid=type(x) is bool
        else:valid=isinstance(x,str) and x in allowed
        if not valid:raise ValueError('Invalid '+name+' evidence')
    if len(set(json.dumps(x) for x in vals))!=len(vals):raise ValueError('Duplicate '+name+' alternatives')


def _safety_validate(obj):
    _object(obj,SAFETY_FIELDS)
    for k,v in obj.items():_choice(v,'bool',k)


def validate(value):
    _object(value,['schema_version','profile','task','mode','origin','safety','observations','notes','context','documentary_reference'])
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer 1')
    if value.get('profile')!=PROFILE or value.get('task')!='symbolic_candle_observation' or value.get('mode')!='manual':
        raise ValueError('Exact public2026 profile,symbolic_candle_observation task and manual mode required')
    if value.get('origin','unknown') not in ORIGINS:raise ValueError('Unsupported observation origin')
    if 'documentary_reference' in value and value['documentary_reference']!='pgm_iv_52_87':raise ValueError('Only pgm_iv_52_87 documentary context is available')
    _safety_validate(value.get('safety',{}))
    for k in ('notes','context'):_optional_text(value,k,10000)
    rows=value.get('observations',[])
    if not isinstance(rows,list) or len(rows)>64:raise ValueError('Use up to64 ordered observations')
    ids=set();last=0
    for row in rows:
        _object(row,['id','phenomenon','origin','sequence','alternatives','uncertainty','attributes','physical','safety','flame_color','wax_color','observation','association'])
        if not _id(row.get('id')) or row['id'] in ids:raise ValueError('Unique plain observation IDs required')
        ids.add(row['id'])
        if row.get('phenomenon') not in PHENOMENA:raise ValueError('Explicit supported observation category required;unknown is available')
        if row.get('origin','unknown') not in ORIGINS:raise ValueError('Unsupported observation origin')
        if 'sequence' in row:
            n=row['sequence']
            if type(n) is not int or not last<n<=1000000:raise ValueError('Explicit sequence must strictly increase within bounds')
            last=n
        alt=row.get('alternatives',[])
        if not isinstance(alt,list) or len(alt)>4 or any(not isinstance(x,str) or x not in PHENOMENA for x in alt) or len(set(alt))!=len(alt) or row['phenomenon'] in alt:
            raise ValueError('Use up to four distinct alternative phenomenon categories')
        if 'uncertainty' in row and type(row['uncertainty']) is not bool:raise ValueError('Uncertainty must be boolean')
        for name,fields in [('attributes',ATTRIBUTES),('physical',PHYSICAL)]:
            obj=row.get(name,{})
            _object(obj,fields)
            for k,v in obj.items():_choice(v,fields[k],k)
        _safety_validate(row.get('safety',{}))
        for k in ('observation','association'):_optional_text(row,k,10000)
        for k in ('flame_color','wax_color'):_optional_text(row,k,80)
    return copy.deepcopy(value)


def _condition(actual,expected):
    vals=_values(actual);known=[v for v in vals if v not in UNKNOWN];matches=[v==expected for v in known]
    if any(matches) and not all(matches):return 'conflicting_evidence'
    if matches and not any(matches):return 'not_applicable'
    if not known or len(known)!=len(vals):return 'insufficient_evidence'
    return 'applicable'


def _combine(states):
    for s in ('conflicting_evidence','not_applicable','insufficient_evidence'):
        if s in states:return s
    return 'applicable'


def _known(v):return [x for x in _values(v) if x not in UNKNOWN]


def safety(request):
    declarations=[dict(location='session',declared=request.get('safety',{}))]
    declarations += [dict(location=o['id'],declared=o.get('safety',{})) for o in request.get('observations',[]) if 'safety' in o]
    hazards=[dict(location=d['location'],field=k,declared=copy.deepcopy(d['declared'][k])) for d in declarations for k in SAFETY_FIELDS[:3] if k in d['declared'] and True in _values(d['declared'][k])]
    stopped=any(True in _values(d['declared'].get('stopped')) for d in declarations)
    hold=bool(hazards)
    if hold:
        message='Keep the reported activity stopped;do not handle hot equipment. Use recorded or hypothetical observations.' if stopped else 'Prioritize stopping the reported unsafe activity safely. Do not handle hot equipment or maintain a hazardous burn for a reading.'
    elif stopped:message='Activity is reported stopped;no relighting is needed. Recorded or hypothetical observations are sufficient.'
    else:message='No real flame is required. Safety declarations are not physical verification or permission to burn a candle.'
    return dict(priority='safety_hold' if hold else 'documentary_comparison_only',symbolic_hold=hold,declarations=copy.deepcopy(declarations),hazards=hazards,
        stopped_reported=stopped,message=message,physically_verified=False,policy=thaw(DATA['safety_policy']))


def physical(row):
    p=row.get('physical',{});a=row.get('attributes',{});missing=[];conflicts=[];adverse=[]
    for k,v in p.items():
        if len(set(_known(v)))>1:conflicts.append('Competing '+k+' declarations')
    explanation=p.get('explanation');correction=p.get('correction');after=p.get('after_correction')
    # Current detailed concerns are never silently cleared by a favorable summary.
    for k,normal in [('wick','normal'),('draft',False),('dressing','clear'),('construction','suitable')]:
        if any(x!=normal for x in _known(p.get(k))):adverse.append(k)
    e=_known(explanation);corr=_known(correction);post=_known(after)
    clear=any(x in ('checked_no_issue','addressed') for x in e)
    if clear and adverse:conflicts.append('Qualified physical summary conflicts with current concerns:'+','.join(adverse))
    if 'addressed' in e and any(x in ('none','not_needed_after_check') for x in corr):conflicts.append('Addressed explanation without a completed correction')
    if any(x in ('none','not_needed_after_check') for x in corr) and post:conflicts.append('Follow-up supplied despite explicitly absent correction')
    persistent=_known(a.get('persistence'))
    if ('persistent' in persistent and any(x in ('improved','changed') for x in post)) or ('transient' in persistent and 'persisted' in post):
        conflicts.append('Current persistence conflicts with the reported follow-up')
    if conflicts:state='conflicting_evidence'
    elif adverse or any(x in ('known','possible') for x in e):state='not_applicable'
    elif not e or 'not_noticed' in e or len(e)!=len(_values(explanation)):
        state='insufficient_evidence';missing.append('Explicit qualified physical check/correction;no cause noticed is not absence')
    elif not corr or len(corr)!=len(_values(correction)):
        state='insufficient_evidence';missing.append('Explicit correction status')
    elif correction=='none' or corr==['none']:
        state='insufficient_evidence';missing.append('Completed correction or explicit not-needed-after-check declaration')
    else:state='applicable'
    return dict(status=state,declared=copy.deepcopy(p),current_concerns=adverse,missing=missing,conflicts=conflicts,
        cause_verified=False,note=DATA['physical_policy']['no_proof'])


def _followup(row):
    p=row.get('physical',{});correction=p.get('correction')
    if _condition(correction,'reported_completed')=='applicable':return _condition(p.get('after_correction'),'persisted')
    if _condition(correction,'not_needed_after_check')=='applicable':return _condition(p.get('explanation'),'checked_no_issue')
    if len(set(_known(correction)))>1:return 'conflicting_evidence'
    return 'insufficient_evidence'


def _geometry_conflicts(row):
    a=row.get('attributes',{});conflicts=[]
    # These fields describe the same current deposit;opposed meanings cannot be silently repaired.
    if 'full_jar' in _known(a.get('soot_extent')) and (True in _known(a.get('lower_glass_clear')) or 'upper' in _known(a.get('soot_location'))):
        conflicts.append('Full-jar extent conflicts with clear lower glass or upper-only location')
    if 'upper_only' in _known(a.get('soot_extent')) and 'top_to_bottom' in _known(a.get('soot_location')):
        conflicts.append('Upper-only extent conflicts with top-to-bottom location')
    return conflicts


def evaluate(row,request,guard):
    p=physical(row);geo=_geometry_conflicts(row);cases=[]
    for rule in RULES:
        if rule['requires']['phenomenon']!=row['phenomenon']:continue
        conditions=[]
        for key,expected in rule['requires'].items():
            if key=='physical_qualified':actual=p['status'];state=p['status']
            elif key=='followup_qualified':actual=copy.deepcopy(row.get('physical',{}));state=_followup(row)
            else:
                actual=row['phenomenon'] if key=='phenomenon' else row.get('physical',{}).get(key) if key in PHYSICAL else row.get('attributes',{}).get(key)
                state=_condition(actual,expected)
            conditions.append(dict(field=key,expected=expected,declared=copy.deepcopy(actual),status=state))
        state=_combine([x['status'] for x in conditions])
        if geo or row.get('alternatives'):state='conflicting_evidence'
        elif row.get('uncertainty') and state=='applicable':state='insufficient_evidence'
        candidate=state
        if guard['symbolic_hold'] and state=='applicable':state='not_applicable'
        cases.append(dict(id=rule['case'],rule_id=rule['id'],status=state,condition_status=candidate,
            source_id=rule['source_id'],locator=rule['locator'],conditions=conditions,
            displayed_account=rule['statement'] if state=='applicable' else None,
            safety_hold=guard['symbolic_hold']))
    statuses=[r['status'] for r in cases]
    if not statuses:status='unsupported'
    elif 'conflicting_evidence' in statuses:status='conflicting_evidence'
    elif 'applicable' in statuses:status='applicable'
    elif 'insufficient_evidence' in statuses:status='insufficient_evidence'
    else:status='not_applicable'
    unresolved=[dict(case=c['id'],field=x['field'],status=x['status']) for c in cases for x in c['conditions'] if x['status'] in ('insufficient_evidence','conflicting_evidence')]
    if row.get('alternatives'):unresolved.append(dict(field='phenomenon_identification',status='conflicting_evidence'))
    if row.get('uncertainty'):unresolved.append(dict(field='user_uncertainty',status='insufficient_evidence'))
    unsupported_fields=[k for k in ('flame_color','wax_color') if k in row]
    return dict(id=row['id'],phenomenon=row['phenomenon'],origin=row.get('origin',request.get('origin','unknown')),status=status,
        declared=copy.deepcopy(row),physical_assessment=p,cases=cases,unresolved=unresolved,conflicts=geo,
        unsupported_symbolic_fields=unsupported_fields,color_correspondences=None,
        note='Unsupported categories and colors retain declarations without invented meanings. Nonapplication is not a negative forecast.')


def register_knowledge(registry):
    for s in (*DATA['sources'],*DATA['documentary_sources']):registry.add_source(thaw(s))
    for r in RULES:
        registry.add_rule(Rule(r['id'],1,30,'Contemporary candle flame and jar soot',PROFILE,r['source_id'],r['locator'],r['statement'],
            'pyromancy_manual_condition',thaw(r['requires']),'proposed','traditional',[]))


def read(value,registry=None):
    q=validate(value)
    if registry is not None:register_knowledge(registry)
    guard=safety(q);rows=[evaluate(o,q,guard) for o in q.get('observations',[])]
    synthesis=[dict(observation_id=r['id'],evidence='editorial',accounts=[c['displayed_account'] for c in r['cases'] if c['displayed_account']],
        unresolved=r['unresolved'],physical_missing=r['physical_assessment']['missing'],conflicts=r['physical_assessment']['conflicts']+r['conflicts'],
        reflection=None if guard['symbolic_hold'] else 'Which parts are your direct observations,and which are your own associations?',
        note='Attributed practitioner metaphor only;no conclusion about a person,spirit or future event.') for r in rows]
    return dict(schema_version=1,technique_id=30,profile=PROFILE,task='symbolic_candle_observation',mode='manual',safety=guard,
        sources=thaw(DATA['sources']),observation_provenance=dict(default_origin=q.get('origin','unknown'),physically_verified=False,input_order_retained=True),
        observations=rows,editorial_synthesis=synthesis,summary=dict(observations=len(rows),counts={s:sum(r['status']==s for r in rows) for s in STATES}),
        physical_policy=thaw(DATA['physical_policy']),documentary_lamp=thaw(DATA['documentary_lamp'])|dict(requested=q.get('documentary_reference')=='pgm_iv_52_87'),
        documentary_sources=thaw(DATA['documentary_sources']),user_notes=q.get('notes'),user_context=q.get('context'),
        provenance_matrix=dict(direct='Dated public practitioner accounts and practical qualifications;separate documentary lamp/physical context',
            user_attributed='Ordered manual observations,origins,features,checks,corrections,safety and voluntary text',editorial='Conservative condition comparisons,physical-confound bookkeeping,safety hold and neutral reflection',
            unsupported='Objective prediction,clinical/personality/willpower conclusions,spirits,third-party emotions,hidden intentions or validated paranormal influence'),
        conventions=thaw(DATA['editorial_conventions']),limitations=thaw(DATA['unsupported']),
        replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,source_sha256={s['id']:s['snapshot_sha256'] for s in DATA['sources']},
            serialization='Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw content line endings retained',external_calls=False,rng=False,generated_observations=False))


def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2);fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Pyromancy historical symbolic candle report','','Profile: '+PROFILE,'',html.escape(result['safety']['message'])]
    for title,key in [('Safety and stopping','safety'),('Exact public sources and rights','sources'),('Observation provenance','observation_provenance'),
        ('Ordered manual observations and conditions','observations'),('Editorial symbolic comparison','editorial_synthesis'),('Coverage summary','summary'),('Physical qualifications','physical_policy'),
        ('Ancient lamp documentary context','documentary_lamp'),('Separate documentary sources','documentary_sources'),('User notes','user_notes'),('User context','user_context'),
        ('Evidence layers','provenance_matrix'),('Application conventions','conventions'),('Limits','limitations'),('Exact replay metadata','replay')]:
        lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'


def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),pyromancy_report=None),indent=2)
    return '# Pyromancy request rejected\n\n'+html.escape(str(message))+'\n'
