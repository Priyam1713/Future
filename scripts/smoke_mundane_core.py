"""Public CLI acceptance and reproducible Green-based examples."""
from pathlib import Path
import json,subprocess,sys

def run():
    base=[sys.executable,'-X','utf8','-m','future']
    ingress=['mundane-ingress','2026','Europe/London','51.5','0']
    cycle=['mundane-cycle','2020-12-01T00:00:00+00:00','2021-01-01T00:00:00+00:00','Europe/London','51.5','0']
    cases=[('London JSON',ingress,False,'mundane-ingresses-2026-london.json'),
        ('London Markdown',ingress+['--historical-duration','--format','markdown'],False,'mundane-ingresses-2026-london.md'),
        ('Sydney JSON',['mundane-ingress','2026','Australia/Sydney','-33.8688','151.2093'],False,'mundane-ingresses-2026-sydney.json'),
        ('leap2000',['mundane-ingress','2000','UTC','0','0'],False,None),
        ('cycle JSON',cycle,False,'mundane-cycle-2020.json'),
        ('cycle Markdown',cycle+['--format','markdown'],False,'mundane-cycle-2020.md'),
        ('empty window',['mundane-cycle','2026-07-01T00:00:00+00:00','2026-07-02T00:00:00+00:00','UTC','0','0'],False,None),
        ('wrong profile',ingress+['--profile','Raphael'],True,None),
        ('polar',['mundane-ingress','2026','UTC','60','0'],True,None),
        ('unsupported year',['mundane-ingress','2149','UTC','0','0'],True,None),
        ('explicit location required',['mundane-ingress','2026','UTC'],True,None),
        ('naive range',['mundane-cycle','2026-01-01','2026-02-01','UTC','0','0'],True,None)]
    results=[];london=None
    for name,args,reject,output in cases:
        p=subprocess.run(base+args,capture_output=True,text=True,encoding='utf-8')
        assert (p.returncode!=0)==reject,(name,p.stderr)
        if not reject and 'Markdown' not in name:
            r=json.loads(p.stdout);assert r['technique_id']==6 and r['profile']=='green-1911-tropical-placidus-v1'
            if name in ('London JSON','Sydney JSON','leap2000'):assert len(r['events'])==4
            if name=='London JSON':london=r
            if name=='Sydney JSON':
                assert [e['utc'] for e in r['events']]==[e['utc'] for e in london['events']]
                assert r['events'][0]['chart']['angles']!=london['events'][0]['chart']['angles']
            if name=='cycle JSON':assert len(r['events'])==1
            if name=='empty window':assert not r['events']
        if output:Path('data',output).write_text(p.stdout,encoding='utf-8')
        results.append({'case':name,'passed':True})
    Path('data/mundane-smoke.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(len(results),'Mundane CLI cases passed')
if __name__=='__main__':run()
