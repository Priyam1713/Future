"""Versioned Roman historical condition comparison; no physical specimen required."""
import copy
import html
import itertools
import json
import re
from pathlib import Path
from .knowledge import Rule
from .scrying import freeze, digest, _object, _optional_text, load_input

ROOT = Path(__file__).resolve().parents[1]
PROFILE = 'cicero-falconer1923-roman-entrail-references-v1'
PROFILE_HASH = '44b5d1c3c779c1308ac6d929d593ac8d87cbc98cd51cace967dc423088ac2dd6'
DATA = freeze(load_input(ROOT / 'knowledge/haruspicy_roman_profile_v1.json'))
CATALOG_HASH = DATA['catalog_sha256']

def assets():
    p = load_input(ROOT / 'knowledge/haruspicy_roman_profile_v1.json')
    c = load_input(ROOT / 'knowledge/haruspicy_catalog_v1.json')
    if digest(p) != PROFILE_HASH or digest(c) != CATALOG_HASH:
        raise ValueError('Pinned Haruspicy profile/catalog integrity mismatch')
    if digest(c['sources']) != p['source_manifest_sha256']:
        raise ValueError('Pinned source manifest mismatch')
    return p, c

def integrity():
    p,c = assets()
    return dict(verified=True, profile_sha256=PROFILE_HASH, catalog_sha256=CATALOG_HASH,
                source_manifest_sha256=p['source_manifest_sha256'], records=len(c['records']))

def lookup(identifier):
    if not isinstance(identifier,str): raise ValueError('Exact Roman reference ID required')
    found = [r for r in assets()[1]['records'] if r['id'] == identifier]
    if not found: raise ValueError('Unknown Roman reference ID')
    return found[0]

