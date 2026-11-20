"""Bind Block 10 browser media and privacy proof to independently replayed native results."""

import hashlib
import json
import re
import subprocess

from future import remote_viewing

from .futures import ROOT, MODULES, StudyInput, native_request, read
from .record_manuscript import log_text


FATE = ROOT/'fate'
EVIDENCE = FATE/'evidence'
BASE = '0461d9a'
ROOMS = dict(zip([24,26,43,44,45,46,*range(49,61)],(
    'automatic-writing','akashic','remote-viewing','prophetic-dreams','intuitive-prediction','deja-reve',
    'forecast-models','quantum-circuit','forecast-updates','population-dynamics','digital-twin',
    'cellular-automata','intention-classifier','causal-graphs','collective-forecasts',
    'prediction-market','lorenz-chaos','scenario-trees',
)))


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def index(files):
    return {p.relative_to(FATE).as_posix():sha(p) for p in files}


def regression():
    counts={'unit':2522,'workbench':77,'fate':77}
    for name,n in counts.items():
        log=log_text(ROOT/'tmp'/f'block10-{name}.log')
        assert re.search(rf'^Ran {n} tests\b',log,re.M) and re.search(r'^OK$',log,re.M), name
    node=log_text(ROOT/'tmp/block10-node.log')
    assert 'pass 27' in node and 'fail 0' in node
    counts['codex_node']=27
    browsers={}
    for key,pre,n in (('fate','',98),('workbench','workbench-',9)):
        value=load(FATE/f'{pre}browser-acceptance.json')['stats']
        assert value['expected']==n and value['unexpected']==value['skipped']==value['flaky']==0,value
        browsers[key]=value
    cli=load(FATE/'inherited-cli-acceptance.json')
    assert cli['complete'] and cli['passed'] and not cli['changed_protected_files']
    assert (cli['cli_cases'],cli['independent_verifiers'],cli['protected_count'])==(3515,52,576)
    subprocess.run(['git','-c','core.safecrlf=false','diff','--exit-code',BASE,'--',
                    'future','knowledge','resources','tests','workbench','data'],cwd=ROOT,check=True)
    assert 'No broken requirements found.' in log_text(ROOT/'tmp/block10-pip.log')
    assert '60 IDs and six exclusions pass' in log_text(ROOT/'tmp/block10-inventory.log')
    assert load(ROOT/'tmp/block10-npm-audit.json')['metadata']['vulnerabilities']['total']==0
    return counts,browsers,{key:cli[key] for key in ('cli_cases','independent_verifiers','protected_count')}


def verify_trial(report):
    r=remote_viewing.report(report['trial'])
    assert r==report and r['commitment_verified'] and r['revealed'] and r['viewer_lock'] and r['judge_lock']


def artifacts():
    native=load(EVIDENCE/'block10-native.json')['reports']
    profiles=load(EVIDENCE/'block10-performance.json')['profiles']
    assert {int(key) for key in native}==set(ROOMS)
    assert {(r['oracle'],r['mode']) for r in profiles}=={(i,m) for i in ROOMS for m in ('mobile','desktop')}
    out={}
    for oracle,slug in ROOMS.items():
        observed=native[str(oracle)]
        if oracle==43:
            verify_trial(observed['result'])
        else:
            q=StudyInput(**observed['wire'])
            request=native_request(q,lambda:0)
            assert observed['request']==json.loads(json.dumps(request)),slug
            expected=MODULES[oracle].read(request)
            assert observed['result']==json.loads(json.dumps(expected)),slug
        paths=[FATE/'screenshots'/f'10-{slug}-{size}.png' for size in ('mobile','desktop')]
        if oracle in (24,43,49,50):
            paths.extend(FATE/'screenshots'/f'10-{slug}-entrance-{size}.png' for size in ('mobile','desktop'))
        out[slug]=dict(oracle=oracle,exact_native_parity=True,media=index(paths))
    blind=load(EVIDENCE/'block10-blind-browser.json')
    verify_trial(blind['report'])
    assert blind['phases']==['viewing','judging','judging','revealed']
    assert not set(blind['packetFields']+blind['judgePacketFields']) & {'trial','nonce','actual_target_id','selection','preimage'}
    dream=load(EVIDENCE/'block10-dream-browser.json')
    assert dream['phase']=='awaiting' and dream['futureObservationStatus']==422 and not dream['anticipatedResultsShown']
    privacy=load(EVIDENCE/'block10-privacy-browser.json')
    assert not privacy['reopenPostRequests']
    snapshot=privacy['stored']['chapters'][0]['snapshot']
    assert snapshot==privacy['exported']['chapters'][0]['snapshot']==dict(oracle=54,profile='fate-future-studies-v1',option=4)
    history=load(EVIDENCE/'block10-historical.json')
    historical=read(StudyInput(**history['request']),lambda:0)
    assert historical['result']['report_sha256']==history['reportHash'] and historical['view']==history['view']
    recordings=load(EVIDENCE/'block10-recordings.json')['recordings']
    assert set(recordings)=={'viewer','judge','dream','quantum-circuit','cellular-automata'}
    assert recordings['viewer']['commitment']==recordings['judge']['commitment']
    assert recordings['dream']['phase']=='awaiting'
    for name,r in recordings.items():
        stream=r['media']['streams'][0]
        assert (stream['codec_name'],stream['width'],stream['height'])==('h264',390,844)
        assert float(r['media']['format']['duration'])>=3
    extra=[FATE/'screenshots/10-noaa-evaluation-desktop.png']
    extra.extend(EVIDENCE/f'block10-{name}.mp4' for name in recordings)
    extra.extend(EVIDENCE/f'block10-{name}.json' for name in ('native','performance','historical','recordings',
                                                              'dream-browser','blind-browser','privacy-browser'))
    return out,profiles,extra


def main():
    counts,browsers,cli=regression()
    rooms,profiles,media=artifacts()
    art=FATE/'design/block10-artwork.json'
    artwork=load(art)
    assert {s['id'] for s in artwork['environments']}=={'dream','tomorrow'}
    for row in [*artwork['environments'],artwork['plates']]:
        assert all(sha(ROOT/path)==digest for path,digest in row['files'].items())
    methods=load(FATE/'web/src/gallery/inventory.json')['methods']
    assert len(methods)==54 and all(m['status']=='available' for m in methods)
    assert [m['id'] for m in methods]==load(FATE/'experience.json')['technique_ids']
    media.extend([art,FATE/'browser-acceptance.json',FATE/'workbench-browser-acceptance.json',
                  FATE/'inherited-cli-acceptance.json'])
    out=dict(block=10,baseline=BASE,open_rooms=54,rooms=rooms,unit_tests=counts,browsers=browsers,cli=cli,
             performance_profiles=profiles,evidence=index(media),limits=[
                 'Demo inputs are synthetic except the separate retrospective NOAA benchmark.',
                 'Blind workflow uses separate browser profiles and one trial. Independence of people is a declaration.',
                 'Prospective sessions remain in server memory. Browser evidence stops at an authentic pending state.',
                 'Browser timings are local emulation with frame callback intervals, not physical device measurements.',
             ])
    (EVIDENCE/'block10-acceptance.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(f'Block 10 verified: 18 new rooms, {sum(counts.values())} unit tests, 107 browser tests, 3515 CLI cases, 52 verifiers.')


if __name__=='__main__':
    main()
