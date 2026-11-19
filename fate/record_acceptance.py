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
    for name, filename, count in [('native', 'fate-inherited-unit.log', 2522), ('workbench', 'fate-workbench-unit.log', 77), ('fate', 'fate-api-tests.log', 45)]:
        log = (ROOT / 'tmp' / filename).read_text(encoding='utf-8-sig')
        assert re.search(r'Ran ' + str(count) + r' tests', log) and re.search(r'\nOK\s', log + '\n'), filename
        units[name] = dict(tests=count, passed=True, output=log)
    browser = load('fate/browser-acceptance.json')['stats']
    workbench = load('fate/workbench-browser-acceptance.json')['stats']
    comparison = load('fate/comparison-final-acceptance.json')['stats']
    for stats, expected in [(browser,36),(workbench,9),(comparison,2)]:
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
    node_output=(ROOT/'tmp/fate-codex-unit.log').read_text(encoding='utf-8-sig')
    assert re.search(r'\btests 24\b',node_output) and re.search(r'\bpass 24\b',node_output) and re.search(r'\bfail 0\b',node_output)
    codex_recording=load('fate/evidence/codex-recording.json')
    codex_privacy=load('fate/evidence/codex-privacy.json')
    codex_performance=load('fate/evidence/codex-performance.json')
    assert len(codex_recording['persisted']['chapters'])==2 and codex_recording['persisted']['schemaVersion']==1
    tarot_native=codex_recording['native']['tarot']
    from future.tarot import read
    assert tarot_native==read(tarot_native['replay']['request'])
    n=codex_recording['native']['numerology']
    assert n==native_numbers(NumberInput(name=n['name']['original'],birth=n['birth'],target=n['target'],basis=n['name']['basis'],y_roles=n['name']['y_roles']))
    for chapter,native_result in zip(codex_recording['persisted']['chapters'],[tarot_native,n]):
        assert set(chapter)=={'id','savedAt','reference','snapshot'} and chapter['reference']=='fate-codex-reference-v1'
        s=chapter['snapshot']
        if s['oracle']==16:
            assert set(s)=={'oracle','profile','spread','cards'}
            assert s['cards']==[dict(id=r['card']['id'],orientation=r['orientation']) for r in native_result['readings']]
        else:
            assert s==dict(oracle=4,profile=n['profile'],expression=n['expression']['result'],personalYear=n['cycles']['year']['result'],lifePath=n['life_path']['result'])
    assert not codex_privacy['postRequestsDuringReopen']
    assert len(codex_performance['profiles'])==5
    for p in codex_performance['profiles']:
        assert not p['posts'] and p['metrics']['canvases']==0 and p['metrics']['recordBytes']<=65536
        assert p['metrics']['cls'] < 0.001
        assert not any('createOrbScene' in r['name'] for r in p['metrics']['resources'])
    western_evidence=load('fate/evidence/western-engine.json')
    western_recording=load('fate/evidence/western-recording.json')
    western_privacy=load('fate/evidence/western-privacy.json')
    western_comparison=load('fate/evidence/western-comparison.json')
    western_performance=load('fate/evidence/western-performance.json')
    from future.natal import chart, Settings, SkyfieldEphemeris
    from future.core_readings import placements
    from future.knowledge import Registry
    ephemeris=SkyfieldEphemeris(ROOT/'data/de440s.bsp')
    registry=Registry()
    try:
        q=western_evidence['input']
        expected=chart(ephemeris,q['local'],q['zone'],q['latitude'],q['longitude'],Settings(houses=q['houses']),q['fold'])
        expected['reading']=placements(expected,registry)
        expected=json.loads(json.dumps(expected))
        assert expected==western_evidence['native']==western_recording['native']==load('fate/evidence/western-browser-native.json')['native']==western_comparison['western']
    finally:
        registry.close();ephemeris.kernel.close()
    cn=western_comparison['numerology']
    assert cn==native_numbers(NumberInput(name=cn['name']['original'],birth=cn['birth'],target=cn['target'],basis=cn['name']['basis'],y_roles=cn['name']['y_roles']))
    for c in [western_evidence['saved']['chapters'][0],western_privacy['saved']['chapters'][0]]:
        assert set(c)=={'id','savedAt','reference','snapshot'} and c['reference']=='fate-western-reference-v1'
        ss=c['snapshot'];assert set(ss)=={'oracle','profile','houses','planets','angles','cusps','aspects'}
        assert ss['oracle']==1 and ss['angles']==list(expected['angles'].values()) and ss['cusps']==expected['house_cusps'] and ss['aspects']==expected['aspects']
        assert ss['planets']==[[p['longitude'],p['retrograde'],p['house']] for p in expected['planets'].values()]
    assert western_evidence['beforeSaveStorage']=={} and western_privacy['assertionsPassed'] and not western_privacy['postsOnReopen']
    assert len(western_performance['profiles'])==5
    provenance=load('fate/data/places-provenance.json')
    assert hashlib.sha256((FATE/'data/places-v1.json').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==provenance['projection_sha256']
    for p in western_performance['profiles']:
        assert p['planets']==10 and p['metrics']['canvases']==0 and p['snapshotBytes']<65536
        assert not any('createOrbScene' in r['name'] for r in p['metrics']['resources'])
        assert all(url.endswith(('/api/western','/api/western/places')) for url in p['posts'])
        assert p['metrics']['cls'] < 0.1
    turning_evidence=load('fate/evidence/turning-engine.json')
    turning_browser=load('fate/evidence/turning-browser-native.json')
    turning_recording=load('fate/evidence/turning-recording.json')
    turning_privacy=load('fate/evidence/turning-privacy.json')
    turning_performance=load('fate/evidence/turning-performance.json')
    turning_computation=load('fate/evidence/turning-computation.json')
    assert turning_evidence['result']['report']==turning_browser['result']['report']
    assert turning_evidence['result']['sky_samples']==turning_browser['result']['sky_samples']
    assert turning_evidence['birthFieldsExcludedFromBasis'] and not turning_privacy['postRequestsOnReopen']
    for document in [turning_evidence['saved'],turning_privacy['saved']]:
        c=document['chapters'][0];assert c['reference']=='fate-transit-reference-v1'
        ss=c['snapshot'];assert set(ss)=={'oracle','profile','window','targets','configs','events','frames'} and ss['profile']=='turning-sky-v1'
        assert len(ss['events'])==len(turning_evidence['result']['report']['exact_events'])
        assert len(ss['frames'])==7
        assert all(len(config)==9 and all(len(w)==5 for w in config[5]) for config in ss['configs'])
    assert len(turning_performance['profiles'])==5 and len(turning_computation['profiles'])==3
    assert [p['days'] for p in turning_computation['profiles']]==[1,7,30]
    assert all(p['native_parity'] and p['daily_sample_parity'] and not p['raw_birth_fields_present'] and p['worker']['seconds']<=62 for p in turning_computation['profiles'])
    assert turning_recording['result']['computation']['native_days']==30 and turning_recording['result']['report']['presentation']['repeated_patterns']
    for p in turning_performance['profiles']:
        assert p['metrics']['canvases']==0 and p['savedBytes']<=65536 and p['metrics']['cls']<.1
        assert p['worker']['deadline_seconds']==60
        assert not any('createOrbScene' in r['name'] for r in p['metrics']['resources'])
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
    assets = dict(turning_pack=load('fate/design/block05-artwork.json'), western_pack=load('fate/design/block04-artwork.json'), pack=dict(name='FATE-asset-pack-01.zip', sha256=pack_hash, provenance='Project owner supplied; original artwork/audio declaration retained in pack README'),
                  files={p.relative_to(FATE).as_posix(): sha(p) for p in sorted((FATE/'web/public').rglob('*')) if p.is_file()})
    (FATE/'assets.json').write_text(json.dumps(assets, indent=2)+'\n', encoding='utf-8')
    source_paths = list(FATE.glob('*.py')) + list((FATE/'tests').glob('*.py')) + list((FATE/'web/src').rglob('*')) + list((FATE/'web/e2e').glob('*.ts')) + list((FATE/'web/scripts').glob('*.mjs'))
    source_paths += list((FATE/'data').glob('*.json'))
    source_paths += [FATE / p for p in ['web/package.json', 'web/package-lock.json', 'web/vite.config.ts', 'web/tsconfig.json', 'web/playwright.config.ts', 'experience.json', 'requirements.txt']]
    source_hashes = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(source_paths) if p.is_file()}
    receipt = dict(schema_version=6, date='2026-11-19', block='05 · The Turning Sky',
                   status='Verified Turning Sky over unchanged native transits, three existing oracle rooms and versioned local Codex; physical-device/public-deployment acceptance remains P1',
                   units=units, fate_browser=browser, workbench_browser=workbench, final_comparison_browser=comparison,
                   cli_cases=3515, independent_verifiers=52, protected_source_files=inherited['protected_count'], changed_protected_source_files=[],
                   npm_vulnerabilities=0, live_gemini='Retained Block 01 Tarot synthetic live-provider check. Numerology and Western boundaries have provider-shape/reference/privacy tests and separate browser consent checks; no new live-provider claim.',
                   gates=gates, performance=load('fate/performance.json'),
                   rendering=load('fate/evidence/render-performance.json'),
                   host_performance=load('fate/evidence/host-performance.json'),
                   numerology_performance=load('fate/evidence/numerology-performance.json'),
                   numerology_native_evidence=number_evidence,
                   numerology_recording=number_recording,
                   codex_node=dict(tests=24,passed=True,output=node_output),
                   codex_performance=codex_performance,
                   codex_recording=codex_recording,
                   codex_privacy=codex_privacy,
                   turning_native=turning_evidence, turning_browser=turning_browser, turning_recording=turning_recording, turning_privacy=turning_privacy, turning_performance=turning_performance, turning_computation=turning_computation,
                   block05_art_provenance_sha256=sha(FATE/'design/block05-artwork.json'),
                   transit_source_edition_sha256=sha(FATE/'web/src/turning/reference-v1.json'),
                   western_comparison=western_comparison, western_native=western_evidence, western_recording=western_recording, western_privacy=western_privacy, western_performance=western_performance,
                   execution_note='Complete 36-group browser gate runs separately from inherited CLI work, video and performance profiling. All original oracle, Codex and motion checks retained; six new Turning Sky groups cover native data, source depth, storage, cancellation, responsive/reduced motion and mobile labels/short comparison. Final stills settle motion only for capture; recording remains live.',
                   codex_reference_sha256=sha(FATE/'web/src/codex/reference-v1.json'),
                   gallery_projection_sha256=sha(FATE/'web/src/gallery/inventory.json'),
                   artwork_registry_sha256=sha(FATE/'artwork-sources.json'),
                   generated_art_provenance_sha256=sha(FATE/'design/generated-artwork.json'),
                   block02_art_provenance_sha256=sha(FATE/'design/block02-artwork.json'),
                   block04_art_provenance_sha256=sha(FATE/'design/block04-artwork.json'),
                   western_source_edition_sha256=sha(FATE/'web/src/astrology/reference-v1.json'),
                   block03_art_provenance_sha256=sha(FATE/'design/block03-artwork.json'),
                   original_artwork_sha256={p.name:sha(p) for p in sorted((FATE/'design/sources').glob('*.png'))},
                   source_sha256=source_hashes,
                   built_files_sha256={p.relative_to(FATE/'web/dist').as_posix(): sha(p) for p in sorted((FATE/'web/dist').rglob('*')) if p.is_file()},
                   screenshot_sha256={p.name: sha(p) for p in sorted((FATE/'screenshots').glob('*.png'))},
                   recording_sha256={p.name:sha(p) for p in sorted((FATE/'evidence').iterdir()) if p.suffix in ('.mp4','.webm')},
                   acceptance_criteria=['Native result equals replay through unchanged future.tarot.read', 'One/three cards, reversals and source references preserved', 'Progressive reveal and skip path; duplicates blocked and retry seed retained', 'No automatic cloud transmission; chapter persistence requires explicit Save to this device', 'Pixi renders without console errors, animates, and stops on pause/reduced motion', 'Complete journeys and export in mobile browser; accessibility scans and keyboard dialog pass', 'Small/tablet/desktop and doubled-text control geometry checks pass', 'No-WebGL fallback completes a native reading', 'Existing native/Workbench tests, full CLI/verifier gates, production builds and inventory/dependency gates pass'],
                   limitations=['Local Chromium mobile/desktop emulation and software WebGL only; no physical iOS/Android, field CWV or actual INP certification', '60 Hz is a target; sustained missed budgets reduce resolution and can select a 30 Hz low-power mode', 'No public deployment, distributed limiter, accounts or cloud sync; local chapters require explicit saving', 'Complete verified historical Archive Edition; a fully bespoke figurative FATE deck remains future artwork, never mixed into draws as placeholders', 'Gemini semantic faithfulness is not guaranteed', 'Software acceptance is not empirical prediction validation'])
    receipt['acceptance_criteria'] += ['All 54 retained inventory IDs, six exclusions and availability categories match frozen projection', 'Real native Numerology parity, independent arithmetic, explicit Y/name basis and unsupported context preserved', 'Complete three-seal ritual, immediate reading path, exact export, retry/duplicate guards and session-only continuity', 'Numerology live material transforms, keyboard touch, reduced motion and low-power pause checks', 'Separate signed Numerology consent; provider prompt excludes names and dates; no automatic cloud transmission or original-input storage']
    receipt['limitations'] += ['Numerology direct themes cover Expression and Personal Year only; other numbers are context, never assigned unsupported meanings', 'Gallery upcoming status describes consumer availability only; no new engine or launch commitment', 'Numerology RAF cadence is main-thread scheduling evidence, not hardware compositor FPS; live provider semantic quality remains unverified']
    receipt['acceptance_criteria'] += ['Native transit report and all daily ephemeris samples independently replay for 1/7/30-day bounded API windows', 'Signed current natal basis excludes raw birth inputs; altered/expired/restarted proofs cannot reconstruct missing birth information', 'One killable worker, no queue; strict bounds, hard timeout, disconnect termination and slot cleanup tested', 'Saved dated edition preserves native exact timestamps, longitudes, matched rules, phase samples and native interval hours without new API calls', 'Mobile natal labels resolve collisions while longitude markers stay unchanged; compact comparison retains all citations on demand']
    receipt['limitations'] += ['Daily sky samples are discrete at the chosen UTC clock time; exact focus shows only the actual contact geometry, without interpolated ephemeris positions', 'Natal origin proof lasts one hour and ends on process-key restart; saved chapters cannot restart live searches or recover birth inputs', 'Transit computation is bounded to 60 seconds and one active worker per process; long chapters may fill the 64K local document before the chapter-count cap']
    receipt['acceptance_criteria'] += ['Native Western chart and source composition equal direct unchanged engine replay', 'Exact live SVG planet longitudes, twelve house cusps and aspects match native results', 'Unknown time blocked; DST gaps, explicit folds, IANA historical offsets and polar restrictions tested', 'Explicit chart snapshot excludes raw birth datetime, coordinates, timezone, place, receipt and commentary', 'Frozen Western source edition restores source components without chart/provider POSTs', 'Gemini requires signed per-chart consent and omits original birth inputs from provider prompt', 'Responsive 320/390/768/1440 chart, keyboard turn, pause/reduced/low-capability and source depth pass']
    receipt['limitations'] += ['City points are approximate current GeoNames references; exact birthplace coordinates and historical timezone/birth-record accuracy need visitor verification', 'Western consumer room supports tropical modern natal components only; no unknown birth times, direct combined placement/planet-pair readings or event predictions', 'Derived saved chart geometry can reveal birth-moment information; size cap may bind before 50 chapters']
    receipt['acceptance_criteria'] += ['Explicit local save excludes raw birth/name/question inputs, Numerology target dates, traces, replay seeds and Gemini commentary; dated transit windows require explicit save', 'Frozen source edition reopens minimal chapters after refresh without new engine/provider POST requests', 'Unknown/corrupt/private-extra-key records fail closed; quota failures never fabricate saved status', 'Individual/all deletion preserves unrelated storage; other tabs refresh without stale chapter content', 'Real cover/leaf, source chapter navigation, keyboard/reduced motion and bounded responsive folios pass', 'Source-language comparison cites original themes, keeps alternatives separate and invents no agreement score or combined prediction']
    receipt['limitations'] += ['Local records are unencrypted, editable and subject to browser clearing/quota/origin policies; no accounts, sync, automatic backup or import UI', 'Simultaneous cross-tab writes can conflict; explicit exports are the independent backup', 'Source-language comparison uses a bounded editorial vocabulary; lexical echoes are not independent corroboration', 'App/artwork must be available to reopen chapters; normal asset requests still reach the host']
    (FATE/'acceptance.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print('Recorded: 2522 native + 77 Workbench + 45 FATE + 24 Codex Node tests; 36 + 9 browser groups; 3515 CLI cases; 52 independent verifiers; zero changed protected sources.')


if __name__ == '__main__':
    main()