def _identifier(value):
    return isinstance(value,str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',value) is not None

def validate(value):
    if not isinstance(value,dict): raise ValueError('Expected request object')
    task = value.get('task')
    selector = ['observations'] if task == 'compare' else ['reference_ids'] if task == 'reference' else []
    _object(value,['schema_version','profile','mode','task','catalog_id','catalog_version','catalog_sha256','question','reflection','notes']+selector)
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1 or value.get('profile') != PROFILE or value.get('mode') != 'manual':
        raise ValueError('Exact Roman profile,manual mode and integer schema_version1 required')
    if value.get('catalog_id') != DATA['catalog_id'] or type(value.get('catalog_version')) is not int or value['catalog_version'] != 1 or value.get('catalog_sha256') != CATALOG_HASH:
        raise ValueError('Exact Roman catalog ID,integer version1 and pinned hash required;foreign catalogs unsupported')
    if task not in ('compare','reference','catalog'): raise ValueError('Supported tasks:compare,reference,catalog;prediction and ritual procedures unsupported')
    for key in ('question','reflection','notes'): _optional_text(value,key,10000)
    if task == 'reference':
        ids = value.get('reference_ids')
        if not isinstance(ids,list) or not 1 <= len(ids) <= 9: raise ValueError('One to9 reference IDs required')
        for i in ids: lookup(i)
        if len(set(ids)) != len(ids): raise ValueError('Duplicate reference IDs rejected')
    if task == 'compare':
        rows = value.get('observations')
        if not isinstance(rows,list) or not 1 <= len(rows) <= 8: raise ValueError('One to8 ordered observations required')
        ids = set()
        for o in rows:
            _object(o,['observation_id','origin',*DATA['required_fields'],'source_qualification','uncertainty','raw_observation','user_association','sequence','uncertain_fields','contradictory_assertions','presence_reports','other_vitals_reports'])
            identifier = o.get('observation_id')
            if not _identifier(identifier) or identifier in ids: raise ValueError('Distinct bounded ASCII observation_id required')
            ids.add(identifier)
            for key,domain in DATA['domains'].items():
                if key in o and (not isinstance(o[key],str) or o[key] not in domain): raise ValueError('Unsupported '+key)
            if 'origin' in o and (not isinstance(o['origin'],str) or o['origin'] not in DATA['origins']): raise ValueError('Unsupported origin')
            if o.get('prior_observation_id') is not None and not _identifier(o['prior_observation_id']): raise ValueError('Invalid predecessor ID')
            for key in ('source_qualification','uncertainty','raw_observation','user_association'): _optional_text(o,key,10000)
            for key in ('uncertain_fields','presence_reports','other_vitals_reports','sequence'):
                values = o.get(key,[])
                if not isinstance(values,list) or len(values)>12: raise ValueError('Bounded list required: '+key)
                if key == 'sequence':
                    for x in values: _optional_text({'text':x},'text',2000)
                    if any(x is None for x in values): raise ValueError('Sequence entries must be text')
                else:
                    domain = DATA['required_fields'] if key == 'uncertain_fields' else DATA['domains'][key.removesuffix('_reports')]
                    if any(not isinstance(x,str) or x not in domain for x in values): raise ValueError('Unknown '+key)
                    if key == 'uncertain_fields' and len(values)!=len(set(values)): raise ValueError('Duplicate uncertain fields rejected')
            assertions = o.get('contradictory_assertions',{})
            _object(assertions,DATA['domains'])
            for key,values in assertions.items():
                if not isinstance(values,list) or not 1<=len(values)<=12 or any(not isinstance(x,str) or x not in DATA['domains'][key] for x in values): raise ValueError('Invalid contradictory assertions')
    return copy.deepcopy(value)

def evaluate_all(observations):
    p,c = assets()
    fields = p['required_fields']
    prepared=[]
    for o in observations:
        effective={k:o.get(k,'unknown') or 'unknown' for k in fields}
        for k in o.get('uncertain_fields',[]): effective[k]='unknown'
        assertions = copy.deepcopy(o.get('contradictory_assertions',{}))
        for k in ('presence','other_vitals'): assertions[k] = assertions.get(k,[]) + o.get(k+'_reports',[])
        conflicts=[]
        for k,values in assertions.items():
            known=set(values+[o.get(k,'unknown')])-{'unknown'}
            if len(known)>1: conflicts.append(k)
        prepared.append((effective,conflicts))
    results=[]
    # Local case evaluation is separate from resolving the only supported sequence link.
    for index,o in enumerate(observations):
        e,conflicts=prepared[index]
        unsupported=e['tradition'] not in ('roman','unknown')
        evaluations=[]
        for r in c['records']:
            terms=r['conditions']
            if terms is None: continue
            missing=[k for k in terms if e[k]=='unknown']
            mismatch=[k for k,v in terms.items() if e[k]!='unknown' and e[k]!=v]
            relevant=[k for k in conflicts if k in terms]
            reason=None
            if unsupported: status='unsupported'
            elif mismatch: status='not_applicable'
            elif relevant: status='conflicting_evidence'
            elif missing: status='insufficient_evidence'
            else: status='applicable'
            if r['requires_preceding_case'] and status=='applicable':
                prior=e['prior_observation_id']
                linked=next((i for i,x in enumerate(observations) if x['observation_id']==prior),None)
                if prior=='unknown' or linked is None:
                    status='insufficient_evidence'; missing.append('prior_observation_id');reason='Named predecessor is missing or unknown'
                elif linked>=index:
                    status='not_applicable';reason='Predecessor must occur earlier in declared request order'
                else:
                    previous=next(x for x in results[linked]['evaluations'] if x['rule_id']==r['requires_preceding_case'])
                    status=previous['status']
                    reason='Explicit earlier heart account: '+status
            evaluations.append(dict(rule_id=r['id'],status=status,condition_satisfied=status=='applicable',missing_fields=missing,mismatched_fields=mismatch,conflicting_fields=relevant,sequence_reason=reason,source_record=r))
        statuses=[x['status'] for x in evaluations]
        overall='conflicting_evidence' if conflicts else 'unsupported' if unsupported else 'applicable' if 'applicable' in statuses else 'conflicting_evidence' if 'conflicting_evidence' in statuses else 'insufficient_evidence' if 'insufficient_evidence' in statuses else 'not_applicable'
        applicable=[x['rule_id'] for x in evaluations if x['status']=='applicable']
        results.append(dict(observation_id=o['observation_id'],declared=copy.deepcopy(o),effective_fields=e,structured_conflicts=conflicts,status=overall,evaluations=evaluations,applicable_ids=applicable,
            matched_source_accounts=[x['source_record'] for x in evaluations if x['status']=='applicable'],documentary_sequence_complete='caesar-liver-next-day' in applicable,
            historical_polarities=[dict(reference_id=x['rule_id'],source_polarity=x['source_record']['source_polarity'],attribution=x['source_record']['attribution']) for x in evaluations if x['status']=='applicable'],
            empirical_prediction=None,anatomical_diagnosis=None,modern_anatomical_mapping=None,ritual_authority=False))
    return results

def register_knowledge(registry):
    _,c=assets()
    for s in c['sources']: registry.add_source(s)
    for r in c['records']:
        registry.add_rule(Rule('haruspicy.'+r['id'],1,39,'Roman entrail reading',PROFILE,r['source_id'],r['locator'],r['source_account'],'haruspicy_source_condition' if r['conditions'] else 'haruspicy_context_reference',dict(reference_id=r['id']),'proposed','traditional',[]))

def read(value,registry=None):
    p,c=assets(); q=validate(value)
    if registry is not None: register_knowledge(registry)
    observations=evaluate_all(q.get('observations',[]))
    refs=[lookup(i) for i in q['reference_ids']] if q['task']=='reference' else c['records'] if q['task']=='catalog' else []
    items=[dict(kind='observation',id=o['observation_id'],applicable_ids=o['applicable_ids']) for o in observations] or [dict(kind='source_reference',id=r['id'],speaker=r['speaker'],source_account=r['source_account']) for r in refs]
    comparisons=[dict(left=a,right=b,combined_omen=None,score=None,qualification='Side-by-side documentary comparison;accounts retain independent scope') for a,b in itertools.combinations(items,2)]
    return dict(schema_version=1,technique_id=39,profile=PROFILE,catalog_id=p['catalog_id'],catalog_version=1,mode='manual',task=q['task'],sources=c['sources'],observations=observations,references=refs,comparisons=comparisons,
        context_references=[r for r in c['records'] if r['conditions'] is None],translation_notes=c['translation_notes'],conventions=p['conventions'],evaluation_policy=p['priority'],
        user_text={k:q[k] for k in ('question','reflection','notes') if k in q},
        evidence_matrix=dict(direct='Source-located historical accounts,reported practitioner beliefs and critical dialogue',user_attributed='Declared observations,source terms,context,chronology and raw personal text;not independently authenticated',editorial='Exact predicate matching,unknown/conflict statuses and explicit ordered-link safeguards',unsupported='Factual future,death,financial or clinical conclusions,supernatural validation,modern anatomy identification or animal-ritual authority'),
        variation_matrix=dict(supported=p['supported'],experimental=p['experimental'],unsupported=p['unsupported']),qualification=p['qualification'],rights=p['rights'],
        replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,catalog_sha256=CATALOG_HASH,source_manifest_sha256=p['source_manifest_sha256'],source_snapshot_sha256={s['id']:s['snapshot_sha256'] for s in c['sources']},serialization='Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw text preserved',external_calls=False,rng=False,integrity_checked=True))

def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2)
        fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Haruspicy: Roman historical source comparison','',result['qualification'],'','Profile: '+PROFILE]
    for o in result['observations']: lines+=['',f'## {o["observation_id"]}: {o["status"]}','',block(dict(declared=o['declared'],applicable_ids=o['applicable_ids'],historical_polarities=o['historical_polarities']))]
    for title,key in [('Source editions and rights','sources'),('Complete observation evaluation','observations'),('Selected source references','references'),('Neutral documentary comparison','comparisons'),('Marcus criticism and historical context','context_references'),('Latin translation qualifications','translation_notes'),('Frozen conventions','conventions'),('Evaluation policy','evaluation_policy'),('Raw user text','user_text'),('Evidence layers','evidence_matrix'),('Variation support','variation_matrix'),('Rights','rights'),('Exact replay metadata','replay')]: lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'

def rejection(message,fmt):
    if fmt=='json': return json.dumps(dict(status='rejected',error=str(message),haruspicy_report=None),indent=2)
    return '# Haruspicy request rejected\n\n'+html.escape(str(message))+'\n'
