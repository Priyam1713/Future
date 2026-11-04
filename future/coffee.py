"""Edition-bounded manual Turkish coffee references; no perception or forecasting."""
import copy
import html
import json
from pathlib import Path
import re
from .knowledge import Rule
from .scrying import freeze, thaw, digest, _object, _optional_text, load_input

ROOT = Path(__file__).resolve().parents[1]
DATA = freeze(json.loads((ROOT/'knowledge/coffee_profile_v1.json').read_text(encoding='utf-8')))
PROFILE = DATA['profile']
PROFILE_HASH = digest(thaw(DATA))
SYMBOLS = DATA['symbols']
STATES = ('applicable','not_applicable','insufficient_evidence','conflicting_evidence','unsupported')
UNKNOWN = (None,'unknown','ambiguous')
ATTRIBUTES = {
    'adhered_after_inversion': 'bool', 'stain': 'bool', 'humps': 'humps', 'dots': 'dots',
    'shape': ('flat','curved','moon_shaped','other','unknown','ambiguous'),
    'dot_arrangement': ('at_line_end','scattered','other','unknown','ambiguous'),
    'stain_position': ('peak_of_bird_figure','beak','other','unknown','ambiguous'),
    'color': ('white','dark','other','unknown','ambiguous'),
    'location': ('bottom','side','rim','saucer_surface','other','unknown','ambiguous')}
HALVES = ('subject_facing','opposite','unknown','ambiguous')


