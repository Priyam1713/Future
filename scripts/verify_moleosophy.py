"""Compare independent pre-matcher transcription fixtures to documentary lookup."""
import json
from pathlib import Path
from future.moleosophy import PROFILE,reference


def run():
    f=json.loads(Path('tests/fixtures/moleosophy_fontaine_examples.json').read_text(encoding='utf-8'));cases=[]
    for region,side,location,key,label,pages in f['cases']:
        r=reference(dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',
            orientation=dict(frame='subject',view='frontal',mirrored=False),
            selections=[dict(region_id=region,side=side,location_id=location)]))['results'][0]
        actual=r['entry']
        assert r['status']=='resolved' and (actual['id'],actual['original_label'],actual['printed_pages'])==(key,label,pages)
        assert actual['source_id']==f['source_id'] and not actual['applied_to_individual']
        cases.append(dict(region_id=region,side=side,location_id=location,expected_entry=key,expected_pages=pages,
            actual_entry=actual['id'],actual_locator=actual['locator'],passed=True))
    report=dict(profile=PROFILE,source_id=f['source_id'],method=f['method'],cases=cases,passed=True,
        limits=f['limits'],empirical_or_individual_judgment_validated=False)
    Path('data/moleosophy-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'independent original-page entry/side/locator cases passed')


if __name__=='__main__':run()
