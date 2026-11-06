"""CLI lifecycle and byte-exact accepted/rejected JSON/Markdown private replay."""
import copy
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from future import deja_reve as d
from scripts.verify_deja_reve import F, analysis, seal, sha
from tests.test_deja_reve import invalid_records, invalid_analyses, req

ROOT = Path(__file__).resolve().parents[1]


def examples():
    good = {'reference': req('reference')}
    for c in F['source_cases']: good[c['id']] = req('reference', case_id=c['id'])
    for name, changes in [
        ('specific-prior-dream', {}),
        ('general-dream-familiarity', dict(specific_recollection=False, temporal_context='vague', proposal='familiarity-like')),
        ('present-dreamy-state', dict(specific_recollection=False, temporal_context='none', familiarity=False, present_dreamy_state=True, proposal='dreamy-state')),
        ('generic-deja-vu', dict(dream_association=False, specific_recollection=False, temporal_context='none', proposal=None)),
        ('mixed-uncertain', dict(present_dreamy_state=True, uncertain=True)),
        ('missing-attributes', dict(dream_association=None, specific_recollection=None, temporal_context='unknown')),
        ('high-confidence-undocumented', dict(subjective_confidence='Certain,without independent original record')),
        ('vague-temporal-context', dict(temporal_context='vague'))]:
        r = copy.deepcopy(F['observation']); r['original']['attributes'].update(changes); seal(r)
        good[name] = req('annotate', record=r)
    good['record'] = req('record', record=F['dream'])
    good['amend'] = req('amend', record=F['dream'], amendment=F['amendment'])
    good['freeze-candidates'] = req('freeze-candidates', manifest=F['analysis']['manifest'])
    good['link-dream'] = req('link-dream', analysis=analysis(comparisons=[]), comparison=F['analysis']['comparisons'][0])
    good['earlier-original'] = req('report', analysis=F['analysis'])
    good['no-original'] = req('report', analysis=analysis(dreams=[], comparisons=[]))
    for name, key, value in [
        ('equal-lock', 'lock_at', '2026-11-04T10:00:00Z'),
        ('later-lock', 'lock_at', '2026-11-05T00:00:00Z'),
        ('missing-lock', 'lock_at', None), ('missing-first-record', 'first_record_at', None),
        ('missing-dream-occurrence', 'occurrence', None),
        ('conflicting-chronology', 'lock_at', '2026-10-31T00:00:00Z')]:
        r = copy.deepcopy(F['dream']); r['original'][key] = value; seal(r)
        good[name] = req('compare', analysis=analysis(r))
    a = analysis(); a['observation']['original']['occurrence'] = dict(start='2026-11-01T07:00:00Z', end='2026-11-01T09:00:00Z'); seal(a['observation'])
    good['overlapping-experience'] = req('compare', analysis=a)
    a = analysis(); a['observation']['original']['occurrence'] = None; seal(a['observation'])
    good['unknown-experience'] = req('compare', analysis=a)
    a = analysis(); a['observation']['original']['occurrence'] = dict(start='2026-10-31T08:00:00Z', end='2026-10-31T08:00:00Z'); seal(a['observation'])
    good['experience-before-event'] = req('compare', analysis=a)
    a = analysis(); a['event'] = None
    good['no-external-event'] = req('compare', analysis=a)
    a = analysis(); a['dreams'][0]['amendments'].append(copy.deepcopy(F['amendment']))
    a['comparisons'][0].update(version_sha256=sha(F['amendment']), at='2026-11-06T00:00:00Z')
    good['post-event-amendment'] = req('report', analysis=a)
    a = analysis(); a['comparisons'][0]['status'] = 'nonmatch'
    good['manual-nonmatch'] = req('report', analysis=a)
    a = analysis()
    for i, status in enumerate(['nonmatch', 'unscorable', 'unreviewed', 'excluded', 'nonmatch'], 2):
        r = copy.deepcopy(F['dream']); r['original']['id'] = 'dream'+str(i); seal(r); a['dreams'].append(r)
        a['manifest']['payload']['candidates'].append(dict(dream_id='dream'+str(i), original_sha256=r['original_sha256'], disposition='excluded' if status == 'excluded' else 'included', reason='Frozen synthetic candidate'))
        if status in ('nonmatch', 'unscorable'):
            c = copy.deepcopy(a['comparisons'][0]); c.update(dream_id='dream'+str(i), version_sha256=r['original_sha256'], status=status); a['comparisons'].append(c)
    a['comparisons'][0]['status'] = 'match'; a['manifest']['sha256'] = sha(a['manifest']['payload'])
    good['multiple-candidates'] = req('report', analysis=copy.deepcopy(a))
    a['post_hoc'] = [{k: copy.deepcopy(F['analysis'][k]) for k in ('manifest', 'dreams', 'comparisons')}]
    a['post_hoc'][0]['manifest']['payload']['frozen_at'] = '2026-11-04T11:45:00Z'
    a['post_hoc'][0]['manifest']['sha256'] = sha(a['post_hoc'][0]['manifest']['payload'])
    good['post-hoc-search'] = req('report', analysis=a)
    r = copy.deepcopy(F['observation']); r['original']['narrative'] += '\n`````json\n<html>raw</html>'; seal(r)
    good['unicode-whitespace'] = req('annotate', record=r)
    bad = {name: req('record', record=r) for name, r in invalid_records().items()}
    bad.update({name: req('report', analysis=a) for name, a in invalid_analyses().items()})
    for task in ('diagnose', 'predict', 'verify-memory', 'export'): bad['unsupported-'+task] = req(task)
    bad['unknown-case'] = req('reference', case_id='not-a-case')
    bad['schema'] = req('reference', unknown=True)
    return good, bad


