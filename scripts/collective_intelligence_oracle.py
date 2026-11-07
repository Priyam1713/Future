"""Pre-engine literal revision choices and independent exact pooling anchors."""
import copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def question(qid='q1',event='event1',partition='test',outcome=1):
    return dict(definition=dict(id=qid,version=1,event_id=event,dependency_group='group-'+event,partition=partition,text='Does synthetic event '+event+' occur?',positive_rule='Declared synthetic outcome1',negative_rule='Declared synthetic outcome0 at event end',clarity_confirmed=True,created_at='2025-01-01T00:00:00Z',locked_at='2025-01-02T00:00:00Z',cutoff='2025-01-10T00:00:00Z',event_end='2025-01-20T00:00:00Z'),resolution=dict(status='resolved',outcome=outcome,event_at='2025-01-20T00:00:00Z',outcome_known_at='2025-01-20T00:00:00Z',resolved_at='2025-01-21T00:00:00Z'))
def append(q,fid,probability,issued='2025-01-05T00:00:00Z',knowledge='2025-01-04T00:00:00Z',qid='q1'):
    prior=[r for r in q['forecasts'] if r['question_id']==qid and r['forecaster']==fid];d=next(a['definition'] for a in q['questions'] if a['definition']['id']==qid)
    q['forecasts'].append(dict(question_id=qid,question_sha256=digest(d),forecaster=fid,revision=len(prior)+1,parent_sha256=digest(prior[-1]) if prior else None,issued_at=issued,knowledge_at=knowledge,probability=probability))
def request():
    p=json.loads((R/'knowledge/collective_intelligence_profile_v1.json').read_text(encoding='utf-8'));snapshot='Self-authored fictional probability records; no participant data.'
    q=dict(schema_version=1,profile=dict(id=p['id'],version=1,sha256=digest(p),catalog_sha256=p['source_manifest_sha256']),pool=dict(kind='equal',frozen_at='2025-01-03T00:00:00Z',weights_available_at='2025-01-03T00:00:00Z'),forecasters=[dict(id=f,kind='synthetic',dependency_group='person-'+f,weight='1') for f in ['fa','fb']],questions=[question()],forecasts=[],provenance=dict(evidence_mode='synthetic',source_ref='collective-intelligence-mellers-author-v1',rights='self_authored',attribution='Future original fictional forecast example',snapshot=snapshot,snapshot_sha256=hashlib.sha256(snapshot.encode()).hexdigest()))
    append(q,'fa','1/5');append(q,'fb','4/5');return q
def expected(q,choices=None):
    # Revision choices supplied literally by each case; no chronology/eligibility algorithm here.
    qs={a['definition']['id']:a for a in q['questions']};fs={a['id']:a for a in q['forecasters']};rows={};scores=[];individuals={f:[] for f in fs}
    for qid,item in sorted(qs.items()):
        chosen={};probs={};weights={};versions={}
        for fid in sorted(fs):
            v=choices.get(qid,{}).get(fid,1) if choices is not None else 1
            found=next((r for r in q['forecasts'] if r['question_id']==qid and r['forecaster']==fid and r['revision']==v),None) if v is not None else None
            versions[fid]=found['revision'] if found else None;probs[fid]=None if found is None or found['probability'] is None else F(found['probability']);weights[fid]=F(fs[fid]['weight'])
        active=[f for f in fs if probs[f] is not None and weights[f]>0];present=[f for f in fs if probs[f] is not None];den=sum(weights[f] for f in active)
        pool=sum(weights[f]*probs[f] for f in active)/den if den else None;equal=sum(probs[f] for f in present)/len(present) if present else None
        norm={f:str(weights[f]/den) if f in active else '0' for f in sorted(fs)}
        rows[qid]=dict(probability=None if pool is None else str(pool),equal_probability=None if equal is None else str(equal),selected_versions=versions,normalized_weights=norm,selected_probabilities={f:None if p is None else str(p) for f,p in probs.items()})
        if item['definition']['partition']=='test' and item['resolution']['status']=='resolved' and pool is not None:
            y=item['resolution']['outcome'];scores.append((qid,(pool-y)**2,(equal-y)**2))
            for f in fs:
                if probs[f] is not None:individuals[f].append((qid,(probs[f]-y)**2,(pool-y)**2))
    primary=dict(count=len(scores),question_ids=[a[0] for a in scores],binary_brier=str(sum(a[1] for a in scores)/len(scores)) if scores else None,two_category_brier=str(2*sum(a[1] for a in scores)/len(scores)) if scores else None,equal_pool_brier=str(sum(a[2] for a in scores)/len(scores)) if scores else None,half_baseline_brier='1/4' if scores else None)
    matched={f:dict(question_ids=[a[0] for a in v],count=len(v),individual_brier=str(sum(a[1] for a in v)/len(v)) if v else None,aggregate_brier=str(sum(a[2] for a in v)/len(v)) if v else None) for f,v in sorted(individuals.items())}
    return dict(questions=rows,primary=primary,individuals=matched)
