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
        "id": "R",
        "parent": null,
        "weight": "1",
        "utility": null
      },
      {
        "id": "no",
        "parent": "R",
        "weight": "0",
        "utility": "100"
      },
      {
        "id": "yes",
        "parent": "R",
        "weight": "1",
        "utility": "-4"
      }
    ],
    "queries": [
      {
        "id": "q",
        "given": "no",
        "target": "yes"
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
  "input_sha256": "4c8770fe3bdfea31376f4b73cc767e0f65144ca773e749cdfadad68202f811b5",
  "model_sha256": "ea1b4c097d1d8e1a02f7167c1934348d0074ffe0b3162c491c0848d3f7a22bec",
  "schema_sha256": "f85fc694bf585d0a6b9c88b71755ebbe5137e456ef67929c344eff79bfec9b59",
  "source_manifest_sha256": "5089c43fb7f5d9bbca169a297801dccdd3c3eca36722ef2c87b31949a2769cdf",
  "source_freeze_sha256": "f960074ef48f003e362a46edff887a4a7bbff943961241fe4ba287684ae29add",
  "code_sha256": "715e7b8f06dacc932758e7146cba9389a0c1fe40b998270d19ae1a5c455ddbf0",
  "root": "R",
  "nodes": [
    {
      "id": "R",
      "parent": null,
      "children": [
        "no",
        "yes"
      ],
      "path": [
        "R"
      ],
      "depth": 0,
      "local_weight": "1",
      "mass": "1",
      "terminal": false,
      "declared_utility": null,
      "conditional_expected_utility": "-4"
    },
    {
      "id": "no",
      "parent": "R",
      "children": [],
      "path": [
        "R",
        "no"
      ],
      "depth": 1,
      "local_weight": "0",
      "mass": "0",
      "terminal": true,
      "declared_utility": "100",
      "conditional_expected_utility": null
    },
    {
      "id": "yes",
      "parent": "R",
      "children": [],
      "path": [
        "R",
        "yes"
      ],
      "depth": 1,
      "local_weight": "1",
      "mass": "1",
      "terminal": true,
      "declared_utility": "-4",
      "conditional_expected_utility": "-4"
    }
  ],
  "leaves": [
    {
      "id": "no",
      "mass": "0",
      "utility": "100",
      "weighted_utility": "0"
    },
    {
      "id": "yes",
      "mass": "1",
      "utility": "-4",
      "weighted_utility": "-4"
    }
  ],
  "total_leaf_mass": "1",
  "expected_utility": "-4",
  "queries": [
    {
      "id": "q",
      "given": "no",
      "target": "yes",
      "condition_mass": "0",
      "intersection_mass": "0",
      "probability": null,
      "status": "not_estimable_zero_condition"
    }
  ],
  "budget": {
    "work": 12,
    "returned_cells": 56
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
  "report_sha256": "5978da3d0b9f4fc1ad779c346e2e1c25938622031c4cd36a4e8281e28fbba009"
}
```

