"""Exact synthetic offline classification and declared leakage diagnostics."""
import copy,hashlib,json,re
from fractions import Fraction as F
from pathlib import Path
from .remote_viewing import digest,obj,identifier,integer,text
from .scrying import load_input,freeze
ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='30f541e00247d4c9f78fa5218cba83e5e5caf7417868743cf4e3b4cebfa629a0'
def assets():
    p=load_input(ROOT/'knowledge/brain_intention_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned classifier profile mismatch')
    for file,key in [('brain_intention_sources.json','source_manifest_sha256'),('brain_intention_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/file))!=p[key]:raise ValueError('Pinned source integrity mismatch')
    return p
DATA=freeze(assets())
def fields(v,name):obj(v,DATA['schema'][name])
def seq(v,limit):
    if not isinstance(v,list) or len(v)>limit:raise ValueError('Bounded list required')
    return v
def rational(v):
    if type(v) is int:
        if len(str(abs(v)))>18:raise ValueError('Rational component digits exceeded')
        return F(v)
    if not isinstance(v,str) or not re.fullmatch(r'-?(?:0|[1-9][0-9]{0,17})(?:/[1-9][0-9]{0,17})?',v) or v.startswith('-0'):raise ValueError('Exact bounded rational required')
    return F(v)
def checked(a,b,operation):
    # Reserve before constructing cross products; conservative, deterministic refusal.
    an,ad=a.numerator.bit_length(),a.denominator.bit_length();bn,bd=b.numerator.bit_length(),b.denominator.bit_length()
    if operation=='add':nb=max(an+bd,bn+ad)+1;db=ad+bd
    else:nb=an+bn;db=ad+bd
    if max(nb,db)>8192:raise ValueError('Intermediate rational bit reservation exceeded')
    return a+b if operation=='add' else a*b
def add(a,b):return checked(a,b,'add')
def mul(a,b):return checked(a,b,'mul')
def total(xs):
    result=F(0)
    for x in xs:result=add(result,x)
    return result
def div(a,n):return mul(a,F(1,n))
def validate(q):
    fields(q,'root');integer(q['schema_version'],1,1);fields(q['profile'],'profile');integer(q['profile']['version'],1,1)
    if q['profile']!=dict(id=DATA['id'],version=1,sha256=PROFILE_HASH,catalog_sha256=DATA['source_manifest_sha256']):raise ValueError('Profile identity mismatch')
    if q['mode'] not in ('features','windows'):raise ValueError('Unsupported feature mode')
    if q['task'] not in ('editorial_binary','synthetic_imagined_hands_feet'):raise ValueError('Unsupported task or modality')
    if q['protocol'] not in ('subject_disjoint','within_subject_heldout_run'):raise ValueError('Unsupported split protocol')
    if q['filter']!='none':raise ValueError('Signal preprocessing including noncausal filters unsupported')
    fit=integer(q['fit_at'],0,10**9);channels=seq(q['channels'],8)
    if not channels:raise ValueError('Channels required')
    ids=[]
    for c in channels:
        fields(c,'channel');identifier(c['id']);ids.append(c['id'])
        if c['unit']!='arbitrary_units':raise ValueError('Only synthetic arbitrary units supported')
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate channel')
    trials=seq(q['trials'],256)
    if len(trials)<2:raise ValueError('TRAIN and TEST trials required')
    p=q['provenance'];fields(p,'provenance')
    if p['synthetic'] is not True or p['rights']!='self_authored':raise ValueError('Self-authored synthetic data required')
    if p['source_ref'] not in [s['id'] for s in load_input(ROOT/'knowledge/brain_intention_sources.json')]:raise ValueError('Unknown source reference')
    for key in ['attribution','snapshot']:
        if not text(p[key],4000).strip():raise ValueError('Nonempty provenance required')
    if p['snapshot_sha256']!=hashlib.sha256(p['snapshot'].encode('utf-8')).hexdigest():raise ValueError('Snapshot hash mismatch')
    groups={};sources={};subject_parts={};run_parts={};parsed={};ids=[];raw=0;intervals=[];train_labels=[];partitions=set()
    for t in trials:
        fields(t,'trial')
        for key in ['id','subject','run','source_id','trial_id']:identifier(t[key])
        ids.append(t['id']);part=t['partition']
        if part not in ('TRAIN','VALIDATION','TEST'):raise ValueError('Unknown partition')
        partitions.add(part)
        if t['label'] not in ('A','B'):raise ValueError('Binary A/B labels required')
        if t['session'] is not None:raise ValueError('Session metadata and cross-session claims unsupported')
        if q['task']=='editorial_binary':
            if t['annotation'] is not None:raise ValueError('Editorial task has no neural annotation')
        elif t['run'] not in ('6','10','14') or t['annotation']!=('T1' if t['label']=='A' else 'T2'):raise ValueError('Run-specific T1 hands/T2 feet mapping required')
        for key in ['start','end','available_at','predict_at','label_available_at']:integer(t[key],0,10**9)
        if not t['start']<t['end']<=t['available_at']<=t['predict_at']:raise ValueError('Window or feature availability violation')
        if part=='TRAIN':
            train_labels.append(t['label'])
            if max(t['available_at'],t['label_available_at'])>fit:raise ValueError('TRAIN data/labels unavailable at fit')
        elif t['predict_at']<fit or t['label_available_at']<=t['predict_at']:raise ValueError('Fit/prediction/outcome availability violation')
        group=(t['subject'],t['run'],t['trial_id'])
        if group in groups and groups[group]!=part:raise ValueError('Dependent trial crosses partition')
        groups[group]=part
        identity=(t['subject'],t['run'])
        if t['source_id'] in sources and sources[t['source_id']]!=identity:raise ValueError('Source file identity alias')
        sources[t['source_id']]=identity
        subject_parts.setdefault(t['subject'],set()).add(part);run_parts.setdefault(t['run'],set()).add(part)
        for source,start,end,previous in intervals:
            if source==t['source_id'] and part!=previous and max(start,t['start'])<min(end,t['end']):raise ValueError('Source intervals overlap across partition')
        intervals.append((t['source_id'],t['start'],t['end'],part))
        v=seq(t['values'],512)
        if q['mode']=='features':
            if len(v)!=2*len(channels):raise ValueError('Feature dimension mismatch')
            raw+=len(v);parsed[t['id']]=[rational(a) for a in v]
            if any(a<0 for a in parsed[t['id']][1::2]):raise ValueError('Variance feature must be nonnegative')
        else:
            if len(v)!=len(channels):raise ValueError('Channel order/dimension mismatch')
            arrays=[]
            for c in v:
                seq(c,512)
                if not 2<=len(c)==t['end']-t['start']:raise ValueError('Window sample count/interval mismatch')
                raw+=len(c);arrays.append([rational(a) for a in c])
            parsed[t['id']]=arrays
        if raw>262144:raise ValueError('Combined raw cell cap exceeded')
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate trial ID')
    if not {'TRAIN','TEST'}<=partitions or set(train_labels)!={'A','B'}:raise ValueError('TRAIN both classes and TEST required')
    if q['protocol']=='subject_disjoint':
        if any(len(ps)>1 for ps in subject_parts.values()):raise ValueError('Subject leakage across partitions')
    elif len(subject_parts)!=1 or any(len(ps)>1 for ps in run_parts.values()):raise ValueError('Single subject with held-out runs required')
    features=2*len(channels);budget=dict(raw_cells=raw,features=features,work=raw*6+len(trials)*features*12,returned_cells=len(trials)*(2*features+32))
    for key,value in budget.items():
        if value>DATA['bounds'][key]:raise ValueError('Combined '+key+' cap exceeded')
    return parsed,budget
def extract(arrays):
    result=[]
    for xs in arrays:
        mean=div(total(xs),len(xs));variance=div(total(mul(add(x,-mean),add(x,-mean)) for x in xs),len(xs));result.extend([mean,variance])
    return result
def score(actual,predicted):
    matrix=[[0,0],[0,0]]
    for a,p in zip(actual,predicted):matrix['AB'.index(a)]['AB'.index(p)]+=1
    recalls=[F(matrix[i][i],sum(matrix[i])) if sum(matrix[i]) else None for i in (0,1)]
    return dict(confusion=matrix,count=len(actual),accuracy=str(F(matrix[0][0]+matrix[1][1],len(actual))),recall={c:None if v is None else str(v) for c,v in zip('AB',recalls)},balanced_accuracy=None if None in recalls else str(sum(recalls)/2),status='not_estimable' if None in recalls else 'estimable')
def read(request,registry=None):
    q=copy.deepcopy(request);parsed,budget=validate(q);trials=sorted(q['trials'],key=lambda t:t['id'])
    vectors={t['id']:extract(parsed[t['id']]) if q['mode']=='windows' else parsed[t['id']] for t in trials}
    train=[t for t in trials if t['partition']=='TRAIN'];test=[t for t in trials if t['partition']=='TEST'];dim=budget['features'];centroids={}
    counts={c:sum(t['label']==c for t in train) for c in 'AB'}
    for c in 'AB':centroids[c]=[div(total(vectors[t['id']][j] for t in train if t['label']==c),counts[c]) for j in range(dim)]
    predictions=[]
    for t in test:
        ds={c:total(mul(add(x,-v),add(x,-v)) for x,v in zip(vectors[t['id']],centroids[c])) for c in 'AB'}
        predictions.append(dict(id=t['id'],prediction='A' if ds['A']<=ds['B'] else 'B',distances={c:str(ds[c]) for c in 'AB'}))
    centroid_strings={c:list(map(str,centroids[c])) for c in 'AB'}
    model=dict(algorithm='unscaled-uniform-nearest-arithmetic-centroid',tie='A',channels=q['channels'],task=q['task'],centroids=centroid_strings,training=[dict(id=t['id'],label=t['label'],features=list(map(str,vectors[t['id']]))) for t in train])
    split=[{k:v for k,v in t.items() if k not in ('label','annotation','values')} for t in trials]
    majority='A' if counts['A']>=counts['B'] else 'B';actual=[t['label'] for t in test]
    sources=load_input(ROOT/'knowledge/brain_intention_sources.json')
    if registry is not None:
        for source in sources:registry.add_source(source)
    result=dict(status='accepted',technique_id=55,schema_version=1,profile=q['profile'],request=q,input_sha256=digest(q),schema_sha256=digest(dict(DATA['schema'])),source_manifest_sha256=DATA['source_manifest_sha256'],source_freeze_sha256=DATA['source_freeze_sha256'],code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),model=model,model_sha256=digest(model),split_sha256=digest(split),features={k:list(map(str,v)) for k,v in vectors.items()},centroids=centroid_strings,predictions=predictions,evaluation=score(actual,[p['prediction'] for p in predictions]),baseline=dict(prediction=majority,evaluation=score(actual,[majority]*len(test))),test_ids=[t['id'] for t in test],validation_ids=[t['id'] for t in trials if t['partition']=='VALIDATION'],diagnostics=dict(protocol=q['protocol'],subject_partition_check='passed',trial_source_interval_check='passed',availability_check='passed',test_labels_used_for='Scoring only; never fitting,selection or prediction',session_claim='unsupported',numeric_duplicate_features='Allowed; source identity and interval checks govern leakage'),iid_arithmetic_toy=dict(upper_tail_8_of_10='7/128',scope='Ideal iid fair binary arithmetic only; not EEG significance'),budget=budget,sources=sources,limitations=list(DATA['configuration_matrix']['unsupported'])+['Synthetic software correctness is not empirical neural decoding or unrestricted intention prediction.','Identities, clocks and rights are declarations; hashes do not externally certify them.','No calibration, p-value, clinical or cross-session certification.'])
    result['report_sha256']=digest(result);return result
def markdown(result):
    body=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False);fence='`'*max(3,1+max([len(x) for x in re.findall(r'`+',body)]+[0]))
    return '# Brain-Based Intention Prediction — synthetic offline reference\n\n'+fence+'json\n'+body+'\n'+fence+'\n'
