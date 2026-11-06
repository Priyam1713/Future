"""Independent pre-engine documentary labels, truth table and chronology oracle."""
import copy
import hashlib
import json
from pathlib import Path
from future import deja_reve as engine

ROOT = Path(__file__).resolve().parents[1]
F = json.loads((ROOT/'tests/fixtures/deja_reve_reference_v1.json').read_text(encoding='utf-8'))


def sha(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def seal(r):
    r['original']['narrative_sha256'] = hashlib.sha256(r['original']['narrative'].encode()).hexdigest()
    r['original_sha256'] = sha(r['original'])
    return r


def analysis(dream=None, **changes):
    a = copy.deepcopy(F['analysis'])
    if dream is not None:
        a['dreams'] = [dream]
        a['manifest']['payload']['candidates'][0]['original_sha256'] = dream['original_sha256']
        a['manifest']['sha256'] = sha(a['manifest']['payload'])
        a['comparisons'][0]['version_sha256'] = dream['original_sha256']
    a.update(changes)
    return a


def reject(fn):
    try:
        fn()
    except (ValueError, KeyError, TypeError):
        return
    raise AssertionError('Invalid configuration accepted')


def eq(a, b):
    assert a == b, (a, b)


def run(write=False):
    frozen = json.loads((ROOT/'data/deja-reve-fixture-freeze.json').read_text())
    eq(sha(F), frozen['fixture_sha256']); eq(engine.PROFILE_HASH, F['profile_sha256'])
    checks = {}
    for case, family in zip(F['source_cases'], F['families'][:4]):
        r = engine.reference(case['id'])
        eq(r['case']['authors_category'], case['expected'])
        assert 'Table' in r['case']['locator']
        checks[family] = 2
    counts = engine.reference()['counts']; eq(counts, F['source_counts'])
    eq(sum(counts['local_classified']), 7); eq(sum(counts['literature_classified']), 19)
    eq(7 + 19, counts['total_classified']); eq(19 + counts['literature_unclassifiable'], 35)
    # Expected values are committed table entries authored before engine code.
    for row in F['compatibility']:
        a = {**F['observation']['original']['attributes'], **row['declarations']}
        eq(engine.compatibility(a)['status'], row['expected'])
    checks['mixed-uncertain'] = len(F['compatibility'])
    for row in F['chronology']:
        eq(engine.chronology(row['lock'], row['target']), row['expected'])
    d = copy.deepcopy(F['dream']); o = F['observation']; event = F['analysis']['event']
    eq(sha(o['original']), F['known_hashes']['observation'])
    eq(sha(d['original']), F['known_hashes']['dream'])
    eq(sha(F['amendment']), F['known_hashes']['amendment'])
    eq(engine.compare_record(d, o, event)['chronology']['experience'], F['semantic_expectations']['prior_record'])
    eq(engine.compare_record(d, o, event)['chronology']['event'], F['semantic_expectations']['event_before_lock'])
    checks['original-prior-record'] = 5
    empty = analysis(dreams=[], comparisons=[])
    r = engine.evaluate(empty)
    eq(r['prior_documentary_status'], F['semantic_expectations']['no_record'])
    eq(r['candidate_ledger']['denominators']['outcomes']['missing_original'], 1)
    checks['no-prior-record'] = 2
    # Independent fixed chronology constants plus conflicting recorded assertions.
    for key, value in [('lock_at', '2026-10-31T08:00:00Z'), ('occurrence', dict(start='2026-11-02T06:00:00Z', end='2026-11-02T06:00:00Z'))]:
        z = copy.deepcopy(d); z['original'][key] = value; seal(z)
        eq(engine.compare_record(z, o, event)['chronology']['experience'], 'conflicting_evidence')
    checks['conflicting-chronology'] = len(F['chronology']) + 2
    d['amendments'].append(copy.deepcopy(F['amendment'])); engine.validate_record(d)
    r = engine.compare_record(d, o, event)
    eq(r['versions'][0]['narrative'], F['dream']['original']['narrative'])
    eq(r['versions'][1]['chronology']['experience'], F['semantic_expectations']['amendment_after_experience'])
    eq(r['chronology']['experience'], 'strictly_earlier')
    bad = copy.deepcopy(d); bad['amendments'][0]['parent_sha256'] = '0'*64
    reject(lambda: engine.validate_record(bad))
    bad = copy.deepcopy(d); bad['amendments'][0]['at'] = '2026-10-30T00:00:00Z'
    reject(lambda: engine.validate_record(bad))
    checks['original-versus-amendment'] = 5
    a = copy.deepcopy(o['original']['attributes']); a.update(dream_association=False, specific_recollection=False, temporal_context='none')
    eq(engine.compatibility(a)['status'], 'unsupported')
    a['subjective_confidence'] = 'Absolutely certain'; eq(engine.compatibility(a)['status'], 'unsupported')
    checks['generic-familiarity-negative-control'] = 2
    a = copy.deepcopy(o['original']['attributes']); a['temporal_context'] = 'vague'
    eq(engine.compatibility(a)['status'], 'unclassifiable')
    a['temporal_context'] = 'specific'; eq(engine.compatibility(a)['status'], 'episodic_like_compatible')
    checks['specific-versus-vague'] = 2
    a = analysis(); a['comparisons'][0]['status'] = 'nonmatch'
    eq(engine.evaluate(a)['candidate_ledger']['denominators']['outcomes']['nonmatch'], 1)
    checks['manual-nonmatch'] = 1
    # Complete finite ledger: all four manual statuses, unreviewed, excluded,
    # missing original and a distinct later search with its own denominator.
    a = analysis(); a['dreams'] = []; a['manifest']['payload']['candidates'] = []; a['comparisons'] = []
    for i, status in enumerate(['match', 'nonmatch', 'insufficient_information', 'unscorable', 'unreviewed', 'excluded', 'missing_original']):
        z = copy.deepcopy(F['dream']); z['original']['id'] = 'dream'+str(i); seal(z)
        c = dict(dream_id=z['original']['id'], original_sha256=z['original_sha256'], disposition='excluded' if status == 'excluded' else 'included', reason='Synthetic finite ledger control')
        a['manifest']['payload']['candidates'].append(c)
        if status != 'missing_original': a['dreams'].append(z)
        if i < 4:
            v = copy.deepcopy(F['analysis']['comparisons'][0]); v.update(dream_id=z['original']['id'], version_sha256=z['original_sha256'], status=status); a['comparisons'].append(v)
    a['manifest']['sha256'] = sha(a['manifest']['payload'])
    a['post_hoc'] = [{k: copy.deepcopy(F['analysis'][k]) for k in ('manifest', 'dreams', 'comparisons')}]
    a['post_hoc'][0]['manifest']['payload']['frozen_at'] = '2026-11-04T11:45:00Z'
    a['post_hoc'][0]['manifest']['sha256'] = sha(a['post_hoc'][0]['manifest']['payload'])
    r = engine.evaluate(a); eq(r['candidate_ledger']['denominators']['candidates'], 7)
    eq(list(r['candidate_ledger']['denominators']['outcomes'].values()), [1]*7)
    eq(r['post_hoc_searches'][0]['denominators']['candidates'], 1)
    eq(r['post_hoc_searches'][0]['post_hoc'], True)
    checks['multiple-candidates'] = 10
    for key in ('first_record_at', 'lock_at'):
        z = copy.deepcopy(F['dream']); z['original'][key] = None; seal(z)
        eq(engine.compare_record(z, o, event)['chronology']['experience'], 'unknown')
    z = copy.deepcopy(F['dream']); z['original']['occurrence'] = None; seal(z)
    eq(engine.compare_record(z, o, event)['chronology']['experience'], 'strictly_earlier')
    checks['missing-original-time'] = 3
    for task in ('diagnose', 'predict', 'verify-memory', 'localize-brain', 'export'):
        reject(lambda: engine.read(dict(schema_version=1, task=task)))
    checks['no-diagnosis-prediction'] = 5
    q = dict(schema_version=1, task='report', analysis=F['analysis'])
    r = engine.read(q); eq(r, engine.read(q))
    eq(r['result']['analysis']['observation']['original']['narrative'].encode(), o['original']['narrative'].encode())
    eq(r['report_sha256'], sha({k:v for k,v in r.items() if k != 'report_sha256'}))
    bad = copy.deepcopy(o); bad['original']['consent']['export'] = True; seal(bad)
    reject(lambda: engine.validate_record(bad))
    bad = copy.deepcopy(o); bad['original']['narrative'] += 'changed'
    reject(lambda: engine.validate_record(bad))
    ref = engine.reference(); assert '1927' in ref['dunne_boundary'] and 'CC BY-NC-ND' in ref['rights']
    checks['source-edition-rights-replay'] = 7
    eq(set(checks), set(F['families']))
    out = dict(passed=True, fixture_sha256=sha(F), profile_sha256=engine.PROFILE_HASH, fixture_commit='2ee614e',
               families=[dict(id=k, passed=True, checks=checks[k]) for k in F['families']], category_cases=len(F['compatibility']),
               chronology_constants=len(F['chronology']), source_case_checks=4, source_counts_verified=True,
               empirical_or_clinical_validation=False, method='Pre-engine known-answer tables and constants;independent canonical SHA256;no expected values generated by production.')
    if write: (ROOT/'data/deja-reve-verification.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    return out


if __name__ == '__main__':
    print(json.dumps(run(write=True), indent=2))
