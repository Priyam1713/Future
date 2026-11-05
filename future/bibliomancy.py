"""Edition-pinned manual sentence selection and separate historical indexing reference."""
import copy,hashlib,html,json,re
from pathlib import Path
from .knowledge import Rule
from .scrying import freeze,thaw,digest,_object,_optional_text,load_input

ROOT=Path(__file__).resolve().parents[1]
PROFILE='mascaro2022-manual-coarse-webclassic-ruth-v1'
PROFILE_HASH='8fb64b52b632362cfc9633d6c4a01cceebeed51a14beef84b384105dca12cf34'
DATA=freeze(load_input(ROOT/'knowledge/bibliomancy_profile_v1.json'))

def _assets():
    profile=load_input(ROOT/'knowledge/bibliomancy_profile_v1.json')
    if digest(profile)!=PROFILE_HASH:raise ValueError('Pinned profile integrity mismatch; a new edition requires a new profile')
    corpus=load_input(ROOT/'knowledge/bibliomancy_corpus_v1.json');index=load_input(ROOT/'knowledge/bibliomancy_index_v1.json')
    if digest(corpus)!=profile['corpus_sha256']:raise ValueError('Pinned corpus hash mismatch')
    if digest(index)!=profile['index_sha256']:raise ValueError('Pinned sentence index hash mismatch; reordered units require a new profile')
    if corpus['id']!=profile['corpus_id'] or index['corpus_id']!=corpus['id'] or index['corpus_sha256']!=digest(corpus):raise ValueError('Corpus/index identity mismatch')
    if digest(corpus['raw_witnesses'])!=profile['raw_manifest_sha256']:raise ValueError('Raw witness manifest mismatch')
    for raw in corpus['raw_witnesses']:
        if hashlib.sha256((ROOT/raw['path']).read_bytes()).hexdigest()!=raw['sha256']:raise ValueError('Downloaded source witness hash mismatch: '+raw['name'])
    return profile,corpus,index

def integrity():
    p,c,i=_assets()
    return dict(verified=True,profile_sha256=PROFILE_HASH,corpus_sha256=digest(c),index_sha256=digest(i),raw_manifest_sha256=p['raw_manifest_sha256'],raw_witnesses=4)

def _integer(v,low,high,name):
    if type(v) is not int or not low<=v<=high:raise ValueError(f'{name} must be an integer in{low}..{high}; booleans/floats rejected')
    return v

def _path(path,index):
    if not isinstance(path,list) or len(path)!=4:raise ValueError('Selection path requires four one-based integers: shelf,book,logical_page,sentence')
    children=index['shelves'];selected=[]
    for depth,name in enumerate(('shelf','book','logical_page','sentence')):
        if not children:raise ValueError('Selected logical page has no selectable sentences (heading-only/empty page); no reroll')
        node=children[_integer(path[depth],1,len(children),name)-1];selected.append(node)
        if depth<3:children=node[('books','pages','sentences')[depth]]
    return selected

def validate(value,index):
    common=['schema_version','profile','mode','question','reflection','notes']
    if not isinstance(value,dict):raise ValueError('Expected request object')
    mode=value.get('mode')
    fields=common+(['corpus_id','corpus_version','corpus_sha256','index_id','index_version','index_sha256','selections','context'] if mode=='manual_coarse' else ['faces'])
    _object(value,fields)
    if type(value.get('schema_version')) is not int or value['schema_version']!=1 or value.get('profile')!=PROFILE:raise ValueError('Exact profile and integer schema_version1 required')
    if mode not in ('manual_coarse','homeric_index_reference'):raise ValueError('Supported modes: manual_coarse, homeric_index_reference; fine and seeded modes unsupported')
    for k in ('question','reflection','notes'):_optional_text(value,k,10000)
    if mode=='manual_coarse':
        for k in ('corpus_id','corpus_sha256','index_id','index_sha256'):
            if value.get(k)!=DATA[k]:raise ValueError('Exact pinned '+k+' required; no missing/unknown corpus or hash substitution')
        for k in ('corpus_version','index_version'):
            if type(value.get(k)) is not int or value[k]!=1:raise ValueError('Exact integer '+k+'1 required')
        _integer(value.get('context',1),0,2,'context radius')
        rows=value.get('selections')
        if not isinstance(rows,list) or not 1<=len(rows)<=32:raise ValueError('One to32 ordered selections required; repeats are preserved')
        for row in rows:
            _object(row,['path','sentence_id','reflection']);nodes=_path(row.get('path'),index)
            if 'sentence_id' in row and row['sentence_id']!=nodes[-1]['id']:raise ValueError('Unknown or mismatching sentence_id at the supplied path')
            _optional_text(row,'reflection',10000)
    else:
        faces=value.get('faces')
        if not isinstance(faces,list) or len(faces)!=3:raise ValueError('Exactly three ordered six-face values required')
        for f in faces:_integer(f,1,6,'face')
    return copy.deepcopy(value)

def _passage(sentence,chapter,page):
    verses=list(sentence['verse_ids']);first,last=[v.rsplit('.',1)[1] for v in (verses[0],verses[-1])]
    return dict(sentence_id=sentence['id'],text=chapter['text'][sentence['start']:sentence['end']],verse_ids=verses,
        citation=f'Ruth {chapter["chapter"]}:{first}'+('-'+last if last!=first else ''),source_url=page['source_url']+'#V'+first,
        source_span=dict(start=sentence['start'],end=sentence['end'],unit='Unicode codepoints; half-open normalized chapter stream'))

