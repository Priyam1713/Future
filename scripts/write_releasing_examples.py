"""Reproduce separately labeled Spirit/Fortune examples, plus published date check."""
from pathlib import Path
from datetime import datetime
import json
from future.natal import SkyfieldEphemeris,chart,Settings
from future.releasing import from_natal,markdown

e=SkyfieldEphemeris('data/de440s.bsp')
try:
    n=chart(e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,Settings(tradition='Hellenistic'))
    start=datetime.fromisoformat('2026-11-02T00:00:00+00:00');end=datetime.fromisoformat('2026-12-02T00:00:00+00:00')
    for lot in ('Spirit','Fortune'):
        r=from_natal(e,n,start,end,lot=lot)
        path=Path('data/releasing-'+lot.lower()+'-1990-2026')
        path.with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
        path.with_suffix('.md').write_text(markdown(r),encoding='utf-8')
    n=chart(e,'1961-07-01T19:45','Europe/London',52+50/60,.5,Settings(tradition='Hellenistic'))
    r=from_natal(e,n,datetime.fromisoformat('1997-07-21T00:00:00+00:00'),datetime.fromisoformat('1997-07-24T00:00:00+00:00'),lot='Fortune')
    r['published_comparison']={'source_id':'zr-brennan-schaim-192','locator':'Loosing of the Bond: Diana Fortune example',
        'published_transition_date':'1997-07-22','validation':'Date-level agreement only. Published source does not establish an exact UTC time.',
        'birth_source':'https://www.astro.com/astro-databank/Diana,_Princess_of_Wales','limitation':'Selected 19:45 BST birth record; historical alternatives exist. This is a procedural comparison, not a prediction about accidents or health.'}
    Path('data/releasing-diana-reference.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
finally:e.kernel.close()
