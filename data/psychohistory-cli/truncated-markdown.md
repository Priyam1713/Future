# Psychohistory — synthetic threshold dynamics

```json
{
  "status": "accepted",
  "technique_id": 52,
  "profile": {
    "id": "psychohistory-synthetic-threshold-dynamics-v1",
    "sha256": "b7e9f2d27994be3e89ac0bba0e2066bbc19bd89241e01e4b0989621de061988f",
    "catalog_sha256": "9dbd60a7838818c8e4332caaea837b4a2e7232ec02ec1a8434415150880144db"
  },
  "schema_version": 1,
  "request": {
    "schema_version": 1,
    "profile": {
      "id": "psychohistory-synthetic-threshold-dynamics-v1",
      "sha256": "b7e9f2d27994be3e89ac0bba0e2066bbc19bd89241e01e4b0989621de061988f",
      "catalog_sha256": "9dbd60a7838818c8e4332caaea837b4a2e7232ec02ec1a8434415150880144db"
    },
    "population": {
      "size": 3,
      "nodes": [
        "000",
        "001",
        "002"
      ]
    },
    "runs": 1,
    "rounds": 1,
    "trace_states": true,
    "rng": {
      "algorithm": "xorshift32-v1",
      "seed": 1
    },
    "scenarios": [
      {
        "id": "base",
        "edges": [
          [
            "000",
            "001"
          ],
          [
            "001",
            "002"
          ]
        ],
        "thresholds": [
          {
            "node": "000",
            "phi": "1/2"
          },
          {
            "node": "001",
            "phi": "1/2"
          },
          {
            "node": "002",
            "phi": "1/2"
          }
        ],
        "initial": {
          "mode": "fixed",
          "probability": null,
          "fixed_seeds": [
            "000"
          ],
          "run_seeds": [],
          "overrides": []
        }
      }
    ],
    "reference_scenario": "base",
    "provenance": {
      "synthetic": true,
      "source_ref": "psychohistory-watts-threshold-v1",
      "rights": "self_authored",
      "attribution": "Future original synthetic fixture",
      "snapshot": "Original synthetic graph; no observed people or causal claims.",
      "snapshot_sha256": "8f263eb52465b0e892fa5463028cef8f29dd999e333165f83a9fdd664bf12abe"
    }
  },
  "input_sha256": "adb044a0a81fd1ba32ed900b235c5c5c2169cbe16026c7422eee919c20b9d633",
  "code_sha256": "fd187915dfca927e046800be389a1fe9b547653488d29055fcfb5cfb39445386",
  "source_manifest_sha256": "9dbd60a7838818c8e4332caaea837b4a2e7232ec02ec1a8434415150880144db",
  "source_freeze_sha256": "59a045aa4a7ee17579f7973cc91f2175fe842302c61dc087ae8bd919d914c99a",
  "source_snapshot_sha256": "8f263eb52465b0e892fa5463028cef8f29dd999e333165f83a9fdd664bf12abe",
  "stream_sha256": "d8d164b0a8fb92c56fa3d71a953ff79db86278fe564971f7936e80e2ef9b22de",
  "draw_count": 3,
  "budget": {
    "work_units": 14,
    "count_cells": 52,
    "state_cells": 6
  },
  "scenarios": [
    {
      "id": "base",
      "graph_sha256": "cd2afabcd01191b890913591f9b2908a4c8b654b686941781ca00c9555eda279",
      "thresholds_sha256": "7b9b35f0c548f54fb9457980a38f6318d51d277bde6979eb2d831006d6449b64",
      "initial_spec_sha256": "962845d9d7001920bcb053819cfc7285c27c19f62dd8201ae260af688f10da93",
      "model_sha256": "1f7cc12f1832f92e2256f7451c20d396b419aef0b21045f48f0d24ae3e93e5e0",
      "initialization_design": "fixed",
      "rows": [
        {
          "run": 0,
          "initial_active": 1,
          "final_active": 2,
          "initial_fraction": "1/3",
          "final_fraction": "2/3",
          "active_counts": [
            1,
            2
          ],
          "inactive_counts": [
            2,
            1
          ],
          "states": [
            [
              1,
              0,
              0
            ],
            [
              1,
              1,
              0
            ]
          ],
          "initial_state_sha256": "7ff52993d5d3cb149089942de7fc7a6511db2671cf2125976c081ad6fff89772",
          "final_state_sha256": "bdd574af065475251acfcde22de003ba6c910cf9af755ef567267c4378ee47e3",
          "draw_row_sha256": "46ee7825afd48ec6b662d8daf0efb5da8ef1671f9ac210853cb7b34c44e0b6f7",
          "converged": false,
          "truncated": true,
          "executed_rounds": 1,
          "persistence_final_active": 1,
          "paired_gain": 1
        }
      ],
      "initial_count": {
        "runs": 1,
        "mean": "1",
        "population_variance": "0",
        "population_denominator": 1,
        "sample_variance": null,
        "sample_denominator": null,
        "sample_status": "not_estimable"
      },
      "final_count": {
        "runs": 1,
        "mean": "2",
        "population_variance": "0",
        "population_denominator": 1,
        "sample_variance": null,
        "sample_denominator": null,
        "sample_status": "not_estimable"
      },
      "initial_fraction": {
        "runs": 1,
        "mean": "1/3",
        "population_variance": "0",
        "population_denominator": 1,
        "sample_variance": null,
        "sample_denominator": null,
        "sample_status": "not_estimable"
      },
      "final_fraction": {
        "runs": 1,
        "mean": "2/3",
        "population_variance": "0",
        "population_denominator": 1,
        "sample_variance": null,
        "sample_denominator": null,
        "sample_status": "not_estimable"
      },
      "per_round_mean_active": [
        "1",
        "2"
      ],
      "per_round_mean_inactive": [
        "2",
        "1"
      ],
      "ideal_initial_moments": {
        "status": "not_applicable",
        "reason": "Not an iid Bernoulli initialization",
        "mean": null,
        "variance": null
      },
      "persistence_baseline": {
        "name": "no-influence persistence; same initial states",
        "final_count": {
          "runs": 1,
          "mean": "1",
          "population_variance": "0",
          "population_denominator": 1,
          "sample_variance": null,
          "sample_denominator": null,
          "sample_status": "not_estimable"
        },
        "paired_gains": [
          1
        ],
        "gain": {
          "runs": 1,
          "mean": "1",
          "population_variance": "0",
          "population_denominator": 1,
          "sample_variance": null,
          "sample_denominator": null,
          "sample_status": "not_estimable"
        }
      },
      "converged_runs": 0,
      "truncated_runs": 1
    }
  ],
  "comparisons": [
    {
      "scenario": "base",
      "reference": "base",
      "changed_parameters": [],
      "identical_configuration": true,
      "paired_final_differences": [
        0
      ],
      "statistics": {
        "runs": 1,
        "mean": "0",
        "population_variance": "0",
        "population_denominator": 1,
        "sample_variance": null,
        "sample_denominator": null,
        "sample_status": "not_estimable"
      },
      "pairing_stream_sha256": "d8d164b0a8fb92c56fa3d71a953ff79db86278fe564971f7936e80e2ef9b22de"
    }
  ],
  "sources": [
    {
      "id": "psychohistory-foundation-v1",
      "technique_id": 52,
      "rank": 1,
      "author": "Isaac Asimov",
      "edition": "Foundation; Del Rey paperback, 2008-04-29; ISBN9780553382570;272pages",
      "url": "https://www.penguinrandomhouse.com/books/5655/foundation-by-isaac-asimov/",
      "locator": "Publisher product details; separate1991mass-market and2004ebook formats",
      "ingestion": "facts_only",
      "rights_note": "Copyrighted novel; metadata and original brief factual notes only. No novel body redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-pentland-v1",
      "technique_id": 52,
      "rank": 2,
      "author": "Alex Pentland / MIT Industrial Liaison Program",
      "edition": "Original ranked MIT book lead: Social Physics: How Ideas Turn into Action; listing dated2013-09-27",
      "url": "https://ilpstex.mit.edu/content/books/social-physics-how-ideas-turn-into-action-25070",
      "locator": "Book listing; its webpage date/heading are not silently substituted for a verified book-edition publication date/subtitle",
      "ingestion": "facts_only",
      "rights_note": "Facts-only listing/context. Promotional predictive claims are not algorithm or empirical-validation evidence.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-page-v1",
      "technique_id": 52,
      "rank": 3,
      "author": "Scott E. Page",
      "edition": "The Model Thinker: What You Need to Know to Make Data Work for You; Basic Books hardcover,2018-11-27;ISBN9780465094622;448pages",
      "url": "https://www.hachettebookgroup.com/titles/scott-e-page/the-model-thinker/9780465094622/?lens=basic-books",
      "locator": "Publisher edition metadata and many-model description; detailed book chapters not inspected",
      "ingestion": "facts_only",
      "rights_note": "Copyrighted book; facts-only edition/context notes. No unauthorized full-book copy or chapter formulas ingested.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-foundation-excerpt-v1",
      "technique_id": 52,
      "rank": null,
      "author": "Isaac Asimov / Penguin Random House",
      "edition": "Authorized Foundation opening excerpt on publisher retailer page; excerpt copyright notice2004, distinct from2008product format",
      "url": "https://www.penguinrandomhouseretail.com/book/?isbn=9780553382570",
      "locator": "Excerpt introduction of Gaal and the Seldon Project; sample does not expose a complete predictive method",
      "ingestion": "facts_only",
      "rights_note": "Publisher explicitly reserves excerpt reproduction rights; read only. No passages redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-foundation-history-v1",
      "technique_id": 52,
      "rank": null,
      "author": "The Encyclopedia of Science Fiction; Asimov entry",
      "edition": "Literary bibliography updated2026-09-07",
      "url": "https://sf-encyclopedia.com/entry/asimov_isaac",
      "locator": "Foundation sequence publication paragraph:1942–1944Astounding material,1951fixup; literary secondary source only",
      "ingestion": "facts_only",
      "rights_note": "Facts-only literary history. Not a technical/scientific source or a license for novel text.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-fiction-boundary-v1",
      "technique_id": 52,
      "rank": null,
      "author": "The Encyclopedia of Science Fiction; Psychohistory entry",
      "edition": "Literary theme entry updated2026-07-06",
      "url": "https://sf-encyclopedia.com/entry/psychohistory",
      "locator": "Fictional mass-behavior and observer-unawareness assumptions; distinguishes the historical-psychology homonym",
      "ingestion": "facts_only",
      "rights_note": "Original concise paraphrase only; no quoted novel passage. Literary interpretation is not empirical proof.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-pentland-edition-v1",
      "technique_id": 52,
      "rank": null,
      "author": "Alex Pentland / Penguin Random House",
      "edition": "Social Physics; Penguin Books paperback,2015-01-27;ISBN9780143126331;320pages; separately listed2014-01-30ebook",
      "url": "https://www.penguinrandomhouse.com/books/314230/social-physics-by-alex-pentland/",
      "locator": "Publisher format metadata; no detailed chapter algorithm available in the retailer payload",
      "ingestion": "facts_only",
      "rights_note": "Copyrighted book; metadata/context only. Broader book quantitative claims remain unimplemented and unvalidated here.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-pentland-whitepaper-v1",
      "technique_id": 52,
      "rank": null,
      "author": "Alex Pentland, David Lazer, Devon Brewer, Tracy Heibeck",
      "edition": "Using Reality Mining to Improve Public Health and Medicine; Robert Wood Johnson Foundation-commissioned whitepaper,February2009;16pages",
      "url": "https://hd.media.mit.edu/RWJF-Reality-Mining-summary.pdf",
      "locator": "Sections1.2 and privacy framework;100phone MIT2004–2005 study description",
      "ingestion": "facts_only",
      "rights_note": "Primary author-hosted contextual reading, not a dataset license. No PDF,figures,individual traces or medical-performance claims redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-page-paperback-v1",
      "technique_id": 52,
      "rank": null,
      "author": "Scott E. Page / Basic Books",
      "edition": "The Model Thinker; trade paperback,2021-03-16;ISBN9781541675711;464pages; distinct from2018hardcover",
      "url": "https://www.hachettebookgroup.com/titles/scott-e-page/the-model-thinker/9781541675711/?lens=basic-books",
      "locator": "Publisher format link from the2018hardcover page; do not assume page or byte equivalence",
      "ingestion": "facts_only",
      "rights_note": "Metadata only; publisher copyright and third-party content restrictions retained.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-watts-threshold-v1",
      "technique_id": 52,
      "rank": null,
      "author": "Duncan J. Watts",
      "edition": "A simple model of global cascades on random networks;PNAS99(9),5766–5771;2002-04-30;DOI10.1073/pnas.082090499",
      "url": "https://snap.stanford.edu/class/cs224w-readings/watts02randomnetworks.pdf",
      "locator": "Primary authored article at institutional mirror; Model Specification,p5767; primary indexed full paragraph inspected",
      "ingestion": "facts_only",
      "rights_note": "Copyright2002National Academy of Sciences per primary metadata. Facts and original mathematical notes only; no PDF/source figures redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-census-v1",
      "technique_id": 52,
      "rank": null,
      "author": "U.S. Census Bureau",
      "edition": "Population Estimates APIs documentation; revised2026-05-20; page example Vintage2023",
      "url": "https://www.census.gov/data/developers/data-sets/popest-popproj/popest.html",
      "locator": "Vintage replacement and births/deaths/migration description; current API-key requirement",
      "ingestion": "facts_only",
      "rights_note": "Documentation inspected only; no data acquired or selected file-level rights certified. Do not assume third-party assets share a blanket license.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-sociopatterns-v1",
      "technique_id": 52,
      "rank": null,
      "author": "SocioPatterns collaboration",
      "edition": "High school dynamic contact networks; dataset page2014-08-24;2011/2012Marseilles observations",
      "url": "https://sociopatterns.org/datasets/high-school-dynamic-contact-networks/",
      "locator": "Contact-list format,20second time bins,anonymous supplier IDs,class/gender metadata andTerms and Conditions",
      "ingestion": "facts_only",
      "rights_note": "Dataset terms link CC BY-NC-SA3.0;attribution,noncommercial andshare-alike limits retained. No contact files or participant metadata acquired; privacy/consent scope not certified.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-sociopatterns-license-v1",
      "technique_id": 52,
      "rank": null,
      "author": "Creative Commons",
      "edition": "Attribution-NonCommercial-ShareAlike3.0Unported deed",
      "url": "https://creativecommons.org/licenses/by-nc-sa/3.0/",
      "locator": "Exact linked license from SocioPatterns Terms and Conditions",
      "ingestion": "facts_only",
      "rights_note": "License metadata only. Privacy/publicity rights can remain separate; no assertion of permission for this project's unexamined uses.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "psychohistory-page-context-v1",
      "technique_id": 52,
      "rank": null,
      "author": "Scott E. Page / University of Michigan",
      "edition": "Official faculty publication context for The Model Thinker",
      "url": "https://lsa.umich.edu/cscs/people/core-faculty/spage.html",
      "locator": "Highlighted book and research context; detailed computational chapter examples unavailable in inspected pages",
      "ingestion": "facts_only",
      "rights_note": "Facts-only context; no book text,course recordings or example code redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    }
  ],
  "interpretation": {
    "fictional_inspiration": "Asimov; fictional premise",
    "simulation": "Original synthetic editorial synchronous finite-graph model",
    "scenario_differences": "Hypothetical model sensitivity only",
    "empirical_calibration": "unsupported",
    "held_out_validation": "unsupported",
    "causal_inference": "unsupported",
    "rounds": "Dimensionless steps; not dates",
    "statistics": "Exact deterministic finite-PRNG sample summaries; correlated cascade outcomes; no confidence interval or guaranteed CRN variance reduction"
  },
  "limits": [
    "Real population forecasting",
    "Empirical calibration",
    "Held-out predictive validation",
    "Causal inference",
    "Asimovian population laws",
    "Dynamic/weighted graphs",
    "Births/deaths/migration",
    "Learning/adaptation",
    "Infection/recovery",
    "Per-contact transmission",
    "Watts random-asynchronous experiment reproduction"
  ],
  "report_sha256": "452f28cb6d773939d4f82f8d9beae5102942f81fa3a5b7d3a588d7de6a1c3423"
}
```

