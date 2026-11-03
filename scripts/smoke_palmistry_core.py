"""Reproducible source-scoped manual readings and public CLI acceptance cases."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import copy


def run():
    base=[sys.executable,'-X','utf8','-m','future','palmistry']
    source=Path('data/palmistry-observations.json')
    observation=json.loads(source.read_text(encoding='utf-8'))
    cases=[]
    def check(name,path,extra=(),reject=False,output=None):
        p=subprocess.run(base+[str(path)]+list(extra),capture_output=True,text=True,encoding='utf-8')
        assert (p.returncode!=0)==reject,(name,p.stderr)
        if not reject and '--format' not in extra:
            r=json.loads(p.stdout);assert r['technique_id']==8 and r['profile']=='cheiro-ninth-manual-v1'
            if name=='complete JSON':
                assert len(r['hands'])==2
                assert all(len(h['readings'])>=12 for h in r['hands'])
                assert not any(h['observation_conflicts'] for h in r['hands'])
            if name=='unknown':assert not r['hands'][0]['readings']
            if name=='conflict':assert r['hands'][0]['observation_conflicts']
            if name=='left dominance':assert not r['hand_use']['dominance_reversal_applied']
        if output:Path('data',output).write_text(p.stdout,encoding='utf-8')
        cases.append(dict(case=name,passed=True))
    check('complete JSON',source,output='palmistry-reading.json')
    check('Markdown',source,['--format','markdown'],output='palmistry-reading.md')
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'observations.json')
        def case(name,o,reject=False):
            path.write_text(json.dumps(o),encoding='utf-8');check(name,path,reject=reject)
        minimal=dict(schema_version=1,profile='cheiro-ninth-manual-v1',hands=[dict(side='left')])
        case('unknown',minimal)
        o=copy.deepcopy(minimal);o['dominance']='left';case('left dominance',o)
        o=copy.deepcopy(minimal);o['hands'][0]['lines']=dict(heart=dict(presence='absent',origin='jupiter'));case('conflict',o)
        o=copy.deepcopy(minimal);o['profile']='Benham';case('wrong school',o,True)
        o=copy.deepcopy(minimal);o['hands'][0]['shape']=dict(type='fire');case('unverified type',o,True)
        o=copy.deepcopy(minimal);o['hands']*=2;case('duplicate side',o,True)
        o=copy.deepcopy(minimal);o['hands'][0]['image']='hand.jpg';case('image not silently read',o,True)
        path.write_text('{"schema_version":1,"schema_version":2}',encoding='utf-8');check('duplicate JSON keys',path,reject=True)
    Path('data/palmistry-smoke.json').write_text(json.dumps(cases,indent=2)+'\n')
    print(len(cases),'Palmistry CLI cases passed')

if __name__=='__main__':run()
