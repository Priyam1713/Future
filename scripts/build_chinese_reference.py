"""Optional independent lunar-python1.4.8 oracle; no Future imports/code reuse.

Its astronomy/calendar implementation differs from Future's DE440s solar roots.
Year/month queried at the same instant in fixed Hong Kong time; day/hour at
the profile's effective wall date. This is not an independent IANA/DST check.
"""
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, reset_tzpath
from pathlib import Path
import json
from importlib.metadata import version
from lunar_python import Solar,Lunar

reset_tzpath(())
assert version('lunar-python')=='1.4.8'

def lunar(d):
    return Solar.fromYmdHms(d.year,d.month,d.day,d.hour,d.minute,d.second).getLunar()

cases=[]
for local,zone,lat,lon,fold in [
    ('1901-01-01T12:00','Asia/Shanghai',31.2,121.5,0),
    ('1918-12-01T12:30','Asia/Shanghai',0,120,0),
    ('1988-02-15T23:30','Asia/Shanghai',31.2,121.5,0),
    ('1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,0),
    ('2000-02-29T23:30','Australia/Sydney',-33.9,151.2,0),
    ('2005-12-23T08:37','Asia/Shanghai',31.2,121.5,0),
    ('2022-08-28T01:50','Asia/Shanghai',31.2,121.5,0),
    ('2026-02-04T04:01','Asia/Hong_Kong',22.3,114.2,0),
    ('2026-02-04T04:03','Asia/Hong_Kong',22.3,114.2,0),
    ('2026-03-05T21:58','Asia/Hong_Kong',22.3,114.2,0),
    ('2026-03-05T22:00','Asia/Hong_Kong',22.3,114.2,0),
    ('2026-11-01T01:30','America/New_York',40.7,-74,0),
    ('2026-11-01T01:30','America/New_York',40.7,-74,1),
    ('2034-02-19T00:00','Asia/Hong_Kong',22.3,114.2,0),
    ('2100-12-31T23:30','UTC',0,0,0)]:
    d=datetime.fromisoformat(local).replace(tzinfo=ZoneInfo(zone),fold=fold)
    utc=d.astimezone(timezone.utc)
    astro=lunar(utc.astimezone(timezone(timedelta(hours=8)))).getEightChar()
    for profile in ['civil-zi23','civil-split-zi','standard-zi23']:
        clock=d.replace(tzinfo=None)-(d.dst() if profile=='standard-zi23' else timedelta())
        day=lunar(clock).getEightChar();day.setSect(2 if profile=='civil-split-zi' else 1)
        ps=[astro.getYear(),astro.getMonth(),day.getDay(),day.getTime()]
        cases.append(dict(local=local,zone=zone,latitude=lat,longitude=lon,fold=fold,profile=profile,
            utc=utc.isoformat(),pillars=ps,
            ten_gods=[day.getYearShiShenGan(),day.getMonthShiShenGan(),day.getDayShiShenGan(),day.getTimeShiShenGan()]
            if zone=='Asia/Shanghai' and profile!='standard-zi23' else None))
# Read whole table as oracle facts, no code copied into production.
from lunar_python.util import LunarUtil
hidden=LunarUtil.ZHI_HIDE_GAN
Path('tests/fixtures/chinese_reference.json').write_text(json.dumps({
    'oracle':'lunar-python1.4.8/MIT; numeric results only. Shared pinned IANA inputs, independent calendar/astronomy.',
    'source_id':'chinese-six-tail-reference-v1','cases':cases,'hidden_stems':hidden,
    'cny_dates':{str(y):Lunar.fromYmd(y,1,1).getSolar().toYmd() for y in range(1901,2101)}},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(cases)} independent pillar cases')
