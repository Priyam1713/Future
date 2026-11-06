# CPU forecasting workbench

Retrospective evaluation on a fixed revised data snapshot;historical publication vintages are unverified. Software prefix isolation does not prove as-of historical data availability.

```json
{
  "status": "accepted",
  "task": "metrics",
  "profile": {
    "id": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
    "version": 1,
    "sha256": "ed2490bf3ddc5861b3a406e2ba8aa93b3f2b2fe33e0b7917371e5c26875e7fdb"
  },
  "request_sha256": "a1bb9c8b08ef8491992df4a6e8f2e2165c6c58904fd5e96e7e9cd20e74bdf5a1",
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
    "planned": 1,
    "scored": 1,
    "status_counts": {
      "success": 1,
      "missing_target": 0,
      "ineligible_origin": 0,
      "unsupported_configuration": 0,
      "model_failure": 0
    },
    "planned_distinct_target_months": 1,
    "distinct_target_months": 1,
    "mae": {
      "exact": "1",
      "decimal": "1.000000000000",
      "reason": null
    },
    "mse": {
      "exact": "1",
      "decimal": "1.000000000000",
      "reason": null
    },
    "rmse": {
      "exact": "sqrt(1)",
      "decimal": "1.000000000000",
      "reason": null
    },
    "bias": {
      "exact": "-1",
      "decimal": "-1.000000000000",
      "reason": null
    },
    "mase": {
      "exact": "1",
      "decimal": "1.000000000000",
      "reason": null
    },
    "mase_count": 1,
    "undefined_scale_counts": {
      "zero_training_scale": 0,
      "insufficient_scale_history": 0,
      "missing_training_target": 0
    },
    "wape": {
      "exact": null,
      "decimal": null,
      "reason": "zero_actual_denominator"
    },
    "absolute_smape_percent": {
      "exact": "200",
      "decimal": "200.000000000000",
      "reason": null
    },
    "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
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
  "report_sha256": "338f5b7e9a97c7fc32264f2f2cf29a158ba56162c4fd07a54922589eb87c730e"
}
```
