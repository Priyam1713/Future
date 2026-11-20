"""Verify and index the photographed World of Signs release against native replays."""

import hashlib
import json
import re
import subprocess

from .build_signs import OUT
from .signs import ENGINES, native_request, project
from .western import ROOT


FATE = ROOT / 'fate'
EVIDENCE = FATE / 'evidence'
BASE = '5227490'
ROOMS = {
    28: 'tea-leaves', 29: 'coffee-grounds', 30: 'candle-lore',
    31: 'water-signs', 32: 'weather-lore', 34: 'stone-table',
    35: 'bone-archive', 37: 'letter-lot', 38: 'bird-signs', 39: 'roman-cases',
}
CLIPS = {28, 32, 34, 35}


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regressions():
    unit = {'native': 2522, 'workbench': 77, 'fate': 65}
    for label, count in unit.items():
        log = (ROOT / f'tmp/block08-{label}.log').read_text(encoding='utf-8-sig')
        assert re.search(rf'^Ran {count} tests\b', log, re.M) and re.search(r'^OK$', log, re.M), label
    node = (ROOT / 'tmp/block08-node.log').read_text(encoding='utf-8-sig')
    assert 'pass 27' in node and 'fail 0' in node
    unit['codex_node'] = 27
    browser = {}
    for label, prefix, count in [('fate', '', 61), ('workbench', 'workbench-', 9)]:
        stats = load(FATE / f'{prefix}browser-acceptance.json')['stats']
        assert stats['expected'] == count and stats['unexpected'] == stats['skipped'] == stats['flaky'] == 0, stats
        browser[label] = stats
    cli = load(FATE / 'inherited-cli-acceptance.json')
    assert cli['complete'] and cli['passed'] and not cli['changed_protected_files']
    assert (cli['cli_cases'], cli['independent_verifiers'], cli['protected_count']) == (3515, 52, 576)
    subprocess.run(
        ['git', '-c', 'core.safecrlf=false', 'diff', '--exit-code', BASE, '--',
         'future', 'knowledge', 'resources', 'tests', 'data', 'workbench'], cwd=ROOT, check=True,
    )
    assert load(ROOT / 'tmp/block08-npm-audit.json')['metadata']['vulnerabilities']['total'] == 0
    assert 'No broken requirements found.' in (ROOT / 'tmp/block08-pip.log').read_text(encoding='utf-8-sig')
    assert '60 IDs and six exclusions pass' in (ROOT / 'tmp/block08-inventory.log').read_text(encoding='utf-8-sig')
    return unit, browser, {key: cli[key] for key in ('cli_cases', 'independent_verifiers', 'protected_count')}


def artifacts():
    native = load(EVIDENCE / 'block08-native.json')['native']
    clips = load(EVIDENCE / 'block08-recordings.json')['recordings']
    archive = load(OUT / 'reference-v1.json')
    performance = load(EVIDENCE / 'block08-performance.json')['profiles']
    assert set(native) == set(map(str, ROOMS))
    assert set(clips) == {ROOMS[oracle] for oracle in CLIPS}
    assert {(row['oracle'], row['mode']) for row in performance} == {
        (oracle, mode) for oracle in ROOMS for mode in ('mobile', 'desktop')
    }
    rooms = {}
    for oracle, slug in ROOMS.items():
        observed = native[str(oracle)]
        values = observed['request']['values']
        expected = ENGINES[oracle].read(native_request(oracle, values))
        assert observed['request']['oracle'] == oracle
        assert observed['result'] == json.loads(json.dumps(expected)), slug
        view = project(oracle, expected)
        assert observed['view'] == view == archive[str(oracle)]['|'.join(values)], slug
        snapshot = {'oracle': oracle, 'profile': ENGINES[oracle].PROFILE, 'values': values}
        assert observed['snapshot'] == snapshot
        proof = EVIDENCE / f'block08-privacy-{oracle}.json'
        privacy = load(proof)
        saved = privacy['stored']['chapters'][0]
        exported = privacy['exported']['chapters'][0]
        assert privacy['storageBeforeSave'] is None and not privacy['reopenPostRequests']
        assert saved['reference'] == 'fate-world-of-signs-v1'
        assert saved['snapshot'] == exported['snapshot'] == snapshot
        assert [entry['wording'] for entry in exported['source_readings']] == [row['text'] for row in view['excerpts']]
        paths = [proof, *(FATE / 'screenshots' / f'08-{slug}-{mode}.png'
                          for mode in ('mobile', 'desktop', 'entrance'))]
        if oracle in CLIPS:
            clip = clips[slug]
            assert clip['request'] == observed['request'] and clip['snapshot'] == snapshot
            stream = clip['media']['streams'][0]
            assert (stream['codec_name'], stream['width'], stream['height']) == ('h264', 390, 844)
            assert float(clip['media']['format']['duration']) >= 3
            paths.append(EVIDENCE / f'block08-{slug}.mp4')
        rooms[slug] = {
            'oracle': oracle, 'native_parity': True, 'reference_parity': True,
            'privacy': 'Explicit save, categorical snapshot, reload and open without POST, source-aligned export.',
            'files': {path.relative_to(FATE).as_posix(): digest(path) for path in paths},
        }
    return rooms, performance


def main():
    unit, browser, cli = regressions()
    rooms, performance = artifacts()
    art = FATE / 'design/block08-artwork.json'
    environments = load(art)['environments']
    assert {row['id'] for row in environments} == {'table', 'elemental', 'omens'}
    assert all(digest(ROOT / name) == sha for row in environments for name, sha in row['files'].items())
    gallery = load(FATE / 'web/src/gallery/inventory.json')
    available = {row['id'] for row in gallery['methods'] if row['status'] == 'available'}
    assert len(gallery['methods']) == 54 and len(available) == 24
    assert available == set(load(FATE / 'experience.json')['technique_ids'])
    variants = sum(map(len, load(OUT / 'reference-v1.json').values()))
    evidence = [art, *OUT.glob('*.json'), FATE / 'browser-acceptance.json',
                FATE / 'workbench-browser-acceptance.json', FATE / 'inherited-cli-acceptance.json',
                *(EVIDENCE / f'block08-{kind}.json' for kind in ('native', 'performance', 'recordings')),
                *(FATE / 'screenshots' / f'08-refined-{slug}-mobile.png'
                  for slug in ('crystal', 'mirror', 'geomancy', 'bibliomancy')),
                *(FATE / 'screenshots' / f'08-{slug}-entrance-mobile.png'
                  for slug in ('tea-leaves', 'weather-lore', 'bone-archive')),
                FATE / 'screenshots/08-gallery-desktop.png',
                FATE / 'screenshots/08-stone-table-placement-mobile.png']
    receipt = dict(
        block=8, baseline=BASE, unit_tests=unit, browser=browser, cli=cli, rooms=rooms,
        profiles=performance, saved_variants=variants, available_rooms=len(available),
        npm_reported_vulnerabilities=0, pip_check=True, inventory_check=True,
        evidence={p.relative_to(FATE).as_posix(): digest(p) for p in evidence},
        limits=['Local Chromium emulation and frame scheduling measurements.',
                'Source coverage limited to the categorical methods pinned in experience.json.'],
    )
    (EVIDENCE / 'block08-acceptance.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(f'Block 08 verified: ten native rooms, {sum(unit.values())} unit tests, 70 browser tests, '
          '3515 CLI cases and 52 independent verifiers.')


if __name__ == '__main__':
    main()
