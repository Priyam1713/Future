# Future Lab v1 — complete synthetic experiment

**SYNTHETIC: no empirical superiority claim.**

Three fictional questions were frozen before their declared outcomes. One outcome is missing; two are scored on the same sample as the fixed 1/2 baseline. Model Brier is 17/50; baseline Brier is 1/4; model-minus-baseline is 9/100, so this toy model underperforms.

The JSON artifact retains the full append-only ledger, original native forecast output, hashes, separate outcome evidence and research report. Dataset, plan and intermediate forecast snapshots are in `data/future-lab-demo/`.

# Future Lab research report

**SYNTHETIC DEMONSTRATION — no empirical skill claim.**

```json
{
  "schema_version": 1,
  "experiment_id": "synthetic-switch-study",
  "experiment_version": 1,
  "mode": "synthetic",
  "visibly_synthetic": true,
  "technique_id": 51,
  "registry_sha256": "2b2c0a4f372b8861b1471b50acc2313b6cc2882293273c2924a84aac3a0ccf2d",
  "profile_identifiers": "tetlock-mellers-binary-forecast-updates-v1",
  "plan_sha256": "0d98cab5c56c95ab06b4c023b937780f4614707a7b03352a78803bc32ef7f0bf",
  "ledger_sha256": "5b2c88858f547b61f5860b71aea47f64c0829cfcc7d7a1f7305f2bb851c1a005",
  "forecast_output_sha256": "dc516085179dc99645dfa247349a0135293a8551123d8c26277e007aabe69c92",
  "metric": "brier",
  "target_definition": "Three fictional binary switch questions, fixed before their outcomes.",
  "target_unit": "binary_event",
  "dataset": {
    "id": "synthetic-switch-data",
    "version": 1,
    "rights": "self_authored",
    "attribution": "Future original synthetic experiment",
    "snapshot": "Self-authored synthetic switch experiment; no real participants or measured forecasting skill.",
    "snapshot_sha256": "ca9de6ef51fac4a35df21bdafe16631310e7338fb4b7197dc6574fd948de47a8",
    "available_at": "2024-12-31T00:00:00Z",
    "source_vintage": {
      "status": "declared_as_of",
      "retrieved_at": "2024-12-31T00:00:00Z",
      "notes": "Synthetic declarations only; no external information-vintage certification."
    }
  },
  "selection": {
    "frozen_at": "2025-01-01T00:00:00Z",
    "model_id": "native_forecast_versions",
    "native_input_sha256": "f3409d8d1c0b20f5f5f4ccfcd2036f2e5dc1bdd118d1a9786576e5eceeb0aa4b",
    "training_ids": [],
    "validation_ids": []
  },
  "splits": [
    {
      "id": "q1",
      "group": "test1",
      "partition": "test",
      "available_at": "2025-01-10T00:00:00Z"
    },
    {
      "id": "q2",
      "group": "test2",
      "partition": "test",
      "available_at": "2025-01-10T00:00:00Z"
    },
    {
      "id": "q3",
      "group": "test3",
      "partition": "test",
      "available_at": "2025-01-10T00:00:00Z"
    }
  ],
  "cases": [
    {
      "target_id": "q1",
      "event_id": "event1",
      "dependency_group": "test1",
      "target_at": "2025-01-10T00:00:00Z",
      "prediction": "1/5",
      "baseline": "1/2",
      "outcome": "0",
      "outcome_status": "resolved",
      "outcome_record": {
        "target_id": "q1",
        "event_id": "event1",
        "version": 1,
        "status": "resolved",
        "value": "0",
        "known_at": "2025-01-10T00:00:00Z",
        "reason": "Synthetic switch remained zero throughout its closed window",
        "evidence": {
          "id": "evidence-q1",
          "available_at": "2025-01-11T00:00:00Z",
          "rights": "self_authored",
          "attribution": "Original synthetic outcome author",
          "snapshot": "Synthetic switch outcome log, authored separately after forecast commitment.",
          "snapshot_sha256": "78b099f69634074e8ee964434a946331a1d58c150ebf1d78b8be84b7dfadb7ef"
        }
      },
      "eligible": true,
      "exclusion_reasons": []
    },
    {
      "target_id": "q2",
      "event_id": "event2",
      "dependency_group": "test2",
      "target_at": "2025-01-10T00:00:00Z",
      "prediction": "4/5",
      "baseline": "1/2",
      "outcome": "0",
      "outcome_status": "resolved",
      "outcome_record": {
        "target_id": "q2",
        "event_id": "event2",
        "version": 1,
        "status": "resolved",
        "value": "0",
        "known_at": "2025-01-10T00:00:00Z",
        "reason": "Synthetic switch remained zero throughout its closed window",
        "evidence": {
          "id": "evidence-q2",
          "available_at": "2025-01-11T00:00:00Z",
          "rights": "self_authored",
          "attribution": "Original synthetic outcome author",
          "snapshot": "Synthetic switch outcome log, authored separately after forecast commitment.",
          "snapshot_sha256": "78b099f69634074e8ee964434a946331a1d58c150ebf1d78b8be84b7dfadb7ef"
        }
      },
      "eligible": true,
      "exclusion_reasons": []
    },
    {
      "target_id": "q3",
      "event_id": "event3",
      "dependency_group": "test3",
      "target_at": "2025-01-10T00:00:00Z",
      "prediction": "1/2",
      "baseline": "1/2",
      "outcome": null,
      "outcome_status": "missing",
      "outcome_record": {
        "target_id": "q3",
        "event_id": "event3",
        "version": 1,
        "status": "missing",
        "value": null,
        "known_at": null,
        "reason": "Synthetic observation missing",
        "evidence": {
          "id": "evidence-q3",
          "available_at": "2025-01-11T00:00:00Z",
          "rights": "self_authored",
          "attribution": "Original synthetic outcome author",
          "snapshot": "Synthetic switch outcome log, authored separately after forecast commitment.",
          "snapshot_sha256": "78b099f69634074e8ee964434a946331a1d58c150ebf1d78b8be84b7dfadb7ef"
        }
      },
      "eligible": false,
      "exclusion_reasons": [
        "outcome_missing"
      ]
    }
  ],
  "coverage": {
    "planned": 3,
    "matched": 2,
    "matched_target_ids": [
      "q1",
      "q2"
    ],
    "missing_outcomes": 1,
    "excluded_outcomes": 0,
    "missing_forecasts": 0,
    "missing_baselines": 0,
    "unique_matched_events": 2,
    "matched_dependency_groups": 2
  },
  "model": {
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
  },
  "baseline": {
    "count": 2,
    "brier": {
      "status": "finite",
      "exact": "1/4",
      "decimal": "0.250000000000"
    },
    "two_category_brier": {
      "status": "finite",
      "exact": "1/2",
      "decimal": "0.500000000000"
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
        "count": 0,
        "mean_probability": null,
        "observed_frequency": null
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
        "count": 2,
        "mean_probability": "1/2",
        "observed_frequency": "0"
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
        "count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 9,
        "count": 0,
        "mean_probability": null,
        "observed_frequency": null
      }
    ]
  },
  "comparison": {
    "status": "estimable",
    "model_minus_baseline": "9/100",
    "direction": "Negative matched loss difference favors model; synthetic differences are not empirical skill.",
    "matched_only": true
  },
  "uncertainty": {
    "independence_certified": false,
    "effective_sample_size": null,
    "confidence_interval": null,
    "note": "Descriptive counts and calibration only. Shared events, horizons and groups can be dependent."
  },
  "source_vintage_certified": false,
  "empirical_skill_certified": false,
  "independent_held_out_superiority_certified": false,
  "limitations": [
    "Rights,clocks,availability andtargetdefinitions aredeclared; semantic leakage andexternaltruth arenotcertified.",
    "No tuning or selection using newly recorded test outcomes.",
    "One immutable forecast and one outcome record pertarget/version; corrections require an explicitnewversion."
  ],
  "cutoff": "2025-01-03T00:00:00Z",
  "created_at": "2025-01-01T00:00:00Z",
  "forecast_execution_provenance": {
    "registry_sha256": "2b2c0a4f372b8861b1471b50acc2313b6cc2882293273c2924a84aac3a0ccf2d",
    "core_sha256": "443261a2a3b9c4d6f1c8d3bd5c73652fe5c6284f0e9813ddce16f621442d769e",
    "request_sha256": "3e8492ce0ba013d96fda05527c8b420376e7ec9e9a5525cede3f3f52cdbf5b07",
    "adapter": "native_request",
    "provenance": {
      "core_release": "core-v1.0.0",
      "profile_identifiers": "tetlock-mellers-binary-forecast-updates-v1",
      "python_entry_point": "future.superforecasting.read",
      "sources": [
        {
          "path": "knowledge/superforecasting_sources.json",
          "sha256": "7502f901d5e17b31e7e798e192473bc8ae73854e863484c2f65a6f251d841e0b"
        }
      ]
    },
    "lab_profile_sha256": "5b8b09b98f1f3a46a24db9fc6b334e7ea776f7e03d6646e2e05fa8907e95a3a3",
    "lab_code_sha256": "74284978fb37ad9edc423588f27e0ce190d575e04b266ac2757b27417340edba"
  },
  "report_sha256": "50b5078d9156f67fe493322c06ad0a6463adb517eeb8de9df5000a44f06ed1d4"
}
```
