"""Independent frozen native outputs/Fraction answers plus protocol negative controls."""
import copy,hashlib,importlib,json,tempfile
from fractions import Fraction as F
from pathlib import Path
from future.lab import capability,invoke,create,forecast,resolve,replay,evaluate,compare,persist
from future.lab.common import ROOT as R,REGISTRY_HASH,digest,LabError,load_input
from future.lab.evaluation import scores
def fixture():
    original=load_input(R/'tests/fixtures/future-lab-independent-v1.json');first=load_input(R/'knowledge/future_lab_fixture_freeze_v1.json');assert digest(original)==first['fixture_sha256'] and not first['lab_production_exists'];assert hashlib.sha256((R/'scripts/future_lab_oracle.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==first['oracle_sha256']
    f=load_input(R/'tests/fixtures/future-lab-independent-v2.json');freeze=load_input(R/'knowledge/future_lab_fixture_freeze_v2.json');assert digest(f)==freeze['fixture_sha256'] and freeze['original_fixture_sha256']==digest(original) and freeze['numeric_and_native_expectations_unchanged'];assert hashlib.sha256((R/'scripts/correct_future_lab_registry_types.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==freeze['metadata_transform_sha256'];restored=copy.deepcopy(f);restored.pop('metadata_revision');restored.pop('supersedes_fixture_sha256');restored['demo_plan']['registry_sha256']=original['demo_plan']['registry_sha256'];assert restored==original;return f
def native_sample(i):
    c=fixture()['native_samples'][str(i)];r=invoke(c['request']);assert r['native_error'] is None and r['native_exit_code']==0 and r['native_output_sha256']==c['native_output_sha256'];return r
def metadata_revision():
    from future.lab.registry import registry
    old=load_input(R/'data/future-lab-capability-registry-v1.json');current=registry();restored=copy.deepcopy(current);restored['id']=old['id'];restored.pop('metadata_revision');restored.pop('supersedes_registry_sha256');oldtypes={x['technique_id']:x['capability_type'] for x in old['entries']}
    for e in restored['entries']:e['capability_type']=oldtypes[e['technique_id']]
    assert restored==old
    p1=load_input(R/'knowledge/future_lab_profile_v1.json');p2=load_input(R/'knowledge/future_lab_profile_v2.json')
    for key in ['id','version','registry_sha256']:p2[key]=p1[key]
    p2.pop('supersedes_profile_sha256');p2.pop('revision_reason');assert p2==p1
def demo():
    f=fixture();l=create(f['demo_plan']);before=copy.deepcopy(l);l=forecast(l,'2025-01-02T00:00:00Z');assert before['actions']==[]
    for outcome in f['demo_outcomes']:l=resolve(l,outcome,'2025-01-11T00:00:00Z')
    r=evaluate(l);e=f['demo_expected'];assert (r['coverage']['planned'],r['coverage']['matched'],r['coverage']['missing_outcomes'])==(e['planned'],e['matched'],e['missing']);assert r['model']['brier']['exact']==e['model_brier'] and r['baseline']['brier']['exact']==e['baseline_brier'] and r['comparison']['model_minus_baseline']==e['model_minus_baseline'];assert r['model']['two_category_brier']['exact']==e['two_category'] and r['empirical_skill_certified'] is False;assert r==evaluate(l);return l,r
def numeric_plan():
    p=copy.deepcopy(fixture()['demo_plan']);entry=capability(49);snapshot='Original synthetic monthly values -8,-5,-2; future targets absent before forecast.';sha=hashlib.sha256(snapshot.encode()).hexdigest()
    dataset=dict(id='monthly-toy',version=1,frequency='monthly',units='toy_units',series=[dict(id='s',availability=dict(status='declared_as_of',vintage='2025-04-01',notes='Synthetic declared availability'),observations=[dict(period=m,value=v) for m,v in [('2025-01','-8'),('2025-02','-5'),('2025-03','-2'),('2025-04',None),('2025-05',None)]])],provenance=dict(source_ref='original-synthetic',snapshot_sha256=sha,rights='self_authored',attribution='Original synthetic author',notes='No empirical observations.'))
    q=dict(schema_version=1,task='forecast',profile=entry['profile_identifiers'],profile_version=1,dataset=dataset,dataset_sha256=digest(dataset),model='drift',origin='2025-03',horizons=[1,2],seasonal_period=1)
    p.update(id='monthly-study',created_at='2025-04-01T00:00:00Z',cutoff='2025-04-01T00:00:00Z',technique_id=49,operation='ai-predictive-modeling',profile_identifiers=entry['profile_identifiers'],target_definition='Synthetic monthly values, with future observations withheld.',target_unit='toy_units',native_input=q,metric='mae',baseline='naive')
    p['dataset'].update(id='monthly-toy',snapshot=snapshot,snapshot_sha256=sha,available_at=p['cutoff'],source_vintage=dict(status='declared_as_of',retrieved_at=p['cutoff'],notes='Synthetic declared vintage'))
    p['targets']=[dict(id='t'+str(i),native_key='s:'+period,event_id='s--'+period,dependency_group='s',target_at=when) for i,(period,when) in enumerate([('2025-04','2025-05-01T00:00:00Z'),('2025-05','2025-06-01T00:00:00Z')])];p['splits']=[dict(id=t['id'],group='s',partition='test',available_at=t['target_at']) for t in p['targets']]+[dict(id='history'+str(i),group='history',partition='train',available_at=p['cutoff']) for i in range(3)];p['selection']=dict(frozen_at=p['cutoff'],model_id='drift',native_input_sha256=digest(q),training_ids=['history0','history1','history2'],validation_ids=[]);return p
def collective_plan():
    p=copy.deepcopy(fixture()['demo_plan']);entry=capability(57);q=load_input(R/'tests/fixtures/collective-intelligence-independent-v1.json')['cases']['equal']['input']
    for question in q['questions']:question['resolution']=dict(status='unresolved',outcome=None,event_at=None,outcome_known_at=None,resolved_at=None)
    d=q['questions'][0]['definition'];p.update(id='pool-study',technique_id=57,operation='collective-intelligence',profile_identifiers=entry['profile_identifiers'],cutoff=d['cutoff'],native_input=q);p['selection']=dict(frozen_at=q['pool']['frozen_at'],model_id='precommitted_linear_pool',native_input_sha256=digest(q),training_ids=[],validation_ids=[]);p['targets']=[dict(id=d['id'],native_key=d['id'],event_id=d['event_id'],dependency_group=d['dependency_group'],target_at=d['event_end'])];p['splits']=[dict(id=d['id'],group=d['dependency_group'],partition='test',available_at=d['event_end'])];return p
def protocol_cases():
    f=fixture();p=f['demo_plan'];cases={}
    def bad(name,change,stage='create'):
        q=copy.deepcopy(p);change(q);cases[name]=(q,stage)
    bad('registry-hash',lambda q:q.update(registry_sha256='0'*64))
    bad('profile-identity',lambda q:q.update(profile_identifiers='different'))
    bad('native-profile',lambda q:q['native_input']['profile'].update(sha256='0'*64),'seal')
    bad('native-source',lambda q:q['native_input']['profile'].update(catalog_sha256='0'*64),'seal')
    bad('input-binding',lambda q:q['selection'].update(native_input_sha256='0'*64))
    bad('snapshot-binding',lambda q:q['dataset'].update(snapshot_sha256='0'*64))
    bad('rights',lambda q:q['dataset'].update(rights='unknown'))
    bad('selection-after-cutoff',lambda q:q['selection'].update(frozen_at='2025-01-04T00:00:00Z'))
    bad('dataset-after-freeze',lambda q:q['dataset'].update(available_at='2025-01-02T00:00:00Z'))
    bad('metric-combination',lambda q:q.update(metric='mae'))
    bad('baseline-combination',lambda q:q.update(baseline='naive'))
    bad('unsupported-technique',lambda q:q.update(technique_id=60,operation='multiverse'))
    bad('unregistered-operation',lambda q:q.update(operation='multiverse'))
    bad('version-parent',lambda q:q.update(version=2))
    bad('target-group',lambda q:q['targets'][0].update(dependency_group='other'))
    bad('duplicate-event',lambda q:q['targets'][1].update(event_id=q['targets'][0]['event_id']))
    bad('missing-target',lambda q:q['targets'].pop())
    bad('native-target-key',lambda q:q['targets'][0].update(native_key='not-a-slot'),'forecast')
    bad('native-target-time',lambda q:q['targets'][0].update(target_at='2025-01-11T00:00:00Z'),'forecast')
    def split(q):q['splits'].append(dict(id='train0',group=q['targets'][0]['dependency_group'],partition='train',available_at='2024-12-31T00:00:00Z'));q['selection']['training_ids']=['train0']
    bad('cross-split-group',split)
    def unavailable(q):q['splits'].append(dict(id='train0',group='train-group',partition='train',available_at='2025-01-04T00:00:00Z'));q['selection']['training_ids']=['train0']
    bad('late-training',unavailable)
    def resolution_leak(q):
        from future import superforecasting as sf
        from scripts.superforecasting_oracle import resolution
        ledger=q['native_input']['payload'];q['native_input']['payload']=sf.append(ledger,'resolve',resolution(ledger['plan']))
    bad('outcome-leakage',resolution_leak,'seal')
    def late_revision(q):
        from future import superforecasting as sf
        from scripts.superforecasting_oracle import forecast as native_forecast
        ledger=q['native_input']['payload'];old=ledger['actions'][0]['record'];record=native_forecast(ledger['plan'],probability='9/10',version=2,parent=digest(old),at='2025-01-04T00:00:00Z');q['native_input']['payload']=sf.append(ledger,'forecast',record)
    bad('post-cutoff-native-revision',late_revision,'seal')
    return cases
def protocol_case(name):
    p,stage=protocol_cases()[name]
    if stage=='seal':p['selection']['native_input_sha256']=digest(p['native_input'])
    try:
        l=create(p)
        if stage=='forecast':forecast(l,'2025-01-02T00:00:00Z')
    except (ValueError,TypeError,KeyError):return
    raise AssertionError('Invalid experiment accepted: '+name)
def reject(fn):
    try:fn()
    except (ValueError,TypeError,KeyError):return
    raise AssertionError('Expected explicit rejection')
def boundary_check(name):
    f=fixture();p=copy.deepcopy(f['demo_plan']);empty=create(p);l=forecast(empty,'2025-01-02T00:00:00Z')
    if name=='late-forecast':reject(lambda:forecast(empty,'2025-01-04T00:00:00Z'))
    elif name=='early-forecast':reject(lambda:forecast(empty,'2025-01-01T01:00:00Z'))
    elif name=='duplicate-forecast':reject(lambda:forecast(l,'2025-01-02T01:00:00Z'))
    elif name=='outcome-before-forecast':reject(lambda:resolve(empty,f['demo_outcomes'][0],'2025-01-11T00:00:00Z'))
    elif name=='early-outcome':
        o=copy.deepcopy(f['demo_outcomes'][0]);o['known_at']='2025-01-09T00:00:00Z';reject(lambda:resolve(l,o,'2025-01-11T00:00:00Z'))
    elif name=='unavailable-evidence':
        o=copy.deepcopy(f['demo_outcomes'][0]);o['evidence']['available_at']='2025-01-12T00:00:00Z';reject(lambda:resolve(l,o,'2025-01-11T00:00:00Z'))
    elif name=='wrong-outcome-event':
        o=copy.deepcopy(f['demo_outcomes'][0]);o['event_id']='different-event';reject(lambda:resolve(l,o,'2025-01-11T00:00:00Z'))
    elif name=='boolean-outcome':
        o=copy.deepcopy(f['demo_outcomes'][0]);o['value']=False;reject(lambda:resolve(l,o,'2025-01-11T00:00:00Z'))
    elif name=='duplicate-outcome':
        l=resolve(l,f['demo_outcomes'][0],'2025-01-11T00:00:00Z');reject(lambda:resolve(l,f['demo_outcomes'][0],'2025-01-11T00:00:00Z'))
    elif name=='chain-tampering':
        l['actions'][0]['parent_sha256']='0'*64;reject(lambda:replay(l))
    elif name=='forged-native-output':
        a=l['actions'][0];a['record']['native_output']['result']['evaluation']['rows'][0]['probability']['exact']='9/10';body=copy.deepcopy(a['record']['native_output']);body.pop('report_sha256');a['record']['native_output']['report_sha256']=digest(body);a['record']['native_output_sha256']=digest(a['record']['native_output']);a['sha256']=digest({k:v for k,v in a.items() if k!='sha256'});reject(lambda:replay(l))
    elif name=='version-parent':
        p.update(version=2,parent_ledger_sha256=digest(empty));v=create(p,empty);assert v['plan']['version']==2 and empty['plan']['version']==1;p['parent_ledger_sha256']='0'*64;reject(lambda:create(p,empty))
    elif name=='exclusive-snapshot':
        with tempfile.TemporaryDirectory(prefix='future-lab-boundary-') as directory:
            assert Path(directory).resolve().is_relative_to(Path(tempfile.gettempdir()).resolve());path=Path(persist(directory,l));assert persist(directory,l)==str(path);different=copy.deepcopy(p);different['target_definition']='A different target definition under a conflicting ID/version';reject(lambda:persist(directory,create(different)));path.write_bytes(b'conflicting bytes');reject(lambda:persist(directory,l))
    elif name=='incompatible-comparison':
        _,r=demo();changed=copy.deepcopy(r);changed['target_unit']='different-unit';changed.pop('report_sha256');changed['report_sha256']=digest(changed);reject(lambda:compare([r,changed]))
    elif name=='different-cutoff-comparison':
        _,r=demo();changed=copy.deepcopy(r);changed['cutoff']='2025-01-04T00:00:00Z';changed.pop('report_sha256');changed['report_sha256']=digest(changed);reject(lambda:compare([r,changed]))
    elif name=='native-error-preservation':
        sample=copy.deepcopy(f['native_samples']['55']['request']);sample['input']['profile']['id']='wrong';r=invoke(sample);assert r['native_error']['type']=='ValueError' and r['native_output'] is None and r['native_exit_code']==2
        legacy=invoke(dict(technique_id=1,operation='natal',arguments=[]));assert legacy['native_error']['type']=='SystemExit' and legacy['native_exit_code']==2 and 'usage:' in legacy['native_stderr']
    elif name in ['source-file-tamper','profile-file-tamper','registry-file-tamper']:
        from unittest.mock import patch
        module=importlib.import_module('future.lab.registry');original=module.load_input;filename={'source-file-tamper':'superforecasting_sources.json','profile-file-tamper':'superforecasting_profile_v1.json','registry-file-tamper':'future-lab-capability-registry.json'}[name]
        def changed(path):
            value=original(path)
            if path.name==filename:
                if isinstance(value,list):value[0]['author']='Changed'
                else:value['version']=99
            return value
        with patch.object(module,'load_input',side_effect=changed):reject(lambda:capability(51))
    elif name=='lab-profile-tamper':
        from unittest.mock import patch
        module=importlib.import_module('future.lab.common');original=module.load_input
        def changed(path):
            value=original(path)
            if path.name=='future_lab_profile_v2.json':value['version']=99
            return value
        with patch.object(module,'load_input',side_effect=changed):reject(lambda:invoke(f['native_samples']['51']['request']))
    elif name=='numeric-future-leak':
        p=numeric_plan();q=p['native_input'];q['dataset']['series'][0]['observations'][-1]['value']='42';q['dataset_sha256']=digest(q['dataset']);p['selection']['native_input_sha256']=digest(q);reject(lambda:create(p))
    elif name=='pool-outcome-leak':
        p=collective_plan();p['native_input']['questions'][0]['resolution'].update(status='resolved',outcome=1,event_at='2025-01-20T00:00:00Z',outcome_known_at='2025-01-20T00:00:00Z',resolved_at='2025-01-21T00:00:00Z');p['selection']['native_input_sha256']=digest(p['native_input']);reject(lambda:create(p))
    elif name=='uncertainty-disclosures':
        _,r=demo();assert r['uncertainty']['effective_sample_size'] is None and r['uncertainty']['confidence_interval'] is None and not r['source_vintage_certified']
        p['mode']='retrospective';reject(lambda:create(p));pool=collective_plan();pool['mode']='retrospective';reject(lambda:create(pool))
    elif name=='json-markdown-replay':
        from future.lab.evaluation import markdown
        _,r=demo();_,s=demo();assert json.dumps(r,sort_keys=True)==json.dumps(s,sort_keys=True) and markdown(r)==markdown(s) and 'SYNTHETIC' in markdown(r) and 'SYNTHETIC' in markdown(dict(status='accepted',result=r))
    elif name=='calibration-endpoint':assert scores(['0','1'],['0','1'],'binary')['calibration'][9]['count']==1
    elif name=='native-state-preservation':
        before=copy.deepcopy(p);l=forecast(create(p),'2025-01-02T00:00:00Z');assert p==before and empty['actions']==[] and l['plan']==p
    else:raise AssertionError(name)
BOUNDARIES=['late-forecast','early-forecast','duplicate-forecast','outcome-before-forecast','early-outcome','unavailable-evidence','wrong-outcome-event','boolean-outcome','duplicate-outcome','chain-tampering','forged-native-output','version-parent','exclusive-snapshot','incompatible-comparison','different-cutoff-comparison','native-error-preservation','source-file-tamper','profile-file-tamper','registry-file-tamper','lab-profile-tamper','numeric-future-leak','pool-outcome-leak','uncertainty-disclosures','json-markdown-replay','calibration-endpoint','native-state-preservation']
def run():
    f=fixture();metadata_revision();ids=[e['technique_id'] for e in __import__('future.lab',fromlist=['registry']).registry()['entries']];assert ids==f['retained_ids']
    for i in f['excluded_ids']:
        try:capability(i)
        except ValueError:pass
        else:raise AssertionError('Excluded technique admitted')
    for i in ids:native_sample(i)
    for name in protocol_cases():protocol_case(name)
    for name in BOUNDARIES:boundary_check(name)
    l,r=demo()
    for v in f['binary_vectors']:
        score=scores(v['predictions'],list(map(str,v['outcomes'])),'binary');baseline=scores(v['baseline'],list(map(str,v['outcomes'])),'binary');assert score['brier']['exact']==v['brier'] and baseline['brier']['exact']==v['baseline_brier'] and score['two_category_brier']['exact']==v['two_category']
    n=f['numeric_vector'];score=scores(n['predictions'],n['outcomes'],'numeric');assert score['mae']['exact']==n['mae'] and score['mse']['exact']==n['mse'] and score['bias']['exact']==n['bias'] and score['rmse']['exact']==n['rmse_expression'] and score['rmse']['decimal']==n['rmse_decimal']
    assert evaluate(create(f['demo_plan']))['model']['brier']['status']=='not_estimable'
    numeric=forecast(create(numeric_plan()),'2025-04-01T00:00:00Z');assert replay(numeric)['forecast']['predictions']==dict(t0='1',t1='4') and replay(numeric)['forecast']['baseline_predictions']==dict(t0='-2',t1='-2')
    pool=forecast(create(collective_plan()),'2025-01-06T00:00:00Z');assert replay(pool)['forecast']['predictions']==dict(q1='1/2')
    comparison=compare([r,r]);assert comparison['matched_count']==2
    with tempfile.TemporaryDirectory(prefix='future-lab-verify-') as directory:
        assert Path(directory).resolve().is_relative_to(Path(tempfile.gettempdir()).resolve());a=persist(directory,l);assert persist(directory,l)==a and load_input(Path(a))==l
    from future.lab.reference import noaa_reference
    noaa=noaa_reference();assert noaa['empirical_superiority_certified'] is False and 'underperformed' in noaa['primary_result']
    out=dict(passed=True,fixture_families=len(f['families']),families={name:dict(passed=True) for name in f['families']},native_schema_cases=54,excluded_ids=f['excluded_ids'],protocol_negative_cases=len(protocol_cases()),boundary_checks=BOUNDARIES,demo_expected=f['demo_expected'],numeric_anchor=n,fixture_sha256=digest(f),noaa_primary_result=noaa['primary_result'],scope='Native schema,exact math andprocedural validation;noempirical superiority certification.')
    (R/'data/future-lab-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('26 independent Lab families pass;54native schemas;'+str(len(protocol_cases()))+'protocolnegativecontrols;exactscore/baseline andNOAAreference pass')
if __name__=='__main__':run()
