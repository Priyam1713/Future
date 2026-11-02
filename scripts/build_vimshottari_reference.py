"""Independent rational arithmetic implementation from documented tables.
Uses previously generated Swiss Moon positions; no Future imports. This is a
second implementation of the same symbolic rule, not evidence of prediction.
"""
from fractions import Fraction as F
from datetime import datetime,timedelta
from pathlib import Path
import json
names=['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']
years=[7,20,6,10,7,18,16,19,17]
cases=[]
for c in json.loads(Path('tests/fixtures/vedic_reference.json').read_text())['cases']:
    for key,year_days in [('pvr-2000-savana',F(360)),('solar-365.2425',F(146097,400))]:
        birth=datetime.fromisoformat(c['utc']);target=birth+timedelta(days=10000)
        unit=year_days*86400;position=F(str(c['positions']['Moon']['longitude']))*27/360
        index=int(position)%9;elapsed=position-int(position)
        current_offset=-unit*years[index]*elapsed;rows=[]
        first_end=current_offset+unit*years[index]
        for count in range(27):
            parent=(index+count)%9;length=unit*years[parent];end=current_offset+length
            if current_offset<=10000*86400<end:
                used=F(0)
                for child in list(range(parent,9))+list(range(parent)):
                    right=current_offset+length*(used+years[child])/120
                    if current_offset+length*used/120<=10000*86400<right:
                        cases.append(dict(local=c['local'],zone=c['zone'],latitude=c['latitude'],longitude=c['longitude'],year_key=key,
                            target_utc=target.isoformat(),birth_md_end_utc=(birth+timedelta(seconds=float(first_end))).isoformat(),
                            moon_reference=c['positions']['Moon']['longitude'],
                            current_md=names[parent],current_ad=names[child],current_ad_end_utc=(birth+timedelta(seconds=float(right))).isoformat()))
                        break
                    used+=years[child]
                break
            current_offset=end
Path('tests/fixtures/vimshottari_reference.json').write_text(json.dumps({'oracle':'Independent Fraction implementation, PVR Table38/16.2–16.3, Swiss/Moshier Moon input; fixed elapsed days. Same symbolic rule, independently implemented; no predictive validity inferred.',
    'moon_tolerance_degrees':.0005,
    'tolerance_note':'Require Moon agreement within .0005 degree (1.8 arcseconds); derive timing bound per initial MD length and selected year: .0005*MDyears*yearDays*86400/(40/3). At most about 6.6 hours for a 20-year solar MD. Pure published arithmetic checked separately at microsecond scale.',
    'cases':cases},indent=2)+'\n',encoding='utf-8')
