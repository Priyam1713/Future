"""One user-declared Greek Alphabet Oracle lot; no numeric oracle or generated draw."""
import copy,html,json,re
from .knowledge import Rule
from .scrying import _object,_optional_text,digest,load_input
from .cleromancy_catalog import PROFILE,PROFILE_HASH,CATALOG_HASH,DATA,assets,lookup,catalog,integrity,thaw

def validate(value):
    fields=['schema_version','profile','mode','task','catalog_id','catalog_version','catalog_sha256','question','association','reflection','notes','uncertainty']
    if not isinstance(value,dict):raise ValueError('Expected a request object')
    task=value.get('task')
    _object(value,fields+(['mark','observation_origin'] if task in ('reading','lookup') else []))
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE or value.get('mode')!='manual':raise ValueError('Exact named profile and manual mode required; dice/astragaloi/seeded methods unsupported')
    if task not in ('reading','lookup','catalog'):raise ValueError('Supported tasks: reading,lookup,catalog; no prediction, numeric mapping or multiple draw')
    if value.get('catalog_id')!=DATA['catalog_id'] or value.get('catalog_sha256')!=CATALOG_HASH:raise ValueError('Exact catalog identity/hash required; no unknown source or edition substitution')
    if type(value.get('catalog_version')) is not int or value['catalog_version']!=1:raise ValueError('catalog_version must be exact integer1')
    for key in ('question','association','reflection','notes','uncertainty'):_optional_text(value,key,10000)
    if task!='catalog':
        lookup(value.get('mark'))
        if value.get('observation_origin','unknown') not in DATA['observation_origins']:raise ValueError('observation_origin must be reported_real,hypothetical or unknown; never software-verified')
    return copy.deepcopy(value)

def register_knowledge(registry):
    for key in ('source','identity_source'):registry.add_source(thaw(DATA[key]))
    for r in catalog():
        registry.add_rule(Rule('cleromancy.mark.'+r['id'],1,37,'casting marked lots',PROFILE,DATA['source']['id'],r['locator'],r['source_account'],'cleromancy_source_account',dict(mark_id=r['id'],account_tag=r['account_tag']),'proposed','traditional',[]))
    registry.add_rule(Rule('cleromancy.manual.single',1,37,'casting marked lots',PROFILE,DATA['source']['id'],'Introduction,first method',DATA['method']['description'],'cleromancy_manual_declaration',dict(lots=1),'proposed','traditional',[]))

def read(value,registry=None):
    profile,_=assets();q=validate(value)
    if registry is not None:register_knowledge(registry)
    resolved=lookup(q['mark']) if q['task']!='catalog' else None
    selected=resolved['record'] if resolved else None
    selection=dict(declared_mark=q['mark'],canonical_id=selected['id'],observation_origin=q.get('observation_origin','unknown'),generated=False,physical_selection_verified=False,probability=None,normalization=resolved['normalization'],lot_count=1,replacement_policy='not_applicable_single_declared_lot',qualification=profile['origin_policy']) if selected else None
    return dict(schema_version=1,technique_id=37,profile=PROFILE,mode='manual',task=q['task'],source=profile['source'],identity_source=profile['identity_source'],
        selection=selection,selected_mark=selected,catalog_records=catalog() if q['task']=='catalog' else [],catalog=dict(id=profile['catalog_id'],version=1,mark_count=24,ordering='Frozen24 Greek letter source order, separate from dice sums or isopsephic values',normalization=profile['normalization']),
        source_procedure=profile['method'],historical_boundary=profile['historical_boundary'],
        source_interpretation=dict(status='attributed_source_account',text=selected['source_account'] if selected else None,user_application=None,qualification='Original concise factual account of Opsopaus-attributed oracle; not a verbatim translation, verified ancient inscription, automatic application or demonstrated future event.'),
        user_text={k:q[k] for k in ('question','association','reflection','notes','uncertainty') if k in q},
        variation_matrix=dict(supported='Named Greek Alphabet Oracle single declared marked-lot reference only',experimental=[],unsupported=profile['unsupported']),
        numeric_discrepancies=profile['numeric_discrepancies'],
        evidence_matrix=dict(direct='Verified author-origin indexed source identities, stated single-lot method and attributed accounts; original inscription not independently authenticated',compositional='Explicit alias normalization and exact catalog lookup/trace',user_attributed='Raw declared mark, reported observation origin, question, uncertainty and personal reflections',unsupported='Objective future prediction, ritual success, random fairness, diagnosis, spirit contact or supernatural guarantees'),
        source_layers=profile['evidence_layers'],rights=profile['rights'],
        replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,catalog_sha256=CATALOG_HASH,source_record_sha256=profile['source_record_sha256'],source_html_sha256=profile['source_html_sha256'],
            serialization='SHA256 canonical UTF8 sorted-key compact JSON, unescaped Unicode, no terminal LF; raw user text preserved',external_calls=False,rng=False,integrity_checked=True))

def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2);fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Cleromancy: Greek Alphabet Oracle marked lot','',f'Profile: {PROFILE}','','One user-declared mark; no software-generated or verified physical selection.']
    if result['selected_mark']:
        r=result['selected_mark'];lines+=['',f'## {r["glyph"]} — {r["name"]} ({r["id"]}, source order {r["order"]})','',r['source_account'],'',r['lexical_qualification']]
    for title,key in [('Exact source and access','source'),('Greek identity reference','identity_source'),('Declared selection and normalization','selection'),('Selected source record','selected_mark'),('Complete source-order catalog','catalog_records'),('Catalog identity','catalog'),('Source single-lot method','source_procedure'),('Historical boundary','historical_boundary'),('Attributed account and limits','source_interpretation'),('Raw user text','user_text'),('Variation support','variation_matrix'),('Unresolved numeric source methods','numeric_discrepancies'),('Evidence matrix','evidence_matrix'),('Source layers','source_layers'),('Rights and attribution','rights'),('Exact replay metadata','replay')]:lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'

def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),cleromancy_report=None),indent=2)
    return '# Cleromancy request rejected\n\n'+html.escape(str(message))+'\n'