def run(write=False):
    good, bad = examples(); cases = []
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp, 'request.json')
        for rejected, examples_ in [(False, good), (True, bad)]:
            for name, q in examples_.items():
                raw = json.dumps(q, ensure_ascii=False, indent=2)+'\n'
                p = ROOT/f'data/deja-reve-{name}-input.json'
                if write: p.write_text(raw, encoding='utf-8')
                else: assert p.read_text(encoding='utf-8') == raw
                path.write_text(raw, encoding='utf-8'); values = []
                for fmt in ('json', 'markdown'):
                    cmd = [sys.executable, '-m', 'future', 'deja-reve', str(path), '--format', fmt]
                    cp = subprocess.run(cmd, cwd=ROOT, capture_output=True)
                    assert cp.returncode == (2 if rejected else 0), (name, cp.stderr.decode(errors='replace'))
                    rawout = cp.stdout.decode('utf-8').replace('\r\n', '\n').rstrip('\n')+'\n'
                    value = json.loads(rawout) if fmt == 'json' else json.loads(re.search(r'(`{3,})json\n(.*?)\n\1', rawout, re.S)[2])
                    values.append(value)
                    p = ROOT/f'data/deja-reve-{name}.{ "json" if fmt == "json" else "md"}'
                    if write: p.write_text(rawout, encoding='utf-8')
                    else: assert p.read_text(encoding='utf-8') == rawout, ('replay', name, fmt)
                    cases.append(dict(name=name, format=fmt, rejected=rejected, passed=True))
                assert values[0] == values[1]
        for raw in ('{"schema_version":1,"task":"reference","task":"reference"}', '{"schema_version":1,"task":"reference","x":NaN}'):
            path.write_text(raw, encoding='utf-8')
            for fmt in ('json', 'markdown'):
                cp = subprocess.run([sys.executable, '-m', 'future', 'deja-reve', str(path), '--format', fmt], cwd=ROOT, capture_output=True)
                assert cp.returncode == 2
                cases.append(dict(name='strict-json', format=fmt, rejected=True, passed=True))
    out = dict(passed=True, cases=cases, count=len(cases), accepted_pairs=len(good), rejected_pairs=len(bad), exact_replay=True)
    if write: (ROOT/'data/deja-reve-cli-smoke.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    return out


if __name__ == '__main__':
    result = run('--write' in sys.argv)
    print(f"{result['count']} Deja Reve CLI cases passed;{result['accepted_pairs']}accepted/{result['rejected_pairs']}rejected JSON/Markdown pairs replayed")
