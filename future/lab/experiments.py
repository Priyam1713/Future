"""Versioned local experiment commitments; no new prediction method or tuning."""
import copy,json
from pathlib import Path
from .common import ROOT,REGISTRY_HASH,LabError,IntegrityError,at,bounded_json,digest,fields,identifier,integer,nonempty,obj,profile,rational,sequence,snapshot
from .registry import capability
from .invocation import invoke
def _next_month_end(period):
    from ..ai_predictive_modeling import add_month
    return add_month(period,1)+'-01T00:00:00Z'
def native_guard(p):
    q=p['native_input'];cutoff=at(p['cutoff']);latest=at(p['selection']['frozen_at']);i=p['technique_id']
    if not isinstance(q,dict):raise LabError('Native input object required')
    if i==51:
        if q.get('task') not in ['report','score']:raise LabError('Lab51requires an unresolved report/score request')
        ledger=q['payload']
        for question in ledger['plan']['questions']:
            if at(question['cutoff'])!=cutoff or question['partition']!='test':raise LabError('Native question cutoff/test partition mismatch')
        for action in ledger['actions']:
            if action['kind'] not in ['forecast','update']:raise LabError('Outcome/resolution actions prohibited in forecast input')
            record=action['record']
            if record['outcome_known'] is not False:raise LabError('Native outcome leakage')
            for value in [action['at'],record['recorded_at'],record['knowledge_at']]:
                t=at(value)
                if t>cutoff:raise LabError('Native forecast revision after cutoff')
                latest=max(latest,t)
        if p['selection']['model_id']!='native_forecast_versions':raise LabError('Frozen51model identity mismatch')
    elif i==57:
        for question in q['questions']:
            d=question['definition'];r=question['resolution']
            if at(d['cutoff'])!=cutoff or d['partition']!='test':raise LabError('Native question cutoff/test partition mismatch')
            if r['status']!='unresolved' or any(r[k] is not None for k in ['outcome','event_at','outcome_known_at','resolved_at']):raise LabError('Outcome labels prohibited in native pool input')
        if any(at(q['pool'][key])>at(p['selection']['frozen_at']) for key in ['frozen_at','weights_available_at']):raise LabError('Pool weights not available at model-selection freeze')
        for f in q['forecasts']:
            for value in [f['issued_at'],f['knowledge_at']]:
                t=at(value)
                if t>cutoff:raise LabError('Native forecast revision after cutoff')
                latest=max(latest,t)
        if p['selection']['model_id']!='precommitted_linear_pool':raise LabError('Frozen57model identity mismatch')
    elif i==49:
        if q.get('task')!='forecast':raise LabError('Only49forecast admitted; retrospective benchmark has a separate reference operation')
        if p['selection']['model_id']!=q['model']:raise LabError('Model-selection/native model mismatch')
        dataset=q['dataset']
        if dataset['id']!=p['dataset']['id'] or dataset['version']!=p['dataset']['version'] or dataset['units']!=p['target_unit']:raise LabError('Native dataset identity/version/units mismatch')
        if p['dataset']['source_vintage']['status']!='declared_as_of':raise LabError('Custom49forecast requires a declared information vintage')
        if at(_next_month_end(q['origin']))>cutoff:raise LabError('Monthly history not complete by forecast cutoff')
        for series in dataset['series']:
            if series['availability']['status']!='declared_as_of':raise LabError('Native series availability must be declared_as_of')
            if any(row['period']>q['origin'] and row['value'] is not None for row in series['observations']):raise LabError('Future target values prohibited in native49forecast input')
        if dataset['provenance']['rights']!=p['dataset']['rights'] or dataset['provenance']['snapshot_sha256']!=p['dataset']['snapshot_sha256']:raise LabError('Native dataset rights/source commitment mismatch')
    else:raise LabError('Technique is not admitted to Lab v1 experiment evaluation')
    return latest
