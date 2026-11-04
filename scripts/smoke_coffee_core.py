import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from future.coffee import PROFILE,read


def examples():
    def row(symbol='camel',i=1,**kw):return dict(id='o'+str(i),symbol_id=symbol)|kw
    def q(rows=None,**kw):return dict(schema_version=1,profile=PROFILE,task='symbolic_coffee_reading',mode='manual',vessel='cup',observations=rows or [])|kw
    line=row('line',attributes=dict(shape='flat',dots=3,dot_arrangement='at_line_end'))
    bird=row('bird',attributes=dict(stain=True,stain_position='peak_of_bird_figure'))
    moon=row('moon_patch',attributes=dict(shape='moon_shaped',color='white',location='bottom'))
    fixture=json.loads(Path('tests/fixtures/coffee_reference_v1.json').read_text(encoding='utf-8'))
    return {
        'basic':q([row('adhered_grounds',half='subject_facing',attributes=dict(adhered_after_inversion=True))],preparation=dict(grounds_remaining=True,inverted_onto_saucer=True,cooled=True)),
        'halves':q([row('horse',half='subject_facing'),row('fish',2,half='opposite')]),
        'direction':q([row('horse',half='opposite')],rotation='counterclockwise',intention='another'),
        'camel':q([row(attributes=dict(humps=2)),row(i=2,attributes=dict(humps=1)),row(i=3)]),
        'bird':q([bird,row('bird',2,attributes=dict(stain=False,stain_position='peak_of_bird_figure')),row('bird',3,attributes=dict(stain=True,stain_position='beak'))]),
        'line':q([line,row('line',2,attributes=dict(shape='flat',dots=3,dot_arrangement='scattered'))]),
        'moon-cup':q([moon,row('moon_patch',2,attributes=dict(shape='moon_shaped',color='white',location='side'))]),
        'moon-saucer':q([row('moon_patch',attributes=dict(shape='moon_shaped',color='white')),row('horse',2)],vessel='saucer'),
        'timing':q([line],notes='Three source alternatives remain days/months/years;no calendar selection or deadline.'),
        'multiple':q([row('horse',half='subject_facing'),row('camel',2,attributes=dict(humps=2)),row('moon_patch',3,vessel='saucer',attributes=dict(shape='moon_shaped',color='white'))]),
        'missing':q([row(),row('bird',2,attributes=dict(stain=True)),row('moon_patch',3,attributes=dict(shape='moon_shaped',color='white'))]),
        'conflicting':q([row(half=['subject_facing','opposite'],attributes=dict(humps=[1,2])),row('bird',2,attributes=dict(stain=[True,False],stain_position='peak_of_bird_figure'))],rotation=['clockwise','counterclockwise'],intention='self'),
        'unknown':q([row('anchor',observation='  Café Café\r\n猫 🐪\t  ',association='```json\n voluntary  ')]),
        'documentary':q(fixture['documentary_comparison']['observations'],source_example='p104_narrative',notes='Reconstructed comparisons of original p104 narrative examples,not a historical worked cup or experimental validation.'),
        'empty':q(notes=None)}


def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp,'input.json')
        def check(name,q,fmt='json',reject=False,output=None):
            p.write_bytes(json.dumps(q,ensure_ascii=False).encode('utf-8'))
            r=subprocess.run([sys.executable,'-m','future','coffee-reading',str(p),'--format',fmt],capture_output=True)
            assert r.returncode==(2 if reject else 0),(name,r.stderr)
            text=r.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['coffee_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==read(q)
            else:
                part=text.split('## Exact replay metadata')[1];m=re.search(r'(`{3,})json\n(.*?)\n\1',part,re.S)
                assert read(json.loads(m[2])['request'])==read(q)
            if output:Path('data',output).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,q in rows.items():
            Path('data',f'coffee-{name}-input.json').write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
            check(name+' JSON',q,output=f'coffee-{name}.json')
            check(name+' Markdown',q,'markdown',output=f'coffee-{name}.md')
            check(name+' repeat JSON',q)
        invalid=copy.deepcopy(rows['camel']);invalid['observations'][0]['attributes']['humps']=True
        bad=[('invalid hump boolean',invalid),('Kent profile',rows['empty']|dict(profile='kent-pg6964-ordinary-cup-v2')),
            ('seed unsupported',rows['empty']|dict(seed=1)),('image mode unsupported',rows['empty']|dict(mode='image')),
            ('handle axis unsupported',rows['empty']|dict(handle_orientation='top')),('turn count unsupported',rows['empty']|dict(turns=3)),
            ('wrong vessel',rows['empty']|dict(vessel='tea')),('bad source example',rows['empty']|dict(source_example='figure_viii'))]
        for name,q in bad:check(name,q,reject=True,output='coffee-invalid.json' if name=='invalid hump boolean' else None)
        check('invalid Markdown',invalid,'markdown',True,'coffee-invalid.md')
        Path('data/coffee-invalid-input.json').write_text(json.dumps(invalid,indent=2)+'\n',encoding='utf-8')
    Path('data/coffee-input.json').write_text(json.dumps(rows['basic'],indent=2)+'\n',encoding='utf-8')
    Path('data/coffee-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Coffee CLI cases passed')


if __name__=='__main__':run()