def build():
    path=R/'tests/fixtures/collective-intelligence-independent-v1.json'
    if path.exists():raise ValueError('Immutable fixture exists')
    cases={}
    def add(name,q,good=True,choices=None):cases[name]=dict(input=q,exit_code=0 if good else 2,expected=expected(q,choices) if good else None)
    q=request();add('equal',q);assert expected(q)['questions']['q1']['probability']=='1/2'
    x=request();x['pool']['kind']='declared_weight';x['forecasters'][1]['weight']='3';add('weighted',x);assert expected(x)['questions']['q1']['probability']=='13/20' and expected(x)['primary']['binary_brier']=='49/400'
    y=copy.deepcopy(x);y['forecasters'][0]['weight']='7';y['forecasters'][1]['weight']='21';add('weight-scale',y)
    x=request();x['forecasts'].pop();add('missing',x,choices={'q1':{'fa':1,'fb':None}})
    x=request();x['forecasters'].append(dict(id='fc',kind='synthetic',dependency_group='person-fc',weight='1'));add('unsubmitted-roster',x,choices={'q1':{'fa':1,'fb':1,'fc':None}})
    x=request();append(x,'fa',None,'2025-01-06T00:00:00Z');add('abstention',x,choices={'q1':{'fa':2,'fb':1}})
    x=request();append(x,'fa','2/5','2025-01-06T00:00:00Z');add('revision',x,choices={'q1':{'fa':2,'fb':1}})
    x=request();append(x,'fa','2/5','2025-01-10T00:00:00Z');add('cutoff-equality',x,choices={'q1':{'fa':2,'fb':1}})
    x=request();append(x,'fa','9/10','2025-01-10T00:00:01Z');add('late-revision',x)
    x=request();x['questions'][0]['resolution'].update(event_at='2025-01-07T00:00:00Z',outcome_known_at='2025-01-07T00:00:00Z');append(x,'fa','9/10','2025-01-08T00:00:00Z');add('informed-revision',x)
    x=request();x['pool']['kind']='declared_weight';x['forecasters'][0]['weight']='0';add('zero-weight',x)
    x=copy.deepcopy(x);x['forecasts'].pop();add('no-positive-available',x,choices={'q1':{'fa':1,'fb':None}})
    x=request();x['forecasts']=[];add('no-forecasts',x,choices={'q1':{'fa':None,'fb':None}})
    x=request();x['questions'][0]['resolution']['outcome']=0;add('outcome-flip',x)
    x=request()
    for f in x['forecasters']:f['dependency_group']='shared'
    add('dependent',x)
    x=request()
    for f in x['forecasters']:f['kind']='llm_simulated';f['dependency_group']='shared-model'
    add('llm',x)
    x=request();x['provenance'].update(evidence_mode='user_supplied_unvalidated',rights='permission_granted')
    for f in x['forecasters']:f['kind']='human_declared'
    add('unvalidated-declared',x)
    x=request();x['questions'].append(question('q2','event2','train',0));append(x,'fa','1/5',qid='q2');append(x,'fb','1/5',qid='q2');add('train-test',x)
    for status in ['unresolved','void','disputed']:
        x=request();r=x['questions'][0]['resolution'];r.update(status=status,outcome=None,event_at=None,outcome_known_at=None if status=='unresolved' else '2025-01-20T00:00:00Z',resolved_at=None if status=='unresolved' else '2025-01-21T00:00:00Z');add(status,x)
    for name,probs,labels in [('decomposition',['1/5','1/5','4/5','4/5'],[0,1,0,1]),('perfect',['0','1'],[0,1]),('contradicted',['1','0'],[0,1])]:
        x=request();x['questions']=[];x['forecasts']=[]
        for i,(prob,label) in enumerate(zip(probs,labels)):
            qid='q'+str(i+1);x['questions'].append(question(qid,'event'+str(i+1),outcome=label));append(x,'fa',prob,qid=qid);append(x,'fb',prob,qid=qid)
        add(name,x)
    x=request();x['forecasters'].reverse();x['forecasts'].reverse();add('reordered',x)
    mutations={
     'all-zero-weights':lambda x:[f.update(weight='0') for f in x['forecasters']],
     'negative-weight':lambda x:x['forecasters'][0].update(weight='-1'),
     'ignored-equal-weights':lambda x:x['forecasters'][0].update(weight='2'),
     'float-probability':lambda x:x['forecasts'][0].update(probability=0.2),
     'boolean-probability':lambda x:x['forecasts'][0].update(probability=True),
     'out-of-range':lambda x:x['forecasts'][0].update(probability='6/5'),
     'zero-denominator':lambda x:x['forecasts'][0].update(probability='1/0'),
     'large-rational':lambda x:x['forecasts'][0].update(probability=10**18),
     'duplicate-forecaster':lambda x:x['forecasters'].append(copy.deepcopy(x['forecasters'][0])),
     'duplicate-revision':lambda x:x['forecasts'].append(copy.deepcopy(x['forecasts'][0])),
     'unknown-forecaster':lambda x:x['forecasts'][0].update(forecaster='unknown'),
     'unknown-question':lambda x:x['forecasts'][0].update(question_id='unknown'),
     'question-hash':lambda x:x['forecasts'][0].update(question_sha256='0'*64),
     'initial-parent':lambda x:x['forecasts'][0].update(parent_sha256='0'*64),
     'revision-gap':lambda x:x['forecasts'][0].update(revision=2),
     'future-knowledge':lambda x:x['forecasts'][0].update(knowledge_at='2025-01-06T00:00:00Z'),
     'future-weights':lambda x:x['pool'].update(weights_available_at='2025-01-04T00:00:00Z'),
     'after-cutoff-weights':lambda x:x['pool'].update(frozen_at='2025-01-11T00:00:00Z'),
     'outcome-bool':lambda x:x['questions'][0]['resolution'].update(outcome=True),
     'outcome-before-weights':lambda x:x['questions'][0]['resolution'].update(event_at='2025-01-03T00:00:00Z',outcome_known_at='2025-01-03T00:00:00Z'),
     'duplicate-question':lambda x:x['questions'].append(copy.deepcopy(x['questions'][0])),
     'unclear-question':lambda x:x['questions'][0]['definition'].update(clarity_confirmed=False),
     'offset-time':lambda x:x['pool'].update(frozen_at='2025-01-03T00:00:00+00:00'),
     'synthetic-human':lambda x:x['forecasters'][0].update(kind='human_declared'),
     'source':lambda x:x['provenance'].update(source_ref='unknown'),
     'rights':lambda x:x['provenance'].update(rights='unknown'),
     'snapshot':lambda x:x['provenance'].update(snapshot_sha256='0'*64),
     'profile':lambda x:x['profile'].update(sha256='0'*64),
     'extra-field':lambda x:x.update(learn_weights=True),
     'forecast-cap':lambda x:x.update(forecasts=x['forecasts']*1025),
     'roster-cap':lambda x:x.update(forecasters=[dict(id='f'+str(i),kind='synthetic',dependency_group='g'+str(i),weight='1') for i in range(33)])}
    for name,change in mutations.items():x=request();change(x);add(name,x,False)
    x=request();append(x,'fa','2/5','2025-01-06T00:00:00Z');x['forecasts'][-1]['parent_sha256']='0'*64;add('broken-parent',x,False)
    x=request();append(x,'fa','2/5','2025-01-04T00:00:00Z');add('nonmonotonic-revision',x,False)
    x=request();x['questions'].append(question('q2','event1'));add('duplicate-event',x,False)
    x=request();q2=question('q2','event2','train');q2['definition']['dependency_group']=x['questions'][0]['definition']['dependency_group'];x['questions'].append(q2);add('cross-partition-dependence',x,False)
    families={'equal-pool':['equal'],'weighted-pool':['weighted'],'weight-normalization':['weighted'],'weight-scale-invariance':['weighted','weight-scale'],'missing-forecaster':['missing','unsubmitted-roster'],'abstention-withdrawal':['abstention'],'zero-weight':['zero-weight'],'all-zero-roster':['all-zero-weights'],'all-missing-positive-weight':['no-positive-available','no-forecasts'],'revision-latest':['revision'],'cutoff-inclusive':['cutoff-equality'],'late-revision-refusal':['late-revision'],'duplicate-revision':['duplicate-revision'],'parent-chain':['broken-parent','initial-parent','revision-gap'],'question-identity':['question-hash','duplicate-event'],'outcome-information-gate':['informed-revision','outcome-before-weights'],'outcome-label-isolation':['equal','outcome-flip'],'dependency-reporting':['dependent'],'llm-not-independent':['llm'],'binary-brier':['weighted'],'two-category-scale':['weighted','decomposition'],'exact-decomposition':['decomposition'],'certainty-boundaries':['perfect','contradicted'],'matched-individual-comparison':['missing','train-test'],'baseline-comparison':['weighted'],'heldout-partition':['train-test','cross-partition-dependence'],'unresolved-exclusion':['unresolved','void','disputed'],'canonical-order':['reordered'],'rights-provenance':['unvalidated-declared','synthetic-human','source','rights','snapshot'],'resource-bounds':['forecast-cap','roster-cap','large-rational'],'raw-json-markdown-replay':['profile','reordered']}
    literal=dict(equal='1/2',weighted='13/20',normalized_weights=['1/4','3/4'],weighted_binary_brier='49/400',weighted_two_category_brier='49/200',equal_binary_brier='1/4',individual_losses=['16/25','1/25'],decomposition=dict(binary_brier='17/50',reliability='9/100',resolution='0',uncertainty='1/4',two_category_brier='17/25'),perfect='0',contradicted='1')
    assert expected(cases['decomposition']['input'])['primary']['binary_brier']=='17/50'
    out=dict(version=1,technique_id=57,profile_sha256=q['profile']['sha256'],families=families,cases=cases,literal_anchors=literal,independence='Created before production. Revision choices are explicit case literals; independent Fraction weighted sums and direct outcome squared errors. No production imports or selection algorithm used.')
    path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');freeze=dict(version=1,fixture_sha256=digest(out),oracle_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),fixture_families=len(families),accepted=sum(c['exit_code']==0 for c in cases.values()),rejected=sum(c['exit_code']==2 for c in cases.values()),literal_anchors=literal)
    (R/'knowledge/collective_intelligence_fixture_freeze_v1.json').write_text(json.dumps(freeze,indent=2)+'\n',encoding='utf-8',newline='\n');print(freeze)
if __name__=='__main__':build()
