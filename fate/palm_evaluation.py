"""Offline evaluation of independent palm labels and separately produced suggestions."""
import argparse
import json
import math
from pathlib import Path

FEATURES = ("palm", "orientation", "heart", "head", "life", "marking")
GEOMETRY = {"palm", "heart", "head", "life", "marking"}


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def points(value):
    if not isinstance(value, list) or not value:
        raise ValueError("Geometry requires at least one normalized XY point")
    for point in value:
        if (not isinstance(point, list) or len(point) != 2 or
                any(type(x) not in (int, float) or not 0 <= x <= 1 for x in point)):
            raise ValueError("Expected normalized XY coordinates")
    return value


def distance_to_path(point, path):
    if len(path) == 1:
        return math.dist(point, path[0])
    distances = []
    for start, end in zip(path, path[1:]):
        dx, dy = end[0] - start[0], end[1] - start[1]
        length2 = dx * dx + dy * dy
        projection = ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy)
        t = max(0, min(1, projection / length2)) if length2 else 0
        distances.append(math.dist(point, (start[0] + t * dx, start[1] + t * dy)))
    return min(distances)


def geometry_error(reference, predicted):
    a, b = points(reference), points(predicted)
    return max(max(distance_to_path(p, b) for p in a),
               max(distance_to_path(p, a) for p in b))


def validate_rotation(value):
    if type(value) not in (int, float) or not -180 <= value <= 180:
        raise ValueError("Rotation must be between -180 and 180 degrees")


def index(rows):
    result = {}
    for row in rows:
        key = row["id"]
        if key in result:
            raise ValueError(f"Duplicate photo ID {key}")
        result[key] = row
    return result


def score(rows, feature, tolerance):
    tp = fp = fn = abstain = unknown = known = 0
    distances, angles, scored_confidence, bins = [], [], [], [[], [], [], [], []]
    negative_controls = negative_hits = positive = localized = 0
    for truth, prediction in rows:
        expected = truth["features"][feature]
        suggestion = prediction.get(feature, {})
        label = suggestion.get("label")
        if expected["label"] is None:
            unknown += 1
            continue
        known += 1
        present = expected["label"] != "absent"
        positive += present
        if truth["features"]["palm"]["label"] == "absent":
            negative_controls += 1
            negative_hits += label not in (None, "absent")
        if label is None:
            abstain += 1
            fn += present
            continue
        correct = expected["label"] == label
        tp += correct and present
        fp += not correct and label != "absent"
        fn += not correct and present
        confidence = suggestion.get("confidence")
        if confidence is not None:
            if type(confidence) not in (int, float) or not 0 <= confidence <= 1:
                raise ValueError("Confidence must be between zero and one")
            scored_confidence.append((confidence - int(correct)) ** 2)
            bins[min(4, int(5 * confidence))].append((confidence, int(correct)))
        if feature in GEOMETRY and correct and present and "points" in suggestion:
            error = geometry_error(expected["points"], suggestion["points"])
            distances.append(error)
            localized += error <= tolerance
        if (feature == "orientation" and correct and present and
                "rotation_degrees" in expected and "rotation_degrees" in suggestion):
            delta = suggestion["rotation_degrees"] - expected["rotation_degrees"]
            angles.append(abs((delta + 180) % 360 - 180))
    return {
        "known": known, "positive": positive, "unknown_truth": unknown,
        "tp": tp, "fp": fp, "fn": fn, "precision": ratio(tp, tp + fp),
        "recall": ratio(tp, tp + fn), "abstention": ratio(abstain, known),
        "negative_controls": negative_controls,
        "negative_false_positive_rate": ratio(negative_hits, negative_controls),
        "localized": len(distances), "localized_recall": ratio(localized, positive) if feature in GEOMETRY else None,
        "mean_max_path_error": ratio(sum(distances), len(distances)),
        "rotation_samples": len(angles), "mean_rotation_error_degrees": ratio(sum(angles), len(angles)),
        "confidence_coverage": ratio(len(scored_confidence), known - abstain),
        "confidence_brier": ratio(sum(scored_confidence), len(scored_confidence)),
        "reliability_bins": [
            {"count": len(bucket), "mean_confidence": ratio(sum(c for c, _ in bucket), len(bucket)),
             "accuracy": ratio(sum(ok for _, ok in bucket), len(bucket))}
            for bucket in bins
        ],
    }


def evaluate(labels, predictions, tolerance=0.03):
    if labels.get("schema_version") != 1 or predictions.get("schema_version") != 1:
        raise ValueError("Expected schema version 1")
    if labels.get("label_origin") not in ("independent-human", "synthetic-test"):
        raise ValueError("Model-generated reference labels are forbidden")
    synthetic = labels["label_origin"] == "synthetic-test"
    if not synthetic and not predictions.get("operator"):
        raise ValueError("Independent evaluation requires an identified prediction operator")
    if predictions.get("model_id") in (None, "") or not 0 < tolerance < 1:
        raise ValueError("A pinned model ID and valid localization tolerance are required")
    reference, suggestions = index(labels["photos"]), index(predictions["photos"])
    if not reference or suggestions.keys() != reference.keys():
        raise ValueError("Submit exactly one prediction record per photo; use empty features to abstain")
    rows = []
    for key, photo in reference.items():
        if not photo.get("conditions") or set(photo["features"]) != set(FEATURES):
            raise ValueError(f"{key} needs conditions and explicit labels for every feature")
        if not synthetic and not all(photo.get(k) for k in
                                     ("image_sha256", "subject", "license", "reviewer")):
            raise ValueError(f"{key} needs image digest, subject group, usage rights and reviewer")
        predicted = suggestions[key]
        if not synthetic and (predicted.get("image_sha256") != photo["image_sha256"] or
                              photo["reviewer"] == predictions.get("operator")):
            raise ValueError(f"Image mismatch or non-independent reviewer for {key}")
        for feature in FEATURES:
            expected = photo["features"][feature]
            suggestion = predicted["features"].get(feature, {})
            allowed = (None, "left", "right", "absent") if feature == "orientation" else (None, "present", "absent")
            if expected["label"] not in allowed or suggestion.get("label") not in allowed:
                raise ValueError(f"Unsupported label for {feature}")
            if feature in GEOMETRY and expected["label"] == "present":
                points(expected.get("points"))
            if "points" in suggestion:
                points(suggestion["points"])
            if feature == "orientation":
                for annotation in (expected, suggestion):
                    if "rotation_degrees" in annotation:
                        validate_rotation(annotation["rotation_degrees"])
        if photo["features"]["palm"]["label"] == "absent" and any(
                photo["features"][f]["label"] != "absent" for f in FEATURES[1:]):
            raise ValueError("Negative controls must label every feature absent")
        rows.append((photo, predicted["features"]))

    conditions = sorted({c for photo, _ in rows for c in photo["conditions"]})
    return {
        "photos": len(rows), "label_origin": labels["label_origin"],
        "model_id": predictions["model_id"], "normalized_path_tolerance": tolerance,
        "overall": {f: score(rows, f, tolerance) for f in FEATURES},
        "by_condition": {c: {f: score([(p, s) for p, s in rows if c in p["conditions"]], f, tolerance)
                            for f in FEATURES} for c in conditions},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("labels", type=Path)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--tolerance", type=float, default=0.03)
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.labels.read_text(encoding="utf-8")),
                          json.loads(args.predictions.read_text(encoding="utf-8")), args.tolerance)
    except (KeyError, TypeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
