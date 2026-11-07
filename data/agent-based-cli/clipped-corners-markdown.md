# Agent-Based Simulation — finite-grid B3/S23

```json
{
  "status": "accepted",
  "technique_id": 54,
  "schema_version": 1,
  "profile": {
    "id": "agent-based-finite-grid-b3s23-v1",
    "version": 1,
    "sha256": "e6d0487cf23393a1262efb227ef912542f38ae6cb9232358a6bbc34c9053a62b",
    "catalog_sha256": "d95cbfa701819bf23b3df2647c8ee6454963a397654588672818e8daec2ee02f"
  },
  "schema_sha256": "66224741762dd682c34fbdfd788c67e13e598887aecb29c1d993d66a1738a496",
  "request": {
    "schema_version": 1,
    "profile": {
      "id": "agent-based-finite-grid-b3s23-v1",
      "version": 1,
      "sha256": "e6d0487cf23393a1262efb227ef912542f38ae6cb9232358a6bbc34c9053a62b",
      "catalog_sha256": "d95cbfa701819bf23b3df2647c8ee6454963a397654588672818e8daec2ee02f"
    },
    "model": {
      "rule": "B3/S23",
      "boundary": "finite-zero-exterior",
      "scheduler": "synchronous",
      "neighborhood": "moore-radius-1-exclude-center"
    },
    "geometry": {
      "height": 3,
      "width": 3
    },
    "ticks": 2,
    "trace_states": true,
    "scenarios": [
      {
        "id": "base",
        "initial_grid": [
          [
            1,
            0,
            1
          ],
          [
            0,
            0,
            0
          ],
          [
            1,
            0,
            0
          ]
        ]
      }
    ],
    "reference_scenario": "base",
    "provenance": {
      "synthetic": true,
      "source_ref": "agent-based-mesa-life-agents-v1",
      "rights": "self_authored",
      "attribution": "Future original synthetic Life fixture",
      "snapshot": "Original explicit synthetic binary board; no observed people or assets.",
      "snapshot_sha256": "a4e825ca4014988b83d9f049adbbdb364a382ab0fa12da872c8bdd5c962c9a7e"
    }
  },
  "input_sha256": "b2af2293c42497215bb4f19b7134215fc723ab240f6a766ed42aa8570ebd29af",
  "model_sha256": "3a4d3144b073ac2bad8d7aeb67fe7e2d3d20206b8012a01bea6dcadcb321757a",
  "geometry_sha256": "33070e5d39514fd81bab1b274201ddfabe2a866c83a7c5d7ee77f37a6011e851",
  "rule_sha256": "8aa106cf9e3488cc2a1cdf56fa42ab0ca01bd0d19b94b329dcc6d1c9b03273c6",
  "source_manifest_sha256": "d95cbfa701819bf23b3df2647c8ee6454963a397654588672818e8daec2ee02f",
  "source_freeze_sha256": "7f253ec16471ce6a5a4a35193cb06fa065077a598a1aed293d61a63e82c1232b",
  "snapshot_sha256": "a4e825ca4014988b83d9f049adbbdb364a382ab0fa12da872c8bdd5c962c9a7e",
  "code_sha256": "cd6d2b3efba558253ab77212b67fd2e80c1d632d8c48e8fd358b38b7b80c896c",
  "state_hash_convention": "SHA256 ofraw row-majorbinarybytes0/1;dimensions boundbymodel/geometry hashes",
  "budget": {
    "cell_ticks": 18,
    "neighbor_cell_work": 162,
    "returned_state_cells": 45,
    "returned_count_cells": 62
  },
  "scenarios": [
    {
      "id": "base",
      "initial_grid": [
        [
          1,
          0,
          1
        ],
        [
          0,
          0,
          0
        ],
        [
          1,
          0,
          0
        ]
      ],
      "final_grid": [
        [
          0,
          0,
          0
        ],
        [
          0,
          0,
          0
        ],
        [
          0,
          0,
          0
        ]
      ],
      "initial_state_sha256": "21eb87b39d85357c5d57628631d72daa4b6a01c8cc82a0e651ef700ab67921e5",
      "final_state_sha256": "3e7077fd2f66d689e0cee6a7cf5b37bf2dca7c979af356d0a31cbc5c85605c7d",
      "scenario_sha256": "329086f0930276d882580bafdf20ebcf8129b9b119cde07bd4bed88b02e728fa",
      "model_sha256": "3a4d3144b073ac2bad8d7aeb67fe7e2d3d20206b8012a01bea6dcadcb321757a",
      "initial_alive": 3,
      "initial_dead": 6,
      "final_alive": 0,
      "final_dead": 9,
      "counts": [
        {
          "tick": 0,
          "alive": 3,
          "dead": 6,
          "births": null,
          "deaths": null,
          "state_sha256": "21eb87b39d85357c5d57628631d72daa4b6a01c8cc82a0e651ef700ab67921e5"
        },
        {
          "tick": 1,
          "alive": 1,
          "dead": 8,
          "births": 1,
          "deaths": 3,
          "state_sha256": "cdb032de4c6cb506da0606e0934e69ad1ae64773ffaa76f9d6e28192067c43cf"
        },
        {
          "tick": 2,
          "alive": 0,
          "dead": 9,
          "births": 0,
          "deaths": 1,
          "state_sha256": "3e7077fd2f66d689e0cee6a7cf5b37bf2dca7c979af356d0a31cbc5c85605c7d"
        }
      ],
      "state_trace": [
        [
          [
            1,
            0,
            1
          ],
          [
            0,
            0,
            0
          ],
          [
            1,
            0,
            0
          ]
        ],
        [
          [
            0,
            0,
            0
          ],
          [
            0,
            1,
            0
          ],
          [
            0,
            0,
            0
          ]
        ],
        [
          [
            0,
            0,
            0
          ],
          [
            0,
            0,
            0
          ],
          [
            0,
            0,
            0
          ]
        ]
      ],
      "classification": "unclassified",
      "fixed_point": false,
      "periodic_cycle": false,
      "cycle_start": null,
      "period": null,
      "first_repeat_tick": null,
      "requested_ticks": 2,
      "executed_ticks": 2,
      "early_stopped": false,
      "truncated": true
    }
  ],
  "comparisons": [
    {
      "scenario": "base",
      "reference": "base",
      "identical_initial_state": true,
      "per_tick": [
        {
          "tick": 0,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 1,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 2,
          "alive_difference": 0,
          "hamming_distance": 0
        }
      ],
      "final_alive_difference": 0,
      "final_hamming_distance": 0,
      "final_states_equal": true,
      "interpretation": "Conditional synthetic initial-state sensitivity;notreal-world causal effects"
    }
  ],
  "sources": [
    {
      "id": "agent-based-epstein-v1",
      "technique_id": 54,
      "rank": 1,
      "author": "Joshua M. Epstein",
      "edition": "Generative Social Science;2006 copyright;Chapter1 educational witness,44PDF pages",
      "url": "https://ocw.tudelft.nl/wp-content/uploads/GenerativeScienceEpstein_01.pdf",
      "locator": "Original inventory URL null;resolved primary chapter witness. Chapter1 printedpp4–8 generative sufficiency;pp38–39 explanation/prediction;copyright cover",
      "ingestion": "facts_only",
      "rights_note": "Copyright Princeton University Press. Reading/browsing access is not permission to redistribute chapters,figures,CD-ROM models or downloaded teaching code. Original facts/notes only;no body orcode bundled.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "agent-based-railsback-grimm-v1",
      "technique_id": 54,
      "rank": 2,
      "author": "Steven F. Railsback and Volker Grimm",
      "edition": "Agent-Based and Individual-Based Modeling:A Practical Introduction,Second Edition;authors confirm2019release",
      "url": "https://www.railsback-grimm-abm-book.com/",
      "locator": "Authors site;objectives,second-edition distinction anddownloads",
      "ingestion": "facts_only",
      "rights_note": "Copyright Princeton University Press. Reading/browsing access is not permission to redistribute chapters,figures,CD-ROM models or downloaded teaching code. Original facts/notes only;no body orcode bundled.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "agent-based-park-v1",
      "technique_id": 54,
      "rank": 3,
      "author": "Joon Sung Park et al.",
      "edition": "Generative Agents:Interactive Simulacra of Human Behavior;UIST2023;DOI10.1145/3586183.3606763",
      "url": "https://research.google/pubs/generative-agents-interactive-simulacra-of-human-behavior/",
      "locator": "Original ranked Google Research publication page",
      "ingestion": "facts_only",
      "rights_note": "Paper/code/assets have separate rights;facts only,no paper,figures,prompts orassets redistributed.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "agent-based-mesa-v1",
      "technique_id": 54,
      "rank": 4,
      "author": "Mesa maintainers",
      "edition": "Original stable documentation lead;mutable,notanimmutable release certification",
      "url": "https://mesa.readthedocs.io/stable/",
      "locator": "Framework overview andexamples;current pinned source revision assessed separately",
      "ingestion": "facts_only",
      "rights_note": "Apache2 framework;review LICENSE/NOTICE andfile-specific rights beforeanyreuse. No Mesa installed,vendored orrequired byrecommendation.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "agent-based-railsback-chapter-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Steven F. Railsback and Volker Grimm",
      "edition": "Second Edition;publisher-authorized Chapter1 sample,11PDF pages",
      "url": "https://assets.press.princeton.edu/chapters/s14270.pdf",
      "locator": "Chapter1 Models,Agent-Based Models,andtheModeling Cycle;purpose-driven design andempirical testing context",
      "ingestion": "facts_only",
      "rights_note": "Copyright Princeton University Press. Reading/browsing access is not permission to redistribute chapters,figures,CD-ROM models or downloaded teaching code. Original facts/notes only;no body orcode bundled.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "agent-based-railsback-preface-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Steven F. Railsback and Volker Grimm",
      "edition": "Second Edition;publisher-authorized preface,6PDF pages",
      "url": "https://assets.press.princeton.edu/releases/p14270.pdf",
      "locator": "Prefacexi–xiv;ODD,software testing,analysis andNetLogo6.0.4 edition context",
      "ingestion": "facts_only",
      "rights_note": "Copyright Princeton University Press. Reading/browsing access is not permission to redistribute chapters,figures,CD-ROM models or downloaded teaching code. Original facts/notes only;no body orcode bundled.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "agent-based-park-arxiv-v2",
      "technique_id": 54,
      "rank": null,
      "author": "Joon Sung Park et al.",
      "edition": "arXiv2304.03442v2;2023-08-06;v1 submitted2023-04-07",
      "url": "https://arxiv.org/html/2304.03442v2",
      "locator": "Sections4.1–4.3 architecture;Sections6–8 believability evaluation andlimits",
      "ingestion": "facts_only",
      "rights_note": "arXiv perpetual non-exclusive distribution license is not CC-BY orblanket downstream redistribution permission. No text/figures bundled.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "agent-based-park-paper-license-v1",
      "technique_id": 54,
      "rank": null,
      "author": "arXiv",
      "edition": "Non-exclusive distribution license",
      "url": "https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html",
      "locator": "License linked by2304.03442v2",
      "ingestion": "facts_only",
      "rights_note": "Policy facts only;do notsubstitute repository Apache2 license forpaper rights.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "agent-based-park-code-license-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Joon Sung Park",
      "edition": "Generative Agents repository atfe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4",
      "url": "https://github.com/joonspk-research/generative_agents/blob/fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4/LICENSE",
      "locator": "Apache2 license andcopyright2023 Joon Sung Park;README has separateartist acknowledgements",
      "ingestion": "facts_only",
      "rights_note": "Apache2 source license withnotice/modification obligations;no asset-specific rights certification andnocode/assets copied.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null,
      "git_commit": "fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4",
      "git_blob_sha1": "e0d8210e8009de93c35050c71db7af0d88c37660"
    },
    {
      "id": "agent-based-mesa-life-agents-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Mesa maintainers",
      "edition": "Mesa4.0.0a0 source atfe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "url": "https://github.com/mesa/mesa/blob/fe24c24ee34762de2ff85d487af14bfb5cd1dbb2/mesa/examples/basic/conways_game_of_life/agents.py",
      "locator": "determine_state andassume_state;binary B3/S23 rule",
      "ingestion": "facts_only",
      "rights_note": "Apache2 source;LICENSE/NOTICE obligations apply tocopying. Mathematical facts andoriginal notes only;no sourcecode bundled.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null,
      "git_commit": "fe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "git_blob_sha1": "7b12248e0dbfd9bb77ecd31ad17dd7f24b31a5de"
    },
    {
      "id": "agent-based-mesa-life-model-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Mesa maintainers",
      "edition": "Mesa4.0.0a0 source atfe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "url": "https://github.com/mesa/mesa/blob/fe24c24ee34762de2ff85d487af14bfb5cd1dbb2/mesa/examples/basic/conways_game_of_life/model.py",
      "locator": "Toroidal OrthogonalMooreGrid;random initialization;two-stage synchronous commit",
      "ingestion": "facts_only",
      "rights_note": "Apache2 source;LICENSE/NOTICE obligations apply tocopying. Mathematical facts andoriginal notes only;no sourcecode bundled.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null,
      "git_commit": "fe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "git_blob_sha1": "5bb93f7c3af3bedd6fc019bc9c4f2c03f7cda133"
    },
    {
      "id": "agent-based-mesa-schelling-agents-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Mesa maintainers",
      "edition": "Mesa4.0.0a0 source atfe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "url": "https://github.com/mesa/mesa/blob/fe24c24ee34762de2ff85d487af14bfb5cd1dbb2/mesa/examples/basic/schelling/agents.py",
      "locator": "assign_state computes occupied-neighbor fraction;zero-neighbor fraction0;strict < unhappiness;random-empty move",
      "ingestion": "facts_only",
      "rights_note": "Apache2 source;LICENSE/NOTICE obligations apply tocopying. Mathematical facts andoriginal notes only;no sourcecode bundled.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null,
      "git_commit": "fe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "git_blob_sha1": "6b347d7f4b3ad7c621922c4b8e5ad18de81a1608"
    },
    {
      "id": "agent-based-mesa-schelling-model-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Mesa maintainers",
      "edition": "Mesa4.0.0a0 source atfe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "url": "https://github.com/mesa/mesa/blob/fe24c24ee34762de2ff85d487af14bfb5cd1dbb2/mesa/examples/basic/schelling/model.py",
      "locator": "Scenario default homophily0.4;precomputed happiness,shuffled moves,thenrecompute;experimental scenario API",
      "ingestion": "facts_only",
      "rights_note": "Apache2 source;LICENSE/NOTICE obligations apply tocopying. Mathematical facts andoriginal notes only;no sourcecode bundled.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null,
      "git_commit": "fe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "git_blob_sha1": "b3f54c173686202d5478bc8652b128a243655597"
    },
    {
      "id": "agent-based-mesa-sugar-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Mesa maintainers",
      "edition": "Mutable stable-doc example;notbook/release-equivalence certification",
      "url": "https://mesa.readthedocs.io/stable/examples/advanced/sugarscape_g1mt.html",
      "locator": "G1Mt growback/vision/welfare/trade;model.step growsresources,shuffles move/eat/death,thenoptionaltrading",
      "ingestion": "facts_only",
      "rights_note": "FrameworkApache2 isnotblanketbook/landscape data rights. No sugar-map,book figure orcode copied.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "agent-based-mesa-virus-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Mesa maintainers",
      "edition": "Mutable stable-doc example;notclinical validation",
      "url": "https://mesa.readthedocs.io/stable/examples/basic/virus_on_network.html",
      "locator": "VirusAgent infection/recovery/resistance andshuffle_do schedule",
      "ingestion": "facts_only",
      "rights_note": "Framework/source rights do notcertify medical applicability,graph data rights orcalibration;facts only.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null
    },
    {
      "id": "agent-based-mesa-license-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Mesa maintainers",
      "edition": "Apache2 LICENSE atfe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "url": "https://github.com/mesa/mesa/blob/fe24c24ee34762de2ff85d487af14bfb5cd1dbb2/LICENSE",
      "locator": "Full license inspected",
      "ingestion": "facts_only",
      "rights_note": "No source vendored. Futurecopying mustpreserve requiredlicense andnotices.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null,
      "git_commit": "fe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "git_blob_sha1": "d645695673349e3947e8e5ae42332d0ac3164cd7"
    },
    {
      "id": "agent-based-mesa-notice-v1",
      "technique_id": 54,
      "rank": null,
      "author": "Mesa maintainers",
      "edition": "NOTICE atfe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "url": "https://github.com/mesa/mesa/blob/fe24c24ee34762de2ff85d487af14bfb5cd1dbb2/NOTICE",
      "locator": "CoreMesaTeam/contributors copyright2014–2024 notice inspected",
      "ingestion": "facts_only",
      "rights_note": "Notice remainsseparate fromproject license;no frameworkbundle introduced.",
      "checked_on": "2026-11-07",
      "snapshot_sha256": null,
      "snapshot_bytes": null,
      "git_commit": "fe24c24ee34762de2ff85d487af14bfb5cd1dbb2",
      "git_blob_sha1": "abeac775e0c94ec6596166b1f32aaa4ccb332809"
    }
  ],
  "scope": {
    "execution": "Verified bounded exact B3/S23 withfinite-zero-exterior synchronous updates",
    "scenarios": "Synthetic initial-state sensitivity andmodel patterns",
    "empirical_calibration": "unsupported",
    "real_world_social_forecasting": "unsupported",
    "epidemiological_prediction": "unsupported",
    "LLM_behavior_simulation": "unsupported",
    "Schelling": "unsupported",
    "Sugarscape": "unsupported",
    "time": "Ticks aremodel updates,notreal-world time units",
    "source_comparison": "Editorial finite-boundary/explicit-input variant;notexactreproduction ofpinnedMesa toroidal/random-initial model",
    "rights": "Source/snapshot declarations andhashes arenotindependent truth orrights certification"
  },
  "limits": [
    "Schelling relocation",
    "Sugarscape",
    "Epidemiological/social forecasting",
    "LLM generative agents",
    "Stochastic initialization/scheduling",
    "Toroidal boundaries",
    "Other CA rules",
    "Empirical calibration",
    "Causalpolicy effects",
    "Arbitrarynodepermutation invariance"
  ],
  "report_sha256": "2dc56e524ad014b7868cef50e7c9d29cb47cd09e63e8de76856ddb3e41c79b3f"
}
```

