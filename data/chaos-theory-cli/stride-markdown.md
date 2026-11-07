# Chaos theory — finite Lorenz63 simulation

```json
{
  "status": "accepted",
  "technique_id": 59,
  "schema_version": 1,
  "profile": {
    "id": "chaos-theory-lorenz63-rk4-v1",
    "version": 1,
    "sha256": "9cefe49f10b6a149c86ee527abd16f2932e939364a1088fcc2a3fe5d26750d0f",
    "catalog_sha256": "8998ef41e7e380f546c7de331125f0fd43dba95c70a1413d7c88c549697beeb1"
  },
  "request": {
    "schema_version": 1,
    "profile": {
      "id": "chaos-theory-lorenz63-rk4-v1",
      "version": 1,
      "sha256": "9cefe49f10b6a149c86ee527abd16f2932e939364a1088fcc2a3fe5d26750d0f",
      "catalog_sha256": "8998ef41e7e380f546c7de331125f0fd43dba95c70a1413d7c88c549697beeb1"
    },
    "parameters": {
      "sigma": "10",
      "rho": "28",
      "beta": "8/3"
    },
    "initial": [
      "1",
      "1",
      "1"
    ],
    "perturbed_initial": [
      "1000001/1000000",
      "1",
      "1"
    ],
    "integration": {
      "solver": "classical_rk4",
      "dt": "1/1000",
      "steps": 11,
      "trace_stride": 4
    },
    "provenance": {
      "synthetic": true,
      "source_ref": "chaos-theory-ucar-v1",
      "rights": "self_authored",
      "attribution": "Original synthetic educational fixture",
      "snapshot": "Self-authored synthetic Lorenz63 initial states; no observations.",
      "snapshot_sha256": "d9b576eb2d65d69d3bb255d6761a281a455c86c66a45e0ec9ce4f87e184bfee7"
    }
  },
  "input_sha256": "8e26f275dfe55328f1d08cd09a98a22e11b3d719ca1340bc01fab64503998e0b",
  "model_sha256": "dbb1412bf0862be68a408fe046b644daf2ed8515a4a5509460ada1a148433bff",
  "schema_sha256": "f9f63b00543be666baecdaafcecffdae3f4309d8bc1d60c422eb34e9ea35444f",
  "source_manifest_sha256": "8998ef41e7e380f546c7de331125f0fd43dba95c70a1413d7c88c549697beeb1",
  "source_freeze_sha256": "9663f768b409a7fe59d56f65415df4121d005836f705dc1207beca56b0d88695",
  "code_sha256": "ffac2760befd1870402e7e2100a84a82b1a018d965b1440421983486fde5d1af",
  "budget": {
    "work": 264,
    "returned_cells": 68
  },
  "rows": [
    {
      "time": "0",
      "coarse_base": [
        1.0,
        1.0,
        1.0
      ],
      "coarse_perturbed": [
        1.000001,
        1.0,
        1.0
      ],
      "refined_base": [
        1.0,
        1.0,
        1.0
      ],
      "refined_perturbed": [
        1.000001,
        1.0,
        1.0
      ],
      "coarse_separation": 9.999999999177334e-07,
      "refined_separation": 9.999999999177334e-07,
      "base_refinement_difference": 0.0,
      "perturbed_refinement_difference": 0.0
    },
    {
      "time": "1/250",
      "coarse_base": [
        1.0020507073919616,
        1.103879288949218,
        0.9935787900298502
      ],
      "coarse_perturbed": [
        1.002051670282653,
        1.103879394685197,
        0.9935787943470015
      ],
      "refined_base": [
        1.0020507073393214,
        1.1038792890303992,
        0.9935787900322209
      ],
      "refined_perturbed": [
        1.0020516702300128,
        1.1038793947663783,
        0.9935787943493721
      ],
      "coarse_separation": 9.686884012200235e-07,
      "refined_separation": 9.686884012195286e-07,
      "base_refinement_difference": 9.67832788425839e-11,
      "perturbed_refinement_difference": 9.678327612308302e-11
    },
    {
      "time": "1/125",
      "coarse_base": [
        1.00809371303096,
        1.2078064549514689,
        0.9876580814116677
      ],
      "coarse_perturbed": [
        1.0080946443301617,
        1.2078066623068469,
        0.987658090663173
      ],
      "refined_base": [
        1.0080937129359113,
        1.2078064551023833,
        0.987658081416048
      ],
      "refined_perturbed": [
        1.008094644235113,
        1.2078066624577615,
        0.9876580906675532
      ],
      "coarse_separation": 9.541488596229542e-07,
      "refined_separation": 9.541488596690559e-07,
      "base_refinement_difference": 1.784056743724721e-10,
      "perturbed_refinement_difference": 1.7840585674962188e-10
    },
    {
      "time": "11/1000",
      "coarse_base": [
        1.0151570614952312,
        1.2860367772374344,
        0.9835570553734602
      ],
      "coarse_perturbed": [
        1.0151579725002589,
        1.2860370584593355,
        0.9835570687211076
      ],
      "refined_base": [
        1.0151570613743413,
        1.2860367774341348,
        0.9835570553791111
      ],
      "refined_perturbed": [
        1.015157972379369,
        1.2860370586560363,
        0.9835570687267582
      ],
      "coarse_separation": 9.535166898017068e-07,
      "refined_separation": 9.535166899280201e-07,
      "base_refinement_difference": 2.309488625987952e-10,
      "perturbed_refinement_difference": 2.3094923268284316e-10
    }
  ],
  "diagnostics": {
    "maxima_over_all_aligned_times": {
      "coarse_separation": 9.999999999177334e-07,
      "refined_separation": 9.999999999177334e-07,
      "base_refinement_difference": 2.309488625987952e-10,
      "perturbed_refinement_difference": 2.3094923268284316e-10
    },
    "initial_separation": 9.999999999177334e-07,
    "final_refined_amplification": 0.9535166900064628,
    "amplification_status": "finite_pair_ratio_only",
    "integrated_coarse_steps_per_trajectory": 11,
    "integrated_refined_steps_per_trajectory": 22,
    "aligned_times": 12,
    "returned_times": 4,
    "horizon": "11/1000",
    "lyapunov_exponent": null,
    "validated_forecast_horizon": null,
    "refinement_is_rigorous_error_bound": false
  },
  "sources": [
    {
      "id": "chaos-theory-lorenz-v1",
      "technique_id": 59,
      "rank": 1,
      "author": "Edward N. Lorenz",
      "edition": "Deterministic Nonperiodic Flow;1963;JAS20(2),130–141;DOI10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2",
      "url": "https://journals.ametsoc.org/abstract/journals/atsc/20/2/1520-0469_1963_020_0130_dnf_2_0_co_2.xml",
      "locator": "Official abstract/metadata inspected; original ranked full-text URL403. Sensitivity context only; no full-text replication claim.",
      "ingestion": "facts_only",
      "rights_note": "Copyright retained by source owners; mathematical facts and original synthetic fixtures only; no bodies,figures,data or third-party code redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "chaos-theory-strogatz-v1",
      "technique_id": 59,
      "rank": 2,
      "author": "Steven H. Strogatz",
      "edition": "Nonlinear Dynamics and Chaos;3rdedition;2024;616pages;Chapman and Hall",
      "url": "https://www.routledge.com/Nonlinear-Dynamics-and-Chaos/Strogatz/p/book/9780429398490",
      "locator": "Official indexed publisher metadata only; direct403; no chapters inspected or inferred.",
      "ingestion": "facts_only",
      "rights_note": "Copyright retained by source owners; mathematical facts and original synthetic fixtures only; no bodies,figures,data or third-party code redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "chaos-theory-sugihara-may-v1",
      "technique_id": 59,
      "rank": 3,
      "author": "George Sugihara and Robert M. May",
      "edition": "Nature344,734–741;19April1990;DOI10.1038/344734a0",
      "url": "https://www.nature.com/articles/344734a0",
      "locator": "Official abstract/metadata inspected; nonlinear forecasting context,not an RK4 recipe. Author-hosted scanned witness copyright restrictions observed; no methods OCR or empirical reproduction.",
      "ingestion": "facts_only",
      "rights_note": "Copyright retained by source owners; mathematical facts and original synthetic fixtures only; no bodies,figures,data or third-party code redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "chaos-theory-ucar-v1",
      "technique_id": 59,
      "rank": null,
      "author": "UCAR DART developers",
      "edition": "DART10.10.1 Lorenz63 model documentation",
      "url": "https://docs.dart.ucar.edu/en/v10.10.1/models/lorenz_63/readme.html",
      "locator": "Equations/defaults and namelist solver sections inspected. RK2 default distinguished from optional classical RK4. Dimensionless model time.",
      "ingestion": "facts_only",
      "rights_note": "Copyright retained by source owners; mathematical facts and original synthetic fixtures only; no bodies,figures,data or third-party code redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "chaos-theory-moler-v1",
      "technique_id": 59,
      "rank": null,
      "author": "Cleve Moler / MathWorks",
      "edition": "Ordinary Differential Equation Suite;12May2014",
      "url": "https://blogs.mathworks.com/cleve/2014/05/12/ordinary-differential-equation-suite/",
      "locator": "Classical RK4 four-stage formula inspected. Facts independently reimplemented; fixed-step method has no automatic error estimate.",
      "ingestion": "facts_only",
      "rights_note": "Copyright retained by source owners; mathematical facts and original synthetic fixtures only; no bodies,figures,data or third-party code redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    }
  ],
  "numerics": {
    "arithmetic": "IEEE754 binary64 scalar Python",
    "oracle": "ExactFraction RK4 stages and independent Taylor coefficient recurrence",
    "one_step_absolute_tolerance": "1e-12",
    "model_time": "dimensionless"
  },
  "empirical_forecast_accuracy_validated": false,
  "limitations": [
    "Certified Lyapunov exponent or forecast horizon",
    "Nonlinear delay embedding",
    "Reservoir computing",
    "Empirical weather-like ensembles",
    "Random/stochastic/data assimilation modes",
    "Initial-state separation and step-refinement difference are separate diagnostics.",
    "No original Lorenz RK2 replication or long-horizon accuracy certification.",
    "Binary64 integration uses approximate h; displayed times are exact nominal grid values."
  ],
  "report_sha256": "10f0ef1c5d14b67a1a90fcf46927bf94a93db965feacd5d90225e868b53a094c"
}
```

