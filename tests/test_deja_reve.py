"""Behavior and rejection tests for the bounded private documentary workbench."""
import copy
import json
import re
import unittest
from pathlib import Path
from future import deja_reve as d
from future.knowledge import Registry
from scripts.verify_deja_reve import F, analysis, seal, sha, run


def req(task, **kw):
    return dict(schema_version=1, task=task, **kw)


class DejaReve(unittest.TestCase):
    def test_preengine_oracle(self):
        self.assertTrue(run()['passed'])

    def test_reference_without_observation(self):
        self.assertEqual(d.read(req('reference'))['visibility'], 'public_reference')

    def test_private_report_carries_documentary_source_metadata(self):
        r = d.read(req('report', analysis=F['analysis']))
        self.assertIn('875', r['source_reference']['edition'])
        self.assertEqual([c['authors_category'] for c in r['source_reference']['cases']],
                         ['episodic-like', 'familiarity-like', 'dreamy-state', 'unclassifiable'])

    def test_raw_text_never_supplies_declarations(self):
        r = copy.deepcopy(F['observation'])
        r['original']['attributes'].update(dream_association=False, specific_recollection=False, temporal_context='none')
        r['original']['narrative'] = 'specific prior dream yesterday hospital orange room diagnose epilepsy'
        seal(r)
        self.assertEqual(d.read(req('annotate', record=r))['result']['compatibility']['status'], 'unsupported')

    def test_original_and_amendment_lifecycle(self):
        r = d.read(req('record', record=F['dream']))['result']['record']
        r = d.read(req('amend', record=r, amendment=F['amendment']))['result']['record']
        self.assertEqual(r['original'], F['dream']['original'])
        a = analysis(r)
        a['comparisons'][0].update(version_sha256=sha(F['amendment']), at='2026-11-06T00:00:00Z')
        e = d.evaluate(a)['candidate_ledger']['candidates'][0]
        self.assertEqual(e['provenance']['versions'][1]['chronology']['experience'], 'later')
        self.assertEqual(e['comparisons'][0]['version_sha256'], sha(F['amendment']))

    def test_candidate_freeze_and_append(self):
        m = d.read(req('freeze-candidates', manifest=F['analysis']['manifest']))['result']
        a = analysis(manifest=m, comparisons=[])
        r = d.read(req('link-dream', analysis=a, comparison=F['analysis']['comparisons'][0]))
        self.assertEqual(r['result']['evaluation']['candidate_ledger']['denominators']['comparison_attempts'], 1)
        self.assertEqual(a['comparisons'], [])

    def test_private_and_rejected_markdown_replay(self):
        r = d.read(req('report', analysis=F['analysis']))
        raw = d.markdown(r)
        self.assertEqual(json.loads(re.search(r'(`{3,})json\n(.*?)\n\1', raw, re.S)[2]), r)
        r = dict(status='rejected', result=None)
        self.assertIn('rejected', d.markdown(r))

    def test_fence_injection_preserves_unicode_bytes(self):
        r = copy.deepcopy(F['observation']); r['original']['narrative'] += '\n``````json\n<script>x</script>'
        seal(r); out = d.read(req('annotate', record=r)); raw = d.markdown(out)
        self.assertIn('```````json', raw)
        self.assertEqual(json.loads(re.search(r'(`{7})json\n(.*?)\n\1', raw, re.S)[2]), out)

    def test_registry_idempotence(self):
        reg = Registry(':memory:')
        try:
            for _ in range(2): d.read(req('reference'), reg)
        finally: reg.close()

    def test_interval_to_event_uses_entire_interval(self):
        self.assertEqual(d.interval_relation(dict(start='2026-11-01T00:00:00Z', end='2026-11-03T00:00:00Z'),
                                             dict(start='2026-11-02T00:00:00Z', end='2026-11-02T00:00:00Z')), 'overlapping_or_ambiguous')

    def test_unknown_and_late_do_not_claim_earlier_record(self):
        for time in (None, '2026-11-04T10:00:00Z', '2026-11-05T00:00:00Z'):
            r = copy.deepcopy(F['dream']); r['original']['lock_at'] = time; seal(r)
            self.assertEqual(d.evaluate(analysis(r))['prior_documentary_status'], F['semantic_expectations']['no_record'])

    def test_proposal_preserved_separately(self):
        r = copy.deepcopy(F['observation']); r['original']['attributes']['proposal'] = 'dreamy-state'; seal(r)
        e = d.read(req('annotate', record=r))['result']['compatibility']
        self.assertEqual(e['status'], 'episodic_like_compatible'); self.assertTrue(e['proposal_disagrees'])


