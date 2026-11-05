import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future.pyromancy import PROFILE,read


def examples():
    f=json.loads(Path('tests/fixtures/pyromancy_reference_v1.json').read_text(encoding='utf-8'))
    def row(name):
        c=next(x for x in f['cases'] if x['name']==name)
        return dict(id='o1',phenomenon=c['phenomenon'],attributes=copy.deepcopy(c['attributes']),physical=copy.deepcopy(c['physical']))
    def q(rows=None,**kw):return dict(schema_version=1,profile=PROFILE,task='symbolic_candle_observation',mode='manual',origin='hypothetical',observations=rows or [])|kw
    conflict=row('low_sound_no_correction_needed');conflict['physical']['wick']='drowned'
    missing=row('upper_black');missing['attributes'].pop('soot_location');missing['attributes'].pop('soot_extent')
    return {
        'tall-persistent':q([row('high_after_correction')]),
        'tall-physical':q([row('high_known_cause')]),
        'tall-changed':q([row('high_changed')]),
        'low-persistent':q([row('low_sound_no_correction_needed')]),
        'low-improved':q([row('low_improved')]),
        'upper-soot':q([row('upper_dense')]),
        'full-soot':q([row('full_jar')]),
        'unknown-soot':q([missing]),
        'smoke':q([row('smoke_no_soot')]),
        'conflicting':q([conflict]),
        'hypothetical':q([row('high_after_correction')|dict(observation='  Café Café\r\n猫 🕯\t ',association='```json\n voluntary  ')],notes='Hypothetical comparison;no candle or flame was required.'),
        'unsafe-stopped':q([row('upper_dense')],safety=dict(unsafe_burning=True,stopped=True)),
        'active-hazard':q([row('high_after_correction')],origin='reported_real',safety=dict(active_hazard=True)),
        'lamp':q([row('lamp_no_rules')],documentary_reference='pgm_iv_52_87'),
        'color':q([row('color_no_rules')|dict(flame_color='blue',wax_color='red')]),
        'light-haze':q([row('upper_light')]),
        'empty':q(notes=None)}


def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'q.json')
        def check(name,q,fmt='json',reject=False,output=None):
            path.write_bytes(json.dumps(q,ensure_ascii=False).encode('utf-8'))
            p=subprocess.run([sys.executable,'-m','future','pyromancy',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr)
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['pyromancy_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==read(q)
            else:
                match=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S)
                assert read(json.loads(match[2])['request'])==read(q)
            if output:Path('data',output).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'pyromancy-{name}-input.json').write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
            check(name+' JSON',q,output=f'pyromancy-{name}.json')
            check(name+' Markdown',q,'markdown',output=f'pyromancy-{name}.md')
            check(name+' repeat JSON',q)
        invalid=copy.deepcopy(rows['tall-persistent']);invalid['observations'][0]['physical']['draft']=1
        bad=[('invalid draft',invalid),('book profile unsupported',rows['empty']|dict(profile='pamita-book2020')),
            ('seed unsupported',rows['empty']|dict(seed=1)),('camera unsupported',rows['empty']|dict(mode='camera')),
            ('ritual unsupported',rows['empty']|dict(documentary_reference='execute_lamp_rite')),('physical sensor unsupported',rows['empty']|dict(temperature=500)),
            ('duplicate observations',rows['empty']|dict(observations=[dict(id='x',phenomenon='flame')]*2)),('bad safety',rows['empty']|dict(safety=dict(active_hazard='no')))]
        for name,q in bad:check(name,q,reject=True,output='pyromancy-invalid.json' if name=='invalid draft' else None)
        check('invalid Markdown',invalid,'markdown',True,'pyromancy-invalid.md')
        Path('data/pyromancy-invalid-input.json').write_text(json.dumps(invalid,indent=2)+'\n',encoding='utf-8')
    Path('data/pyromancy-input.json').write_text(json.dumps(rows['tall-persistent'],indent=2)+'\n',encoding='utf-8')
    Path('data/pyromancy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Pyromancy CLI cases passed')


if __name__=='__main__':run()
