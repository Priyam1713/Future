# Future Lab research report

**User-declared research or native procedural output — no empirical skill certification.**

```json
{
  "status": "accepted",
  "task": "compare",
  "result": {
    "status": "estimable",
    "matched_target_ids": [
      "q1",
      "q2"
    ],
    "matched_count": 2,
    "models": [
      {
        "report_sha256": "50b5078d9156f67fe493322c06ad0a6463adb517eeb8de9df5000a44f06ed1d4",
        "technique_id": 51,
        "scores": {
          "count": 2,
          "brier": {
            "status": "finite",
            "exact": "17/50",
            "decimal": "0.340000000000"
          },
          "two_category_brier": {
            "status": "finite",
            "exact": "17/25",
            "decimal": "0.680000000000"
          },
          "calibration": [
            {
              "index": 0,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 1,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 2,
              "count": 1,
              "mean_probability": "1/5",
              "observed_frequency": "0"
            },
            {
              "index": 3,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 4,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 5,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 6,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 7,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 8,
              "count": 1,
              "mean_probability": "4/5",
              "observed_frequency": "0"
            },
            {
              "index": 9,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            }
          ]
        }
      },
      {
        "report_sha256": "50b5078d9156f67fe493322c06ad0a6463adb517eeb8de9df5000a44f06ed1d4",
        "technique_id": 51,
        "scores": {
          "count": 2,
          "brier": {
            "status": "finite",
            "exact": "17/50",
            "decimal": "0.340000000000"
          },
          "two_category_brier": {
            "status": "finite",
            "exact": "17/25",
            "decimal": "0.680000000000"
          },
          "calibration": [
            {
              "index": 0,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 1,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 2,
              "count": 1,
              "mean_probability": "1/5",
              "observed_frequency": "0"
            },
            {
              "index": 3,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 4,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 5,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 6,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 7,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            },
            {
              "index": 8,
              "count": 1,
              "mean_probability": "4/5",
              "observed_frequency": "0"
            },
            {
              "index": 9,
              "count": 0,
              "mean_probability": null,
              "observed_frequency": null
            }
          ]
        }
      }
    ],
    "empirical_superiority_certified": false,
    "limits": "Compatible targets and exact matched scores do not establish independent held-out superiority."
  }
}
```

