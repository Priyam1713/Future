# Hydromancy water observation/reference report

Profile: andrews-spees2005-water-reference-v1

Jennifer Spees article,July1,2005,explicitly excerpts Ted Andrews,Crystal Balls &amp; Crystal Bowls,in Water Scrying. Not Donald Tyson’s instructions;original Andrews book edition/pagination uninspected. Ranked Tyson/Betz metadata remain separate.

Hypothetical orrecorded observations suffice;no unusual imagery is required.

## Sources andrights

```json
[
  {
    "id": "hydromancy-spees-andrews2005-public-water-core-v1",
    "technique_id": 31,
    "rank": null,
    "author": "Jennifer Spees,article;Ted Andrews,explicitly attributed Water Scrying excerpt;Llewellyn Worldwide",
    "edition": "Scrying:Catch a Glimpse of Your Future;publisher article dated2005-07-01,Water Scrying section excerpted from Crystal Balls & Crystal Bowls;original Andrews book edition/pagination not inspected",
    "url": "https://www.llewellyn.com/journal/article/877",
    "locator": "Byline/date;introductory Tyson discussion;Water Scrying heading andexplicit Andrews attribution;water-bowl/puddle,gaze andfogginess paragraphs",
    "finding": "Separates Tyson book discussion from Andrews water excerpt. Selected water-specific facts:rain pool orrainwater in dark bowl/cauldron,undisturbed positioning,relaxation andsoft half-focused gaze rather than intense staring. Perceived fogginess is given an attributed opening/awakening account;later colors/images/faces are claimed experiences,not a shape dictionary. Faerie/spirit access andpromised improvement remain practitioner claims. No ripple-count,drop-count orcolor-outcome mapping supplied.",
    "ingestion": "facts_only",
    "rights_note": "Book text,modern translations,publisher article,editorial database andimages have separate rights. Original concise factual notes/locators only;no chapters,invocations,ritual corpus,scans orillustrations redistributed. Public hosting is not blanket reproduction permission.",
    "checked_on": "2026-11-05",
    "snapshot_sha256": "9c33165a8013d5f29a92d9d15f2025bcaba9ff14035b24bfc96b9e43b90394be",
    "snapshot_bytes": 156847
  },
  {
    "id": "hydromancy-kyprianos-t1085-water-context-core-v1",
    "technique_id": 31,
    "rank": null,
    "author": "Kyprianos Database;principal editors Korshi Dosoo,Markéta Preininger,Roxanne Bélanger Sarrazin;entry reports text/translation from Tibet2014,subsequent MPS/EL/KD editorial checks",
    "edition": "KYP T1085:Bowl divination procedure;M106,StrasbourgK550/P.Stras.Copt.9/PCM I34;catalog date901–1100;Coptic,Fayumic(non-standard);entry includes revisions through2023",
    "url": "https://www.coptic-magic.phil.uni-wuerzburg.de/index.php/text/kyp-t-1085/",
    "locator": "Metadata Date/Type of text/Language/Text position;translation p1,ll7–10 and17–26;p2,ll6–17;apparatus;Editor field",
    "finding": "Fragmentary later Coptic formulary describes a cup of water before the speaker andan invoked vision through a scryer. Medium identification is marked uncertain;editorial lacunae andquestion marks are preserved. This is documentary evidence for a distinct bowl-inquiry tradition,not a complete reproducible rite,a Betz original passage,orverified treasure/spirit information. No invocation text orrepetition protocol copied.",
    "ingestion": "facts_only",
    "rights_note": "Book text,modern translations,publisher article,editorial database andimages have separate rights. Original concise factual notes/locators only;no chapters,invocations,ritual corpus,scans orillustrations redistributed. Public hosting is not blanket reproduction permission.",
    "checked_on": "2026-11-05",
    "snapshot_sha256": "393a072d1f85809ebf673a1414902d8de74320c59746ca9b346eac1ccf46b54c",
    "snapshot_bytes": 135433
  },
  {
    "id": "hydromancy-noaa2020-oil-water-physical-core-v1",
    "technique_id": 31,
    "rank": null,
    "author": "NOAA Office of Response andRestoration",
    "edition": "How Does Oil Act in Water?;educational webpage,last updated2020-06-12",
    "url": "https://response.restoration.noaa.gov/exercises_oilfloats",
    "locator": "Vegetable-oil observation steps3–4;phase/layer discussion;wind/current context;last updated field",
    "finding": "Described vegetable-oil example spreads andforms blobs over water,with separate oil/water phases;the page notes differing oil spreading rates andenvironmental transport effects. This is physical educational context,not an omen system,a guarantee for every liquid orsoftware fluid validation. No experiment,water orchemical use required for a manual/hypothetical software record.",
    "ingestion": "facts_only",
    "rights_note": "Book text,modern translations,publisher article,editorial database andimages have separate rights. Original concise factual notes/locators only;no chapters,invocations,ritual corpus,scans orillustrations redistributed. Public hosting is not blanket reproduction permission.",
    "checked_on": "2026-11-05",
    "snapshot_sha256": "5529a9b6ac2028374abcc29fcc3260bda06f061b6385aeff51955be8510ef332",
    "snapshot_bytes": 41845
  }
]
```

