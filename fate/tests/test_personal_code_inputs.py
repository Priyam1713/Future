from datetime import date
import unittest

from future.numerology import calculate


class PersonalCodeInputs(unittest.TestCase):
    def test_all_name_values_and_master_parts(self):
        for value in (*range(1, 10), 11, 22, 33):
            vowel = calculate("2000-01-08", "A" * value, "birth", "2026-01-01")
            consonant = calculate("2000-01-08", "J" * value, "current", "2026-01-01")
            self.assertEqual((vowel["expression"]["result"], vowel["soul_urge"]["result"]), (value, value))
            self.assertEqual((consonant["expression"]["result"], consonant["personality"]["result"]), (value, value))
            self.assertIsNone(vowel["personality"]["result"])
            self.assertIsNone(consonant["soul_urge"]["result"])
        combined = calculate("2009-11-11", "A" * 11 + " " + "J" * 22, "birth", "2026-01-01")
        self.assertEqual(combined["expression"]["result"], 33)
        self.assertEqual(combined["life_path"]["result"], 33)
        for birth, value in (("2000-01-08", 11), ("2000-11-09", 22)):
            self.assertEqual(calculate(birth, "A", "birth", "2026-01-01")["life_path"]["result"], value)

    def test_birthdays_and_calendar_cycles_against_independent_values(self):
        companions = (1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 11, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 22, 5, 6, 7, 8, 9, 1, 11, 3, 4)
        for day, companion in enumerate(companions, 1):
            result = calculate(f"2000-01-{day:02}", "A", "birth", "2026-01-01")
            self.assertEqual(result["birthday"]["original_day"], day)
            self.assertEqual(result["birthday"]["companion"]["result"], companion)
        years = set()
        for target in (*[f"{year}-01-01" for year in range(2020, 2029)],
                       "2024-02-28", "2024-02-29", "2024-03-01", "2026-12-31", "2027-01-01"):
            selected = date.fromisoformat(target)
            result = calculate("2000-02-29", "A-J O'Neil", "birth", target)
            total = 2 + 29 + selected.year
            expected = tuple(1 + (value - 1) % 9 for value in
                             (total, total + selected.month, total + selected.month + selected.day))
            self.assertEqual(tuple(result["cycles"][key]["result"] for key in ("year", "month", "day")), expected)
            self.assertEqual(result["cycles"]["year_interval"],
                             [f"{selected.year}-01-01", f"{selected.year + 1}-01-01"])
            years.add(expected[0])
        self.assertEqual(years, set(range(1, 10)))
        for birth, target, expected in (
            ("2000-05-05", "2026-11-01", (2, 4, 5)),
            ("2000-05-05", "2026-12-31", (2, 5, 9)),
            ("2000-05-05", "2027-01-31", (3, 4, 8)),
            ("2000-05-05", "2027-02-01", (3, 5, 6)),
            ("2000-09-12", "2026-10-12", (4, 5, 8)),
        ):
            result = calculate(birth, "A", "birth", target)
            self.assertEqual(tuple(result["cycles"][key]["result"] for key in ("year", "month", "day")), expected)

    def test_name_forms_and_explicit_y_roles(self):
        inputs = ("1996-03-19", "Y-A O'Y", "current", "2026-02-17")
        result = calculate(*inputs, "vc")
        self.assertEqual(result["name"]["original"], inputs[1])
        self.assertEqual([p["part"] for p in result["name"]["tokens"]], ["Y-A", "O'Y"])
        self.assertEqual([letter["vowel"] for part in result["name"]["tokens"]
                          for letter in part["letters"] if letter["letter"] == "Y"], [True, False])
        self.assertNotEqual(calculate(*inputs, "cv")["soul_urge"], result["soul_urge"])
        for invalid in ("Éloise", "山田", " A", "A—B", "A--B"):
            with self.assertRaises(ValueError):
                calculate(inputs[0], invalid, "birth", inputs[3])
        with self.assertRaises(ValueError):
            calculate(*inputs, "v")
