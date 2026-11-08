"""Unmodified #49 retrospective reference; never a new held-out result."""
from .common import ROOT,LabError,digest,load_input
from .invocation import invoke
def noaa_reference():
    core=load_input(ROOT/'knowledge/ai_predictive_modeling_core_v1.json')
    request=dict(technique_id=49,operation='ai-predictive-modeling',input=dict(schema_version=1,task='benchmark',profile=core['profile'],profile_version=1));result=invoke(request)
    if result['native_error'] is not None:raise LabError('Frozen NOAA benchmark failed: '+str(result['native_error']))
    native=result['native_output'];evaluation=native['result']['evaluation'];selected=evaluation['primary_selected_test'];original=core['selected_test']
    if evaluation['selection']['selected']!='drift' or selected['aggregate']['mae']!=original['aggregate']['mae'] or selected['paired_seasonal_naive']!=original['paired_seasonal_naive'] or native['result']['dataset_sha256']!=core['normalized_workbench_dataset_sha256']:raise LabError('Frozen unfavorable NOAA reference changed')
    r=dict(schema_version=1,mode='retrospective_reference_replay',visibly_synthetic=False,technique_id=49,native_invocation=result,frozen_core_record='knowledge/ai_predictive_modeling_core_v1.json',frozen_core_sha256=digest(core),primary_result=core['primary_result'],selection='Original validation-selected drift; exposed test diagnostics do not retune or reselect.',source_vintage_certified=False,new_held_out_result=False,empirical_superiority_certified=False,limits=['This reproduces one previously exposed retrospective NOAA benchmark.','Any new superiority claim requires a separately frozen untouched period and appropriate data-vintage protocol.','Overlapping forecast cells are not independent trials.'])
    r['report_sha256']=digest(r);return r
