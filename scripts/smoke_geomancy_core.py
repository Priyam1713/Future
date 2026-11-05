import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future.geomancy import PROFILE,read

def examples():
    f=json.loads(Path('tests/fixtures/geomancy_reference_v1.json').read_text(encoding='utf-8'))
    def q(m,**kw):return dict(schema_version=1,profile=PROFILE,task='shield',mode='manual',input_mode='patterns',mothers=m,origin='hypothetical')|kw
    out={c['id']:q(c['positions'][:4]) for c in f['charts']}
    out['basic']=q(['1111','1212','2121','2222'])
    marks=q([]);marks.pop('mothers');marks.update(input_mode='mark_counts',mark_counts=[2,3,2,3,3,2,2,3,3,3,2,3,2,3,2,2]);out['marks']=marks
    ids=q([]);ids.pop('mothers');ids.update(input_mode='figure_ids',figure_ids=['Acquisitio','Carcer','Puer','Rubeus']);out['figure-ids']=ids
    out['catalog']=dict(schema_version=1,profile=PROFILE,task='figure_catalog',mode='manual')
    out['lookup']=out['catalog']|dict(lookup=['Puella','Puer','Dragons head','1112'])
    out['display-ltr']=q(f['charts'][0]['positions'][:4],layout='left_to_right')
    out['unicode']=q(f['charts'][0]['positions'][:4],question='  Café Café\r\n猫\t `````json  ',commentary=' Hypothetical construction only. ',association=' personal\n ')
    return out

def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'q.json')
        def check(name,q,fmt='json',reject=False,save=None):
            path.write_bytes(json.dumps(q,ensure_ascii=False).encode('utf-8'))
            p=subprocess.run([sys.executable,'-m','future','geomancy',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr,p.stdout[:300])
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['geomancy_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==read(q)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S)
                assert read(json.loads(m[2])['request'])==read(q)
            if save:Path('data',save).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'geomancy-{name}-input.json').write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
            check(name+' JSON',q,save=f'geomancy-{name}.json');check(name+' Markdown',q,'markdown',save=f'geomancy-{name}.md');check(name+' repeat',q)
        basic=rows['basic']
        bad={'house':basic|dict(task='house_chart'),'horary':basic|dict(task='horary_judgment'),
            'unknown-convention':basic|dict(figure_convention='universal'),'invalid':basic|dict(mothers=['1231']*4),
            'seeded':basic|dict(mode='seeded'),'super-judge':basic|dict(super_judge=True),
            'mixed':basic|dict(mark_counts=[1]*16),'bool-schema':basic|dict(schema_version=True)}
        for name,q in bad.items():
            save=name in ('house','horary','unknown-convention','invalid')
            if save:Path('data',f'geomancy-{name}-input.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,reject=True,save=f'geomancy-{name}.json' if save else None)
            check(name+' Markdown',q,'markdown',True,f'geomancy-{name}.md' if save else None)
    Path('data/geomancy-input.json').write_text(json.dumps(rows['basic'],indent=2)+'\n',encoding='utf-8')
    Path('data/geomancy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    for name,q in rows.items():
        assert json.loads(Path('data',f'geomancy-{name}.json').read_text(encoding='utf-8'))==read(q)
        text=Path('data',f'geomancy-{name}.md').read_text(encoding='utf-8')
        m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S)
        assert read(json.loads(m[2])['request'])==read(q)
    print(len(cases),f'Geomancy CLI cases passed; {len(rows)} JSON/{len(rows)} Markdown saved replays verified')

if __name__=='__main__':run()