## Declared session

```json
{
  "medium": "water",
  "container": "dark_bowl",
  "rainwater": true,
  "gaze": "soft"
}
```

## Water-specific session conditions

```json
[
  {
    "id": "dark_bowl",
    "rule_id": "hydromancy.andrews2005.dark_bowl",
    "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
    "locator": "Water Scrying:opening/context paragraphs",
    "status": "source_supported",
    "conditions": [
      {
        "field": "medium",
        "expected": "water",
        "declared": "water",
        "status": "source_supported"
      },
      {
        "field": "container",
        "expected": "dark_bowl",
        "declared": "dark_bowl",
        "status": "source_supported"
      },
      {
        "field": "rainwater",
        "expected": true,
        "declared": true,
        "status": "source_supported"
      }
    ],
    "account": "Andrews describes rainwater in a dark bowl.",
    "display_held": false
  },
  {
    "id": "cauldron",
    "rule_id": "hydromancy.andrews2005.cauldron",
    "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
    "locator": "Water Scrying:opening/context paragraphs",
    "status": "context_mismatch",
    "conditions": [
      {
        "field": "medium",
        "expected": "water",
        "declared": "water",
        "status": "source_supported"
      },
      {
        "field": "container",
        "expected": "cauldron",
        "declared": "dark_bowl",
        "status": "context_mismatch"
      },
      {
        "field": "rainwater",
        "expected": true,
        "declared": true,
        "status": "source_supported"
      }
    ],
    "account": null,
    "display_held": false
  },
  {
    "id": "rain_pool",
    "rule_id": "hydromancy.andrews2005.rain_pool",
    "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
    "locator": "Water Scrying:opening/context paragraphs",
    "status": "context_mismatch",
    "conditions": [
      {
        "field": "medium",
        "expected": "water",
        "declared": "water",
        "status": "source_supported"
      },
      {
        "field": "container",
        "expected": "natural_pool",
        "declared": "dark_bowl",
        "status": "context_mismatch"
      },
      {
        "field": "rainwater",
        "expected": true,
        "declared": true,
        "status": "source_supported"
      }
    ],
    "account": null,
    "display_held": false
  },
  {
    "id": "position",
    "rule_id": "hydromancy.andrews2005.position",
    "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
    "locator": "Water Scrying:positioning paragraph",
    "status": "insufficient_information",
    "conditions": [
      {
        "field": "water_context",
        "expected": true,
        "declared": {
          "medium": "water",
          "container": "dark_bowl",
          "rainwater": true
        },
        "status": "source_supported"
      },
      {
        "field": "observer_undisturbed",
        "expected": true,
        "declared": null,
        "status": "insufficient_information"
      },
      {
        "field": "surface_visible",
        "expected": true,
        "declared": null,
        "status": "insufficient_information"
      }
    ],
    "account": null,
    "display_held": false
  },
  {
    "id": "gaze",
    "rule_id": "hydromancy.andrews2005.gaze",
    "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
    "locator": "Water Scrying:gaze paragraph",
    "status": "source_supported",
    "conditions": [
      {
        "field": "water_context",
        "expected": true,
        "declared": {
          "medium": "water",
          "container": "dark_bowl",
          "rainwater": true
        },
        "status": "source_supported"
      },
      {
        "field": "gaze",
        "expected": [
          "soft",
          "half_focused"
        ],
        "declared": "soft",
        "status": "source_supported"
      }
    ],
    "account": "Andrews recommends soft,half-focused gazing rather than intense staring.",
    "display_held": false
  },
  {
    "id": "relaxation",
    "rule_id": "hydromancy.andrews2005.relaxation",
    "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
    "locator": "Water Scrying:positioning/relaxation paragraph",
    "status": "insufficient_information",
    "conditions": [
      {
        "field": "water_context",
        "expected": true,
        "declared": {
          "medium": "water",
          "container": "dark_bowl",
          "rainwater": true
        },
        "status": "source_supported"
      },
      {
        "field": "relaxed",
        "expected": true,
        "declared": null,
        "status": "insufficient_information"
      }
    ],
    "account": null,
    "display_held": false
  }
]
```

