"""Source-fidelity check against independently transcribed historic illustrated details."""
import json
from pathlib import Path
from future.palmistry import read,PROFILE,DATA


def run():
    fixture=json.loads(Path('tests/fixtures/palmistry_cheiro_examples.json').read_text())
    rows=[]
    for case in fixture['cases']:
        observation=dict(schema_version=1,profile=PROFILE,hands=[dict(side='right',**case['observation'])])
        result=read(observation)
        actual=sorted(r['id'] for h in result['hands'] for r in h['readings'])
        expected=sorted(case['expected_ids'])
        assert actual==expected,(case['id'],actual,expected)
        rows.append(dict(case_id=case['id'],kind=case['kind'],locator=case['locator'],
                         observation=case['observation'],expected_rules=expected,actual_rules=actual,
                         expected_theme=case['expected_theme'],passed=True))
    report=dict(profile=PROFILE,source_id=DATA['source']['id'],source_scan_sha256=fixture['scan_sha256'],
        verification_scope=fixture['method'],cases=rows,passed=True,
        limits=['Published schematic/type illustrations,not whole-person acceptance charts.',
                'Manual transcription and rule-selection checks do not validate photo extraction.',
                'Agreement with a historical source does not establish personality or predictive validity.'])
    Path('data/palmistry-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(len(rows),'independently transcribed illustrated source cases passed')

if __name__=='__main__':run()
