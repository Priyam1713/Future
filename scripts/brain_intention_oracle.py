"""Pre-engine independent fixture builder: moments identity and literal geometry.

No production classifier import. This file and its fixture are frozen before engine.
"""
import copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def request(mode='features'):
    p=json.loads((R/'knowledge/brain_intention_profile_v1.json').read_text(encoding='utf-8'))
    q=dict(schema_version=1,profile=dict(id=p['id'],version=1,sha256=digest(p),catalog_sha256=p['source_manifest_sha256']),mode=mode,channels=[dict(id='c0',unit='arbitrary_units')],task='editorial_binary',protocol='subject_disjoint',fit_at=100,filter='none',trials=[],provenance=dict(synthetic=True,source_ref='brain-intention-centroid-v1',rights='self_authored',attribution='Future original synthetic arithmetic example',snapshot='Original synthetic trial table; no human data.'))
    q['provenance']['snapshot_sha256']=hashlib.sha256(q['provenance']['snapshot'].encode()).hexdigest()
    values=[(0,2),(2,4),(4,2),(6,4),(2,3),(4,3),(4,3),(5,3)]
    labels=['A','A','B','B','A','A','B','B']
    for i,(v,label) in enumerate(zip(values,labels)):
        train=i<4;start=i*5
        q['trials'].append(dict(id='t'+str(i),subject='train' if train else 'test',run='r1',session=None,source_id='file-train' if train else 'file-test',trial_id='trial'+str(i),start=start,end=start+4,available_at=50 if train else 110,predict_at=90 if train else 120,label_available_at=80 if train else 130,partition='TRAIN' if train else 'TEST',label=label,annotation=None,values=list(v) if mode=='features' else [[-1,1,-1,1] if label=='A' else [-2,2,-2,2]]))
    return q
def expected(q):
    # Independent E[X²]-E[X]² extraction, explicit sum-of-squares geometry.
    vectors={}
    for t in q['trials']:
        if q['mode']=='features':v=list(map(F,t['values']))
        else:
            v=[]
            for c in t['values']:
                xs=list(map(F,c));m=sum(xs)/len(xs);v += [m,sum(x*x for x in xs)/len(xs)-m*m]
        vectors[t['id']]=v
    train=[t for t in q['trials'] if t['partition']=='TRAIN'];test=sorted([t for t in q['trials'] if t['partition']=='TEST'],key=lambda t:t['id'])
    cs={c:[sum(vectors[t['id']][j] for t in train if t['label']==c)/sum(t['label']==c for t in train) for j in range(len(next(iter(vectors.values()))))] for c in ['A','B']}
    predictions=[];matrix=[[0,0],[0,0]];majority='A' if sum(t['label']=='A' for t in train)>=sum(t['label']=='B' for t in train) else 'B'
    for t in test:
        x=vectors[t['id']];ds={c:sum(xi*xi-2*xi*ci+ci*ci for xi,ci in zip(x,cs[c])) for c in ['A','B']};pred='A' if ds['A']<=ds['B'] else 'B';matrix['AB'.index(t['label'])]['AB'.index(pred)]+=1
        predictions.append(dict(id=t['id'],prediction=pred,distances={c:str(ds[c]) for c in ['A','B']}))
    counts=list(map(sum,matrix));rec=[F(matrix[i][i],counts[i]) if counts[i] else None for i in [0,1]]
    return dict(features={k:list(map(str,v)) for k,v in sorted(vectors.items())},centroids={c:list(map(str,v)) for c,v in cs.items()},predictions=predictions,confusion=matrix,accuracy=str(F(matrix[0][0]+matrix[1][1],len(test))),balanced_accuracy=None if None in rec else str(sum(rec)/2),baseline_accuracy=str(F(sum(t['label']==majority for t in test),len(test))))
