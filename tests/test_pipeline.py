from dataclasses import replace
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from future.__main__ import ROOT, load_registry
from future.knowledge import Rule
from future.astrology import julian_date_ut1, run_calendar


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.registry = load_registry()
        self.addCleanup(self.registry.close)
        self.rule = Rule(**json.loads((ROOT/'knowledge/rules.json').read_text())[0])

    def test_published_examples_and_provenance(self):
        for fixture in json.loads((ROOT/'knowledge/examples.json').read_text()):
            with self.subTest(fixture=fixture['id']):
                result = run_calendar(self.registry, *fixture['inputs'])
                self.assertAlmostEqual(result['result']['julian_date_ut1'], fixture['expected_jd'], places=9)
                self.assertEqual(result['retrieved_references'][0]['source_id'], fixture['source_id'])
                self.assertEqual(result['rules_applied'][0]['version'], 1)
                self.assertIsNone(result['interpretation'])

    def test_boundaries_and_independent_date_arithmetic(self):
        from datetime import date
        for year, month, day in [(1801, 1, 1), (1900, 2, 28), (1900, 3, 1), (2000, 2, 29), (2099, 12, 31)]:
            expected = 2451544.5 + (date(year, month, day) - date(2000, 1, 1)).days
            self.assertEqual(julian_date_ut1(year, month, day, 0), expected)

    def test_bad_dates_and_time_scales_not_guessed(self):
        for values in [(1800,1,1,0), (2100,1,1,0), (1900,2,29,0), (2000,13,1,0),
                       (2000,1,1,24), (2000,1,1,-1), (2000,1,1,float('nan')),
                       (2000,1,1,float('inf')), (True,1,1,0), (2000,1,1,True)]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                julian_date_ut1(*values)

    def test_tradition_isolation_and_unverified_rules(self):
        self.registry.add_rule(replace(self.rule, id='different-school', tradition='different school'))
        self.registry.add_rule(replace(self.rule, id='candidate', status='proposed', fixture_ids=[]))
        found = self.registry.select_rules(1, 'natal', 'shared astronomical computation')
        self.assertEqual([r['id'] for r in found], [self.rule.id])
        self.assertEqual(self.registry.select_rules(1, 'electional', 'shared astronomical computation'), [])
        self.assertEqual(len(self.registry.select_rules(1, 'natal', 'different school')), 1)

    def test_rule_version_immutability(self):
        with self.assertRaises(ValueError):
            self.registry.add_rule(replace(self.rule, statement='conflicting statement'))
        self.registry.add_rule(replace(self.rule, version=2, status='proposed'))
        self.assertEqual(self.registry.select_rules(1, 'natal', self.rule.tradition)[0]['version'], 1)

    def test_unknown_source_and_missing_locator(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.registry.add_rule(replace(self.rule, id='unknown', source_id='missing'))
        with self.assertRaises(ValueError):
            replace(self.rule, locator='')

    def test_ingestion_rights_gate(self):
        path = ROOT/'knowledge/notes/usno-jd-v1.txt'
        with self.assertRaises(ValueError):
            self.registry.ingest_text('no-rights', 'hand-transits', path, 'chapter 1', content_kind='source_text')
        with self.assertRaises(ValueError):
            self.registry.ingest_text('wrong-kind', 'usno-jd', path, 'intro', content_kind='source_text')

    def test_retrieval_scope_and_empty_input(self):
        self.assertEqual(len(self.registry.search('Gregorian UT1', ['usno-jd'])), 1)
        self.assertEqual(self.registry.search('Gregorian', ['hand-transits']), [])
        self.assertEqual(self.registry.search('" OR *', []), [])
        self.assertEqual(self.registry.search('', ['usno-jd']), [])
        self.assertEqual(self.registry.search('xyzunmatched', ['usno-jd']), [])

    def test_persistent_ingestion_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory)/'knowledge.sqlite3')
            first = load_registry(path)
            first.close()
            second = load_registry(path)
            try:
                self.assertEqual(second.db.execute('SELECT count(*) FROM documents').fetchone()[0], 1)
                self.assertEqual(len(second.search('UT1', ['usno-jd'])), 1)
            finally:
                second.close()


if __name__ == '__main__':
    unittest.main()
