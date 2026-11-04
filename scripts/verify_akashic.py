"""Independent pre-engine source/structure and question/workflow known answers."""
import json
from pathlib import Path
from future import akashic as a


def run():
    ref=json.loads(Path('tests/fixtures/akashic_reference.json').read_text(encoding='utf-8'));counts={}
    assert len(a.CONCEPTS)==len(ref['definitions'])==10
    for key,row in ref['source_locations'].items():
        actual=a.lookup(key)['reference'];p=actual['provenance']
        assert p['locator']==row['locator'] and p['source_id']=='akashic-howe-public-'+row['source_key']+'-facts-v2'
        assert actual['description']==ref['definitions'][key]
    counts.update(concept_locators=10,concept_definitions=10)
    p=a.DATA['procedure']
    assert p['opening']['silent_stanza_repetitions']==ref['procedure']['silent_stanza_repetitions']
    assert p['closing']['declaration_repetitions']==ref['procedure']['closing_declaration_repetitions']
    assert not p['prayer_reproduced'] and list(p).index('opening')<list(p).index('closing')
    counts['procedure_structure']=4
    base=dict(schema_version=1,profile=a.PROFILE,task='reference_reflection',mode='manual')
    for row in ref['purposes']:
        r=a.read(base|dict(question=dict(purpose=row['purpose'])))
        assert r['question']['status']==row['status'] and r['guidance']['purpose_reference_ids']==row['reference_ids']
        assert r['question']['answer'] is None
    counts['purpose_known_answers']=len(ref['purposes'])
    for form,status in ref['question_forms'].items():
        assert a.read(base|dict(question=dict(form=form)))['question']['form_guidance']==status
    counts['explicit_question_forms']=len(ref['question_forms'])
    for ids in ref['stage_sequences']['valid']:
        a.read(base|dict(session=dict(state='in_progress',stages=[dict(id=k,status='skipped') for k in ids])))
    for ids in ref['stage_sequences']['invalid']:
        try:a.read(base|dict(session=dict(stages=[dict(id=k) for k in ids])))
        except ValueError:pass
        else:raise AssertionError('Invalid stage sequence accepted')
    counts['stage_sequences']=5
    for key in ref['unsupported_concepts']:assert a.lookup(key)['reference'] is None
    counts['unsupported_concepts']=3
    for profile in ref['unsupported_profiles']:
        try:a.read(base|dict(profile=profile))
        except ValueError:pass
        else:raise AssertionError('Unsupported tradition accepted')
    counts['tradition_isolation']=3
    assert all(s['ingestion']=='facts_only' for s in a.DATA['sources'])
    assert 'book' in a.DATA['edition_boundary'] and 'Earlier editions' in a.DATA['edition_boundary']
    counts['rights_and_edition_boundaries']=2
    result=dict(passed=True,checks=sum(counts.values()),counts=counts,
        assurance='Original public-source attribution/structure and synthetic independent workflow fixtures;not evidence of metaphysical archives or extraordinary abilities.')
    Path('data/akashic-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['checks'],'Akashic independent reference checks passed')


if __name__=='__main__':run()
