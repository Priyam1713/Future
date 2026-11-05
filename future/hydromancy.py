"""Water-specific manual reference conditions;no perception or physical inference."""
import copy,html,json,re
from pathlib import Path
from .knowledge import Rule
from .scrying import freeze,thaw,digest,_object,_optional_text,_timestamp,load_input

ROOT=Path(__file__).resolve().parents[1]
DATA=freeze(json.loads((ROOT/'knowledge/hydromancy_profile_v1.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile'];PROFILE_HASH=digest(thaw(DATA));RULES=DATA['rules']
STATES=('source_supported','context_mismatch','insufficient_information','conflicting_evidence','unsupported')
UNKNOWN=(None,'unknown','ambiguous')
CONTEXT={
 'medium':('water','oil_on_water','oil_only','other','unknown','ambiguous'),
 'container':('dark_bowl','cauldron','natural_pool','other','unknown','ambiguous'),
 'rainwater':'bool','observer_undisturbed':'bool','surface_visible':'bool','relaxed':'bool',
 'gaze':('soft','half_focused','intense','other','unknown','ambiguous'),
 'surface_motion':('still','ripples','moving','unknown','ambiguous'),
 'reflection':('visible','glare','none','unknown','ambiguous')}
CATEGORIES=('physical_ripples','reflection','glare','physical_mist','perceived_fogginess','subjective_image','imagined_image','no_imagery','oil_layer','oil_drops','unknown')
ORIGINS=('reported_real','hypothetical','synthetic','unknown')


def _vals(v):return v if isinstance(v,list) else [v]
def _id(v):return isinstance(v,str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',v) is not None


def _choice(v,allowed,name):
 vals=_vals(v)
 if not vals or len(vals)>4:raise ValueError(name+' requires one value or up to four alternatives')
 for x in vals:
  if x is None:continue
  if not (type(x) is bool if allowed=='bool' else isinstance(x,str) and x in allowed):raise ValueError('Unsupported '+name)
 if len(set(json.dumps(x) for x in vals))!=len(vals):raise ValueError('Duplicate '+name+' alternatives')


def _context(obj):
 _object(obj,CONTEXT)
 for k,v in obj.items():_choice(v,CONTEXT[k],k)


def validate(value):
 _object(value,['schema_version','profile','task','mode','origin','session','observations','notes','documentary_comparison'])
 if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
 if value.get('profile')!=PROFILE or value.get('task')!='water_observation_reference' or value.get('mode')!='manual':raise ValueError('Exact Andrews/Spees profile,water_observation_reference task andmanual mode required')
 if value.get('origin','unknown') not in ORIGINS:raise ValueError('Unknown origin')
 if 'documentary_comparison' in value and type(value['documentary_comparison']) is not bool:raise ValueError('Documentary comparison must be boolean')
 _optional_text(value,'notes',10000)
 session=value.get('session',{});_object(session,[*CONTEXT,'intention','question','lighting','timestamp','status','discomfort'])
 _context({k:v for k,v in session.items() if k in CONTEXT})
 for k in ('intention','question','lighting'):_optional_text(session,k,10000)
 _timestamp(session.get('timestamp'))
 if session.get('status','unknown') not in ('planned','hypothetical','recorded','discontinued','unknown'):raise ValueError('Invalid session status')
 if 'discomfort' in session and session['discomfort'] is not None and type(session['discomfort']) is not bool:raise ValueError('Discomfort must be boolean ornull')
 rows=value.get('observations',[])
 if not isinstance(rows,list) or len(rows)>64:raise ValueError('Use up to64 ordered observations')
 ids=set();last=0
 for row in rows:
  _object(row,['id','sequence','origin','category','basis','alternatives','uncertainty','context','description','association','discomfort','stopped','color','drop_count'])
  if not _id(row.get('id')) or row['id'] in ids:raise ValueError('Unique plain observation ID required')
  ids.add(row['id']);n=row.get('sequence')
  if type(n) is not int or not last<n<=1000000:raise ValueError('Explicit sequence must strictly increase')
  last=n
  if row.get('category') not in CATEGORIES:raise ValueError('Explicit observation category required;unknown available')
  if row.get('origin','unknown') not in ORIGINS:raise ValueError('Invalid origin')
  if 'basis' in row:_choice(row['basis'],('physical','subjective','imagined','unknown','ambiguous'),'basis')
  alt=row.get('alternatives',[])
  if not isinstance(alt,list) or len(alt)>4 or any(not isinstance(x,str) or x not in CATEGORIES for x in alt) or len(set(alt))!=len(alt) or row['category'] in alt:raise ValueError('Distinct alternative categories required')
  _context(row.get('context',{}))
  for k in ('uncertainty','discomfort','stopped'):
   if k in row and type(row[k]) is not bool:raise ValueError(k+' must be boolean')
  for k in ('description','association'):_optional_text(row,k,10000)
  _optional_text(row,'color',80)
  if 'drop_count' in row and (type(row['drop_count']) is not int or not 0<=row['drop_count']<=1000000):raise ValueError('drop_count must be a bounded nonnegative integer')
 return copy.deepcopy(value)


def condition(actual,expected):
 vals=_vals(actual);known=[v for v in vals if v not in UNKNOWN];allowed=_vals(expected);truth=[v in allowed for v in known]
 if any(truth) and not all(truth):return 'conflicting_evidence'
 if truth and not any(truth):return 'context_mismatch'
 if not known or len(known)!=len(vals):return 'insufficient_information'
 return 'source_supported'


def combine(states):
 for state in ('conflicting_evidence','context_mismatch','insufficient_information'):
  if state in states:return state
 return 'source_supported'


def water_context(context):
 return combine([condition(context.get('medium'),'water'),condition(context.get('rainwater'),True),condition(context.get('container'),['dark_bowl','cauldron','natural_pool'])])


def _evaluate(rule,context,row=None,hold=False):
 checks=[]
 for field,expected in rule['requires'].items():
  if field=='water_context':actual={k:context.get(k) for k in ('medium','container','rainwater')};state=water_context(context)
  else:
   actual=(row or {}).get(field) if field in ('category','basis') else context.get(field)
   state=condition(actual,thaw(expected))
  checks.append(dict(field=field,expected=thaw(expected),declared=copy.deepcopy(actual),status=state))
 state=combine([c['status'] for c in checks])
 if row:
  expected_basis='subjective' if row['category'] in ('perceived_fogginess','subjective_image') else 'imagined' if row['category']=='imagined_image' else 'physical' if row['category'] in ('reflection','glare','physical_mist','physical_ripples','oil_layer','oil_drops') else None
  if row.get('alternatives') or (expected_basis and row.get('basis') is not None and condition(row['basis'],expected_basis) in ('context_mismatch','conflicting_evidence')):state='conflicting_evidence'
  elif row.get('uncertainty') and state=='source_supported':state='insufficient_information'
 return dict(id=rule['case'],rule_id=rule['id'],source_id=rule['source_id'],locator=rule['locator'],status=state,conditions=checks,
  account=rule['statement'] if state=='source_supported' and not hold else None,display_held=hold)


def _context_results(context):return [_evaluate(r,context) for r in RULES if 'category' not in r['requires']]


def register_knowledge(registry):
 for s in DATA['sources']:registry.add_source(thaw(s))
 for r in RULES:registry.add_rule(Rule(r['id'],1,31,'Water-bowl andrain-pool reference',PROFILE,r['source_id'],r['locator'],r['statement'],'hydromancy_manual_reference',thaw(r['requires']),'proposed','traditional',[]))


def read(value,registry=None):
 q=validate(value)
 if registry is not None:register_knowledge(registry)
 session=q.get('session',{});context={k:v for k,v in session.items() if k in CONTEXT}
 held=session.get('status')=='discontinued' or session.get('discomfort') is True or any(o.get('stopped') or o.get('discomfort') for o in q.get('observations',[]))
 rows=[]
 for row in q.get('observations',[]):
  ctx=context|row.get('context',{});cases=[_evaluate(r,ctx,row,held) for r in RULES if r['requires'].get('category')==row['category']]
  expected='subjective' if row['category'] in ('perceived_fogginess','subjective_image') else 'imagined' if row['category']=='imagined_image' else 'physical' if row['category'] not in ('unknown','no_imagery') else None
  conflict=bool(row.get('alternatives')) or bool(expected and condition(row.get('basis'),expected) in ('context_mismatch','conflicting_evidence'))
  status='conflicting_evidence' if conflict else combine([r['status'] for r in cases]) if cases else 'unsupported'
  rows.append(dict(id=row['id'],sequence=row['sequence'],origin=row.get('origin',q.get('origin','unknown')),declared=copy.deepcopy(row),effective_context=copy.deepcopy(ctx),
   status=status,context_evaluation=_context_results(ctx),cases=cases,classification_conflict=conflict,
   unresolved=[dict(case=c['id'],field=x['field'],status=x['status']) for c in cases for x in c['conditions'] if x['status'] in ('insufficient_information','conflicting_evidence')],
   symbolic_mapping='No universal ripple/drop/color/shape meaning',physical_or_extraordinary_cause_verified=False))
 comparison=None
 if q.get('documentary_comparison'):
  comparison=dict(contemporary=dict(source_id=DATA['sources'][0]['id'],date='2005-07-01',attribution=DATA['attribution'],vessels=['rain pool','dark bowl','cauldron'],purpose='Practitioner reflective-water gazing andclaimed impressions',coverage='Selected public excerpt;original book edition not inspected'),
   coptic=thaw(DATA['documentary']),shared='Documented water-vessel imagery only;no equivalence of ritual orcapability',limits='Fragmentary later Coptic inquiry andmodern practitioner guidance remain distinct;no invocations,ancient ritual execution orBetz alignment.')
 return dict(schema_version=1,technique_id=31,profile=PROFILE,task='water_observation_reference',mode='manual',sources=thaw(DATA['sources']),attribution=DATA['attribution'],
  session=copy.deepcopy(session),session_evaluation=_context_results(context),origin=q.get('origin','unknown'),observations=rows,
  continuation=dict(display_held=held,message='Keep a discontinued activity stopped;no imagery orphysical equipment is required.' if held else 'Hypothetical orrecorded observations suffice;no unusual imagery is required.'),
  editorial_reflection=None if held else 'Compare your selected classifications with your own associations;source conformity does not establish an external orfuture event.',
  documentary_reference=thaw(DATA['documentary']),documentary_comparison=comparison,user_notes=q.get('notes'),
  provenance_matrix=dict(direct_source='Verified water-specific practitioner references andseparate Coptic/NOAA documentary facts',user_attributed='Declared medium,vessel,conditions,physical movement,perceptions,imagination andraw associations',editorial='Condition matching,classification/conflict bookkeeping andneutral reflection',unsupported='Spirits,clairvoyance,hidden facts,future events,psychological diagnoses orphysical causes from text'),
  conventions=thaw(DATA['conventions']),limitations=thaw(DATA['unsupported']),
  replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,source_sha256={s['id']:s['snapshot_sha256'] for s in DATA['sources']},serialization='Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw field line endings retained',external_calls=False,rng=False,generated_observations=False))


def markdown(result):
 def block(obj):
  text=json.dumps(obj,ensure_ascii=False,indent=2);fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
  return fence+'json\n'+text+'\n'+fence
 lines=['# Hydromancy water observation/reference report','','Profile: '+PROFILE,'',html.escape(result['attribution']),'',html.escape(result['continuation']['message'])]
 for title,key in [('Sources andrights','sources'),('Declared session','session'),('Water-specific session conditions','session_evaluation'),('Ordered observations','observations'),('Continuation','continuation'),('Editorial reflection','editorial_reflection'),('Historical documentary reference','documentary_reference'),('Requested documentary comparison','documentary_comparison'),('User notes','user_notes'),('Evidence layers','provenance_matrix'),('Application conventions','conventions'),('Limits','limitations'),('Exact replay metadata','replay')]:lines+=['','## '+title,'',block(result[key])]
 return '\n'.join(lines)+'\n'


def rejection(message,fmt):
 if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),hydromancy_report=None),indent=2)
 return '# Hydromancy request rejected\n\n'+html.escape(str(message))+'\n'
