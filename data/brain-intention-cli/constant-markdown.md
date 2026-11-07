# Brain-Based Intention Prediction — synthetic offline reference

```json
{
  "status": "accepted",
  "technique_id": 55,
  "schema_version": 1,
  "profile": {
    "id": "brain-intention-synthetic-offline-classification-v1",
    "version": 1,
    "sha256": "30f541e00247d4c9f78fa5218cba83e5e5caf7417868743cf4e3b4cebfa629a0",
    "catalog_sha256": "3fdd4d5fd4490cc162e2f6a4aa1926a418522be894e6a6f43daae2287fd30ab1"
  },
  "request": {
    "schema_version": 1,
    "profile": {
      "id": "brain-intention-synthetic-offline-classification-v1",
      "version": 1,
      "sha256": "30f541e00247d4c9f78fa5218cba83e5e5caf7417868743cf4e3b4cebfa629a0",
      "catalog_sha256": "3fdd4d5fd4490cc162e2f6a4aa1926a418522be894e6a6f43daae2287fd30ab1"
    },
    "mode": "windows",
    "channels": [
      {
        "id": "c0",
        "unit": "arbitrary_units"
      }
    ],
    "task": "editorial_binary",
    "protocol": "subject_disjoint",
    "fit_at": 100,
    "filter": "none",
    "trials": [
      {
        "id": "t0",
        "subject": "train",
        "run": "r1",
        "session": null,
        "source_id": "file-train",
        "trial_id": "trial0",
        "start": 0,
        "end": 4,
        "available_at": 50,
        "predict_at": 90,
        "label_available_at": 80,
        "partition": "TRAIN",
        "label": "A",
        "annotation": null,
        "values": [
          [
            -1,
            1,
            -1,
            1
          ]
        ]
      },
      {
        "id": "t1",
        "subject": "train",
        "run": "r1",
        "session": null,
        "source_id": "file-train",
        "trial_id": "trial1",
        "start": 5,
        "end": 9,
        "available_at": 50,
        "predict_at": 90,
        "label_available_at": 80,
        "partition": "TRAIN",
        "label": "A",
        "annotation": null,
        "values": [
          [
            -1,
            1,
            -1,
            1
          ]
        ]
      },
      {
        "id": "t2",
        "subject": "train",
        "run": "r1",
        "session": null,
        "source_id": "file-train",
        "trial_id": "trial2",
        "start": 10,
        "end": 14,
        "available_at": 50,
        "predict_at": 90,
        "label_available_at": 80,
        "partition": "TRAIN",
        "label": "B",
        "annotation": null,
        "values": [
          [
            -2,
            2,
            -2,
            2
          ]
        ]
      },
      {
        "id": "t3",
        "subject": "train",
        "run": "r1",
        "session": null,
        "source_id": "file-train",
        "trial_id": "trial3",
        "start": 15,
        "end": 19,
        "available_at": 50,
        "predict_at": 90,
        "label_available_at": 80,
        "partition": "TRAIN",
        "label": "B",
        "annotation": null,
        "values": [
          [
            -2,
            2,
            -2,
            2
          ]
        ]
      },
      {
        "id": "t4",
        "subject": "test",
        "run": "r1",
        "session": null,
        "source_id": "file-test",
        "trial_id": "trial4",
        "start": 20,
        "end": 24,
        "available_at": 110,
        "predict_at": 120,
        "label_available_at": 130,
        "partition": "TEST",
        "label": "A",
        "annotation": null,
        "values": [
          [
            3,
            3,
            3,
            3
          ]
        ]
      },
      {
        "id": "t5",
        "subject": "test",
        "run": "r1",
        "session": null,
        "source_id": "file-test",
        "trial_id": "trial5",
        "start": 25,
        "end": 29,
        "available_at": 110,
        "predict_at": 120,
        "label_available_at": 130,
        "partition": "TEST",
        "label": "A",
        "annotation": null,
        "values": [
          [
            -1,
            1,
            -1,
            1
          ]
        ]
      },
      {
        "id": "t6",
        "subject": "test",
        "run": "r1",
        "session": null,
        "source_id": "file-test",
        "trial_id": "trial6",
        "start": 30,
        "end": 34,
        "available_at": 110,
        "predict_at": 120,
        "label_available_at": 130,
        "partition": "TEST",
        "label": "B",
        "annotation": null,
        "values": [
          [
            -2,
            2,
            -2,
            2
          ]
        ]
      },
      {
        "id": "t7",
        "subject": "test",
        "run": "r1",
        "session": null,
        "source_id": "file-test",
        "trial_id": "trial7",
        "start": 35,
        "end": 39,
        "available_at": 110,
        "predict_at": 120,
        "label_available_at": 130,
        "partition": "TEST",
        "label": "B",
        "annotation": null,
        "values": [
          [
            -2,
            2,
            -2,
            2
          ]
        ]
      }
    ],
    "provenance": {
      "synthetic": true,
      "source_ref": "brain-intention-centroid-v1",
      "rights": "self_authored",
      "attribution": "Future original synthetic arithmetic example",
      "snapshot": "Original synthetic trial table; no human data.",
      "snapshot_sha256": "7811d5503fd38d958f3f83d61d104e0a4e6480534c7fc65a65cb579521df8b69"
    }
  },
  "input_sha256": "09e4d6aaf06fec7d74afa0216471e12b63c41d63a65d0822b4075c3ae26e004f",
  "schema_sha256": "3bdc8e7845f616006a7dd13bb9ba762bba0f2d512f28d07bd3ee493987a443cc",
  "source_manifest_sha256": "3fdd4d5fd4490cc162e2f6a4aa1926a418522be894e6a6f43daae2287fd30ab1",
  "source_freeze_sha256": "93ea4163ac65b1525b21474c882df807d80599426f5fce1606666c91bce35847",
  "code_sha256": "c2c0ab880202fbaa9cb3140cdabf7962eb2d2a30e222a8dd527b52d0651f0384",
  "model": {
    "algorithm": "unscaled-uniform-nearest-arithmetic-centroid",
    "tie": "A",
    "channels": [
      {
        "id": "c0",
        "unit": "arbitrary_units"
      }
    ],
    "task": "editorial_binary",
    "centroids": {
      "A": [
        "0",
        "1"
      ],
      "B": [
        "0",
        "4"
      ]
    },
    "training": [
      {
        "id": "t0",
        "label": "A",
        "features": [
          "0",
          "1"
        ]
      },
      {
        "id": "t1",
        "label": "A",
        "features": [
          "0",
          "1"
        ]
      },
      {
        "id": "t2",
        "label": "B",
        "features": [
          "0",
          "4"
        ]
      },
      {
        "id": "t3",
        "label": "B",
        "features": [
          "0",
          "4"
        ]
      }
    ]
  },
  "model_sha256": "458710c95ab7c14e69d1371e3e401005c0a0521251aef12ffad7969a0f3b6a8d",
  "split_sha256": "1a1c976adf4efc651c6b0937af3530d9c29c47b1344fa6b67d433f14afb97f36",
  "features": {
    "t0": [
      "0",
      "1"
    ],
    "t1": [
      "0",
      "1"
    ],
    "t2": [
      "0",
      "4"
    ],
    "t3": [
      "0",
      "4"
    ],
    "t4": [
      "3",
      "0"
    ],
    "t5": [
      "0",
      "1"
    ],
    "t6": [
      "0",
      "4"
    ],
    "t7": [
      "0",
      "4"
    ]
  },
  "centroids": {
    "A": [
      "0",
      "1"
    ],
    "B": [
      "0",
      "4"
    ]
  },
  "predictions": [
    {
      "id": "t4",
      "prediction": "A",
      "distances": {
        "A": "10",
        "B": "25"
      }
    },
    {
      "id": "t5",
      "prediction": "A",
      "distances": {
        "A": "0",
        "B": "9"
      }
    },
    {
      "id": "t6",
      "prediction": "B",
      "distances": {
        "A": "9",
        "B": "0"
      }
    },
    {
      "id": "t7",
      "prediction": "B",
      "distances": {
        "A": "9",
        "B": "0"
      }
    }
  ],
  "evaluation": {
    "confusion": [
      [
        2,
        0
      ],
      [
        0,
        2
      ]
    ],
    "count": 4,
    "accuracy": "1",
    "recall": {
      "A": "1",
      "B": "1"
    },
    "balanced_accuracy": "1",
    "status": "estimable"
  },
  "baseline": {
    "prediction": "A",
    "evaluation": {
      "confusion": [
        [
          2,
          0
        ],
        [
          2,
          0
        ]
      ],
      "count": 4,
      "accuracy": "1/2",
      "recall": {
        "A": "1",
        "B": "0"
      },
      "balanced_accuracy": "1/2",
      "status": "estimable"
    }
  },
  "test_ids": [
    "t4",
    "t5",
    "t6",
    "t7"
  ],
  "validation_ids": [],
  "diagnostics": {
    "protocol": "subject_disjoint",
    "subject_partition_check": "passed",
    "trial_source_interval_check": "passed",
    "availability_check": "passed",
    "test_labels_used_for": "Scoring only; never fitting,selection or prediction",
    "session_claim": "unsupported",
    "numeric_duplicate_features": "Allowed; source identity and interval checks govern leakage"
  },
  "iid_arithmetic_toy": {
    "upper_tail_8_of_10": "7/128",
    "scope": "Ideal iid fair binary arithmetic only; not EEG significance"
  },
  "budget": {
    "raw_cells": 32,
    "features": 2,
    "work": 384,
    "returned_cells": 288
  },
  "sources": [
    {
      "id": "brain-intention-wolpaw-v1",
      "technique_id": 55,
      "rank": 1,
      "author": "Jonathan Wolpaw and Elizabeth Winter Wolpaw (eds.)",
      "edition": "Brain–Computer Interfaces: Principles and Practice; 23 January 2012; DOI 10.1093/acprof:oso/9780195388855.001.0001",
      "url": "https://academic.oup.com/book/1700",
      "locator": "Official metadata and 25-chapter TOC only; full algorithms not inspected.",
      "ingestion": "facts_only",
      "rights_note": "OUP copyright; metadata and original notes only; no book body redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-soon-v1",
      "technique_id": 55,
      "rank": 2,
      "author": "Chun Siong Soon, Marcel Brass, Hans-Jochen Heinze, John-Dylan Haynes",
      "edition": "Unconscious Determinants of Free Decisions in the Human Brain; Nature Neuroscience 11,543–545; online 13 April 2008; DOI 10.1038/nn.2112",
      "url": "https://www.nature.com/articles/nn.2112",
      "locator": "Publisher indexed abstract and publication metadata; full text and supplement blocked by publisher cookie/identity gateway.",
      "ingestion": "facts_only",
      "rights_note": "Publisher copyright; no body/figures redistributed; exact numerical protocol remains unverified.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-eegmmidb-v1",
      "technique_id": 55,
      "rank": 3,
      "author": "Gerwin Schalk / PhysioNet / BCI2000 team",
      "edition": "EEG Motor Movement/Imagery Dataset 1.0.0; 9 September 2009; DOI 10.13026/C28G6P",
      "url": "https://www.physionet.org/content/eegmmidb/1.0.0/",
      "locator": "64 channels,160 Hz,EDF+ annotations,14 runs; documentation inspected, no EDF downloaded.",
      "ingestion": "facts_only",
      "rights_note": "ODC-By 1.0 database license; attribution required; individual contents, consent, privacy and personality rights need separate review.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-operating-protocols-v1",
      "technique_id": 55,
      "rank": null,
      "author": "Wolpaw book chapter authors / OUP",
      "edition": "Chapter 10, Operating Protocols; pp189–196; 2012",
      "url": "https://academic.oup.com/book/1700/chapter-abstract/141290465",
      "locator": "Abstract only: synchronous/self-paced operation, control and error handling.",
      "ingestion": "facts_only",
      "rights_note": "OUP copyright; abstract-derived facts only.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-reliability-v1",
      "technique_id": 55,
      "rank": null,
      "author": "Wolpaw book chapter authors / OUP",
      "edition": "Chapter 25, reliability and dissemination; pp387–392; 2012",
      "url": "https://academic.oup.com/book/1700/chapter-abstract/141298120",
      "locator": "Abstract only: reliability, hardware and clinical validation gaps.",
      "ingestion": "facts_only",
      "rights_note": "OUP copyright; abstract-derived facts only.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-dataset-license-v1",
      "technique_id": 55,
      "rank": null,
      "author": "Open Data Commons / PhysioNet",
      "edition": "Open Data Commons Attribution License 1.0",
      "url": "https://www.physionet.org/content/eegmmidb/view-license/1.0.0/",
      "locator": "Section4 attribution; section2.4 excludes individual contents and privacy/personality rights.",
      "ingestion": "facts_only",
      "rights_note": "Database license is not blanket consent or a software license; no dataset redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-run-map-v1",
      "technique_id": 55,
      "rank": null,
      "author": "MNE contributors",
      "edition": "MNE 1.13.2 documentation; eegbci.load_data",
      "url": "https://mne.tools/stable/generated/mne.datasets.eegbci.load_data.html",
      "locator": "Run table 1–14 and subject IDs1–109. Mutable documentation, not installed/executed.",
      "ingestion": "facts_only",
      "rights_note": "Facts only; MNE software BSD-3-Clause; no copied code.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-csp-example-v1",
      "technique_id": 55,
      "rank": null,
      "author": "MNE contributors",
      "edition": "MNE 1.13.2 Motor imagery decoding from EEG data using CSP",
      "url": "https://mne.tools/stable/auto_examples/decoding/decoding_csp_eeg.html",
      "locator": "Subject1,runs6/10/14; 7–30Hz noncausal FIR; training crop1–2s; CSP4+LDA Pipeline; ShuffleSplit10,test.2,seed103.",
      "ingestion": "facts_only",
      "rights_note": "Example BSD-3-Clause; original facts only, no code/data copied or example executed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-libet-v1",
      "technique_id": 55,
      "rank": null,
      "author": "Benjamin Libet, Curtis A. Gleason, Elwood W. Wright, Dennis K. Pearl",
      "edition": "Time of conscious intention to act in relation to onset of cerebral activity (readiness-potential); Brain106,623–642;1983; DOI10.1093/brain/106.3.623",
      "url": "https://training.incf.org/sites/default/files/2023-05/Libet%20-%20Time%20of%20Conscious%20Intention%20to%20Act.pdf",
      "locator": "Primary article teaching witness; movement-locked readiness potential and reported awareness timing.",
      "ingestion": "facts_only",
      "rights_note": "OUP copyright; teaching access is not redistribution permission; no body/figures bundled.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-schurger-v1",
      "technique_id": 55,
      "rank": null,
      "author": "Aaron Schurger, Jacobo D. Sitt, Stanislas Dehaene",
      "edition": "An accumulator model for spontaneous neural activity prior to self-initiated movement;PNAS109,E2904–E2913;2012;DOI10.1073/pnas.1210467109",
      "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3479453/",
      "locator": "Primary abstract/methods: stochastic accumulator, threshold crossing and time-locked averaging can generate RP.",
      "ingestion": "facts_only",
      "rights_note": "Facts and original notes only; no article/figures or model code redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-centroid-v1",
      "technique_id": 55,
      "rank": null,
      "author": "scikit-learn developers",
      "edition": "NearestCentroid official documentation;1.9.1 observed",
      "url": "https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestCentroid.html",
      "locator": "Euclidean arithmetic-mean centroids; editorial exact toy below is not version-equivalent package replication.",
      "ingestion": "facts_only",
      "rights_note": "Facts only; no library code copied or dependency installed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-leakage-v1",
      "technique_id": 55,
      "rank": null,
      "author": "scikit-learn developers",
      "edition": "Common pitfalls: data leakage",
      "url": "https://scikit-learn.org/stable/common_pitfalls.html#data-leakage",
      "locator": "Split before preprocessing; fit only on training subset; use pipelines.",
      "ingestion": "facts_only",
      "rights_note": "Facts only; no code copied.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-groups-v1",
      "technique_id": 55,
      "rank": null,
      "author": "scikit-learn developers",
      "edition": "GroupKFold official documentation",
      "url": "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html",
      "locator": "Non-overlapping groups between training and test folds; group identity must match scientific claim.",
      "ingestion": "facts_only",
      "rights_note": "Facts only; no code copied.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-balanced-accuracy-v1",
      "technique_id": 55,
      "rank": null,
      "author": "scikit-learn developers",
      "edition": "balanced_accuracy_score official documentation",
      "url": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html",
      "locator": "Balanced accuracy is average recall across classes; proposed fixed-class absent-class convention must be named.",
      "ingestion": "facts_only",
      "rights_note": "Facts only; no code copied.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "brain-intention-binomial-v1",
      "technique_id": 55,
      "rank": null,
      "author": "SciPy developers",
      "edition": "scipy.stats.binomtest official documentation",
      "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html",
      "locator": "Binomial test assumes declared success probability and binomial model; not automatic EEG significance.",
      "ingestion": "facts_only",
      "rights_note": "Facts only; no code copied.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    }
  ],
  "limitations": [
    "Real EEG ingestion",
    "CSP/LDA or signal preprocessing",
    "fMRI and readiness potential replication",
    "Cross-session generalization",
    "Clinical assessment",
    "Live BCI or unrestricted intention prediction",
    "Synthetic software correctness is not empirical neural decoding or unrestricted intention prediction.",
    "Identities, clocks and rights are declarations; hashes do not externally certify them.",
    "No calibration, p-value, clinical or cross-session certification."
  ],
  "report_sha256": "a490a588fd7751ee773043eec22269be408a8d6ab8901cfdc3d2b3fc4f5fe351"
}
```

