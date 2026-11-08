"""Source-derived capability discovery and pinned selected-entry validation."""
import copy
from .common import ROOT,REGISTRY_HASH,IntegrityError,LabError,code_sha,digest,integer,load_input
def registry():
    r=load_input(ROOT/'data/future-lab-capability-registry.json')
    if digest(r)!=REGISTRY_HASH:raise IntegrityError('Capability registry hash mismatch')
    if len(r['entries'])!=54 or [e['technique_id'] for e in r['entries']]!=[i for i in range(1,61) if i not in r['excluded_ids']]:raise IntegrityError('Capability inventory mismatch')
    return r
def list_techniques():return [dict(technique_id=e['technique_id'],name=e['name'],capability_type=e['capability_type'],operations=[o['command'] for o in e['operations']],evaluation=e['evaluation']) for e in registry()['entries']]
def capability(technique_id,verify=True):
    integer(technique_id,1,60);r=registry()
    if technique_id in r['excluded_ids']:raise LabError('Technique is explicitly excluded from retained scope')
    e=next(x for x in r['entries'] if x['technique_id']==technique_id)
    if verify:
        if digest(load_input(ROOT/e['core_record']))!=e['core_sha256']:raise IntegrityError('Frozen core release hash mismatch')
        for source in e['sources']:
            if digest(load_input(ROOT/source['path']))!=source['sha256']:raise IntegrityError('Native source catalog hash mismatch')
        for p in e['profiles']:
            if digest(load_input(ROOT/p['path']))!=p['sha256']:raise IntegrityError('Native profile hash mismatch')
        for o in e['operations']:
            if code_sha(o['implementation_file'])!=o['implementation_sha256']:raise IntegrityError('Native implementation hash mismatch')
    return copy.deepcopy(e)