def invalid_records():
    out = {}
    mutations = [('hash', lambda r: r.update(original_sha256='0'*64)),
        ('bytes', lambda r: r['original'].update(narrative='changed')),
        ('version', lambda r: r['original'].update(profile_version=True)),
        ('profile', lambda r: r['original'].update(profile='other')),
        ('kind', lambda r: r['original'].update(kind='clinical-diagnosis')),
        ('extra', lambda r: r['original'].update(diagnosis='epilepsy')),
        ('naive-time', lambda r: r['original'].update(first_record_at='2026-11-04T00:00:00')),
        ('boolean-time', lambda r: r['original'].update(lock_at=True)),
        ('reversed-time', lambda r: r['original'].update(occurrence=dict(start='2026-11-05T00:00:00Z', end='2026-11-04T00:00:00Z'))),
        ('export', lambda r: r['original']['consent'].update(export=True)),
        ('no-consent', lambda r: r['original']['consent'].update(local_processing=False)),
        ('no-rights', lambda r: r['original']['consent'].update(rights='unknown')),
        ('boolean-flag', lambda r: r['original']['attributes'].update(dream_association=1)),
        ('temporal-enum', lambda r: r['original']['attributes'].update(temporal_context='exact_verified')),
        ('proposal-enum', lambda r: r['original']['attributes'].update(proposal='brain-localized')),
        ('context-enum', lambda r: r['original'].update(context='epilepsy_detected')),
        ('empty-source', lambda r: r['original'].update(source_ref='')),
        ('no-reviewer', lambda r: r['original']['attributes'].update(reviewer=''))]
    for name, mutation in mutations:
        r = copy.deepcopy(F['observation']); mutation(r)
        if name not in ('hash', 'bytes'): seal(r)
        out[name] = r
    return out


for name, value in invalid_records().items():
    def test(self, value=value):
        with self.assertRaises(ValueError): d.validate_record(value)
    setattr(DejaReve, 'test_reject_'+name.replace('-', '_'), test)


def invalid_analyses():
    cases = {}
    a = analysis(); a['manifest']['sha256'] = '0'*64; cases['manifest-hash'] = a
    a = analysis(); a['dreams'][0]['original_sha256'] = '0'*64; cases['record-hash'] = a
    a = analysis(); a['comparisons'][0]['version_sha256'] = '0'*64; cases['version-hash'] = a
    a = analysis(); a['comparisons'][0]['dream_id'] = 'outside'; cases['outside-candidate'] = a
    a = analysis(); a['comparisons'][0]['at'] = '2026-11-04T10:00:00Z'; cases['prefreeze-comparison'] = a
    a = analysis(); a['comparisons'][0]['status'] = 'verified-memory'; cases['manual-enum'] = a
    a = analysis(); a['manifest']['payload']['candidates'] *= 2; a['manifest']['sha256'] = sha(a['manifest']['payload']); cases['duplicate-candidate'] = a
    a = analysis(); a['manifest']['payload']['candidates'][0]['disposition'] = 'excluded'; a['manifest']['sha256'] = sha(a['manifest']['payload']); cases['excluded-comparison'] = a
    a = analysis(); a['dreams'] *= 2; cases['duplicate-record'] = a
    a = analysis(); a['event']['evidence_sha256'] = 'bad'; cases['event-hash'] = a
    a = analysis(); a['event']['occurrence']['start'] = '2026-11-04T00:00:00'; cases['event-timezone'] = a
    a = analysis(); a['comparisons'].append(copy.deepcopy(a['comparisons'][0])); a['comparisons'][-1]['at'] = '2026-11-04T11:45:00Z'; cases['backdated-comparison'] = a
    a = analysis(); g = {k: copy.deepcopy(a[k]) for k in ('manifest', 'dreams', 'comparisons')}
    g['dreams'][0]['original']['narrative'] += 'rewritten root'; seal(g['dreams'][0])
    g['manifest']['payload']['candidates'][0]['original_sha256'] = g['dreams'][0]['original_sha256']
    g['manifest']['sha256'] = sha(g['manifest']['payload'])
    g['comparisons'][0]['version_sha256'] = g['dreams'][0]['original_sha256']
    a['post_hoc'] = [g]; cases['conflicting-posthoc-original'] = a
    return cases


for name, value in invalid_analyses().items():
    def test(self, value=value):
        with self.assertRaises(ValueError): d.evaluate(value)
    setattr(DejaReve, 'test_reject_'+name.replace('-', '_'), test)


if __name__ == '__main__': unittest.main()
