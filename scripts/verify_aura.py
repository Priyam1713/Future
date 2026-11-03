"""Reproducible documentary checks against separately transcribed primary fixtures."""
import json
from pathlib import Path
from future.aura import PROFILE,reference


def run():
    fixtures=json.loads(Path('tests/fixtures/aura_source_examples.json').read_text(encoding='utf-8'))
    results=[]
    for color,row,column,label in fixtures['key_cases']:
        r=reference(dict(schema_version=1,profile=PROFILE,task='symbolic_reference',mode='manual',components=[dict(color=color)]))
        t=r['components'][0]['reference'];expected=dict(row=row,column=column,label=label)
        assert t['key']==expected and t['source_id']==fixtures['source_id'],color
        results.append(dict(case=color,expected=expected,actual=t['key'],passed=True))
    for key,figure,title,colors,section in fixtures['figure_cases']:
        r=reference(dict(schema_version=1,profile=PROFILE,task='symbolic_reference',mode='source_example',example_id=key));e=r['source_example']
        assert [e['figure'],e['title'],e['colors']]==[figure,title,colors] and section in e['locator']
        results.append(dict(case=key,figure=figure,title=title,colors=colors,passed=True))
    output=dict(profile=PROFILE,source_id=fixtures['source_id'],method=fixtures['method'],checks=results,
        passed=len(results),empirical_validation=False,limitations='Same primary edition,independent manual transcription;not independent confirmation of clairvoyant claims or color fidelity.')
    Path('data/aura-verification.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(len(results),'original-source documentary checks passed')


if __name__=='__main__':run()