def validate_plan(p):
    bounded_json(p);fields(p,'plan');integer(p['schema_version'],1,1);identifier(p['id']);integer(p['version'],1,1000)
    if p['mode'] not in ['synthetic','retrospective']:raise LabError('Explicit synthetic/retrospective research mode required')
    entry=capability(p['technique_id'])
    if not entry['evaluation']['lab_v1_supported']:raise LabError('Selected technique is not an admitted Lab predictor')
    if p['registry_sha256']!=REGISTRY_HASH or p['profile_identifiers']!=entry['profile_identifiers']:raise IntegrityError('Experiment registry/profile identity mismatch')
    if p['operation'] not in [o['command'] for o in entry['operations']]:raise LabError('Experiment operation mismatch')
    q=p['native_input']
    if not isinstance(q,dict):raise LabError('Native input object required')
    if p['technique_id']==49:
        if q.get('profile')!=entry['profile_identifiers'] or type(q.get('profile_version')) is not int or q['profile_version']!=1:raise IntegrityError('Native experiment profile mismatch')
    else:
        native_profile=q.get('profile',{})
        if not isinstance(native_profile,dict) or native_profile.get('id')!=entry['profile_identifiers'] or native_profile.get('sha256')!=entry['profile_sha256'] or native_profile.get('catalog_sha256')!=entry['sources'][0]['sha256']:raise IntegrityError('Native experiment profile/source hash mismatch')
    policy=profile()
    if p['metric'] not in policy['metrics'][str(p['technique_id'])] or p['baseline'] not in policy['baselines'][str(p['technique_id'])]:raise LabError('Unsupported technique/metric/baseline combination')
    nonempty(p['target_definition']);nonempty(p['target_unit'],200)
    if p['technique_id']!=49 and p['target_unit']!='binary_event':raise LabError('Binary event unit required')
    if p['version']==1 and p['parent_ledger_sha256'] is not None or p['version']>1 and (not isinstance(p['parent_ledger_sha256'],str) or len(p['parent_ledger_sha256'])!=64 or any(c not in '0123456789abcdef' for c in p['parent_ledger_sha256'])):raise IntegrityError('Experiment version parent commitment invalid')
    d=p['dataset'];fields(d,'dataset');identifier(d['id']);integer(d['version'],1,1000000);snapshot(d);v=d['source_vintage'];fields(v,'vintage');nonempty(v['notes'])
    if v['status'] not in ['unknown','declared_as_of'] or at(v['retrieved_at'])>at(d['available_at']):raise LabError('Dataset vintage/availability chronology mismatch')
    if p['mode']=='synthetic' and d['rights']!='self_authored':raise LabError('Synthetic experiment requires self-authored dataset')
    s=p['selection'];fields(s,'selection');nonempty(s['model_id'],128)
    if s['native_input_sha256']!=digest(p['native_input']):raise IntegrityError('Frozen native input hash mismatch')
    created,frozen,cutoff=at(p['created_at']),at(s['frozen_at']),at(p['cutoff'])
    if not created<=frozen<=cutoff or at(d['available_at'])>frozen:raise LabError('Selection/dataset availability after cutoff or before creation')
    splits=sequence(p['splits'],2048);by={};groups={}
    for row in splits:
        fields(row,'split');identifier(row['id']);identifier(row['group'])
        if row['id'] in by or row['partition'] not in ['train','validation','test']:raise LabError('Unique split identities and explicit partitions required')
        if row['group'] in groups and groups[row['group']]!=row['partition']:raise LabError('Dependency group crosses training/validation/test partitions')
        groups[row['group']]=row['partition'];by[row['id']]=row
        if row['partition']!='test' and at(row['available_at'])>frozen:raise LabError('Training/validation information unavailable at frozen selection')
        at(row['available_at'])
    for partition,key in [('train','training_ids'),('validation','validation_ids')]:
        ids=sequence(s[key],2048)
        if len(ids)!=len(set(ids)) or set(ids)!={k for k,x in by.items() if x['partition']==partition}:raise LabError('Frozen selection/split membership mismatch')
    targets=sequence(p['targets'],256)
    if not targets:raise LabError('At least one declared target required')
    seen=set();keys=set();events=set()
    for t in targets:
        fields(t,'target')
        for key in ['id','event_id','dependency_group']:identifier(t[key])
        nonempty(t['native_key'],256)
        if t['id'] in seen or t['native_key'] in keys or t['event_id'] in events:raise LabError('Duplicate target/native-key/event identity')
        seen.add(t['id']);keys.add(t['native_key']);events.add(t['event_id'])
        if t['id'] not in by or by[t['id']]['partition']!='test' or by[t['id']]['group']!=t['dependency_group']:raise LabError('Target must map to its frozen TEST split and group')
        if at(t['target_at'])<cutoff:raise LabError('Target observation precedes forecast cutoff')
    if seen!={k for k,row in by.items() if row['partition']=='test'}:raise LabError('Every TEST identity must have a declared target')
    return native_guard(p)
