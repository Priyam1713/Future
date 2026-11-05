import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future.osteomancy import PROFILE,ORDER,read

def examples():
    def q(ids,task='reference',**kw):return dict(schema_version=1,profile=PROFILE,mode='documentary',task=task,case_ids=ids)|kw
    out={'basic':q(['8']),'ancestor-contrast':q(['9A','9B'],'compare'),'settlement':q(['19A','19B'],'compare'),
         'approval-uncertainty':q(['20A','20B'],'compare'),'harvest':q(['22A','22B'],'compare'),'warfare-distinct':q(['24A','24B'],'compare'),
         'missing-prognostication':q(['8','10','20A']),'unavailable-verification':q(['19A','22A','23']),
         'days':q(['8','19A','19B','20A'],'compare'),
         'unicode':q(['8'],notes='  Café Café\r\n猫\t `````json  ',annotations=[dict(case_id='8',note='  Research note\r\n only. ',association=' 個人 ')]),
         'named-group':dict(schema_version=1,profile=PROFILE,mode='documentary',task='group',group='ancestor-harm'),
         'topic':dict(schema_version=1,profile=PROFILE,mode='documentary',task='topic',topic='royal_affliction'),
         'multiple':q(['24B','8','19A']),'unresolved':q(['8','24B'],'compare'),'reversed':q(['19B','19A'],'compare'),'catalog':q(list(ORDER))}
    return out

def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'q.json')
        def check(name,q,fmt='json',reject=False,save=None):
            path.write_bytes(json.dumps(q,ensure_ascii=False).encode('utf-8'))
            p=subprocess.run([sys.executable,'-m','future','osteomancy',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr,p.stdout[:300])
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['osteomancy_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==read(q)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert read(json.loads(m[2])['request'])==read(q)
            if save:Path('data',save).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'osteomancy-{name}-input.json').write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
            check(name+' JSON',q,save=f'osteomancy-{name}.json');check(name+' Markdown',q,'markdown',save=f'osteomancy-{name}.md');check(name+' repeat',q)
        basic=rows['basic']
        bad={'unknown-case':basic|dict(case_ids=['99']),'bone-toss':basic|dict(task='bone_toss'),'crack-classification':basic|dict(task='crack_classification'),
             'invalid':basic|dict(schema_version=True),'seeded':basic|dict(seed='x'),'wrong-profile':basic|dict(profile='universal-bones'),
             'compare-one':basic|dict(task='compare'),'duplicate':basic|dict(case_ids=['8','8'])}
        saved={'unknown-case','bone-toss','crack-classification','invalid'}
        for name,q in bad.items():
            if name in saved:Path('data',f'osteomancy-{name}-input.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,reject=True,save=f'osteomancy-{name}.json' if name in saved else None)
            check(name+' Markdown',q,'markdown',True,f'osteomancy-{name}.md' if name in saved else None)
    Path('data/osteomancy-input.json').write_text(json.dumps(rows['basic'],indent=2)+'\n',encoding='utf-8')
    Path('data/osteomancy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    for name,q in rows.items():
        assert json.loads(Path('data',f'osteomancy-{name}.json').read_text(encoding='utf-8'))==read(q)
        text=Path('data',f'osteomancy-{name}.md').read_text(encoding='utf-8');m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert read(json.loads(m[2])['request'])==read(q)
    print(len(cases),f'Osteomancy CLI cases passed;16 JSON/16 Markdown saved replays verified')
if __name__=='__main__':run()
