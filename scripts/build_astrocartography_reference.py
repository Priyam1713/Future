"""Optional Swiss/Moshier oracle; no Future or Skyfield imports. Reference-only license."""
import json
from pathlib import Path
from datetime import datetime
import swisseph as s
from importlib.metadata import version

NAMES='Sun Moon Mercury Venus Mars Jupiter Saturn Uranus Neptune Pluto'.split()


def build():
    cases=[]
    for iso in ['1990-07-15T06:30:00+00:00','2000-02-29T23:55:00+00:00',
                '2024-12-21T12:00:00+00:00','2026-03-20T18:00:00+00:00']:
        d=datetime.fromisoformat(iso)
        tt,ut=s.utc_to_jd(d.year,d.month,d.day,d.hour,d.minute,d.second)
        planets={};lines=[]
        for b,name in enumerate(NAMES):
            p=s.calc(tt,b,s.FLG_MOSEPH|s.FLG_EQUATORIAL)[0]
            planets[name]={'ra':p[0],'dec':p[1]}
            # Roots of Swiss altitude evaluated over geographic longitude; rising direction
            # determined independently by altitude change at increasing longitude.
            for lat in [-80,-60,-30,0,30,60,80]:
                def altitude(lon):return s.azalt(ut,s.EQU2HOR,(lon,lat,0),0,10,(p[0],p[1],1))[1]
                roots=[]
                for lo in range(-180,180):
                    hi=lo+1;fa=altitude(lo);fb=altitude(hi)
                    if fa*fb>=0:continue
                    a,bound=lo,hi
                    for _ in range(45):
                        mid=(a+bound)/2
                        if fa*altitude(mid)<=0:bound=mid
                        else:a=mid;fa=altitude(mid)
                    root=(a+bound)/2
                    angle='ASC' if altitude(root+.0001)>altitude(root-.0001) else 'DSC'
                    roots.append({'angle':angle,'longitude':root})
                lines.append(dict(planet=name,latitude=lat,roots=roots))
        sites=[]
        for lat,lon in [(51.5,0),(-33.8688,151.2093),(0,179.9),(59.9,-179.9)]:
            for system in ['P','R','C','O','E','W']:
                cusps,angles=s.houses_ex(ut,lat,lon,system.encode())
                sites.append(dict(latitude=lat,longitude=lon,system=system,cusps=list(cusps),ascendant=angles[0],midheaven=angles[1]))
        cases.append(dict(utc=iso,jd_tt=tt,jd_ut1=ut,gast_degrees=s.sidtime(ut)*15,planets=planets,horizon_roots=lines,sites=sites))
    data=dict(id='astrocartography-swiss-v1',oracle='pyswisseph '+version('pyswisseph')+' / Swiss '+s.version,
        license='Swiss reference-only; not a production dependency. See existing licensing audit.',
        method='Swiss Moshier apparent equatorial coordinates; Swiss UTC/TT/UT1; azalt true altitude roots over longitude and houses_ex.',
        cases=cases)
    Path('tests/fixtures/astrocartography_swiss.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Built',len(cases),'independent epochs,',len(cases)*70,'latitude/planet root cases,',len(cases)*24,'house charts')

if __name__=='__main__':build()
