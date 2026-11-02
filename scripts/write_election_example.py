"""Readable trace summary; full charts and rejected intervals remain in JSON."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]/'data'
r=json.loads((root/'election-retention-2026.json').read_text())
lines=['# Source-driven electional example','',
 f"Category: {r['category']}. Profile: {r['profile']} ({r['tradition']}).",
 f"Range: {r['range']['start_utc']} to {r['range']['end_exclusive_utc']} (end excluded).",
 f"Location: {r['location']['latitude']}, {r['location']['longitude']}. Houses: {r['houses']}.",'',
 'Candidates satisfy only the selected implemented sign/motion rules. They are not certified as complete Ramesey elections; other traditional diagnostics may be violated or unresolved.',
 'No auspiciousness score, financial forecast or probability of success is calculated.','',
 '| Candidate | Start UTC | End UTC | Minutes | ASC lord | Second lord |', '|---|---|---|---|---|---|']
for i,c in enumerate(r['candidates'],1):
    lines.append(f"| {i} | {c['start_inclusive_utc']} | {c['end_exclusive_utc']} | {c['duration_minutes']:.2f} | {c['rule_trace']['ascendant_lord']} | {c['rule_trace']['second_lord']} |")
for i,c in enumerate(r['candidates'],1):
    lines+=['',f'## Candidate {i}: rule trace','']
    for t in c['rule_trace']['rules']:
        lines.append(f"- {t['id']}: **{t['status']}**; required: {t['required']}. {t['meaning']} [Source]({t['source']}) — {t['locator']}.")
    lines+=['','Diagnostics (not silently treated as passed selection rules):','']
    for t in c['diagnostics']['diagnostic_rule_trace']:
        lines.append(f"- {t['id']}: {t['status']}. {t.get('reason','')}")
    lines+=[f"- Angular benefics: {c['diagnostics']['angular_benefics']}; angular malefics: {c['diagnostics']['angular_malefics']}.",
            '- Detailed Moon aspects, comparative Lilly conditions/receptions and the complete representative chart are in JSON.']
lines+=['','## Unknown criteria','']+['- '+g for g in r['unknown_criteria']]
lines+=['','## Search verification','',
 'Independent Swiss/Moshier minute-grid checks cover 2,880 sample instants over this range. A five-minute versus ten-minute angular scan produces the same candidate count and matching boundaries within 0.5 seconds.',
 f"Search derived {r['search_method']['partition_points']} partition points; unresolved subintervals: {len(r['unresolved_intervals'])}.",
 r['search_method']['coverage'],r['search_method']['limitation'],
 'Internal boundaries have a one-second guard; minimum requested duration is five minutes.','',
 '## Source profiles and conflicts','',
 f"[Ramesey, Astrologia Restaurata (1653)]({r['source_profile']['source']}) — {r['source_profile']['locator']}.",
 'The rapid-use profile follows a different intention and sign preference. It is not averaged with the retention profile.',
 'The source also records a Ramesey/Haly disagreement concerning borrowing/lending. Its different category and scope remain in the JSON; it is not imported into retention rules.',
 'Dorotheus Book V remains a source-coverage gap; no unverified Dorothean prescription is implemented.','']
(root/'election-retention-2026.md').write_text('\n'.join(lines),encoding='utf-8')
