"""Bind Block 07 browser evidence to replays through the unchanged native engines."""
import hashlib
import json
import re
import subprocess

from .ritual import ENGINES, native_request, snapshot
from .western import ROOT

FATE = ROOT / 'fate'
EVIDENCE = FATE / 'evidence'
BASE = '668333f'
ROOMS = {'oracle':17, 'pendulum':20, 'crystal':21, 'mirror':22,
         'dream':23, 'geomancy':33, 'bibliomancy':36}


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regressions():
    unit = {}
    for label, count in [('native',2522),('workbench',77),('fate',60)]:
        log=(ROOT/f'tmp/block07-{label}.log').read_text(encoding='utf-8-sig')
        assert re.search(rf'^Ran {count} tests\b',log,re.M) and re.search(r'^OK$',log,re.M),label
        unit[label]=count
    node=(ROOT/'tmp/block07-node.log').read_text(encoding='utf-8-sig')
    assert 'pass 26' in node and 'fail 0' in node
    unit['codex_node']=26
    browser={}
    for label, name, count in [('fate','browser-acceptance.json',49),('workbench','workbench-browser-acceptance.json',9)]:
        stats=load(FATE/name)['stats']
        assert stats['expected']==count and stats['unexpected']==stats['skipped']==stats['flaky']==0,stats
        browser[label]=stats
    cli=load(FATE/'inherited-cli-acceptance.json')
    assert cli['complete'] and cli['passed'] and cli['protected_count']==576
    assert (cli['cli_cases'],cli['independent_verifiers'])==(3515,52)
    subprocess.run(['git','diff','--exit-code',BASE,'--','future','knowledge','resources','tests','data','workbench'],
                   cwd=ROOT,check=True)
    audit=load(ROOT/'tmp/block07-npm-audit.json')['metadata']['vulnerabilities']
    assert audit['total']==0
    assert 'No broken requirements found.' in (ROOT/'tmp/block07-pip.log').read_text(encoding='utf-8-sig')
    assert '60 IDs and six exclusions pass' in (ROOT/'tmp/block07-inventory.log').read_text(encoding='utf-8-sig')
    return unit,browser,{key:cli[key] for key in ('cli_cases','independent_verifiers','protected_count')}


def artifacts():
    native=load(EVIDENCE/'block07-native.json')['native']
    records=load(EVIDENCE/'block07-recordings.json')['recordings']
    perf=load(EVIDENCE/'block07-performance.json')['profiles']
    assert set(native)==set(records)==set(ROOMS)
    assert {(row['room'],row['profile']) for row in perf}=={
        (room,mode) for room in ROOMS for mode in ('mobile','desktop')}
    assert all(row['metrics']['canvases']==(1 if row['room'] in ('crystal','mirror') else 0) for row in perf)
    assert all(row['metrics']['renderer']=='volumetric' for row in perf if row['room'] in ('crystal','mirror'))
    outcomes={}
    for room,oracle in ROOMS.items():
        observed,video=native[room],records[room]
        engine=ENGINES[oracle]
        q=native_request(oracle,observed['request']['input'])
        assert observed['request']['oracle']==oracle
        assert observed['result']['replay']['request']==q
        direct=engine.read(q)
        assert json.loads(json.dumps(direct))==observed['result'],room
        assert snapshot(oracle,direct)==observed['snapshot']
        replay=engine.read(native_request(oracle,video['request']['input']))
        assert snapshot(oracle,replay)==video['snapshot'],room
        media=video['media']
        stream=media['streams'][0]
        assert (stream['codec_name'],stream['width'],stream['height'])==('h264',390,844)
        assert float(media['format']['duration'])>=3
        privacy=load(EVIDENCE/f'block07-privacy-{oracle}.json')
        chapter=privacy['stored']['chapters'][0]
        assert privacy['storageBeforeSave'] is None and privacy['reopenPostRequests']==[]
        assert chapter['reference']=='fate-ritual-wing-v1' and chapter['snapshot']['oracle']==oracle
        assert set(chapter['snapshot'])=={'oracle','profile','values'}
        assert privacy['exported']['chapters'][0]['snapshot']==chapter['snapshot']
        if oracle in (21,22):
            assert chapter['snapshot']['values']==[]
        assert 'Synthetic QA note:' not in json.dumps(privacy)
        shots=list((FATE/'screenshots').glob(f'07-{room}-*.png'))
        assert {f'07-{room}-{mode}.png' for mode in ('mobile','desktop','entrance')}<={p.name for p in shots}
        paths=[*shots,EVIDENCE/f'block07-{room}.mp4',EVIDENCE/f'block07-privacy-{oracle}.json']
        outcomes[room]=dict(oracle=oracle,native_parity=True,recording_parity=True,
            recorded_seconds=float(media['format']['duration']),
            chapter_bytes=len(json.dumps(privacy['stored'],separators=(',',':')).encode()),
            artifact_hashes={p.relative_to(FATE).as_posix():digest(p) for p in sorted(paths)})
    return outcomes,perf


def main():
    unit,browser,cli=regressions()
    rooms,performance=artifacts()
    art=load(FATE/'design/block07-artwork.json')
    assert len(art)==17
    files={name:sha for row in art for name,sha in row['files'].items()}
    assert {f'fate/web/public/art/ritual-deck/lenormand-{i:02d}.webp' for i in range(1,37)}<=files.keys()
    assert all(digest(ROOT/name)==sha for name,sha in files.items())
    dist=FATE/'web/dist'
    evidence=[FATE/'design/block07-artwork.json',EVIDENCE/'block07-native.json',EVIDENCE/'block07-recordings.json',
              EVIDENCE/'block07-performance.json',FATE/'browser-acceptance.json',FATE/'workbench-browser-acceptance.json',
              FATE/'inherited-cli-acceptance.json',*list((FATE/'web/src/ritual').glob('*.json'))]
    receipt=dict(block=7,baseline=BASE,unit_tests=unit,browser=browser,cli=cli,
        npm_reported_vulnerabilities=0,pip_check=True,inventory_check=True,rooms=rooms,performance=performance,
        evidence={p.relative_to(FATE).as_posix():digest(p) for p in evidence},
        production={p.relative_to(dist).as_posix():digest(p) for p in sorted(dist.rglob('*')) if p.is_file()},
        limits=['Local Chromium emulation. No physical phone or compositor frame certification.',
                'Saved journals reopen public guide bookmarks. Dream bookmarks keep motif IDs without private context.',
                'The manual geomancy consumer accepts row patterns. The bibliomancy consumer selects from Ruth only.'])
    (EVIDENCE/'block07-acceptance.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(f"Block 07 verified: {sum(unit.values())} unit and boundary tests, 58 browser groups, "
          "3515 CLI cases, 52 verifiers and seven native-replayed recordings.")


if __name__=='__main__':
    main()