## Ordered observations

```json
[
  {
    "id": "o1",
    "sequence": 1,
    "origin": "hypothetical",
    "declared": {
      "id": "o1",
      "sequence": 1,
      "category": "perceived_fogginess",
      "basis": "physical",
      "alternatives": [
        "physical_mist"
      ]
    },
    "effective_context": {
      "medium": "water",
      "container": "dark_bowl",
      "rainwater": true,
      "gaze": "soft"
    },
    "status": "conflicting_evidence",
    "context_evaluation": [
      {
        "id": "dark_bowl",
        "rule_id": "hydromancy.andrews2005.dark_bowl",
        "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
        "locator": "Water Scrying:opening/context paragraphs",
        "status": "source_supported",
        "conditions": [
          {
            "field": "medium",
            "expected": "water",
            "declared": "water",
            "status": "source_supported"
          },
          {
            "field": "container",
            "expected": "dark_bowl",
            "declared": "dark_bowl",
            "status": "source_supported"
          },
          {
            "field": "rainwater",
            "expected": true,
            "declared": true,
            "status": "source_supported"
          }
        ],
        "account": "Andrews describes rainwater in a dark bowl.",
        "display_held": false
      },
      {
        "id": "cauldron",
        "rule_id": "hydromancy.andrews2005.cauldron",
        "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
        "locator": "Water Scrying:opening/context paragraphs",
        "status": "context_mismatch",
        "conditions": [
          {
            "field": "medium",
            "expected": "water",
            "declared": "water",
            "status": "source_supported"
          },
          {
            "field": "container",
            "expected": "cauldron",
            "declared": "dark_bowl",
            "status": "context_mismatch"
          },
          {
            "field": "rainwater",
            "expected": true,
            "declared": true,
            "status": "source_supported"
          }
        ],
        "account": null,
        "display_held": false
      },
      {
        "id": "rain_pool",
        "rule_id": "hydromancy.andrews2005.rain_pool",
        "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
        "locator": "Water Scrying:opening/context paragraphs",
        "status": "context_mismatch",
        "conditions": [
          {
            "field": "medium",
            "expected": "water",
            "declared": "water",
            "status": "source_supported"
          },
          {
            "field": "container",
            "expected": "natural_pool",
            "declared": "dark_bowl",
            "status": "context_mismatch"
          },
          {
            "field": "rainwater",
            "expected": true,
            "declared": true,
            "status": "source_supported"
          }
        ],
        "account": null,
        "display_held": false
      },
      {
        "id": "position",
        "rule_id": "hydromancy.andrews2005.position",
        "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
        "locator": "Water Scrying:positioning paragraph",
        "status": "insufficient_information",
        "conditions": [
          {
            "field": "water_context",
            "expected": true,
            "declared": {
              "medium": "water",
              "container": "dark_bowl",
              "rainwater": true
            },
            "status": "source_supported"
          },
          {
            "field": "observer_undisturbed",
            "expected": true,
            "declared": null,
            "status": "insufficient_information"
          },
          {
            "field": "surface_visible",
            "expected": true,
            "declared": null,
            "status": "insufficient_information"
          }
        ],
        "account": null,
        "display_held": false
      },
      {
        "id": "gaze",
        "rule_id": "hydromancy.andrews2005.gaze",
        "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
        "locator": "Water Scrying:gaze paragraph",
        "status": "source_supported",
        "conditions": [
          {
            "field": "water_context",
            "expected": true,
            "declared": {
              "medium": "water",
              "container": "dark_bowl",
              "rainwater": true
            },
            "status": "source_supported"
          },
          {
            "field": "gaze",
            "expected": [
              "soft",
              "half_focused"
            ],
            "declared": "soft",
            "status": "source_supported"
          }
        ],
        "account": "Andrews recommends soft,half-focused gazing rather than intense staring.",
        "display_held": false
      },
      {
        "id": "relaxation",
        "rule_id": "hydromancy.andrews2005.relaxation",
        "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
        "locator": "Water Scrying:positioning/relaxation paragraph",
        "status": "insufficient_information",
        "conditions": [
          {
            "field": "water_context",
            "expected": true,
            "declared": {
              "medium": "water",
              "container": "dark_bowl",
              "rainwater": true
            },
            "status": "source_supported"
          },
          {
            "field": "relaxed",
            "expected": true,
            "declared": null,
            "status": "insufficient_information"
          }
        ],
        "account": null,
        "display_held": false
      }
    ],
    "cases": [
      {
        "id": "fogginess",
        "rule_id": "hydromancy.andrews2005.fogginess",
        "source_id": "hydromancy-spees-andrews2005-public-water-core-v1",
        "locator": "Water Scrying:final perceived-fogginess paragraph",
        "status": "conflicting_evidence",
        "conditions": [
          {
            "field": "water_context",
            "expected": true,
            "declared": {
              "medium": "water",
              "container": "dark_bowl",
              "rainwater": true
            },
            "status": "source_supported"
          },
          {
            "field": "gaze",
            "expected": [
              "soft",
              "half_focused"
            ],
            "declared": "soft",
            "status": "source_supported"
          },
          {
            "field": "category",
            "expected": "perceived_fogginess",
            "declared": "perceived_fogginess",
            "status": "source_supported"
          },
          {
            "field": "basis",
            "expected": "subjective",
            "declared": "physical",
            "status": "context_mismatch"
          }
        ],
        "account": null,
        "display_held": false
      }
    ],
    "classification_conflict": true,
    "unresolved": [],
    "symbolic_mapping": "No universal ripple/drop/color/shape meaning",
    "physical_or_extraordinary_cause_verified": false
  }
]
```

