"""Bind real browser artifacts to the native reports and regression receipts."""

import hashlib
import json
import re
import subprocess

from pydantic import TypeAdapter

from .build_manuscript import OUT
from .manuscript import Request, read
from .western import ROOT, WesternService


FATE = ROOT / 'fate'
EVIDENCE = FATE / 'evidence'
BASE = 'f444fc0'
ROOMS = {
    5: 'horary', 6: 'mundane', 7: 'astrocartography', 8: 'palmistry',
    9: 'face-reading', 10: 'phrenology', 11: 'moleosophy', 12: 'podomancy',
    13: 'graphology', 14: 'aura', 15: 'iridology', 40: 'compass',
}
FILMED = {7, 8, 40}


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def log_text(path):
    data = path.read_bytes()
    encoding = 'utf-16' if data.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig'
    return data.decode(encoding).replace('\r\n', '\n')


def indexed(paths):
    return {path.relative_to(FATE).as_posix(): digest(path) for path in paths}


def regressions():
    units = {'native': 2522, 'workbench': 77, 'fate': 71}
    for label, count in units.items():
        log = log_text(ROOT / f'tmp/block09-{label}.log')
        assert re.search(rf'^Ran {count} tests\b', log, re.M) and re.search(r'^OK$', log, re.M), label
    node = (ROOT / 'tmp/block09-node.log').read_text(encoding='utf-8-sig')
    assert 'pass 27' in node and 'fail 0' in node
    units['codex_node'] = 27
    browsers = {}
    for name, prefix, count in [('fate', '', 77), ('workbench', 'workbench-', 9)]:
        result = load(FATE / f'{prefix}browser-acceptance.json')['stats']
        assert result['expected'] == count and result['unexpected'] == result['skipped'] == result['flaky'] == 0, result
        browsers[name] = result
    cli = load(FATE / 'inherited-cli-acceptance.json')
    assert cli['complete'] and cli['passed'] and not cli['changed_protected_files']
    assert (cli['cli_cases'], cli['independent_verifiers'], cli['protected_count']) == (3515, 52, 576)
    subprocess.run(['git', '-c', 'core.safecrlf=false', 'diff', '--exit-code', BASE, '--',
                    'future', 'knowledge', 'resources', 'tests', 'workbench', 'data'], cwd=ROOT, check=True)
    assert load(ROOT / 'tmp/block09-npm-audit.json')['metadata']['vulnerabilities']['total'] == 0
    assert 'No broken requirements found.' in (ROOT / 'tmp/block09-pip.log').read_text(encoding='utf-8-sig')
    assert '60 IDs and six exclusions pass' in (ROOT / 'tmp/block09-inventory.log').read_text(encoding='utf-8-sig')
    return units, browsers, {key: cli[key] for key in ('cli_cases', 'independent_verifiers', 'protected_count')}


def replay(service, observed):
    query = TypeAdapter(Request).validate_python(observed['request'])
    expected = json.loads(json.dumps(read(query, service)))
    assert all(observed[key] == value for key, value in expected.items()), query.oracle
    return expected


def artifacts():
    reports = load(EVIDENCE / 'block09-native.json')['reports']
    recordings = load(EVIDENCE / 'block09-recordings.json')['recordings']
    profile = load(EVIDENCE / 'block09-performance.json')['profiles']
    archive = load(OUT / 'reference-v1.json')
    assert set(reports) == set(map(str, ROOMS))
    assert set(recordings) == {ROOMS[i] for i in FILMED}
    assert {(row['oracle'], row['device']) for row in profile} == {
        (oracle, device) for oracle in ROOMS for device in ('mobile', 'desktop')
    }
    service = WesternService()
    rooms = {}
    try:
        for oracle, slug in ROOMS.items():
            observed = reports[str(oracle)]
            expected = replay(service, observed)
            assert expected['result']['technique_id'] == oracle
            paths = [FATE / 'screenshots' / f'09-{slug}-{device}.png' for device in ('mobile', 'desktop')]
            if oracle in (5, 6):
                paths.append(FATE / 'screenshots' / f'09-{slug}-reading-mobile.png')
            if oracle in FILMED:
                paths.extend(FATE / 'screenshots' / f'09-{slug}-entrance-{device}.png' for device in ('mobile', 'desktop'))
                recording = recordings[slug]
                assert recording['request'] == observed['request']
                stream = recording['media']['streams'][0]
                assert (stream['codec_name'], stream['width'], stream['height']) == ('h264', 390, 844)
                assert float(recording['media']['format']['duration']) >= 3
                paths.append(EVIDENCE / f'block09-{slug}.mp4')
            if oracle >= 8:
                path = EVIDENCE / f'block09-privacy-{oracle}.json'
                proof = load(path)
                assert proof['storageBeforeSave'] is None and not proof['reopenPostRequests']
                chapter = proof['stored']['chapters'][0]
                exported = proof['exported']['chapters'][0]
                keys = expected['references'] if oracle == 40 else [expected['reference']]
                edition = 'fate-manuscript-reference-v1'
                assert chapter['reference'] == edition
                assert chapter['snapshot'] == exported['snapshot'] == dict(oracle=oracle, profile=edition, entries=keys)
                expected_sources = [row for key in keys for row in archive[str(oracle)][key]['sources']]
                assert [row['wording'] for row in exported['source_readings']] == [s['text'] for s in expected_sources]
                paths.append(path)
            rooms[slug] = dict(oracle=oracle, full_native_parity=True,
                               storage='explicit source IDs' if oracle >= 8 else 'visit only', files=indexed(paths))
        conjunction = load(EVIDENCE / 'block09-conjunction.json')
        assert len(replay(service, conjunction)['result']['events']) == 1
    finally:
        service.close()
    return rooms, profile, conjunction['actionMs']


def main():
    units, browsers, cli = regressions()
    rooms, profiles, conjunction_ms = artifacts()
    art = FATE / 'design/block09-artwork.json'
    artwork = load(art)
    assert {row['id'] for row in artwork['environments']} == {'court', 'manuscript', 'compass'}
    assert all(digest(ROOT / path) == sha for row in artwork['environments'] for path, sha in row['files'].items())
    inventory = load(FATE / 'web/src/gallery/inventory.json')
    available = [row['id'] for row in inventory['methods'] if row['status'] == 'available']
    assert len(inventory['methods']) == 54 and len(available) == 36
    assert available == load(FATE / 'experience.json')['technique_ids']
    paths = [art, *OUT.glob('*.json'), FATE / 'browser-acceptance.json', FATE / 'workbench-browser-acceptance.json',
             FATE / 'inherited-cli-acceptance.json', *(EVIDENCE / f'block09-{kind}.json'
             for kind in ('native', 'conjunction', 'performance', 'recordings'))]
    loopback = load(ROOT / 'tmp/block09-http.json')
    assert {row['oracle'] for row in loopback} == {5, 6, 7, 40}
    receipt = dict(block=9, baseline=BASE, available_rooms=len(available), rooms=rooms, unit_tests=units,
                   browsers=browsers, cli=cli, profiles=profiles, conjunction_action_ms=conjunction_ms,
                   loopback_http_sample=loopback,
                   evidence=indexed(paths), limits=['Local Chromium emulation; frame intervals describe callback scheduling.',
                       'Court calculations remain in the visit. Manuscript and Compass save source references.',
                       'Room-supported profiles are bounded in experience.json.'])
    (EVIDENCE / 'block09-acceptance.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(f'Block 09 verified: 12 native rooms, {sum(units.values())} unit tests, 86 browser tests, '
          '3515 CLI cases and 52 verifiers.')


if __name__ == '__main__':
    main()
