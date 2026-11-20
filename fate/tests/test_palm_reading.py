from unittest import TestCase

from fate.palm_reading import PalmInput, read
from future import palmistry


class ConsumerPalmTests(TestCase):
    def read(self, hand, confirmed=True):
        return read(PalmInput(confirmed=confirmed, hand={"side": "left", **hand}))

    def test_named_composition_has_native_provenance(self):
        hand = dict(shape={"type": "square"}, lines={
            "head": {"presence": "present", "curvature": "slight_slope"},
            "heart": {"presence": "present", "origin": "jupiter"},
        })
        report = self.read(hand)
        native = report["native"]["hands"][0]
        self.assertEqual(report["native"], palmistry.read(dict(
            schema_version=1, profile=palmistry.PROFILE, hands=[{"side": "left", **hand}])).copy())
        stories = report["narrative"]
        self.assertEqual(len(stories["matched_sections"]), 3)
        self.assertTrue(stories["connections"])
        matched = {rule["id"] for rule in native["readings"]}
        self.assertTrue(all(set(c["rule_ids"]) <= matched for c in stories["chapters"]))
        heart = [c for c in stories["chapters"] if "below your index finger" in c["body"]]
        self.assertEqual([c["title"] for c in heart], ["Steady affection"])

    def test_unknown_and_conflicting_observations_abstain(self):
        self.assertTrue(self.read({})["narrative"]["abstained"])
        result = self.read({"lines": {"heart": {"presence": "absent", "origin": "jupiter"}}})
        self.assertTrue(result["narrative"]["abstained"])
        self.assertTrue(result["native"]["hands"][0]["observation_conflicts"])

    def test_no_confirmation_no_reading(self):
        with self.assertRaisesRegex(ValueError, "Confirm"):
            self.read({}, confirmed=False)

    def test_image_field_rejected(self):
        with self.assertRaises(ValueError):
            read(PalmInput(confirmed=True, hand={"side": "right", "image": "not accepted"}))

    def test_new_combinations_require_exact_confirmed_features(self):
        rejected = read(PalmInput(confirmed=True, hand={"side": "left"}, fingertips="conic"))
        self.assertFalse(rejected["supplement"])
        result = read(PalmInput(confirmed=True, hand={"side": "left", "shape": {"type": "square"}},
                                fingertips="conic", mount_lean="saturn_sun"))
        self.assertEqual([x["locator"] for x in result["supplement"]],
                         ["p. 30, scan page 56", "p. 65, scan page 113"])
        self.assertEqual(len(result["native"]["hands"][0]["readings"]), 1)