## Continuation

```json
{
  "display_held": false,
  "message": "Hypothetical orrecorded observations suffice;no unusual imagery is required."
}
```

## Editorial reflection

```json
"Compare your selected classifications with your own associations;source conformity does not establish an external orfuture event."
```

## Historical documentary reference

```json
{
  "source_id": "hydromancy-kyprianos-t1085-water-context-core-v1",
  "title": "KYP T1085:Bowl divination procedure",
  "witness": "M106;Strasbourg K550;P.Stras.Copt.9;PCM I34",
  "catalog_date": [
    901,
    1100
  ],
  "language": "Egyptian (Coptic)",
  "dialect": "Fayumic (non-standard)",
  "locator": "Metadata;translation p1,ll7–10,17–26;p2,ll6–17;Editor/apparatus",
  "editorial_layers": "Text/translation from Tibet2014;MPS2019–2020;EL/team photograph checks2021;KD autopsy2021/revision2023",
  "medium_identification": "uncertain",
  "fragmentary": true,
  "betz_alignment_verified": false,
  "executable": false,
  "account": "The fragmentary formulary mentions a water cup before the speaker andan invoked inquiry through a scryer. Lacunae anduncertain identification prevent reconstruction of a complete rite."
}
```

## Requested documentary comparison

```json
null
```

