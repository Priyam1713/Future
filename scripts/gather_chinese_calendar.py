"""Collect numeric CNY facts from HKO primary tables; no book/webpage ingestion."""
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen, Request
from pathlib import Path
import re, json, hashlib, time

def get(year):
    url=f'https://www.weather.gov.hk/en/gts/time/calendar/text/files/T{year}e.txt'
    for attempt in range(3):
        try:
            raw=urlopen(Request(url,headers={'User-Agent':'Future calendar verification'}),timeout=35).read()
            # Older tables include legacy encoded footer characters. Parsed calendar
            # labels/dates are ASCII; preserve raw hash and do not ingest the footer.
            text=raw.decode('ascii',errors='replace')
            matches=re.findall(r'^(\d{4})/(\d{1,2})/(\d{1,2})\s+1st Lunar Month\b',text,re.M|re.I)
            if len(matches)!=1:raise ValueError(f'CNY marker not unique: {year}: {matches}')
            y,m,d=map(int,matches[0]);assert y==year and m in (1,2)
            return {'year':year,'cny':f'{y:04}-{m:02}-{d:02}','url':url,'sha256':hashlib.sha256(raw).hexdigest()}
        except Exception:
            if attempt==2:raise
            time.sleep(1)

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        records=list(pool.map(get,range(1901,2101)))
    Path('knowledge/chinese_new_years.json').write_text(json.dumps({'source_id':'chinese-hko-cny-v1',
        'convention':'HKO Gregorian date of first lunar month; local festival date profile, not conjunction instant',
        'records':records},indent=2)+'\n',encoding='utf-8')
    print(f'Validated {len(records)} unique primary CNY dates,1901–2100',flush=True)
