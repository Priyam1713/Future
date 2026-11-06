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
  "request_sha256": "9304645cbc0b607b81aac30ef708c173728f5382d1d891766286814627d9aa19",
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
        "dataset_sha256": "737e3f5fc2c3677979a49cb5072ee4f749ec0d3068da80b4b25c9f1cb3e9ad15",
        "source_sha256": null,
        "training_cutoff": "2020-03",
        "training_rows": 3,
        "training_prefix_sha256": "6a73c489a47c9c2dc76579bacb5f5b59fb822a9a5da5a62bc0b0b113c32016cc",
        "origin": "2020-03",
        "horizon": 1,
        "target_period": "2020-04",
        "partition": "forecast",
        "status": "success",
        "reason": null,
        "prediction": {
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "point_functional": "last observed value",
        "actual": "100",
        "error": {
          "exact": "99",
          "decimal": "99.000000000000",
          "reason": null
        },
        "absolute_error": {
          "exact": "99",
          "decimal": "99.000000000000",
          "reason": null
        },
        "squared_error": {
          "exact": "9801",
          "decimal": "9801.000000000000",
          "reason": null
        },
        "training_scale": {
          "exact": null,
          "decimal": null,
          "reason": "zero_training_scale"
        },
        "scaled_absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "zero_training_scale"
        },
        "sha256": "4be55933b89d3d65638f3c3d6d96a1cb6a04ab125337613d800b3213d821f740"
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
        "dataset_sha256": "737e3f5fc2c3677979a49cb5072ee4f749ec0d3068da80b4b25c9f1cb3e9ad15",
        "source_sha256": null,
        "training_cutoff": "2020-03",
        "training_rows": 3,
        "training_prefix_sha256": "6a73c489a47c9c2dc76579bacb5f5b59fb822a9a5da5a62bc0b0b113c32016cc",
        "origin": "2020-03",
        "horizon": 2,
        "target_period": "2020-05",
        "partition": "forecast",
        "status": "success",
        "reason": null,
        "prediction": {
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "point_functional": "last observed value",
        "actual": "100",
        "error": {
          "exact": "99",
          "decimal": "99.000000000000",
          "reason": null
        },
        "absolute_error": {
          "exact": "99",
          "decimal": "99.000000000000",
          "reason": null
        },
        "squared_error": {
          "exact": "9801",
          "decimal": "9801.000000000000",
          "reason": null
        },
        "training_scale": {
          "exact": null,
          "decimal": null,
          "reason": "zero_training_scale"
        },
        "scaled_absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "zero_training_scale"
        },
        "sha256": "722517caf07a6939f8152f0dd358973ff6e515c32ebeff8b74598446e54f408f"
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
        "dataset_sha256": "737e3f5fc2c3677979a49cb5072ee4f749ec0d3068da80b4b25c9f1cb3e9ad15",
        "source_sha256": null,
        "training_cutoff": "2020-03",
        "training_rows": 3,
        "training_prefix_sha256": "6a73c489a47c9c2dc76579bacb5f5b59fb822a9a5da5a62bc0b0b113c32016cc",
        "origin": "2020-03",
        "horizon": 3,
        "target_period": "2020-06",
        "partition": "forecast",
        "status": "success",
        "reason": null,
        "prediction": {
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "point_functional": "last observed value",
        "actual": "100",
        "error": {
          "exact": "99",
          "decimal": "99.000000000000",
          "reason": null
        },
        "absolute_error": {
          "exact": "99",
          "decimal": "99.000000000000",
          "reason": null
        },
        "squared_error": {
          "exact": "9801",
          "decimal": "9801.000000000000",
          "reason": null
        },
        "training_scale": {
          "exact": null,
          "decimal": null,
          "reason": "zero_training_scale"
        },
        "scaled_absolute_error": {
          "exact": null,
          "decimal": null,
          "reason": "zero_training_scale"
        },
        "sha256": "1012ad252f5216ac01a6ab7a42ece9ad7cf82594f7132853fef8f9471b29bda5"
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
              "value": "1"
            },
            {
              "period": "2020-03",
              "value": "1"
            },
            {
              "period": "2020-04",
              "value": "100"
            },
            {
              "period": "2020-05",
              "value": "100"
            },
            {
              "period": "2020-06",
              "value": "100"
            }
          ]
        }
      ]
    },
    "dataset_sha256": "737e3f5fc2c3677979a49cb5072ee4f749ec0d3068da80b4b25c9f1cb3e9ad15"
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
  "report_sha256": "485bdeb6046a97fc0a00d4c8834ee4713047f2d22ec6d897fe1f260ccc3fa37d"
}
```
