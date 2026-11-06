"""Cicero/Falconer1923 manual Roman source-condition reference; no predictive judgment."""
import copy,html,itertools,json,re
from pathlib import Path
from .knowledge import Rule
from .scrying import freeze,thaw,digest,_object,_optional_text,_raw,load_input
ROOT=Path(__file__).resolve().parents[1]
PROFILE='cicero-falconer1923-roman-bird-signs-v1'
PROFILE_HASH='47b427d3b058085f06dcb9e7265840d7df53a0ea378c4553bd6cfe4dc43d25c1'
DATA=freeze(load_input(ROOT/'knowledge/augury_profile_v1.json'))
CATALOG_HASH=DATA['catalog_sha256']

def assets():
    p=load_input(ROOT/'knowledge/augury_profile_v1.json');c=load_input(ROOT/'knowledge/augury_catalog_v1.json')
    if digest(p)!=PROFILE_HASH or digest(c)!=CATALOG_HASH:raise ValueError('Pinned Augury profile/catalog integrity mismatch; no changed edition/source/order substitution')
    if digest(c['sources'])!=p['source_manifest_sha256']:raise ValueError('Pinned source manifest mismatch')
    return p,c

def integrity():
    p,c=assets();return dict(verified=True,profile_sha256=PROFILE_HASH,catalog_sha256=CATALOG_HASH,source_manifest_sha256=p['source_manifest_sha256'],records=len(c['records']))

def lookup(identifier):
    if not isinstance(identifier,str):raise ValueError('Exact source reference ID required')
    matches=[r for r in assets()[1]['records'] if r['id']==identifier]
    if not matches:raise ValueError('Unknown Roman source reference ID')
    return matches[0]

def _enum(o,key,values,default):
    if key in o and (not isinstance(o[key],str) or o[key] not in values):raise ValueError('Unsupported '+key)
    return o.get(key,default)

