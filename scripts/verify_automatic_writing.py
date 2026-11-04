"""Compare frozen pre-engine facts and synthetic known answers; no runtime-derived fixture creation."""
import json
from pathlib import Path
from future import automatic_writing as a
from tests.test_automatic_writing import base, log


def run():
    ref=json.loads(Path('tests/fixtures/automatic_writing_reference.json').read_text(encoding='utf-8'))
    counts={}
    for expected,actual in zip(ref['rules'],a.DATA['rules']):
        assert actual['id']=='automatic.breton.'+expected['id'] and actual['statement']==expected['meaning']
        assert actual['source_id']==ref['source_id'] and 'p4' in actual['locator']
    assert len(a.DATA['rules'])==len(ref['rules'])==7
    counts['historical_facts']=7
    for row in ref['metrics']:
        assert ''.join(row['segments'])==row['draft']
        actual=a.metrics(row['draft'])
        assert [actual[k] for k in ('unicode_code_points','words','lines')]==[row['code_points'],row['words'],row['lines']]
    counts['independent_metric_vectors']=len(ref['metrics'])
    for row in ref['transitions']:
        assert a.read(base(log(row['events']),row['state']))['session']['state']==row['state']
    counts['pre_engine_valid_sequences']=len(ref['transitions'])
    for kinds in ref['invalid']:
        try:a.read(base(log(kinds)))
        except ValueError:pass
        else:raise AssertionError('Invalid transition accepted')
    counts['pre_engine_invalid_sequences']=len(ref['invalid'])
    row=ref['duration'];assert a.interval(row['start'],row['stop'])['seconds']==row['seconds']
    counts['independent_duration']=1
    e=log(['begin','append','append','stop','review','revise','revise']);e[2]['segment']['text']='two'
    for event,row in zip(e[5:],ref['revisions']['rows']):event['revision']=row|dict(authorship='user')
    report=a.read(base(e,'under_review'))
    assert report['first_draft']['text']==ref['revisions']['first_draft']
    assert [r['record']['parent'] for r in report['revisions']]==['first_draft','r1']
    counts['independent_revision_checks']=2
    assert 'not authenticated' in a.DATA['source']['edition']
    assert 'Moses' in a.DATA['limits'][1] and a.DATA['source']['ingestion']=='facts_only'
    counts['source_isolation_and_rights']=3
    result=dict(passed=True,checks=sum(counts.values()),counts=counts,
                assurance='Institutional French-subset source fidelity and synthetic pre-engine workflow/metric references; not empirical authorship or mental-state validation.')
    Path('data/automatic-writing-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['checks'],'Automatic Writing reference checks passed')


if __name__=='__main__':run()