def _identifier(v):
    return isinstance(v,str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',v) is not None


def _values(v):
    return v if isinstance(v,list) else [v]


def _validate_choice(v, kind, name):
    values = _values(v)
    if not values or len(values)>4 or len({json.dumps(x,sort_keys=True) for x in values})!=len(values):
        raise ValueError(name+' requires one value or up to four distinct alternatives')
    for x in values:
        if x is None:continue
        if kind=='bool':ok = type(x) is bool
        elif kind in ('dots','humps'):ok = type(x) is int and 0<=x<=(64 if kind=='dots' else 8)
        else:ok = isinstance(x,str) and x in kind
        if not ok:raise ValueError('Unsupported '+name+' evidence')


def validate(value):
    _object(value,['schema_version','profile','task','mode','vessel','rotation','intention','preparation','context','observations','notes','source_example'])
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:
        raise ValueError('schema_version must be integer 1')
    if value.get('profile')!=PROFILE or value.get('task')!='symbolic_coffee_reading' or value.get('mode')!='manual':
        raise ValueError('Exact coffee profile, symbolic_coffee_reading task and manual mode required')
    if value.get('vessel') not in ('cup','saucer'):raise ValueError('Declare cup or saucer')
    for k,choices in [('rotation',('clockwise','counterclockwise','unknown','ambiguous')),('intention',('self','another','unknown','ambiguous'))]:
        if k in value:_validate_choice(value[k],choices,k)
    for k in ('notes','context'):_optional_text(value,k,10000)
    if 'source_example' in value and value['source_example']!='p104_narrative':raise ValueError('Only p104_narrative documentary comparison is available')
    prep=value.get('preparation',{})
    _object(prep,['grounds_remaining','inverted_onto_saucer','cooled','stuck','upright_after_reading'])
    for k,v in prep.items():
        if v is not None and type(v) is not bool:raise ValueError('Preparation declarations must be boolean or null')
    rows=value.get('observations',[])
    if not isinstance(rows,list) or len(rows)>64:raise ValueError('Use up to 64 ordered observations')
    ids=set()
    for row in rows:
        _object(row,['id','symbol_id','alternatives','uncertainty','vessel','half','attributes','observation','association'])
        if not _identifier(row.get('id')) or row['id'] in ids:raise ValueError('Unique plain observation IDs required')
        ids.add(row['id'])
        if not _identifier(row.get('symbol_id')):raise ValueError('Explicit symbol identifier required')
        alt=row.get('alternatives',[])
        if not isinstance(alt,list) or len(alt)>4 or any(not _identifier(x) for x in alt) or len(set(alt))!=len(alt) or row['symbol_id'] in alt:
            raise ValueError('Use up to four distinct alternative symbol IDs')
        if 'uncertainty' in row and type(row['uncertainty']) is not bool:raise ValueError('Uncertainty must be boolean')
        if 'vessel' in row:_validate_choice(row['vessel'],('cup','saucer','unknown','ambiguous'),'vessel')
        if 'half' in row:_validate_choice(row['half'],HALVES,'half')
        attrs=row.get('attributes',{})
        _object(attrs,ATTRIBUTES)
        for k,v in attrs.items():_validate_choice(v,ATTRIBUTES[k],k)
        for k in ('observation','association'):_optional_text(row,k,10000)
    return copy.deepcopy(value)


def _condition(actual, expected):
    vals=_values(actual)
    known=[v for v in vals if v not in UNKNOWN]
    # Booleans and integers have distinct input domains; numeric equality is used only within a field.
    truth=[v==expected for v in known]
    if any(truth) and not all(truth):return 'conflicting_evidence'
    if truth and not any(truth):return 'not_applicable'
    if len(known)!=len(vals) or not known:return 'insufficient_evidence'
    return 'applicable'


def _combine(states):
    for state in ('conflicting_evidence','not_applicable','insufficient_evidence'):
        if state in states:return state
    return 'applicable'


def _half(row,vessel):
    declared=copy.deepcopy(row.get('half','unknown'))
    vals=_values(declared)
    known=[v for v in vals if v not in UNKNOWN]
    vessels=_values(vessel)
    if 'cup' in vessels and 'saucer' in vessels:state='conflicting_evidence'
    elif vessels==['saucer']:state='unsupported'
    elif vessels!=['cup']:state='insufficient_evidence'
    elif len(set(known))>1:state='conflicting_evidence'
    elif not known or len(known)!=len(vals):state='insufficient_evidence'
    else:state='applicable'
    return dict(declared=declared,status=state,source_association=DATA['orientation'][known[0]] if state=='applicable' else None,
        locator=DATA['orientation']['locator'],axis='Subject-facing cup half;no handle or angle inference',calendar_date=None)


def rotation(request):
    direction=request.get('rotation','unknown');intent=request.get('intention','unknown')
    dirs=_values(direction);known=[v for v in dirs if v not in UNKNOWN]
    meanings=[DATA['rotation'][v] for v in known]
    if len(set(meanings))>1:state='conflicting_evidence'
    elif not known or len(known)!=len(dirs):state='insufficient_evidence'
    else:state=_condition(intent,meanings[0])
    return dict(declared_rotation=copy.deepcopy(direction),declared_intention=copy.deepcopy(intent),status=state,
        source_intent=meanings[0] if meanings and len(set(meanings))==1 and len(known)==len(dirs) else None,
        locator=DATA['rotation']['locator'],note='Reported stirring convention compared with declarations;no actual stirring or subject identity inferred. Half orientation is independent.')


def evaluate(row,request):
    vessel=row.get('vessel',request['vessel']);symbol=row['symbol_id']
    attrs=row.get('attributes',{});cases=[]
    for case in SYMBOLS.get(symbol,()):
        checks=[]
        for key,expected in case['requires'].items():
            actual=vessel if key=='vessel' else attrs.get(key)
            checks.append(dict(field=key,expected=expected,declared=copy.deepcopy(actual),status=_condition(actual,expected)))
        state=_combine([c['status'] for c in checks])
        # No source-backed general saucer account for the selected cup-ground motifs.
        if symbol!='moon_patch' and _values(vessel)==['saucer']:state='unsupported'
        if state!='unsupported':
            if row.get('alternatives'):state='conflicting_evidence'
            elif row.get('uncertainty') and state=='applicable':state='insufficient_evidence'
        cases.append(dict(id=case['id'],rule_id='coffee.ayvazoglu2011.'+symbol+'.'+case['id'],status=state,
            reference=thaw(case),conditions=checks,
            timing=thaw(DATA['timing']) if symbol=='line' and state=='applicable' else None))
    states=[c['status'] for c in cases]
    if not states:state='unsupported'
    elif 'conflicting_evidence' in states:state='conflicting_evidence'
    elif 'applicable' in states:state='applicable'
    elif 'insufficient_evidence' in states:state='insufficient_evidence'
    elif all(s=='unsupported' for s in states):state='unsupported'
    else:state='not_applicable'
    unresolved=[dict(case=c['id'],field=x['field'],status=x['status']) for c in cases for x in c['conditions'] if x['status'] in ('insufficient_evidence','conflicting_evidence')]
    if row.get('alternatives'):unresolved.append(dict(field='symbol_identity',status='conflicting_evidence'))
    if row.get('uncertainty'):unresolved.append(dict(field='user_uncertainty',status='insufficient_evidence'))
    return dict(id=row['id'],symbol_id=symbol,status=state,declared=copy.deepcopy(row),effective_vessel=copy.deepcopy(vessel),
        orientation=_half(row,vessel),cases=cases,unresolved=unresolved,
        note='A nonmatching case is not a negative forecast;unknown symbols have no invented source meaning.')


def register_knowledge(registry):
    for k in ('source','preparation_source'):registry.add_source(thaw(DATA[k]))
    for key,cases in SYMBOLS.items():
        for c in cases:
            registry.add_rule(Rule('coffee.ayvazoglu2011.'+key+'.'+c['id'],1,29,'Turkish kahve falı',PROFILE,
                c['source_id'],c['locator'],c['statement'],'coffee_manual_condition',thaw(c['requires']),'proposed','traditional',[]))


def read(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    results=[evaluate(row,request) for row in request.get('observations',[])]
    synthesis=[dict(observation_id=r['id'],evidence='editorial',
        attributed_accounts=[c['reference']['statement'] for c in r['cases'] if c['status']=='applicable'],
        source_half_association=r['orientation']['source_association'],
        timing_alternatives=[c['timing'] for c in r['cases'] if c['timing']],unresolved=r['unresolved'],
        note='Conditional historical comparison,not a factual future outcome or hidden personal information.') for r in results]
    return dict(schema_version=1,technique_id=29,profile=PROFILE,task='symbolic_coffee_reading',mode='manual',
        source=thaw(DATA['source']),edition=thaw(DATA['source_edition']),
        preparation=dict(references=thaw(DATA['procedures']),separate_official_webpage=thaw(DATA['preparation_source']),
            note=DATA['preparation_note'],declared=copy.deepcopy(request.get('preparation',{})),physically_verified=False),
        layout=dict(vessel=request['vessel'],rotation=rotation(request),orientation_axis='Subject-facing half,independent of handle and rotation',ordering='Input order',geometry_inferred=False),
        observations=results,editorial_synthesis=synthesis,
        summary=dict(observations=len(results),counts={s:sum(r['status']==s for r in results) for s in STATES}),
        documentary_comparison=dict(requested=request.get('source_example')=='p104_narrative',locator='ChXIV,printed p104,first paragraph',
            comparison=[dict(id=r['id'],cases=[dict(id=c['id'],status=c['status']) for c in r['cases']]) for r in results] if request.get('source_example') else [],
            assurance='Selected author narrative examples,not one worked historical cup,experimental validation or recognized source image.'),
        user_notes=request.get('notes'),user_context=request.get('context'),
        provenance_matrix=dict(direct='Source-located historical coffee accounts and cultural procedures',user_attributed='Manual identities,features,vessels,halves,intent,uncertainty,raw notes and associations',
            editorial='Condition comparisons,unknown/conflict bookkeeping and neutral symbolic synthesis',unsupported='Factual future predictions,hidden knowledge,clinical/personality inference,spirit identification or verified paranormal capabilities'),
        conventions=thaw(DATA['editorial_conventions']),limitations=thaw(DATA['unsupported'])+['No prediction confidence,selected time unit,calendar deadline or empirical predictive certification.'],
        replay=dict(request=request,input_sha256=digest(request),profile_sha256=PROFILE_HASH,source_sha256=DATA['source']['snapshot_sha256'],
            serialization='Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw content line endings retained',external_calls=False,rng=False,generated_placements=False))


def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2)
        fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Coffee historical symbolic reading','','Profile: '+PROFILE,'',html.escape(result['source']['edition']),'',
        '['+result['source']['id']+']('+result['source']['url']+')','',html.escape(result['source']['rights_note'])]
    for title,key in [('Coffee preparation references and declarations','preparation'),('Declared vessels and orientation','layout'),('Ordered manual motifs and conditions','observations'),
        ('Editorial symbolic synthesis','editorial_synthesis'),('Coverage summary','summary'),('Documentary narrative comparison','documentary_comparison'),('User notes','user_notes'),('User context','user_context'),
        ('Evidence layers','provenance_matrix'),('Application conventions','conventions'),('Limits','limitations'),('Exact replay metadata','replay')]:
        lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'


def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),coffee_report=None),indent=2)
    return '# Coffee request rejected\n\n'+html.escape(str(message))+'\n'
