"""Verify Block 06 evidence against direct native replays and the final build."""
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone

from future import chinese, chinese_readings, iching, runes, vedic, vedic_timing
from future.iching_cast import PROTOCOL as COIN_PROTOCOL
from future.natal import SkyfieldEphemeris

from .chambers import snapshot
from .western import ROOT

FATE = ROOT / 'fate'
EVIDENCE = FATE / 'evidence'
BASE = '551dda5'
ROOMS = {'vedic': 2, 'bazi': 3, 'iching': 18, 'runes': 19}


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(q, engine):
    oracle = q['oracle']
    if oracle in (2, 3):
        birth = [q[k] for k in ('local', 'zone', 'latitude', 'longitude', 'fold')]
        if oracle == 2:
            target = datetime.fromisoformat(q['target']).replace(tzinfo=timezone.utc)
            return vedic_timing.enrich(vedic.d1(engine, *birth), target, q['year_key'], include_d9=True)
        return chinese_readings.enrich(chinese.chart(engine, *birth, q['profile']))
    common = dict(schema_version=1, task='symbolic_reading', mode='seeded', seed=q['seed'])
    if oracle == 18:
        return iching.read(dict(common, profile=iching.PROFILE, reading_policy=iching.POLICY,
            method='three-coin', protocol=COIN_PROTOCOL, line_order='bottom_to_top'))
    return runes.read(dict(common, profile=runes.PROFILE, protocol=runes.PROTOCOL,
        orientation_policy='upright_only', spread=q['spread']))


def verify_gates():
    units = {}
    for suite, count in (('native', 2522), ('workbench', 77), ('fate', 52)):
        log = (ROOT/f'tmp/block06-{suite}.log').read_text(encoding='utf-8-sig')
        assert re.search(rf'^Ran {count} tests\b', log, re.M) and re.search(r'^OK$', log, re.M), suite
        units[suite] = count
    node = (ROOT/'tmp/block06-node.log').read_text(encoding='utf-8-sig')
    assert 'pass 25' in node and 'fail 0' in node
    units['codex_node'] = 25
    browser = {}
    for suite, name, count in (('fate', 'browser-acceptance.json', 41), ('workbench', 'workbench-browser-acceptance.json', 9)):
        stats = read(FATE/name)['stats']
        assert stats['expected'] == count and stats['unexpected'] == stats['flaky'] == stats['skipped'] == 0
        browser[suite] = stats
    cli = read(FATE/'inherited-cli-acceptance.json')
    assert cli['complete'] and cli['passed'] and cli['cli_cases'] == 3515 and cli['independent_verifiers'] == 52
    assert cli['protected_count'] == 576 and cli['changed_protected_files'] == []
    subprocess.run(['git', 'diff', '--exit-code', BASE, '--', 'future', 'workbench', 'knowledge',
                    'resources', 'tests', 'data'], cwd=ROOT, check=True)
    audit = read(ROOT/'tmp/block06-npm-audit.json')['metadata']['vulnerabilities']
    assert audit['total'] == 0
    assert 'No broken requirements found.' in (ROOT/'tmp/block06-pip.log').read_text(encoding='utf-8-sig')
    inventory = (ROOT/'tmp/block06-inventory.log').read_text(encoding='utf-8-sig')
    assert '60 IDs and six exclusions pass' in inventory
    return units, browser, {k: cli[k] for k in ('cli_cases', 'independent_verifiers', 'protected_count')}


