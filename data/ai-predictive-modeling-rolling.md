# CPU forecasting workbench

Retrospective evaluation on a fixed revised data snapshot;historical publication vintages are unverified. Software prefix isolation does not prove as-of historical data availability.

Validation-selected model: drift

| Candidate | Validation MAE | Test MAE | Test RMSE | Test MASE |
|---|---:|---:|---:|---:|
| naive | 1.000000000000 | 1.000000000000 | 1.000000000000 | 1.000000000000 |
| mean | 1.750000000000 | 2.750000000000 | 2.761340254297 | 2.750000000000 |
| drift | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.000000000000 |
| ses_alpha0.2_initial_y1 | 2.120000000000 | 3.156800000000 | 3.163436308826 | 3.156800000000 |

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
  "request_sha256": "fc473577ce6e47e3c98bc48d0b98ff5e985ff0ea1f8ffdbbbbb219f0ed508716",
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
          "naive",
          "mean",
          "drift",
          "ses_alpha0.2_initial_y1"
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
        "seasonal_period": 1,
        "selection": "validation_macro_mae_then_order"
      },
      "plan_sha256": "ccff48531215a03a31a614ab59d123c5bd304de92bad63b8215f4c485b0161cd",
      "selection": {
        "selected": "drift",
        "candidates": [
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
            "model": "mean",
            "validation_macro_mae": {
              "exact": "7/4",
              "decimal": "1.750000000000",
              "reason": null
            },
            "eligible": true,
            "reason": null
          },
          {
            "model": "drift",
            "validation_macro_mae": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "eligible": true,
            "reason": null
          },
          {
            "model": "ses_alpha0.2_initial_y1",
            "validation_macro_mae": {
              "exact": "53/25",
              "decimal": "2.120000000000",
              "reason": null
            },
            "eligible": true,
            "reason": null
          }
        ],
        "tie_order": [
          "naive",
          "mean",
          "drift",
          "ses_alpha0.2_initial_y1"
        ],
        "rule": "Validation per-series macro MAE only;complete forecast coverage required. Test diagnostics never select.",
        "sha256": "2b6f5f8f5b69bfe666c055d38db6154430cbd36ac3ab44c1eb886dcfaad588e4"
      },
      "summary": {
        "validation": [
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
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "mase_count": 2,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
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
                  "exact": "1",
                  "decimal": "1.000000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
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
                  "exact": "1",
                  "decimal": "1.000000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
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
              "common_scored": 2,
              "candidate_mae": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "reference_mae": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "candidate_minus_reference_mae": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "ratio": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          },
          {
            "model": "mean",
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
                "exact": "7/4",
                "decimal": "1.750000000000",
                "reason": null
              },
              "mse": {
                "exact": "25/8",
                "decimal": "3.125000000000",
                "reason": null
              },
              "rmse": {
                "exact": "sqrt(25/8)",
                "decimal": "1.767766952966",
                "reason": null
              },
              "bias": {
                "exact": "7/4",
                "decimal": "1.750000000000",
                "reason": null
              },
              "mase": {
                "exact": "7/4",
                "decimal": "1.750000000000",
                "reason": null
              },
              "mase_count": 2,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
                "missing_training_target": 0
              },
              "wape": {
                "exact": "1/2",
                "decimal": "0.500000000000",
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
                  "exact": "7/4",
                  "decimal": "1.750000000000",
                  "reason": null
                },
                "mse": {
                  "exact": "25/8",
                  "decimal": "3.125000000000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(25/8)",
                  "decimal": "1.767766952966",
                  "reason": null
                },
                "bias": {
                  "exact": "7/4",
                  "decimal": "1.750000000000",
                  "reason": null
                },
                "mase": {
                  "exact": "7/4",
                  "decimal": "1.750000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "1/2",
                  "decimal": "0.500000000000",
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
              "exact": "7/4",
              "decimal": "1.750000000000",
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
                  "exact": "7/4",
                  "decimal": "1.750000000000",
                  "reason": null
                },
                "mse": {
                  "exact": "25/8",
                  "decimal": "3.125000000000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(25/8)",
                  "decimal": "1.767766952966",
                  "reason": null
                },
                "bias": {
                  "exact": "7/4",
                  "decimal": "1.750000000000",
                  "reason": null
                },
                "mase": {
                  "exact": "7/4",
                  "decimal": "1.750000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "1/2",
                  "decimal": "0.500000000000",
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
              "common_scored": 2,
              "candidate_mae": {
                "exact": "7/4",
                "decimal": "1.750000000000",
                "reason": null
              },
              "reference_mae": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "candidate_minus_reference_mae": {
                "exact": "3/4",
                "decimal": "0.750000000000",
                "reason": null
              },
              "ratio": {
                "exact": "7/4",
                "decimal": "1.750000000000",
                "reason": null
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          },
          {
            "model": "drift",
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
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "mse": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "rmse": {
                "exact": "sqrt(0)",
                "decimal": "0.000000000000",
                "reason": null
              },
              "bias": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "mase": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "mase_count": 2,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
                "missing_training_target": 0
              },
              "wape": {
                "exact": "0",
                "decimal": "0.000000000000",
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
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mse": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(0)",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "bias": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mase": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "0",
                  "decimal": "0.000000000000",
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
              "exact": "0",
              "decimal": "0.000000000000",
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
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mse": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(0)",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "bias": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mase": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "0",
                  "decimal": "0.000000000000",
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
              "common_scored": 2,
              "candidate_mae": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "reference_mae": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "candidate_minus_reference_mae": {
                "exact": "-1",
                "decimal": "-1.000000000000",
                "reason": null
              },
              "ratio": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          },
          {
            "model": "ses_alpha0.2_initial_y1",
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
                "exact": "53/25",
                "decimal": "2.120000000000",
                "reason": null
              },
              "mse": {
                "exact": "2873/625",
                "decimal": "4.596800000000",
                "reason": null
              },
              "rmse": {
                "exact": "sqrt(2873/625)",
                "decimal": "2.144014925321",
                "reason": null
              },
              "bias": {
                "exact": "53/25",
                "decimal": "2.120000000000",
                "reason": null
              },
              "mase": {
                "exact": "53/25",
                "decimal": "2.120000000000",
                "reason": null
              },
              "mase_count": 2,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
                "missing_training_target": 0
              },
              "wape": {
                "exact": "106/175",
                "decimal": "0.605714285714",
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
                  "exact": "53/25",
                  "decimal": "2.120000000000",
                  "reason": null
                },
                "mse": {
                  "exact": "2873/625",
                  "decimal": "4.596800000000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(2873/625)",
                  "decimal": "2.144014925321",
                  "reason": null
                },
                "bias": {
                  "exact": "53/25",
                  "decimal": "2.120000000000",
                  "reason": null
                },
                "mase": {
                  "exact": "53/25",
                  "decimal": "2.120000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "106/175",
                  "decimal": "0.605714285714",
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
              "exact": "53/25",
              "decimal": "2.120000000000",
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
                  "exact": "53/25",
                  "decimal": "2.120000000000",
                  "reason": null
                },
                "mse": {
                  "exact": "2873/625",
                  "decimal": "4.596800000000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(2873/625)",
                  "decimal": "2.144014925321",
                  "reason": null
                },
                "bias": {
                  "exact": "53/25",
                  "decimal": "2.120000000000",
                  "reason": null
                },
                "mase": {
                  "exact": "53/25",
                  "decimal": "2.120000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "106/175",
                  "decimal": "0.605714285714",
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
              "common_scored": 2,
              "candidate_mae": {
                "exact": "53/25",
                "decimal": "2.120000000000",
                "reason": null
              },
              "reference_mae": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "candidate_minus_reference_mae": {
                "exact": "28/25",
                "decimal": "1.120000000000",
                "reason": null
              },
              "ratio": {
                "exact": "53/25",
                "decimal": "2.120000000000",
                "reason": null
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          }
        ],
        "test": [
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
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "mase_count": 2,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
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
                  "exact": "1",
                  "decimal": "1.000000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
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
                  "exact": "1",
                  "decimal": "1.000000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
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
              "common_scored": 2,
              "candidate_mae": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "reference_mae": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "candidate_minus_reference_mae": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "ratio": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          },
          {
            "model": "mean",
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
                "exact": "11/4",
                "decimal": "2.750000000000",
                "reason": null
              },
              "mse": {
                "exact": "61/8",
                "decimal": "7.625000000000",
                "reason": null
              },
              "rmse": {
                "exact": "sqrt(61/8)",
                "decimal": "2.761340254297",
                "reason": null
              },
              "bias": {
                "exact": "11/4",
                "decimal": "2.750000000000",
                "reason": null
              },
              "mase": {
                "exact": "11/4",
                "decimal": "2.750000000000",
                "reason": null
              },
              "mase_count": 2,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
                "missing_training_target": 0
              },
              "wape": {
                "exact": "1/2",
                "decimal": "0.500000000000",
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
                  "exact": "11/4",
                  "decimal": "2.750000000000",
                  "reason": null
                },
                "mse": {
                  "exact": "61/8",
                  "decimal": "7.625000000000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(61/8)",
                  "decimal": "2.761340254297",
                  "reason": null
                },
                "bias": {
                  "exact": "11/4",
                  "decimal": "2.750000000000",
                  "reason": null
                },
                "mase": {
                  "exact": "11/4",
                  "decimal": "2.750000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "1/2",
                  "decimal": "0.500000000000",
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
              "exact": "11/4",
              "decimal": "2.750000000000",
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
                  "exact": "11/4",
                  "decimal": "2.750000000000",
                  "reason": null
                },
                "mse": {
                  "exact": "61/8",
                  "decimal": "7.625000000000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(61/8)",
                  "decimal": "2.761340254297",
                  "reason": null
                },
                "bias": {
                  "exact": "11/4",
                  "decimal": "2.750000000000",
                  "reason": null
                },
                "mase": {
                  "exact": "11/4",
                  "decimal": "2.750000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "1/2",
                  "decimal": "0.500000000000",
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
              "common_scored": 2,
              "candidate_mae": {
                "exact": "11/4",
                "decimal": "2.750000000000",
                "reason": null
              },
              "reference_mae": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "candidate_minus_reference_mae": {
                "exact": "7/4",
                "decimal": "1.750000000000",
                "reason": null
              },
              "ratio": {
                "exact": "11/4",
                "decimal": "2.750000000000",
                "reason": null
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          },
          {
            "model": "drift",
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
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "mse": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "rmse": {
                "exact": "sqrt(0)",
                "decimal": "0.000000000000",
                "reason": null
              },
              "bias": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "mase": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "mase_count": 2,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
                "missing_training_target": 0
              },
              "wape": {
                "exact": "0",
                "decimal": "0.000000000000",
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
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mse": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(0)",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "bias": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mase": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "0",
                  "decimal": "0.000000000000",
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
              "exact": "0",
              "decimal": "0.000000000000",
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
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mse": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(0)",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "bias": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mase": {
                  "exact": "0",
                  "decimal": "0.000000000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "0",
                  "decimal": "0.000000000000",
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
              "common_scored": 2,
              "candidate_mae": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "reference_mae": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "candidate_minus_reference_mae": {
                "exact": "-1",
                "decimal": "-1.000000000000",
                "reason": null
              },
              "ratio": {
                "exact": "0",
                "decimal": "0.000000000000",
                "reason": null
              },
              "reference_model": "seasonal_naive",
              "direction": "Negative MAE difference or ratio<1 favors candidate;comparison limited to common eligible cells."
            }
          },
          {
            "model": "ses_alpha0.2_initial_y1",
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
                "exact": "1973/625",
                "decimal": "3.156800000000",
                "reason": null
              },
              "mse": {
                "exact": "3909113/390625",
                "decimal": "10.007329280000",
                "reason": null
              },
              "rmse": {
                "exact": "sqrt(3909113/390625)",
                "decimal": "3.163436308826",
                "reason": null
              },
              "bias": {
                "exact": "1973/625",
                "decimal": "3.156800000000",
                "reason": null
              },
              "mase": {
                "exact": "1973/625",
                "decimal": "3.156800000000",
                "reason": null
              },
              "mase_count": 2,
              "undefined_scale_counts": {
                "zero_training_scale": 0,
                "insufficient_scale_history": 0,
                "missing_training_target": 0
              },
              "wape": {
                "exact": "3946/6875",
                "decimal": "0.573963636364",
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
                  "exact": "1973/625",
                  "decimal": "3.156800000000",
                  "reason": null
                },
                "mse": {
                  "exact": "3909113/390625",
                  "decimal": "10.007329280000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(3909113/390625)",
                  "decimal": "3.163436308826",
                  "reason": null
                },
                "bias": {
                  "exact": "1973/625",
                  "decimal": "3.156800000000",
                  "reason": null
                },
                "mase": {
                  "exact": "1973/625",
                  "decimal": "3.156800000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "3946/6875",
                  "decimal": "0.573963636364",
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
              "exact": "1973/625",
              "decimal": "3.156800000000",
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
                  "exact": "1973/625",
                  "decimal": "3.156800000000",
                  "reason": null
                },
                "mse": {
                  "exact": "3909113/390625",
                  "decimal": "10.007329280000",
                  "reason": null
                },
                "rmse": {
                  "exact": "sqrt(3909113/390625)",
                  "decimal": "3.163436308826",
                  "reason": null
                },
                "bias": {
                  "exact": "1973/625",
                  "decimal": "3.156800000000",
                  "reason": null
                },
                "mase": {
                  "exact": "1973/625",
                  "decimal": "3.156800000000",
                  "reason": null
                },
                "mase_count": 2,
                "undefined_scale_counts": {
                  "zero_training_scale": 0,
                  "insufficient_scale_history": 0,
                  "missing_training_target": 0
                },
                "wape": {
                  "exact": "3946/6875",
                  "decimal": "0.573963636364",
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
              "common_scored": 2,
              "candidate_mae": {
                "exact": "1973/625",
                "decimal": "3.156800000000",
                "reason": null
              },
              "reference_mae": {
                "exact": "1",
                "decimal": "1.000000000000",
                "reason": null
              },
              "candidate_minus_reference_mae": {
                "exact": "1348/625",
                "decimal": "2.156800000000",
                "reason": null
              },
              "ratio": {
                "exact": "1973/625",
                "decimal": "3.156800000000",
                "reason": null
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
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "sha256": "fb3c7fa14dd3a4664b9bc241284f53d293ebb5f57363d468273d373beacdcbbd"
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
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "sha256": "fb757511dc80ea9b96581e80676857eb71eb5ad8c7e0b1e7b26a78de9b9f0bd4"
          },
          {
            "model": {
              "id": "mean",
              "version": 1,
              "family": "mean",
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
              "exact": "3/2",
              "decimal": "1.500000000000",
              "reason": null
            },
            "point_functional": "training arithmetic mean",
            "actual": "3",
            "error": {
              "exact": "3/2",
              "decimal": "1.500000000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "3/2",
              "decimal": "1.500000000000",
              "reason": null
            },
            "squared_error": {
              "exact": "9/4",
              "decimal": "2.250000000000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "3/2",
              "decimal": "1.500000000000",
              "reason": null
            },
            "sha256": "74261eed4fd596725314a86b59155a6257892b30e78b3df101c997eb3ee58a5b"
          },
          {
            "model": {
              "id": "mean",
              "version": 1,
              "family": "mean",
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
              "exact": "2",
              "decimal": "2.000000000000",
              "reason": null
            },
            "point_functional": "training arithmetic mean",
            "actual": "4",
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
            "sha256": "20e4fcb6b074d2b019dd2cb8abb9e5a91aedcd84ba9d4f6ce6b219c2a0de3c82"
          },
          {
            "model": {
              "id": "drift",
              "version": 1,
              "family": "drift",
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
              "exact": "3",
              "decimal": "3.000000000000",
              "reason": null
            },
            "point_functional": "endpoint linear extrapolation",
            "actual": "3",
            "error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "squared_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "sha256": "98c48d645a0a6f09746f5390eec4e97e37c912e1080a3f1918b5eb60f55d09b7"
          },
          {
            "model": {
              "id": "drift",
              "version": 1,
              "family": "drift",
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
              "exact": "4",
              "decimal": "4.000000000000",
              "reason": null
            },
            "point_functional": "endpoint linear extrapolation",
            "actual": "4",
            "error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "squared_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "sha256": "c3c25e602efb4bd71ad106d2955ea50e537668f738443be11671dd0a888e9bd1"
          },
          {
            "model": {
              "id": "ses_alpha0.2_initial_y1",
              "version": 1,
              "family": "ses",
              "alpha": "0.2",
              "seasonal_period": null,
              "initialization": "first observation,then consume subsequent observations"
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
              "exact": "6/5",
              "decimal": "1.200000000000",
              "reason": null
            },
            "point_functional": "fixed-alpha final level",
            "actual": "3",
            "error": {
              "exact": "9/5",
              "decimal": "1.800000000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "9/5",
              "decimal": "1.800000000000",
              "reason": null
            },
            "squared_error": {
              "exact": "81/25",
              "decimal": "3.240000000000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "9/5",
              "decimal": "1.800000000000",
              "reason": null
            },
            "sha256": "6b89f3e079b2057177bf5a2b6a502be726443c3f661d311cd6498a0d9d80c5a7"
          },
          {
            "model": {
              "id": "ses_alpha0.2_initial_y1",
              "version": 1,
              "family": "ses",
              "alpha": "0.2",
              "seasonal_period": null,
              "initialization": "first observation,then consume subsequent observations"
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
              "exact": "39/25",
              "decimal": "1.560000000000",
              "reason": null
            },
            "point_functional": "fixed-alpha final level",
            "actual": "4",
            "error": {
              "exact": "61/25",
              "decimal": "2.440000000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "61/25",
              "decimal": "2.440000000000",
              "reason": null
            },
            "squared_error": {
              "exact": "3721/625",
              "decimal": "5.953600000000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "61/25",
              "decimal": "2.440000000000",
              "reason": null
            },
            "sha256": "81c053f0279d2ee10b48739d6082e88486ec298bdd76d238a4e252970c0cc92e"
          }
        ],
        "test": [
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
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "sha256": "5f10024f07db72b76deab19f8e7868027fae403fa25d0d80a53e3d26c4ceb0ae"
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
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "sha256": "e930a2d8f7efe7403632a97035f7478a2313e03ca7dca46474da333dc7fdfffd"
          },
          {
            "model": {
              "id": "mean",
              "version": 1,
              "family": "mean",
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
              "exact": "5/2",
              "decimal": "2.500000000000",
              "reason": null
            },
            "point_functional": "training arithmetic mean",
            "actual": "5",
            "error": {
              "exact": "5/2",
              "decimal": "2.500000000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "5/2",
              "decimal": "2.500000000000",
              "reason": null
            },
            "squared_error": {
              "exact": "25/4",
              "decimal": "6.250000000000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "5/2",
              "decimal": "2.500000000000",
              "reason": null
            },
            "sha256": "2f93f3dc259cc39b6f8a078e9de75396d60d630e36f931e6dea66fdd1d86e9d3"
          },
          {
            "model": {
              "id": "mean",
              "version": 1,
              "family": "mean",
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
              "exact": "3",
              "decimal": "3.000000000000",
              "reason": null
            },
            "point_functional": "training arithmetic mean",
            "actual": "6",
            "error": {
              "exact": "3",
              "decimal": "3.000000000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "3",
              "decimal": "3.000000000000",
              "reason": null
            },
            "squared_error": {
              "exact": "9",
              "decimal": "9.000000000000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "3",
              "decimal": "3.000000000000",
              "reason": null
            },
            "sha256": "b63431d6040b429bc5db25bbb7a9e9b360e58bd48c3c78067d450ba43c9b2f27"
          },
          {
            "model": {
              "id": "drift",
              "version": 1,
              "family": "drift",
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
              "exact": "5",
              "decimal": "5.000000000000",
              "reason": null
            },
            "point_functional": "endpoint linear extrapolation",
            "actual": "5",
            "error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "squared_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "sha256": "ea76eb5c465505251ba6bbe85bd7f33985b954a91689f7e826585745975232e1"
          },
          {
            "model": {
              "id": "drift",
              "version": 1,
              "family": "drift",
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
              "exact": "6",
              "decimal": "6.000000000000",
              "reason": null
            },
            "point_functional": "endpoint linear extrapolation",
            "actual": "6",
            "error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "squared_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "sha256": "cce57c55c1342b71275d10ed2980cbcc11589270455cb7fb25bbf8d121321df1"
          },
          {
            "model": {
              "id": "ses_alpha0.2_initial_y1",
              "version": 1,
              "family": "ses",
              "alpha": "0.2",
              "seasonal_period": null,
              "initialization": "first observation,then consume subsequent observations"
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
              "exact": "256/125",
              "decimal": "2.048000000000",
              "reason": null
            },
            "point_functional": "fixed-alpha final level",
            "actual": "5",
            "error": {
              "exact": "369/125",
              "decimal": "2.952000000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "369/125",
              "decimal": "2.952000000000",
              "reason": null
            },
            "squared_error": {
              "exact": "136161/15625",
              "decimal": "8.714304000000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "369/125",
              "decimal": "2.952000000000",
              "reason": null
            },
            "sha256": "4d6197499ad59a105be52422c5a0fb7b65c7a8428b608bb8d783dcf0da258367"
          },
          {
            "model": {
              "id": "ses_alpha0.2_initial_y1",
              "version": 1,
              "family": "ses",
              "alpha": "0.2",
              "seasonal_period": null,
              "initialization": "first observation,then consume subsequent observations"
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
              "exact": "1649/625",
              "decimal": "2.638400000000",
              "reason": null
            },
            "point_functional": "fixed-alpha final level",
            "actual": "6",
            "error": {
              "exact": "2101/625",
              "decimal": "3.361600000000",
              "reason": null
            },
            "absolute_error": {
              "exact": "2101/625",
              "decimal": "3.361600000000",
              "reason": null
            },
            "squared_error": {
              "exact": "4414201/390625",
              "decimal": "11.300354560000",
              "reason": null
            },
            "training_scale": {
              "exact": "1",
              "decimal": "1.000000000000",
              "reason": null
            },
            "scaled_absolute_error": {
              "exact": "2101/625",
              "decimal": "3.361600000000",
              "reason": null
            },
            "sha256": "ce6fae9048717b7120da819d07f04b24ef080e3b13d3457bf3d22c7df95d18bd"
          }
        ]
      },
      "primary_selected_test": {
        "model": "drift",
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
            "exact": "0",
            "decimal": "0.000000000000",
            "reason": null
          },
          "mse": {
            "exact": "0",
            "decimal": "0.000000000000",
            "reason": null
          },
          "rmse": {
            "exact": "sqrt(0)",
            "decimal": "0.000000000000",
            "reason": null
          },
          "bias": {
            "exact": "0",
            "decimal": "0.000000000000",
            "reason": null
          },
          "mase": {
            "exact": "0",
            "decimal": "0.000000000000",
            "reason": null
          },
          "mase_count": 2,
          "undefined_scale_counts": {
            "zero_training_scale": 0,
            "insufficient_scale_history": 0,
            "missing_training_target": 0
          },
          "wape": {
            "exact": "0",
            "decimal": "0.000000000000",
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
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "mse": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "rmse": {
              "exact": "sqrt(0)",
              "decimal": "0.000000000000",
              "reason": null
            },
            "bias": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "mase": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "mase_count": 2,
            "undefined_scale_counts": {
              "zero_training_scale": 0,
              "insufficient_scale_history": 0,
              "missing_training_target": 0
            },
            "wape": {
              "exact": "0",
              "decimal": "0.000000000000",
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
          "exact": "0",
          "decimal": "0.000000000000",
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
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "mse": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "rmse": {
              "exact": "sqrt(0)",
              "decimal": "0.000000000000",
              "reason": null
            },
            "bias": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "mase": {
              "exact": "0",
              "decimal": "0.000000000000",
              "reason": null
            },
            "mase_count": 2,
            "undefined_scale_counts": {
              "zero_training_scale": 0,
              "insufficient_scale_history": 0,
              "missing_training_target": 0
            },
            "wape": {
              "exact": "0",
              "decimal": "0.000000000000",
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
          "common_scored": 2,
          "candidate_mae": {
            "exact": "0",
            "decimal": "0.000000000000",
            "reason": null
          },
          "reference_mae": {
            "exact": "1",
            "decimal": "1.000000000000",
            "reason": null
          },
          "candidate_minus_reference_mae": {
            "exact": "-1",
            "decimal": "-1.000000000000",
            "reason": null
          },
          "ratio": {
            "exact": "0",
            "decimal": "0.000000000000",
            "reason": null
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
  "report_sha256": "ed55bc9e2621bfbdc285797afa8199afc0fbb7e1a33b36af6e48c0fea4b3f8a2"
}
```
