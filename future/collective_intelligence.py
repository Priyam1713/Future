"""Versioned exact offline binary linear pools; no empirical wisdom certification."""
import copy,hashlib,json,re
from fractions import Fraction as F
from pathlib import Path
from .remote_viewing import digest,obj,identifier,integer,text,timestamp
from .scrying import load_input,freeze
ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='925a21d05410b91f073d50b403f17c3cf709d28194f539d5c292bf328dd8b854'
def assets():
    p=load_input(ROOT/'knowledge/collective_intelligence_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned collective profile mismatch')
    for name,key in [('collective_intelligence_sources.json','source_manifest_sha256'),('collective_intelligence_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/name))!=p[key]:raise ValueError('Pinned source integrity mismatch')
    return p
DATA=freeze(assets())
def fields(v,key):obj(v,DATA['schema'][key])
def seq(v,limit):
    if not isinstance(v,list) or len(v)>limit:raise ValueError('Bounded list required')
    return v
def at(v):
    if not isinstance(v,str) or not v.endswith('Z'):raise ValueError('UTC-Z timestamp required')
    return timestamp(v)
def nonempty(v):
    if not text(v,4000).strip():raise ValueError('Nonempty bounded text required')
def rational(v):
    if type(v) is int:
        if len(str(abs(v)))>18:raise ValueError('Rational component digits exceeded')
        return F(v)
    if not isinstance(v,str) or not re.fullmatch(r'-?(?:0|[1-9][0-9]{0,17})(?:/[1-9][0-9]{0,17})?',v) or v.startswith('-0'):raise ValueError('Exact bounded rational required')
    return F(v)
def operation(a,b,kind):
    an,ad=a.numerator.bit_length(),a.denominator.bit_length();bn,bd=b.numerator.bit_length(),b.denominator.bit_length()
    if max(max(an+bd,bn+ad)+1 if kind=='add' else an+bn,ad+bd)>8192:raise ValueError('Intermediate rational bit reservation exceeded')
    return a+b if kind=='add' else a*b
def add(a,b):return operation(a,b,'add')
def mul(a,b):return operation(a,b,'mul')
def ratio(a,b):
    if not b:raise ValueError('Undefined denominator')
    return mul(a,F(b.denominator,b.numerator))
def total(xs):
    value=F(0)
    for x in xs:value=add(value,x)
    return value
def mean(xs):return ratio(total(xs),F(len(xs))) if xs else None
def loss(p,y):
    delta=add(p,-F(y));return mul(delta,delta)
def validate(q):
    fields(q,'root');integer(q['schema_version'],1,1);fields(q['profile'],'profile');integer(q['profile']['version'],1,1)
    if q['profile']!=dict(id=DATA['id'],version=1,sha256=PROFILE_HASH,catalog_sha256=DATA['source_manifest_sha256']):raise ValueError('Profile identity mismatch')
    pool=q['pool'];fields(pool,'pool');frozen=at(pool['frozen_at'])
    if pool['kind'] not in ('equal','declared_weight') or at(pool['weights_available_at'])>frozen:raise ValueError('Precommitted pool/weight availability required')
    provenance=q['provenance'];fields(provenance,'provenance')
    if provenance['evidence_mode'] not in ('synthetic','user_supplied_unvalidated'):raise ValueError('Unsupported evidence mode')
    if provenance['rights'] not in ('self_authored','permission_granted','public_domain','cc_by') or provenance['evidence_mode']=='synthetic' and provenance['rights']!='self_authored':raise ValueError('Explicit evidence rights required')
    if provenance['source_ref'] not in [s['id'] for s in load_input(ROOT/'knowledge/collective_intelligence_sources.json')]:raise ValueError('Unknown source reference')
    nonempty(provenance['attribution']);nonempty(provenance['snapshot'])
    if provenance['snapshot_sha256']!=hashlib.sha256(provenance['snapshot'].encode()).hexdigest():raise ValueError('Snapshot hash mismatch')
    forecasters=seq(q['forecasters'],32);questions=seq(q['questions'],32);forecasts=seq(q['forecasts'],2048)
    if not forecasters or not questions:raise ValueError('Question and forecaster roster required')
    budget=dict(work=len(forecasts)*64+len(questions)*len(forecasters)*32,returned_cells=len(questions)*len(forecasters)*24+len(forecasts)*16)
    for k,v in budget.items():
        if v>DATA['bounds'][k]:raise ValueError('Combined '+k+' cap exceeded')
    fs={};weights={}
    for f in forecasters:
        fields(f,'forecaster');identifier(f['id']);identifier(f['dependency_group'])
        if f['id'] in fs:raise ValueError('Duplicate forecaster identity')
        if f['kind'] not in ('human_declared','synthetic','llm_simulated') or provenance['evidence_mode']=='synthetic' and f['kind']=='human_declared':raise ValueError('Forecaster kind/evidence mismatch')
        weight=rational(f['weight'])
        if weight<0 or pool['kind']=='equal' and weight!=1:raise ValueError('Nonnegative declared weights; equal mode requires all1')
        fs[f['id']]=f;weights[f['id']]=weight
    if total(weights[f] for f in sorted(weights))<=0:raise ValueError('At least one positive roster weight required')
    qs={};events=set();group_partitions={};boundaries={}
    for item in questions:
        fields(item,'question');d=item['definition'];r=item['resolution'];fields(d,'definition');fields(r,'resolution')
        for key in ['id','event_id','dependency_group']:identifier(d[key])
        integer(d['version'],1,1)
        if d['id'] in qs or d['event_id'] in events:raise ValueError('Duplicate question/event identity')
        if d['partition'] not in ('train','test'):raise ValueError('Unknown question partition')
        if d['dependency_group'] in group_partitions and group_partitions[d['dependency_group']]!=d['partition']:raise ValueError('Question dependency group crosses held-out partitions')
        group_partitions[d['dependency_group']]=d['partition']
        if d['clarity_confirmed'] is not True:raise ValueError('Binary clarity declaration required')
        for key in ('text','positive_rule','negative_rule'):nonempty(d[key])
        created,locked,cutoff,end=(at(d[k]) for k in ['created_at','locked_at','cutoff','event_end'])
        if not created<=locked<=frozen<=cutoff<=end or not created<end:raise ValueError('Question lock/pool freeze/cutoff chronology violation')
        status=r['status'];boundary=[]
        if status=='resolved':
            integer(r['outcome'],0,1);event,known,resolved=(at(r[k]) for k in ['event_at','outcome_known_at','resolved_at'])
            if not created<=event<=end or not event<=known<=resolved or r['outcome']==0 and event!=end:raise ValueError('Outcome resolution chronology violation')
            boundary=[event,known]
        elif status=='unresolved':
            if any(r[k] is not None for k in ['outcome','event_at','outcome_known_at','resolved_at']):raise ValueError('Unresolved fields must be null')
        elif status in ('void','disputed'):
            if r['outcome'] is not None or r['event_at'] is not None:raise ValueError('Void/disputed outcome must be null')
            known,resolved=at(r['outcome_known_at']),at(r['resolved_at'])
            if known>resolved:raise ValueError('Resolution knowledge chronology violation')
            boundary=[known]
        else:raise ValueError('Unknown resolution status')
        if boundary and frozen>=min(boundary):raise ValueError('Weights frozen at/after outcome information')
        qs[d['id']]=item;events.add(d['event_id']);boundaries[d['id']]=min(boundary) if boundary else None
    histories={};probabilities={}
    for record in forecasts:
        fields(record,'forecast');qid=identifier(record['question_id']);fid=identifier(record['forecaster']);revision=integer(record['revision'],1,2048)
        if qid not in qs or fid not in fs:raise ValueError('Unknown question/forecaster reference')
        if record['question_sha256']!=digest(qs[qid]['definition']):raise ValueError('Question definition hash mismatch')
        issued,knowledge=at(record['issued_at']),at(record['knowledge_at'])
        if issued<at(qs[qid]['definition']['locked_at']):raise ValueError('Forecast before question lock')
        if knowledge>issued:raise ValueError('Knowledge after forecast issue')
        p=None if record['probability'] is None else rational(record['probability'])
        if p is not None and not 0<=p<=1:raise ValueError('Probability outside0..1')
        key=(qid,fid,revision)
        if key in probabilities:raise ValueError('Duplicate forecast revision')
        probabilities[key]=p;histories.setdefault((qid,fid),[]).append(record)
    decisions={};selected={}
    for (qid,fid),records in sorted(histories.items()):
        records.sort(key=lambda r:r['revision']);previous=None;last_time=None;decisions[(qid,fid)]=[]
        for n,r in enumerate(records,1):
            if r['revision']!=n or r['parent_sha256']!=(digest(previous) if previous is not None else None):raise ValueError('Forecast parent/version chain mismatch')
            issued,knowledge=at(r['issued_at']),at(r['knowledge_at'])
            if last_time is not None and issued<=last_time:raise ValueError('Forecast revision times must strictly increase')
            reasons=[]
            if issued>at(qs[qid]['definition']['cutoff']) or knowledge>at(qs[qid]['definition']['cutoff']):reasons.append('after_cutoff')
            if boundaries[qid] is not None and (issued>=boundaries[qid] or knowledge>=boundaries[qid]):reasons.append('at_or_after_outcome_information')
            decisions[(qid,fid)].append(dict(revision=n,record_sha256=digest(r),decision='rejected' if reasons else 'eligible_abstention' if r['probability'] is None else 'eligible',reasons=reasons))
            if not reasons:selected[(qid,fid)]=r
            previous=r;last_time=issued
    return fs,weights,qs,probabilities,histories,decisions,selected,budget
def summarize(rows):
    # Each row=(question_id,probability,outcome,equal_pool_probability).
    n=len(rows);ids=[r[0] for r in rows];ps=[r[1] for r in rows];ys=[r[2] for r in rows]
    bs=mean([loss(p,y) for p,y in zip(ps,ys)]);groups=[];bins=[];rel=res=unc=None
    if n:
        overall=ratio(F(sum(ys)),F(n));rel=res=F(0);unc=mul(overall,add(F(1),-overall))
        for p in sorted(set(ps)):
            outcomes=[y for value,y in zip(ps,ys) if value==p];frequency=ratio(F(sum(outcomes)),F(len(outcomes)));share=F(len(outcomes),n)
            rel=add(rel,mul(share,loss(p,frequency)));res=add(res,mul(share,loss(frequency,overall)));groups.append(dict(probability=str(p),count=len(outcomes),observed_frequency=str(frequency)))
        if add(add(rel,-res),unc)!=bs:raise ValueError('Exact Brier decomposition identity failed')
    for i in range(10):
        entries=[(p,y) for p,y in zip(ps,ys) if min(9,int(mul(p,F(10))))==i];count=len(entries)
        bins.append(dict(index=i,lower=str(F(i,10)),upper=str(F(i+1,10)),upper_inclusive=i==9,count=count,positive_count=sum(y for _,y in entries),mean_probability=str(mean([p for p,_ in entries])) if count else None,observed_frequency=str(F(sum(y for _,y in entries),count)) if count else None))
    equal=mean([loss(r[3],r[2]) for r in rows]);half=F(1,4) if n else None
    return dict(status='estimable' if n else 'not_estimable',count=n,question_ids=ids,binary_brier=None if bs is None else str(bs),two_category_brier=None if bs is None else str(mul(F(2),bs)),equal_pool_brier=None if equal is None else str(equal),half_baseline_brier=None if half is None else str(half),half_baseline_improvement=None if bs is None else str(add(half,-bs)),decomposition=dict(grouping='Exact identical Fraction probabilities,not coarse calibration bins',groups=groups,reliability=None if rel is None else str(rel),resolution=None if res is None else str(res),uncertainty=None if unc is None else str(unc),identity_passed=None if bs is None else add(add(rel,-res),unc)==bs),calibration=bins,scope='Descriptive matched declared event scores; not empirical skill or independent-sample certification')
def read(request,registry=None):
    q=copy.deepcopy(request);fs,weights,qs,probabilities,histories,decisions,selected,budget=validate(q);results={};scores={'train':[],'test':[]};individuals={f:[] for f in fs};chosen_for_hash=[]
    for qid,item in sorted(qs.items()):
        versions={};ps={};account=[]
        for fid in sorted(fs):
            r=selected.get((qid,fid));versions[fid]=r['revision'] if r else None;ps[fid]=None if r is None else probabilities[(qid,fid,r['revision'])]
            status='missing' if r is None else 'abstaining' if ps[fid] is None else 'zero_weight' if weights[fid]==0 else 'contributing'
            account.append(dict(forecaster=fid,status=status,selected_revision=versions[fid],selected_record_sha256=digest(r) if r else None,probability=None if ps[fid] is None else str(ps[fid]),declared_weight=str(weights[fid]),dependency_group=fs[fid]['dependency_group'],kind=fs[fid]['kind'],revisions=decisions.get((qid,fid),[])))
            if r is not None:chosen_for_hash.append(r)
        active=[f for f in sorted(fs) if ps[f] is not None and weights[f]>0];present=[f for f in sorted(fs) if ps[f] is not None];den=total(weights[f] for f in active)
        pool=ratio(total(mul(weights[f],ps[f]) for f in active),den) if den else None;equal=mean([ps[f] for f in present]);norm={f:str(ratio(weights[f],den)) if f in active else '0' for f in sorted(fs)}
        results[qid]=dict(status='estimable' if pool is not None else 'not_estimable',probability=None if pool is None else str(pool),equal_probability=None if equal is None else str(equal),selected_versions=versions,selected_probabilities={f:None if p is None else str(p) for f,p in ps.items()},normalized_weights=norm,available_weight=str(den),contributors=len(active),equal_pool_participants=len(present),participant_accounting=account,question_sha256=digest(item['definition']),resolution_sha256=digest(item['resolution']),resolution_status=item['resolution']['status'],exclusion_reason='zero_available_weight' if pool is None else None)
        if pool is not None and item['resolution']['status']=='resolved':
            y=item['resolution']['outcome'];partition=item['definition']['partition'];scores[partition].append((qid,pool,y,equal))
            if partition=='test':
                for f in fs:
                    if ps[f] is not None:individuals[f].append((qid,loss(ps[f],y),loss(pool,y)))
    comparisons={f:dict(question_ids=[r[0] for r in rows],count=len(rows),individual_brier=str(mean([r[1] for r in rows])) if rows else None,aggregate_brier=str(mean([r[2] for r in rows])) if rows else None,status='estimable' if rows else 'not_estimable') for f,rows in sorted(individuals.items())}
    definition_list=[v['definition'] for _,v in sorted(qs.items())];forecaster_list=[v for _,v in sorted(fs.items())];model=dict(profile_sha256=PROFILE_HASH,pool=q['pool'],forecasters=forecaster_list,definitions=definition_list,chosen_forecasts=sorted(chosen_for_hash,key=lambda r:(r['question_id'],r['forecaster'])))
    split=[{k:d[k] for k in ['id','event_id','dependency_group','partition','cutoff']} for d in definition_list];groups={}
    for f in forecaster_list:groups.setdefault(f['dependency_group'],[]).append(f['id'])
    sources=load_input(ROOT/'knowledge/collective_intelligence_sources.json')
    if registry is not None:
        for source in sources:registry.add_source(source)
    result=dict(status='accepted',technique_id=57,schema_version=1,profile=q['profile'],request=q,input_sha256=digest(q),model_sha256=digest(model),split_sha256=digest(split),resolution_sha256=digest({qid:item['resolution'] for qid,item in sorted(qs.items())}),schema_sha256=digest(dict(DATA['schema'])),source_manifest_sha256=DATA['source_manifest_sha256'],source_freeze_sha256=DATA['source_freeze_sha256'],code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),questions=results,primary=summarize(scores['test']),train=summarize(scores['train']),individuals=comparisons,dependence=dict(forecaster_groups=groups,dependent_groups=[g for g,ids in sorted(groups.items()) if len(ids)>1],kind_counts={kind:sum(f['kind']==kind for f in fs.values()) for kind in ['human_declared','synthetic','llm_simulated']},independence_certified=False,effective_sample_size=None),denominators=dict(planned_questions=len(qs),unique_events=len(qs),question_dependency_groups=len({v['definition']['dependency_group'] for v in qs.values()}),forecasters=len(fs),forecaster_dependency_groups=len(groups),revisions=len(q['forecasts']),rejected_revisions=sum(d['decision']=='rejected' for ds in decisions.values() for d in ds),selected_pairs=len(selected),test_scored_questions=len(scores['test']),train_scored_questions=len(scores['train'])),budget=budget,sources=sources,evidence_mode=q['provenance']['evidence_mode'],empirical_skill_validated=False,compatibility_51=dict(profile='tetlock-mellers-binary-forecast-updates-v1',conventions='Exact probabilities,UTC-Z/cutoff-inclusive timing,binary0–1 and two-category0–2 scores,exact decomposition',full_ledger_adapter='unsupported'),limitations=list(DATA['configuration_matrix']['unsupported'])+['Linear-pool software correctness is not proof of independent crowd wisdom or empirical superiority.','Clocks,identities,dependencies,rights and labels are declarations; hashes cannot independently certify them.','Parent chains are local commitments; owner can rewrite all history without an external anchor.','Mellers daily/question-standardized tournament and team-median leaderboard results are not reproduced.'])
    result['report_sha256']=digest(result);return result
def markdown(result):
    body=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False);fence='`'*max(3,1+max([len(x) for x in re.findall(r'`+',body)]+[0]))
    return '# Collective intelligence — offline binary linear pool\n\n'+fence+'json\n'+body+'\n'+fence+'\n'
