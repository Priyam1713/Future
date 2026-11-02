"""Independent Swiss/Moshier reference; no Future imports, no runtime Swiss dependency."""
from datetime import datetime,timezone
from zoneinfo import ZoneInfo,reset_tzpath
from pathlib import Path
import json,swisseph as s
from skyfield.api import load
reset_tzpath(())
ts=load.timescale(builtin=True)
cases=[];s.set_sid_mode(s.SIDM_LAHIRI)
for local,zone,lat,lon in [('1990-07-15T14:30','Asia/Kolkata',28.6139,77.209),
    ('2000-04-09T17:55','America/New_York',42.5,-71.2),('1970-10-05T12:34','Asia/Kolkata',15.816666666666666,80.35),
    ('2000-02-29T23:00','Australia/Sydney',-33.9,151.2),('1879-03-14T11:30','Europe/Berlin',48.4,10),
    ('2149-06-01T12:00','UTC',51.5,0)]:
    utc=datetime.fromisoformat(local).replace(tzinfo=ZoneInfo(zone)).astimezone(timezone.utc)
    hour=utc.hour+utc.minute/60+utc.second/3600
    civil=s.julday(utc.year,utc.month,utc.day,hour)
    tt=(civil+42.184/86400 if utc.year<1972 else civil+69.184/86400 if utc.year>=2017
        else s.utc_to_jd(utc.year,utc.month,utc.day,utc.hour,utc.minute,utc.second)[0])
    # Geometry comparison needs identical UT1: this is a declared shared time
    # input, not an independent verification of the Skyfield delta-T model.
    ut=float(ts.from_datetime(utc).ut1)
    ps={n:s.calc(tt,i,s.FLG_MOSEPH|s.FLG_SIDEREAL|s.FLG_SPEED)[0] for n,i in [('Sun',0),('Moon',1),('Mercury',2),('Venus',3),('Mars',4),('Jupiter',5),('Saturn',6),('Rahu',s.MEAN_NODE)]}
    positions={n:{'longitude':p[0],'retrograde':p[3]<0} for n,p in ps.items()}
    positions['Ketu']={'longitude':(ps['Rahu'][0]+180)%360,'retrograde':ps['Rahu'][3]<0}
    _,axes=s.houses_ex(ut,lat,lon,b'W',s.FLG_SIDEREAL)
    sun=s.calc(tt,s.SUN,s.FLG_MOSEPH)[0]
    altitude=s.azalt(ut,s.ECL2HOR,(lon,lat,0),0,0,sun[:3])[1]
    cases.append(dict(local=local,zone=zone,latitude=lat,longitude=lon,utc=utc.isoformat(),jd_tt=tt,
        ayanamsha_true=s.get_ayanamsa_ex(tt,s.FLG_MOSEPH)[1],ascendant=axes[0],positions=positions,
        moon_nakshatra_index=int(ps['Moon'][0]*27/360),moon_pada=int(ps['Moon'][0]*108/360)%4+1,
        sun_above_horizon=altitude>=0))
Path('tests/fixtures/vedic_reference.json').write_text(json.dumps({'oracle':'Swiss Ephemeris 2.10.3.2/Moshier, SIDM_LAHIRI default; mean nodes; shared pinned Skyfield UT1 input for independent Swiss house geometry, not independent delta-T validation. Explicit pre-1972 proleptic UTC TT offset 42.184s and post-2017 frozen 69.184s.',
    'tolerances':{'positions_degrees':.01,'ascendant_degrees':.02,'ayanamsha_arcseconds':1},'cases':cases},indent=2)+'\n',encoding='utf-8')
