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
    for name, filename, count in [('native', 'fate-inherited-unit.log', 2522), ('workbench', 'fate-workbench-unit.log', 77), ('fate', 'fate-api-tests.log', 21)]:
        log = (ROOT / 'tmp' / filename).read_text(encoding='utf-8-sig')
        assert re.search(r'Ran ' + str(count) + r' tests', log) and re.search(r'\nOK\s', log + '\n'), filename
        units[name] = dict(tests=count, passed=True, output=log)
    browser = load('fate/browser-acceptance.json')['stats']
    workbench = load('fate/workbench-browser-acceptance.json')['stats']
    for stats, expected in [(browser,18),(workbench,9)]:
        assert stats['expected'] == expected and stats['unexpected'] == stats['skipped'] == stats['flaky'] == 0
    inherited = load('fate/inherited-cli-acceptance.json')
    assert inherited['complete'] and inherited['passed'] and inherited['cli_cases'] == 3515 and inherited['independent_verifiers'] == 52
    audit = load('tmp/fate-npm-audit.json')
    assert audit['metadata']['vulnerabilities']['total'] == 0
    live = load('fate/live-gemini-acceptance.json')
    assert live['passed']
    number_evidence = load('fate/evidence/numerology-engine.json')
    number_recording = load('fate/evidence/numerology-recording.json')
    from fate.api import NumberInput, native_numbers
    assert number_evidence['result'] == native_numbers(NumberInput(**number_evidence['input']))
    assert number_recording['nativeReading'] == number_evidence['result']
    assert number_recording['media']['streams'][0]['width'] == 390
    assert len(load('fate/evidence/numerology-performance.json')['profiles']) == 5
    final_motion = (ROOT/'tmp/fate-final-motion-recheck.log').read_text(encoding='utf-8-sig')
    assert '2 passed' in final_motion and 'failed' not in final_motion.lower()
    recording=load('fate/evidence/recording.json')
    assert recording['mp4'] and recording['nativeReading']['factual_prediction'] is False
    for row in recording['nativeReading']['readings']:
        assert row['card']['id'] in load('fate/web/src/artwork/deck-manifest.json')['cards']
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
    source_paths = list(FATE.glob('*.py')) + list((FATE/'tests').glob('*.py')) + list((FATE/'web/src').rglob('*')) + list((FATE/'web/e2e').glob('*.ts')) + list((FATE/'web/scripts').glob('*.mjs'))
    source_paths += [FATE / p for p in ['web/package.json', 'web/package-lock.json', 'web/vite.config.ts', 'web/tsconfig.json', 'web/playwright.config.ts', 'experience.json', 'requirements.txt']]
    source_hashes = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(source_paths) if p.is_file()}
    receipt = dict(schema_version=3, date='2026-11-19', block='02 · The Oracle Gallery & Second Door',
                   status='Verified two-room consumer slice; physical-device/public-deployment acceptance remains P1',
                   units=units, fate_browser=browser, workbench_browser=workbench,
                   cli_cases=3515, independent_verifiers=52, protected_source_files=inherited['protected_count'], changed_protected_source_files=[],
                   npm_vulnerabilities=0, live_gemini='Retained Block 01 Tarot synthetic live-provider check. New Numerology boundary has provider-shape/reference/privacy tests and separate browser consent checks; no new live-provider claim.',
                   gates=gates, performance=load('fate/performance.json'),
                   rendering=load('fate/evidence/render-performance.json'),
                   host_performance=load('fate/evidence/host-performance.json'),
                   numerology_performance=load('fate/evidence/numerology-performance.json'),
                   numerology_native_evidence=number_evidence,
                   numerology_recording=number_recording,
                   execution_note='One earlier browser run overlapping the CLI verifiers missed the existing 20-second orb-start expectation; the final full browser gate was run without that competing workload. Performance and media collected separately.',
                   final_motion_recheck=dict(groups=2, passed=True, scope='Static manual dial turn retained under reduced motion, without restarting continuous animation; original initial-reduced/rapid-orb-cleanup group rechecked after this small CSS refinement', output=final_motion),
                   gallery_projection_sha256=sha(FATE/'web/src/gallery/inventory.json'),
                   artwork_registry_sha256=sha(FATE/'artwork-sources.json'),
                   generated_art_provenance_sha256=sha(FATE/'design/generated-artwork.json'),
                   block02_art_provenance_sha256=sha(FATE/'design/block02-artwork.json'),
                   original_artwork_sha256={p.name:sha(p) for p in sorted((FATE/'design/sources').glob('*.png'))},
                   source_sha256=source_hashes,
                   built_files_sha256={p.relative_to(FATE/'web/dist').as_posix(): sha(p) for p in sorted((FATE/'web/dist').rglob('*')) if p.is_file()},
                   screenshot_sha256={p.name: sha(p) for p in sorted((FATE/'screenshots').glob('*.png'))},
                   recording_sha256={p.name:sha(p) for p in sorted((FATE/'evidence').iterdir()) if p.suffix in ('.mp4','.webm')},
                   acceptance_criteria=['Native result equals replay through unchanged future.tarot.read', 'One/three cards, reversals and source references preserved', 'Progressive reveal and skip path; duplicates blocked and retry seed retained', 'No automatic cloud transmission or persistence', 'Pixi renders without console errors, animates, and stops on pause/reduced motion', 'Complete journey and export in mobile browser; accessibility scans and keyboard dialog pass', 'Small/tablet/desktop and doubled-text control geometry checks pass', 'No-WebGL fallback completes a native reading', 'Existing native/Workbench tests, full CLI/verifier gates, production builds and inventory/dependency gates pass'],
                   limitations=['Local Chromium mobile/desktop emulation and software WebGL only; no physical iOS/Android, field CWV or actual INP certification', '60 Hz is a target; sustained missed budgets reduce resolution and can select a 30 Hz low-power mode', 'No public deployment, distributed limiter, accounts or persistence', 'Complete verified historical Archive Edition; a fully bespoke figurative FATE deck remains future artwork, never mixed into draws as placeholders', 'Gemini semantic faithfulness is not guaranteed', 'Software acceptance is not empirical prediction validation'])
    receipt['acceptance_criteria'] += ['All 54 retained inventory IDs, six exclusions and availability categories match frozen projection', 'Real native Numerology parity, independent arithmetic, explicit Y/name basis and unsupported context preserved', 'Complete three-seal ritual, immediate reading path, exact export, retry/duplicate guards and session-only continuity', 'Numerology live material transforms, keyboard touch, reduced motion and low-power pause checks', 'Separate signed Numerology consent; provider prompt excludes names and dates; no automatic cloud or browser storage']
    receipt['limitations'] += ['Numerology direct themes cover Expression and Personal Year only; other numbers are context, never assigned unsupported meanings', 'Gallery upcoming status describes consumer availability only; no new engine or launch commitment', 'Numerology RAF cadence is main-thread scheduling evidence, not hardware compositor FPS; live provider semantic quality remains unverified']
    (FATE/'acceptance.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print('Recorded: 2522 native + 77 Workbench + 21 FATE tests; 18 + 9 browser groups; 3515 CLI cases; 52 independent verifiers; zero changed protected sources.')


if __name__ == '__main__':
    main()
