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
      "height": 4,
      "width": 4
    },
    "ticks": 256,
    "trace_states": false,
    "scenarios": [
      {
        "id": "base",
        "initial_grid": [
          [
            0,
            0,
            0,
            0
          ],
          [
            0,
            1,
            1,
            0
          ],
          [
            0,
            1,
            1,
            0
          ],
          [
            0,
            0,
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
  "input_sha256": "d6ed2aa2167d879bbd3a871e3390f1711515f58941124afacdc0366cc9e5c0bc",
  "model_sha256": "ac5f7e6412f1351450c13fdf7a974510780760743984f24a08dd01670f6c791d",
  "geometry_sha256": "82b983f77b119f370379673df97f43a16fcc45add6dd9775e6b3022eb17970de",
  "rule_sha256": "8aa106cf9e3488cc2a1cdf56fa42ab0ca01bd0d19b94b329dcc6d1c9b03273c6",
  "source_manifest_sha256": "d95cbfa701819bf23b3df2647c8ee6454963a397654588672818e8daec2ee02f",
  "source_freeze_sha256": "7f253ec16471ce6a5a4a35193cb06fa065077a598a1aed293d61a63e82c1232b",
  "snapshot_sha256": "a4e825ca4014988b83d9f049adbbdb364a382ab0fa12da872c8bdd5c962c9a7e",
  "code_sha256": "cd6d2b3efba558253ab77212b67fd2e80c1d632d8c48e8fd358b38b7b80c896c",
  "state_hash_convention": "SHA256 ofraw row-majorbinarybytes0/1;dimensions boundbymodel/geometry hashes",
  "budget": {
    "cell_ticks": 4096,
    "neighbor_cell_work": 36864,
    "returned_state_cells": 32,
    "returned_count_cells": 2602
  },
  "scenarios": [
    {
      "id": "base",
      "initial_grid": [
        [
          0,
          0,
          0,
          0
        ],
        [
          0,
          1,
          1,
          0
        ],
        [
          0,
          1,
          1,
          0
        ],
        [
          0,
          0,
          0,
          0
        ]
      ],
      "final_grid": [
        [
          0,
          0,
          0,
          0
        ],
        [
          0,
          1,
          1,
          0
        ],
        [
          0,
          1,
          1,
          0
        ],
        [
          0,
          0,
          0,
          0
        ]
      ],
      "initial_state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037",
      "final_state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037",
      "scenario_sha256": "9082e3f79e697c269ae557539835ebd6f5eafab6dd2bc7e023ac9d7b21543e73",
      "model_sha256": "ac5f7e6412f1351450c13fdf7a974510780760743984f24a08dd01670f6c791d",
      "initial_alive": 4,
      "initial_dead": 12,
      "final_alive": 4,
      "final_dead": 12,
      "counts": [
        {
          "tick": 0,
          "alive": 4,
          "dead": 12,
          "births": null,
          "deaths": null,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 1,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 2,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 3,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 4,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 5,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 6,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 7,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 8,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 9,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 10,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 11,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 12,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 13,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 14,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 15,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 16,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 17,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 18,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 19,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 20,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 21,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 22,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 23,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 24,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 25,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 26,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 27,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 28,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 29,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 30,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 31,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 32,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 33,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 34,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 35,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 36,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 37,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 38,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 39,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 40,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 41,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 42,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 43,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 44,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 45,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 46,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 47,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 48,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 49,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 50,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 51,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 52,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 53,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 54,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 55,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 56,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 57,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 58,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 59,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 60,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 61,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 62,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 63,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 64,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 65,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 66,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 67,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 68,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 69,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 70,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 71,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 72,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 73,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 74,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 75,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 76,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 77,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 78,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 79,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 80,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 81,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 82,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 83,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 84,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 85,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 86,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 87,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 88,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 89,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 90,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 91,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 92,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 93,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 94,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 95,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 96,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 97,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 98,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 99,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 100,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 101,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 102,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 103,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 104,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 105,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 106,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 107,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 108,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 109,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 110,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 111,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 112,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 113,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 114,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 115,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 116,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 117,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 118,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 119,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 120,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 121,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 122,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 123,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 124,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 125,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 126,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 127,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 128,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 129,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 130,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 131,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 132,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 133,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 134,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 135,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 136,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 137,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 138,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 139,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 140,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 141,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 142,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 143,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 144,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 145,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 146,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 147,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 148,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 149,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 150,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 151,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 152,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 153,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 154,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 155,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 156,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 157,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 158,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 159,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 160,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 161,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 162,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 163,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 164,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 165,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 166,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 167,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 168,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 169,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 170,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 171,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 172,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 173,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 174,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 175,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 176,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 177,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 178,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 179,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 180,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 181,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 182,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 183,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 184,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 185,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 186,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 187,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 188,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 189,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 190,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 191,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 192,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 193,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 194,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 195,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 196,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 197,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 198,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 199,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 200,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 201,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 202,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 203,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 204,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 205,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 206,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 207,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 208,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 209,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 210,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 211,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 212,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 213,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 214,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 215,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 216,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 217,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 218,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 219,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 220,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 221,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 222,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 223,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 224,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 225,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 226,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 227,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 228,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 229,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 230,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 231,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 232,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 233,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 234,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 235,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 236,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 237,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 238,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 239,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 240,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 241,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 242,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 243,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 244,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 245,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 246,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 247,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 248,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 249,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 250,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 251,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 252,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 253,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 254,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 255,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        },
        {
          "tick": 256,
          "alive": 4,
          "dead": 12,
          "births": 0,
          "deaths": 0,
          "state_sha256": "cfb45cf1b6d09f7909bf5c541a7a6382ad9b6741fdaf1767f1d4a040ff9d2037"
        }
      ],
      "state_trace": null,
      "classification": "fixed_point",
      "fixed_point": true,
      "periodic_cycle": false,
      "cycle_start": 0,
      "period": 1,
      "first_repeat_tick": 1,
      "requested_ticks": 256,
      "executed_ticks": 256,
      "early_stopped": false,
      "truncated": false
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
        },
        {
          "tick": 3,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 4,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 5,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 6,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 7,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 8,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 9,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 10,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 11,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 12,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 13,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 14,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 15,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 16,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 17,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 18,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 19,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 20,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 21,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 22,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 23,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 24,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 25,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 26,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 27,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 28,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 29,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 30,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 31,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 32,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 33,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 34,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 35,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 36,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 37,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 38,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 39,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 40,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 41,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 42,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 43,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 44,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 45,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 46,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 47,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 48,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 49,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 50,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 51,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 52,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 53,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 54,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 55,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 56,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 57,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 58,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 59,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 60,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 61,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 62,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 63,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 64,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 65,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 66,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 67,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 68,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 69,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 70,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 71,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 72,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 73,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 74,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 75,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 76,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 77,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 78,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 79,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 80,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 81,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 82,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 83,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 84,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 85,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 86,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 87,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 88,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 89,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 90,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 91,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 92,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 93,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 94,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 95,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 96,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 97,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 98,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 99,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 100,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 101,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 102,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 103,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 104,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 105,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 106,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 107,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 108,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 109,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 110,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 111,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 112,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 113,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 114,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 115,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 116,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 117,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 118,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 119,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 120,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 121,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 122,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 123,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 124,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 125,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 126,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 127,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 128,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 129,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 130,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 131,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 132,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 133,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 134,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 135,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 136,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 137,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 138,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 139,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 140,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 141,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 142,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 143,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 144,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 145,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 146,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 147,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 148,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 149,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 150,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 151,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 152,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 153,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 154,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 155,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 156,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 157,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 158,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 159,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 160,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 161,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 162,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 163,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 164,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 165,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 166,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 167,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 168,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 169,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 170,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 171,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 172,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 173,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 174,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 175,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 176,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 177,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 178,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 179,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 180,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 181,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 182,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 183,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 184,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 185,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 186,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 187,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 188,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 189,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 190,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 191,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 192,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 193,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 194,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 195,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 196,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 197,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 198,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 199,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 200,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 201,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 202,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 203,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 204,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 205,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 206,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 207,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 208,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 209,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 210,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 211,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 212,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 213,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 214,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 215,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 216,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 217,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 218,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 219,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 220,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 221,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 222,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 223,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 224,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 225,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 226,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 227,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 228,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 229,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 230,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 231,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 232,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 233,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 234,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 235,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 236,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 237,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 238,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 239,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 240,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 241,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 242,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 243,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 244,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 245,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 246,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 247,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 248,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 249,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 250,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 251,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 252,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 253,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 254,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 255,
          "alive_difference": 0,
          "hamming_distance": 0
        },
        {
          "tick": 256,
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
  "report_sha256": "ee8ce868c17d8ec85b2651c678507dbab313fa857fcfb38a0b4456c3d9758e6e"
}
```

