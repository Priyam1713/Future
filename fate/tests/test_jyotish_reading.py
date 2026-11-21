from copy import deepcopy
from datetime import datetime, timedelta, timezone
from unittest import TestCase

from fate.chambers import VedicInput, read, snapshot
from fate.jyotish_reading import reading
from fate.western import WesternService
from future.vedic import d1, nakshatra
from future.vedic_timing import enrich, vimshottari


class JyotishReadingTests(TestCase):
    def setUp(self):
        self.service = WesternService()
        self.addCleanup(self.service.close)
        self.request = VedicInput(oracle=2, local="1990-07-15T14:30", zone="Europe/London",
                                  latitude=51.50853, longitude=-0.12574, target="2026-11-21")

    def test_native_replay_and_reading_provenance(self):
        native = read(self.request, self.service)
        expected = enrich(d1(self.service.get_ephemeris(), *self.request.args()),
                          datetime(2026, 11, 21, tzinfo=timezone.utc), self.request.year_key, True)
        self.assertEqual(native, expected)
        original = deepcopy(native)
        consumer = reading(native)
        self.assertEqual(native, original)
        self.assertEqual(consumer["lagna_lord"], native["planets"]["Moon"]["sign_ruler"]
                         if native["planets"]["Moon"]["sign"] == native["ascendant"]["sign"] else
                         next(body for body, row in native["planets"].items() if 1 in row["rules_houses"]))
        self.assertTrue(all(set(row["rule_ids"]) <= consumer["sources"].keys()
                            for row in consumer["chapters"]))
        for body, row in consumer["grahas"].items():
            self.assertEqual(row["d1"]["rules_houses"], native["planets"][body]["rules_houses"])
            self.assertEqual(row["d9"]["dignities"], native["d9"]["planets"][body]["sign_dignities"])
            for contact in row["contacts"]:
                self.assertEqual({key: value for key, value in contact.items() if key != "index"},
                                 native["graha_aspects"][contact["index"]])
        self.assertTrue(consumer["grahas"]["Rahu"]["nodal"])
        self.assertFalse(consumer["grahas"]["Rahu"]["d1"]["dignities"])
        self.assertNotIn("birth", consumer)
        self.assertNotIn("latitude", consumer)
        self.assertEqual(len(snapshot(native)["sub"]), 9)

    def test_half_open_boundaries_conventions_and_birth_sensitivity(self):
        start = datetime(1990, 7, 15, tzinfo=timezone.utc)
        self.assertEqual(nakshatra(40 / 3)["index"], 1)
        self.assertEqual(nakshatra(10 / 3)["pada"], 2)
        self.assertEqual(nakshatra(10 / 3 - 1e-6)["pada"], 1)
        base = vimshottari(start, 0, start)
        boundary = datetime.fromisoformat(base["current"]["antardasha"]["end_exclusive_utc"])
        before = vimshottari(start, 0, boundary - timedelta(microseconds=1))
        after = vimshottari(start, 0, boundary)
        self.assertNotEqual(before["current"]["antardasha"]["lord"], after["current"]["antardasha"]["lord"])
        self.assertEqual(after["current"]["antardasha"]["start_inclusive_utc"], boundary.isoformat())
        solar = vimshottari(start, 0, boundary, "solar-365.2425")
        self.assertNotEqual(solar["current"]["antardasha"]["lord"], after["current"]["antardasha"]["lord"])
        a = read(self.request, self.service)
        changed = self.request.model_copy(update={"local": "1990-07-15T15:00"})
        b = read(changed, self.service)
        self.assertNotEqual(a["d9"]["ascendant"], b["d9"]["ascendant"])
        self.assertNotEqual(reading(a)["timing"]["sub"], reading(b)["timing"]["sub"])

    def test_contrasting_conditions_abstain_from_an_aggregate(self):
        chart = deepcopy(read(self.request, self.service))
        chart["planets"]["Sun"]["dignity"]["flags"] = ["exaltation_sign"]
        chart["d9"]["planets"]["Sun"]["sign_dignities"] = ["debilitation_sign"]
        sun = reading(chart)["grahas"]["Sun"]
        self.assertIn("different dignity indications", sun["comparison"]["text"])
        self.assertNotIn("strength", sun)
        chart["profile"] = "other"
        self.assertIsNone(reading(chart))
