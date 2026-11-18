"""Bind completed test receipts to this slice's source/build and asset hashes."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FATE = ROOT / 'fate'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def main():
    units = {}
    for name, filename, count in [('native', 'fate-inherited-unit.log', 2522), ('workbench', 'fate-workbench-unit.log', 77), ('fate', 'fate-api-tests.log', 13)]:
        log = (ROOT / 'tmp' / filename).read_text(encoding='utf-8-sig')
        assert re.search(r'Ran ' + str(count) + r' tests', log) and re.search(r'\nOK\s', log + '\n'), filename
        units[name] = dict(tests=count, passed=True, output=log)
    browser = load('fate/browser-acceptance.json')['stats']
    workbench = load('fate/workbench-browser-acceptance.json')['stats']
    for stats in [browser, workbench]:
        assert stats['expected'] == 9 and stats['unexpected'] == stats['skipped'] == stats['flaky'] == 0
    inherited = load('fate/inherited-cli-acceptance.json')
    assert inherited['complete'] and inherited['passed'] and inherited['cli_cases'] == 3515 and inherited['independent_verifiers'] == 52
    audit = load('tmp/fate-npm-audit.json')
    assert audit['metadata']['vulnerabilities']['total'] == 0
    live = load('fate/live-gemini-acceptance.json')
    assert live['passed']
    commands = [[sys.executable, '-m', 'pip', 'check'], [sys.executable, '-m', 'scripts.audit_dependencies'],
                [sys.executable, '-m', 'scripts.check_inventory_workbook'], ['git', '-c', 'core.safecrlf=false', 'diff', '--check'],
                ['git', '-c', 'core.safecrlf=false', 'diff', '--cached', '--check'],
                ['git', 'diff', '--exit-code', '--', 'future', 'knowledge', 'resources', 'tests', 'workbench'],
                ['git', 'diff', '--cached', '--exit-code', '--', 'future', 'knowledge', 'resources', 'tests', 'workbench']]
    gates = []
    for command in commands:
        cp = subprocess.run(command, cwd=ROOT, capture_output=True)
        assert cp.returncode == 0, cp.stdout.decode(errors='replace') + cp.stderr.decode(errors='replace')
        gates.append(dict(command=command, returncode=cp.returncode, stdout=cp.stdout.decode(errors='replace')))
    archive = Path.home() / 'Downloads/FATE-asset-pack-01.zip'
    pack_hash = sha(archive) if archive.exists() else load('fate/assets.json')['pack']['sha256']
    assets = dict(pack=dict(name='FATE-asset-pack-01.zip', sha256=pack_hash, provenance='Project owner supplied; original artwork/audio declaration retained in pack README'),
                  files={p.relative_to(FATE).as_posix(): sha(p) for p in sorted((FATE/'web/public').rglob('*')) if p.is_file()})
    (FATE/'assets.json').write_text(json.dumps(assets, indent=2)+'\n', encoding='utf-8')
    source_paths = list(FATE.glob('*.py')) + list((FATE/'tests').glob('*.py')) + list((FATE/'web/src').glob('*')) + list((FATE/'web/e2e').glob('*.ts'))
    source_paths += [FATE / p for p in ['web/package.json', 'web/package-lock.json', 'web/vite.config.ts', 'web/tsconfig.json', 'web/playwright.config.ts', 'experience.json', 'requirements.txt']]
    source_hashes = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(source_paths) if p.is_file()}
    receipt = dict(schema_version=1, date='2026-11-19', block='01 · The Living Oracle',
                   status='Implemented and verified consumer vertical slice; physical-device/public-deployment acceptance remains P1',
                   units=units, fate_browser=browser, workbench_browser=workbench,
                   cli_cases=3515, independent_verifiers=52, protected_source_files=inherited['protected_count'], changed_protected_source_files=[],
                   npm_vulnerabilities=0, live_gemini='One synthetic developer question; references/shape verified, not semantic or predictive validation',
                   gates=gates, performance=load('fate/performance.json'),
                   source_sha256=source_hashes,
                   built_files_sha256={p.relative_to(FATE/'web/dist').as_posix(): sha(p) for p in sorted((FATE/'web/dist').rglob('*')) if p.is_file()},
                   screenshot_sha256={p.name: sha(p) for p in sorted((FATE/'screenshots').glob('*.png'))},
                   acceptance_criteria=['Native result equals replay through unchanged future.tarot.read', 'One/three cards, reversals and source references preserved', 'Progressive reveal and skip path; duplicates blocked and retry seed retained', 'No automatic cloud transmission or persistence', 'Pixi renders without console errors, animates, and stops on pause/reduced motion', 'Complete journey and export in mobile browser; accessibility scans and keyboard dialog pass', 'Small/tablet/desktop and doubled-text control geometry checks pass', 'No-WebGL fallback completes a native reading', 'Existing native/Workbench tests, full CLI/verifier gates, production builds and inventory/dependency gates pass'],
                   limitations=['Local Chromium mobile emulation only; no physical iOS/Android, field CWV or actual INP certification', 'No public deployment, distributed limiter, accounts or persistence', 'Original celestial deck and supplied starter art/audio; no historical illustrated deck claim', 'Gemini semantic faithfulness is not guaranteed', 'Software acceptance is not empirical prediction validation'])
    (FATE/'acceptance.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print('Recorded: 2522 native + 77 Workbench + 13 FATE tests; 9 + 9 browser groups; 3515 CLI cases; 52 independent verifiers; zero changed protected sources.')


if __name__ == '__main__':
    main()
