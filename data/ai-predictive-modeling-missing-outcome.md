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
  "request_sha256": "2ee216953f17b3580076fea9ccfe00f0eaa3655e8fa00515d05f0abc3818418a",
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
          "id": "naive",
          "version": 1,
          "family": "naive",
          "alpha": null,
          "seasonal_period": null,
          "initialization": null
        },
        "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
        "profile_version": 1,
        "series_id": "synthetic1",
        "dataset_sha256": "49cf68b8cda9b2a13f0566588215b08b0ac7151f074490f17ca2d2e06e7958b1",
        "source_sha256": null,
        "training_cutoff": "2020-03",
        "training_rows": 3,
        "training_prefix_sha256": "be384a25c4c3fc8af8f2dadd9a7f4f2afa3d8bfcead76a1e18ab27fb1eb25944",
        "origin": "2020-03",
        "horizon": 1,
        "target_period": "2020-04",
        "partition": "forecast",
        "status": "missing_target",
        "reason": "missing_evaluation_outcome",
        "prediction": {
          "exact": "3",
          "decimal": "3.000000000000",
          "reason": null
        },
        "point_functional": "last observed value",
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
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "scaled_absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "sha256": "1b75e2c0b4787bf7604af4d3fb06e148ce4ad6e4f4afa669acf611815c702d47"
      },
      {
        "model": {
          "id": "naive",
          "version": 1,
          "family": "naive",
          "alpha": null,
          "seasonal_period": null,
          "initialization": null
        },
        "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
        "profile_version": 1,
        "series_id": "synthetic1",
        "dataset_sha256": "49cf68b8cda9b2a13f0566588215b08b0ac7151f074490f17ca2d2e06e7958b1",
        "source_sha256": null,
        "training_cutoff": "2020-03",
        "training_rows": 3,
        "training_prefix_sha256": "be384a25c4c3fc8af8f2dadd9a7f4f2afa3d8bfcead76a1e18ab27fb1eb25944",
        "origin": "2020-03",
        "horizon": 12,
        "target_period": "2021-03",
        "partition": "forecast",
        "status": "missing_target",
        "reason": "missing_evaluation_outcome",
        "prediction": {
          "exact": "3",
          "decimal": "3.000000000000",
          "reason": null
        },
        "point_functional": "last observed value",
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
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "scaled_absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "sha256": "22526b76395ef4d1052fd072becb6d587ab8db0c7319486e8b7a00b7dce6c142"
      },
      {
        "model": {
          "id": "naive",
          "version": 1,
          "family": "naive",
          "alpha": null,
          "seasonal_period": null,
          "initialization": null
        },
        "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
        "profile_version": 1,
        "series_id": "synthetic1",
        "dataset_sha256": "49cf68b8cda9b2a13f0566588215b08b0ac7151f074490f17ca2d2e06e7958b1",
        "source_sha256": null,
        "training_cutoff": "2020-03",
        "training_rows": 3,
        "training_prefix_sha256": "be384a25c4c3fc8af8f2dadd9a7f4f2afa3d8bfcead76a1e18ab27fb1eb25944",
        "origin": "2020-03",
        "horizon": 13,
        "target_period": "2021-04",
        "partition": "forecast",
        "status": "missing_target",
        "reason": "missing_evaluation_outcome",
        "prediction": {
          "exact": "3",
          "decimal": "3.000000000000",
          "reason": null
        },
        "point_functional": "last observed value",
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
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "scaled_absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "unscored"
        },
        "sha256": "d4d19bd621d4d40192a538c783dfcbc0b5eeb0223c3791ecf55eed5bb52d99f9"
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
              "value": "2"
            },
            {
              "period": "2020-03",
              "value": "3"
            }
          ]
        }
      ]
    },
    "dataset_sha256": "49cf68b8cda9b2a13f0566588215b08b0ac7151f074490f17ca2d2e06e7958b1"
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
  "report_sha256": "e64384f679d68a7419171811715d9f2869c71b7f1cd9f9a00e203c970d243ced"
}
```
