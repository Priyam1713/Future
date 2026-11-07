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
      "size": 4,
      "nodes": [
        "000",
        "001",
        "002",
        "003"
      ]
    },
    "runs": 8,
    "rounds": 4,
    "trace_states": false,
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
          ],
          [
            "002",
            "003"
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
          },
          {
            "node": "003",
            "phi": "1/2"
          }
        ],
        "initial": {
          "mode": "bernoulli",
          "probability": "0",
          "fixed_seeds": [],
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
  "input_sha256": "b8914a5b282f891fe0da02686686c08e37201d86fa14e7d6e9e8b3d8071af20f",
  "code_sha256": "fd187915dfca927e046800be389a1fe9b547653488d29055fcfb5cfb39445386",
  "source_manifest_sha256": "9dbd60a7838818c8e4332caaea837b4a2e7232ec02ec1a8434415150880144db",
  "source_freeze_sha256": "59a045aa4a7ee17579f7973cc91f2175fe842302c61dc087ae8bd919d914c99a",
  "source_snapshot_sha256": "8f263eb52465b0e892fa5463028cef8f29dd999e333165f83a9fdd664bf12abe",
  "stream_sha256": "7461fb7e78801025e47dc1382046fe2771fff76647922ad72122a7c943834f79",
  "draw_count": 32,
  "budget": {
    "work_units": 400,
    "count_cells": 218,
    "state_cells": 0
  },
  "scenarios": [
    {
      "id": "base",
      "graph_sha256": "aad557d9fec5bdaf7e41f73df700b7b913726d3f0dd01faa1cfa618d84505b9b",
      "thresholds_sha256": "b92dc65f91b824a5e2f209b1ffa8fe7daa5b87db3d96159fe5d0aa55f7d17b06",
      "initial_spec_sha256": "866f2b66d2ad5fafd4740c68b28e1280c688c4c66ee514f2724b80ff4b2f5fbc",
      "model_sha256": "5f65b026eeead8f3c083797b194f9b71b08cd22a072393559dc3a693d9a328a3",
      "initialization_design": "bernoulli",
      "rows": [
        {
          "run": 0,
          "initial_active": 0,
          "final_active": 0,
          "initial_fraction": "0",
          "final_fraction": "0",
          "active_counts": [
            0
          ],
          "inactive_counts": [
            4
          ],
          "states": null,
          "initial_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "final_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "draw_row_sha256": "47a2d8958cdfa6581ea0e96fa06a4b19bbd516eb7378ce326fed62aa6b7b5ae2",
          "converged": true,
          "truncated": false,
          "executed_rounds": 0,
          "persistence_final_active": 0,
          "paired_gain": 0
        },
        {
          "run": 1,
          "initial_active": 0,
          "final_active": 0,
          "initial_fraction": "0",
          "final_fraction": "0",
          "active_counts": [
            0
          ],
          "inactive_counts": [
            4
          ],
          "states": null,
          "initial_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "final_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "draw_row_sha256": "d9cbdd23e9b99e064a4db48d56d2746866c8256f21699b6cd86b78e4c29e3eed",
          "converged": true,
          "truncated": false,
          "executed_rounds": 0,
          "persistence_final_active": 0,
          "paired_gain": 0
        },
        {
          "run": 2,
          "initial_active": 0,
          "final_active": 0,
          "initial_fraction": "0",
          "final_fraction": "0",
          "active_counts": [
            0
          ],
          "inactive_counts": [
            4
          ],
          "states": null,
          "initial_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "final_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "draw_row_sha256": "e642f46d5a39e30c916e8a1f9811446f264c47fd434463d17a637f706f588b68",
          "converged": true,
          "truncated": false,
          "executed_rounds": 0,
          "persistence_final_active": 0,
          "paired_gain": 0
        },
        {
          "run": 3,
          "initial_active": 0,
          "final_active": 0,
          "initial_fraction": "0",
          "final_fraction": "0",
          "active_counts": [
            0
          ],
          "inactive_counts": [
            4
          ],
          "states": null,
          "initial_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "final_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "draw_row_sha256": "b9760ac3f26675b69317db39d32fadf58c5dcf08c9a412c03a27ac63f8358d8c",
          "converged": true,
          "truncated": false,
          "executed_rounds": 0,
          "persistence_final_active": 0,
          "paired_gain": 0
        },
        {
          "run": 4,
          "initial_active": 0,
          "final_active": 0,
          "initial_fraction": "0",
          "final_fraction": "0",
          "active_counts": [
            0
          ],
          "inactive_counts": [
            4
          ],
          "states": null,
          "initial_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "final_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "draw_row_sha256": "82a7f9ad560aff05c4dd86ba556033f0eb19b22dc7cd1f55e6827a523f5724c6",
          "converged": true,
          "truncated": false,
          "executed_rounds": 0,
          "persistence_final_active": 0,
          "paired_gain": 0
        },
        {
          "run": 5,
          "initial_active": 0,
          "final_active": 0,
          "initial_fraction": "0",
          "final_fraction": "0",
          "active_counts": [
            0
          ],
          "inactive_counts": [
            4
          ],
          "states": null,
          "initial_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "final_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "draw_row_sha256": "f4b794e92f4f7f91f2c138667047815ae06051ea366342182060d8885a1ad3b6",
          "converged": true,
          "truncated": false,
          "executed_rounds": 0,
          "persistence_final_active": 0,
          "paired_gain": 0
        },
        {
          "run": 6,
          "initial_active": 0,
          "final_active": 0,
          "initial_fraction": "0",
          "final_fraction": "0",
          "active_counts": [
            0
          ],
          "inactive_counts": [
            4
          ],
          "states": null,
          "initial_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "final_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "draw_row_sha256": "d13b58677d993a41e8961fa376f6ecb7e552736fd0f61555672678916f29109f",
          "converged": true,
          "truncated": false,
          "executed_rounds": 0,
          "persistence_final_active": 0,
          "paired_gain": 0
        },
        {
          "run": 7,
          "initial_active": 0,
          "final_active": 0,
          "initial_fraction": "0",
          "final_fraction": "0",
          "active_counts": [
            0
          ],
          "inactive_counts": [
            4
          ],
          "states": null,
          "initial_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "final_state_sha256": "1c10b03518fff8fc374a20bbf5107c66496656bec0662d6c6db123d4a898f121",
          "draw_row_sha256": "54e0e0040c9358e48583d5b029d72a29a372bb07f71c7c62fa33de2031e1cb52",
          "converged": true,
          "truncated": false,
          "executed_rounds": 0,
          "persistence_final_active": 0,
          "paired_gain": 0
        }
      ],
      "initial_count": {
        "runs": 8,
        "mean": "0",
        "population_variance": "0",
        "population_denominator": 8,
        "sample_variance": "0",
        "sample_denominator": 7,
        "sample_status": "estimable"
      },
      "final_count": {
        "runs": 8,
        "mean": "0",
        "population_variance": "0",
        "population_denominator": 8,
        "sample_variance": "0",
        "sample_denominator": 7,
        "sample_status": "estimable"
      },
      "initial_fraction": {
        "runs": 8,
        "mean": "0",
        "population_variance": "0",
        "population_denominator": 8,
        "sample_variance": "0",
        "sample_denominator": 7,
        "sample_status": "estimable"
      },
      "final_fraction": {
        "runs": 8,
        "mean": "0",
        "population_variance": "0",
        "population_denominator": 8,
        "sample_variance": "0",
        "sample_denominator": 7,
        "sample_status": "estimable"
      },
      "per_round_mean_active": [
        "0",
        "0",
        "0",
        "0",
        "0"
      ],
      "per_round_mean_inactive": [
        "4",
        "4",
        "4",
        "4",
        "4"
      ],
      "ideal_initial_moments": {
        "status": "ideal_iid_initial_only",
        "mean": "0",
        "variance": "0",
        "free_nodes": 4,
        "fixed_active": 0
      },
      "persistence_baseline": {
        "name": "no-influence persistence; same initial states",
        "final_count": {
          "runs": 8,
          "mean": "0",
          "population_variance": "0",
          "population_denominator": 8,
          "sample_variance": "0",
          "sample_denominator": 7,
          "sample_status": "estimable"
        },
        "paired_gains": [
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0
        ],
        "gain": {
          "runs": 8,
          "mean": "0",
          "population_variance": "0",
          "population_denominator": 8,
          "sample_variance": "0",
          "sample_denominator": 7,
          "sample_status": "estimable"
        }
      },
      "converged_runs": 8,
      "truncated_runs": 0
    }
  ],
  "comparisons": [
    {
      "scenario": "base",
      "reference": "base",
      "changed_parameters": [],
      "identical_configuration": true,
      "paired_final_differences": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "statistics": {
        "runs": 8,
        "mean": "0",
        "population_variance": "0",
        "population_denominator": 8,
        "sample_variance": "0",
        "sample_denominator": 7,
        "sample_status": "estimable"
      },
      "pairing_stream_sha256": "7461fb7e78801025e47dc1382046fe2771fff76647922ad72122a7c943834f79"
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
  "report_sha256": "1877cc76a03784dbd5281c8ff4ce7e43197f1ea9f193576825c58828d0448b77"
}
```