def build():
    if (R/'tests/fixtures/brain-intention-independent-v1.json').exists():raise ValueError('Fixture already frozen')
    cases={}
    def add(name,q,good=True):cases[name]=dict(input=q,exit_code=0 if good else 2,expected=expected(q) if good else None)
    q=request();add('worked',q);assert expected(q)['centroids']=={'A':['1','3'],'B':['5','3']};assert expected(q)['confusion']==[[1,1],[0,2]]
    add('windows',request('windows'))
    for name,values in [('constant',[3,3,3,3]),('offset',[4,6,4,6]),('scaled',[-2,2,-2,2]),('rational',['-1/2','1/2','-1/2','1/2'])]:
        x=request('windows');x['trials'][4]['values']=[values];add(name,x)
    x=copy.deepcopy(q);x['trials'][4]['values']=[3,3];add('tie',x)
    x=copy.deepcopy(q)
    for t in x['trials']:
        if t['partition']=='TEST':t['label']='B' if t['label']=='A' else 'A'
    add('test-label-flip',x)
    x=copy.deepcopy(q)
    for t in x['trials']:
        if t['partition']=='TEST':t['label']='A'
    add('absent-class',x)
    x=copy.deepcopy(q);x['protocol']='within_subject_heldout_run'
    for t in x['trials']:t['subject']='s';t['run']='r1' if t['partition']=='TRAIN' else 'r2'
    add('heldout-run',x)
    x=copy.deepcopy(q);x['task']='synthetic_imagined_hands_feet'
    for t in x['trials']:t['run']='6';t['annotation']='T1' if t['label']=='A' else 'T2'
    add('cue-labels',x)
    x=copy.deepcopy(q);x['trials'].reverse();add('reordered',x)
    x=copy.deepcopy(q);x['trials'][7]['partition']='VALIDATION';add('validation-unused',x)
    x=request('windows');x['channels'].append(dict(id='c1',unit='arbitrary_units'))
    for t in x['trials']:t['values'].append([3,3,3,3])
    add('two-channels',x)
    mutations={
      'subject-leak':lambda x:x['trials'][4].update(subject='train'),
      'source-alias':lambda x:x['trials'][4].update(source_id='file-train'),
      'overlap':lambda x:x['trials'][4].update(subject='train',source_id='file-train',start=0,end=4),
      'run-leak':lambda x:x['trials'][4].update(run='r1'),
      'session-claim':lambda x:x['trials'][0].update(session='visit1'),
      'future-data':lambda x:x['trials'][4].update(available_at=121),
      'future-train':lambda x:x['trials'][0].update(label_available_at=101),
      'outcome-known':lambda x:x['trials'][4].update(label_available_at=120),
      'fit-after-predict':lambda x:x.update(fit_at=121),
      'noncausal-filter':lambda x:x.update(filter='zero_phase'),
      'unknown-task':lambda x:x.update(task='readiness_potential'),
      'bad-cue-run':lambda x:x['trials'][0].update(run='4'),
      'bad-cue-label':lambda x:x['trials'][0].update(annotation='T2'),
      'mixed-modality':lambda x:x.update(task='fmri'),
      'bad-units':lambda x:x['channels'][0].update(unit='microvolts'),
      'duplicate-channel':lambda x:x['channels'].append(dict(x['channels'][0])),
      'duplicate-id':lambda x:x['trials'][4].update(id='t0'),
      'bad-partition':lambda x:x['trials'][4].update(partition='TUNE'),
      'one-train-class':lambda x:[t.update(label='A') for t in x['trials'] if t['partition']=='TRAIN'],
      'negative-variance':lambda x:x['trials'][0].update(values=[0,-1]),
      'bad-dimension':lambda x:x['trials'][0].update(values=[1]),
      'boolean':lambda x:x['trials'][0].update(values=[True,1]),
      'float':lambda x:x['trials'][0].update(values=[0.1,1]),
      'decimal-string':lambda x:x['trials'][0].update(values=['0.1',1]),
      'zero-denominator':lambda x:x['trials'][0].update(values=['1/0',1]),
      'large-number':lambda x:x['trials'][0].update(values=[10**18,1]),
      'empirical':lambda x:x['provenance'].update(synthetic=False),
      'rights':lambda x:x['provenance'].update(rights='unknown'),
      'source':lambda x:x['provenance'].update(source_ref='unknown'),
      'snapshot':lambda x:x['provenance'].update(snapshot_sha256='0'*64),
      'profile':lambda x:x['profile'].update(sha256='0'*64),
      'excess-field':lambda x:x.update(mind_reading=True),
      'too-many-trials':lambda x:x.update(trials=x['trials']*33),
      'time-order':lambda x:x['trials'][0].update(end=0),
      'non-null-annotation':lambda x:x['trials'][0].update(annotation='T1')}
    for name,mutate in mutations.items():
        x=copy.deepcopy(cases['heldout-run' if name=='run-leak' else 'cue-labels' if name.startswith('bad-cue') else 'worked']['input']);mutate(x);add(name,x,False)
    x=request('windows');x['trials'][0]['values']=[[1]];add('one-sample',x,False)
    x=request('windows');x['trials'][0]['values']=[[0]*513];add('sample-cap',x,False)
    families={
     'window-mean':['windows'],'population-variance':['windows','rational'],'constant-window':['constant'],'dc-offset':['offset'],'amplitude-scaling':['scaled'],'channel-order-units':['two-channels','bad-units','duplicate-channel'],'training-centroid':['worked'],'squared-distance':['worked'],'exact-tie':['tie'],'train-only-fit':['worked','validation-unused'],'test-label-isolation':['worked','test-label-flip'],'subject-disjoint':['worked','subject-leak'],'heldout-run':['heldout-run','run-leak'],'session-metadata':['session-claim'],'trial-overlap':['overlap'],'duplicate-source':['source-alias'],'cue-run-label-map':['cue-labels','bad-cue-run','bad-cue-label'],'modality-separation':['mixed-modality'],'window-availability':['future-data','future-train','outcome-known','fit-after-predict'],'noncausal-filter-refusal':['noncausal-filter'],'confusion-matrix':['worked'],'matched-majority-baseline':['worked'],'balanced-accuracy':['worked'],'absent-class':['absent-class'],'chance-null':['literal-anchors'],'rights-consent':['empirical','rights','source','snapshot'],'resource-bounds':['sample-cap','too-many-trials','large-number'],'json-markdown-hashes':['reordered','profile']}
    literal=dict(population_variance='1',sample_variance='4/3',centroid_A=['1','3'],centroid_B=['5','3'],distance_A=['1','9'],distance_B=['9','1'],tie=['4','4'],confusion=[[1,1],[0,2]],accuracy='3/4',balanced_accuracy='3/4',baseline_accuracy='1/2',iid_toy_upper_tail='7/128')
    fixture=dict(version=1,technique_id=55,profile_sha256=q['profile']['sha256'],families=families,cases=cases,literal_anchors=literal,independence='Created before engine; Fraction moments identity and expanded quadratic distances; literal centroid/scoring anchors; no production imports.')
    path=R/'tests/fixtures/brain-intention-independent-v1.json';path.write_text(json.dumps(fixture,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    freeze=dict(version=1,fixture_sha256=digest(fixture),oracle_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),fixture_families=28,accepted=sum(c['exit_code']==0 for c in cases.values()),rejected=sum(c['exit_code']==2 for c in cases.values()),literal_anchors=literal)
    (R/'knowledge/brain_intention_fixture_freeze_v1.json').write_text(json.dumps(freeze,indent=2)+'\n',encoding='utf-8',newline='\n');print(freeze)
if __name__=='__main__':build()
