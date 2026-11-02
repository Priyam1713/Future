"""Independent minute-grid verification with Swiss/Moshier, no Future imports."""
from datetime import datetime,timezone,timedelta
from pathlib import Path
import json
import swisseph as s
start=datetime(2026,11,1,tzinfo=timezone.utc)
base=s.julday(2026,11,1,0)
# Swiss body indexes; traditional domicile mapping from the historical table.
rulers=[4,3,2,1,0,2,3,4,5,6,6,5]
fixed={1,4,7,10};runs=[];begin=None
for minute in range(2880):
    jd=base+(minute+.5)/1440
    positions=[s.calc_ut(jd,i,s.FLG_MOSEPH|s.FLG_SPEED)[0] for i in range(7)]
    cusps,axes=s.houses(jd,28.6139,77.209,b'R')
    asc=int(axes[0]//30);mc=int(axes[1]//30);second=int(cusps[1]//30)
    asc_lord=rulers[asc];second_lord=rulers[second]
    ok=(asc in fixed and mc in fixed and int(positions[asc_lord][0]//30) in fixed
        and int(positions[1][0]//30) in fixed and int(positions[second_lord][0]//30) in fixed
        and positions[asc_lord][3]>=0)
    if ok and begin is None:begin=minute
    if not ok and begin is not None:runs.append([begin,minute]);begin=None
if begin is not None:runs.append([begin,2880])
Path('tests/fixtures/election_reference.json').write_text(json.dumps({'oracle':'Swiss Ephemeris 2.10.3.2/Moshier, Regiomontanus; UTC approximates UT1',
 'source':'Ramesey Astrologia Restaurata Liber III second-house chapter II p.135; introduction p.124',
 'start_utc':start.isoformat(),'end_exclusive_utc':(start+timedelta(days=2)).isoformat(),
 'latitude':28.6139,'longitude':77.209,'sample_offset_seconds':30,'sample_step_seconds':60,
 'minute_samples':2880,'true_index_runs':runs},indent=2))
