"""Explainable views referencing canonical events; never a likelihood ranking."""
from collections import Counter

TIMING_SOURCE='https://theastrologypodcast.com/transcripts/tap-ep-365-transcript-transits-in-astrology-an-introduction-to-timing/'
PHASE_SOURCE='https://www.skyscript.co.uk/aspects2.html'

def present(report):
    events=report['exact_events']
    configurations=report['configurations']
    by_config={c['configuration_id']:[] for c in configurations}
    for e in events: by_config[e['configuration_id']].append(e)
    patterns=[]
    for cid,group in by_config.items():
        if len(group)>1:
            retrograde=any(e['retrograde'] for e in group)
            patterns.append({'configuration_id':cid,'event_ids':[e['id'] for e in group],
                'kind':'retrograde repetition' if retrograde else 'recurring contact',
                'explanation':'The same directed aspect recurs in this window; passes outside it are not counted.',
                'source':TIMING_SOURCE,'locator':'Retrogrades, stations and extended transit sequences'})
    themes={}
    for e in events:
        house=report['natal_summary']['planets'].get(e['natal_target'],{}).get('house')
        key=f'Natal house {house}' if house else 'Natal angles'
        themes.setdefault(key,[]).append(e['id'])
    coverage=Counter(e['interpretations'].get('coverage','unsupported') if isinstance(e['interpretations'],dict)
                     else 'unsupported' for e in events)
    ongoing=sorted([c for c in configurations if c['hours_in_window']>=24],key=lambda c:(-c['hours_in_window'],c['configuration_id']))
    short=[c['configuration_id'] for c in configurations if 0<c['hours_in_window']<24]
    approaching=[c['configuration_id'] for c in report['active_at_start'] if c['phase']=='applying']
    report['presentation']={
        'overview':{'exact_contacts':len(events),'active_at_start':len(report['active_at_start']),
                    'configurations':len(configurations),'repeated_patterns':len(patterns),'interpretation_coverage':dict(coverage)},
        'duration_convention':'Brief means less than 24 calculated hours within the selected orb and window; multi-day means at least 24. These are display bins, not significance judgments.',
        'major_ongoing_configurations':[{'configuration_id':c['configuration_id'],'hours_in_window':c['hours_in_window'],
                  'intervals':c['intervals'],'event_ids':[e['id'] for e in by_config[c['configuration_id']]]} for c in ongoing],
        'short_lived_configurations':short,'active_configuration_ids':[c['configuration_id'] for c in report['active_at_start']],
        'approaching_at_start':approaching,'upcoming_event_ids':[e['id'] for e in events],
        'repeated_patterns':patterns,'themes':[{'title':k,'event_ids':v,'basis':'Shared calculated natal house of target; no merged life-event prediction.'} for k,v in themes.items()],
        'phase_context':{'meaning':'Applying approaches exactness; separating recedes. A station can interrupt application.',
                         'source':PHASE_SOURCE,'locator':'Applying & Separating Aspects'},
        'grouping_source':{'url':TIMING_SOURCE,'locator':'Discussion of duration, retrograde repetitions and stations',
            'principle':'A transit can describe a sequence across a period, not only a single instant. Duration here is computed from the chosen orb.'}}
    return report