def verify_rooms():
    native = read(EVIDENCE/'block06-native.json')['native']
    recordings = read(EVIDENCE/'block06-recordings.json')['recordings']
    performance = read(EVIDENCE/'block06-performance.json')['profiles']
    assert set(native) == set(recordings) == set(ROOMS)
    assert {(r['room'], r['profile']) for r in performance} == {(room, mode) for room in ROOMS for mode in ('mobile', 'desktop')}
    assert all(r['metrics']['canvases'] == 0 for r in performance)
    engine = SkyfieldEphemeris(ROOT/'data/de440s.bsp')
    rooms = {}
    try:
        for room, oracle in ROOMS.items():
            source, video = native[room], recordings[room]
            expected = replay(source['request'], engine)
            assert json.loads(json.dumps(expected)) == source['result']
            assert snapshot(expected) == source['snapshot']
            assert snapshot(replay(video['request'], engine)) == video['snapshot']
            media = video['media']
            assert media['streams'][0]['width'] == 390 and media['streams'][0]['height'] == 844
            assert media['streams'][0]['codec_name'] == 'h264' and float(media['format']['duration']) > 3
            if oracle == 18:
                assert video['snapshot']['figures'][0] != video['snapshot']['figures'][1]
            privacy = read(EVIDENCE/f'block06-privacy-{oracle}.json')
            assert privacy['storageBeforeSave'] is None and not privacy['reopenPostRequests']
            c = privacy['stored']['chapters'][0]
            assert c['reference'] == 'fate-four-chambers-v1' and c['snapshot']['oracle'] == oracle
            assert privacy['exported']['chapters'][0]['snapshot'] == c['snapshot']
            assert privacy['exported']['chapters'][0]['source_readings']
            images = sorted((FATE/'screenshots').glob(f'06-{room}-*.png'))
            assert len(images) == 3
            files = [*images, EVIDENCE/f'block06-{room}.mp4', EVIDENCE/f'block06-privacy-{oracle}.json']
            rooms[room] = dict(oracle=oracle, native_parity=True, recording_snapshot_parity=True,
                recorded_seconds=float(media['format']['duration']), local_reopen_without_post=True,
                chapter_bytes=len(json.dumps(privacy['stored'], separators=(',', ':')).encode()),
                artifacts={p.relative_to(FATE).as_posix():digest(p) for p in files})
    finally:
        engine.kernel.close()
    return rooms, performance


def main():
    units, browser, cli = verify_gates()
    rooms, performance = verify_rooms()
    art = read(FATE/'design/block06-artwork.json')
    assert len(art) == 8 and set(row['room'] for row in art) == set(ROOMS)
    for row in art:
        for name, expected in row['files'].items():
            assert digest(ROOT/name) == expected
    archive = FATE/'web/src/chambers'
    manifest = dict(block=6, baseline=BASE, unit_tests=units, browser=browser, cli=cli,
        npm_reported_vulnerabilities=0, pip_check=True, inventory_check=True,
        rooms=rooms, performance=performance,
        evidence={p.relative_to(FATE).as_posix():digest(p) for p in [
            *archive.glob('*.json'), FATE/'design/block06-artwork.json', EVIDENCE/'block06-native.json',
            EVIDENCE/'block06-recordings.json', EVIDENCE/'block06-performance.json',
            FATE/'browser-acceptance.json', FATE/'workbench-browser-acceptance.json', FATE/'inherited-cli-acceptance.json',
        ]}, limits=[
            'Local Chromium emulation with a warmed service process. Physical devices and field performance remain unverified.',
            'Vedic saved dasha views use UTC boundary days. The full live native export includes the exact timing data.',
            'Saved calculated geometry and pillars remain personal in unencrypted local storage.',
            'Optional Gemini was checked with a controlled provider. The native playback and media contain no provider output.',
        ])
    entry = FATE/'web/dist/index.html'
    manifest['production_entry_sha256'] = digest(entry)
    manifest['production_assets_sha256'] = {p.name:digest(p) for p in sorted((entry.parent/'assets').glob('*')) if p.is_file()}
    (EVIDENCE/'block06-acceptance.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Block 06 verified:', sum(units.values()), 'unit/boundary tests, 50 browser groups,',
          cli['cli_cases'], 'CLI cases,', cli['independent_verifiers'], 'independent verifiers.')


if __name__ == '__main__':
    main()