## User notes

```json
null
```

## Evidence layers

```json
{
  "direct_source": "Verified water-specific practitioner references andseparate Coptic/NOAA documentary facts",
  "user_attributed": "Declared medium,vessel,conditions,physical movement,perceptions,imagination andraw associations",
  "editorial": "Condition matching,classification/conflict bookkeeping andneutral reflection",
  "unsupported": "Spirits,clairvoyance,hidden facts,future events,psychological diagnoses orphysical causes from text"
}
```

## Application conventions

```json
[
  "Water context requires declared water-only medium,rain provenance anddark bowl/cauldron/natural pool. Unknown values are never defaulted to water.",
  "Observer undisturbed andsurface visibility compare the positioning passage. Still water is not a source requirement;surface movement is recorded without an omen meaning.",
  "Fogginess means an explicitly selected subjective experience,not physical mist,glare,reflection orimagined imagery. Source-supported labels mean conformity of declarations,not empirical validation.",
  "Per-observation context explicitly overrides supplied session fields;remaining context inherits session declarations. No text orphoto inference.",
  "Feature alternatives that match andfail a condition conflict;missing/null/unknown evidence stays insufficient. Contradictory category/basis declarations conflict.",
  "Discontinued ordiscomfort declarations hold displayed subjective symbolic accounts andreflection prompts;reference conditions remain reviewable. No imagery,water orhardware required.",
  "Relaxation/gaze references are optional source comparisons,not an instruction to induce altered states orsee unusual imagery. Hand gestures/spirit invitations andoperational invocations omitted."
]
```

## Limits

```json
[
  "Universal ripple/drop/color/shape omens",
  "Spirits,clairvoyance,hidden information orfactual future events",
  "Clinical/psychological diagnosis orphysical cause verification",
  "Full Tyson orBetz methods",
  "Historical ritual execution",
  "Fluid/optical detection,recognition,simulation,LLM orrandom generation"
]
```

## Exact replay metadata

```json
{
  "request": {
    "schema_version": 1,
    "profile": "andrews-spees2005-water-reference-v1",
    "task": "water_observation_reference",
    "mode": "manual",
    "origin": "hypothetical",
    "session": {
      "medium": "water",
      "container": "dark_bowl",
      "rainwater": true,
      "gaze": "soft"
    },
    "observations": [
      {
        "id": "o1",
        "sequence": 1,
        "category": "perceived_fogginess",
        "basis": "physical",
        "alternatives": [
          "physical_mist"
        ]
      }
    ]
  },
  "input_sha256": "6d2b27ee91844f63fe27c209c0d115703ca4919051b54a920746adec3a06eb1c",
  "profile_sha256": "fb829b4364b439a47b4d059a3769710d51fa180b51147095b05e6a15c3513beb",
  "source_sha256": {
    "hydromancy-spees-andrews2005-public-water-core-v1": "9c33165a8013d5f29a92d9d15f2025bcaba9ff14035b24bfc96b9e43b90394be",
    "hydromancy-kyprianos-t1085-water-context-core-v1": "393a072d1f85809ebf673a1414902d8de74320c59746ca9b346eac1ccf46b54c",
    "hydromancy-noaa2020-oil-water-physical-core-v1": "5529a9b6ac2028374abcc29fcc3260bda06f061b6385aeff51955be8510ef332"
  },
  "serialization": "Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw field line endings retained",
  "external_calls": false,
  "rng": false,
  "generated_observations": false
}
```
