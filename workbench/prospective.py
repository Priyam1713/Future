"""Human binary-event form -> native #51 -> unchanged Future Lab ledger."""
import copy, hashlib
from datetime import datetime
from future import lab, superforecasting as native
from future.lab.common import digest, REGISTRY_HASH

def at(v): return datetime.fromisoformat(v.replace('Z','+00:00'))
def snapshot(text): return hashlib.sha256(text.encode('utf-8')).hexdigest()

def build(values,stamp,identity):
    cutoff,end=values['cutoff'],values['window_end']
    if not at(stamp)<at(cutoff)<at(end): raise ValueError('Cutoff and complete observation window must be in the future')
    for k in ['question','positive_rule','negative_rule','source_ref','evidence','reason']:
        if not isinstance(values.get(k),str) or not values[k].strip():raise ValueError(k+' is required')
    if not values.get('clarity_confirmed'):raise ValueError('Explicit binary clarity confirmation required')
    def source(id):
        text=values['evidence']
        return dict(id=id,locator=values['source_ref'],rights='self_authored',attribution='Local researcher declaration, not independently authenticated',snapshot=text,snapshot_sha256=snapshot(text),available_at=stamp)
    question=dict(id='q1',version=1,event_id=identity,dependency_group=identity,partition='test',text=values['question'],event_definition=values['question'],window_start=cutoff,window_end=end,cutoff=cutoff,created_at=stamp,locked_at=stamp,timezone='UTC',clarity_confirmed=True,resolution=dict(source_ref=values['source_ref'],positive_rule=values['positive_rule'],negative_rule=values['negative_rule'],dispute_policy='Unscored while disputed; independent evidence required',void_policy='Unscored void annotation; never a binary outcome'),class_id=None,class_sha256=None,baseline=dict(kind='constant',probability='1/2',frozen_at=stamp,domain='user-declared-events',horizon='fixed-window',source=source('baseline')),reasoning={k:[] if k in ['assumptions','subquestions','evidence_gaps','alternatives'] else values['reason'] for k in ['base_rate_rationale','comparability','assumptions','subquestions','evidence_gaps','alternatives','dependence','disagreement']},source=source('question'))
    plan=dict(study_id=identity,created_at=stamp,evidence_mode='user_supplied_unvalidated',domain='user-declared-events',horizon='fixed-window',partition=dict(frozen_at=stamp,train_groups=[],test_groups=[identity]),questions=[question],classes=[],slots=[dict(forecast_id='f1',question_id='q1',participant='local-forecaster',participant_kind='individual')],provenance=source('protocol'))
    record=dict(forecast_id='f1',question_id='q1',question_version=1,question_sha256=digest(question),participant='local-forecaster',version=1,parent_sha256=None,recorded_at=stamp,knowledge_at=stamp,probability=values['probability'],mode='manual',reason=values['reason'],evidence=[],assumptions=['User-supplied unvalidated judgment'],outcome_known=False,bayes=None)
    nl=native.append(native.create(plan),'forecast',record)
    request=native.request('report',nl); entry=lab.capability(51)
    p=dict(schema_version=1,id=identity,version=1,parent_ledger_sha256=None,mode='declared_prospective',created_at=stamp,cutoff=cutoff,technique_id=51,operation='superforecasting',registry_sha256=REGISTRY_HASH,profile_identifiers=entry['profile_identifiers'],target_definition=values['question'],target_unit='binary_event',dataset=dict(id=identity,version=1,rights='self_authored',attribution='Local researcher declaration',snapshot=values['evidence'],snapshot_sha256=snapshot(values['evidence']),available_at=stamp,source_vintage=dict(status='declared_as_of',retrieved_at=stamp,notes='User declaration; external vintage not certified')),splits=[dict(id='q1',group=identity,partition='test',available_at=end)],selection=dict(frozen_at=stamp,model_id='native_forecast_versions',native_input_sha256=digest(request),training_ids=[],validation_ids=[]),native_input=request,targets=[dict(id='q1',native_key='f1',event_id=identity,dependency_group=identity,target_at=end)],metric='brier',baseline='fixed_half')
    return lab.forecast(lab.create(p),stamp)
