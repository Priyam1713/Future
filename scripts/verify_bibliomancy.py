"""Independent raw-witness/index reference, then runtime comparison; no runtime parser used."""
import hashlib,html,itertools,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def get(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def reference():
    f=get('tests/fixtures/bibliomancy_corpus_v1.json');n=get('tests/fixtures/bibliomancy_source_v1.json')
    c=get('knowledge/bibliomancy_corpus_v1.json');idx=get('knowledge/bibliomancy_index_v1.json')
    assert sha(c)==f['corpus_canonical_sha256'] and sha(idx)==f['index_canonical_sha256']
    expected={};verse_count=0;sentence_count=0
    for chapter_number in range(1,5):
        p=f'resources/corpora/webclassic-ruth-v1/RUT{chapter_number:02}.html'
        raw=(ROOT/p).read_bytes();assert hashlib.sha256(raw).hexdigest()==f['raw_sha256'][p]
        # Independent regular-expression/HTML-entity extraction, not the preparation HTMLParser.
        body=raw.decode('utf-8').split('<div class="main">',1)[1].split("<ul class='tnav'>",1)[0]
        body=re.sub(r'<a\b[^>]*class="notemark".*?</a>','',body,flags=re.S)
        parts=re.split(r'<span class="verse" id="V(\d+)">\d+&#160;</span>',body)
        verses=[];stream='';ranges=[]
        for v,markup in zip(parts[1::2],parts[2::2]):
            text=' '.join(html.unescape(re.sub('<[^>]+>',' ',markup)).split())
            identifier=f'RUT.{chapter_number}.{int(v)}';start=len(stream)+(bool(stream));stream+=(' ' if stream else '')+text
            verses.append(dict(id=identifier,number=int(v),text=text));ranges.append(dict(id=identifier,start=start,end=len(stream)))
        actual=c['chapters'][chapter_number-1]
        assert verses==actual['verses'] and stream==actual['text'] and ranges==actual['verse_ranges']
        assert len(verses)==f['verse_counts'][chapter_number-1]
        page=idx['shelves'][0]['books'][0]['pages'][chapter_number]
        assert len(page['sentences'])==f['sentence_counts'][chapter_number-1]
        ending=[];texts=[];last=0
        for number,s in enumerate(page['sentences'],1):
            assert s['id']==f'RUT.{chapter_number}.s{number:03}'
            assert s['start']>=last and not stream[last:s['start']].strip() and s['end']>s['start']
            text=stream[s['start']:s['end']];assert not text.startswith(('”','’'))
            assert re.search(r'[.!?][”’\x27" ]*$',text)
            native=[v['id'] for v in ranges if v['end']>s['start'] and v['start']<s['end']]
            assert s['verse_ids']==native;ending.append(int(native[-1].split('.')[-1]))
            expected[(1,1,chapter_number+1,number)]=dict(text=text,id=s['id'],verses=native)
            last=s['end'];texts.append(text)
        assert last==len(stream) and ' '.join(texts)==stream
        assert ending==f['sentence_ending_verses'][chapter_number-1]
        verse_count+=len(verses);sentence_count+=len(texts)
    for fixture in f['selections']:
        assert expected[tuple(fixture['path'])]=={k:fixture[k] for k in ('text','id','verses')}
    assert idx['shelves'][0]['books'][0]['pages'][0]['sentences']==[]
    assert any('’' in x['text'] and '“' in x['text'] for x in expected.values())
    triples=list(itertools.product(range(1,7),repeat=3))
    assert n['homeric']==[dict(faces=list(t),ordinal=i) for i,t in enumerate(triples,1)]
    sums=[sum(1 for a,b in itertools.product(range(10),repeat=2) if a+b==s) for s in range(19)]
    assert sums==n['literal_d10_sum_counts'] and sum(sums)==100
    assert [10*t+u for t in (0,1) for u in range(8)]==n['literal_seventeen_book_candidates']
    assert sorted(set(range(1,18))-set(n['literal_seventeen_book_candidates']))==[8,9]
    assert verse_count==85 and sentence_count==141
    return expected,triples

def verify():
    expected,triples=reference()
    from future import bibliomancy as b
    runtime=b.integrity();assert runtime['verified']
    def q(path):return dict(schema_version=1,profile=b.PROFILE,mode='manual_coarse',corpus_id=b.DATA['corpus_id'],corpus_version=1,corpus_sha256=b.DATA['corpus_sha256'],index_id=b.DATA['index_id'],index_version=1,index_sha256=b.DATA['index_sha256'],selections=[dict(path=list(path))])
    contexts=0
    for path,e in expected.items():
        r=b.read(q(path));s=r['selections'][0]
        assert s['text']==e['text'] and s['sentence_id']==e['id'] and s['verse_ids']==e['verses']
        assert s['citation'].startswith('Ruth ') and s['source_url'].endswith('#V'+e['verses'][0].split('.')[-1])
        for radius in range(3):
            selected=b.read(q(path)|dict(context=radius))['selections'][0]
            before=[expected[(1,1,path[2],i)]['text'] for i in range(max(1,path[3]-radius),path[3])]
            count=[41,37,33,30][path[2]-2]
            after=[expected[(1,1,path[2],i)]['text'] for i in range(path[3]+1,min(count,path[3]+radius)+1)]
            assert [s['text'] for s in selected['context_before']]==before
            assert [s['text'] for s in selected['context_after']]==after;contexts+=1
        assert b.read(r['replay']['request'])==r
    values=[]
    for i,t in enumerate(triples,1):
        h=b.read(dict(schema_version=1,profile=b.PROFILE,mode='homeric_index_reference',faces=list(t)))['historical_reference']
        assert h['ordinal']==i and h['faces']==list(t) and h['verse_mapping']=='mapping unavailable' and h['passage'] is None
        values.append(h['ordinal'])
    assert values==list(range(1,217))
    result=dict(passed=True,profile=b.PROFILE,profile_sha256=b.PROFILE_HASH,corpus_sha256=b.DATA['corpus_sha256'],index_sha256=b.DATA['index_sha256'],raw_witnesses=4,source_verses=85,selected_sentences=141,exact_manual_source_fixtures=12,all_sentence_ending_verse_checks=141,context_checks=contexts,homeric_ordered_keys=216,verified_homeric_verse_mappings=0,literal_d10_ordered_pairs=100,seventeen_book_unreachable=[8,9],source='Independent regex/entity parsing of raw witnesses; hand-authored pre-engine boundary/path/text fixtures. Expectations never obtained from runtime corpus parsing/selection.',empirical_validation=False)
    (ROOT/'data/bibliomancy-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('141 Bibliomancy selections;85 independently parsed verses;423 context cases;216 historical indices;100 literal dice sums passed')
    return result
if __name__=='__main__':
    if '--reference-only' in sys.argv:
        e,t=reference();print('Pre-engine reference passed:',len(e),'sentences,85 verses,',len(t),'ordered triples')
    else:verify()
