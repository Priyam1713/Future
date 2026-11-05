import json,re,subprocess,sys,tempfile
from pathlib import Path
from future import cleromancy as e,cleromancy_catalog as c

def examples():
    def q(mark='gao-alpha',**kw):return dict(schema_version=1,profile=c.PROFILE,mode='manual',task='reading',catalog_id=c.DATA['catalog_id'],catalog_version=1,catalog_sha256=c.CATALOG_HASH,mark=mark)|kw
    catalog={k:v for k,v in q(task='catalog').items() if k!='mark'}
    return {'alpha':q(),'omega':q('Ω'),'interior':q('mu'),'delta':q('Δ'),'epsilon':q('epsilon'),
        'khi':q('KHI'),'chi':q('Chi'),'sigma':q('σ'),'final-sigma':q('ς'),
        'unicode':q('  ALPHA\t',question='  Café Café\r\n猫\t `````json ',association=' 個人 ',notes=' 原文 ',uncertainty=' not sure '),
        'question-a':q('rho',question='Question A'),'question-b':q('rho',question='Different question B'),
        'hypothetical':q('psi',observation_origin='hypothetical',reflection='My own reflection, not a source claim.'),
        'reported-real':q('beta',observation_origin='reported_real'),'lookup':q('υ',task='lookup'),'catalog':catalog}

def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'q.json')
        def check(name,q,fmt='json',reject=False,save=None):
            path.write_bytes(json.dumps(q,ensure_ascii=True).encode('utf-8'))
            p=subprocess.run([sys.executable,'-m','future','cleromancy',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr,p.stdout[:300])
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['cleromancy_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==e.read(q)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert e.read(json.loads(m[2])['request'])==e.read(q)
            if save:Path('data',save).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'cleromancy-{name}-input.json').write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
            check(name+' JSON',q,save=f'cleromancy-{name}.json');check(name+' Markdown',q,'markdown',save=f'cleromancy-{name}.md');check(name+' repeat',q)
        base=rows['alpha']
        bad={'five-astragaloi':base|dict(mode='five_astragaloi'),'five-d6':base|dict(mode='five_d6'),
            'source-face-five':base|dict(mode='five_astragaloi',faces=[6,5,3,6,6]),'homeric-passage':base|dict(task='homeric_passage'),
            'unknown-mark':base|dict(mark='digamma'),'ambiguous-mark':base|dict(mark='alpha beta'),'invalid-unicode':base|dict(mark='\ud800'),
            'confusable':base|dict(mark='A'),'wrong-profile':base|dict(profile='generic-lots'),'wrong-hash':base|dict(catalog_sha256='0'*64),
            'multiple-draw':base|dict(marks=['alpha','beta']),'prediction':base|dict(task='predict'),'seeded':base|dict(seed='x'),
            'missing-mark':{k:v for k,v in base.items() if k!='mark'},'invalid-type':base|dict(mark=True),'wrong-version':base|dict(catalog_version=2)}
        for name,q in bad.items():
            Path('data',f'cleromancy-{name}-input.json').write_text(json.dumps(q,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,reject=True,save=f'cleromancy-{name}.json');check(name+' Markdown',q,'markdown',True,f'cleromancy-{name}.md')
    Path('data/cleromancy-input.json').write_text(json.dumps(rows['alpha'],indent=2)+'\n',encoding='utf-8')
    Path('data/cleromancy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    for name,q in rows.items():
        assert json.loads(Path('data',f'cleromancy-{name}.json').read_text(encoding='utf-8'))==e.read(q)
        text=Path('data',f'cleromancy-{name}.md').read_text(encoding='utf-8');m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert e.read(json.loads(m[2])['request'])==e.read(q)
    assert e.read(rows['question-a'])['selected_mark']==e.read(rows['question-b'])['selected_mark']
    print(len(cases),'Cleromancy CLI cases passed;16 valid JSON/Markdown saved replays and16 saved rejection pairs verified')
if __name__=='__main__':run()
