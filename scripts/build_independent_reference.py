"""Development-only independent oracle; pyswisseph is never a product dependency.
Run locally with pyswisseph 2.10.3.2. Uses Moshier, not the JPL kernel under test.
"""
import json
from pathlib import Path
import swisseph as swe
from datetime import datetime
from future.natal import birth_utc
charts=[]
for local,zone,lat,lon in [('2000-01-01T12:00','Europe/London',51.4779,0),
                           ('1990-07-15T14:30','Asia/Kolkata',28.6139,77.209),
                           ('2024-04-08T14:00','America/New_York',40.7128,-74.006)]:
    utc=birth_utc(local,zone)
    jd=swe.julday(utc.year,utc.month,utc.day,utc.hour+utc.minute/60)
    longs={}; retro={}
    for i,name in enumerate(['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']):
        values,flags=swe.calc_ut(jd,i,swe.FLG_MOSEPH|swe.FLG_SPEED)
        longs[name]=values[0]; retro[name]=values[3]<0
    cusps,angles=swe.houses(jd,lat,lon,b'E')
    charts.append(dict(local=local,zone=zone,latitude=lat,longitude=lon,longitudes=longs,retrograde=retro,
                       ascendant=angles[0],midheaven=angles[1],equal_cusps=list(cusps)))
path=Path('tests/fixtures/swiss_reference.json'); path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps({'oracle':'Swiss Ephemeris 2.10.03 / pyswisseph 2.10.3.2, Moshier, apparent tropical of date; UTC approximates UT1 for reference only',
                           'source':'https://www.astro.com/swisseph/swephprg.htm','charts':charts},indent=2))
