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
      "-1",
      "-1",
      "1"
    ],
    "integration": {
      "solver": "classical_rk4",
      "dt": "1/100",
      "steps": 20,
      "trace_stride": 3
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
  "input_sha256": "3989e995a4f5c797ca04076ebb9c287fe64e012773a9bc92c7e77fd6d42734dd",
  "model_sha256": "dbb1412bf0862be68a408fe046b644daf2ed8515a4a5509460ada1a148433bff",
  "schema_sha256": "f9f63b00543be666baecdaafcecffdae3f4309d8bc1d60c422eb34e9ea35444f",
  "source_manifest_sha256": "8998ef41e7e380f546c7de331125f0fd43dba95c70a1413d7c88c549697beeb1",
  "source_freeze_sha256": "9663f768b409a7fe59d56f65415df4121d005836f705dc1207beca56b0d88695",
  "code_sha256": "ffac2760befd1870402e7e2100a84a82b1a018d965b1440421983486fde5d1af",
  "budget": {
    "work": 480,
    "returned_cells": 136
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
        -1.0,
        -1.0,
        1.0
      ],
      "refined_base": [
        1.0,
        1.0,
        1.0
      ],
      "refined_perturbed": [
        -1.0,
        -1.0,
        1.0
      ],
      "coarse_separation": 2.8284271247461903,
      "refined_separation": 2.8284271247461903,
      "base_refinement_difference": 0.0,
      "perturbed_refinement_difference": 0.0
    },
    {
      "time": "3/100",
      "coarse_base": [
        1.1072088542956613,
        1.7983098897421352,
        0.9651589513000616
      ],
      "coarse_perturbed": [
        -1.1072088542956613,
        -1.7983098897421352,
        0.9651589513000616
      ],
      "refined_base": [
        1.1072064229216019,
        1.7983143351741737,
        0.9651590842529619
      ],
      "refined_perturbed": [
        -1.1072064229216019,
        -1.7983143351741737,
        0.9651590842529619
      ],
      "coarse_separation": 4.2236618740496175,
      "refined_separation": 4.223666895507637,
      "base_refinement_difference": 5.068641070274829e-06,
      "perturbed_refinement_difference": 5.068641070274829e-06
    },
    {
      "time": "3/50",
      "coarse_base": [
        1.4095706581041882,
        2.738545613747143,
        0.9726081698899176
      ],
      "coarse_perturbed": [
        -1.4095706581041882,
        -2.738545613747143,
        0.9726081698899176
      ],
      "refined_base": [
        1.4095689110023955,
        2.738551713325957,
        0.9726082596217598
      ],
      "refined_perturbed": [
        -1.4095689110023955,
        -2.738551713325957,
        0.9726082596217598
      ],
      "coarse_separation": 6.160039454017155,
      "refined_separation": 6.160048701568849,
      "base_refinement_difference": 6.345492745759916e-06,
      "perturbed_refinement_difference": 6.345492745759916e-06
    },
    {
      "time": "9/100",
      "coarse_base": [
        1.9135962032916782,
        3.969615009809224,
        1.0575118553930003
      ],
      "coarse_perturbed": [
        -1.9135962032916782,
        -3.969615009809224,
        1.0575118553930003
      ],
      "refined_base": [
        1.913596378459932,
        3.9696229842307034,
        1.0575118435919515
      ],
      "refined_perturbed": [
        -1.913596378459932,
        -3.9696229842307034,
        1.0575118435919515
      ],
      "coarse_separation": 8.81355632088546,
      "refined_separation": 8.813570839696618,
      "base_refinement_difference": 7.976353873104926e-06,
      "perturbed_refinement_difference": 7.976353873104926e-06
    },
    {
      "time": "3/25",
      "coarse_base": [
        2.663580910085269,
        5.650437904613584,
        1.291893499664662
      ],
      "coarse_perturbed": [
        -2.663580910085269,
        -5.650437904613584,
        1.291893499664662
      ],
      "refined_base": [
        2.663583760912624,
        5.65044947175931,
        1.2918935208070974
      ],
      "refined_perturbed": [
        -2.663583760912624,
        -5.65044947175931,
        1.2918935208070974
      ],
      "coarse_separation": 12.493536213332817,
      "refined_separation": 12.493559570323024,
      "base_refinement_difference": 1.191329189815164e-05,
      "perturbed_refinement_difference": 1.191329189815164e-05
    },
    {
      "time": "3/20",
      "coarse_base": [
        3.736715793797584,
        7.964065218724182,
        1.8177565221880947
      ],
      "coarse_perturbed": [
        -3.736715793797584,
        -7.964065218724182,
        1.8177565221880947
      ],
      "refined_base": [
        3.7367220955069653,
        7.964083063295479,
        1.8177571236354484
      ],
      "refined_perturbed": [
        -3.7367220955069653,
        -7.964083063295479,
        1.8177571236354484
      ],
      "coarse_separation": 17.594246756449515,
      "refined_separation": 17.594284419449387,
      "base_refinement_difference": 1.893414917082131e-05,
      "perturbed_refinement_difference": 1.893414917082131e-05
    },
    {
      "time": "9/50",
      "coarse_base": [
        5.23996732507253,
        11.105288107586523,
        2.9075570279825036
      ],
      "coarse_perturbed": [
        -5.23996732507253,
        -11.105288107586523,
        2.9075570279825036
      ],
      "refined_base": [
        5.239977837006906,
        11.105315491321853,
        2.907559684286644
      ],
      "refined_perturbed": [
        -5.239977837006906,
        -11.105315491321853,
        2.907559684286644
      ],
      "coarse_separation": 24.5588828345534,
      "refined_separation": 24.558941336638817,
      "base_refinement_difference": 2.945209121075057e-05,
      "perturbed_refinement_difference": 2.945209121075057e-05
    },
    {
      "time": "1/5",
      "coarse_base": [
        6.542513103944859,
        13.731148820534644,
        4.180191224257708
      ],
      "coarse_perturbed": [
        -6.542513103944859,
        -13.731148820534644,
        4.180191224257708
      ],
      "refined_base": [
        6.5425266023347675,
        13.731184236560878,
        4.180196983788113
      ],
      "refined_perturbed": [
        -6.5425266023347675,
        -13.731184236560878,
        4.180196983788113
      ],
      "coarse_separation": 30.420317266390246,
      "refined_separation": 30.42039282327801,
      "base_refinement_difference": 3.83363226565105e-05,
      "perturbed_refinement_difference": 3.83363226565105e-05
    }
  ],
  "diagnostics": {
    "maxima_over_all_aligned_times": {
      "coarse_separation": 30.420317266390246,
      "refined_separation": 30.42039282327801,
      "base_refinement_difference": 3.83363226565105e-05,
      "perturbed_refinement_difference": 3.83363226565105e-05
    },
    "initial_separation": 2.8284271247461903,
    "final_refined_amplification": 10.755233025849233,
    "amplification_status": "finite_pair_ratio_only",
    "integrated_coarse_steps_per_trajectory": 20,
    "integrated_refined_steps_per_trajectory": 40,
    "aligned_times": 21,
    "returned_times": 8,
    "horizon": "1/5",
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
  "report_sha256": "20291c5a8a6445ce24eba2b1037911b8819bd526742059e1b72daf86f2f923f9"
}
```

