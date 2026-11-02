"""Swiss/Moshier development oracle; independent symbolic epoch arithmetic."""
from datetime import datetime
from pathlib import Path
import json,math
import swisseph as s

def tt(date):
    d=datetime.fromisoformat(date)
    hour=d.hour+d.minute/60+d.second/3600
    if d.year<1972:
        # Match the explicitly declared proleptic UTC convention, not historical UT1.
        return s.julday(d.year,d.month,d.day,hour)+42.184/86400
    if d.year>=2017:
        # Explicitly freeze the known 37-second TAI-UTC offset, as Skyfield does.
        # Do not let the oracle silently switch future UTC to UT1.
        return s.julday(d.year,d.month,d.day,hour)+69.184/86400
    return s.utc_to_jd(d.year,d.month,d.day,d.hour,d.minute,d.second)[0]

systems={'porphyry':b'O','placidus':b'P','regiomontanus':b'R','campanus':b'C'}
rows=[]
for birth,target,lat,lon in [('1990-07-15T09:00:00','2026-11-02T00:00:00',28.6139,77.209),
 ('2000-02-29T12:00:00','2001-02-28T12:00:00',-33.9,151.2),
 ('1940-06-01T12:00:00','1980-06-01T12:00:00',51.5,0),
 ('1990-07-15T09:00:00','2050-07-15T09:00:00',-45,-70)]:
    b,t=tt(birth),tt(target)
    for year_key,year_days in [('tropical',365.24219),('julian',365.25)]:
        age=(t-b)/year_days; jd=b+age
        positions={name:{'longitude':s.calc(jd,i,s.FLG_MOSEPH|s.FLG_SPEED)[0][0],
                         'retrograde':s.calc(jd,i,s.FLG_MOSEPH|s.FLG_SPEED)[0][3]<0}
                   for i,name in enumerate(['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto'])}
        natal_positions={name:s.calc(b,i,s.FLG_MOSEPH)[0][0] for i,name in enumerate(positions)}
        natal_ut=b-s.deltat(b)
        axes=s.houses(natal_ut,lat,lon,b'E')[1]
        natal_positions.update(ascendant=axes[0],midheaven=axes[1])
        expected_cross=[];expected_mutual=[]
        for name,p in positions.items():
            for target_name,q in natal_positions.items():
                separation=abs((p['longitude']-q+180)%360-180)
                for angle in (0,60,90,120,180):
                    if abs(separation-angle)<=1:expected_cross.append([name,target_name,angle])
        names=list(positions)
        for i,name in enumerate(names):
            for other in names[i+1:]:
                separation=abs((positions[name]['longitude']-positions[other]['longitude']+180)%360-180)
                for angle in (0,60,90,120,180):
                    if abs(separation-angle)<=1:expected_mutual.append([name,other,angle])
        eps=s.calc(jd,s.ECL_NUT)[0][0]
        birth_ut=b-s.deltat(b);prog_ut=jd-s.deltat(jd)
        birth_armc=(s.sidtime(birth_ut)*15+lon)%360
        mc=s.houses(birth_ut,lat,lon,b'E')[1][1]
        arc=(positions['Sun']['longitude']-s.calc(b,s.SUN,s.FLG_MOSEPH)[0][0]+180)%360-180
        rad=math.radians((mc+arc)%360)
        armcs={'naibod-ra':(birth_armc+age*.98564733)%360,
               'solar-arc-mc':math.degrees(math.atan2(math.sin(rad)*math.cos(math.radians(eps)),math.cos(rad)))%360,
               'secondary-rotation':(s.sidtime(prog_ut)*15+lon)%360}
        row=dict(birth_utc=birth+'+00:00',target_utc=target+'+00:00',latitude=lat,longitude=lon,
                 year_key=year_key,year_days=year_days,jd_tt=jd,planets=positions,
                 progressed_to_natal=expected_cross,progressed_to_progressed=expected_mutual,
                 angle_cusps={a:{n:list(s.houses_armc(armc,lat,eps,c)[0]) for n,c in systems.items()} for a,armc in armcs.items()})
        if birth.startswith('1990') and target.startswith('2026') and year_key=='tropical':
            a,bis=jd,jd+1
            for _ in range(50):
                mid=(a+bis)/2
                if s.calc(mid,s.MOON,s.FLG_MOSEPH)[0][0]<150:a=mid
                else:bis=mid
            real_tt=b+((a+bis)/2-b)*year_days
            row['moon_virgo_ingress_utc']=s.jdet_to_utc(real_tt)
            a,bis=jd-.5,jd
            for _ in range(50):
                mid=(a+bis)/2
                difference=(s.calc(mid,s.MOON,s.FLG_MOSEPH)[0][0]-s.calc(mid,s.SUN,s.FLG_MOSEPH)[0][0]+180)%360-180
                if difference<0:a=mid
                else:bis=mid
            row['newmoon_before_target_utc']=s.jdet_to_utc(b+((a+bis)/2-b)*year_days)
        rows.append(row)
Path('tests/fixtures/progression_reference.json').write_text(json.dumps({'oracle':'Swiss Ephemeris/Moshier 2.10.3.2 TT positions; independent day/year formula; angle reference uses Swiss delta-T',
    'historical_clock':'Before 1972 use proleptic 42.184 seconds TT-minus-UTC to match declared Skyfield model, not reconstructed historical UTC.',
    'charts':rows},indent=2))
