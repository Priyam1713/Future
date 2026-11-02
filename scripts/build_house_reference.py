"""Independent Swiss oracle, development only; no Swiss code in runtime."""
import json
from pathlib import Path
import swisseph as swe
systems={'porphyry':b'O','placidus':b'P','regiomontanus':b'R','campanus':b'C'}
frames=[]
for armc in (0,17,89.9,120,230,359.9):
    for lat in (-60,-33.9,0,28.6,51.5,65):
        frames.append({'armc':armc,'latitude':lat,'obliquity':23.44,'systems':
                       {name:list(swe.houses_armc(armc,lat,23.44,code)[0]) for name,code in systems.items()}})
dates=[]
for year,month,day,lat,lon in [(1879,3,14,48.4,10),(1990,7,15,28.6139,77.209),
                              (2000,2,29,-33.9,151.2),(2024,4,8,40.7,-74),(2026,11,2,-60,-70)]:
    jd=swe.julday(year,month,day,12)
    dates.append({'ut1_calendar':f'{year:04d}-{month:02d}-{day:02d}T12:00:00','jd_ut1':jd,'latitude':lat,'longitude':lon,
                  'systems':{name:list(swe.houses(jd,lat,lon,code)[0]) for name,code in systems.items()}})
Path('tests/fixtures/house_reference.json').write_text(json.dumps({'oracle':'Swiss Ephemeris 2.10.3.2 houses_armc / houses; date references approximate UTC as UT1',
    'source':'https://www.astro.com/swisseph/swephprg.htm','frames':frames,'dates':dates},indent=2))
