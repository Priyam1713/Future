"""Freeze independent native outputs and exact scoring before Lab implementation."""
import copy,hashlib,importlib,json,subprocess,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def save(p,x):(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def native_samples(registry):
    from future.__main__ import load_registry
    legacy={1:['1990-07-15T14:30','Asia/Kolkata','28.6139','77.209'],2:['1990-07-15T14:30','Asia/Kolkata','28.6139','77.209'],3:['1990-07-15T14:30','Asia/Kolkata','28.6139','77.209'],4:['1990-07-15','ALICE','2026-11-09','--basis','birth'],5:['Was this advice given with honest intent?','advice-intent','2026-11-03T12:00:00','Asia/Kolkata','28.6139','77.209','--protocol','advice-begins'],6:['2026','Europe/London','51.5','0'],7:['1990-07-15T14:30:00','Asia/Kolkata','28.6139','77.209']};samples={}
    for entry in registry['entries']:
        i=entry['technique_id'];op=entry['operations'][0]
        if i in legacy:
            cp=subprocess.run([sys.executable,'-m','future',op['command']]+legacy[i],cwd=R,capture_output=True);assert cp.returncode==0,(i,cp.stderr);body=json.loads(cp.stdout);samples[str(i)]=dict(request=dict(technique_id=i,operation=op['command'],arguments=legacy[i]),native_output_sha256=digest(body),method='Existing public CLI subprocess, before Lab code')
        else:
            module,function=op['python_entry_point'].rsplit('.',1);fn=getattr(importlib.import_module(module),function);stem=Path(entry['core_record']).stem.removesuffix('_core_v1');slug=stem.replace('_','-');candidates=[]
            manifest=R/('data/'+slug+'-cli-replay.json')
            if manifest.exists():candidates += [R/x['input'] for x in json.loads(manifest.read_text(encoding='utf-8'))['records'] if x['exit_code']==0]
            for prefix in [slug,stem,op['command'],stem.split('_')[0]]:
                candidates += sorted((R/'data').glob(prefix+'*input*.json'))+sorted((R/'data').glob(prefix+'*observations*.json'))+sorted((R/'data').glob(prefix+'*descriptors*.json'))
            candidates += sorted((R/('data/'+slug+'-cli')).glob('*input*.json'))
            seen=set();chosen=None
            for path in candidates:
                if path in seen:continue
                seen.add(path)
                try:
                    q=json.loads(path.read_text(encoding='utf-8'));reg=load_registry()
                    try:body=fn(copy.deepcopy(q),reg)
                    finally:reg.close()
                except (ValueError,TypeError,KeyError,OSError,OverflowError):continue
                chosen=dict(request=dict(technique_id=i,operation=op['command'],input=q),native_output_sha256=digest(body),source_input=path.relative_to(R).as_posix(),method='Existing unchanged native API before Lab code');break
            if chosen is None:raise ValueError('No existing accepted sample found for '+str(i)+' '+stem)
            samples[str(i)]=chosen
        print('Frozen native sample '+str(i),flush=True)
    return samples
def demo_plan(registry):
    from future import superforecasting as e
    from scripts.superforecasting_oracle import plan,forecast
    p=plan(3);ledger=e.create(p)
    for i,probability in enumerate(['1/5','4/5','1/2']):ledger=e.append(ledger,'forecast',forecast(p,i,probability))
    native=e.request('report',ledger);entry=next(x for x in registry['entries'] if x['technique_id']==51);snapshot='Self-authored synthetic switch experiment; no real participants or measured forecasting skill.'
    return dict(schema_version=1,id='synthetic-switch-study',version=1,parent_ledger_sha256=None,mode='synthetic',created_at='2025-01-01T00:00:00Z',cutoff='2025-01-03T00:00:00Z',technique_id=51,operation='superforecasting',registry_sha256=digest(registry),profile_identifiers=entry['profile_identifiers'],target_definition='Three fictional binary switch questions, fixed before their outcomes.',target_unit='binary_event',dataset=dict(id='synthetic-switch-data',version=1,rights='self_authored',attribution='Future original synthetic experiment',snapshot=snapshot,snapshot_sha256=hashlib.sha256(snapshot.encode()).hexdigest(),available_at='2024-12-31T00:00:00Z',source_vintage=dict(status='declared_as_of',retrieved_at='2024-12-31T00:00:00Z',notes='Synthetic declarations only; no external information-vintage certification.')),splits=[dict(id=q['id'],group=q['dependency_group'],partition='test',available_at='2025-01-10T00:00:00Z') for q in p['questions']],selection=dict(frozen_at='2025-01-01T00:00:00Z',model_id='native_forecast_versions',native_input_sha256=digest(native),training_ids=[],validation_ids=[]),native_input=native,targets=[dict(id=q['id'],native_key=slot['forecast_id'],event_id=q['event_id'],dependency_group=q['dependency_group'],target_at=q['window_end']) for q,slot in zip(p['questions'],p['slots'])],metric='brier',baseline='fixed_half')
def outcome(target,missing=False):
    text='Synthetic switch outcome log, authored separately after forecast commitment.'
    return dict(target_id=target['id'],event_id=target['event_id'],version=1,status='missing' if missing else 'resolved',value=None if missing else '0',known_at=None if missing else '2025-01-10T00:00:00Z',reason='Synthetic observation missing' if missing else 'Synthetic switch remained zero throughout its closed window',evidence=dict(id='evidence-'+target['id'],available_at='2025-01-11T00:00:00Z',rights='self_authored',attribution='Original synthetic outcome author',snapshot=text,snapshot_sha256=hashlib.sha256(text.encode()).hexdigest()))
def build():
    path=R/'tests/fixtures/future-lab-independent-v1.json'
    if path.exists():raise ValueError('Immutable Lab fixtures already exist')
    registry=json.loads((R/'data/future-lab-capability-registry.json').read_text(encoding='utf-8'));p=demo_plan(registry);samples=native_samples(registry)
    binary=[]
    for ps,ys,bs in [(['1/5','4/5'],[0,0],['1/2','1/2']),(['1/5','4/5'],[0,1],['1/2','1/2']),(['0','1'],[0,1],['1/2','1/2']),([],[],[])]:
        losses=[(F(x)-y)**2 for x,y in zip(ps,ys)];baseline=[(F(x)-y)**2 for x,y in zip(bs,ys)];binary.append(dict(predictions=ps,outcomes=ys,baseline=bs,brier=str(sum(losses,F(0))/len(losses)) if losses else None,baseline_brier=str(sum(baseline,F(0))/len(baseline)) if losses else None,two_category=str(2*sum(losses,F(0))/len(losses)) if losses else None))
    numeric=dict(predictions=['1','4'],outcomes=['2','2'],baseline=['0','0'],mae='3/2',mse='5/2',bias='1/2',baseline_mae='2',rmse_expression='sqrt(5/2)',rmse_decimal='1.581138830084')
    families=['54-registry-ids','six-exclusions','54-native-schema-preservation','native-errors','unsupported-comparison','registry-hash','profile-hash','source-hash','cutoff','outcome-leakage','split-separation','selection-freeze','missing-outcomes','not-estimable','binary-identities','numeric-identities','matched-baseline','calibration','deterministic-forecast','immutable-actions','version-parent','exclusive-snapshot','native-reexecution','json-markdown-replay','noaa-negative-reference','scope-boundaries']
    f=dict(version=1,families=families,retained_ids=[i for i in range(1,61) if i not in [25,27,41,42,47,48]],excluded_ids=[25,27,41,42,47,48],native_samples=samples,demo_plan=p,demo_outcomes=[outcome(t,i==2) for i,t in enumerate(p['targets'])],demo_expected=dict(planned=3,matched=2,missing=1,model_brier='17/50',baseline_brier='1/4',model_minus_baseline='9/100',two_category='17/25',empirical_skill_certified=False),binary_vectors=binary,numeric_vector=numeric)
    save(path.relative_to(R),f);save('knowledge/future_lab_fixture_freeze_v1.json',dict(version=1,fixture_sha256=digest(f),oracle_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),lab_production_exists=(R/'future/lab/__init__.py').exists(),independence='Expected native outputs from unchanged engines/public CLI before Lab code; exact scoring independently computed with Fraction; no Lab imports.'))
    print('54 native fixtures;26 acceptance families;independent scoring frozen before Lab')
if __name__=='__main__':build()
