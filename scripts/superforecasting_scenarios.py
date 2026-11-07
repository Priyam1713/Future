"""Original synthetic lifecycle and review cases;no empirical participant data."""
import copy
from future import superforecasting as e
from scripts.superforecasting_oracle import plan,reference_class,forecast,update,resolution,sha,source


def resolved(ps,ys,statuses=None):
    p=plan(len(ps));l=e.create(p)
    for i,prob in enumerate(ps):l=e.append(l,'forecast',forecast(p,i,prob))
    for i,y in enumerate(ys):l=e.append(l,'resolve',resolution(p,i,y,(statuses or ['resolved']*len(ps))[i]))
    return l


def lifecycle():
    p=plan(1);p['questions'][0]['baseline'].update(kind='reference_class',probability='3/10');created=e.create(p);v=forecast(p);first=e.append(created,'forecast',v)
    manual=forecast(p,probability='2/5',version=2,parent=sha(v),at='2025-01-02T12:00:00Z');amended=e.append(first,'forecast',manual)
    u=update(manual,p,at='2025-01-02T18:00:00Z');updated=e.append(amended,'update',u)
    duplicate=update(u,p,at='2025-01-02T19:00:00Z',dependence='independent');attempted=e.append(updated,'update',duplicate,keep_rejected=True)
    late=forecast(p,probability='9/10',version=4,parent=sha(u),at='2025-01-04T00:00:00Z');with_late=e.append(attempted,'forecast',late)
    r=resolution(p);final=e.append(with_late,'resolve',r)
    return dict(plan=p,created=created,original=v,first=first,manual=manual,amended=amended,bayes=u,updated=updated,duplicate=duplicate,attempted=attempted,late=late,with_late=with_late,resolution=r,final=final)


