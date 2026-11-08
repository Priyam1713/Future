# Future Lab research report

**User-declared research or native procedural output — no empirical skill certification.**

```json
{
  "status": "accepted",
  "task": "run",
  "result": {
    "schema_version": 1,
    "technique_id": 4,
    "operation": "numerology",
    "adapter": "legacy_cli_inprocess",
    "registry_sha256": "2b2c0a4f372b8861b1471b50acc2313b6cc2882293273c2924a84aac3a0ccf2d",
    "core_sha256": "51d59bbd50adb57c75106cec83cf6141682dd3597dddad00c2347a4b82ee4880",
    "request_sha256": "f2c0ce9b3d39b17c3472dc7ca46df82a54b7052101339e0e2f4d45709d550d3f",
    "execution_status": "returned",
    "native_output": {
      "technique_id": 4,
      "profile": "decoz-component-reduction",
      "birth": "1990-07-15",
      "target": "2026-11-09",
      "name": {
        "original": "ALICE",
        "basis": "birth",
        "y_roles": "",
        "tokens": [
          {
            "part": "ALICE",
            "letters": [
              {
                "letter": "A",
                "value": 1,
                "vowel": true
              },
              {
                "letter": "L",
                "value": 3,
                "vowel": false
              },
              {
                "letter": "I",
                "value": 9,
                "vowel": true
              },
              {
                "letter": "C",
                "value": 3,
                "vowel": false
              },
              {
                "letter": "E",
                "value": 5,
                "vowel": true
              }
            ]
          }
        ]
      },
      "life_path": {
        "input": 14,
        "steps": [
          14,
          5
        ],
        "result": 5,
        "components": [
          {
            "input": 7,
            "steps": [
              7
            ],
            "result": 7
          },
          {
            "input": 15,
            "steps": [
              15,
              6
            ],
            "result": 6
          },
          {
            "input": 1990,
            "steps": [
              1990,
              19,
              10,
              1
            ],
            "result": 1
          }
        ]
      },
      "birthday": {
        "original_day": 15,
        "companion": {
          "input": 15,
          "steps": [
            15,
            6
          ],
          "result": 6
        }
      },
      "expression": {
        "input": 3,
        "steps": [
          3
        ],
        "result": 3,
        "components": [
          {
            "input": 21,
            "steps": [
              21,
              3
            ],
            "result": 3
          }
        ]
      },
      "soul_urge": {
        "input": 6,
        "steps": [
          6
        ],
        "result": 6,
        "components": [
          {
            "input": 15,
            "steps": [
              15,
              6
            ],
            "result": 6
          }
        ]
      },
      "personality": {
        "input": 6,
        "steps": [
          6
        ],
        "result": 6,
        "components": [
          {
            "input": 6,
            "steps": [
              6
            ],
            "result": 6
          }
        ]
      },
      "cycles": {
        "sun": {
          "input": 22,
          "steps": [
            22,
            4
          ],
          "result": 4
        },
        "year": {
          "input": 2030,
          "steps": [
            2030,
            5
          ],
          "result": 5
        },
        "month": {
          "input": 16,
          "steps": [
            16,
            7
          ],
          "result": 7
        },
        "day": {
          "input": 16,
          "steps": [
            16,
            7
          ],
          "result": 7
        },
        "year_interval": [
          "2026-01-01",
          "2027-01-01"
        ]
      },
      "sources": [
        {
          "id": "numerology-decoz-life-path-v1",
          "url": "https://www.worldnumerology.com/numerology-life-path/",
          "locator": "Calculation steps; October15,1998 example"
        },
        {
          "id": "numerology-decoz-expression-v1",
          "url": "https://www.worldnumerology.com/numerology-expression/",
          "locator": "Thomas Cruise Mapother example; name selection"
        },
        {
          "id": "numerology-decoz-guide-v1",
          "url": "https://www.worldnumerology.com/do-your-own-reading/",
          "locator": "Birthday, Heart's Desire, Personality and personal-cycle sections"
        },
        {
          "id": "numerology-decoz-daily-v1",
          "url": "https://www.worldnumerology.com/free-forecasts/daily-number-forecast/",
          "locator": "Steps1–4, September12/October12,2026 example"
        },
        {
          "id": "numerology-decoz-vowels-v1",
          "url": "https://www.worldnumerology.com/numerology-soul-urge/",
          "locator": "Vowel and pronunciation-dependent Y calculation"
        }
      ],
      "conventions": {
        "technique_id": 4,
        "profile": "decoz-component-reduction",
        "version": 1,
        "core": "Reduce date components/name parts separately, retaining11/22/33 at every core reduction stage. Keep original totals and digit-sum steps.",
        "birthday": "Retain actual day1–31 as Birthday number; show reduced/master companion separately, never replace original day.",
        "cycles": "Calendar Jan1 year transition; reduce cycles to1–9 without masters. Use sequential Sun/birth-month-day → year → month → day method from daily guide; compounds belong to that method, not aggregate formula.",
        "name_policy": "Explicit birth/current basis. ASCII A–Z case-insensitive only; ASCII space separates name parts. Hyphen/apostrophe join letters inside a part and are recorded as zero-value separators. This token policy is an explicit implementation convention, not claimed universal Decoz doctrine. Reject other characters/diacritics rather than transliterate. Every Y occurrence requires caller-specified vowel/consonant role, ordered left-to-right. No vowels/consonants in entire name yields unsupported null for that number.",
        "sources": [
          {
            "id": "numerology-decoz-life-path-v1",
            "url": "https://www.worldnumerology.com/numerology-life-path/",
            "locator": "Calculation steps; October15,1998 example"
          },
          {
            "id": "numerology-decoz-expression-v1",
            "url": "https://www.worldnumerology.com/numerology-expression/",
            "locator": "Thomas Cruise Mapother example; name selection"
          },
          {
            "id": "numerology-decoz-guide-v1",
            "url": "https://www.worldnumerology.com/do-your-own-reading/",
            "locator": "Birthday, Heart's Desire, Personality and personal-cycle sections"
          },
          {
            "id": "numerology-decoz-daily-v1",
            "url": "https://www.worldnumerology.com/free-forecasts/daily-number-forecast/",
            "locator": "Steps1–4, September12/October12,2026 example"
          },
          {
            "id": "numerology-decoz-vowels-v1",
            "url": "https://www.worldnumerology.com/numerology-soul-urge/",
            "locator": "Vowel and pronunciation-dependent Y calculation"
          }
        ],
        "unsupported": [
          "Chaldean",
          "Lo Shu",
          "gematria",
          "automatic pronunciation/transliteration",
          "birthday-based personal-year transition",
          "aggregate-method compound interpretations"
        ],
        "rights": "Factual procedures and short original summaries only; no copyrighted corpus ingested."
      },
      "limitations": [
        "Symbolic calculations, not validated personality diagnoses or event probabilities.",
        "Current-name results are overlays, not silently substituted birth-name numbers."
      ],
      "readings": [
        {
          "scope": "expression",
          "number": 3,
          "coverage": "direct",
          "text": "Creative communication.",
          "source_id": "numerology-decoz-expression-v1",
          "url": "https://www.worldnumerology.com/numerology-expression/",
          "locator": "The Meaning of Your Expression Numbers"
        },
        {
          "scope": "personal_year",
          "number": 5,
          "coverage": "direct",
          "text": "Change and flexibility.",
          "source_id": "numerology-decoz-year-symbols-v1",
          "url": "https://www.worldnumerology.com/personal-numerology-forecast/",
          "locator": "Meaning of Your Personal Year Cycles, numbered year sections; timeless themes only, not2026 event claims"
        },
        {
          "scope": "life_path",
          "coverage": "compositional",
          "text": "Birth-date framework; no direct number-specific delineation in this core.",
          "source_id": "numerology-decoz-guide-v1",
          "url": "https://www.worldnumerology.com/do-your-own-reading/",
          "locator": "Birthday, Heart's Desire, Personality and personal-cycle sections"
        },
        {
          "scope": "soul_urge",
          "coverage": "compositional",
          "text": "Vowel-based motivation context.",
          "source_id": "numerology-decoz-guide-v1",
          "url": "https://www.worldnumerology.com/do-your-own-reading/",
          "locator": "Birthday, Heart's Desire, Personality and personal-cycle sections"
        },
        {
          "scope": "personality",
          "coverage": "compositional",
          "text": "Consonant-based outward presentation context.",
          "source_id": "numerology-decoz-guide-v1",
          "url": "https://www.worldnumerology.com/do-your-own-reading/",
          "locator": "Birthday, Heart's Desire, Personality and personal-cycle sections"
        },
        {
          "scope": "birthday",
          "coverage": "compositional",
          "text": "Actual day retained alongside its reduced companion.",
          "source_id": "numerology-decoz-guide-v1",
          "url": "https://www.worldnumerology.com/do-your-own-reading/",
          "locator": "Birthday, Heart's Desire, Personality and personal-cycle sections"
        }
      ],
      "interpretation_limits": "Short original source summaries, symbolic themes only. No empirical personality/outcome validation. Core numbers other than Expression are not assigned Expression meanings; cycle Month/Day-specific delineations remain unsupported."
    },
    "native_output_sha256": "a609195f14053ab01365a06c9edeff0548387a293cf289d4e31f6e0c29001595",
    "native_error": null,
    "native_exit_code": 0,
    "native_stdout": "{\n  \"technique_id\": 4,\n  \"profile\": \"decoz-component-reduction\",\n  \"birth\": \"1990-07-15\",\n  \"target\": \"2026-11-09\",\n  \"name\": {\n    \"original\": \"ALICE\",\n    \"basis\": \"birth\",\n    \"y_roles\": \"\",\n    \"tokens\": [\n      {\n        \"part\": \"ALICE\",\n        \"letters\": [\n          {\n            \"letter\": \"A\",\n            \"value\": 1,\n            \"vowel\": true\n          },\n          {\n            \"letter\": \"L\",\n            \"value\": 3,\n            \"vowel\": false\n          },\n          {\n            \"letter\": \"I\",\n            \"value\": 9,\n            \"vowel\": true\n          },\n          {\n            \"letter\": \"C\",\n            \"value\": 3,\n            \"vowel\": false\n          },\n          {\n            \"letter\": \"E\",\n            \"value\": 5,\n            \"vowel\": true\n          }\n        ]\n      }\n    ]\n  },\n  \"life_path\": {\n    \"input\": 14,\n    \"steps\": [\n      14,\n      5\n    ],\n    \"result\": 5,\n    \"components\": [\n      {\n        \"input\": 7,\n        \"steps\": [\n          7\n        ],\n        \"result\": 7\n      },\n      {\n        \"input\": 15,\n        \"steps\": [\n          15,\n          6\n        ],\n        \"result\": 6\n      },\n      {\n        \"input\": 1990,\n        \"steps\": [\n          1990,\n          19,\n          10,\n          1\n        ],\n        \"result\": 1\n      }\n    ]\n  },\n  \"birthday\": {\n    \"original_day\": 15,\n    \"companion\": {\n      \"input\": 15,\n      \"steps\": [\n        15,\n        6\n      ],\n      \"result\": 6\n    }\n  },\n  \"expression\": {\n    \"input\": 3,\n    \"steps\": [\n      3\n    ],\n    \"result\": 3,\n    \"components\": [\n      {\n        \"input\": 21,\n        \"steps\": [\n          21,\n          3\n        ],\n        \"result\": 3\n      }\n    ]\n  },\n  \"soul_urge\": {\n    \"input\": 6,\n    \"steps\": [\n      6\n    ],\n    \"result\": 6,\n    \"components\": [\n      {\n        \"input\": 15,\n        \"steps\": [\n          15,\n          6\n        ],\n        \"result\": 6\n      }\n    ]\n  },\n  \"personality\": {\n    \"input\": 6,\n    \"steps\": [\n      6\n    ],\n    \"result\": 6,\n    \"components\": [\n      {\n        \"input\": 6,\n        \"steps\": [\n          6\n        ],\n        \"result\": 6\n      }\n    ]\n  },\n  \"cycles\": {\n    \"sun\": {\n      \"input\": 22,\n      \"steps\": [\n        22,\n        4\n      ],\n      \"result\": 4\n    },\n    \"year\": {\n      \"input\": 2030,\n      \"steps\": [\n        2030,\n        5\n      ],\n      \"result\": 5\n    },\n    \"month\": {\n      \"input\": 16,\n      \"steps\": [\n        16,\n        7\n      ],\n      \"result\": 7\n    },\n    \"day\": {\n      \"input\": 16,\n      \"steps\": [\n        16,\n        7\n      ],\n      \"result\": 7\n    },\n    \"year_interval\": [\n      \"2026-01-01\",\n      \"2027-01-01\"\n    ]\n  },\n  \"sources\": [\n    {\n      \"id\": \"numerology-decoz-life-path-v1\",\n      \"url\": \"https://www.worldnumerology.com/numerology-life-path/\",\n      \"locator\": \"Calculation steps; October15,1998 example\"\n    },\n    {\n      \"id\": \"numerology-decoz-expression-v1\",\n      \"url\": \"https://www.worldnumerology.com/numerology-expression/\",\n      \"locator\": \"Thomas Cruise Mapother example; name selection\"\n    },\n    {\n      \"id\": \"numerology-decoz-guide-v1\",\n      \"url\": \"https://www.worldnumerology.com/do-your-own-reading/\",\n      \"locator\": \"Birthday, Heart's Desire, Personality and personal-cycle sections\"\n    },\n    {\n      \"id\": \"numerology-decoz-daily-v1\",\n      \"url\": \"https://www.worldnumerology.com/free-forecasts/daily-number-forecast/\",\n      \"locator\": \"Steps1\\u20134, September12/October12,2026 example\"\n    },\n    {\n      \"id\": \"numerology-decoz-vowels-v1\",\n      \"url\": \"https://www.worldnumerology.com/numerology-soul-urge/\",\n      \"locator\": \"Vowel and pronunciation-dependent Y calculation\"\n    }\n  ],\n  \"conventions\": {\n    \"technique_id\": 4,\n    \"profile\": \"decoz-component-reduction\",\n    \"version\": 1,\n    \"core\": \"Reduce date components/name parts separately, retaining11/22/33 at every core reduction stage. Keep original totals and digit-sum steps.\",\n    \"birthday\": \"Retain actual day1\\u201331 as Birthday number; show reduced/master companion separately, never replace original day.\",\n    \"cycles\": \"Calendar Jan1 year transition; reduce cycles to1\\u20139 without masters. Use sequential Sun/birth-month-day \\u2192 year \\u2192 month \\u2192 day method from daily guide; compounds belong to that method, not aggregate formula.\",\n    \"name_policy\": \"Explicit birth/current basis. ASCII A\\u2013Z case-insensitive only; ASCII space separates name parts. Hyphen/apostrophe join letters inside a part and are recorded as zero-value separators. This token policy is an explicit implementation convention, not claimed universal Decoz doctrine. Reject other characters/diacritics rather than transliterate. Every Y occurrence requires caller-specified vowel/consonant role, ordered left-to-right. No vowels/consonants in entire name yields unsupported null for that number.\",\n    \"sources\": [\n      {\n        \"id\": \"numerology-decoz-life-path-v1\",\n        \"url\": \"https://www.worldnumerology.com/numerology-life-path/\",\n        \"locator\": \"Calculation steps; October15,1998 example\"\n      },\n      {\n        \"id\": \"numerology-decoz-expression-v1\",\n        \"url\": \"https://www.worldnumerology.com/numerology-expression/\",\n        \"locator\": \"Thomas Cruise Mapother example; name selection\"\n      },\n      {\n        \"id\": \"numerology-decoz-guide-v1\",\n        \"url\": \"https://www.worldnumerology.com/do-your-own-reading/\",\n        \"locator\": \"Birthday, Heart's Desire, Personality and personal-cycle sections\"\n      },\n      {\n        \"id\": \"numerology-decoz-daily-v1\",\n        \"url\": \"https://www.worldnumerology.com/free-forecasts/daily-number-forecast/\",\n        \"locator\": \"Steps1\\u20134, September12/October12,2026 example\"\n      },\n      {\n        \"id\": \"numerology-decoz-vowels-v1\",\n        \"url\": \"https://www.worldnumerology.com/numerology-soul-urge/\",\n        \"locator\": \"Vowel and pronunciation-dependent Y calculation\"\n      }\n    ],\n    \"unsupported\": [\n      \"Chaldean\",\n      \"Lo Shu\",\n      \"gematria\",\n      \"automatic pronunciation/transliteration\",\n      \"birthday-based personal-year transition\",\n      \"aggregate-method compound interpretations\"\n    ],\n    \"rights\": \"Factual procedures and short original summaries only; no copyrighted corpus ingested.\"\n  },\n  \"limitations\": [\n    \"Symbolic calculations, not validated personality diagnoses or event probabilities.\",\n    \"Current-name results are overlays, not silently substituted birth-name numbers.\"\n  ],\n  \"readings\": [\n    {\n      \"scope\": \"expression\",\n      \"number\": 3,\n      \"coverage\": \"direct\",\n      \"text\": \"Creative communication.\",\n      \"source_id\": \"numerology-decoz-expression-v1\",\n      \"url\": \"https://www.worldnumerology.com/numerology-expression/\",\n      \"locator\": \"The Meaning of Your Expression Numbers\"\n    },\n    {\n      \"scope\": \"personal_year\",\n      \"number\": 5,\n      \"coverage\": \"direct\",\n      \"text\": \"Change and flexibility.\",\n      \"source_id\": \"numerology-decoz-year-symbols-v1\",\n      \"url\": \"https://www.worldnumerology.com/personal-numerology-forecast/\",\n      \"locator\": \"Meaning of Your Personal Year Cycles, numbered year sections; timeless themes only, not2026 event claims\"\n    },\n    {\n      \"scope\": \"life_path\",\n      \"coverage\": \"compositional\",\n      \"text\": \"Birth-date framework; no direct number-specific delineation in this core.\",\n      \"source_id\": \"numerology-decoz-guide-v1\",\n      \"url\": \"https://www.worldnumerology.com/do-your-own-reading/\",\n      \"locator\": \"Birthday, Heart's Desire, Personality and personal-cycle sections\"\n    },\n    {\n      \"scope\": \"soul_urge\",\n      \"coverage\": \"compositional\",\n      \"text\": \"Vowel-based motivation context.\",\n      \"source_id\": \"numerology-decoz-guide-v1\",\n      \"url\": \"https://www.worldnumerology.com/do-your-own-reading/\",\n      \"locator\": \"Birthday, Heart's Desire, Personality and personal-cycle sections\"\n    },\n    {\n      \"scope\": \"personality\",\n      \"coverage\": \"compositional\",\n      \"text\": \"Consonant-based outward presentation context.\",\n      \"source_id\": \"numerology-decoz-guide-v1\",\n      \"url\": \"https://www.worldnumerology.com/do-your-own-reading/\",\n      \"locator\": \"Birthday, Heart's Desire, Personality and personal-cycle sections\"\n    },\n    {\n      \"scope\": \"birthday\",\n      \"coverage\": \"compositional\",\n      \"text\": \"Actual day retained alongside its reduced companion.\",\n      \"source_id\": \"numerology-decoz-guide-v1\",\n      \"url\": \"https://www.worldnumerology.com/do-your-own-reading/\",\n      \"locator\": \"Birthday, Heart's Desire, Personality and personal-cycle sections\"\n    }\n  ],\n  \"interpretation_limits\": \"Short original source summaries, symbolic themes only. No empirical personality/outcome validation. Core numbers other than Expression are not assigned Expression meanings; cycle Month/Day-specific delineations remain unsupported.\"\n}\n",
    "native_stderr": "",
    "provenance": {
      "core_release": "core-v1.0.0",
      "profile_identifiers": "decoz-component-reduction",
      "python_entry_point": "future.__main__.main",
      "sources": [
        {
          "path": "knowledge/numerology_sources.json",
          "sha256": "ef7211d145b278f4d0d6d73243949c582c30f447c2aabe21a4633947644a99e6"
        }
      ]
    },
    "limits": [
      "Native unsupported states remain inside native_output.",
      "This invocation is not empirical validation or a shared prediction score."
    ],
    "lab_profile_sha256": "5b8b09b98f1f3a46a24db9fc6b334e7ea776f7e03d6646e2e05fa8907e95a3a3",
    "lab_code_sha256": "74284978fb37ad9edc423588f27e0ce190d575e04b266ac2757b27417340edba",
    "invocation_sha256": "7b1bd67d77aeb30251510f1d86203166c79acf002168d74ab4fbac5c3052c32a"
  }
}
```

