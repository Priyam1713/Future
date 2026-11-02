"""Independent Swiss/Moshier true-altitude oracle, geocentric solar parallax tolerance."""
import json
from pathlib import Path
import swisseph as s
cases=[]
for y,m,d in [(1940,6,1),(1990,7,15),(2024,12,21)]:
    for hour,lat,lon in [(0,28.6,77.2),(12,28.6,77.2),(0,-33.9,151.2),(12,-33.9,151.2)]:
        jd=s.julday(y,m,d,hour)
        coords=s.calc_ut(jd,s.SUN,s.FLG_MOSEPH|s.FLG_EQUATORIAL)[0][:3]
        alt=s.azalt(jd,s.EQU2HOR,(lon,lat,0),0,0,coords)[1]
        cases.append({'jd_ut1':jd,'latitude':lat,'longitude':lon,'sun_true_altitude':alt,'sect':'day' if alt>=0 else 'night'})
Path('tests/fixtures/sect_reference.json').write_text(json.dumps({'oracle':'Swiss/Moshier apparent geocentric Sun, true horizon altitude. Topocentric comparison tolerance 0.02 degree.',
 'cases':cases},indent=2))