def markdown(report):
    p=report['presentation']; natal=report['natal_summary']; birth=natal['birth']; events=report['exact_events']
    name=lambda e:f"{e['transiting']} {e['aspect_degrees']}° natal {e['natal_target']}"
    lines=['# Example Western Astrology forecast','',
        f"Birth: {birth['local']} in {birth['zone']}, latitude {birth['latitude']}, longitude {birth['longitude']}.",
        f"Period: {report['window']['start_utc']} to {report['window']['end_utc']} (end excluded).",'',
        f"{len(events)} exact contacts; {p['overview']['active_at_start']} configurations active at the start; {len(p['repeated_patterns'])} recurring patterns.",
        f"Interpretation coverage: {p['overview']['interpretation_coverage']}.",'',
        '## Birth-chart context','',
        ', '.join(f"{k}: {v['sign']} {v['degree_in_sign']:.2f}°, house {v['house']}" for k,v in natal['planets'].items())+'.','',
        '## Ongoing configurations','',p['duration_convention'],'']
    configs={c['configuration_id']:c for c in report['configurations']}
    for c in p['major_ongoing_configurations']:
        obj=configs[c['configuration_id']]
        clipped=any(s['start_clipped'] or s['end_clipped'] for s in c['intervals'])
        lines.append(f"- {name(obj)}: {c['hours_in_window']:.1f} hours in this window"+(' (clipped; full duration unknown).' if clipped else '.'))
    lines+=['','## Repeated patterns','']
    for group in p['repeated_patterns']:
        lines.append(f"- {group['configuration_id']}: {group['kind']}; {', '.join(group['event_ids'])}.")
    lines+=['','## Active and approaching at the start','',
            'Approaching: '+(', '.join(p['approaching_at_start']) or 'none')+'.',
            'All active: '+(', '.join(p['active_configuration_ids']) or 'none')+'.','',
            f"[Timing context]({TIMING_SOURCE}): retrograde motion can extend a sequence and repeat contacts. Pass counts apply only to this window.",
            f"[Phase context]({PHASE_SOURCE}): applying approaches exactness; separating recedes. A station can interrupt application."]
    lines+=['','## Chronological events and interpretations','']
    lines+=['Interpretation IDs below resolve to the source-specific notes following the table. Components are explicitly compositional.','',
            '| Contact | Exact UTC | Transit | Motion / pass | Coverage | Interpretation IDs |',
            '|---|---|---|---|---|---|']
    notes={}
    for e in events:
        interp=e['interpretations']
        refs=[]
        for kind in ('direct','components'):
            for r in interp.get(kind,[]):
                notes[r['rule_id']]=(kind,r)
                refs.append(r['rule_id'])
        lines.append(f"| {e['id']} | {e['exact_utc']} | {name(e)} | {'R' if e['retrograde'] else 'D'} / {e['pass_in_window']} of {e['passes_in_window']} | {interp['coverage']} | {', '.join(refs)} |")
    lines+=['','## Source-grounded interpretation notes','',
            'These are symbolic readings. Direct records retain source scope; components do not establish a documented planet-pair interpretation.','']
    for rid,(kind,r) in notes.items():
        lines.append(f"- **{rid}** ({kind}): {r['text']} [{r['author']}]({r['source']}) — {r['locator']}.")
        if 'documentation_scope' in r: lines.append('  - Documentation: '+r['documentation_scope'])
        for exception in r['exceptions']: lines.append('  - Scope: '+exception)
    lines+=['','## Ongoing-configuration interpretations','']
    seen=set()
    for c in report['configurations']:
        direct=c['interpretations'].get('direct',[]) if isinstance(c['interpretations'],dict) else []
        for r in direct:
            if r['rule_id'] in seen:continue
            seen.add(r['rule_id'])
            lines.append(f"- {c['configuration_id']}: {r['text']} [{r['author']}]({r['source']}) — {r['locator']}. Documentation: {r['documentation_scope']}.")
            for exception in r['exceptions']: lines.append('  - Scope: '+exception)
    lines+=['','## Coverage gaps','',
            'Contacts labeled compositional have no direct rule for the selected tradition and conditions. Unsupported contacts have neither a matching direct rule nor documented components. Traditional and Hellenistic pair coverage, and condition-specific house/dignity delineations, remain incomplete.','']
    lines+=['## Calculation provenance and limitations','',report['predictive_validity'],'',
            f"Kernel SHA-256: `{report['reproducibility']['kernel_sha256']}`. Skyfield {report['reproducibility']['skyfield']}.",
            report['precision']['note'],'']
    lines.extend('- '+l for l in report['limitations'])
    lines+=['','Full inputs, intervals, event data, grouping membership and interpretations are in the accompanying JSON.','']
    return '\n'.join(lines)
