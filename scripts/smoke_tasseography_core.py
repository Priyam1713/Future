import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future.tasseography import PROFILE,read


def examples():
    def row(key,i=1,**kwargs):return dict(id='o'+str(i),symbol_id=key)|kwargs
    def request(rows=None,**kwargs):return dict(schema_version=1,profile=PROFILE,task='symbolic_cup_reading',mode='manual',vessel='cup',observations=rows or [])|kwargs
    f=json.loads(Path('tests/fixtures/tasseography_reference_v2.json').read_text(encoding='utf-8'))
    figure=[]
    for i,e in enumerate(f['figure_viii']['placements']):figure.append({k:v for k,v in e.items() if k!='beside'}|dict(id='f'+str(i)))
    figure[2]['adjacent_to']=['f1']
    return {
        'basic':request([row('anchor',region='rim')],handle_orientation='top'),
        'zones':request([row('anchor',region='rim'),row('apron',2,region='side',proximity='far'),row('acorn',3,region='bottom')]),
        'handle':request([row('cross',region='bottom',handle_relation='under_handle',size='small',multiplicity='single')],context=dict(abode='away')),
        'direction':request([row('aircraft',region='side',motion='flying',heading='towards_handle')]),
        'multiplicity':request([row('acorn',multiplicity='several',region='rim'),row('beetle',2,multiplicity='several',region='side')]),
        'adjacency':request([row('bird',motion='flying',heading='towards_handle',multiplicity='single',adjacent_to=['o2']),row('postal_mark',2)]),
        'conflicting':request([row('aircraft',motion='stationary',heading='towards_handle',alternatives=['apron'],region='side',region_alternatives=['bottom'],uncertainty=True)]),
        'missing':request([row('tea_cosy'),row('organ',2),row('unknown',3,observation='  A🐍 Café\r\n猫 ')]),
        'figure-viii':request(figure,source_example='figure_viii',context=dict(musician=True),notes='Original Kent FigureVIII comparison from independently transcribed source facts;not a synthetic cup advertised as historical.'),
        'marks':request([row('letter',mark='M',size='small',region='rim'),row('numeral',2,numeral=90,adjacent_to=['o3']),row('dots',3,arrangement='surrounding')],notes='No person,calendar date,currency or actual gain inferred.'),
        'empty':request(notes=None)}


def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            p=subprocess.run([sys.executable,'-m','future','tasseography',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr)
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['tasseography_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==read(value)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S)
                assert read(json.loads(m[2])['request'])==read(value)
            if output:Path('data',output).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'tasseography-{name}-input.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',q,output=f'tasseography-{name}.json');check(name+' Markdown',q,'markdown',output=f'tasseography-{name}.md')
        base=rows['empty'];invalid=copy.deepcopy(rows['basic']);invalid['observations'][0]['region']='saucer_centre'
        saucer=base|dict(vessel='saucer')
        bad=[('invalid placement',invalid),('saucer unsupported',saucer),('wrong profile',base|dict(profile='kent-pg6964-ordinary-cup-v1')),
            ('seed unsupported',base|dict(seed=1)),('wrong mode',base|dict(mode='image')),('duplicate observations',base|dict(observations=[dict(id='x',symbol_id='anchor')]*2)),
            ('unknown adjacency',base|dict(observations=[dict(id='x',symbol_id='anchor',adjacent_to=['y'])])),('bad context',base|dict(context=dict(musician='yes'))),
            ('invalid numeral',base|dict(observations=[dict(id='x',symbol_id='numeral',numeral=True)])),('invalid uncertainty',base|dict(observations=[dict(id='x',symbol_id='anchor',uncertainty=1)]))]
        for name,q in bad:
            output='tasseography-invalid.json' if name=='invalid placement' else 'tasseography-saucer-unsupported.json' if name=='saucer unsupported' else None
            check(name,q,reject=True,output=output)
        check('invalid Markdown',invalid,'markdown',True,'tasseography-invalid.md');check('saucer Markdown',saucer,'markdown',True,'tasseography-saucer-unsupported.md')
        Path('data/tasseography-invalid-input.json').write_text(json.dumps(invalid,indent=2)+'\n',encoding='utf-8')
        Path('data/tasseography-saucer-unsupported-input.json').write_text(json.dumps(saucer,indent=2)+'\n',encoding='utf-8')
    Path('data/tasseography-input.json').write_text(json.dumps(rows['basic'],indent=2)+'\n',encoding='utf-8')
    Path('data/tasseography-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Tasseography CLI cases passed')


if __name__=='__main__':run()