def register_knowledge(registry):
    for key in ('procedure_source','corpus_source','historical_source'):registry.add_source(thaw(DATA[key]))
    for name,key,locator,statement in [
        ('coarse','procedure_source','The first step;The next step;Upon selecting;Next','Mascaro coarse procedure selects a sentence within a selected page; software manual/logical-page adaptation is separate.'),
        ('ruth','corpus_source','Complete Ruth chapters1–4; native verses1:1–4:22','Edition-pinned public-domain Ruth text with independently reviewed sentence index and native citations.'),
        ('homeric-index','historical_source','§18;notes24,29','Ordered three six-face values define216 keys; editorial ordinals are indexing only, no verified verse mappings.')]:
        registry.add_rule(Rule('bibliomancy.'+name,1,36,'Bibliomancy',PROFILE,DATA[key]['id'],locator,statement,'bibliomancy_documentary_selection',{},'proposed','traditional',[]))

def read(value,registry=None):
    profile,corpus,index=_assets();q=validate(value,index)
    if registry is not None:register_knowledge(registry)
    selections=[];historical=None
    if q['mode']=='manual_coarse':
        radius=q.get('context',1)
        for row in q['selections']:
            shelf,book,page,sentence=_path(row['path'],index);chapter=corpus['chapters'][page['chapter']-1];position=row['path'][3]-1
            result=_passage(sentence,chapter,page)
            result.update(path=row['path'].copy(),stable_path=[shelf['id'],book['id'],page['id'],sentence['id']],logical_page=dict(index=row['path'][2],id=page['id'],label=page['label'],editorial=True,printed_page=None,native_chapter=page['chapter']),
                context_before=[_passage(s,chapter,page) for s in page['sentences'][max(0,position-radius):position]],
                context_after=[_passage(s,chapter,page) for s in page['sentences'][position+1:position+radius+1]],
                context_policy=f'Up to{radius} sentence units each side, clipped to the same chapter logical page; no wrap or crossing',user_reflection=row.get('reflection'))
            selections.append(result)
    else:
        a,b,c=q['faces'];historical=dict(faces=q['faces'].copy(),face_label=''.join(map(str,q['faces'])),ordinal=36*(a-1)+6*(b-1)+c,
            ordinal_convention=profile['historical']['ordinal'],verse_mapping='mapping unavailable',passage=None,source=profile['historical_source'],context=profile['historical'],
            qualification='216 verified numerical keys are not216 verified textual outcomes. No casting, verse reconstruction or complete oracle table.')
    identities=[s['sentence_id'] for s in selections]
    return dict(schema_version=1,technique_id=36,profile=PROFILE,mode=q['mode'],adaptation=profile['description'],procedure_source=profile['procedure_source'],
        corpus=dict(id=corpus['id'],version=corpus['version'],title=corpus['title'],edition=corpus['edition'],source=corpus['source'],normalization=corpus['normalization'],scope='Complete Ruth only:85 native verses,141 sentence units; not a full Bible or historical Christian lots procedure'),
        index=dict(id=index['id'],version=index['version'],ordering=index['ordering'],boundaries=index['boundaries'],cross_page=index['cross_page'],empty_page=index['empty_page'],abbreviation=index['abbreviation']),
        selections=selections,historical_reference=historical,
        comparison=dict(ordered_sentence_ids=identities,repeated_ids=list(dict.fromkeys(i for i in identities if identities.count(i)>1)),combined_meaning=None,policy='Neutral identity comparison only; repeated selections retained in order, no inferred combined message'),
        user_text={k:q[k] for k in ('question','reflection','notes') if k in q},source_discrepancies=profile['source_discrepancies'],
        selection_origin=dict(kind='user_supplied_manual',generated_draw=False,selection_probability=None,distribution_policy=profile['manual_probability']),
        evidence_layers=dict(direct='Source procedure attribution, exact rights-cleared text and edition/native citations',editorial='Manual digital adaptation, normalized display whitespace, logical pages, curated sentence spans, trace/context and identity comparison',user_attributed='Raw user question, reflection and notes, never edits to source text',unsupported='Objective predictions, verified divine selection, diagnoses, supernatural guarantees or unverified Homeric verses'),
        limitations=profile['unsupported'],
        replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,corpus_sha256=profile['corpus_sha256'],index_sha256=profile['index_sha256'],raw_manifest_sha256=profile['raw_manifest_sha256'],raw_witnesses=corpus['raw_witnesses'],
            serialization='SHA256 canonical UTF8 sorted-key compact JSON, unescaped Unicode, no terminal LF; raw user whitespace preserved',external_calls=False,rng=False,integrity_checked=True))

def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2);fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Bibliomancy: edition-pinned manual passage selection','',result['adaptation'],'',f'Profile: {PROFILE}']
    for s in result['selections']:
        lines+=['','## '+s['sentence_id'],'',f'[{s["citation"]}]({s["source_url"]}) — editorial logical page {s["logical_page"]["index"]}; path '+str(s['path']),'',block(dict(exact_source_text=s['text'],context_before=s['context_before'],context_after=s['context_after']))]
    for title,key in [('Source procedure','procedure_source'),('Corpus edition and rights','corpus'),('Index boundaries','index'),('Complete selections and raw per-selection reflections','selections'),('Historical indexing reference','historical_reference'),('Neutral selection comparison','comparison'),('Raw user text','user_text'),('Source numeric discrepancies','source_discrepancies'),('Manual selection boundary','selection_origin'),('Evidence layers','evidence_layers'),('Unsupported scope','limitations'),('Exact replay metadata','replay')]:lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'

def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),bibliomancy_report=None),indent=2)
    return '# Bibliomancy request rejected\n\n'+html.escape(str(message))+'\n'