def cases():
    d=lifecycle();p=plan(1);v=forecast(p);first=e.append(e.create(p),'forecast',v);u=update(v,p);updated=e.append(first,'update',u);out={}
    def add(name,task,payload,code=0):out[name]=(e.request(task,payload),code)
    add('question','question',p['questions'][0]);add('class-ten-three','reference-class',reference_class());add('create','create',d['plan'])
    for name,ys in [('empty',[]),('zero',[0]*5),('full',[1]*5),('missing',[None,1,0])]:add('class-'+name,'reference-class',reference_class(ys))
    c=reference_class();c['members'][0]['eligibility']='ambiguous';c['members'][1]['eligibility']='excluded';add('class-ambiguous-excluded','reference-class',c)
    add('original','forecast',dict(ledger=d['created'],record=d['original']));add('manual','forecast',dict(ledger=d['first'],record=d['manual']));add('bayes-after-manual','update',dict(ledger=d['amended'],record=d['bayes']));add('retained-rejected-attempt','attempt',dict(ledger=d['updated'],kind='update',record=d['duplicate'],attempted_at=d['duplicate']['recorded_at']));add('late','forecast',dict(ledger=d['attempted'],record=d['late']));add('resolve','resolve',dict(ledger=d['with_late'],record=d['resolution']));add('lifecycle-report','report',d['final']);add('lifecycle-score','score',d['final']);add('unresolved-report','report',d['created'])
    for name,ratio in [('neutral','1'),('positive','3'),('zero','0')]:add('bayes-'+name,'update',dict(ledger=first,record=update(v,p,ratio=ratio)))
    conditional=update(v,p);conditional['bayes'].update(kind='conditional_likelihoods',ratio=None,likelihood_h='3/5',likelihood_not_h='1/5');add('conditional-likelihoods','update',dict(ledger=first,record=conditional))
    for prob in ('0','1'):
        original=forecast(p,probability=prob);initial=e.append(e.create(p),'forecast',original);add('certain-prior-'+prob,'update',dict(ledger=initial,record=update(original,p)))
    independent=update(u,p,evidence_id='e2',fact='fact2',group='group2',dependence='independent',at='2025-01-02T01:00:00Z');add('independent-new-evidence','update',dict(ledger=updated,record=independent))
    contingent=update(u,p,evidence_id='e2',fact='fact2',dependence='conditional',conditioned_on=['evidence1'],at='2025-01-02T01:00:00Z');add('conditional-history','update',dict(ledger=updated,record=contingent))
    for name,ps,ys in [('paired',['4/5','3/10'],[1,0]),('decomposition',['1/5','1/5','4/5','4/5'],[0,1,1,1]),('calibration',['1/5','1/5'],[0,1]),('brier-one',['9/10'],[1]),('brier-zero',['9/10'],[0]),('log-infinite',['0','1'],[1,0]),('log-correct-endpoints',['0','1'],[0,1]),('log-half',['1/2','1/2'],[0,1]),('negative-event',['1/2'],[0])]:add(name,'report',resolved(ps,ys))
    add('statuses','report',resolved(['1/2']*4,[0,1,0,0],['resolved','resolved','disputed','void']))
    atcut=forecast(p,at=p['questions'][0]['cutoff']);lc=e.append(e.create(p),'forecast',atcut);lc=e.append(lc,'resolve',resolution(p));add('at-cutoff','report',lc)
    post=plan(1);post['questions'][0]['cutoff']='2025-01-07T00:00:00Z';lp=e.append(e.create(post),'forecast',forecast(post,at='2025-01-06T00:00:00Z'));lp=e.append(lp,'resolve',resolution(post));add('post-outcome-retained','report',lp)
    pp=plan(1);pp['slots'].append(dict(forecast_id='f2',question_id='q1',participant='person2',participant_kind='individual'));two=e.create(pp);f=forecast(pp);f2=copy.deepcopy(f);f2.update(forecast_id='f2',participant='person2',probability='4/5');two=e.append(e.append(two,'forecast',f),'forecast',f2);two=e.append(two,'resolve',resolution(pp));add('two-people-one-event','report',two)
    z=copy.deepcopy(d['plan']);z['questions'][0]['reasoning']['disagreement']='  नमस्ते\n```json\n  ';add('unicode-whitespace','create',z)
    for name in e.REFERENCES:add('reference-'+name,'reference',dict(id=name))
    bad=copy.deepcopy(p['questions'][0]);bad['clarity_confirmed']=False;add('reject-ambiguous','question',bad,2)
    bad=reference_class();bad['members'][1]['event_id']=bad['members'][0]['event_id'];add('reject-duplicate-history','reference-class',bad,2)
    for name,path,value in [('unknown-class',['questions',0,'class_id'],'missing'),('class-mutation',['classes',0,'members',0,'outcome'],0),('baseline-leak',['questions',0,'baseline','frozen_at'],'2025-01-04T00:00:00Z'),('reference-leak',['classes',0,'members',0,'dependency_group'],'test1'),('missing-rights',['provenance','rights'],'unknown'),('snapshot-hash',['provenance','snapshot_sha256'],'0'*64),('missing-resolution-source',['questions',0,'resolution','source_ref'],''),('unknown-field',['extra'],True),('empirical-mode',['evidence_mode'],'empirically_validated')]:
        bad=copy.deepcopy(p);value_at=bad
        for k in path[:-1]:value_at=value_at[k]
        value_at[path[-1]]=value;add('reject-'+name,'create',bad,2)
    bad=update(u,p,at='2025-01-02T01:00:00Z',dependence='independent');add('reject-duplicate-evidence','update',dict(ledger=updated,record=bad),2)
    for name,change in [('same-fact',lambda b:b['evidence'][0].update(original_fact_id='fact1')),('same-group',lambda b:b['evidence'][0].update(dependency_group='evidence-group1')),('one-hypothesis-only',lambda b:b['bayes'].update(independent_given_not_h=False)),('negative-ratio',lambda b:b['bayes'].update(ratio='-1')),('wrong-posterior',lambda b:b.update(probability='1/2')),('bad-parent',lambda b:b.update(parent_sha256='0'*64)),('bool-probability',lambda b:b.update(probability=True)),('above-one',lambda b:b.update(probability='11/10')),('nonfinite-probability',lambda b:b.update(probability='NaN')),('both-likelihoods-zero',lambda b:b['bayes'].update(kind='conditional_likelihoods',ratio=None,likelihood_h='0',likelihood_not_h='0'))]:
        bad=copy.deepcopy(independent);change(bad);add('reject-'+name,'update',dict(ledger=updated,record=bad),2)
    bad=copy.deepcopy(contingent);bad['bayes']['conditioned_on']=[];add('reject-conditional-history','update',dict(ledger=updated,record=bad),2)
    one=forecast(p,probability='1');lone=e.append(e.create(p),'forecast',one);bad=update(one,p,ratio='1');bad['bayes']['ratio']='0';bad['probability']='0';add('reject-certain-impossible','update',dict(ledger=lone,record=bad),2)
    bad=copy.deepcopy(d['manual']);bad['parent_sha256']='0'*64;add('reject-amendment-parent','forecast',dict(ledger=d['first'],record=bad),2)
    for name,change in [('negative-early',lambda b:b.update(outcome_known_at='2025-01-09T00:00:00Z')),('negative-invented-occurrence',lambda b:b.update(occurrence_at=b['window_end'])),('resolution-no-source',lambda b:b['source'].update(snapshot_sha256='0'*64))]:
        bad=resolution(p,outcome=0);change(bad);add('reject-'+name,'resolve',dict(ledger=first,record=bad),2)
    bad=copy.deepcopy(d['final']);bad['actions'][0]['record']['probability']='1';add('reject-chain-mutation','report',bad,2)
    rp=plan(1);rl=e.create(rp);r1=resolution(rp);rl=e.append(rl,'resolve',r1)
    unresolved=resolution(rp,status='unresolved',version=2,parent=sha(r1),at='2025-01-12T00:00:00Z');reopened=e.append(rl,'resolve',unresolved)
    correction=resolution(rp,outcome=0,version=3,parent=sha(unresolved),at='2025-01-13T00:00:00Z');add('reject-resolution-unresolved-bypass','resolve',dict(ledger=reopened,record=correction),2)
    dispute=resolution(rp,status='disputed',version=2,parent=sha(r1),at='2025-01-12T00:00:00Z');disputed=e.append(rl,'resolve',dispute);correction=resolution(rp,outcome=0,version=3,parent=sha(dispute),at='2025-01-13T00:00:00Z');add('resolution-correction-after-dispute','resolve',dict(ledger=disputed,record=correction))
    corrected=e.append(disputed,'resolve',correction);reopen=resolution(rp,status='unresolved',version=4,parent=sha(correction),at='2025-01-14T00:00:00Z');reopened=e.append(corrected,'resolve',reopen);stale=resolution(rp,version=5,parent=sha(reopen),at='2025-01-15T00:00:00Z');add('reject-resolution-stale-dispute','resolve',dict(ledger=reopened,record=stale),2)
    q=e.request('report',d['final']);q['profile']['catalog_sha256']='0'*64;out['reject-catalog-hash']=(q,2)
    q=e.request('certify_skill',d['final']);out['reject-empirical-skill']=(q,2)
    return out
