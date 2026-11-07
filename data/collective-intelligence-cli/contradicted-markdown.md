# Collective intelligence — offline binary linear pool

```json
{
  "status": "accepted",
  "technique_id": 57,
  "schema_version": 1,
  "profile": {
    "id": "collective-intelligence-binary-linear-pool-v1",
    "version": 1,
    "sha256": "925a21d05410b91f073d50b403f17c3cf709d28194f539d5c292bf328dd8b854",
    "catalog_sha256": "4d5b136cc95b9747c782d1c446e1a8b36d157eeeae969cf4aa2b0a90ab071d58"
  },
  "request": {
    "schema_version": 1,
    "profile": {
      "id": "collective-intelligence-binary-linear-pool-v1",
      "version": 1,
      "sha256": "925a21d05410b91f073d50b403f17c3cf709d28194f539d5c292bf328dd8b854",
      "catalog_sha256": "4d5b136cc95b9747c782d1c446e1a8b36d157eeeae969cf4aa2b0a90ab071d58"
    },
    "pool": {
      "kind": "equal",
      "frozen_at": "2025-01-03T00:00:00Z",
      "weights_available_at": "2025-01-03T00:00:00Z"
    },
    "forecasters": [
      {
        "id": "fa",
        "kind": "synthetic",
        "dependency_group": "person-fa",
        "weight": "1"
      },
      {
        "id": "fb",
        "kind": "synthetic",
        "dependency_group": "person-fb",
        "weight": "1"
      }
    ],
    "questions": [
      {
        "definition": {
          "id": "q1",
          "version": 1,
          "event_id": "event1",
          "dependency_group": "group-event1",
          "partition": "test",
          "text": "Does synthetic event event1 occur?",
          "positive_rule": "Declared synthetic outcome1",
          "negative_rule": "Declared synthetic outcome0 at event end",
          "clarity_confirmed": true,
          "created_at": "2025-01-01T00:00:00Z",
          "locked_at": "2025-01-02T00:00:00Z",
          "cutoff": "2025-01-10T00:00:00Z",
          "event_end": "2025-01-20T00:00:00Z"
        },
        "resolution": {
          "status": "resolved",
          "outcome": 0,
          "event_at": "2025-01-20T00:00:00Z",
          "outcome_known_at": "2025-01-20T00:00:00Z",
          "resolved_at": "2025-01-21T00:00:00Z"
        }
      },
      {
        "definition": {
          "id": "q2",
          "version": 1,
          "event_id": "event2",
          "dependency_group": "group-event2",
          "partition": "test",
          "text": "Does synthetic event event2 occur?",
          "positive_rule": "Declared synthetic outcome1",
          "negative_rule": "Declared synthetic outcome0 at event end",
          "clarity_confirmed": true,
          "created_at": "2025-01-01T00:00:00Z",
          "locked_at": "2025-01-02T00:00:00Z",
          "cutoff": "2025-01-10T00:00:00Z",
          "event_end": "2025-01-20T00:00:00Z"
        },
        "resolution": {
          "status": "resolved",
          "outcome": 1,
          "event_at": "2025-01-20T00:00:00Z",
          "outcome_known_at": "2025-01-20T00:00:00Z",
          "resolved_at": "2025-01-21T00:00:00Z"
        }
      }
    ],
    "forecasts": [
      {
        "question_id": "q1",
        "question_sha256": "f71d8ea1393c306ee9329850b211694b2e52af6f3b6818ccd328bb110f9f2b2c",
        "forecaster": "fa",
        "revision": 1,
        "parent_sha256": null,
        "issued_at": "2025-01-05T00:00:00Z",
        "knowledge_at": "2025-01-04T00:00:00Z",
        "probability": "1"
      },
      {
        "question_id": "q1",
        "question_sha256": "f71d8ea1393c306ee9329850b211694b2e52af6f3b6818ccd328bb110f9f2b2c",
        "forecaster": "fb",
        "revision": 1,
        "parent_sha256": null,
        "issued_at": "2025-01-05T00:00:00Z",
        "knowledge_at": "2025-01-04T00:00:00Z",
        "probability": "1"
      },
      {
        "question_id": "q2",
        "question_sha256": "f161af50843968afccc8d2f984da0fa1ae6e8986a861411eacc071cd49e6bb22",
        "forecaster": "fa",
        "revision": 1,
        "parent_sha256": null,
        "issued_at": "2025-01-05T00:00:00Z",
        "knowledge_at": "2025-01-04T00:00:00Z",
        "probability": "0"
      },
      {
        "question_id": "q2",
        "question_sha256": "f161af50843968afccc8d2f984da0fa1ae6e8986a861411eacc071cd49e6bb22",
        "forecaster": "fb",
        "revision": 1,
        "parent_sha256": null,
        "issued_at": "2025-01-05T00:00:00Z",
        "knowledge_at": "2025-01-04T00:00:00Z",
        "probability": "0"
      }
    ],
    "provenance": {
      "evidence_mode": "synthetic",
      "source_ref": "collective-intelligence-mellers-author-v1",
      "rights": "self_authored",
      "attribution": "Future original fictional forecast example",
      "snapshot": "Self-authored fictional probability records; no participant data.",
      "snapshot_sha256": "d30bdfa4057e1a57b5cdbd5f7f6573eb60755ec35e88ead04ee24a4d4818b380"
    }
  },
  "input_sha256": "00397f0a59eb622c037f2abe0fcf2ddf99911f0b217411e5ce604f2185ea0984",
  "model_sha256": "d10dd89e2ec12637bbe04b80514f77217a2d3021d96c1ed7333b16b75e8ba88f",
  "split_sha256": "bbf1dfb05a93d6bf3ff670ae10a1229d31962eb7e7585aad6223ae36eab8aad7",
  "resolution_sha256": "f63b9d59b05d73f8fbefad20cbadfffa2141bae1a5e2da869c59ea335e5b5d52",
  "schema_sha256": "a4253b1a600b06ff9d67860ba9e13eea0bfe4759590942d49e4aad0af43f19c7",
  "source_manifest_sha256": "4d5b136cc95b9747c782d1c446e1a8b36d157eeeae969cf4aa2b0a90ab071d58",
  "source_freeze_sha256": "60d31c96e29d3a88b41af2e67d524a6e958440a7524b53558bcfd9b84c8fe8b1",
  "code_sha256": "134412c37ea8122285d7bb8a95717a71d0fed29a2a62cd11b3f7c5e5a2c819ba",
  "questions": {
    "q1": {
      "status": "estimable",
      "probability": "1",
      "equal_probability": "1",
      "selected_versions": {
        "fa": 1,
        "fb": 1
      },
      "selected_probabilities": {
        "fa": "1",
        "fb": "1"
      },
      "normalized_weights": {
        "fa": "1/2",
        "fb": "1/2"
      },
      "available_weight": "2",
      "contributors": 2,
      "equal_pool_participants": 2,
      "participant_accounting": [
        {
          "forecaster": "fa",
          "status": "contributing",
          "selected_revision": 1,
          "selected_record_sha256": "df31bca47e16a896730d624b78fb80db9adc5abd89b47ef90919871c5a2e5143",
          "probability": "1",
          "declared_weight": "1",
          "dependency_group": "person-fa",
          "kind": "synthetic",
          "revisions": [
            {
              "revision": 1,
              "record_sha256": "df31bca47e16a896730d624b78fb80db9adc5abd89b47ef90919871c5a2e5143",
              "decision": "eligible",
              "reasons": []
            }
          ]
        },
        {
          "forecaster": "fb",
          "status": "contributing",
          "selected_revision": 1,
          "selected_record_sha256": "5d083ce1fae14ccc2f22a3996ee2ca65eceffcbadf22671e79e578ce4f40f79f",
          "probability": "1",
          "declared_weight": "1",
          "dependency_group": "person-fb",
          "kind": "synthetic",
          "revisions": [
            {
              "revision": 1,
              "record_sha256": "5d083ce1fae14ccc2f22a3996ee2ca65eceffcbadf22671e79e578ce4f40f79f",
              "decision": "eligible",
              "reasons": []
            }
          ]
        }
      ],
      "question_sha256": "f71d8ea1393c306ee9329850b211694b2e52af6f3b6818ccd328bb110f9f2b2c",
      "resolution_sha256": "6248eabec15054626214d76101466f9e75a005f0507115181efa15b369391469",
      "resolution_status": "resolved",
      "exclusion_reason": null
    },
    "q2": {
      "status": "estimable",
      "probability": "0",
      "equal_probability": "0",
      "selected_versions": {
        "fa": 1,
        "fb": 1
      },
      "selected_probabilities": {
        "fa": "0",
        "fb": "0"
      },
      "normalized_weights": {
        "fa": "1/2",
        "fb": "1/2"
      },
      "available_weight": "2",
      "contributors": 2,
      "equal_pool_participants": 2,
      "participant_accounting": [
        {
          "forecaster": "fa",
          "status": "contributing",
          "selected_revision": 1,
          "selected_record_sha256": "88a2c35cc16aadb5ce21f54ff45dc01c23336dc5c6bd60d66a499dd4ccf5e4aa",
          "probability": "0",
          "declared_weight": "1",
          "dependency_group": "person-fa",
          "kind": "synthetic",
          "revisions": [
            {
              "revision": 1,
              "record_sha256": "88a2c35cc16aadb5ce21f54ff45dc01c23336dc5c6bd60d66a499dd4ccf5e4aa",
              "decision": "eligible",
              "reasons": []
            }
          ]
        },
        {
          "forecaster": "fb",
          "status": "contributing",
          "selected_revision": 1,
          "selected_record_sha256": "35a2ff54d886397e658304bf3d41007d5f050f154d28f5d1b2c655053f4afe52",
          "probability": "0",
          "declared_weight": "1",
          "dependency_group": "person-fb",
          "kind": "synthetic",
          "revisions": [
            {
              "revision": 1,
              "record_sha256": "35a2ff54d886397e658304bf3d41007d5f050f154d28f5d1b2c655053f4afe52",
              "decision": "eligible",
              "reasons": []
            }
          ]
        }
      ],
      "question_sha256": "f161af50843968afccc8d2f984da0fa1ae6e8986a861411eacc071cd49e6bb22",
      "resolution_sha256": "e6b47569c0807430339bb8097fbdb08683c49ee0f2284bc8bda232b22cd98724",
      "resolution_status": "resolved",
      "exclusion_reason": null
    }
  },
  "primary": {
    "status": "estimable",
    "count": 2,
    "question_ids": [
      "q1",
      "q2"
    ],
    "binary_brier": "1",
    "two_category_brier": "2",
    "equal_pool_brier": "1",
    "half_baseline_brier": "1/4",
    "half_baseline_improvement": "-3/4",
    "decomposition": {
      "grouping": "Exact identical Fraction probabilities,not coarse calibration bins",
      "groups": [
        {
          "probability": "0",
          "count": 1,
          "observed_frequency": "1"
        },
        {
          "probability": "1",
          "count": 1,
          "observed_frequency": "0"
        }
      ],
      "reliability": "1",
      "resolution": "1/4",
      "uncertainty": "1/4",
      "identity_passed": true
    },
    "calibration": [
      {
        "index": 0,
        "lower": "0",
        "upper": "1/10",
        "upper_inclusive": false,
        "count": 1,
        "positive_count": 1,
        "mean_probability": "0",
        "observed_frequency": "1"
      },
      {
        "index": 1,
        "lower": "1/10",
        "upper": "1/5",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 2,
        "lower": "1/5",
        "upper": "3/10",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 3,
        "lower": "3/10",
        "upper": "2/5",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 4,
        "lower": "2/5",
        "upper": "1/2",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 5,
        "lower": "1/2",
        "upper": "3/5",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 6,
        "lower": "3/5",
        "upper": "7/10",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 7,
        "lower": "7/10",
        "upper": "4/5",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 8,
        "lower": "4/5",
        "upper": "9/10",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 9,
        "lower": "9/10",
        "upper": "1",
        "upper_inclusive": true,
        "count": 1,
        "positive_count": 0,
        "mean_probability": "1",
        "observed_frequency": "0"
      }
    ],
    "scope": "Descriptive matched declared event scores; not empirical skill or independent-sample certification"
  },
  "train": {
    "status": "not_estimable",
    "count": 0,
    "question_ids": [],
    "binary_brier": null,
    "two_category_brier": null,
    "equal_pool_brier": null,
    "half_baseline_brier": null,
    "half_baseline_improvement": null,
    "decomposition": {
      "grouping": "Exact identical Fraction probabilities,not coarse calibration bins",
      "groups": [],
      "reliability": null,
      "resolution": null,
      "uncertainty": null,
      "identity_passed": null
    },
    "calibration": [
      {
        "index": 0,
        "lower": "0",
        "upper": "1/10",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 1,
        "lower": "1/10",
        "upper": "1/5",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 2,
        "lower": "1/5",
        "upper": "3/10",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 3,
        "lower": "3/10",
        "upper": "2/5",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 4,
        "lower": "2/5",
        "upper": "1/2",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 5,
        "lower": "1/2",
        "upper": "3/5",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 6,
        "lower": "3/5",
        "upper": "7/10",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 7,
        "lower": "7/10",
        "upper": "4/5",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 8,
        "lower": "4/5",
        "upper": "9/10",
        "upper_inclusive": false,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      },
      {
        "index": 9,
        "lower": "9/10",
        "upper": "1",
        "upper_inclusive": true,
        "count": 0,
        "positive_count": 0,
        "mean_probability": null,
        "observed_frequency": null
      }
    ],
    "scope": "Descriptive matched declared event scores; not empirical skill or independent-sample certification"
  },
  "individuals": {
    "fa": {
      "question_ids": [
        "q1",
        "q2"
      ],
      "count": 2,
      "individual_brier": "1",
      "aggregate_brier": "1",
      "status": "estimable"
    },
    "fb": {
      "question_ids": [
        "q1",
        "q2"
      ],
      "count": 2,
      "individual_brier": "1",
      "aggregate_brier": "1",
      "status": "estimable"
    }
  },
  "dependence": {
    "forecaster_groups": {
      "person-fa": [
        "fa"
      ],
      "person-fb": [
        "fb"
      ]
    },
    "dependent_groups": [],
    "kind_counts": {
      "human_declared": 0,
      "synthetic": 2,
      "llm_simulated": 0
    },
    "independence_certified": false,
    "effective_sample_size": null
  },
  "denominators": {
    "planned_questions": 2,
    "unique_events": 2,
    "question_dependency_groups": 2,
    "forecasters": 2,
    "forecaster_dependency_groups": 2,
    "revisions": 4,
    "rejected_revisions": 0,
    "selected_pairs": 4,
    "test_scored_questions": 2,
    "train_scored_questions": 0
  },
  "budget": {
    "work": 384,
    "returned_cells": 160
  },
  "sources": [
    {
      "id": "collective-intelligence-malone-v1",
      "technique_id": 57,
      "rank": 1,
      "author": "Thomas W. Malone",
      "edition": "Superminds: The Surprising Power of People and Computers Thinking Together;2018",
      "url": "https://cci.mit.edu/superminds-by-thomas-w-malone/",
      "locator": "Original MIT author/institute descriptive overview; human/computer collective design,not a numerical weighting recipe. Full book not inspected.",
      "ingestion": "facts_only",
      "rights_note": "Book copyright retained; facts/metadata only,no body or figures reproduced.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "collective-intelligence-surowiecki-v1",
      "technique_id": 57,
      "rank": 2,
      "author": "James Surowiecki",
      "edition": "The Wisdom of Crowds; publisher-listed paperbackISBN9780385721707",
      "url": "https://www.penguinrandomhouse.com/books/175380/the-wisdom-of-crowds-by-james-surowiecki/9780385721707/",
      "locator": "Publisher metadata/overview inspected; original inventory URL null resolved without changing rank. No detailed chapter or algorithm extraction.",
      "ingestion": "facts_only",
      "rights_note": "Publisher copyright; no book body or figures redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "collective-intelligence-mellers-v1",
      "technique_id": 57,
      "rank": 3,
      "author": "Barbara Mellers et al.",
      "edition": "Psychological Strategies for Winning a Geopolitical Forecasting Tournament;Psychological Science25(5),1106–1115;online21March2014;DOI10.1177/0956797614524255",
      "url": "https://pubmed.ncbi.nlm.nih.gov/24659192/",
      "locator": "Original ranked PubMed bibliographic/abstract page;13author list. Full article inspected separately through author witness.",
      "ingestion": "facts_only",
      "rights_note": "Facts only; indexed free access does not imply dataset reuse permission.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "collective-intelligence-malone-publisher-v1",
      "technique_id": 57,
      "rank": null,
      "author": "Thomas W. Malone / Hachette",
      "edition": "Superminds ebook;15May2018;ISBN9780316349109;384pages",
      "url": "https://www.hachettebookgroup.com/titles/thomas-w-malone/superminds/9780316349109/",
      "locator": "Official publisher format metadata observed in indexed page.",
      "ingestion": "facts_only",
      "rights_note": "Facts-only metadata; no book text reproduced.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "collective-intelligence-surowiecki-format-v1",
      "technique_id": 57,
      "rank": null,
      "author": "James Surowiecki / Penguin Random House",
      "edition": "The Wisdom of Crowds;paperback16August2005;336pages;ISBN9780385721707",
      "url": "https://penguinrandomhousesecondaryeducation.com/book/?isbn=9780385721707",
      "locator": "Official indexed format metadata; direct follow-up timed out. Do not confuse with2004ebook edition.",
      "ingestion": "facts_only",
      "rights_note": "Facts-only metadata; full book access/rights unverified.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "collective-intelligence-mellers-author-v1",
      "technique_id": 57,
      "rank": null,
      "author": "Barbara Mellers et al. / University of Pennsylvania",
      "edition": "2014author-hosted10-page primary paper;DOI10.1177/0956797614524255",
      "url": "https://faculty.wharton.upenn.edu/wp-content/uploads/2015/07/2014---psychological-strategies-for-winning-a-tournament.pdf",
      "locator": "Methods/scoring and note1:two-category0–2 Brier; daily/question averaging; exact-category reliability-resolution-uncertainty decomposition. Advanced aggregation algorithms reported elsewhere; team leaderboard medians are not probability-mean pooling.",
      "ingestion": "facts_only",
      "rights_note": "Copyright authors2014; reading witness only,no paper,figures or third-party code/data redistributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "collective-intelligence-brier-v1",
      "technique_id": 57,
      "rank": null,
      "author": "Glenn W. Brier",
      "edition": "Verification of Forecasts Expressed in Terms of Probability;Monthly Weather Review78(1),1–3;1950",
      "url": "https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml",
      "locator": "Publisher indexed metadata; direct access403. No full text access claimed; numerical conventions supported by Mellers primary methods and existing51 contracts.",
      "ingestion": "facts_only",
      "rights_note": "Metadata and mathematical facts only; no text distributed.",
      "checked_on": "2026-11-08",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    }
  ],
  "evidence_mode": "synthetic",
  "empirical_skill_validated": false,
  "compatibility_51": {
    "profile": "tetlock-mellers-binary-forecast-updates-v1",
    "conventions": "Exact probabilities,UTC-Z/cutoff-inclusive timing,binary0–1 and two-category0–2 scores,exact decomposition",
    "full_ledger_adapter": "unsupported"
  },
  "limitations": [
    "Automatic independence or empirical skill certification",
    "Learned weights from current outcomes",
    "Full51ledger adapter",
    "Iterative Delphi orchestration",
    "LLM/provider APIs",
    "Complete tournament operations",
    "Automatic statistical significance",
    "Linear-pool software correctness is not proof of independent crowd wisdom or empirical superiority.",
    "Clocks,identities,dependencies,rights and labels are declarations; hashes cannot independently certify them.",
    "Parent chains are local commitments; owner can rewrite all history without an external anchor.",
    "Mellers daily/question-standardized tournament and team-median leaderboard results are not reproduced."
  ],
  "report_sha256": "711ed549243ae883f49b0fc0fe3dc8377e21f5ea2debbd673afd9ae37c3cb869"
}
```