def _extract(p,native):
    i=p['technique_id'];q=p['native_input'];pred={};bases={};metadata={}
    if i==51:
        questions={x['id']:x for x in q['payload']['plan']['questions']}
        for row in native['result']['evaluation']['rows']:
            key=row['forecast_id'];d=questions[row['question_id']];pred[key]=row['probability']['exact'];bases[key]=row['baseline_probability'] if p['baseline']=='native_reference' else '1/2';metadata[key]=(row['event_id'],row['dependency_group'],d['window_end'])
    elif i==57:
        definitions={x['definition']['id']:x['definition'] for x in q['questions']}
        for key,row in native['questions'].items():
            d=definitions[key];pred[key]=row['probability'];bases[key]='1/2';metadata[key]=(d['event_id'],d['dependency_group'],d['event_end'])
    else:
        baseline=copy.deepcopy(q);baseline['model']='naive' if p['baseline']=='naive' else 'seasonal_naive_m12';br=invoke(dict(technique_id=49,operation=p['operation'],input=baseline))
        if br['native_error'] is not None:raise LabError('Native baseline rejected: '+br['native_error']['message'])
        for row in br['native_output']['result']['cells']:bases[row['series_id']+':'+row['target_period']]=row['prediction']['exact']
        for row in native['result']['cells']:
            key=row['series_id']+':'+row['target_period'];pred[key]=row['prediction']['exact'];metadata[key]=(key.replace(':','--'),row['series_id'],_next_month_end(row['target_period']))
    if set(pred)!={t['native_key'] for t in p['targets']}:raise LabError('Declared target/native forecast coverage mismatch')
    predictions={};baseline_predictions={}
    for t in p['targets']:
        key=t['native_key']
        if metadata[key]!=(t['event_id'],t['dependency_group'],t['target_at']):raise LabError('Native target/event/group/time identity mismatch')
        predictions[t['id']]=pred[key];baseline_predictions[t['id']]=bases[key]
        for x in [pred[key],bases[key]]:
            if x is not None:
                v=rational(x)
                if i!=49 and not 0<=v<=1:raise LabError('Native probability outside[0,1]')
    return predictions,baseline_predictions
def _forecast_record(p):
    result=invoke(dict(technique_id=p['technique_id'],operation=p['operation'],input=p['native_input']))
    if result['native_error'] is not None or result['native_exit_code']!=0:raise LabError('Native forecast rejected: '+str(result['native_error']))
    pred,base=_extract(p,result['native_output'])
    return dict(version=1,native_input_sha256=digest(p['native_input']),native_output=result['native_output'],native_output_sha256=result['native_output_sha256'],predictions=pred,baseline_predictions=base,execution_provenance={k:result[k] for k in ['registry_sha256','core_sha256','request_sha256','adapter','provenance','lab_profile_sha256','lab_code_sha256']})
def _outcome(p,record,when):
    fields(record,'outcome');integer(record['version'],1,1);identifier(record['target_id']);identifier(record['event_id']);nonempty(record['reason']);e=record['evidence'];fields(e,'evidence');identifier(e['id']);snapshot(e)
    if p['mode']=='synthetic' and e['rights']!='self_authored':raise LabError('Synthetic outcome evidence requires self-authored rights')
    target=next((t for t in p['targets'] if t['id']==record['target_id']),None)
    if target is None or record['event_id']!=target['event_id']:raise LabError('Outcome target/event identity mismatch')
    if when<at(p['cutoff']) or at(e['available_at'])>when:raise LabError('Outcome/evidence unavailable at recording time')
    if record['status']=='resolved':
        known=at(record['known_at']);value=rational(record['value'])
        if not at(target['target_at'])<=known<=at(e['available_at'])<=when:raise LabError('Resolved outcome precedes target observation or evidence availability')
        if p['technique_id']!=49 and value not in (0,1):raise LabError('Binary outcome must be0or1')
    elif record['status'] not in ['missing','excluded'] or record['value'] is not None or record['known_at'] is not None:raise LabError('Missing/excluded outcomes must have null value/known_at')
