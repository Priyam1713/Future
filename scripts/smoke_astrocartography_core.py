"""Public interfaces, reproducible samples, explicit unsupported configurations."""
import json
import subprocess
import sys
from pathlib import Path


def run():
    base=[sys.executable,'-X','utf8','-m','future']
    args=['astrocartography','1990-07-15T14:30:00','Asia/Kolkata','28.6139','77.209']
    destinations=json.dumps([dict(name='London',latitude=51.5,longitude=0,zone='Europe/London'),
                             dict(name='Sydney',latitude=-33.8688,longitude=151.2093,zone='Australia/Sydney')])
    sample=args+['--destinations',destinations,'--query','28.6','77.2','--uncertainty-minutes','5']
    cases=[('JSON',sample,False,'astrocartography-july1990.json'),
        ('Markdown',sample+['--format','markdown'],False,'astrocartography-july1990.md'),
        ('GeoJSON',args+['--format','geojson'],False,'astrocartography-july1990.geojson'),
        ('classical seven',args+['--bodies','Sun,Moon,Mercury,Venus,Mars,Jupiter,Saturn'],False,None),
        ('polar map',['astrocartography','2000-01-01','UTC','80','179.9','--query','90','180'],False,None),
        ('DST fold',['astrocartography','2024-11-03T01:30:00','America/New_York','40','-74','--fold','1'],False,None),
        ('ambiguous',['astrocartography','2024-11-03T01:30:00','America/New_York','40','-74'],True,None),
        ('gap',['astrocartography','2024-03-10T02:30:00','America/New_York','40','-74'],True,None),
        ('wrong profile',args+['--profile','Lewis'],True,None),
        ('unsupported body',args+['--bodies','Node'],True,None),
        ('invalid query',args+['--query','91','0'],True,None),
        ('invalid tolerance',args+['--tolerance','0'],True,None)]
    results=[]
    for name,command,reject,path in cases:
        p=subprocess.run(base+command,capture_output=True,text=True,encoding='utf-8')
        assert (p.returncode!=0)==reject,(name,p.stderr)
        if not reject and name!='Markdown':
            r=json.loads(p.stdout)
            if name=='GeoJSON':assert len(r['features'])==40 and r['type']=='FeatureCollection'
            else:
                assert r['technique_id']==7
                assert len(r['geojson']['features'])==(28 if name=='classical seven' else 40)
                if name=='polar map':assert r['natal_frame']['status']=='unsupported'
                if name=='JSON':
                    assert len(r['relocated_frames'])==2 and len(r['birth_time_sensitivity'])==2
                    assert r['birth']['utc']=='1990-07-15T09:00:00+00:00'
        if path:Path('data',path).write_text(p.stdout,encoding='utf-8')
        results.append(dict(case=name,passed=True))
    Path('data/astrocartography-smoke.json').write_text(json.dumps(results,indent=2)+'\n')
    print(len(results),'Astrocartography CLI cases passed')

if __name__=='__main__':run()
