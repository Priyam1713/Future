"""Manual Kent ordinary-cup references; no shape recognition or factual fortune claims."""
import copy
import html
import json
from pathlib import Path
import re
from .knowledge import Rule
from .scrying import freeze,thaw,digest,_object,_raw,_optional_text,load_input

ROOT=Path(__file__).resolve().parents[1]
DATA=freeze(json.loads((ROOT/'knowledge/tasseography_profile_v2.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile'];PROFILE_HASH=digest(thaw(DATA));SYMBOLS=DATA['symbols']
ENUMS=dict(region=tuple(DATA['regions']),handle_relation=('under_handle','near_handle','opposite','unknown'),
    proximity=('near','far','unknown'),heading=('towards_handle','away_from_handle','other','unknown'),
    motion=('flying','stationary','unknown'),size=('small','large','unknown'),clarity=('clear','indistinct','unknown'),
    multiplicity=('single','several','unknown'),arrangement=('surrounding','other','unknown'))
BOTTOM=('bottom','bottom_circle','bottom_centre')


def _id(v):return isinstance(v,str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',v) is not None


def _ids(v,n=32):return isinstance(v,list) and len(v)<=n and all(_id(x) for x in v) and len(set(v))==len(v)


def validate(value):
    _object(value,['schema_version','profile','task','mode','vessel','handle_orientation','context','observations','source_example','notes'])
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE or value.get('task')!='symbolic_cup_reading' or value.get('mode')!='manual' or value.get('vessel')!='cup':
        raise ValueError('Exact Kent v2 profile,symbolic_cup_reading task,manual mode and ordinary cup required;other methods unsupported')
    if value.get('handle_orientation','unknown') not in ('top','right','bottom','left','unknown'):raise ValueError('Unsupported declared handle orientation')
    if 'source_example' in value and value['source_example']!='figure_viii':raise ValueError('Only FigureVIII documentary comparison is available')
    _optional_text(value,'notes',10000)
    context=value.get('context',{});_object(context,['musician','sailor','marital_status','abode'])
    for field in ('musician','sailor'):
        if field in context and context[field] is not None and type(context[field]) is not bool:raise ValueError('Context flags must be boolean or null')
    if context.get('marital_status','unknown') not in ('married','unmarried','unknown'):raise ValueError('Unsupported declared marital_status')
    if context.get('abode','unknown') not in ('home','away','unknown'):raise ValueError('Unsupported declared abode')
    observations=value.get('observations',[])
    if not isinstance(observations,list) or len(observations)>64:raise ValueError('Use up to64 ordered manual observations')
    ids=set()
    for row in observations:
        _object(row,['id','symbol_id','alternatives','region_alternatives','adjacent_to','mark','numeral','uncertainty','observation','association',*ENUMS])
        if not _id(row.get('id')) or row['id'] in ids:raise ValueError('Observation IDs must be unique plain identifiers')
        ids.add(row['id'])
        if not _id(row.get('symbol_id')):raise ValueError('Supply an explicit symbol identifier,including unknown if needed')
        for field,allowed in ENUMS.items():
            if field in row and row[field] not in allowed:raise ValueError('Unsupported '+field+' category')
        for field,n in [('alternatives',4),('adjacent_to',64)]:
            if field in row and not _ids(row[field],n):raise ValueError('Distinct bounded identifiers required for '+field)
        if row.get('symbol_id') in row.get('alternatives',[]):raise ValueError('Primary identity cannot repeat as its alternative')
        regions=row.get('region_alternatives',[])
        if not isinstance(regions,list) or len(regions)>3 or any(not isinstance(x,str) or x not in DATA['regions'] for x in regions) or len(set(regions))!=len(regions) or row.get('region') in regions:
            raise ValueError('Use distinct supported alternative regions')
        if 'uncertainty' in row and type(row['uncertainty']) is not bool:raise ValueError('Uncertainty must be boolean')
        for field in ('observation','association'):_optional_text(row,field,10000)
        _optional_text(row,'mark',8)
        if isinstance(row.get('mark'),str) and row['mark'].strip() and not re.fullmatch(r'[A-Za-z]',row['mark']):
            raise ValueError('Supported initial mark is one Latin alphabetic character;other marks may be recorded as raw observations')
        if 'numeral' in row and (type(row['numeral']) is not int or not 0<=row['numeral']<=1000000000):raise ValueError('Numeral must be an explicit nonnegative bounded integer')
        if 'mark' in row and row['symbol_id']!='letter':raise ValueError('Only alphabetic-initial observations carry mark')
        if 'numeral' in row and row['symbol_id']!='numeral':raise ValueError('Only numeral observations carry numeral')
    for row in observations:
        if any(x not in ids or x==row['id'] for x in row.get('adjacent_to',[])):raise ValueError('Adjacency must reference other existing observations')
    return copy.deepcopy(value)


def _identity_uncertain(row):return bool(row.get('uncertainty') or row.get('alternatives'))


def _relation(a,b):
    ap=a.get('adjacent_to');bp=b.get('adjacent_to')
    positive=(ap is not None and b['id'] in ap) or (bp is not None and a['id'] in bp)
    negative=(ap is not None and b['id'] not in ap) or (bp is not None and a['id'] not in bp)
    if positive and negative:return 'conflicting_evidence'
    if positive:return 'applicable'
    if negative:return 'not_applicable'
    return 'insufficient_information'


def _adjacent(row,observations,symbol=None):
    candidates=[o for o in observations if o['id']!=row['id'] and (symbol is None or symbol in [o['symbol_id']]+o.get('alternatives',[]))]
    states=[]
    for other in candidates:
        state=_relation(row,other)
        if state=='applicable' and _identity_uncertain(other):state='conflicting_evidence'
        states.append(state)
    if 'conflicting_evidence' in states:return 'conflicting_evidence'
    if 'applicable' in states:return 'applicable'
    if states and all(s=='not_applicable' for s in states):return 'not_applicable'
    if not states and 'adjacent_to' in row:return 'not_applicable'
    return 'insufficient_information'


def _condition(key,expected,row,request):
    observations=request.get('observations',[])
    if key=='adjacent_symbol':return _adjacent(row,observations,expected)
    if key=='adjacent_any':
        # This source-specific predicate means surrounding dots,not generic proximity.
        arrangement=row.get('arrangement','unknown')
        if arrangement=='unknown':return 'insufficient_information'
        if arrangement!='surrounding':return 'not_applicable'
        return _adjacent(row,observations)
    if key=='bottom_region':
        regions=[row.get('region','unknown')]+row.get('region_alternatives',[])
        if 'unknown' in regions:return 'insufficient_information'
        yes=[r in BOTTOM for r in regions]
        return 'conflicting_evidence' if any(yes) and not all(yes) else 'applicable' if all(yes) else 'not_applicable'
    if key in ('mark_present','numeral_present'):
        field='mark' if key=='mark_present' else 'numeral';v=row.get(field)
        return 'applicable' if v is not None and (field=='numeral' or v.strip()) else 'insufficient_information'
    actual=request.get('context',{}).get(key[8:]) if key.startswith('context.') else row.get(key)
    if actual is None or actual=='unknown':return 'insufficient_information'
    return 'applicable' if actual==expected else 'not_applicable'


def _conflicts(row,observations):
    result=[]
    if _identity_uncertain(row):result.append('Uncertain or competing manual symbol identities;no identity selected automatically')
    if row.get('motion')=='stationary' and row.get('heading') in ('towards_handle','away_from_handle'):
        result.append('Stationary motion and directional heading remain conflicting declarations')
    if row.get('handle_relation') in ('under_handle','near_handle') and row.get('proximity')=='far':
        result.append('Near/under-handle placement and far proximity remain conflicting declarations')
    if row['symbol_id']=='cross' and row.get('multiplicity')=='single' and any(o['id']!=row['id'] and 'cross' in [o['symbol_id']]+o.get('alternatives',[]) for o in observations):
        result.append('Lone-cross declaration conflicts with another selected cross observation')
    return result


def zones(row):
    records=[]
    for region in [row.get('region','unknown')]+row.get('region_alternatives',[]):
        time=DATA['regions'][region]
        if time:records.append(dict(region=region,association=time,source_id=DATA['source']['id'],locator=DATA['zone_locator']))
    if row.get('handle_relation')=='under_handle':
        records.append(dict(region='under_handle',association='present_immediate',source_id=DATA['source']['id'],locator='ChII:directly beneath handle'))
    competing=len({r['association'] for r in records})>1
    return dict(status='conflicting_evidence' if competing else 'applicable' if records else 'insufficient_information',qualifications=records,
        conflicts=['Coexisting depth/handle timing qualifications;no source priority or exact date inferred'] if competing else [],
        missing=[] if records else ['Declared qualitative region or under-handle relation'],calendar_date=None,
        handle_reference=DATA['handle_reference'],convention=DATA['zone_convention'])


def evaluate(row,request):
    identifier=row['symbol_id'];observations=request.get('observations',[]);conflicts=_conflicts(row,observations)
    if identifier not in SYMBOLS:return dict(id=row['id'],user_record=copy.deepcopy(row),status='unsupported',reference=None,cases=[],zones=zones(row),
        missing=['Verified symbol in named catalog'],conflicts=conflicts,alternative_references=[thaw(SYMBOLS[x]) if x in SYMBOLS else dict(id=x,status='unsupported') for x in row.get('alternatives',[])])
    ref=thaw(SYMBOLS[identifier]);cases=[]
    for case in ref['cases']:
        conditions={k:_condition(k,v,row,request) for k,v in case['requires'].items()}
        if case.get('scope') and request.get('source_example')!=case['scope']:
            intrinsic='unsupported'
        else:
            if case.get('scope')=='figure_viii':
                beetles=[o for o in observations if 'beetle' in [o['symbol_id']]+o.get('alternatives',[])]
                conditions['FigureVIII beetle present']='conflicting_evidence' if any(_identity_uncertain(o) for o in beetles) else 'applicable' if beetles else 'insufficient_information'
            states=list(conditions.values())
            intrinsic='conflicting_evidence' if 'conflicting_evidence' in states else 'not_applicable' if 'not_applicable' in states else 'insufficient_information' if 'insufficient_information' in states else 'applicable'
        status='conflicting_evidence' if conflicts and intrinsic in ('applicable','insufficient_information') else intrinsic
        cases.append(dict(reference=case,status=status,intrinsic_status=intrinsic,condition_results=conditions,
            missing=[k for k,v in conditions.items() if v=='insufficient_information'],rule_id='tasseography.kent.'+identifier+'.'+case['id'],forecast=False))
    states=[c['status'] for c in cases];zone=zones(row)
    status='conflicting_evidence' if conflicts or 'conflicting_evidence' in states or zone['conflicts'] else 'applicable' if 'applicable' in states else 'insufficient_information' if 'insufficient_information' in states else 'not_applicable' if 'not_applicable' in states else 'unsupported'
    return dict(id=row['id'],user_record=copy.deepcopy(row),status=status,reference=ref,cases=cases,zones=zone,
        missing=sorted({m for c in cases for m in c['missing']}),conflicts=conflicts+zone['conflicts'],
        alternative_references=[thaw(SYMBOLS[x]) if x in SYMBOLS else dict(id=x,status='unsupported') for x in row.get('alternatives',[])],
        alternatives_scope='Source organ alternatives are retained without selecting wedding/death/ambition from unspecified surrounding signs',
        observed_quantity=row.get('numeral'),qualifiers=thaw(DATA['general_qualifiers']))


def _documentary(request):
    if request.get('source_example')!='figure_viii':return None
    observations=request.get('observations',[]);expected=thaw(DATA['source_example']);checks=[]
    for e in expected['placements']:
        rows=[o for o in observations if o['symbol_id']==e['symbol_id']]
        def matches(o):
            if _identity_uncertain(o):return False
            if any(k not in ('symbol_id','beside') and v!='unknown' and o.get(k)!=v for k,v in e.items()):return False
            if e.get('region')!='unknown' and o.get('region_alternatives'):return False
            if 'beside' in e:
                return any(target['symbol_id']==e['beside'] and not _identity_uncertain(target) and _relation(o,target)=='applicable' for target in observations)
            return True
        match=any(matches(o) for o in rows)
        checks.append(dict(expected=e,status='declared_fields_match' if match else 'missing_or_different',original_shape_recognition=False))
    organs=[o for o in observations if o['symbol_id']=='organ'];acorns=[o for o in observations if o['symbol_id']=='acorn']
    pairs=[]
    for organ in organs:
        for acorn in acorns:
            state=_relation(organ,acorn)
            if state=='applicable' and (_identity_uncertain(organ) or _identity_uncertain(acorn)):state='conflicting_evidence'
            if state=='applicable':
                region_states=[]
                for o in (organ,acorn):
                    regions=[o.get('region','unknown')]+o.get('region_alternatives',[])
                    region_states.append('insufficient_information' if 'unknown' in regions else 'conflicting_evidence' if 'bottom_circle' in regions and any(r!='bottom_circle' for r in regions) else 'not_applicable' if any(r!='bottom_circle' for r in regions) else 'applicable')
                state='conflicting_evidence' if 'conflicting_evidence' in region_states else 'not_applicable' if 'not_applicable' in region_states else 'insufficient_information' if 'insufficient_information' in region_states else 'applicable'
            pairs.append(state)
    pair='conflicting_evidence' if 'conflicting_evidence' in pairs else 'applicable' if 'applicable' in pairs else 'insufficient_information' if not pairs or 'insufficient_information' in pairs else 'not_applicable'
    musician=request.get('context',{}).get('musician')
    music=pair if pair!='applicable' else 'applicable' if musician is True else 'not_applicable' if musician is False else 'insufficient_information'
    cosy=next((o for o in observations if o['symbol_id']=='tea_cosy' and o.get('region')=='bottom_centre'),None)
    cosy_status='insufficient_information' if cosy is None else 'conflicting_evidence' if _identity_uncertain(cosy) or cosy.get('region_alternatives') else 'applicable'
    return dict(coverage='explicit_documentary_comparison',reference=expected,placement_checks=checks,
        cases=[dict(reference=thaw(DATA['documentary_cases'][j])|dict(source_id=DATA['source']['id'],locator=DATA['source_example']['locator']),
                    rule_id='tasseography.kent.figure_viii.'+DATA['documentary_cases'][j]['id'],status=s) for j,s in enumerate((pair,music,cosy_status))],
        adjacency_convention='Original beside-organ placement is checked through explicit user adjacency;not inferred from circle membership.',
        assurance='Source example account compared with user declarations,not a newly published historical cup or verified fortune. Dictionary contexts remain separate.')


def register_knowledge(registry):
    registry.add_source(thaw(DATA['source']))
    for key,item in SYMBOLS.items():
        for case in item['cases']:
            registry.add_rule(Rule('tasseography.kent.'+key+'.'+case['id'],2,28,'British tea-leaf reading',PROFILE,case['source_id'],case['locator'],case['statement'],
                'kent_manual_symbol_condition',thaw(case['requires']),'proposed','traditional',[]))


def read(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    results=[evaluate(o,request) for o in request.get('observations',[])]
    statuses=('applicable','not_applicable','insufficient_information','conflicting_evidence','unsupported')
    counts={s:sum(r['status']==s for r in results) for s in statuses}
    synthesis=[]
    for r in results:
        meanings=[c['reference']['statement'] for c in r['cases'] if c['status']=='applicable']
        synthesis.append(dict(observation_id=r['id'],evidence='editorial_composition_of_source_and_user_declarations',
            source_accounts=meanings,time_qualifications=[z['association'] for z in r['zones']['qualifications']],
            unresolved=r['missing']+r['conflicts']+r['zones']['missing'],
            note='Historically attributed accounts under declared conditions;not an actual event prediction.'))
    return dict(schema_version=1,technique_id=28,profile=PROFILE,task='symbolic_cup_reading',mode='manual',vessel='cup',
        source=thaw(DATA['source']),layout=dict(handle_orientation=request.get('handle_orientation','unknown'),geometry=False,position_inferred=False,
            ordering='Input order retained',vessel_method='Ordinary Kent cup only',context=copy.deepcopy(request.get('context',{}))),
        observations=results,editorial_synthesis=synthesis,summary=dict(observations=len(results),counts=counts,
            text='Each source account is evaluated against explicit manual conditions. Depth and handle timing remain separate;missing or competing evidence is not repaired.'),
        documentary_comparison=_documentary(request),documentary_method_limits=dict(saucer=thaw(DATA['documentary_saucer']),nelros='Separate marked-cup method;unsupported here'),
        user_notes=request.get('notes'),provenance_matrix=dict(direct='Selected Kent source statements,zones,conditions and documentary accounts',
            user_attributed='Manual identities,positions,relations,uncertainty,observations,associations and optional context',editorial='Structured predicates,adjacency bookkeeping,comparisons and synthesis;not general symbol grammar',
            unsupported='Objective future outcomes,clinical/personality conclusions,photo/shape recognition or physical leaf simulation'),
        conventions=thaw(DATA['editorial_conventions'])+['Surrounding-dots predicate requires declared surrounding arrangement plus an associated symbol;generic adjacency alone does not suffice.'],
        limitations=thaw(DATA['unsupported'])+['Qualitative timing only;no dates,probabilities or deadlines computed.','Source fidelity is not independent predictive validation.'],
        replay=dict(request=request,input_sha256=digest(request),profile_sha256=PROFILE_HASH,source_sha256=DATA['source']['snapshot_sha256'],
            serialization='Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw content line endings retained',external_calls=False,rng=False,generated_placements=False))


def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2);fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Tasseography historical symbolic cup report','','Profile: '+PROFILE,'',html.escape(result['source']['edition']),
           '', '['+result['source']['id']+']('+result['source']['url']+')','',html.escape(result['source']['rights_note']),
           '', '## Declared vessel and layout','',block(result['layout']),'','## Ordered manual placements']
    for row in result['observations']:
        lines+=['','### '+html.escape(row['id'])+' — '+row['status'],'',block(row)]
    for title,key in [('Editorial symbolic synthesis','editorial_synthesis'),('Coverage summary','summary'),('Original Kent example comparison','documentary_comparison'),
        ('Separate method limits','documentary_method_limits'),('User notes','user_notes'),('Provenance matrix','provenance_matrix'),('Application conventions','conventions'),('Historical limits','limitations'),('Exact replay metadata','replay')]:
        lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'


def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),tasseography_report=None),indent=2)
    return '# Tasseography request rejected\n\n'+html.escape(str(message))+'\n'
