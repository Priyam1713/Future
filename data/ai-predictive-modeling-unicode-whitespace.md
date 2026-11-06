# CPU forecasting workbench

Retrospective evaluation on a fixed revised data snapshot;historical publication vintages are unverified. Software prefix isolation does not prove as-of historical data availability.

``````json
{
  "status": "accepted",
  "task": "forecast",
  "profile": {
    "id": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
    "version": 1,
    "sha256": "ed2490bf3ddc5861b3a406e2ba8aa93b3f2b2fe33e0b7917371e5c26875e7fdb"
  },
  "request_sha256": "6053ff89a596f23fe27fd55a584c69714993a22f32ce1897454da2464ec6be6c",
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
        "dataset_sha256": "0fbebfe72599f07c84fa7995425cb9c452acff96cea155cb203c873aec119495",
        "source_sha256": null,
        "training_cutoff": "2020-03",
        "training_rows": 3,
        "training_prefix_sha256": "be384a25c4c3fc8af8f2dadd9a7f4f2afa3d8bfcead76a1e18ab27fb1eb25944",
        "origin": "2020-03",
        "horizon": 1,
        "target_period": "2020-04",
        "partition": "forecast",
        "status": "success",
        "reason": null,
        "prediction": {
          "exact": "3",
          "decimal": "3.000000000000",
          "reason": null
        },
        "point_functional": "last observed value",
        "actual": "4",
        "error": {
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "absolute_error": {
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "squared_error": {
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "training_scale": {
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "scaled_absolute_error": {
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "sha256": "fd87c006ee5853d1e22a67fd8e2297c9c40a509f800b81b35ca6c24cdb06f3a7"
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
        "dataset_sha256": "0fbebfe72599f07c84fa7995425cb9c452acff96cea155cb203c873aec119495",
        "source_sha256": null,
        "training_cutoff": "2020-03",
        "training_rows": 3,
        "training_prefix_sha256": "be384a25c4c3fc8af8f2dadd9a7f4f2afa3d8bfcead76a1e18ab27fb1eb25944",
        "origin": "2020-03",
        "horizon": 2,
        "target_period": "2020-05",
        "partition": "forecast",
        "status": "success",
        "reason": null,
        "prediction": {
          "exact": "3",
          "decimal": "3.000000000000",
          "reason": null
        },
        "point_functional": "last observed value",
        "actual": "5",
        "error": {
          "exact": "2",
          "decimal": "2.000000000000",
          "reason": null
        },
        "absolute_error": {
          "exact": "2",
          "decimal": "2.000000000000",
          "reason": null
        },
        "squared_error": {
          "exact": "4",
          "decimal": "4.000000000000",
          "reason": null
        },
        "training_scale": {
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "scaled_absolute_error": {
          "exact": "2",
          "decimal": "2.000000000000",
          "reason": null
        },
        "sha256": "3c6d520c868a2c9f93ea6255723efc4fd5e54821f94b626875a16592b71795e1"
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
        "notes": "  Café 🪁\t\n`````json\n<script>raw</script>"
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
            },
            {
              "period": "2020-04",
              "value": "4"
            },
            {
              "period": "2020-05",
              "value": "5"
            },
            {
              "period": "2020-06",
              "value": "6"
            },
            {
              "period": "2020-07",
              "value": "7"
            },
            {
              "period": "2020-08",
              "value": "8"
            }
          ]
        }
      ]
    },
    "dataset_sha256": "0fbebfe72599f07c84fa7995425cb9c452acff96cea155cb203c873aec119495"
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
  "report_sha256": "9b0704c108431a26d6012fe5f0c503d8ac561857d167aaf3b6e7c59618f9a66b"
}
``````
