import json
from pathlib import Path
import unittest
from fate.build_codex import build
from future.tarot_catalog import CARDS

ROOT=Path(__file__).resolve().parents[2]


class CodexReferenceTests(unittest.TestCase):
    def test_frozen_reference_exactly_matches_native_source_edition(self):
        reference=json.loads((ROOT/'fate/web/src/codex/reference-v1.json').read_text(encoding='utf-8'))
        self.assertEqual(reference,build())
        self.assertEqual(reference['version'],'fate-codex-reference-v1')
        self.assertEqual(len(reference['tarot']['cards']),78)

    def test_all_156_source_glosses_and_rule_identities_are_preserved(self):
        reference=build()
        for identifier,card in CARDS.items():
            for orientation in ('upright','reversed'):
                saved=reference['tarot']['cards'][identifier]['meanings'][orientation]
                self.assertEqual(saved['text'],card['meanings'][orientation]['text'])
                self.assertEqual(saved['symbolic_focus'],card['meanings'][orientation]['symbolic_focus'])
                self.assertEqual(saved['rule_id'],f'tarot.waite1922.{identifier}.{orientation}')

    def test_numerology_has_only_its_two_direct_interpretation_tables(self):
        numbers=build()['numerology']
        self.assertEqual(set(numbers),{'version','expression','year','limitations'})
        self.assertEqual(set(numbers['expression']['meanings']),set(map(str,[1,2,3,4,5,6,7,8,9,11,22,33])))
        self.assertEqual(set(numbers['year']['meanings']),set(map(str,range(1,10))))


if __name__=='__main__':unittest.main()
