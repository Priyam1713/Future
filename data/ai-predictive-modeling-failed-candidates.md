# CPU forecasting workbench

Retrospective evaluation on a fixed revised data snapshot;historical publication vintages are unverified. Software prefix isolation does not prove as-of historical data availability.

Validation-selected model: naive

| Candidate | Validation MAE | Test MAE | Test RMSE | Test MASE |
|---|---:|---:|---:|---:|
| seasonal_naive_m12 | None | None | None | None |
| naive | 1.000000000000 | 1.000000000000 | 1.000000000000 | None |
| unknown | None | None | None | None |

Forecast windows overlap;300cells/model/partition represent36distinct NOAA target months,not300independent trials. No naive significance tests.

All cells,failures,horizon scores and paired comparisons follow.

```json
{
  "status": "accepted",
  "task": "evaluate",
  "profile": {
    "id": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
    "version": 1,
    "sha256": "ed2490bf3ddc5861b3a406e2ba8aa93b3f2b2fe33e0b7917371e5c26875e7fdb"
  },
  "request_sha256": "a28b8fede7e9f6fc02ca7b00f3f6437a7d5b9a49467b8c9c9096afdf22f39487",
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
    "evaluation": {
      "plan": {
        "models": [
          "seasonal_naive_m12",
          "naive",
          "unknown"
        ],
        "validation_origins": [
          "2020-02",
          "2020-03"
        ],
        "test_origins": [
          "2020-04",
          "2020-05"
        ],
        "horizons": [
          1
        ],
        "seasonal_period": 12,
        "selection": "validation_macro_mae_then_order"
      },
      "plan_sha256": "84482cd4bcbb203ca1f77572287b6176350984f9a97ea2afd388f9b4c9a89994",
      "selection": {
        "selected": "naive",
        "candidates": [
          {
            "model": "seasonal_naive_m12",
            "validation_macro_mae": {
              "exact": null,
              "decimal": null,
              "reason": "series_without_scored_pairs"
            },
            "eligible": false,
            "reason": "forecast_failure_or_empty_series"
          },
          {
            "model": "naive",
            "validation_macro_mae": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "eligible": true,
            "reason": null
          },
          {
            "model": "unknown",
            "validation_macro_mae": {
              "exact": null,
              "decimal": null,
              "reason": "series_without_scored_pairs"
            },
            "eligible": false,
            "reason": "forecast_failure_or_empty_series"
          }
        ],
        "tie_order": [
          "seasonal_naive_m12",
          "naive",
          "unknown"
        ],
        "rule": "Validation per-series macro MAE only;complete forecast coverage required. Test diagnostics never select.",
        "sha256": "d2b0684e5d257e1af068e9d26044b1c943b83d6eea199f55b200e7a3cd20c84c"
      },
      "summary": {
        "validation": [
          {
            "model": "seasonal_naive_m12",
            "aggregate": {
              "planned": 2,
              "scored": 0,
              "status_counts": {
                "success": 0,
                "missing_target": 0,
                "ineligible_origin": 0,
                "unsupported_configuration": 0,
                "model_failure": 2
              },
              "planned_distinct_target_months": 2,
              "distinct_target_months": 0,
              "mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mse": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "rmse": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "bias": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mase": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mase_count": 0,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
                "missing_training_target": 0
              },
              "wape": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "absolute_smape_percent": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
            },
            "by_series": {
              "synthetic1": {
                "planned": 2,
                "scored": 0,
                "status_counts": {
                  "success": 0,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 0,
                  "model_failure": 2
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 0,
                "mae": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "rmse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "bias": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "macro_mae": {
              "exact": null,
              "decimal": null,
              "reason": "series_without_scored_pairs"
            },
            "by_horizon": {
              "1": {
                "planned": 2,
                "scored": 0,
                "status_counts": {
                  "success": 0,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 0,
                  "model_failure": 2
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 0,
                "mae": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "rmse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "bias": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "paired_seasonal_naive": {
              "common_scored": 0,
              "candidate_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "candidate_minus_reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "ratio": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          },
          {
            "model": "naive",
            "aggregate": {
              "planned": 2,
              "scored": 2,
              "status_counts": {
                "success": 2,
                "missing_target": 0,
                "ineligible_origin": 0,
                "unsupported_configuration": 0,
                "model_failure": 0
              },
              "planned_distinct_target_months": 2,
              "distinct_target_months": 2,
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
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "mase": {
                "exact": null,
                "decimal": null,
                "reason": "insufficient_scale_history"
              },
              "mase_count": 0,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 2,
                "missing_training_target": 0
              },
              "wape": {
                "exact": "2/7",
                "decimal": "0.285714285714",
                "reason": null
              },
              "absolute_smape_percent": {
                "exact": null,
                "decimal": null,
                "reason": "manual_diagnostic_only_max20_pairs"
              },
              "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
            },
            "by_series": {
              "synthetic1": {
                "planned": 2,
                "scored": 2,
                "status_counts": {
                  "success": 2,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 0,
                  "model_failure": 0
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 2,
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
                  "exact": "1",
                  "decimal": "1.000000000000",
                  "reason": null
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "insufficient_scale_history"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 2,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "2/7",
                  "decimal": "0.285714285714",
                  "reason": null
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "manual_diagnostic_only_max20_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "macro_mae": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "by_horizon": {
              "1": {
                "planned": 2,
                "scored": 2,
                "status_counts": {
                  "success": 2,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 0,
                  "model_failure": 0
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 2,
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
                  "exact": "1",
                  "decimal": "1.000000000000",
                  "reason": null
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "insufficient_scale_history"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 2,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "2/7",
                  "decimal": "0.285714285714",
                  "reason": null
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "manual_diagnostic_only_max20_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "paired_seasonal_naive": {
              "common_scored": 0,
              "candidate_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "candidate_minus_reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "ratio": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          },
          {
            "model": "unknown",
            "aggregate": {
              "planned": 2,
              "scored": 0,
              "status_counts": {
                "success": 0,
                "missing_target": 0,
                "ineligible_origin": 0,
                "unsupported_configuration": 2,
                "model_failure": 0
              },
              "planned_distinct_target_months": 2,
              "distinct_target_months": 0,
              "mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mse": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "rmse": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "bias": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mase": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mase_count": 0,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
                "missing_training_target": 0
              },
              "wape": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "absolute_smape_percent": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
            },
            "by_series": {
              "synthetic1": {
                "planned": 2,
                "scored": 0,
                "status_counts": {
                  "success": 0,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 2,
                  "model_failure": 0
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 0,
                "mae": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "rmse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "bias": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "macro_mae": {
              "exact": null,
              "decimal": null,
              "reason": "series_without_scored_pairs"
            },
            "by_horizon": {
              "1": {
                "planned": 2,
                "scored": 0,
                "status_counts": {
                  "success": 0,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 2,
                  "model_failure": 0
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 0,
                "mae": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "rmse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "bias": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "paired_seasonal_naive": {
              "common_scored": 0,
              "candidate_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "candidate_minus_reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "ratio": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          }
        ],
        "test": [
          {
            "model": "seasonal_naive_m12",
            "aggregate": {
              "planned": 2,
              "scored": 0,
              "status_counts": {
                "success": 0,
                "missing_target": 0,
                "ineligible_origin": 0,
                "unsupported_configuration": 0,
                "model_failure": 2
              },
              "planned_distinct_target_months": 2,
              "distinct_target_months": 0,
              "mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mse": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "rmse": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "bias": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mase": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mase_count": 0,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
                "missing_training_target": 0
              },
              "wape": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "absolute_smape_percent": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
            },
            "by_series": {
              "synthetic1": {
                "planned": 2,
                "scored": 0,
                "status_counts": {
                  "success": 0,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 0,
                  "model_failure": 2
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 0,
                "mae": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "rmse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "bias": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "macro_mae": {
              "exact": null,
              "decimal": null,
              "reason": "series_without_scored_pairs"
            },
            "by_horizon": {
              "1": {
                "planned": 2,
                "scored": 0,
                "status_counts": {
                  "success": 0,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 0,
                  "model_failure": 2
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 0,
                "mae": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "rmse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "bias": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "paired_seasonal_naive": {
              "common_scored": 0,
              "candidate_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "candidate_minus_reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "ratio": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          },
          {
            "model": "naive",
            "aggregate": {
              "planned": 2,
              "scored": 2,
              "status_counts": {
                "success": 2,
                "missing_target": 0,
                "ineligible_origin": 0,
                "unsupported_configuration": 0,
                "model_failure": 0
              },
              "planned_distinct_target_months": 2,
              "distinct_target_months": 2,
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
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "mase": {
                "exact": null,
                "decimal": null,
                "reason": "insufficient_scale_history"
              },
              "mase_count": 0,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 2,
                "missing_training_target": 0
              },
              "wape": {
                "exact": "2/11",
                "decimal": "0.181818181818",
                "reason": null
              },
              "absolute_smape_percent": {
                "exact": null,
                "decimal": null,
                "reason": "manual_diagnostic_only_max20_pairs"
              },
              "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
            },
            "by_series": {
              "synthetic1": {
                "planned": 2,
                "scored": 2,
                "status_counts": {
                  "success": 2,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 0,
                  "model_failure": 0
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 2,
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
                  "exact": "1",
                  "decimal": "1.000000000000",
                  "reason": null
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "insufficient_scale_history"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 2,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "2/11",
                  "decimal": "0.181818181818",
                  "reason": null
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "manual_diagnostic_only_max20_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "macro_mae": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "by_horizon": {
              "1": {
                "planned": 2,
                "scored": 2,
                "status_counts": {
                  "success": 2,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 0,
                  "model_failure": 0
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 2,
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
                  "exact": "1",
                  "decimal": "1.000000000000",
                  "reason": null
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "insufficient_scale_history"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 2,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "2/11",
                  "decimal": "0.181818181818",
                  "reason": null
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "manual_diagnostic_only_max20_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "paired_seasonal_naive": {
              "common_scored": 0,
              "candidate_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "candidate_minus_reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "ratio": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          },
          {
            "model": "unknown",
            "aggregate": {
              "planned": 2,
              "scored": 0,
              "status_counts": {
                "success": 0,
                "missing_target": 0,
                "ineligible_origin": 0,
                "unsupported_configuration": 2,
                "model_failure": 0
              },
              "planned_distinct_target_months": 2,
              "distinct_target_months": 0,
              "mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mse": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "rmse": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "bias": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mase": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "mase_count": 0,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
                "missing_training_target": 0
              },
              "wape": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "absolute_smape_percent": {
                "exact": null,
                "decimal": null,
                "reason": "no_scored_pairs"
              },
              "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
            },
            "by_series": {
              "synthetic1": {
                "planned": 2,
                "scored": 0,
                "status_counts": {
                  "success": 0,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 2,
                  "model_failure": 0
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 0,
                "mae": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "rmse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "bias": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "macro_mae": {
              "exact": null,
              "decimal": null,
              "reason": "series_without_scored_pairs"
            },
            "by_horizon": {
              "1": {
                "planned": 2,
                "scored": 0,
                "status_counts": {
                  "success": 0,
                  "missing_target": 0,
                  "ineligible_origin": 0,
                  "unsupported_configuration": 2,
                  "model_failure": 0
                },
                "planned_distinct_target_months": 2,
                "distinct_target_months": 0,
                "mae": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "rmse": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "bias": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "mase_count": 0,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "absolute_smape_percent": {
                  "exact": null,
                  "decimal": null,
                  "reason": "no_scored_pairs"
                },
                "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
              }
            },
            "paired_seasonal_naive": {
              "common_scored": 0,
              "candidate_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "candidate_minus_reference_mae": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "ratio": {
                "exact": null,
                "decimal": null,
                "reason": "no_common_pairs"
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          }
        ]
      },
      "cells": {
        "validation": [
          {
            "model": {
              "id": "seasonal_naive_m12",
              "version": 1,
              "family": "seasonal_naive",
              "alpha": null,
              "seasonal_period": 12,
              "initialization": null
            },
            "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
            "profile_version": 1,
            "series_id": "synthetic1",
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-02",
            "training_rows": 2,
            "training_prefix_sha256": "a663d15c7aac44daf61a6be150ca99d0c16dde7271f4cecfe7a8828e9c6fd1e6",
            "origin": "2020-02",
            "horizon": 1,
            "target_period": "2020-03",
            "partition": "validation",
            "status": "model_failure",
            "reason": "Insufficient seasonal history",
            "prediction": {
              "exact": null,
              "decimal": null,
              "reason": "forecast_unavailable"
            },
            "point_functional": "last observed seasonal value",
            "actual": "3",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "473aa5a9a21260c54a7db0b0f7c7cdfe2a4476293457be195b04fb2324decf42"
          },
          {
            "model": {
              "id": "seasonal_naive_m12",
              "version": 1,
              "family": "seasonal_naive",
              "alpha": null,
              "seasonal_period": 12,
              "initialization": null
            },
            "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
            "profile_version": 1,
            "series_id": "synthetic1",
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-03",
            "training_rows": 3,
            "training_prefix_sha256": "be384a25c4c3fc8af8f2dadd9a7f4f2afa3d8bfcead76a1e18ab27fb1eb25944",
            "origin": "2020-03",
            "horizon": 1,
            "target_period": "2020-04",
            "partition": "validation",
            "status": "model_failure",
            "reason": "Insufficient seasonal history",
            "prediction": {
              "exact": null,
              "decimal": null,
              "reason": "forecast_unavailable"
            },
            "point_functional": "last observed seasonal value",
            "actual": "4",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "ddbada010c11eecb1ad647692e52c3cec8bb8540909cc64f9f304ed12ed10575"
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
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-02",
            "training_rows": 2,
            "training_prefix_sha256": "a663d15c7aac44daf61a6be150ca99d0c16dde7271f4cecfe7a8828e9c6fd1e6",
            "origin": "2020-02",
            "horizon": 1,
            "target_period": "2020-03",
            "partition": "validation",
            "status": "success",
            "reason": null,
            "prediction": {
              "exact": "2",
              "decimal": "2.000000000000",
              "reason": null
            },
            "point_functional": "last observed value",
            "actual": "3",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "35b6c8a75f4c5b3af033b6e27a4a1381c5b3e97a9c0dad9f9dd37b9a6dcee913"
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
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-03",
            "training_rows": 3,
            "training_prefix_sha256": "be384a25c4c3fc8af8f2dadd9a7f4f2afa3d8bfcead76a1e18ab27fb1eb25944",
            "origin": "2020-03",
            "horizon": 1,
            "target_period": "2020-04",
            "partition": "validation",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "74aac31836b6b2cafbca67d8e59c83f73b924db6ba12ab11cca2475c51609604"
          },
          {
            "model": {
              "id": "unknown",
              "version": null
            },
            "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
            "profile_version": 1,
            "series_id": "synthetic1",
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-02",
            "training_rows": 2,
            "training_prefix_sha256": "a663d15c7aac44daf61a6be150ca99d0c16dde7271f4cecfe7a8828e9c6fd1e6",
            "origin": "2020-02",
            "horizon": 1,
            "target_period": "2020-03",
            "partition": "validation",
            "status": "unsupported_configuration",
            "reason": "unsupported_model_or_season",
            "prediction": {
              "exact": null,
              "decimal": null,
              "reason": "forecast_unavailable"
            },
            "point_functional": "unsupported",
            "actual": "3",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "9de28bcea209ad50a16111822d1ea78c0ae9a429b6247b7b50eb9d430411dfc1"
          },
          {
            "model": {
              "id": "unknown",
              "version": null
            },
            "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
            "profile_version": 1,
            "series_id": "synthetic1",
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-03",
            "training_rows": 3,
            "training_prefix_sha256": "be384a25c4c3fc8af8f2dadd9a7f4f2afa3d8bfcead76a1e18ab27fb1eb25944",
            "origin": "2020-03",
            "horizon": 1,
            "target_period": "2020-04",
            "partition": "validation",
            "status": "unsupported_configuration",
            "reason": "unsupported_model_or_season",
            "prediction": {
              "exact": null,
              "decimal": null,
              "reason": "forecast_unavailable"
            },
            "point_functional": "unsupported",
            "actual": "4",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "0322b3f099c4dc213b5fc0b6b1c84a319530300c32bc4c64fc42a48ef093c4a2"
          }
        ],
        "test": [
          {
            "model": {
              "id": "seasonal_naive_m12",
              "version": 1,
              "family": "seasonal_naive",
              "alpha": null,
              "seasonal_period": 12,
              "initialization": null
            },
            "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
            "profile_version": 1,
            "series_id": "synthetic1",
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-04",
            "training_rows": 4,
            "training_prefix_sha256": "7e5c5c1ffca9c41771f2fcb670fc8f57137ea7ab8cbb8e46d15de406e012b649",
            "origin": "2020-04",
            "horizon": 1,
            "target_period": "2020-05",
            "partition": "test",
            "status": "model_failure",
            "reason": "Insufficient seasonal history",
            "prediction": {
              "exact": null,
              "decimal": null,
              "reason": "forecast_unavailable"
            },
            "point_functional": "last observed seasonal value",
            "actual": "5",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "a0c50d485c57cf6b02a943a67e988c8e5393bfeb08d07b039e1d9cf7ac99c8ae"
          },
          {
            "model": {
              "id": "seasonal_naive_m12",
              "version": 1,
              "family": "seasonal_naive",
              "alpha": null,
              "seasonal_period": 12,
              "initialization": null
            },
            "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
            "profile_version": 1,
            "series_id": "synthetic1",
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-05",
            "training_rows": 5,
            "training_prefix_sha256": "bff1034f7cfa80e6237cbe6983fd20603da357222792fcf886cbd0db9fe8e4a3",
            "origin": "2020-05",
            "horizon": 1,
            "target_period": "2020-06",
            "partition": "test",
            "status": "model_failure",
            "reason": "Insufficient seasonal history",
            "prediction": {
              "exact": null,
              "decimal": null,
              "reason": "forecast_unavailable"
            },
            "point_functional": "last observed seasonal value",
            "actual": "6",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "1f6434a3afb2a842bffc18385326903a2da19e55f07cbc0c42717e203d8a2f6b"
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
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-04",
            "training_rows": 4,
            "training_prefix_sha256": "7e5c5c1ffca9c41771f2fcb670fc8f57137ea7ab8cbb8e46d15de406e012b649",
            "origin": "2020-04",
            "horizon": 1,
            "target_period": "2020-05",
            "partition": "test",
            "status": "success",
            "reason": null,
            "prediction": {
              "exact": "4",
              "decimal": "4.000000000000",
              "reason": null
            },
            "point_functional": "last observed value",
            "actual": "5",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "0610f6d1e7b2c972231839d99da2045c083966ce8729a71bc9e2ec7da98c0b6f"
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
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-05",
            "training_rows": 5,
            "training_prefix_sha256": "bff1034f7cfa80e6237cbe6983fd20603da357222792fcf886cbd0db9fe8e4a3",
            "origin": "2020-05",
            "horizon": 1,
            "target_period": "2020-06",
            "partition": "test",
            "status": "success",
            "reason": null,
            "prediction": {
              "exact": "5",
              "decimal": "5.000000000000",
              "reason": null
            },
            "point_functional": "last observed value",
            "actual": "6",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "c1d5b4c701c8eb774ff67d16bffbf299cda02ef0f3ba544f21bfd77138197426"
          },
          {
            "model": {
              "id": "unknown",
              "version": null
            },
            "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
            "profile_version": 1,
            "series_id": "synthetic1",
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-04",
            "training_rows": 4,
            "training_prefix_sha256": "7e5c5c1ffca9c41771f2fcb670fc8f57137ea7ab8cbb8e46d15de406e012b649",
            "origin": "2020-04",
            "horizon": 1,
            "target_period": "2020-05",
            "partition": "test",
            "status": "unsupported_configuration",
            "reason": "unsupported_model_or_season",
            "prediction": {
              "exact": null,
              "decimal": null,
              "reason": "forecast_unavailable"
            },
            "point_functional": "unsupported",
            "actual": "5",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "9f7afb3c06b6e4e152a9f232ed02e3c4d176a2408b993ef8f3c73682d1e631f4"
          },
          {
            "model": {
              "id": "unknown",
              "version": null
            },
            "profile": "fpp3-noaa-monthly-rolling-origin-baselines-v1",
            "profile_version": 1,
            "series_id": "synthetic1",
            "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4",
            "source_sha256": null,
            "training_cutoff": "2020-05",
            "training_rows": 5,
            "training_prefix_sha256": "bff1034f7cfa80e6237cbe6983fd20603da357222792fcf886cbd0db9fe8e4a3",
            "origin": "2020-05",
            "horizon": 1,
            "target_period": "2020-06",
            "partition": "test",
            "status": "unsupported_configuration",
            "reason": "unsupported_model_or_season",
            "prediction": {
              "exact": null,
              "decimal": null,
              "reason": "forecast_unavailable"
            },
            "point_functional": "unsupported",
            "actual": "6",
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
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "scaled_absolute_error": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "sha256": "d473b1e887a2f5a1f408eed623d5831fc20f9db869632ea3501538b74b8d3b19"
          }
        ]
      },
      "primary_selected_test": {
        "model": "naive",
        "aggregate": {
          "planned": 2,
          "scored": 2,
          "status_counts": {
            "success": 2,
            "missing_target": 0,
            "ineligible_origin": 0,
            "unsupported_configuration": 0,
            "model_failure": 0
          },
          "planned_distinct_target_months": 2,
          "distinct_target_months": 2,
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
            "exact": "1",
            "decimal": "1.000000000000",
            "reason": null
          },
          "mase": {
            "exact": null,
            "decimal": null,
            "reason": "insufficient_scale_history"
          },
          "mase_count": 0,
          "undefined_scale_counts": {
            "zero_training_scale": 0,
            "insufficient_scale_history": 2,
            "missing_training_target": 0
          },
          "wape": {
            "exact": "2/11",
            "decimal": "0.181818181818",
            "reason": null
          },
          "absolute_smape_percent": {
            "exact": null,
            "decimal": null,
            "reason": "manual_diagnostic_only_max20_pairs"
          },
          "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
        },
        "by_series": {
          "synthetic1": {
            "planned": 2,
            "scored": 2,
            "status_counts": {
              "success": 2,
              "missing_target": 0,
              "ineligible_origin": 0,
              "unsupported_configuration": 0,
              "model_failure": 0
            },
            "planned_distinct_target_months": 2,
            "distinct_target_months": 2,
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
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "mase": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "mase_count": 0,
            "undefined_scale_counts": {
              "zero_training_scale": 0,
              "insufficient_scale_history": 2,
              "missing_training_target": 0
            },
            "wape": {
              "exact": "2/11",
              "decimal": "0.181818181818",
              "reason": null
            },
            "absolute_smape_percent": {
              "exact": null,
              "decimal": null,
              "reason": "manual_diagnostic_only_max20_pairs"
            },
            "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
          }
        },
        "macro_mae": {
          "exact": "1",
          "decimal": "1.000000000000",
          "reason": null
        },
        "by_horizon": {
          "1": {
            "planned": 2,
            "scored": 2,
            "status_counts": {
              "success": 2,
              "missing_target": 0,
              "ineligible_origin": 0,
              "unsupported_configuration": 0,
              "model_failure": 0
            },
            "planned_distinct_target_months": 2,
            "distinct_target_months": 2,
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
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "mase": {
              "exact": null,
              "decimal": null,
              "reason": "insufficient_scale_history"
            },
            "mase_count": 0,
            "undefined_scale_counts": {
              "zero_training_scale": 0,
              "insufficient_scale_history": 2,
              "missing_training_target": 0
            },
            "wape": {
              "exact": "2/11",
              "decimal": "0.181818181818",
              "reason": null
            },
            "absolute_smape_percent": {
              "exact": null,
              "decimal": null,
              "reason": "manual_diagnostic_only_max20_pairs"
            },
            "smape_convention": "Editorial absolute denominator,double-zero term0;not the signed denominator in FPP3. Diagnostic only."
          }
        },
        "paired_seasonal_naive": {
          "common_scored": 0,
          "candidate_mae": {
            "exact": null,
            "decimal": null,
            "reason": "no_common_pairs"
          },
          "reference_mae": {
            "exact": null,
            "decimal": null,
            "reason": "no_common_pairs"
          },
          "candidate_minus_reference_mae": {
            "exact": null,
            "decimal": null,
            "reason": "no_common_pairs"
          },
          "ratio": {
            "exact": null,
            "decimal": null,
            "reason": "no_common_pairs"
          },
          "reference_model": "seasonal_naive",
          "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
        }
      },
      "test_all_candidates_role": "Diagnostic reporting only;not a second selection stage.",
      "weighting": "Macro weights series equally;micro weights scored cells equally. With one series they coincide. MASE uses per-origin scales.",
      "dependence": "Forecast windows overlap;300cells/model/partition represent36distinct NOAA target months,not300independent trials. No naive significance tests.",
      "vintage": "Retrospective evaluation on a fixed revised data snapshot;historical publication vintages are unverified. Software prefix isolation does not prove as-of historical data availability."
    },
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
    "dataset_sha256": "7f7171c934b2883847726b661f9a06097e3b664dfdc433340833926d32714be4"
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
  "report_sha256": "ceac9e0c1fdb9b9c1a0cad4eedfdd152c308a00ac6ae85a4fb02e256d5e30dc9"
}
```
