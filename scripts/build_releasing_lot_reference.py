"""Independent Swiss/Moshier angles, altitude/sect and reversed Lots; no Future imports."""
import json
from pathlib import Path
import swisseph as s
cases=[]
for local,zone,utc,lat,lon in [('1961-07-01T19:45','Europe/London',(1961,7,1,18.75),52+50/60,.5),
                              ('1990-07-15T14:30','Asia/Kolkata',(1990,7,15,9),28.6139,77.209),
                              ('2000-02-29T23:00','Australia/Sydney',(2000,2,29,12),-33.9,151.2)]:
    # Match the documented engine time *convention*, not its calculations:
    # pre-1972 proleptic UTC has TT-UTC=42.184s. Derive UT1 independently.
    civil=s.julday(*utc)
    tt=civil+42.184/86400 if utc[0]<1972 else s.utc_to_jd(*utc[:3],int(utc[3]),0,0)[0]
    jd=tt-s.deltat(tt)
    sun=s.calc(tt,s.SUN,s.FLG_MOSEPH)[0];moon=s.calc(tt,s.MOON,s.FLG_MOSEPH)[0]
    _,axes=s.houses(jd,lat,lon,b'W');asc=axes[0]
    altitude=s.azalt(jd,s.ECL2HOR,(lon,lat,0),0,0,sun[:3])[1]
    arc=moon[0]-sun[0] if altitude>=0 else sun[0]-moon[0]
    cases.append(dict(local=local,zone=zone,latitude=lat,longitude=lon,sun_altitude_degrees=altitude,
        Fortune=(asc+arc)%360,Spirit=(asc-arc)%360))
Path('tests/fixtures/releasing_lot_reference.json').write_text(json.dumps({'oracle':'Swiss Ephemeris 2.10.3.2 Moshier; explicit proleptic UTC TT-UTC 42.184s before 1972; Swiss delta-T UT1; geometric Sun altitude; reversed night Lots','tolerance_degrees':.01,'cases':cases},indent=2))
