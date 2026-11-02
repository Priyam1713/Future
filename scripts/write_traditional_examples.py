"""Readable calculated examples, preserving complete JSON alongside them."""
from pathlib import Path
from datetime import datetime,timezone
import json
from future.profections import annual
root=Path(__file__).resolve().parents[1]/'data'
r=json.loads((root/'hellenistic-1990.json').read_text())
c=r['conditions']; n=r['natal']
lines=['# July 1990 — Hellenistic planetary conditions','',
 'Birth: July 15, 1990, 14:30 Asia/Kolkata, Delhi (28.6139 N, 77.209 E).',
 f"Sect: {c['sect']['type']}; unrefracted solar-center altitude {c['sect']['sun_center_altitude_degrees']:.6f} degrees.",
 'Tables: Egyptian bounds, Dorothean triplicities, Chaldean ten-degree faces, sect-reversing Lots.','',
 '| Planet | Sign | Sect affiliation | Of chart sect | Own primary dignities | Debilities | Solar condition |',
 '|---|---|---|---|---|---|---|']
for name,p in c['planets'].items():
    lines.append(f"| {name} | {p['sign']} | {p['sect_affiliation']} | {p['of_chart_sect']} | {', '.join(p['own_dignities']) or 'none'} | {', '.join(p['debilities']) or 'none'} | {p['solar']['state'] if p['solar'] else 'Sun'} |")
lines+=['','## Dignity owners','',
 '| Placement | Domicile | Exaltation | Primary triplicity | Participating | Bound | Face |',
 '|---|---|---|---|---|---|---|']
for name,p in c['planets'].items():
    d=p['rulers'];lines.append('| '+name+' | '+' | '.join(str(d[k]) for k in ('domicile','exaltation','triplicity','participating','bound','face'))+' |')
lines+=['','## Fortune and Spirit','']
for name,p in c['lots'].items():lines.append(f"- {name}: {p['degree_in_sign']:.6f}° {p['sign']}; house {p['house']}; sign ruler {p['sign_ruler']}.")
lines+=['','## Domicile dispositorship','']
for edge in c['receptions']:lines.append(f"- {edge['host']} hosts {edge['guest']} by {', '.join(edge['dignities'])}; reciprocal: {edge['mutual']}.")
lines+=['','## Sources and scope','']
for rule in c['provenance']['rules']:lines.append(f"- {rule['id']}: [{rule['author']}]({rule['source']}), {rule['edition']}, {rule['locator']}.")
lines+=['']+['- '+l for l in c['limitations']]
lines+=['','The separately saved traditional example uses Lilly-Ptolemaic bounds, Lilly triplicities, CA113 combustion/cazimi and fixed-day Fortune. These profiles are not interchangeable.','']
(root/'hellenistic-1990.md').write_text('\n'.join(lines),encoding='utf-8')
r=json.loads((root/'profections-1990-2026.json').read_text());a=r['annual_profection']
lines=['# July 1990 — annual profections','',f"Target: {a['target_utc']}.",
 f"Age {a['completed_age']}: whole-sign house {a['activated_house']}, {a['activated_sign']}, lord of the year **{a['lord_of_year']}**.",
 f"Period: {a['period']['start_inclusive_utc']} to {a['period']['end_exclusive_utc']} (end excluded).",'',
 'Boundary: birth wall-clock time in Asia/Kolkata; this is a civil anniversary, not a calculated solar return.',
 'Annual activation follows whole signs even when the natal chart uses quadrant cusps.','',
 '## Lord-of-year context','']
p=a['lord_natal_context'];condition=p['conditions']
lines+=[f"Mars is natally in {p['sign']}, whole-sign house {p['whole_sign_natal_house']}.",
 f"Sect affiliation: {condition['sect_affiliation']}; of chart sect: {condition['of_chart_sect']}. Debilities: {', '.join(condition['debilities']) or 'none'}.",
 'These are traditional symbolic conditions, not strength scores or probabilities of adverse events.','',
 '## Adjacent years','', '| Age | House | Sign | Lord | Starts UTC |','|---|---|---|---|---|']
timeline=[]
for year in range(2025,2039):
    t=datetime(year,7,15,9,tzinfo=timezone.utc);v=annual(r['natal'],t)
    entry={k:v[k] for k in ('completed_age','activated_house','activated_sign','lord_of_year','period')};timeline.append(entry)
    lines.append(f"| {v['completed_age']} | {v['activated_house']} | {v['activated_sign']} | {v['lord_of_year']} | {v['period']['start_inclusive_utc']} |")
lines+=['','## Interpretation and sources','',a['interpretation']['statement'],
 'Activated-house topic component: '+a['interpretation']['theme']+'.',
 f"[Method and source examples]({a['interpretation']['source']}) — {a['interpretation']['locator']}.",
 f"[House-topic source]({a['interpretation']['topic_source']}).",'',
 'Coverage is compositional. The time-lord context is kept separate from transit calculations and does not assign outcome likelihood.','']
(root/'profections-1990-2026.md').write_text('\n'.join(lines),encoding='utf-8')
(root/'profections-1990-timeline.json').write_text(json.dumps(timeline,indent=2)+'\n')