def validate(value):
    if not isinstance(value,dict):raise ValueError('Expected request object')
    task=value.get('task');selector=['observations'] if task=='observe' else ['reference_ids'] if task=='reference' else []
    _object(value,['schema_version','profile','mode','task','catalog_id','catalog_version','catalog_sha256','question','reflection','notes']+selector)
    if type(value.get('schema_version')) is not int or value['schema_version']!=1 or value.get('profile')!=PROFILE or value.get('mode')!='manual':raise ValueError('Exact Roman profile,manual mode and integer schema_version1 required')
    if value.get('catalog_id')!=DATA['catalog_id'] or value.get('catalog_sha256')!=CATALOG_HASH or type(value.get('catalog_version')) is not int or value['catalog_version']!=1:raise ValueError('Exact pinned catalog ID,integer version1 and hash required')
    if task not in ('observe','reference','catalog'):raise ValueError('Supported tasks:observe,reference,catalog;compass conversion,Greek matching and prediction unsupported')
    for k in ('question','reflection','notes'):_optional_text(value,k,10000)
    if task=='reference':
        ids=value.get('reference_ids')
        if not isinstance(ids,list) or not 1<=len(ids)<=14:raise ValueError('One to14 reference IDs required')
        for i in ids:lookup(i)
        if len(set(ids))!=len(ids):raise ValueError('Duplicate reference IDs rejected')
    if task=='observe':
        rows=value.get('observations')
        if not isinstance(rows,list) or not 1<=len(rows)<=8:raise ValueError('One to8 ordered observations required')
        ids=set()
        for o in rows:
            _object(o,['observation_id','origin','bird_label','modern_species','phenomenon','relative_side','relation','reference_frame','observer_facing','setting','sequence','side_reports','uncertain_fields','uncertainty','description','reflection'])
            identifier=o.get('observation_id')
            if not isinstance(identifier,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',identifier) or identifier in ids:raise ValueError('Distinct bounded ASCII observation_id required')
            ids.add(identifier)
            bird=o.get('bird_label','unknown')
            if not _raw(bird,80) or not bird.strip():raise ValueError('bird_label must be bounded nonempty UTF8 source-label text;unknown is explicit')
            for key,domain,default in [('origin','origins','unknown'),('phenomenon','phenomena','unknown'),('relative_side','sides','unknown'),('relation','relations','unresolved'),('reference_frame','frames','unknown'),('observer_facing','facings','unknown')]:_enum(o,key,DATA[domain],default)
            for key in ('modern_species','setting','uncertainty','description','reflection'):_optional_text(o,key,10000)
            for key in ('side_reports','uncertain_fields','sequence'):
                rows=o.get(key,[])
                if not isinstance(rows,list) or len(rows)>12:raise ValueError(key+' must be a bounded list')
                if key=='sequence':
                    if any(not _raw(x,2000) for x in rows):raise ValueError('Sequence entries must be raw UTF8 text')
                else:
                    domain=DATA['sides'] if key=='side_reports' else DATA['required_fields']
                    if any(not isinstance(x,str) or x not in domain for x in rows):raise ValueError('Unknown '+key+' value')
                    if key=='uncertain_fields' and len(set(rows))!=len(rows):raise ValueError('Duplicate uncertain fields rejected')
    return copy.deepcopy(value)

def evaluate(observation):
    p,c=assets();o=observation
    effective={k:o.get(k,'unresolved' if k=='relation' else 'unknown') for k in p['required_fields']}
    for field in o.get('uncertain_fields',[]):effective[field]='unresolved' if field=='relation' else 'unknown'
    sides=set(o.get('side_reports',[]))-{'unknown'}
    if o.get('relative_side','unknown')!='unknown':sides.add(o['relative_side'])
    conflicting=len(sides)>1
    results=[]
    for r in c['records']:
        if r['conditions'] is None:continue
        needed=r['conditions'];missing=[k for k in needed if effective[k] in ('unknown','unresolved')]
        mismatches=[k for k in ('bird_label','phenomenon','relative_side','relation') if effective[k] not in ('unknown','unresolved') and effective[k]!=needed[k]]
        if effective['bird_label'] not in ('crow','raven','unknown'):status='unsupported'
        elif mismatches:status='not_applicable'
        elif conflicting:status='conflicting_evidence'
        elif effective['reference_frame']=='cardinal':status='unsupported'
        elif missing:status='insufficient_evidence'
        elif r['text_layer']=='translator_note':status='conflicting_evidence'
        else:status='applicable'
        matched=not conflicting and not missing and not mismatches and effective['reference_frame']=='observer_relative' and effective['bird_label'] in ('crow','raven')
        results.append(dict(rule_id=r['id'],status=status,condition_satisfied=matched,missing_fields=missing,mismatched_fields=mismatches,source_record=r))
    statuses=[r['status'] for r in results]
    if conflicting:overall='conflicting_evidence'
    elif effective['bird_label'] not in ('crow','raven','unknown') or effective['reference_frame']=='cardinal':overall='unsupported'
    elif 'conflicting_evidence' in statuses or any(r['rule_id']=='call-crow-left' and r['status']=='applicable' for r in results):overall='conflicting_evidence'
    elif 'applicable' in statuses:overall='applicable'
    elif 'insufficient_evidence' in statuses:overall='insufficient_evidence'
    else:overall='not_applicable'
    return dict(observation_id=o['observation_id'],declared=copy.deepcopy(o),origin=o.get('origin','unknown'),effective_fields=effective,structured_side_conflict=conflicting,status=overall,evaluations=results,
        applicable_main_ids=[r['rule_id'] for r in results if r['status']=='applicable'],matched_note_ids=[r['rule_id'] for r in results if r['condition_satisfied'] and r['source_record']['text_layer']=='translator_note'],
        favorable_main_source_ids=[r['rule_id'] for r in results if r['status']=='applicable' and r['source_record']['explicit_favorable_language']],
        source_conflict_context=['call-crow-left','note226-crow-right','direction-criticism','orientation-note226'] if effective['bird_label']=='crow' and effective['phenomenon'] in ('call','unknown') else [],
        modern_species_inferred=None,cardinal_conversion=None,empirical_prediction=None,public_auspice_authorized=False,qualification=p['public_qualification'])

def register_knowledge(registry):
    _,c=assets()
    for s in c['sources']:registry.add_source(s)
    for r in c['records']:registry.add_rule(Rule('augury.'+r['id'],1,38,'Roman auspices',PROFILE,r['source_id'],r['locator'],r['source_account'],'augury_source_condition' if r['conditions'] else 'augury_context_reference',dict(reference_id=r['id']),'proposed','traditional',[]))

def read(value,registry=None):
    p,c=assets();q=validate(value)
    if registry is not None:register_knowledge(registry)
    observations=[evaluate(o) for o in q.get('observations',[])]
    references=[lookup(i) for i in q['reference_ids']] if q['task']=='reference' else c['records'] if q['task']=='catalog' else []
    comparisons=[dict(observation_ids=[a['observation_id'],b['observation_id']],same_declared_bird=a['effective_fields']['bird_label']==b['effective_fields']['bird_label'],phenomena=[a['effective_fields']['phenomenon'],b['effective_fields']['phenomenon']],applicable_main_ids=[a['applicable_main_ids'],b['applicable_main_ids']],combined_omen=None) for a,b in itertools.combinations(observations,2)]
    return dict(schema_version=1,technique_id=38,profile=PROFILE,mode='manual',task=q['task'],sources=c['sources'],observations=observations,references=references,comparisons=comparisons,
        context_references=[r for r in c['records'] if r['conditions'] is None],translation_notes=c['translation_notes'],conventions=p['conventions'],evaluation_policy=p['priority'],
        user_text={k:q[k] for k in ('question','reflection','notes') if k in q},
        evidence_matrix=dict(direct='Source-located dialogue and separately attributed notes;Quintus and Marcus remain distinct',compositional='Explicit finite condition matching;applicable is documentary compatibility,not factual judgment',user_attributed='Raw reported bird behavior,origin,modern species text,setting,sequence,uncertainty and reflection',unsupported='Prediction,diagnosis,scientific species inference,divine accuracy or authorized public auspices'),
        variation_matrix=dict(supported=p['supported'],experimental=[],unsupported=p['unsupported']),public_qualification=p['public_qualification'],greek_scope=p['greek_scope'],rights=p['rights'],
        replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,catalog_sha256=CATALOG_HASH,source_manifest_sha256=p['source_manifest_sha256'],source_snapshot_sha256={s['id']:s['snapshot_sha256'] for s in c['sources']},serialization='Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw user text preserved',external_calls=False,rng=False,integrity_checked=True))

def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2);fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Augury: Roman bird-sign source reference','',f'Profile: {PROFILE}','','Manual source comparison only;no factual prediction or public auspice authority.']
    for o in result['observations']:lines+=['',f'## {o["observation_id"]}: {o["status"]}','',block(dict(declared=o['declared'],applicable_main_ids=o['applicable_main_ids'],matched_note_ids=o['matched_note_ids'],favorable_main_source_ids=o['favorable_main_source_ids']))]
    for title,key in [('Source editions and rights','sources'),('Complete observation evaluation','observations'),('Selected source references','references'),('Neutral observation comparison','comparisons'),('Critical and contextual references','context_references'),('Latin translation qualification','translation_notes'),('Frozen conventions','conventions'),('Evaluation policy','evaluation_policy'),('Raw user text','user_text'),('Evidence layers','evidence_matrix'),('Variation support','variation_matrix'),('Public authority boundary','public_qualification'),('Greek scope','greek_scope'),('Rights','rights'),('Exact replay metadata','replay')]:lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'

def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),augury_report=None),indent=2)
    return '# Augury request rejected\n\n'+html.escape(str(message))+'\n'
