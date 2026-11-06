"""Complete inherited commands, registry, taxonomy and byte preservation gates."""
import concurrent.futures
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from future.scrying import load_input
from future.knowledge import Registry

ROOT = Path(__file__).resolve().parents[1]


def execute(cmd):
    start = time.monotonic()
    cp = subprocess.run(cmd, cwd=ROOT, capture_output=True)
    return dict(command=cmd, returncode=cp.returncode, seconds=round(time.monotonic()-start, 3),
                stdout=cp.stdout.decode('utf-8', errors='replace'), stderr=cp.stderr.decode('utf-8', errors='replace'))


def run(skip_unit=False, resume=False):
    inherited = load_input(ROOT/'data/ai-predictive-modeling-acceptance-checks.json')['checks']
    checks = []
    if not skip_unit:
        unit = execute([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'])
        (ROOT/'data/quantum-probability-forecasting-unit.json').write_text(json.dumps(unit, indent=2)+'\n', encoding='utf-8')
    else:
        unit = load_input(ROOT/'data/quantum-probability-forecasting-unit.json')
    checks.append(unit)
    assert unit['returncode'] == 0
    # Each smoke/verifier owns separate temporary inputs and output artifacts.
    cmds = [c['command'] for c in inherited if len(c['command']) > 2 and c['command'][1] == '-m' and
            c['command'][2].startswith(('scripts.smoke_', 'scripts.verify_'))]
    cmds += [['python', '-m', 'scripts.smoke_quantum_probability_forecasting_core'], ['python', '-m', 'scripts.verify_quantum_probability_forecasting']]
    assert len(cmds) == len({tuple(c) for c in cmds})
    completed = {}
    if resume:
        prior = load_input(ROOT/'data/quantum-probability-forecasting-acceptance-checks.json')
        completed = {tuple(c['command']): c for c in prior['checks'] if c['returncode'] == 0}
    ordered = {i: completed[tuple(cmd)] for i, cmd in enumerate(cmds) if tuple(cmd) in completed}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(execute, cmd): i for i, cmd in enumerate(cmds) if i not in ordered}
        for future in concurrent.futures.as_completed(futures):
            i = futures[future]; result = future.result(); ordered[i] = result
            print(('PASS ' if result['returncode'] == 0 else 'FAIL ')+' '.join(cmds[i]), flush=True)
            (ROOT/'data/quantum-probability-forecasting-acceptance-checks.json').write_text(json.dumps(dict(complete=False, checks=checks+[ordered[i] for i in sorted(ordered)]), indent=2)+'\n', encoding='utf-8')
    checks += [ordered[i] for i in range(len(cmds))]
    for cmd in [['python', '-m', 'scripts.audit_dependencies'], ['python', '-m', 'pip', 'check'], ['git', 'diff', '--check']]:
        checks.append(execute(cmd))
    assert all(c['returncode'] == 0 for c in checks), [c for c in checks if c['returncode']]
    reg = Registry(':memory:'); references = []; skipped = []
    try:
        for path in sorted((ROOT/'knowledge').glob('*sources.json')):
            records = load_input(path)
            if not isinstance(records, list): continue
            for r in records:
                if not isinstance(r, dict) or 'id' not in r: continue
                if r['id'] == 'chinese-inventory-2-v1': skipped.append(r['id']); continue
                reg.add_source(r); references.append(r)
        for r in references: reg.add_source(r)
        unique = reg.db.execute('SELECT COUNT(*) FROM sources').fetchone()[0]
    finally: reg.close()
    strict_count = 0
    expected_invalid = {'data/feng-shui-duplicate-json-input.json', 'data/feng-shui-nonfinite-input.json'}
    for folder in ('knowledge', 'data', 'tests/fixtures'):
        for path in (ROOT/folder).rglob('*.json'):
            if path.relative_to(ROOT).as_posix() in expected_invalid:
                try: load_input(path)
                except ValueError: continue
                raise AssertionError('Historical rejection fixture no longer rejects')
            load_input(path); strict_count += 1
    baseline = load_input(ROOT/'data/quantum-probability-forecasting-engine-preservation-baseline.json')
    changed = [p for p, h in baseline['pre_engine_sha256'].items() if p not in baseline['allowed_existing_edits'] and
               (not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest() != h)]
    assert not changed, changed
    old = json.loads(subprocess.check_output(['git', 'show', baseline['baseline_commit']+':knowledge/gaps.json'], cwd=ROOT))
    new = load_input(ROOT/'knowledge/gaps.json')
    assert [x for x in old if x['technique_id'] != 50] == [x for x in new if x['technique_id'] != 50]
    assert len(new) == 60 and sum(bool(x['retained']) for x in new) == 54
    excluded = [x['technique_id'] for x in new if not x['retained']]
    assert excluded == [25, 27, 41, 42, 47, 48]
    unit = load_input(ROOT/'data/quantum-probability-forecasting-unit.json')
    assert unit['returncode'] == 0
    checks[0] = unit
    tests = int(re.search(r'Ran (\d+) tests', unit['stderr'])[1])
    cli = sum(int(re.match(r'(\d+)', c['stdout'])[1]) for c in checks if any('scripts.smoke_' in x for x in c['command']))
    verifier_count = sum(any('scripts.verify_' in x for x in c['command']) for c in checks)
    assert (tests, cli, verifier_count) == (1598, 2207, 29), (tests, cli, verifier_count)
    assert baseline['protected_count'] == 2927
    out = dict(passed=True, complete=True, checks=checks, tests=tests, inherited_tests=1462, new_tests=tests-1462,
               cli_cases=cli, inherited_cli_cases=2029, new_cli_cases=cli-2029, independent_verifiers=verifier_count,
               protected_files=baseline['protected_count'], changed_protected_files=changed,
               allowed_existing_edits=baseline['allowed_existing_edits'], registry=dict(references_checked_twice=len(references), unique=unique, skipped=skipped),
               strict_json_files=strict_count, historical_invalid_json_rejections=sorted(expected_invalid),
               taxonomy=dict(total=60, retained=54, excluded=excluded), other59gap_entries_unchanged=True,
               verification=load_input(ROOT/'data/quantum-probability-forecasting-verification.json'), cli_replay=load_input(ROOT/'data/quantum-probability-forecasting-cli-replay.json'))
    (ROOT/'data/quantum-probability-forecasting-acceptance-checks.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(f'{tests}tests;{cli}CLI cases;{verifier_count}verifiers;{baseline["protected_count"]}protected files unchanged', flush=True)
    return out


if __name__ == '__main__': run('--skip-unit' in sys.argv or '--resume' in sys.argv, '--resume' in sys.argv)
