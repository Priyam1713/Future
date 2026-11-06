# CPU forecasting workbench

Retrospective evaluation on a fixed revised data snapshot;historical publication vintages are unverified. Software prefix isolation does not prove as-of historical data availability.

```json
{
  "status": "accepted",
  "task": "forecast",
  "profile": {
    "id": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
    "version": 1,
    "sha256": "ed2490bf3ddc5861b3a406e2ba8aa93b3f2b2fe33e0b7917371e5c26875e7fdb"
  },
  "request_sha256": "7cf8f4242b3b2922b4f5063117adae590762b0820a3e2402adb103cf18e39d35",
  "source": {
    "version": 1,
    "technique_id": 49,
    "date": "2026-11-07",
    "edition": "FPP3 third edition online modified2026-11-04;R/fpp3 examples are not Python implementation parity.",
    "rechecked": [
      {
        "url": "https://otexts.com/fpp3/toolbox.html",
        "locator": "§5.2 mean,naive,seasonal-naive and drift;§5.8–5.10 metrics and rolling origin"
      },
      {
        "url": "https://otexts.com/fpp3/exponential-smoothing.html",
        "locator": "§8.1 weighted/component SES recurrences and initial-level term;fixed y1 initialization is our explicit convention"
      }
    ],
    "ranked_sources": [
      [
        49,
        "AI Predictive Modeling",
        1,
        "Rob J. Hyndman and George Athanasopoulos",
        "Forecasting: Principles and Practice (3rd ed.)",
        "Transparent statistical methods and evaluation",
        "https://otexts.com/fpp3/",
        "Open textbook",
        "Bibliographic lead; check edition, chapters, rights before ingesting"
      ],
      [
        49,
        "AI Predictive Modeling",
        2,
        "Amazon Science",
        "Chronos-2 Model Card",
        "Current pretrained foundation-model implementation",
        "https://huggingface.co/amazon/chronos-2",
        "Open model card / check license",
        "Bibliographic lead; check edition, chapters, rights before ingesting"
      ]
    ],
    "variation_rows": [
      [
        49,
        "AI Predictive Modeling",
        "Classical ARIMA/ETS",
        "Chronos-2 Model Card",
        "Forecasting: Principles and Practice (3rd ed.)",
        "Provisional / chapter check needed",
        "Locate chapters; extract algorithms, symbol tables, exception cases",
        "Knowledge gathering"
      ],
      [
        49,
        "AI Predictive Modeling",
        "boosted trees",
        "Chronos-2 Model Card",
        "Forecasting: Principles and Practice (3rd ed.)",
        "Provisional / chapter check needed",
        "Locate chapters; extract algorithms, symbol tables, exception cases",
        "Knowledge gathering"
      ],
      [
        49,
        "AI Predictive Modeling",
        "neural time-series",
        "Chronos-2 Model Card",
        "Forecasting: Principles and Practice (3rd ed.)",
        "Provisional / chapter check needed",
        "Locate chapters; extract algorithms, symbol tables, exception cases",
        "Knowledge gathering"
      ],
      [
        49,
        "AI Predictive Modeling",
        "probabilistic transformers",
        "Chronos-2 Model Card",
        "Forecasting: Principles and Practice (3rd ed.)",
        "Provisional / chapter check needed",
        "Locate chapters; extract algorithms, symbol tables, exception cases",
        "Knowledge gathering"
      ],
      [
        49,
        "AI Predictive Modeling",
        "foundation models",
        "Chronos-2 Model Card",
        "Forecasting: Principles and Practice (3rd ed.)",
        "Indicative (scope match)",
        "Locate chapters; extract algorithms, symbol tables, exception cases",
        "Knowledge gathering"
      ]
    ],
    "rights": "Facts-only original methodological notes;no textbook corpus,figures or implementation copied. NOAA numerical subset retains attribution/public-domain policy. No Chronos assets acquired.",
    "dataset": {
      "path": "resources/ai-predictive-modeling/noaa_mlo_2000_2023.json",
      "sha256": "303c231dd00ba7cf6302e02dbb25525b91e226008a71b15856f25f775aa9645c",
      "count": 288,
      "first": "2000-01",
      "last": "2023-12",
      "source_sha256": "0ce4e7749217b4af2cca8e0bdf263856ad59b0a2946d4e98c7b22ccfbff21cad",
      "rights": "NOAA government data public domain unless separately annotated;retain source/product credit,no endorsement or misrepresentation. Selected2000–2023 NOAA measurements avoid the pre1974 Scripps-sourced portion of the full file.",
      "attribution": "Data provided by NOAA Global Monitoring Laboratory, Boulder, Colorado, USA;Carbon Cycle and Greenhouse Gases group. Original NOAA values;this selected research subset is not an official NOAA product or endorsement."
    },
    "vintage": "Retrospective evaluation on a fixed revised data snapshot. QC/calibration/midmonth corrections and2022–2023Maunakea substitution;historical publication vintages unverified. Prefix isolation does not prove historical source availability.",
    "formula_provenance": "Seasonal m4 and drift toy sequences are original arithmetic applications,not published empirical accuracy. SES geometric weights and FPP3 Google scoring examples separately source-attributed.",
    "unsupported": [
      "ARIMA search",
      "Likelihood-fitted ETS",
      "Holt/Holt-Winters",
      "Trees or neural training",
      "Chronos inference/downloads",
      "Generated prediction intervals",
      "GPU/cloud forecasting"
    ]
  },
  "result": {
    "cells": [
      {
        "model": {
          "id": "ses_alpha0.5_initial_y1",
          "version": 1,
          "family": "ses",
          "alpha": "0.5",
          "seasonal_period": null,
          "initialization": "first observation,then consume subsequent observations"
        },
        "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
        "profile_version": 1,
        "series_id": "synthetic1",
        "dataset_sha256": "11e7f149a0f7e21ecffe891d7812be86a0b4bbb703b06d2ed4d02de12f638701",
        "source_sha256": null,
        "training_cutoff": "2020-04",
        "training_rows": 4,
        "training_prefix_sha256": "7b4a70dea3360554d2b3d5c5048fd4a79e180c295afe264016ce189d9ee1e16a",
        "origin": "2020-04",
        "horizon": 1,
        "target_period": "2020-05",
        "partition": "forecast",
        "status": "missing_target",
        "reason": "missing_evaluation_outcome",
        "prediction": {
          "exact": "5",
          "decimal": "5.000000000000",
          "reason": null
        },
        "point_functional": "fixed-alpha final level",
        "actual": null,
        "error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "squared_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "training_scale": {
          "exact": "3",
          "decimal": "3.000000000000",
          "reason": null
        },
        "scaled_absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "sha256": "82dcd1a42b7f6e7b10488cd2c0a218771f3da231b3dee07952f0a82aaecc3ac5"
      },
      {
        "model": {
          "id": "ses_alpha0.5_initial_y1",
          "version": 1,
          "family": "ses",
          "alpha": "0.5",
          "seasonal_period": null,
          "initialization": "first observation,then consume subsequent observations"
        },
        "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
        "profile_version": 1,
        "series_id": "synthetic1",
        "dataset_sha256": "11e7f149a0f7e21ecffe891d7812be86a0b4bbb703b06d2ed4d02de12f638701",
        "source_sha256": null,
        "training_cutoff": "2020-04",
        "training_rows": 4,
        "training_prefix_sha256": "7b4a70dea3360554d2b3d5c5048fd4a79e180c295afe264016ce189d9ee1e16a",
        "origin": "2020-04",
        "horizon": 2,
        "target_period": "2020-06",
        "partition": "forecast",
        "status": "missing_target",
        "reason": "missing_evaluation_outcome",
        "prediction": {
          "exact": "5",
          "decimal": "5.000000000000",
          "reason": null
        },
        "point_functional": "fixed-alpha final level",
        "actual": null,
        "error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "squared_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "training_scale": {
          "exact": "3",
          "decimal": "3.000000000000",
          "reason": null
        },
        "scaled_absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "sha256": "7a70e6f1a9f55aec792dd1e86bec039b236cfb0cb6458df3ccfab3fef3a23fc5"
      },
      {
        "model": {
          "id": "ses_alpha0.5_initial_y1",
          "version": 1,
          "family": "ses",
          "alpha": "0.5",
          "seasonal_period": null,
          "initialization": "first observation,then consume subsequent observations"
        },
        "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
        "profile_version": 1,
        "series_id": "synthetic1",
        "dataset_sha256": "11e7f149a0f7e21ecffe891d7812be86a0b4bbb703b06d2ed4d02de12f638701",
        "source_sha256": null,
        "training_cutoff": "2020-04",
        "training_rows": 4,
        "training_prefix_sha256": "7b4a70dea3360554d2b3d5c5048fd4a79e180c295afe264016ce189d9ee1e16a",
        "origin": "2020-04",
        "horizon": 3,
        "target_period": "2020-07",
        "partition": "forecast",
        "status": "missing_target",
        "reason": "missing_evaluation_outcome",
        "prediction": {
          "exact": "5",
          "decimal": "5.000000000000",
          "reason": null
        },
        "point_functional": "fixed-alpha final level",
        "actual": null,
        "error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "squared_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "training_scale": {
          "exact": "3",
          "decimal": "3.000000000000",
          "reason": null
        },
        "scaled_absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "sha256": "4c21750f4d23e613667d14e9f2aafbd53094dfcda48264b18036bf0477216f62"
      }
    ],
    "dataset": {
      "id": "synthetic",
      "version": 1,
      "frequency": "monthly",
      "units": "original units",
      "provenance": {
        "source_ref": "original-synthetic",
        "snapshot_sha256": null,
        "rights": "self_authored",
        "attribution": "Original synthetic numerical demonstration",
        "notes": "Unicode note  \n"
      },
      "series": [
        {
          "id": "synthetic1",
          "availability": {
            "status": "unknown",
            "vintage": null,
            "notes": "No independent availability witness"
          },
          "observations": [
            {
              "period": "2020-01",
              "value": "1"
            },
            {
              "period": "2020-02",
              "value": "3"
            },
            {
              "period": "2020-03",
              "value": "2"
            },
            {
              "period": "2020-04",
              "value": "8"
            }
          ]
        }
      ]
    },
    "dataset_sha256": "11e7f149a0f7e21ecffe891d7812be86a0b4bbb703b06d2ed4d02de12f638701"
  },
  "code_sha256": "b20c30fdfde79e37413bbaae9544ee6ef69cd2765a7ef1ec68a53d0ad765b014",
  "resource_evidence": null,
  "resource_policy": "Measured separately and frozen by hash;pure deterministic forecasts contain no fabricated runtime measurements.",
  "vintage": "Retrospective evaluation on a fixed revised data snapshot;historical publication vintages are unverified. Software prefix isolation does not prove as-of historical data availability.",
  "limits": [
    "Fixed SES conventions are not optimized ETS",
    "No ARIMA/trees/neural/Chronos operation or downloaded assets",
    "No generated prediction intervals or guaranteed accuracy",
    "All-candidate test scores are diagnostic;selection uses validation only",
    "Exact absolute-sMAPE is a manual diagnostic for at most20scored pairs;omitted from benchmark aggregates to avoid impractical rational denominator growth"
  ],
  "report_sha256": "42ef92982c327802d57d8247409d757bee0d38eb17bb206fead40f30c4b3b264"
}
```
