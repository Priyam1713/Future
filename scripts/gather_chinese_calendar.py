"""Collect numeric CNY facts from HKO primary tables; no book/webpage ingestion."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen, Request
from pathlib import Path
import re, json, hashlib, time

def get(year):
    cache=Path(f'tmp/pdfs/hko-cny-{year}.json')
    if cache.exists():return json.loads(cache.read_text(encoding='utf-8'))
    url=f'https://www.weather.gov.hk/en/gts/time/calendar/text/files/T{year}e.txt'
    for attempt in range(3):
        try:
            raw=urlopen(Request(url,headers={'User-Agent':'Future calendar verification'}),timeout=8).read()
            # Older tables include legacy encoded footer characters. Parsed calendar
            # labels/dates are ASCII; preserve raw hash and do not ingest the footer.
            text=raw.decode('ascii',errors='replace')
            matches=re.findall(r'^(\d{4})/(\d{1,2})/(\d{1,2})\s+1st Lunar Month\b',text,re.M|re.I)
            if len(matches)!=1:raise ValueError(f'CNY marker not unique: {year}: {matches}')
            y,m,d=map(int,matches[0]);assert y==year and m in (1,2)
            record={'year':year,'cny':f'{y:04}-{m:02}-{d:02}','url':url,'sha256':hashlib.sha256(raw).hexdigest()}
            cache.parent.mkdir(parents=True,exist_ok=True)
            cache.write_text(json.dumps(record),encoding='utf-8')
            return record
        except Exception:
            if attempt==2:raise
            time.sleep(1)

if __name__=='__main__':
    records=[];errors=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs={pool.submit(get,y):y for y in range(1901,2101)}
        for job in as_completed(jobs):
            try:records.append(job.result())
            except Exception as ex:errors.append((jobs[job],str(ex)))
            if (len(records)+len(errors))%20==0:print(f'CNY facts collected:{len(records)}; failures:{len(errors)}',flush=True)
    if errors:raise ValueError(errors)
    records.sort(key=lambda r:r['year'])
    Path('knowledge/chinese_new_years.json').write_text(json.dumps({'source_id':'chinese-hko-cny-v1',
        'convention':'HKO Gregorian date of first lunar month; local festival date profile, not conjunction instant',
        'records':records},indent=2)+'\n',encoding='utf-8')
    print(f'Validated {len(records)} unique primary CNY dates,1901–2100',flush=True)