def replay(ledger):
    bounded_json(ledger);fields(ledger,'ledger');integer(ledger['schema_version'],1,1);p=ledger['plan'];latest_native=validate_plan(p)
    if ledger['plan_sha256']!=digest(p):raise IntegrityError('Experiment plan commitment mismatch')
    parent=ledger['plan_sha256'];last=at(p['created_at']);forecast=None;outcomes={}
    for index,a in enumerate(sequence(ledger['actions'],512),1):
        fields(a,'action');integer(a['sequence'],index,index);when=at(a['at'])
        if a['parent_sha256']!=parent or digest({k:v for k,v in a.items() if k!='sha256'})!=a['sha256']:raise IntegrityError('Immutable action chain mismatch')
        if when<last:raise LabError('Experiment action chronology must be nondecreasing')
        if a['kind']=='forecast':
            if forecast is not None:raise LabError('Forecast version immutable; create a new experiment version')
            if not latest_native<=when<=at(p['cutoff']):raise LabError('Forecast issued before input availability or after cutoff')
            expected=_forecast_record(p)
            if a['record']!=expected:raise IntegrityError('Stored native forecast differs from independent native replay')
            forecast=a['record']
        elif a['kind']=='outcome':
            if forecast is None:raise LabError('Outcome requires a previously committed forecast')
            _outcome(p,a['record'],when);key=a['record']['target_id']
            if key in outcomes:raise LabError('Outcome immutable within experiment version')
            outcomes[key]=a['record']
        else:raise LabError('Unsupported experiment action')
        parent=a['sha256'];last=when
    return dict(forecast=copy.deepcopy(forecast),outcomes=copy.deepcopy(outcomes),head_sha256=parent,last_at=last)
def create(plan,parent=None):
    p=copy.deepcopy(plan);validate_plan(p)
    if parent is None:
        if p['version']!=1 or p['parent_ledger_sha256'] is not None:raise LabError('Version1requires nullparent; later versions need actual prior ledger')
    else:
        state=replay(parent)
        if p['id']!=parent['plan']['id'] or p['version']!=parent['plan']['version']+1 or p['parent_ledger_sha256']!=digest(parent):raise IntegrityError('Experiment version/parent mismatch')
        if at(p['created_at'])<state['last_at']:raise LabError('New experiment version cannot precede prior actions')
    ledger=dict(schema_version=1,plan=p,plan_sha256=digest(p),actions=[]);bounded_json(ledger);return ledger
def _append(ledger,kind,record,when):
    state=replay(ledger);out=copy.deepcopy(ledger)
    if at(when)<state['last_at'] or len(out['actions'])>=512:raise LabError('Append chronology/action cap exceeded')
    action=dict(sequence=len(out['actions'])+1,kind=kind,at=when,record=copy.deepcopy(record),parent_sha256=state['head_sha256']);action['sha256']=digest(action);out['actions'].append(action);replay(out);return out
def forecast(ledger,issued_at):
    state=replay(ledger)
    if state['forecast'] is not None:raise LabError('Forecast version already committed')
    if at(issued_at)>at(ledger['plan']['cutoff']):raise LabError('Forecast revision after cutoff')
    return _append(ledger,'forecast',_forecast_record(ledger['plan']),issued_at)
def resolve(ledger,outcome,recorded_at):return _append(ledger,'outcome',outcome,recorded_at)
def persist(directory,ledger):
    replay(ledger);destination=Path(directory);destination.mkdir(parents=True,exist_ok=True);name=ledger['plan']['id']+'-v'+str(ledger['plan']['version'])+'-'+digest(ledger)+'.json';path=destination/name;raw=(json.dumps(ledger,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
    try:
        with path.open('xb') as stream:stream.write(raw)
    except FileExistsError:
        if path.read_bytes()!=raw:raise IntegrityError('Existing immutable snapshot bytes differ')
    return str(path.resolve())
