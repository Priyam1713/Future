import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future import bibliomancy as b

def examples():
    def q(paths=None,**kw):return dict(schema_version=1,profile=b.PROFILE,mode='manual_coarse',corpus_id=b.DATA['corpus_id'],corpus_version=1,corpus_sha256=b.DATA['corpus_sha256'],index_id=b.DATA['index_id'],index_version=1,index_sha256=b.DATA['index_sha256'],selections=[dict(path=p) for p in (paths or [[1,1,2,1]])])|kw
    def h(faces):return dict(schema_version=1,profile=b.PROFILE,mode='homeric_index_reference',faces=faces)
    return {'basic':q(),'another-page':q([[1,1,3,3]]),'first-last':q([[1,1,2,1],[1,1,5,30]]),
        'multiple':q([[1,1,5,27],[1,1,2,30],[1,1,4,13]]),'repeated':q([[1,1,2,30],[1,1,2,30]]),
        'question':q(question='What can I reflect on in this passage?'),'reflection':q(reflection='My own association: patience.',selections=[dict(path=[1,1,4,33],reflection='  My reflection only. ')]),
        'unicode':q([[1,1,3,35]],question='  Café Café\r\n猫\t `````json ',reflection=' व्यक्तिगत अर्थ '),
        'boundary':q([[1,1,2,23],[1,1,5,30]],context=2),'native-logical':q([[1,1,2,41],[1,1,3,1]]),
        'nested-quotes':q([[1,1,3,35],[1,1,3,36],[1,1,4,32],[1,1,4,33]]),
        'context-zero':q(context=0),'context-two':q([[1,1,2,30]],context=2),
        'sentence-id':q(selections=[dict(path=[1,1,2,1],sentence_id='RUT.1.s001')]),
        'homeric-index':h([1,3,6]),'homeric-last':h([6,6,6])}

def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'q.json')
        def check(name,q,fmt='json',reject=False,save=None):
            path.write_bytes(json.dumps(q,ensure_ascii=False).encode('utf-8'))
            p=subprocess.run([sys.executable,'-m','future','bibliomancy',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr,p.stdout[:300])
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['bibliomancy_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==b.read(q)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert b.read(json.loads(m[2])['request'])==b.read(q)
            if save:Path('data',save).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'bibliomancy-{name}-input.json').write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
            check(name+' JSON',q,save=f'bibliomancy-{name}.json');check(name+' Markdown',q,'markdown',save=f'bibliomancy-{name}.md');check(name+' repeat',q)
        base=rows['basic']
        def changed_path(p):return base|dict(selections=[dict(path=p)])
        bad={'fine':dict(schema_version=1,profile=b.PROFILE,mode='fine'),'seeded':dict(schema_version=1,profile=b.PROFILE,mode='seeded'),
             'zero':changed_path([0,1,2,1]),'out-of-range':changed_path([1,1,2,42]),'boolean':changed_path([1,1,2,True]),
             'unknown-corpus':base|dict(corpus_id='unknown'),'wrong-hash':base|dict(corpus_sha256='0'*64),'empty-page':changed_path([1,1,1,1]),
             'unsupported-edition':base|dict(corpus_version=2),'unknown-sentence':base|dict(selections=[dict(path=[1,1,2,1],sentence_id='RUT.1.s999')]),
             'negative':changed_path([1,1,-1,1]),'float':changed_path([1,1,2,1.0]),'invalid':base|dict(schema_version=True),
             'index-hash':base|dict(index_sha256='0'*64),'missing-corpus':{k:v for k,v in base.items() if k!='corpus_id'},
             'mixed-historical':rows['homeric-index']|dict(selections=base['selections'])}
        saved=set(list(bad)[:10])
        for name,q in bad.items():
            if name in saved:Path('data',f'bibliomancy-{name}-input.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,reject=True,save=f'bibliomancy-{name}.json' if name in saved else None)
            check(name+' Markdown',q,'markdown',True,f'bibliomancy-{name}.md' if name in saved else None)
    Path('data/bibliomancy-input.json').write_text(json.dumps(rows['basic'],indent=2)+'\n',encoding='utf-8')
    Path('data/bibliomancy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    for name,q in rows.items():
        assert json.loads(Path('data',f'bibliomancy-{name}.json').read_text(encoding='utf-8'))==b.read(q)
        text=Path('data',f'bibliomancy-{name}.md').read_text(encoding='utf-8');m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert b.read(json.loads(m[2])['request'])==b.read(q)
    print(len(cases),'Bibliomancy CLI cases passed;16 JSON/16 Markdown saved replays;10 saved rejection pairs verified')
if __name__=='__main__':run()
