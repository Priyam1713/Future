import json,re,subprocess,sys,tempfile
from pathlib import Path
from future import augury as a
def examples():
    def o(**kw):return dict(observation_id='obs1',bird_label='crow',phenomenon='call',relative_side='left',relation='located_on_side',reference_frame='observer_relative')|kw
    def q(observation=None,**kw):return dict(schema_version=1,profile=a.PROFILE,mode='manual',task='observe',catalog_id=a.DATA['catalog_id'],catalog_version=1,catalog_sha256=a.CATALOG_HASH,observations=[observation or o()])|kw
    def ref(ids):return {k:v for k,v in q(task='reference',reference_ids=ids).items() if k!='observations'}
    return {'crow-left-call':q(),'raven-right-call':q(o(bird_label='raven',relative_side='right')),
        'crow-left-flight':q(o(phenomenon='flight',relation='moving_to_side')),'raven-right-flight':q(o(bird_label='raven',phenomenon='flight',relative_side='right',relation='moving_to_side')),
        'missing-phenomenon':q(o(phenomenon='unknown')),'opposite-flight':q(o(phenomenon='flight',relative_side='right',relation='moving_to_side')),
        'unknown-bird':q(o(bird_label='sparrow')),'unknown-side':q(o(relative_side='unknown')),'conflicting-sides':q(o(side_reports=['left','right'])),
        'call-flight-compare':q(observations=[o(),o(observation_id='obs2',phenomenon='flight',relation='moving_to_side')]),
        'note226':q(o(relative_side='right')),'marcus':ref(['direction-criticism','cock-criticism','public-criticism']),
        'public':ref(['public-early','public-decay','public-criticism']),'ordinary':q(o(origin='hypothetical',setting='ordinary private bird observation')),
        'cardinal-frame':q(o(reference_frame='cardinal',observer_facing='S')),'located-flight':q(o(phenomenon='flight')),
        'moving-from':q(o(phenomenon='flight',relation='moving_from_side')),'uncertain-bird':q(o(phenomenon='flight',relation='moving_to_side',uncertain_fields=['bird_label'])),
        'unicode':q(o(reflection='  Café Café\r\n猫\t `````json ',modern_species='user identification only'),question=' व्यक्तिगत अर्थ '),
        'catalog':{k:v for k,v in q(task='catalog').items() if k!='observations'}}
def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'q.json')
        def check(name,q,fmt='json',reject=False,save=None):
            path.write_bytes(json.dumps(q,ensure_ascii=True).encode('utf-8'));p=subprocess.run([sys.executable,'-m','future','augury',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr,p.stdout[:300])
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['augury_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==a.read(q)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert a.read(json.loads(m[2])['request'])==a.read(q)
            if save:Path('data',save).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'augury-{name}-input.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,save=f'augury-{name}.json');check(name+' Markdown',q,'markdown',save=f'augury-{name}.md');check(name+' repeat',q)
        base=rows['crow-left-call'];bad={'invalid':base|dict(schema_version=True),'wrong-profile':base|dict(profile='unknown'),
            'compass-conversion':base|dict(task='compass_convert'),'greek-profile':base|dict(profile='homer-murray1924-greek-omens'),'wrong-hash':base|dict(catalog_sha256='0'*64),
            'prediction':base|dict(task='predict'),'duplicate-id':base|dict(observations=base['observations']*2),'invalid-unicode':base|dict(question='\ud800'),
            'unknown-reference':{k:v for k,v in base.items() if k!='observations'}|dict(task='reference',reference_ids=['missing']), 'wrong-version':base|dict(catalog_version=2)}
        for name,q in bad.items():
            Path('data',f'augury-{name}-input.json').write_text(json.dumps(q,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,reject=True,save=f'augury-{name}.json');check(name+' Markdown',q,'markdown',True,f'augury-{name}.md')
    Path('data/augury-input.json').write_text(json.dumps(rows['crow-left-call'],indent=2)+'\n',encoding='utf-8')
    Path('data/augury-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    for name,q in rows.items():
        assert json.loads(Path('data',f'augury-{name}.json').read_text(encoding='utf-8'))==a.read(q)
        text=Path('data',f'augury-{name}.md').read_text(encoding='utf-8');m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert a.read(json.loads(m[2])['request'])==a.read(q)
    print(len(cases),'Augury CLI cases passed;20 valid JSON/Markdown saved replays and10 saved rejection pairs verified')
if __name__=='__main__':run()
