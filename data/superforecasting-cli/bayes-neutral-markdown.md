# Superforecasting Workbench

Status: accepted

Synthetic software validation or user-supplied unvalidated records;empirical skill validated: false.

| Slot | Selected version | Status | Binary Brier |
|---|---|---|---|
| f1 | 2 | unresolved | None |

Primary binary Brier: None
Primary two-category sum: None
Natural-log loss status: not_estimable

Selection/availability,identity,rights,comparability andconditional independence aredeclared,not externallyattested.
Multiple participants/updates share events;counts are not effective independent sample sizes.
Calibration andscores are descriptive;synthetic validation establishes software mechanics,not human superforecasting skill.
Local owners can rewrite all hashes/history;prospective integrity requires independent anchoring.

Arithmetic andledger correctness are not demonstrated human expertise,geopolitical skill orhistorical tournament replication.
Book later chapters andGJP file-level rights/completeness remain unverified;no corpus acquired.
Source facts andworkflow context areseparate fromeditorial schema,cutoff,binning andreport conventions.

```json
{
  "status": "accepted",
  "task": "update",
  "profile": {
    "id": "tetlock-mellers-binary-forecast-updates-v1",
    "sha256": "bd6d71ded4dbb2ddc1f60b230c46daff2b735793f6bfe4098899d49bfc6b9933",
    "catalog_sha256": "7502f901d5e17b31e7e798e192473bc8ae73854e863484c2f65a6f251d841e0b"
  },
  "request": {
    "schema_version": 1,
    "profile": {
      "id": "tetlock-mellers-binary-forecast-updates-v1",
      "sha256": "bd6d71ded4dbb2ddc1f60b230c46daff2b735793f6bfe4098899d49bfc6b9933",
      "catalog_sha256": "7502f901d5e17b31e7e798e192473bc8ae73854e863484c2f65a6f251d841e0b"
    },
    "task": "update",
    "payload": {
      "ledger": {
        "schema_version": 1,
        "profile_sha256": "bd6d71ded4dbb2ddc1f60b230c46daff2b735793f6bfe4098899d49bfc6b9933",
        "plan": {
          "study_id": "synthetic-study",
          "created_at": "2025-01-01T00:00:00Z",
          "evidence_mode": "synthetic_software_validation",
          "domain": "synthetic-switches",
          "horizon": "fixed-window",
          "partition": {
            "frozen_at": "2024-12-31T00:00:00Z",
            "train_groups": [
              "history"
            ],
            "test_groups": [
              "test1"
            ]
          },
          "questions": [
            {
              "id": "q1",
              "version": 1,
              "event_id": "event1",
              "dependency_group": "test1",
              "partition": "test",
              "text": "Will synthetic switch 1 enter state 1 in the declared observation window?",
              "event_definition": "Binary occurrence recorded by the synthetic switch log",
              "window_start": "2025-01-01T00:00:00Z",
              "window_end": "2025-01-10T00:00:00Z",
              "cutoff": "2025-01-03T00:00:00Z",
              "created_at": "2024-12-31T00:00:00Z",
              "locked_at": "2024-12-31T00:00:00Z",
              "timezone": "UTC",
              "clarity_confirmed": true,
              "resolution": {
                "source_ref": "original-synthetic-switch-log",
                "positive_rule": "First state1 observation within the half-open window",
                "negative_rule": "No state1 observation through the complete window",
                "dispute_policy": "Disputed questions are excluded pending a sourced correction",
                "void_policy": "Incomplete observation logs void the question"
              },
              "class_id": "class1",
              "class_sha256": "beaeee6344c02525dcbb5e6933069bb89a454a85c24893e0ffbb701a6158bae7",
              "baseline": {
                "kind": "constant",
                "probability": "1/2",
                "frozen_at": "2024-12-31T00:00:00Z",
                "domain": "synthetic-switches",
                "horizon": "fixed-window",
                "source": {
                  "id": "baseline-source",
                  "locator": "original:baseline-source",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: baseline-source",
                  "snapshot_sha256": "ee865768d0e9b7ee132821254268aabfb5d991fbfd408ed585e6f2d4b252fc43",
                  "available_at": "2024-12-30T00:00:00Z"
                }
              },
              "reasoning": {
                "base_rate_rationale": "Documentary synthetic reasoning only",
                "comparability": "Documentary synthetic reasoning only",
                "assumptions": [],
                "subquestions": [],
                "evidence_gaps": [],
                "alternatives": [],
                "dependence": "Documentary synthetic reasoning only",
                "disagreement": "Documentary synthetic reasoning only"
              },
              "source": {
                "id": "question-source",
                "locator": "original:question-source",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: question-source",
                "snapshot_sha256": "7d584a19ae00f69e020e04d21268fa118b6ee1b1a046cfbee85622bf1659dacf",
                "available_at": "2024-12-30T00:00:00Z"
              }
            }
          ],
          "classes": [
            {
              "id": "class1",
              "version": 1,
              "target_question_id": "q1",
              "definition": "Original finite synthetic historical switch events",
              "eligibility_rule": "All distinct synthetic switch events in the declared historical window",
              "frozen_at": "2024-12-30T00:00:00Z",
              "availability_cutoff": "2024-12-29T00:00:00Z",
              "comparability": "Synthetic demonstration only;no population representativeness claimed.",
              "members": [
                {
                  "id": "m0",
                  "event_id": "historical-0",
                  "dependency_group": "history",
                  "eligibility": "included",
                  "reason": "Eligible under the frozen synthetic rule",
                  "status": "resolved",
                  "outcome": 1,
                  "event_at": "2024-12-01T00:00:00Z",
                  "observed_at": "2024-12-20T00:00:00Z",
                  "source": {
                    "id": "member-0",
                    "locator": "original:member-0",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: member-0",
                    "snapshot_sha256": "b2c56227f8f73938d69b8476d05b6b3db549b170d49e1ec2529994a990cd45d8",
                    "available_at": "2024-12-20T00:00:00Z"
                  }
                },
                {
                  "id": "m1",
                  "event_id": "historical-1",
                  "dependency_group": "history",
                  "eligibility": "included",
                  "reason": "Eligible under the frozen synthetic rule",
                  "status": "resolved",
                  "outcome": 1,
                  "event_at": "2024-12-02T00:00:00Z",
                  "observed_at": "2024-12-20T00:00:00Z",
                  "source": {
                    "id": "member-1",
                    "locator": "original:member-1",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: member-1",
                    "snapshot_sha256": "80a4c7004b3e2d93e9aa55f08b6428c23aefcac01f76ebefbb798af6d4c87443",
                    "available_at": "2024-12-20T00:00:00Z"
                  }
                },
                {
                  "id": "m2",
                  "event_id": "historical-2",
                  "dependency_group": "history",
                  "eligibility": "included",
                  "reason": "Eligible under the frozen synthetic rule",
                  "status": "resolved",
                  "outcome": 1,
                  "event_at": "2024-12-03T00:00:00Z",
                  "observed_at": "2024-12-20T00:00:00Z",
                  "source": {
                    "id": "member-2",
                    "locator": "original:member-2",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: member-2",
                    "snapshot_sha256": "019f9724fabd99e5cffc8e64da53e9be85e9d6984ddbebcfcf637cca5d88680b",
                    "available_at": "2024-12-20T00:00:00Z"
                  }
                },
                {
                  "id": "m3",
                  "event_id": "historical-3",
                  "dependency_group": "history",
                  "eligibility": "included",
                  "reason": "Eligible under the frozen synthetic rule",
                  "status": "resolved",
                  "outcome": 0,
                  "event_at": "2024-12-04T00:00:00Z",
                  "observed_at": "2024-12-20T00:00:00Z",
                  "source": {
                    "id": "member-3",
                    "locator": "original:member-3",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: member-3",
                    "snapshot_sha256": "1bbccc0692938b7c36f4e745a8cfbc084dff169af1bf68d8e9a9abc49dd86a1d",
                    "available_at": "2024-12-20T00:00:00Z"
                  }
                },
                {
                  "id": "m4",
                  "event_id": "historical-4",
                  "dependency_group": "history",
                  "eligibility": "included",
                  "reason": "Eligible under the frozen synthetic rule",
                  "status": "resolved",
                  "outcome": 0,
                  "event_at": "2024-12-05T00:00:00Z",
                  "observed_at": "2024-12-20T00:00:00Z",
                  "source": {
                    "id": "member-4",
                    "locator": "original:member-4",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: member-4",
                    "snapshot_sha256": "6a3969d2f67626987e4933118d5ec0702baa408e8c00f5bbe8d0e53c34fcf81c",
                    "available_at": "2024-12-20T00:00:00Z"
                  }
                },
                {
                  "id": "m5",
                  "event_id": "historical-5",
                  "dependency_group": "history",
                  "eligibility": "included",
                  "reason": "Eligible under the frozen synthetic rule",
                  "status": "resolved",
                  "outcome": 0,
                  "event_at": "2024-12-06T00:00:00Z",
                  "observed_at": "2024-12-20T00:00:00Z",
                  "source": {
                    "id": "member-5",
                    "locator": "original:member-5",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: member-5",
                    "snapshot_sha256": "7a132046ab2dece3d5a6e074bf672b503e41a5e6fa4a46ccc6492342a982e802",
                    "available_at": "2024-12-20T00:00:00Z"
                  }
                },
                {
                  "id": "m6",
                  "event_id": "historical-6",
                  "dependency_group": "history",
                  "eligibility": "included",
                  "reason": "Eligible under the frozen synthetic rule",
                  "status": "resolved",
                  "outcome": 0,
                  "event_at": "2024-12-07T00:00:00Z",
                  "observed_at": "2024-12-20T00:00:00Z",
                  "source": {
                    "id": "member-6",
                    "locator": "original:member-6",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: member-6",
                    "snapshot_sha256": "4fb9f6db24a04ca5191e98c461f07a2010598ff8d11fef41b929289a691ba1c7",
                    "available_at": "2024-12-20T00:00:00Z"
                  }
                },
                {
                  "id": "m7",
                  "event_id": "historical-7",
                  "dependency_group": "history",
                  "eligibility": "included",
                  "reason": "Eligible under the frozen synthetic rule",
                  "status": "resolved",
                  "outcome": 0,
                  "event_at": "2024-12-08T00:00:00Z",
                  "observed_at": "2024-12-20T00:00:00Z",
                  "source": {
                    "id": "member-7",
                    "locator": "original:member-7",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: member-7",
                    "snapshot_sha256": "b3891163980c3aaf9d38be9e161f503b1871a57c1af0199ecf683ea97bcf565e",
                    "available_at": "2024-12-20T00:00:00Z"
                  }
                },
                {
                  "id": "m8",
                  "event_id": "historical-8",
                  "dependency_group": "history",
                  "eligibility": "included",
                  "reason": "Eligible under the frozen synthetic rule",
                  "status": "resolved",
                  "outcome": 0,
                  "event_at": "2024-12-09T00:00:00Z",
                  "observed_at": "2024-12-20T00:00:00Z",
                  "source": {
                    "id": "member-8",
                    "locator": "original:member-8",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: member-8",
                    "snapshot_sha256": "f60c7a635c556c921a35312e862a7178464561ab6a4136cffc795cdd8690b07f",
                    "available_at": "2024-12-20T00:00:00Z"
                  }
                },
                {
                  "id": "m9",
                  "event_id": "historical-9",
                  "dependency_group": "history",
                  "eligibility": "included",
                  "reason": "Eligible under the frozen synthetic rule",
                  "status": "resolved",
                  "outcome": 0,
                  "event_at": "2024-12-10T00:00:00Z",
                  "observed_at": "2024-12-20T00:00:00Z",
                  "source": {
                    "id": "member-9",
                    "locator": "original:member-9",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: member-9",
                    "snapshot_sha256": "119152113fcdb397d68fb82c202cc4100cecc72e9c2f4b8cb973e293d548e8b5",
                    "available_at": "2024-12-20T00:00:00Z"
                  }
                }
              ],
              "source": {
                "id": "class-source",
                "locator": "original:class-source",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: class-source",
                "snapshot_sha256": "cba781691cf75ace7849c564f835eec03241068d1c0e83ffe164e9331d17aa72",
                "available_at": "2024-12-29T00:00:00Z"
              }
            }
          ],
          "slots": [
            {
              "forecast_id": "f1",
              "question_id": "q1",
              "participant": "person1",
              "participant_kind": "individual"
            }
          ],
          "provenance": {
            "id": "study-source",
            "locator": "original:study-source",
            "rights": "self_authored",
            "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
            "snapshot": "Original synthetic software validation evidence: study-source",
            "snapshot_sha256": "852af0c234dfa57c63067f12e4adb05ef1d3716e1dd8584ec9808d2e88225918",
            "available_at": "2024-12-30T00:00:00Z"
          }
        },
        "plan_sha256": "058e3b1fec80a53c2544a5e23f534b434b596d3eaead07312cc5bb9606c58702",
        "actions": [
          {
            "sequence": 1,
            "kind": "forecast",
            "at": "2025-01-01T12:00:00Z",
            "record": {
              "forecast_id": "f1",
              "question_id": "q1",
              "question_version": 1,
              "question_sha256": "1ab81cda71d093a51ea4218a1f08ae3922446cc760e6fb0b0002dc4a8bcbad70",
              "participant": "person1",
              "version": 1,
              "parent_sha256": null,
              "recorded_at": "2025-01-01T12:00:00Z",
              "knowledge_at": "2025-01-01T12:00:00Z",
              "probability": "1/5",
              "mode": "manual",
              "reason": "Original synthetic judgment",
              "evidence": [],
              "assumptions": [
                "Submitted probability is a synthetic judgment,not measured expertise"
              ],
              "outcome_known": false,
              "bayes": null
            },
            "parent_sha256": "058e3b1fec80a53c2544a5e23f534b434b596d3eaead07312cc5bb9606c58702",
            "decision": "accepted",
            "reason": null,
            "sha256": "9e555222f9827b8370da3322d1dcc954e91661d4739f45f4b2be20533b70bfd2"
          }
        ]
      },
      "record": {
        "forecast_id": "f1",
        "question_id": "q1",
        "question_version": 1,
        "question_sha256": "1ab81cda71d093a51ea4218a1f08ae3922446cc760e6fb0b0002dc4a8bcbad70",
        "participant": "person1",
        "version": 2,
        "parent_sha256": "f8729aecf950dc62cc2a28cbd5dcda9fcad9080fddc64ceda54f951ca5c510c5",
        "recorded_at": "2025-01-02T00:00:00Z",
        "knowledge_at": "2025-01-02T00:00:00Z",
        "probability": "1/5",
        "mode": "bayes",
        "reason": "Explicit synthetic likelihood-ratio update",
        "evidence": [
          {
            "id": "evidence1",
            "dependency_group": "evidence-group1",
            "original_fact_id": "fact1",
            "statement": "An original synthetic observation,not geopolitical evidence",
            "source": {
              "id": "source-evidence1",
              "locator": "original:source-evidence1",
              "rights": "self_authored",
              "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
              "snapshot": "Original synthetic software validation evidence: source-evidence1",
              "snapshot_sha256": "a3d7718607436ee4118c6d4108253dee5288e57a4b73bfaee47c2db7470d2726",
              "available_at": "2025-01-02T00:00:00Z"
            }
          }
        ],
        "assumptions": [
          "Submitted probability is a synthetic judgment,not measured expertise"
        ],
        "outcome_known": false,
        "bayes": {
          "kind": "ratio",
          "ratio": "1",
          "likelihood_h": null,
          "likelihood_not_h": null,
          "dependence": "first",
          "conditioned_on": [],
          "independent_given_h": false,
          "independent_given_not_h": false,
          "model_status": "user_assumed",
          "measurement_notes": "Assumed illustrative likelihood model;not measured evidence",
          "source": {
            "id": "likelihood-evidence1",
            "locator": "original:likelihood-evidence1",
            "rights": "self_authored",
            "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
            "snapshot": "Original synthetic software validation evidence: likelihood-evidence1",
            "snapshot_sha256": "52ad6f9f37c4c6ee357d02e0c7e3e0e39e793c137fa6a1f7c631c487a8430a19",
            "available_at": "2025-01-02T00:00:00Z"
          }
        }
      }
    }
  },
  "request_sha256": "bcfe07e5ffad840328e91006ce0dfa51b5c84e35c2c2972543d17137ceb0b7a5",
  "source_freeze_sha256": "b8c23a38db5511a2d6a73f8dddce441b22731b4e2de4d5e76b38ce1b22754563",
  "sources": [
    {
      "id": "superforecasting-book-v1",
      "technique_id": 51,
      "rank": 1,
      "author": "Philip E. Tetlock and Dan Gardner",
      "edition": "Superforecasting:The Art and Science of Prediction;2016paperback;ISBN9780804136716;352pages;Crown;2016-09-13",
      "url": "https://www.penguinrandomhouse.com/books/227815/superforecasting-by-philip-e-tetlock-and-dan-gardner/",
      "locator": "Publisher format metadata;2015-09-29ebook separately listed",
      "ingestion": "facts_only",
      "rights_note": "Publisher copyright;facts-only metadata,not full book ingestion.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "superforecasting-mellers-v1",
      "technique_id": 51,
      "rank": 2,
      "author": "Barbara Mellers et al.",
      "edition": "Psychological Strategies for Winning a Geopolitical Forecasting Tournament;Psychological Science25(5),1106–1115;online2014-03-21;May2014issue;DOI10.1177/0956797614524255",
      "url": "https://pubmed.ncbi.nlm.nih.gov/24659192/",
      "locator": "Original rank2locator;PubMed content unavailable here;metadata/fulltext verified separately throughSAGE andauthor witness",
      "ingestion": "facts_only",
      "rights_note": "Facts-only;PubMed URL is preserved,not evidence of local successful fulltext access.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "superforecasting-book-excerpt-v1",
      "technique_id": 51,
      "rank": null,
      "author": "Philip E. Tetlock and Dan Gardner / Penguin Random House",
      "edition": "Publisher-authorized2016excerpt;Chapter1 An Optimistic Skeptic",
      "url": "https://www.penguinrandomhouseretail.com/book/?isbn=9780804136716",
      "locator": "Excerpt section;dated,recorded andindependently assessed forecasts;no detailed later-chapter coverage inferred",
      "ingestion": "facts_only",
      "rights_note": "All rights reserved;explicit permission required for excerpt reproduction. Read only;no excerpt retained in repository.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "superforecasting-commandments-v1",
      "technique_id": 51,
      "rank": null,
      "author": "Good Judgment / Philip Tetlock and Dan Gardner",
      "edition": "Ten Commandments for Aspiring Superforecasters;primary organization publication of book-derived guidance",
      "url": "https://goodjudgment.com/philip-tetlocks-10-commandments-of-superforecasting/",
      "locator": "Items2,3,4,6,7,8,9,10;separate from publisher chapter excerpt",
      "ingestion": "facts_only",
      "rights_note": "Facts-only original brief paraphrase;no article text redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "superforecasting-mellers-sage-v1",
      "technique_id": 51,
      "rank": null,
      "author": "Barbara Mellers et al. / SAGE",
      "edition": "2014publisher metadata,abstract andOpen Practices statement",
      "url": "https://journals.sagepub.com/doi/pdf/10.1177/0956797614524255",
      "locator": "Bibliographic metadata;abstract;data-sharing statement;restricted-access article",
      "ingestion": "facts_only",
      "rights_note": "Copyright authors2014;SAGE reprints/permissions. Facts only;abstract is not a dataset license.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "superforecasting-mellers-author-v1",
      "technique_id": 51,
      "rank": null,
      "author": "Barbara Mellers et al. / University of Pennsylvania",
      "edition": "Author-hosted10page2014article witness,internal pages1–10;publication pages1106–1115 verified separately",
      "url": "https://faculty.wharton.upenn.edu/wp-content/uploads/2015/07/2014---psychological-strategies-for-winning-a-tournament.pdf",
      "locator": "Methods pp3–4,results pp4–9;Note1decomposition;do not assume byte identity withpublisher PDF",
      "ingestion": "facts_only",
      "rights_note": "Author copyright2014;legitimate author access,facts-only notes,no PDF/figures redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "superforecasting-proper-scores-v1",
      "technique_id": 51,
      "rank": null,
      "author": "Tilmann Gneiting and Adrian E. Raftery",
      "edition": "Strictly Proper Scoring Rules,Prediction,andEstimation;JASA102(477),359–378;2007;DOI10.1198/016214506000001437",
      "url": "https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf",
      "locator": "Section1 propriety andorientation;Section3 finite categorical/quadratic/logarithmic scores",
      "ingestion": "facts_only",
      "rights_note": "Copyright2007American Statistical Association;author-hosted access;math facts only,no PDF redistribution.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "superforecasting-bayes-v1",
      "technique_id": 51,
      "rank": null,
      "author": "MIT OpenCourseWare18.05",
      "edition": "Spring2022Class12 Prediction andOdds;21slide primary teaching handout",
      "url": "https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/mit18_05_s22_lec12.pdf",
      "locator": "Slides10–14odds/Bayes factor;18sequential updating",
      "ingestion": "facts_only",
      "rights_note": "Facts-only mathematical identity;no slide text/images redistributed or broad third-party image license assumed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "superforecasting-iarpa-data-v1",
      "technique_id": 51,
      "rank": null,
      "author": "IARPA",
      "edition": "IARPA Announces Publication ofData from theGood Judgment Project;2017-04-28",
      "url": "https://www.iarpa.gov/newsroom/article/iarpa-announces-publication-of-data-from-the-good-judgment-project",
      "locator": "Announcement links HarvardGJP archive anddescribes four-year forecast release",
      "ingestion": "facts_only",
      "rights_note": "Public announcement verifies existence,not file-level license/consent/completeness.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "superforecasting-dataverse-v1",
      "technique_id": 51,
      "rank": null,
      "author": "Good Judgment Project / Harvard Dataverse",
      "edition": "GJP repository access attempted2026-11-07;metadata/file rights not inspected",
      "url": "https://dataverse.harvard.edu/dataverse/gjp",
      "locator": "HTML human-verification response;public metadata API403;no dataset acquired",
      "ingestion": "facts_only",
      "rights_note": "Unknown file-level terms;no dataset redistribution or empirical certification authorized bythis audit.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    }
  ],
  "result": {
    "ledger": {
      "schema_version": 1,
      "profile_sha256": "bd6d71ded4dbb2ddc1f60b230c46daff2b735793f6bfe4098899d49bfc6b9933",
      "plan": {
        "study_id": "synthetic-study",
        "created_at": "2025-01-01T00:00:00Z",
        "evidence_mode": "synthetic_software_validation",
        "domain": "synthetic-switches",
        "horizon": "fixed-window",
        "partition": {
          "frozen_at": "2024-12-31T00:00:00Z",
          "train_groups": [
            "history"
          ],
          "test_groups": [
            "test1"
          ]
        },
        "questions": [
          {
            "id": "q1",
            "version": 1,
            "event_id": "event1",
            "dependency_group": "test1",
            "partition": "test",
            "text": "Will synthetic switch 1 enter state 1 in the declared observation window?",
            "event_definition": "Binary occurrence recorded by the synthetic switch log",
            "window_start": "2025-01-01T00:00:00Z",
            "window_end": "2025-01-10T00:00:00Z",
            "cutoff": "2025-01-03T00:00:00Z",
            "created_at": "2024-12-31T00:00:00Z",
            "locked_at": "2024-12-31T00:00:00Z",
            "timezone": "UTC",
            "clarity_confirmed": true,
            "resolution": {
              "source_ref": "original-synthetic-switch-log",
              "positive_rule": "First state1 observation within the half-open window",
              "negative_rule": "No state1 observation through the complete window",
              "dispute_policy": "Disputed questions are excluded pending a sourced correction",
              "void_policy": "Incomplete observation logs void the question"
            },
            "class_id": "class1",
            "class_sha256": "beaeee6344c02525dcbb5e6933069bb89a454a85c24893e0ffbb701a6158bae7",
            "baseline": {
              "kind": "constant",
              "probability": "1/2",
              "frozen_at": "2024-12-31T00:00:00Z",
              "domain": "synthetic-switches",
              "horizon": "fixed-window",
              "source": {
                "id": "baseline-source",
                "locator": "original:baseline-source",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: baseline-source",
                "snapshot_sha256": "ee865768d0e9b7ee132821254268aabfb5d991fbfd408ed585e6f2d4b252fc43",
                "available_at": "2024-12-30T00:00:00Z"
              }
            },
            "reasoning": {
              "base_rate_rationale": "Documentary synthetic reasoning only",
              "comparability": "Documentary synthetic reasoning only",
              "assumptions": [],
              "subquestions": [],
              "evidence_gaps": [],
              "alternatives": [],
              "dependence": "Documentary synthetic reasoning only",
              "disagreement": "Documentary synthetic reasoning only"
            },
            "source": {
              "id": "question-source",
              "locator": "original:question-source",
              "rights": "self_authored",
              "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
              "snapshot": "Original synthetic software validation evidence: question-source",
              "snapshot_sha256": "7d584a19ae00f69e020e04d21268fa118b6ee1b1a046cfbee85622bf1659dacf",
              "available_at": "2024-12-30T00:00:00Z"
            }
          }
        ],
        "classes": [
          {
            "id": "class1",
            "version": 1,
            "target_question_id": "q1",
            "definition": "Original finite synthetic historical switch events",
            "eligibility_rule": "All distinct synthetic switch events in the declared historical window",
            "frozen_at": "2024-12-30T00:00:00Z",
            "availability_cutoff": "2024-12-29T00:00:00Z",
            "comparability": "Synthetic demonstration only;no population representativeness claimed.",
            "members": [
              {
                "id": "m0",
                "event_id": "historical-0",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 1,
                "event_at": "2024-12-01T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-0",
                  "locator": "original:member-0",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-0",
                  "snapshot_sha256": "b2c56227f8f73938d69b8476d05b6b3db549b170d49e1ec2529994a990cd45d8",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m1",
                "event_id": "historical-1",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 1,
                "event_at": "2024-12-02T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-1",
                  "locator": "original:member-1",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-1",
                  "snapshot_sha256": "80a4c7004b3e2d93e9aa55f08b6428c23aefcac01f76ebefbb798af6d4c87443",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m2",
                "event_id": "historical-2",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 1,
                "event_at": "2024-12-03T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-2",
                  "locator": "original:member-2",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-2",
                  "snapshot_sha256": "019f9724fabd99e5cffc8e64da53e9be85e9d6984ddbebcfcf637cca5d88680b",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m3",
                "event_id": "historical-3",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-04T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-3",
                  "locator": "original:member-3",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-3",
                  "snapshot_sha256": "1bbccc0692938b7c36f4e745a8cfbc084dff169af1bf68d8e9a9abc49dd86a1d",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m4",
                "event_id": "historical-4",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-05T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-4",
                  "locator": "original:member-4",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-4",
                  "snapshot_sha256": "6a3969d2f67626987e4933118d5ec0702baa408e8c00f5bbe8d0e53c34fcf81c",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m5",
                "event_id": "historical-5",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-06T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-5",
                  "locator": "original:member-5",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-5",
                  "snapshot_sha256": "7a132046ab2dece3d5a6e074bf672b503e41a5e6fa4a46ccc6492342a982e802",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m6",
                "event_id": "historical-6",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-07T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-6",
                  "locator": "original:member-6",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-6",
                  "snapshot_sha256": "4fb9f6db24a04ca5191e98c461f07a2010598ff8d11fef41b929289a691ba1c7",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m7",
                "event_id": "historical-7",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-08T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-7",
                  "locator": "original:member-7",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-7",
                  "snapshot_sha256": "b3891163980c3aaf9d38be9e161f503b1871a57c1af0199ecf683ea97bcf565e",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m8",
                "event_id": "historical-8",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-09T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-8",
                  "locator": "original:member-8",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-8",
                  "snapshot_sha256": "f60c7a635c556c921a35312e862a7178464561ab6a4136cffc795cdd8690b07f",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m9",
                "event_id": "historical-9",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-10T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-9",
                  "locator": "original:member-9",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-9",
                  "snapshot_sha256": "119152113fcdb397d68fb82c202cc4100cecc72e9c2f4b8cb973e293d548e8b5",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              }
            ],
            "source": {
              "id": "class-source",
              "locator": "original:class-source",
              "rights": "self_authored",
              "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
              "snapshot": "Original synthetic software validation evidence: class-source",
              "snapshot_sha256": "cba781691cf75ace7849c564f835eec03241068d1c0e83ffe164e9331d17aa72",
              "available_at": "2024-12-29T00:00:00Z"
            }
          }
        ],
        "slots": [
          {
            "forecast_id": "f1",
            "question_id": "q1",
            "participant": "person1",
            "participant_kind": "individual"
          }
        ],
        "provenance": {
          "id": "study-source",
          "locator": "original:study-source",
          "rights": "self_authored",
          "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
          "snapshot": "Original synthetic software validation evidence: study-source",
          "snapshot_sha256": "852af0c234dfa57c63067f12e4adb05ef1d3716e1dd8584ec9808d2e88225918",
          "available_at": "2024-12-30T00:00:00Z"
        }
      },
      "plan_sha256": "058e3b1fec80a53c2544a5e23f534b434b596d3eaead07312cc5bb9606c58702",
      "actions": [
        {
          "sequence": 1,
          "kind": "forecast",
          "at": "2025-01-01T12:00:00Z",
          "record": {
            "forecast_id": "f1",
            "question_id": "q1",
            "question_version": 1,
            "question_sha256": "1ab81cda71d093a51ea4218a1f08ae3922446cc760e6fb0b0002dc4a8bcbad70",
            "participant": "person1",
            "version": 1,
            "parent_sha256": null,
            "recorded_at": "2025-01-01T12:00:00Z",
            "knowledge_at": "2025-01-01T12:00:00Z",
            "probability": "1/5",
            "mode": "manual",
            "reason": "Original synthetic judgment",
            "evidence": [],
            "assumptions": [
              "Submitted probability is a synthetic judgment,not measured expertise"
            ],
            "outcome_known": false,
            "bayes": null
          },
          "parent_sha256": "058e3b1fec80a53c2544a5e23f534b434b596d3eaead07312cc5bb9606c58702",
          "decision": "accepted",
          "reason": null,
          "sha256": "9e555222f9827b8370da3322d1dcc954e91661d4739f45f4b2be20533b70bfd2"
        },
        {
          "sequence": 2,
          "kind": "update",
          "at": "2025-01-02T00:00:00Z",
          "record": {
            "forecast_id": "f1",
            "question_id": "q1",
            "question_version": 1,
            "question_sha256": "1ab81cda71d093a51ea4218a1f08ae3922446cc760e6fb0b0002dc4a8bcbad70",
            "participant": "person1",
            "version": 2,
            "parent_sha256": "f8729aecf950dc62cc2a28cbd5dcda9fcad9080fddc64ceda54f951ca5c510c5",
            "recorded_at": "2025-01-02T00:00:00Z",
            "knowledge_at": "2025-01-02T00:00:00Z",
            "probability": "1/5",
            "mode": "bayes",
            "reason": "Explicit synthetic likelihood-ratio update",
            "evidence": [
              {
                "id": "evidence1",
                "dependency_group": "evidence-group1",
                "original_fact_id": "fact1",
                "statement": "An original synthetic observation,not geopolitical evidence",
                "source": {
                  "id": "source-evidence1",
                  "locator": "original:source-evidence1",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: source-evidence1",
                  "snapshot_sha256": "a3d7718607436ee4118c6d4108253dee5288e57a4b73bfaee47c2db7470d2726",
                  "available_at": "2025-01-02T00:00:00Z"
                }
              }
            ],
            "assumptions": [
              "Submitted probability is a synthetic judgment,not measured expertise"
            ],
            "outcome_known": false,
            "bayes": {
              "kind": "ratio",
              "ratio": "1",
              "likelihood_h": null,
              "likelihood_not_h": null,
              "dependence": "first",
              "conditioned_on": [],
              "independent_given_h": false,
              "independent_given_not_h": false,
              "model_status": "user_assumed",
              "measurement_notes": "Assumed illustrative likelihood model;not measured evidence",
              "source": {
                "id": "likelihood-evidence1",
                "locator": "original:likelihood-evidence1",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: likelihood-evidence1",
                "snapshot_sha256": "52ad6f9f37c4c6ee357d02e0c7e3e0e39e793c137fa6a1f7c631c487a8430a19",
                "available_at": "2025-01-02T00:00:00Z"
              }
            }
          },
          "parent_sha256": "9e555222f9827b8370da3322d1dcc954e91661d4739f45f4b2be20533b70bfd2",
          "decision": "accepted",
          "reason": null,
          "sha256": "b243baa109350b5b64c2117dee2b7ac459b8cac234899c48d1823a645d960fe6"
        }
      ]
    },
    "evaluation": {
      "aggregation_policy": "Equal forecast-slot weight on latest eligible fixed-cutoff resolved TEST questions;training separately summarized;not daily orquestion-standardized tournament replication",
      "evidence_mode": "synthetic_software_validation",
      "empirical_skill_validated": false,
      "questions": [
        {
          "question_id": "q1",
          "event_id": "event1",
          "partition": "test",
          "status": "unresolved",
          "outcome": null,
          "resolution_history": []
        }
      ],
      "reference_classes": [
        {
          "input": {
            "id": "class1",
            "version": 1,
            "target_question_id": "q1",
            "definition": "Original finite synthetic historical switch events",
            "eligibility_rule": "All distinct synthetic switch events in the declared historical window",
            "frozen_at": "2024-12-30T00:00:00Z",
            "availability_cutoff": "2024-12-29T00:00:00Z",
            "comparability": "Synthetic demonstration only;no population representativeness claimed.",
            "members": [
              {
                "id": "m0",
                "event_id": "historical-0",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 1,
                "event_at": "2024-12-01T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-0",
                  "locator": "original:member-0",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-0",
                  "snapshot_sha256": "b2c56227f8f73938d69b8476d05b6b3db549b170d49e1ec2529994a990cd45d8",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m1",
                "event_id": "historical-1",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 1,
                "event_at": "2024-12-02T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-1",
                  "locator": "original:member-1",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-1",
                  "snapshot_sha256": "80a4c7004b3e2d93e9aa55f08b6428c23aefcac01f76ebefbb798af6d4c87443",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m2",
                "event_id": "historical-2",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 1,
                "event_at": "2024-12-03T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-2",
                  "locator": "original:member-2",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-2",
                  "snapshot_sha256": "019f9724fabd99e5cffc8e64da53e9be85e9d6984ddbebcfcf637cca5d88680b",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m3",
                "event_id": "historical-3",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-04T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-3",
                  "locator": "original:member-3",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-3",
                  "snapshot_sha256": "1bbccc0692938b7c36f4e745a8cfbc084dff169af1bf68d8e9a9abc49dd86a1d",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m4",
                "event_id": "historical-4",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-05T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-4",
                  "locator": "original:member-4",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-4",
                  "snapshot_sha256": "6a3969d2f67626987e4933118d5ec0702baa408e8c00f5bbe8d0e53c34fcf81c",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m5",
                "event_id": "historical-5",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-06T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-5",
                  "locator": "original:member-5",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-5",
                  "snapshot_sha256": "7a132046ab2dece3d5a6e074bf672b503e41a5e6fa4a46ccc6492342a982e802",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m6",
                "event_id": "historical-6",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-07T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-6",
                  "locator": "original:member-6",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-6",
                  "snapshot_sha256": "4fb9f6db24a04ca5191e98c461f07a2010598ff8d11fef41b929289a691ba1c7",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m7",
                "event_id": "historical-7",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-08T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-7",
                  "locator": "original:member-7",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-7",
                  "snapshot_sha256": "b3891163980c3aaf9d38be9e161f503b1871a57c1af0199ecf683ea97bcf565e",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m8",
                "event_id": "historical-8",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-09T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-8",
                  "locator": "original:member-8",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-8",
                  "snapshot_sha256": "f60c7a635c556c921a35312e862a7178464561ab6a4136cffc795cdd8690b07f",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              },
              {
                "id": "m9",
                "event_id": "historical-9",
                "dependency_group": "history",
                "eligibility": "included",
                "reason": "Eligible under the frozen synthetic rule",
                "status": "resolved",
                "outcome": 0,
                "event_at": "2024-12-10T00:00:00Z",
                "observed_at": "2024-12-20T00:00:00Z",
                "source": {
                  "id": "member-9",
                  "locator": "original:member-9",
                  "rights": "self_authored",
                  "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                  "snapshot": "Original synthetic software validation evidence: member-9",
                  "snapshot_sha256": "119152113fcdb397d68fb82c202cc4100cecc72e9c2f4b8cb973e293d548e8b5",
                  "available_at": "2024-12-20T00:00:00Z"
                }
              }
            ],
            "source": {
              "id": "class-source",
              "locator": "original:class-source",
              "rights": "self_authored",
              "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
              "snapshot": "Original synthetic software validation evidence: class-source",
              "snapshot_sha256": "cba781691cf75ace7849c564f835eec03241068d1c0e83ffe164e9331d17aa72",
              "available_at": "2024-12-29T00:00:00Z"
            }
          },
          "sha256": "beaeee6344c02525dcbb5e6933069bb89a454a85c24893e0ffbb701a6158bae7",
          "members": [
            {
              "id": "m0",
              "event_id": "historical-0",
              "dependency_group": "history",
              "eligibility": "included",
              "reason": "Eligible under the frozen synthetic rule",
              "status": "resolved",
              "outcome": 1,
              "event_at": "2024-12-01T00:00:00Z",
              "observed_at": "2024-12-20T00:00:00Z",
              "source": {
                "id": "member-0",
                "locator": "original:member-0",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: member-0",
                "snapshot_sha256": "b2c56227f8f73938d69b8476d05b6b3db549b170d49e1ec2529994a990cd45d8",
                "available_at": "2024-12-20T00:00:00Z"
              }
            },
            {
              "id": "m1",
              "event_id": "historical-1",
              "dependency_group": "history",
              "eligibility": "included",
              "reason": "Eligible under the frozen synthetic rule",
              "status": "resolved",
              "outcome": 1,
              "event_at": "2024-12-02T00:00:00Z",
              "observed_at": "2024-12-20T00:00:00Z",
              "source": {
                "id": "member-1",
                "locator": "original:member-1",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: member-1",
                "snapshot_sha256": "80a4c7004b3e2d93e9aa55f08b6428c23aefcac01f76ebefbb798af6d4c87443",
                "available_at": "2024-12-20T00:00:00Z"
              }
            },
            {
              "id": "m2",
              "event_id": "historical-2",
              "dependency_group": "history",
              "eligibility": "included",
              "reason": "Eligible under the frozen synthetic rule",
              "status": "resolved",
              "outcome": 1,
              "event_at": "2024-12-03T00:00:00Z",
              "observed_at": "2024-12-20T00:00:00Z",
              "source": {
                "id": "member-2",
                "locator": "original:member-2",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: member-2",
                "snapshot_sha256": "019f9724fabd99e5cffc8e64da53e9be85e9d6984ddbebcfcf637cca5d88680b",
                "available_at": "2024-12-20T00:00:00Z"
              }
            },
            {
              "id": "m3",
              "event_id": "historical-3",
              "dependency_group": "history",
              "eligibility": "included",
              "reason": "Eligible under the frozen synthetic rule",
              "status": "resolved",
              "outcome": 0,
              "event_at": "2024-12-04T00:00:00Z",
              "observed_at": "2024-12-20T00:00:00Z",
              "source": {
                "id": "member-3",
                "locator": "original:member-3",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: member-3",
                "snapshot_sha256": "1bbccc0692938b7c36f4e745a8cfbc084dff169af1bf68d8e9a9abc49dd86a1d",
                "available_at": "2024-12-20T00:00:00Z"
              }
            },
            {
              "id": "m4",
              "event_id": "historical-4",
              "dependency_group": "history",
              "eligibility": "included",
              "reason": "Eligible under the frozen synthetic rule",
              "status": "resolved",
              "outcome": 0,
              "event_at": "2024-12-05T00:00:00Z",
              "observed_at": "2024-12-20T00:00:00Z",
              "source": {
                "id": "member-4",
                "locator": "original:member-4",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: member-4",
                "snapshot_sha256": "6a3969d2f67626987e4933118d5ec0702baa408e8c00f5bbe8d0e53c34fcf81c",
                "available_at": "2024-12-20T00:00:00Z"
              }
            },
            {
              "id": "m5",
              "event_id": "historical-5",
              "dependency_group": "history",
              "eligibility": "included",
              "reason": "Eligible under the frozen synthetic rule",
              "status": "resolved",
              "outcome": 0,
              "event_at": "2024-12-06T00:00:00Z",
              "observed_at": "2024-12-20T00:00:00Z",
              "source": {
                "id": "member-5",
                "locator": "original:member-5",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: member-5",
                "snapshot_sha256": "7a132046ab2dece3d5a6e074bf672b503e41a5e6fa4a46ccc6492342a982e802",
                "available_at": "2024-12-20T00:00:00Z"
              }
            },
            {
              "id": "m6",
              "event_id": "historical-6",
              "dependency_group": "history",
              "eligibility": "included",
              "reason": "Eligible under the frozen synthetic rule",
              "status": "resolved",
              "outcome": 0,
              "event_at": "2024-12-07T00:00:00Z",
              "observed_at": "2024-12-20T00:00:00Z",
              "source": {
                "id": "member-6",
                "locator": "original:member-6",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: member-6",
                "snapshot_sha256": "4fb9f6db24a04ca5191e98c461f07a2010598ff8d11fef41b929289a691ba1c7",
                "available_at": "2024-12-20T00:00:00Z"
              }
            },
            {
              "id": "m7",
              "event_id": "historical-7",
              "dependency_group": "history",
              "eligibility": "included",
              "reason": "Eligible under the frozen synthetic rule",
              "status": "resolved",
              "outcome": 0,
              "event_at": "2024-12-08T00:00:00Z",
              "observed_at": "2024-12-20T00:00:00Z",
              "source": {
                "id": "member-7",
                "locator": "original:member-7",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: member-7",
                "snapshot_sha256": "b3891163980c3aaf9d38be9e161f503b1871a57c1af0199ecf683ea97bcf565e",
                "available_at": "2024-12-20T00:00:00Z"
              }
            },
            {
              "id": "m8",
              "event_id": "historical-8",
              "dependency_group": "history",
              "eligibility": "included",
              "reason": "Eligible under the frozen synthetic rule",
              "status": "resolved",
              "outcome": 0,
              "event_at": "2024-12-09T00:00:00Z",
              "observed_at": "2024-12-20T00:00:00Z",
              "source": {
                "id": "member-8",
                "locator": "original:member-8",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: member-8",
                "snapshot_sha256": "f60c7a635c556c921a35312e862a7178464561ab6a4136cffc795cdd8690b07f",
                "available_at": "2024-12-20T00:00:00Z"
              }
            },
            {
              "id": "m9",
              "event_id": "historical-9",
              "dependency_group": "history",
              "eligibility": "included",
              "reason": "Eligible under the frozen synthetic rule",
              "status": "resolved",
              "outcome": 0,
              "event_at": "2024-12-10T00:00:00Z",
              "observed_at": "2024-12-20T00:00:00Z",
              "source": {
                "id": "member-9",
                "locator": "original:member-9",
                "rights": "self_authored",
                "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                "snapshot": "Original synthetic software validation evidence: member-9",
                "snapshot_sha256": "119152113fcdb397d68fb82c202cc4100cecc72e9c2f4b8cb973e293d548e8b5",
                "available_at": "2024-12-20T00:00:00Z"
              }
            }
          ],
          "included_resolved_ids": [
            "m0",
            "m1",
            "m2",
            "m3",
            "m4",
            "m5",
            "m6",
            "m7",
            "m8",
            "m9"
          ],
          "numerator": 3,
          "denominator": 10,
          "base_rate": {
            "status": "finite",
            "exact": "3/10",
            "decimal": "0.300000000000",
            "reason": null
          },
          "counts": {
            "universe": 10,
            "eligibility": {
              "included": 10,
              "excluded": 0,
              "ambiguous": 0
            },
            "statuses": {
              "resolved": 10,
              "unresolved": 0,
              "disputed": 0,
              "void": 0
            },
            "unique_events": 10,
            "dependency_groups": 1
          },
          "limits": [
            "Observed frequency is not a guarantee of future probability or population certainty.",
            "Membership,availability andcomparability are declarations;nominal n isnot an independent effective sample size."
          ]
        }
      ],
      "rows": [
        {
          "forecast_id": "f1",
          "question_id": "q1",
          "event_id": "event1",
          "dependency_group": "test1",
          "partition": "test",
          "participant": "person1",
          "participant_kind": "individual",
          "question_sha256": "1ab81cda71d093a51ea4218a1f08ae3922446cc760e6fb0b0002dc4a8bcbad70",
          "cutoff": "2025-01-03T00:00:00Z",
          "lead_seconds": 604800,
          "versions": [
            {
              "record": {
                "forecast_id": "f1",
                "question_id": "q1",
                "question_version": 1,
                "question_sha256": "1ab81cda71d093a51ea4218a1f08ae3922446cc760e6fb0b0002dc4a8bcbad70",
                "participant": "person1",
                "version": 1,
                "parent_sha256": null,
                "recorded_at": "2025-01-01T12:00:00Z",
                "knowledge_at": "2025-01-01T12:00:00Z",
                "probability": "1/5",
                "mode": "manual",
                "reason": "Original synthetic judgment",
                "evidence": [],
                "assumptions": [
                  "Submitted probability is a synthetic judgment,not measured expertise"
                ],
                "outcome_known": false,
                "bayes": null
              },
              "sha256": "f8729aecf950dc62cc2a28cbd5dcda9fcad9080fddc64ceda54f951ca5c510c5",
              "action_sequence": 1,
              "calculation": null,
              "exclusion_reasons": []
            },
            {
              "record": {
                "forecast_id": "f1",
                "question_id": "q1",
                "question_version": 1,
                "question_sha256": "1ab81cda71d093a51ea4218a1f08ae3922446cc760e6fb0b0002dc4a8bcbad70",
                "participant": "person1",
                "version": 2,
                "parent_sha256": "f8729aecf950dc62cc2a28cbd5dcda9fcad9080fddc64ceda54f951ca5c510c5",
                "recorded_at": "2025-01-02T00:00:00Z",
                "knowledge_at": "2025-01-02T00:00:00Z",
                "probability": "1/5",
                "mode": "bayes",
                "reason": "Explicit synthetic likelihood-ratio update",
                "evidence": [
                  {
                    "id": "evidence1",
                    "dependency_group": "evidence-group1",
                    "original_fact_id": "fact1",
                    "statement": "An original synthetic observation,not geopolitical evidence",
                    "source": {
                      "id": "source-evidence1",
                      "locator": "original:source-evidence1",
                      "rights": "self_authored",
                      "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                      "snapshot": "Original synthetic software validation evidence: source-evidence1",
                      "snapshot_sha256": "a3d7718607436ee4118c6d4108253dee5288e57a4b73bfaee47c2db7470d2726",
                      "available_at": "2025-01-02T00:00:00Z"
                    }
                  }
                ],
                "assumptions": [
                  "Submitted probability is a synthetic judgment,not measured expertise"
                ],
                "outcome_known": false,
                "bayes": {
                  "kind": "ratio",
                  "ratio": "1",
                  "likelihood_h": null,
                  "likelihood_not_h": null,
                  "dependence": "first",
                  "conditioned_on": [],
                  "independent_given_h": false,
                  "independent_given_not_h": false,
                  "model_status": "user_assumed",
                  "measurement_notes": "Assumed illustrative likelihood model;not measured evidence",
                  "source": {
                    "id": "likelihood-evidence1",
                    "locator": "original:likelihood-evidence1",
                    "rights": "self_authored",
                    "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
                    "snapshot": "Original synthetic software validation evidence: likelihood-evidence1",
                    "snapshot_sha256": "52ad6f9f37c4c6ee357d02e0c7e3e0e39e793c137fa6a1f7c631c487a8430a19",
                    "available_at": "2025-01-02T00:00:00Z"
                  }
                }
              },
              "sha256": "df60b4aa94e57b0d3c17ff106d1ad3bb782daaa689ac215d588a33326aeb46d3",
              "action_sequence": 2,
              "calculation": {
                "prior_sha256": "f8729aecf950dc62cc2a28cbd5dcda9fcad9080fddc64ceda54f951ca5c510c5",
                "prior": {
                  "status": "finite",
                  "exact": "1/5",
                  "decimal": "0.200000000000",
                  "reason": null
                },
                "likelihood_ratio": {
                  "status": "finite",
                  "exact": "1",
                  "decimal": "1.000000000000",
                  "reason": null
                },
                "posterior": {
                  "status": "finite",
                  "exact": "1/5",
                  "decimal": "0.200000000000",
                  "reason": null
                },
                "evidence_id": "evidence1",
                "dependence": "first",
                "conditioned_on": [],
                "model_status": "user_assumed",
                "empirically_validated": false
              },
              "exclusion_reasons": []
            }
          ],
          "selected_version_sha256": "df60b4aa94e57b0d3c17ff106d1ad3bb782daaa689ac215d588a33326aeb46d3",
          "selected_version": 2,
          "probability": {
            "status": "finite",
            "exact": "1/5",
            "decimal": "0.200000000000",
            "reason": null
          },
          "status": "unresolved",
          "outcome": null,
          "scored": false,
          "primary_included": false,
          "exclusion_reasons": [
            "unresolved"
          ],
          "binary_brier": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "not_eligible_resolved_pair"
          },
          "two_category_sum_of_squares": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "not_eligible_resolved_pair"
          },
          "natural_log_loss": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "not_eligible_resolved_pair"
          },
          "baseline_probability": "1/2",
          "baseline": {
            "kind": "constant",
            "probability": "1/2",
            "frozen_at": "2024-12-31T00:00:00Z",
            "domain": "synthetic-switches",
            "horizon": "fixed-window",
            "source": {
              "id": "baseline-source",
              "locator": "original:baseline-source",
              "rights": "self_authored",
              "attribution": "Original synthetic fixture;no actual participant or geopolitical skill.",
              "snapshot": "Original synthetic software validation evidence: baseline-source",
              "snapshot_sha256": "ee865768d0e9b7ee132821254268aabfb5d991fbfd408ed585e6f2d4b252fc43",
              "available_at": "2024-12-30T00:00:00Z"
            }
          },
          "reference_training": {
            "class_id": "class1",
            "class_sha256": "beaeee6344c02525dcbb5e6933069bb89a454a85c24893e0ffbb701a6158bae7",
            "availability_cutoff": "2024-12-29T00:00:00Z",
            "frozen_at": "2024-12-30T00:00:00Z",
            "member_event_start": "2024-12-01T00:00:00Z",
            "member_observed_end": "2024-12-20T00:00:00Z"
          }
        }
      ],
      "primary": {
        "denominator": 0,
        "unique_questions": 0,
        "unique_events": 0,
        "dependency_groups": 0,
        "participants": 0,
        "binary_brier": {
          "status": "not_estimable",
          "exact": null,
          "decimal": null,
          "reason": "empty_denominator"
        },
        "two_category_sum_of_squares": {
          "status": "not_estimable",
          "exact": null,
          "decimal": null,
          "reason": "empty_denominator"
        },
        "natural_log_loss": {
          "status": "not_estimable",
          "exact": null,
          "decimal": null,
          "reason": "empty_denominator"
        },
        "infinite_log_losses": 0,
        "calibration": [
          {
            "index": 0,
            "lower": "0",
            "upper": "1/10",
            "upper_inclusive": false,
            "count": 0,
            "positive_count": 0,
            "mean_probability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "observed_frequency": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "unique_events": 0,
            "dependency_groups": 0
          },
          {
            "index": 1,
            "lower": "1/10",
            "upper": "1/5",
            "upper_inclusive": false,
            "count": 0,
            "positive_count": 0,
            "mean_probability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "observed_frequency": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "unique_events": 0,
            "dependency_groups": 0
          },
          {
            "index": 2,
            "lower": "1/5",
            "upper": "3/10",
            "upper_inclusive": false,
            "count": 0,
            "positive_count": 0,
            "mean_probability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "observed_frequency": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "unique_events": 0,
            "dependency_groups": 0
          },
          {
            "index": 3,
            "lower": "3/10",
            "upper": "2/5",
            "upper_inclusive": false,
            "count": 0,
            "positive_count": 0,
            "mean_probability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "observed_frequency": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "unique_events": 0,
            "dependency_groups": 0
          },
          {
            "index": 4,
            "lower": "2/5",
            "upper": "1/2",
            "upper_inclusive": false,
            "count": 0,
            "positive_count": 0,
            "mean_probability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "observed_frequency": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "unique_events": 0,
            "dependency_groups": 0
          },
          {
            "index": 5,
            "lower": "1/2",
            "upper": "3/5",
            "upper_inclusive": false,
            "count": 0,
            "positive_count": 0,
            "mean_probability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "observed_frequency": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "unique_events": 0,
            "dependency_groups": 0
          },
          {
            "index": 6,
            "lower": "3/5",
            "upper": "7/10",
            "upper_inclusive": false,
            "count": 0,
            "positive_count": 0,
            "mean_probability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "observed_frequency": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "unique_events": 0,
            "dependency_groups": 0
          },
          {
            "index": 7,
            "lower": "7/10",
            "upper": "4/5",
            "upper_inclusive": false,
            "count": 0,
            "positive_count": 0,
            "mean_probability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "observed_frequency": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "unique_events": 0,
            "dependency_groups": 0
          },
          {
            "index": 8,
            "lower": "4/5",
            "upper": "9/10",
            "upper_inclusive": false,
            "count": 0,
            "positive_count": 0,
            "mean_probability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "observed_frequency": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "unique_events": 0,
            "dependency_groups": 0
          },
          {
            "index": 9,
            "lower": "9/10",
            "upper": "1",
            "upper_inclusive": true,
            "count": 0,
            "positive_count": 0,
            "mean_probability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "observed_frequency": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "unique_events": 0,
            "dependency_groups": 0
          }
        ],
        "decomposition": {
          "grouping": "Exact identical probabilities;separate from coarse calibration bins",
          "groups": [],
          "reliability": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "resolution": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "uncertainty": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "identity_passed": null
        },
        "baseline": {
          "denominator": 0,
          "paired_slot_ids": [],
          "excluded_pairs": [
            {
              "forecast_id": "f1",
              "reasons": [
                "unresolved"
              ]
            }
          ],
          "forecast_brier_on_paired": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "baseline_brier": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "absolute_improvement": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "relative_skill": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          }
        },
        "event_average": {
          "mean": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "groups": 0,
          "members": []
        },
        "participant_average": {
          "mean": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "groups": 0,
          "members": []
        },
        "team_aggregation": null
      },
      "by_partition": {
        "train": {
          "denominator": 0,
          "unique_questions": 0,
          "unique_events": 0,
          "dependency_groups": 0,
          "participants": 0,
          "binary_brier": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "two_category_sum_of_squares": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "natural_log_loss": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "infinite_log_losses": 0,
          "calibration": [
            {
              "index": 0,
              "lower": "0",
              "upper": "1/10",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 1,
              "lower": "1/10",
              "upper": "1/5",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 2,
              "lower": "1/5",
              "upper": "3/10",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 3,
              "lower": "3/10",
              "upper": "2/5",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 4,
              "lower": "2/5",
              "upper": "1/2",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 5,
              "lower": "1/2",
              "upper": "3/5",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 6,
              "lower": "3/5",
              "upper": "7/10",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 7,
              "lower": "7/10",
              "upper": "4/5",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 8,
              "lower": "4/5",
              "upper": "9/10",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 9,
              "lower": "9/10",
              "upper": "1",
              "upper_inclusive": true,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            }
          ],
          "decomposition": {
            "grouping": "Exact identical probabilities;separate from coarse calibration bins",
            "groups": [],
            "reliability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "resolution": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "uncertainty": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "identity_passed": null
          },
          "baseline": {
            "denominator": 0,
            "paired_slot_ids": [],
            "excluded_pairs": [],
            "forecast_brier_on_paired": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "baseline_brier": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "absolute_improvement": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "relative_skill": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            }
          },
          "event_average": {
            "mean": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "groups": 0,
            "members": []
          },
          "participant_average": {
            "mean": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "groups": 0,
            "members": []
          },
          "team_aggregation": null
        },
        "test": {
          "denominator": 0,
          "unique_questions": 0,
          "unique_events": 0,
          "dependency_groups": 0,
          "participants": 0,
          "binary_brier": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "two_category_sum_of_squares": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "natural_log_loss": {
            "status": "not_estimable",
            "exact": null,
            "decimal": null,
            "reason": "empty_denominator"
          },
          "infinite_log_losses": 0,
          "calibration": [
            {
              "index": 0,
              "lower": "0",
              "upper": "1/10",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 1,
              "lower": "1/10",
              "upper": "1/5",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 2,
              "lower": "1/5",
              "upper": "3/10",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 3,
              "lower": "3/10",
              "upper": "2/5",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 4,
              "lower": "2/5",
              "upper": "1/2",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 5,
              "lower": "1/2",
              "upper": "3/5",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 6,
              "lower": "3/5",
              "upper": "7/10",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 7,
              "lower": "7/10",
              "upper": "4/5",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 8,
              "lower": "4/5",
              "upper": "9/10",
              "upper_inclusive": false,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            },
            {
              "index": 9,
              "lower": "9/10",
              "upper": "1",
              "upper_inclusive": true,
              "count": 0,
              "positive_count": 0,
              "mean_probability": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "observed_frequency": {
                "status": "not_estimable",
                "exact": null,
                "decimal": null,
                "reason": "empty_denominator"
              },
              "unique_events": 0,
              "dependency_groups": 0
            }
          ],
          "decomposition": {
            "grouping": "Exact identical probabilities;separate from coarse calibration bins",
            "groups": [],
            "reliability": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "resolution": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "uncertainty": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "identity_passed": null
          },
          "baseline": {
            "denominator": 0,
            "paired_slot_ids": [],
            "excluded_pairs": [
              {
                "forecast_id": "f1",
                "reasons": [
                  "unresolved"
                ]
              }
            ],
            "forecast_brier_on_paired": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "baseline_brier": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "absolute_improvement": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "relative_skill": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            }
          },
          "event_average": {
            "mean": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "groups": 0,
            "members": []
          },
          "participant_average": {
            "mean": {
              "status": "not_estimable",
              "exact": null,
              "decimal": null,
              "reason": "empty_denominator"
            },
            "groups": 0,
            "members": []
          },
          "team_aggregation": null
        }
      },
      "denominators": {
        "planned_questions": 1,
        "planned_events": 1,
        "planned_slots": 1,
        "participants": 1,
        "versions": 2,
        "actions": 2,
        "rejected_attempts": 0,
        "selected_slots": 1,
        "primary_scored_slots": 0,
        "primary_unique_events": 0,
        "primary_dependency_groups": 0,
        "question_statuses": {
          "resolved": 0,
          "unresolved": 1,
          "disputed": 0,
          "void": 0
        },
        "primary_excluded_slot_ids": [
          "f1"
        ]
      },
      "rejected_attempts": [],
      "limits": [
        "Selection/availability,identity,rights,comparability andconditional independence aredeclared,not externallyattested.",
        "Multiple participants/updates share events;counts are not effective independent sample sizes.",
        "Calibration andscores are descriptive;synthetic validation establishes software mechanics,not human superforecasting skill.",
        "Local owners can rewrite all hashes/history;prospective integrity requires independent anchoring."
      ]
    }
  },
  "code_sha256": "6d5d5609717fd9ed309383fe0ea9a4935e7392397eef8dbcc33e5bc206fa9e67",
  "limits": [
    "Arithmetic andledger correctness are not demonstrated human expertise,geopolitical skill orhistorical tournament replication.",
    "Book later chapters andGJP file-level rights/completeness remain unverified;no corpus acquired.",
    "Source facts andworkflow context areseparate fromeditorial schema,cutoff,binning andreport conventions."
  ],
  "report_sha256": "5bd4a13b132003ca515904434cc97f7141db2e523d2f1a76b9ebbf5ae436cea6"
}
```

