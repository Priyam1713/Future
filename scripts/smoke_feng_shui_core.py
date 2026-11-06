import json,re,subprocess,sys,tempfile
from pathlib import Path
from future import feng_shui as f
def examples():
    def q(h=920,**kw):return dict(schema_version=1,profile=f.PROFILE,catalog_id=f.DATA['catalog_id'],catalog_version=1,catalog_sha256=f.CATALOG_HASH,mode='manual',task='classify',bearing_tenths=h,north_reference='source_diagram',bearing_role='source_heading')|kw
    def o(h,id,**kw):return dict(reading_id=id,bearing_tenths=h,north_reference='source_diagram',bearing_role='source_heading')|kw
    def compare(a,b):return {k:v for k,v in q(task='compare',readings=[a,b]).items() if k not in f.READING_FIELDS}
    return {
        'source92':q(),'n2-upper':q(75),'n3-lower':q(76),'zero':q(0),'last':q(3599),
        'east':q(900),'south':q(1800),'west':q(2700),'northeast':q(450),'southwest':q(2250),'northwest':q(3150),
        'boundary-uncertainty':q(75,uncertainty_tenths=1),'north-wrap':q(0,uncertainty_tenths=1),
        'magnetic':q(north_reference='magnetic',bearing_role='building_facing'),'true':q(north_reference='true',bearing_role='building_sitting'),
        'unknown-frame':q(north_reference='unknown'),'missing-frame':{k:v for k,v in q().items() if k not in ('north_reference','bearing_role')},
        'facing-door':compare(o(1800,'facade',north_reference='magnetic',bearing_role='building_facing',building_id='house1'),o(920,'door',north_reference='magnetic',bearing_role='door',building_id='house1')),
        'two-heading':compare(o(920,'a'),o(2700,'b')),
        'reference':{k:v for k,v in q(task='reference',reference_ids=['N2','Gui','Mao 卯']).items() if k not in f.READING_FIELDS},
        'catalog':{k:v for k,v in q(task='catalog').items() if k not in f.READING_FIELDS},
        'contradictory':q(north_reference='magnetic',contradictory_assertions={'north_reference':['true'],'bearing_tenths':[1800]}),
        'alternates':q(75,alternate_readings=[76]),'unicode':q(question='  Café Café\r\n猫\t `````json ',reflection=' व्यक्तिगत अर्थ ')}

def rejected():
    base=examples()['source92']
    bad={name:base|dict(bearing_tenths=v) for name,v in [('negative',-1),('360-degrees',3600),('multiple-turn',7200),('precision',75.5),('boolean',True),('string','75')]}
    bad.update({'wrong-profile':base|dict(profile='unknown'),'wrong-hash':base|dict(catalog_sha256='0'*64),'wrong-version':base|dict(catalog_version=True),'foreign-catalog':base|dict(catalog_id='flying-stars'),'prediction':base|dict(task='predict'),'invalid-role':base|dict(bearing_role='facade'),'bad-uncertainty':base|dict(uncertainty_tenths=1801),'missing-bearing':{k:v for k,v in base.items() if k!='bearing_tenths'}})
    raw=json.dumps(base)
    bad['nonfinite']=raw.replace('"bearing_tenths": 920','"bearing_tenths": NaN')
    bad['duplicate-json']=raw[:-1]+', "bearing_tenths": 75}'
    return bad

def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'q.json')
        def check(name,q,fmt='json',reject=False,save=None):
            path.write_bytes((q if isinstance(q,str) else json.dumps(q,ensure_ascii=True)).encode('utf-8'))
            p=subprocess.run([sys.executable,'-m','future','feng-shui',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr,p.stdout[:300])
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['feng_shui_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==f.read(q)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert f.read(json.loads(m[2])['request'])==f.read(q)
            if save:Path('data',save).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'feng-shui-{name}-input.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,save=f'feng-shui-{name}.json');check(name+' Markdown',q,'markdown',save=f'feng-shui-{name}.md');check(name+' repeat',q)
        for name,q in rejected().items():
            Path('data',f'feng-shui-{name}-input.json').write_text((q if isinstance(q,str) else json.dumps(q,ensure_ascii=True,indent=2))+'\n',encoding='utf-8')
            check(name+' JSON',q,reject=True,save=f'feng-shui-{name}.json');check(name+' Markdown',q,'markdown',True,f'feng-shui-{name}.md')
    Path('data/feng-shui-input.json').write_text(json.dumps(rows['source92'],indent=2)+'\n',encoding='utf-8')
    Path('data/feng-shui-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    for name,q in rows.items():
        assert json.loads(Path('data',f'feng-shui-{name}.json').read_text(encoding='utf-8'))==f.read(q)
        text=Path('data',f'feng-shui-{name}.md').read_text(encoding='utf-8');m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert f.read(json.loads(m[2])['request'])==f.read(q)
    assert len(rows)==24 and len(cases)==104
    print('104 Feng Shui CLI cases passed;24 accepted JSON/Markdown replay pairs and16 rejection pairs verified')
if __name__=='__main__':run()
