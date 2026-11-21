from copy import deepcopy
from unittest import TestCase

from fate.natal_reading import PROFILE, aspect_id, summarize
from fate.western import WesternInput, WesternService
from future.doctrines import analyze
from future.natal import Settings, chart


class NatalReadingTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.western = WesternService()

    @classmethod
    def tearDownClass(cls):
        cls.western.close()

    def calculate(self, local="1990-07-15T14:30:00", **options):
        request = WesternInput(**{
            "local": local, "zone": "Europe/London", "latitude": 51.50853,
            "longitude": -0.12574, **options,
        })
        result = self.western.read(request)
        expected = chart(self.western.get_ephemeris(), request.local, request.zone,
                         request.latitude, request.longitude, Settings(houses=request.houses), request.fold)
        self.assertEqual({k: result[k] for k in expected}, expected)
        before = deepcopy(result)
        reading = summarize(result)
        self.assertEqual(before, result)
        return result, reading

    def test_linked_luminaries_and_competing_symbolism(self):
        result, reading = self.calculate()
        self.assertEqual(reading["profile"], PROFILE)
        passages = [p for c in reading["chapters"] for p in c["passages"]]
        by_title = {p["title"]: p for p in passages}
        self.assertEqual(by_title["Warmth and reserve"]["coverage"], "editorial")
        limits = by_title["Room to grow, room for limits"]
        self.assertEqual(limits["rule_ids"], ["fate.natal.v1.aspect.sun.jupiter.0", "fate.natal.v1.aspect.sun.saturn.180"])
        self.assertTrue(reading["sources"][limits["rule_ids"][0]]["exceptions"])
        self.assertIn("fate.natal.v1.aspect.sun.moon.90", by_title["Purpose and need pull differently"]["rule_ids"])
        self.assertEqual(reading["chart_ruler"]["body"], "Mars")
        self.assertTrue(result["planets"]["Saturn"]["retrograde"])
        self.assertFalse(any("retrograde" in r["id"] for r in reading["sources"].values()))
        native = {aspect_id(aspect): aspect["angle"] for aspect in result["aspects"]}
        self.assertTrue(reading["patterns"])
        for pattern in reading["patterns"]:
            self.assertEqual([native[key] for key in pattern["contacts"]], [180, 90, 90])
        for passage in passages:
            self.assertTrue(set(passage["rule_ids"]) <= set(reading["sources"]))
        self.assertEqual(reading["focuses"]["aspect:Neptune-Pluto:60"]["passages"], [])

    def test_houses_only_affect_house_dependent_evidence(self):
        whole, w = self.calculate()
        quadrant, q = self.calculate(houses="placidus")
        self.assertEqual(whole["aspects"], quadrant["aspects"])
        self.assertNotEqual(whole["house_cusps"], quadrant["house_cusps"])
        for native, reading in [(whole, w), (quadrant, q)]:
            for body in ("Sun", "Moon", "Mercury"):
                n = native["planets"][body]["house"]
                self.assertIn(f"fate.natal.v1.house.{body.lower()}.{n}", reading["sources"])
                self.assertNotIn(f"fate.natal.v1.house.{body.lower()}.{n % 12 + 1}", reading["sources"])
        self.assertEqual(w["chart_ruler"]["body"], q["chart_ruler"]["body"])

    def test_time_boundaries_and_declared_tradition(self):
        # London noon and midnight straddle the horizon in the native house layout.
        day, d = self.calculate("2000-01-01T12:00")
        night, n = self.calculate("2000-01-01T00:00")
        self.assertGreater(day["planets"]["Sun"]["house"], 6)
        self.assertLessEqual(night["planets"]["Sun"]["house"], 6)
        self.assertNotEqual(d["focuses"]["Ascendant"], n["focuses"]["Ascendant"])
        self.assertFalse(any("sect" in rule for rule in (*d["sources"], *n["sources"])))
        day["settings"]["tradition"] = "Hellenistic"
        self.assertFalse(summarize(day)["chapters"])

        for instant, expected_sect in [("08:13", "night"), ("08:14", "day")]:
            native, consumer = self.calculate(f"2000-01-01T{instant}")
            traditional = chart(self.western.get_ephemeris(), native["birth"]["local"], "Europe/London",
                                51.50853, -0.12574, Settings(tradition="Hellenistic"))
            sect = analyze(self.western.get_ephemeris(), traditional)["sect"]
            self.assertEqual(sect["type"], expected_sect)
            self.assertTrue(sect["boundary_sensitive"])
            self.assertNotIn("sect", consumer)

        early, e = self.calculate("2024-11-03T01:30", zone="America/New_York", latitude=40.71, longitude=-74, fold=0)
        late, l = self.calculate("2024-11-03T01:30", zone="America/New_York", latitude=40.71, longitude=-74, fold=1)
        self.assertEqual(early["birth"]["utc"], "2024-11-03T05:30:00+00:00")
        self.assertEqual(late["birth"]["utc"], "2024-11-03T06:30:00+00:00")
        self.assertNotEqual(early["angles"], late["angles"])
        self.assertNotIn("birth", e)
        self.assertNotIn("birth", l)
