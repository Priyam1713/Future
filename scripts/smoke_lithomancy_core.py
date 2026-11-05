import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future.lithomancy import PROFILE,FRAMES,read

def examples():
    roles=json.loads(Path('tests/fixtures/lithomancy_reference_v1.json').read_text(encoding='utf-8'))['roles']
    def stone(i,r,x,y):return dict(id=i,role_id=r,position=dict(x=x,y=y))
    def q(**kw):return dict(schema_version=1,profile=PROFILE,task='manual_spatial_reading',mode='manual',reading_id='example',frame=FRAMES[0],coverage='subset',origin='hypothetical',
        stones=[stone('self','lodestone',0,0),stone('onyx','onyx',3,4),stone('tiger','tigers_eye',1,0),stone('coin','five_pence_coin',-1,0),stone('glass','sea_glass',0,-2)],anchor=dict(kind='personal_stone',stone_id='self'))|kw
    out={'basic':q(coverage='full_example',stones=[stone('s'+str(i),r['role_id'],i,i*i-7) for i,r in enumerate(roles)],anchor=dict(kind='personal_stone',stone_id='s0')),'personal':q(),'reader':q(anchor=dict(kind='reader',position=dict(x=2,y=-3))),
         'nearest':q(stones=[stone('self','lodestone',0,0),stone('onyx','onyx',1,1),stone('tiger','tigers_eye',3,4)]),'tie':q(),
         'coincident':q(stones=[stone('self','lodestone',0,0),stone('onyx','onyx',0,0),stone('coin','five_pence_coin',0,0)]),
         'asymmetric':q(stones=[stone('self','lodestone',2,-3),stone('onyx','onyx',-1,1),stone('tiger','tigers_eye',6,-6),stone('coin','five_pence_coin',3,-1)]),
         'incomplete':q(stones=[stone('onyx','onyx',1,1),stone('tiger','tigers_eye',3,4)],anchor=dict(kind='reader',position=dict(x=0,y=0))),
         'missing-anchor':q(anchor=None),'missing-position':q(),'unknown-anchor':q(),'uncertainty':q(uncertainty=True),
         'relations':q(relations=[dict(**{'from':'onyx','to':'self'},relation='left'),dict(**{'from':'coin','to':'tiger'},relation='near')]),
         'groups':q(groups=[dict(id='pair',members=['coin','tiger'],association=' Voluntarily grouped; no combined source fortune. ')]),
         'unicode':q(question='  Café Café\r\n猫\t `````json  ',commentary='  Manual hypothetical placement. '),'down-frame':q(frame=FRAMES[1])}
    out['missing-position']['stones'][1]['position']=None;out['unknown-anchor']['stones'][0]['position']=None
    out['unicode']['stones'][1]['association']=' 個人\r\n  '
    return out

def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'q.json')
        def check(name,q,fmt='json',reject=False,save=None):
            path.write_bytes(json.dumps(q,ensure_ascii=False).encode('utf-8'))
            p=subprocess.run([sys.executable,'-m','future','lithomancy',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr,p.stdout[:300])
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['lithomancy_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==read(q)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert read(json.loads(m[2])['request'])==read(q)
            if save:Path('data',save).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'lithomancy-{name}-input.json').write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
            check(name+' JSON',q,save=f'lithomancy-{name}.json');check(name+' Markdown',q,'markdown',save=f'lithomancy-{name}.md');check(name+' repeat',q)
        unknown=copy.deepcopy(rows['personal']);unknown['stones'][1]['role_id']='unknown'
        duplicate=copy.deepcopy(rows['personal']);duplicate['stones'][1]['id']='self'
        mixed=copy.deepcopy(rows['personal']);mixed['stones'][1]['role_id']='wimmer.sun'
        invalid=copy.deepcopy(rows['personal']);invalid['stones'][1]['position']['x']=True
        bad={'unknown-role':unknown,'duplicate-id':duplicate,'mixed-author':mixed,'wimmer-circle':rows['personal']|dict(circle_radius=5),'invalid-coordinate':invalid,
             'wrong-frame':rows['personal']|dict(frame='cup-handle'),'seeded':rows['personal']|dict(mode='seeded'),'wrong-profile':rows['personal']|dict(profile='universal13')}
        saved={'unknown-role','duplicate-id','mixed-author','wimmer-circle','invalid-coordinate'}
        for name,q in bad.items():
            if name in saved:Path('data',f'lithomancy-{name}-input.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,reject=True,save=f'lithomancy-{name}.json' if name in saved else None)
            check(name+' Markdown',q,'markdown',True,f'lithomancy-{name}.md' if name in saved else None)
    Path('data/lithomancy-input.json').write_text(json.dumps(rows['basic'],indent=2)+'\n',encoding='utf-8')
    Path('data/lithomancy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    for name,q in rows.items():
        assert json.loads(Path('data',f'lithomancy-{name}.json').read_text(encoding='utf-8'))==read(q)
        text=Path('data',f'lithomancy-{name}.md').read_text(encoding='utf-8');m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert read(json.loads(m[2])['request'])==read(q)
    print(len(cases),f'Lithomancy CLI cases passed;{len(rows)} JSON/{len(rows)} Markdown saved replays verified')
if __name__=='__main__':run()
