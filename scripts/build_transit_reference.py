"""Development oracle: Swiss/Moshier, independent scan and interpolation solver."""
import json
from pathlib import Path
from datetime import datetime,timedelta,timezone
import swisseph as swe
start=datetime(2026,11,1,tzinfo=timezone.utc)
jd=swe.julday(2026,11,1,0)
def lon(t): return swe.calc_ut(t,swe.MERCURY,swe.FLG_MOSEPH|swe.FLG_SPEED)[0]
roots=[]
for i in range(30*4):
    a,b=jd+i/4,jd+(i+1)/4
    fa,fb=lon(a)[0]-225,lon(b)[0]-225
    if fa*fb<0:
        for _ in range(45):
            mid=(a+b)/2; fm=lon(mid)[0]-225
            if fa*fm<=0: b=mid
            else: a=mid; fa=fm
        roots.append({'utc':(start+timedelta(days=(a+b)/2-jd)).isoformat(),'retrograde':lon((a+b)/2)[3]<0})
positions=[]
for day in (0,7,14,21,29):
    positions.append({'utc':(start+timedelta(days=day)).isoformat(),'longitude':lon(jd+day)[0],'retrograde':lon(jd+day)[3]<0})
Path('tests/fixtures/transit_reference.json').write_text(json.dumps({'oracle':'pyswisseph 2.10.3.2 Swiss/Moshier apparent tropical; UTC approximates UT1',
 'target':225,'body':'Mercury','start':start.isoformat(),'roots':roots,'positions':positions},indent=2))
