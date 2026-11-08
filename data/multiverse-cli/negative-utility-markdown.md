# Multiverse — educational finite editorial scenario tree

```json
{
  "status": "accepted",
  "technique_id": 60,
  "schema_version": 1,
  "profile": {
    "id": "multiverse-finite-rational-scenario-tree-v1",
    "version": 1,
    "sha256": "9f1b7221a1c5aece17521729aa61e1c280c2bb39c2639ddaea716bafc06b0506",
    "catalog_sha256": "5089c43fb7f5d9bbca169a297801dccdd3c3eca36722ef2c87b31949a2769cdf"
  },
  "request": {
    "schema_version": 1,
    "profile": {
      "id": "multiverse-finite-rational-scenario-tree-v1",
      "version": 1,
      "sha256": "9f1b7221a1c5aece17521729aa61e1c280c2bb39c2639ddaea716bafc06b0506",
      "catalog_sha256": "5089c43fb7f5d9bbca169a297801dccdd3c3eca36722ef2c87b31949a2769cdf"
    },
    "scenario": {
      "id": "toy-scenario",
      "version": 1,
      "kind": "educational_editorial_weights",
      "exhaustive": true,
      "description": "Fictional branches with declared utilities."
    },
    "nodes": [
      {
        "id": "A",
        "parent": "R",
        "weight": "1/2",
        "utility": null
      },
      {
        "id": "A1",
        "parent": "A",
        "weight": "1/3",
        "utility": "-6"
      },
      {
        "id": "A2",
        "parent": "A",
        "weight": "2/3",
        "utility": "-3"
      },
      {
        "id": "B",
        "parent": "R",
        "weight": "1/2",
        "utility": "2"
      },
      {
        "id": "R",
        "parent": null,
        "weight": "1",
        "utility": null
      },
      {
        "id": "Z",
        "parent": "R",
        "weight": "0",
        "utility": "99"
      }
    ],
    "queries": [
      {
        "id": "q0",
        "given": "R",
        "target": "A1"
      },
      {
        "id": "q1",
        "given": "A",
        "target": "A1"
      },
      {
        "id": "q2",
        "given": "A1",
        "target": "A"
      },
      {
        "id": "q3",
        "given": "A",
        "target": "B"
      },
      {
        "id": "q4",
        "given": "Z",
        "target": "R"
      },
      {
        "id": "q5",
        "given": "R",
        "target": "Z"
      },
      {
        "id": "q6",
        "given": "R",
        "target": "R"
      },
      {
        "id": "q7",
        "given": "A1",
        "target": "A1"
      }
    ],
    "provenance": {
      "synthetic": true,
      "source_ref": "multiverse-mit-multiplication-v1",
      "rights": "self_authored",
      "attribution": "Original synthetic scenario author",
      "snapshot": "Self-authored finite educational editorial scenario; no universe observations.",
      "snapshot_sha256": "2bbe374959a036d5d8f98fe16e00bffccb5b3c0ecb2121060a8e52cb27a216ae"
    }
  },
  "input_sha256": "9d0e060c1ea0fcd81d0aaf01df062b0fca8e589ef5b2db000884f61be0873f6d",
  "model_sha256": "7e95d2062d433de734e81810946b960511237158b37bfb3ecaabf6343ec736e3",
  "schema_sha256": "f85fc694bf585d0a6b9c88b71755ebbe5137e456ef67929c344eff79bfec9b59",
  "source_manifest_sha256": "5089c43fb7f5d9bbca169a297801dccdd3c3eca36722ef2c87b31949a2769cdf",
  "source_freeze_sha256": "f960074ef48f003e362a46edff887a4a7bbff943961241fe4ba287684ae29add",
  "code_sha256": "715e7b8f06dacc932758e7146cba9389a0c1fe40b998270d19ae1a5c455ddbf0",
  "root": "R",
  "nodes": [
    {
      "id": "A",
      "parent": "R",
      "children": [
        "A1",
        "A2"
      ],
      "path": [
        "R",
        "A"
      ],
      "depth": 1,
      "local_weight": "1/2",
      "mass": "1/2",
      "terminal": false,
      "declared_utility": null,
      "conditional_expected_utility": "-4"
    },
    {
      "id": "A1",
      "parent": "A",
      "children": [],
      "path": [
        "R",
        "A",
        "A1"
      ],
      "depth": 2,
      "local_weight": "1/3",
      "mass": "1/6",
      "terminal": true,
      "declared_utility": "-6",
      "conditional_expected_utility": "-6"
    },
    {
      "id": "A2",
      "parent": "A",
      "children": [],
      "path": [
        "R",
        "A",
        "A2"
      ],
      "depth": 2,
      "local_weight": "2/3",
      "mass": "1/3",
      "terminal": true,
      "declared_utility": "-3",
      "conditional_expected_utility": "-3"
    },
    {
      "id": "B",
      "parent": "R",
      "children": [],
      "path": [
        "R",
        "B"
      ],
      "depth": 1,
      "local_weight": "1/2",
      "mass": "1/2",
      "terminal": true,
      "declared_utility": "2",
      "conditional_expected_utility": "2"
    },
    {
      "id": "R",
      "parent": null,
      "children": [
        "A",
        "B",
        "Z"
      ],
      "path": [
        "R"
      ],
      "depth": 0,
      "local_weight": "1",
      "mass": "1",
      "terminal": false,
      "declared_utility": null,
      "conditional_expected_utility": "-1"
    },
    {
      "id": "Z",
      "parent": "R",
      "children": [],
      "path": [
        "R",
        "Z"
      ],
      "depth": 1,
      "local_weight": "0",
      "mass": "0",
      "terminal": true,
      "declared_utility": "99",
      "conditional_expected_utility": null
    }
  ],
  "leaves": [
    {
      "id": "A1",
      "mass": "1/6",
      "utility": "-6",
      "weighted_utility": "-1"
    },
    {
      "id": "A2",
      "mass": "1/3",
      "utility": "-3",
      "weighted_utility": "-1"
    },
    {
      "id": "B",
      "mass": "1/2",
      "utility": "2",
      "weighted_utility": "1"
    },
    {
      "id": "Z",
      "mass": "0",
      "utility": "99",
      "weighted_utility": "0"
    }
  ],
  "total_leaf_mass": "1",
  "expected_utility": "-1",
  "queries": [
    {
      "id": "q0",
      "given": "R",
      "target": "A1",
      "condition_mass": "1",
      "intersection_mass": "1/6",
      "probability": "1/6",
      "status": "estimated_exact_model"
    },
    {
      "id": "q1",
      "given": "A",
      "target": "A1",
      "condition_mass": "1/2",
      "intersection_mass": "1/6",
      "probability": "1/3",
      "status": "estimated_exact_model"
    },
    {
      "id": "q2",
      "given": "A1",
      "target": "A",
      "condition_mass": "1/6",
      "intersection_mass": "1/6",
      "probability": "1",
      "status": "estimated_exact_model"
    },
    {
      "id": "q3",
      "given": "A",
      "target": "B",
      "condition_mass": "1/2",
      "intersection_mass": "0",
      "probability": "0",
      "status": "estimated_exact_model"
    },
    {
      "id": "q4",
      "given": "Z",
      "target": "R",
      "condition_mass": "0",
      "intersection_mass": "0",
      "probability": null,
      "status": "not_estimable_zero_condition"
    },
    {
      "id": "q5",
      "given": "R",
      "target": "Z",
      "condition_mass": "1",
      "intersection_mass": "0",
      "probability": "0",
      "status": "estimated_exact_model"
    },
    {
      "id": "q6",
      "given": "R",
      "target": "R",
      "condition_mass": "1",
      "intersection_mass": "1",
      "probability": "1",
      "status": "estimated_exact_model"
    },
    {
      "id": "q7",
      "given": "A1",
      "target": "A1",
      "condition_mass": "1/6",
      "intersection_mass": "1/6",
      "probability": "1",
      "status": "estimated_exact_model"
    }
  ],
  "budget": {
    "work": 84,
    "returned_cells": 160
  },
  "numerics": {
    "arithmetic": "Exact fractions.Fraction with8192bit guards",
    "weight_interpretation": "Editorial conditional scenario weights;notquantumamplitudes"
  },
  "sources": [
    {
      "id": "multiverse-everett-v1",
      "technique_id": 60,
      "rank": 1,
      "author": "Hugh Everett III",
      "edition": "Relative State Formulation of Quantum Mechanics;Rev.Mod.Phys.29(3),454;1July1957;DOI10.1103/RevModPhys.29.454",
      "url": "https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.29.454",
      "locator": "Official metadata/copyright inspected; content authorization required. No full paper derivation claimed.",
      "ingestion": "facts_only",
      "rights_note": "Source copyright retained; facts only; no bodies,figures,third-party code or observed-universe data redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "multiverse-wallace-v1",
      "technique_id": 60,
      "rank": 2,
      "author": "David Wallace",
      "edition": "The Emergent Multiverse:Quantum Theory according to the Everett Interpretation;OUP;24May2012;DOI10.1093/acprof:oso/9780199546961.001.0001",
      "url": "https://academic.oup.com/book/25622",
      "locator": "Official publisher abstract/contents/date inspected. Probability and decision-theoretic chapter headings are leads; no chapter proofs inspected.",
      "ingestion": "facts_only",
      "rights_note": "Source copyright retained; facts only; no bodies,figures,third-party code or observed-universe data redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "multiverse-carroll-v1",
      "technique_id": 60,
      "rank": 3,
      "author": "Sean Carroll",
      "edition": "Something Deeply Hidden:Quantum Worlds and the Emergence of Spacetime;Dutton2019",
      "url": "https://preposterousuniverse.com/somethingdeeplyhidden/",
      "locator": "Author bibliography/overview/contents inspected; no full book access claimed.",
      "ingestion": "facts_only",
      "rights_note": "Source copyright retained; facts only; no bodies,figures,third-party code or observed-universe data redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "multiverse-mit-multiplication-v1",
      "technique_id": 60,
      "rank": null,
      "author": "MIT OpenCourseWare probability instructors",
      "edition": "RES6.012 Spring2018;L02-06 Multiplication Rule transcript",
      "url": "https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/c22535b6cb3fad2f45dc1e4947ea2afc_ugzs7dgQ-JE.pdf",
      "locator": "Transcript conditional definition and path-product discussion inspected. General finite probability; no independence assumption for conditional edges.",
      "ingestion": "facts_only",
      "rights_note": "Source copyright retained; facts only; no bodies,figures,third-party code or observed-universe data redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "multiverse-mit-expectation-v1",
      "technique_id": 60,
      "rank": null,
      "author": "MIT OpenCourseWare probability instructors",
      "edition": "6.041SC Fall2013;Lecture5 discrete expectation transcript",
      "url": "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/6cb4b105e1e41aa869a2d92764aea126_MIT6_041SCF13_lec05_300k.mp4.pdf",
      "locator": "Discrete expectation weighting and linearity sections inspected; used for generic declared utilities only.",
      "ingestion": "facts_only",
      "rights_note": "Source copyright retained; facts only; no bodies,figures,third-party code or observed-universe data redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    }
  ],
  "universe_observations_used": false,
  "everett_empirically_validated": false,
  "empirical_forecast_accuracy_validated": false,
  "limitations": [
    "Observing/predicting otheruniverses",
    "Bornrule/amplitude/decoherence simulation",
    "Empirical Everettproof",
    "General quantum decision-theory theoremreplication",
    "MonteCarlo/stochasticservices",
    "Editorial weights are declarations,not Born-rule amplitudes or observed frequencies.",
    "Completeness applies to the declared finite tree; externally omitted possibilities cannot be detected.",
    "Utilities and narrative are self-authored synthetic inputs,not recommendations or other-universe predictions."
  ],
  "report_sha256": "643da21b43e33ea3178a84f5fbc8a0862f7d1958087b920be68692d739546421"
}
```

