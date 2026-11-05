"""Edition-bounded atmospheric lore comparison; no weather inference or forecast."""
import copy,html,json,re
from pathlib import Path
from .knowledge import Rule
from .scrying import freeze,thaw,digest,_object,_optional_text,_timestamp,load_input

ROOT=Path(__file__).resolve().parents[1]
DATA=freeze(json.loads((ROOT/'knowledge/aeromancy_profile_v1.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile'];PROFILE_HASH=digest(thaw(DATA));CASES=DATA['cases']
STATES=('applicable','not_applicable','insufficient_evidence','conflicting_evidence','unsupported')
UNKNOWN=(None,'unknown','ambiguous')
REGIONS=('scotland','bedfordshire','texas','other','unknown','ambiguous')
DIRECTIONS=('north','north_east','east','south_east','south','south_west','west','north_west','other','unknown','ambiguous')
ORIGINS=('reported_real','hypothetical','synthetic','unknown')
FEATURES=dict(named_wind_direction=DIRECTIONS,wind_direction_convention=('from','unknown','ambiguous'),wind_strength=('light','moderate','strong','other','unknown','ambiguous'),
 wind_continuity=('considerable_time','brief','other','unknown','ambiguous'),prior_wind_direction=DIRECTIONS,prior_wind_strength=('light','moderate','strong','other','unknown','ambiguous'),
 dry_weather='bool',light_wind_duration_days='days',smoke_drift_towards=DIRECTIONS,cloud_appearance=('hake_shaped','fleecy','other','unknown','ambiguous'),
 cloud_axis=('east_west','north_south','other','unknown','ambiguous'),cloud_motion=('rapid','slow','stationary','other','unknown','ambiguous'),
 cloud_light='bool',relative_cloud_layer=('below','above','same_level','unknown','ambiguous'),upper_cloud_type=('cirro_stratus','other','unknown','ambiguous'),
 upper_cloud_dark='bool',upper_cloud_compact='bool',mackerel_sky='bool',mares_tails='bool')


def _vals(v):return v if isinstance(v,list) else [v]
def _id(v):return isinstance(v,str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',v) is not None


def _choice(v,allowed,name):
 vals=_vals(v)
 if not vals or len(vals)>4:raise ValueError(name+' requires one value or up to four alternatives')
 for x in vals:
  if x is None:continue
  valid=type(x) is bool if allowed=='bool' else type(x) is int and 0<=x<=1000000 if allowed=='days' else isinstance(x,str) and x in allowed
  if not valid:raise ValueError('Invalid '+name+' evidence')
 if len(set(json.dumps(x) for x in vals))!=len(vals):raise ValueError('Duplicate '+name+' alternatives')


def validate(value):
 _object(value,['schema_version','profile','task','mode','origin','region','timestamp','observations','notes','include_reference_catalog'])
 if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer 1')
 if value.get('profile')!=PROFILE or value.get('task')!='atmospheric_lore_comparison' or value.get('mode')!='manual':raise ValueError('Exact Inwards profile,atmospheric_lore_comparison task and manual mode required')
 if value.get('origin','unknown') not in ORIGINS:raise ValueError('Unsupported observation origin')
 if 'region' in value:_choice(value['region'],REGIONS,'region')
 _timestamp(value.get('timestamp'));_optional_text(value,'notes',10000)
 if 'include_reference_catalog' in value and type(value['include_reference_catalog']) is not bool:raise ValueError('include_reference_catalog must be boolean')
 rows=value.get('observations',[])
 if not isinstance(rows,list) or len(rows)>64:raise ValueError('Use up to 64 ordered observations')
 ids=set();last=0
 for row in rows:
  _object(row,['id','sequence','phenomenon','origin','region','timestamp','features','alternatives','uncertainty','description','association'])
  if not _id(row.get('id')) or row['id'] in ids:raise ValueError('Unique plain observation IDs required')
  ids.add(row['id'])
  if row.get('phenomenon') not in ('smoke','wind','cloud','other','unknown'):raise ValueError('Explicit phenomenon required')
  if row.get('origin','unknown') not in ORIGINS:raise ValueError('Unsupported origin')
  if 'sequence' in row:
   n=row['sequence']
   if type(n) is not int or not last<n<=1000000:raise ValueError('Explicit sequence must strictly increase')
   last=n
  if 'region' in row:_choice(row['region'],REGIONS,'region')
  _timestamp(row.get('timestamp'))
  features=row.get('features',{});_object(features,FEATURES)
  for k,v in features.items():_choice(v,FEATURES[k],k)
  alternatives=row.get('alternatives',[])
  if not isinstance(alternatives,list) or len(alternatives)>4 or any(not _id(x) for x in alternatives) or len(set(alternatives))!=len(alternatives):raise ValueError('Distinct bounded alternative identification labels required')
  if 'uncertainty' in row and type(row['uncertainty']) is not bool:raise ValueError('Uncertainty must be boolean')
  for k in ('description','association'):_optional_text(row,k,10000)
 return copy.deepcopy(value)


def condition(actual,expected):
 vals=_vals(actual);known=[v for v in vals if v not in UNKNOWN];allowed=_vals(expected);match=[v in allowed for v in known]
 if any(match) and not all(match):return 'conflicting_evidence'
 if match and not any(match):return 'not_applicable'
 if not known or len(known)!=len(vals):return 'insufficient_evidence'
 return 'applicable'


def combine(states):
 for state in ('conflicting_evidence','not_applicable','insufficient_evidence'):
  if state in states:return state
 return 'applicable'


def regional(source_region,declared):
 return dict(source_region=source_region,declared=copy.deepcopy(declared),status='source_unspecified' if source_region is None else condition(declared,source_region),
  qualification='Region is a user declaration;unspecified source origin is not worldwide applicability. No location is inferred.')


def evaluate(row,request):
 region=row.get('region',request.get('region','unknown'));features=row.get('features',{});results=[]
 for c in CASES:
  if c['phenomenon']!=row['phenomenon']:continue
  checks=[dict(field=k,expected=thaw(v),declared=copy.deepcopy(features.get(k)),status=condition(features.get(k),thaw(v))) for k,v in c['requires'].items()]
  observational=combine([x['status'] for x in checks])
  if row.get('alternatives'):observational='conflicting_evidence'
  elif row.get('uncertainty') and observational=='applicable':observational='insufficient_evidence'
  reg=regional(c['source_region'],region)
  status=combine([observational,reg['status']]) if reg['status']!='source_unspecified' else observational
  results.append(dict(id=c['case'],rule_id=c['id'],status=status,observational_status=observational,regional_context=reg,
   conditions=checks,missing=[x['field'] for x in checks if x['status']=='insufficient_evidence'],conflicts=[x['field'] for x in checks if x['status']=='conflicting_evidence'],
   reference=thaw(c),retrieved_by_observations=observational=='applicable',empirical_validity='not_established',calendar_forecast=None))
 states=[c['status'] for c in results]
 status='unsupported' if not states else 'conflicting_evidence' if 'conflicting_evidence' in states else 'applicable' if 'applicable' in states else 'insufficient_evidence' if 'insufficient_evidence' in states else 'not_applicable'
 retrieved=[c for c in results if c['retrieved_by_observations']]
 accounts=[dict(case=c['id'],attribution=c['reference']['attribution'],historical_statement=c['reference']['statement'],source_horizon=c['reference']['horizon'],regional_status=c['regional_context']['status'],overall_status=c['status'],locator=c['reference']['locator'],empirical_validity='not_established') for c in retrieved]
 return dict(id=row['id'],origin=row.get('origin',request.get('origin','unknown')),declared=copy.deepcopy(row),region=copy.deepcopy(region),status=status,cases=results,historical_accounts=accounts,
  competing_accounts=[c['id'] for c in retrieved if c['reference']['comparison_group']=='mackerel_accounts'],
  comparison_policy='Accounts are an attributed ordered set. Different horizons may coexist;disagreement is not resolved by a vote,priority orsingle forecast.',
  identification_uncertainty=bool(row.get('uncertainty') or row.get('alternatives')))


def register_knowledge(registry):
 for key in ('source','direction_source'):registry.add_source(thaw(DATA[key]))
 for c in CASES:registry.add_rule(Rule(c['id'],1,32,'Historical atmospheric lore',PROFILE,c['source_id'],c['locator'],c['statement'],'aeromancy_manual_condition',dict(features=thaw(c['requires']),source_region=c['source_region']),'proposed','traditional',[]))


def read(value,registry=None):
 q=validate(value)
 if registry is not None:register_knowledge(registry)
 rows=[evaluate(o,q) for o in q.get('observations',[])]
 return dict(schema_version=1,technique_id=32,profile=PROFILE,task='atmospheric_lore_comparison',mode='manual',source=thaw(DATA['source']),edition_limits=DATA['edition_limits'],source_context=thaw(DATA['source_context']),
  declared_context=dict(origin=q.get('origin','unknown'),region=copy.deepcopy(q.get('region','unknown')),timestamp=q.get('timestamp'),location_inferred=False,weather_observed_by_engine=False),
  direction_conventions=thaw(DATA['direction_conventions']),direction_reference=thaw(DATA['direction_source']),observations=rows,
  summary=dict(observations=len(rows),counts={s:sum(r['status']==s for r in rows) for s in STATES}),
  editorial_synthesis=[dict(observation_id=r['id'],retrieved_accounts=r['historical_accounts'],region=r['region'],competing_accounts=r['competing_accounts'],note='Observational retrieval,regional applicability andempirical validity are distinct. No present weather orforecast has been established.') for r in rows],
  reference_catalog=thaw(CASES) if q.get('include_reference_catalog') else None,user_notes=q.get('notes'),
  provenance_matrix=dict(direct='Edition-located compiled historical sayings with individual/regional attribution',user_attributed='Ordered manual phenomena,features,direction categories,region,time,uncertainty andraw text',editorial='Transparent condition matching,separate regional qualifications andcomparison of source accounts',unsupported='Actual weather/forecast,empirical accuracy,maritime orhazard guidance,spirit/personality/future-life conclusions'),
  conventions=thaw(DATA['editorial_conventions']),limitations=thaw(DATA['unsupported']),non_forecast='Historical reference only. No weather API,live observation,forecast,probability ornavigation/safety recommendation.',
  replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,source_sha256=DATA['source']['snapshot_sha256'],serialization='Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw field line endings retained',external_calls=False,rng=False,generated_observations=False))


def markdown(result):
 def block(obj):
  text=json.dumps(obj,ensure_ascii=False,indent=2);fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
  return fence+'json\n'+text+'\n'+fence
 lines=['# Aeromancy historical atmospheric-lore comparison','','Profile: '+PROFILE,'',html.escape(result['non_forecast'])]
 for title,key in [('Source edition andrights','source'),('Edition boundary','edition_limits'),('Compiler context','source_context'),('Declared observation context','declared_context'),('Independent direction concepts','direction_conventions'),('Direction convention reference','direction_reference'),('Ordered observations andconditions','observations'),('Historical comparison','editorial_synthesis'),('Coverage summary','summary'),('Requested source catalog','reference_catalog'),('User notes','user_notes'),('Evidence layers','provenance_matrix'),('Application conventions','conventions'),('Limits','limitations'),('Exact replay metadata','replay')]:lines+=['','## '+title,'',block(result[key])]
 return '\n'.join(lines)+'\n'


def rejection(message,fmt):
 if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),aeromancy_report=None),indent=2)
 return '# Aeromancy request rejected\n\n'+html.escape(str(message))+'\n'
