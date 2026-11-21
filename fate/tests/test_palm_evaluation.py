from unittest import TestCase

from fate.palm_evaluation import FEATURES, evaluate


class PalmEvaluationTests(TestCase):
    def test_localization_abstention_and_negative_controls(self):
        path = [[0.1, 0.2], [0.7, 0.2]]
        clear = {name: {"label": "absent"} for name in FEATURES}
        clear.update(palm={"label": "present", "points": path},
                     head={"label": "present", "points": path},
                     orientation={"label": "left", "rotation_degrees": -175})
        labels = dict(schema_version=1, label_origin="synthetic-test", photos=[
            dict(id="a", conditions=["even"], features=clear),
            dict(id="b", conditions=["background"], features={f: {"label": "absent"} for f in FEATURES}),
        ])
        predictions = dict(schema_version=1, model_id="fixture-v1", photos=[
            dict(id="a", features={"palm": {"label": "present", "points": path, "confidence": .8},
                                   "orientation": {"label": "right", "confidence": .9}}),
            dict(id="b", features={"palm": {"label": "present", "confidence": .6}}),
        ])
        report = evaluate(labels, predictions)
        self.assertEqual(report["overall"]["palm"]["precision"], .5)
        self.assertEqual(report["overall"]["palm"]["localized_recall"], 1)
        self.assertEqual(report["overall"]["palm"]["negative_false_positive_rate"], 1)
        self.assertAlmostEqual(report["overall"]["palm"]["confidence_brier"], .2)
        self.assertEqual(report["overall"]["head"]["abstention"], 1)
        self.assertEqual(report["by_condition"]["even"]["orientation"]["recall"], 0)
        predictions["photos"][0]["features"]["orientation"] = {"label": "left", "rotation_degrees": 175}
        self.assertEqual(evaluate(labels, predictions)["overall"]["orientation"]["mean_rotation_error_degrees"], 10)
        labels["label_origin"] = "model"
        with self.assertRaisesRegex(ValueError, "Model-generated"):
            evaluate(labels, predictions)
