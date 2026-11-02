"""Readable examples derived from the saved executable JSON outputs."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'data'
charts=json.loads((root/'house-comparison-1990.json').read_text())
lines=['# July 15, 1990 — house-system comparison','',
       'Birth: 14:30 Asia/Kolkata, Delhi (28.6139 N, 77.209 E). All cusp values are tropical ecliptic longitude in degrees.','',
       '| House | '+' | '.join(charts)+' |','|---|'+'---|'*len(charts)]
for i in range(12):lines.append(f'| {i+1} | '+' | '.join(f"{c['house_cusps'][i]:.6f}" for c in charts.values())+' |')
lines+=['','Planet assignments use [cusp, next cusp) longitude sectors. No system is silently substituted.','',
        '| Planet | '+' | '.join(charts)+' |','|---|'+'---|'*len(charts)]
for name in next(iter(charts.values()))['planets']:
    lines.append('| '+name+' | '+' | '.join(str(c['planets'][name]['house']) for c in charts.values())+' |')
(root/'house-comparison-1990.md').write_text('\n'.join(lines)+'\n')
r=json.loads((root/'progressed-1990-2026.json').read_text())
lines=['# July 1990 example — secondary progressions','',f"Target: {r['target_utc']}.",
       f"Symbolic age: {r['symbolic_age_years']:.9f} years. Progressed epoch: TT JD {r['progressed_epoch']['jd_tt']:.9f}.",
       f"Year key: {r['conventions']['year_key']} ({r['conventions']['year_days']} days). Angle convention: {r['conventions']['angle_method']}. Houses: {r['conventions']['houses']}.",'',
       r['conventions']['distinction'],'',
       '| Planet | Longitude | Sign | Retrograde | Natal house | Progressed house |',
       '|---|---|---|---|---|---|']
for name,p in r['planets'].items():lines.append(f"| {name} | {p['longitude']:.6f} | {p['sign']} {p['degree_in_sign']:.4f}° | {p['retrograde']} | {p['natal_house']} | {p['progressed_house']} |")
for key,title in [('progressed_to_natal_aspects','Progressed to natal'),('progressed_to_progressed_aspects','Mutual progressed aspects')]:
    lines+=['','## '+title,'','| Progressed | Target | Aspect | Orb | Phase |','|---|---|---|---|---|']
    for a in r[key]:lines.append(f"| {a['progressed']} | {a['target']} | {a['aspect']}° | {a['orb']:.6f}° | {a['phase']} |")
lines+=['','## Moon and upcoming changes','',f"Progressed Moon elongation: {r['moon_cycle']['elongation']:.6f}°, sector: {r['moon_cycle']['phase_sector']}."]
for key in ('sign_changes','progressed_moon_contacts','progressed_lunation_boundaries'):
    lines+=['',key+':']
    lines.extend('- '+json.dumps(e) for e in r['upcoming'][key])
    if not r['upcoming'][key]:lines.append('- None in the selected window.')
lines+=['','## Source-grounded context','']
for i in r['interpretations']:lines.append(f"- {i['statement']} Coverage: {i['coverage']}. [Source]({i['source']}) — {i['locator']}.")
lines+=['','## Limits','']+['- '+l for l in r['limitations']]
(root/'progressed-1990-2026.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
