import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future import haruspicy as h

def examples():
    f=json.loads(Path('tests/fixtures/haruspicy_reference_v1.json').read_text(encoding='utf-8'))
    def q(observations=None,**kw):return dict(schema_version=1,profile=h.PROFILE,mode='manual',task='compare',catalog_id=h.DATA['catalog_id'],catalog_version=1,catalog_sha256=h.CATALOG_HASH,observations=copy.deepcopy(observations or f['known_answers'][0]['observations']))|kw
    rows={x['name']:q(x['observations']) for x in f['known_answers'][:14]}
    rows['reference']={k:v for k,v in q(task='reference',reference_ids=['lung-cleft','liver-head-absent','heart-criticism']).items() if k!='observations'}
    for name,tradition in [('etruscan','etruscan'),('mesopotamian','mesopotamian')]:
        row=q();row['observations'][0]['tradition']=tradition;rows[name]=row
    rows['unicode']=q(question='  Café Café\r\n猫\t `````json ',reflection=' व्यक्तिगत अर्थ ')
    rows['catalog']={k:v for k,v in q(task='catalog').items() if k!='observations'}
    rows['vitals-conflict']=q();rows['vitals-conflict']['observations'][0]['other_vitals_reports']=['sound','not_sound']
    return rows

def rejected():
    base=examples()['exact-lung']
    def bad_obs(**kw):return base|dict(observations=[base['observations'][0]|kw])
    return {'invalid-schema':base|dict(schema_version=True),'prediction':base|dict(task='predict'),'wrong-profile':base|dict(profile='unknown'),
        'wrong-hash':base|dict(catalog_sha256='0'*64),'foreign-catalog':base|dict(catalog_id='barutu-v1'),
        'invalid-organ':bad_obs(organ='gallbladder'),'invalid-feature':bad_obs(feature='modern_caudate_lobe'),'duplicate-id':base|dict(observations=base['observations']*2),
        'invalid-unicode':base|dict(question='\ud800'),'wrong-version':base|dict(catalog_version=2),
        'unknown-reference':{k:v for k,v in base.items() if k!='observations'}|dict(task='reference',reference_ids=['missing']),
        'invalid-link':bad_obs(prior_observation_id=True)}

def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'q.json')
        def check(name,q,fmt='json',reject=False,save=None):
            path.write_bytes(json.dumps(q,ensure_ascii=True).encode('utf-8'))
            p=subprocess.run([sys.executable,'-m','future','haruspicy',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr,p.stdout[:300])
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['haruspicy_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==h.read(q)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S)
                assert h.read(json.loads(m[2])['request'])==h.read(q)
            if save:Path('data',save).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'haruspicy-{name}-input.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,save=f'haruspicy-{name}.json');check(name+' Markdown',q,'markdown',save=f'haruspicy-{name}.md');check(name+' repeat',q)
        for name,q in rejected().items():
            Path('data',f'haruspicy-{name}-input.json').write_text(json.dumps(q,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,reject=True,save=f'haruspicy-{name}.json');check(name+' Markdown',q,'markdown',True,f'haruspicy-{name}.md')
    Path('data/haruspicy-input.json').write_text(json.dumps(rows['exact-lung'],indent=2)+'\n',encoding='utf-8')
    Path('data/haruspicy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    for name,q in rows.items():
        assert json.loads(Path('data',f'haruspicy-{name}.json').read_text(encoding='utf-8'))==h.read(q)
        text=Path('data',f'haruspicy-{name}.md').read_text(encoding='utf-8');m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S)
        assert h.read(json.loads(m[2])['request'])==h.read(q)
    assert len(rows)==20 and len(cases)==84
    print('84 Haruspicy CLI cases passed;20 valid JSON/Markdown saved replays and12 saved rejection pairs verified')
if __name__=='__main__':run()
