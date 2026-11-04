# Tasseography historical symbolic cup report

Profile: kent-pg6964-ordinary-cup-v2

PG6964 illustrated HTML posted2013-03-21,released2004;English digital witness,not verified print pagination

[tasseography-kent-pg6964-cup-facts-v2](https://www.gutenberg.org/files/6964/6964-h/6964-h.htm)

PG metadata lists public domain in USA;non-US law,PG license/trademark and individual images remain separate. Original short factual paraphrases only;no whole book,modern dictionary,scan or source illustration redistributed.

## Declared vessel and layout

```json
{
  "handle_orientation": "unknown",
  "geometry": false,
  "position_inferred": false,
  "ordering": "Input order retained",
  "vessel_method": "Ordinary Kent cup only",
  "context": {}
}
```

## Ordered manual placements

### o1 — insufficient_information

```json
{
  "id": "o1",
  "user_record": {
    "id": "o1",
    "symbol_id": "tea_cosy"
  },
  "status": "insufficient_information",
  "reference": {
    "id": "tea_cosy",
    "name": "Tea Cosy",
    "aliases": [],
    "definition": "Marital-status alternatives are author conventions,not inferred user circumstances.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "Dictionary T:Tea Cosy",
    "alternatives": [],
    "cases": [
      {
        "id": "unmarried",
        "statement": "Kent gives a possible remaining-single account.",
        "requires": {
          "context.marital_status": "unmarried"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary T:Tea Cosy"
      },
      {
        "id": "married",
        "statement": "Kent associates this with affection and small domestic comforts for a married consultant.",
        "requires": {
          "context.marital_status": "married"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary T:Tea Cosy"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "unmarried",
        "statement": "Kent gives a possible remaining-single account.",
        "requires": {
          "context.marital_status": "unmarried"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary T:Tea Cosy"
      },
      "status": "insufficient_information",
      "intrinsic_status": "insufficient_information",
      "condition_results": {
        "context.marital_status": "insufficient_information"
      },
      "missing": [
        "context.marital_status"
      ],
      "rule_id": "tasseography.kent.tea_cosy.unmarried",
      "forecast": false
    },
    {
      "reference": {
        "id": "married",
        "statement": "Kent associates this with affection and small domestic comforts for a married consultant.",
        "requires": {
          "context.marital_status": "married"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary T:Tea Cosy"
      },
      "status": "insufficient_information",
      "intrinsic_status": "insufficient_information",
      "condition_results": {
        "context.marital_status": "insufficient_information"
      },
      "missing": [
        "context.marital_status"
      ],
      "rule_id": "tasseography.kent.tea_cosy.married",
      "forecast": false
    }
  ],
  "zones": {
    "status": "insufficient_information",
    "qualifications": [],
    "conflicts": [],
    "missing": [
      "Declared qualitative region or under-handle relation"
    ],
    "calendar_date": null,
    "handle_reference": "ChII:handle represents consultant,home or current abode when away;directly underneath denotes present/immediate circumstances.",
    "convention": "bottom_circle/bottom_centre are named subregions of source bottom,retaining FigureVIII circle/centre labels. No numeric boundaries,absolute dates or priority over under-handle present/immediate qualification."
  },
  "missing": [
    "context.marital_status"
  ],
  "conflicts": [],
  "alternative_references": [],
  "alternatives_scope": "Source organ alternatives are retained without selecting wedding/death/ambition from unspecified surrounding signs",
  "observed_quantity": null,
  "qualifiers": {
    "locator": "ChIII:size/position and clarity",
    "size": "Relative size and position affect importance;no numeric strength score.",
    "clarity": "Clear separate symbols are more important than indistinct ones;unclear shape is not a personality assessment."
  }
}
```

### o2 — insufficient_information

```json
{
  "id": "o2",
  "user_record": {
    "id": "o2",
    "symbol_id": "organ"
  },
  "status": "insufficient_information",
  "reference": {
    "id": "organ",
    "name": "Organ",
    "aliases": [],
    "definition": "Requires surrounding signs;musician-specific achievement account.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "Dictionary O:Organ",
    "alternatives": [
      "Wedding",
      "Death",
      "Realised ambition"
    ],
    "cases": [
      {
        "id": "musician",
        "statement": "Kent gives an achievement account for a musician.",
        "requires": {
          "context.musician": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary O:Organ"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "musician",
        "statement": "Kent gives an achievement account for a musician.",
        "requires": {
          "context.musician": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary O:Organ"
      },
      "status": "insufficient_information",
      "intrinsic_status": "insufficient_information",
      "condition_results": {
        "context.musician": "insufficient_information"
      },
      "missing": [
        "context.musician"
      ],
      "rule_id": "tasseography.kent.organ.musician",
      "forecast": false
    }
  ],
  "zones": {
    "status": "insufficient_information",
    "qualifications": [],
    "conflicts": [],
    "missing": [
      "Declared qualitative region or under-handle relation"
    ],
    "calendar_date": null,
    "handle_reference": "ChII:handle represents consultant,home or current abode when away;directly underneath denotes present/immediate circumstances.",
    "convention": "bottom_circle/bottom_centre are named subregions of source bottom,retaining FigureVIII circle/centre labels. No numeric boundaries,absolute dates or priority over under-handle present/immediate qualification."
  },
  "missing": [
    "context.musician"
  ],
  "conflicts": [],
  "alternative_references": [],
  "alternatives_scope": "Source organ alternatives are retained without selecting wedding/death/ambition from unspecified surrounding signs",
  "observed_quantity": null,
  "qualifiers": {
    "locator": "ChIII:size/position and clarity",
    "size": "Relative size and position affect importance;no numeric strength score.",
    "clarity": "Clear separate symbols are more important than indistinct ones;unclear shape is not a personality assessment."
  }
}
```

### o3 — unsupported

```json
{
  "id": "o3",
  "user_record": {
    "id": "o3",
    "symbol_id": "unknown",
    "observation": "  A🐍 Café\r\n猫 "
  },
  "status": "unsupported",
  "reference": null,
  "cases": [],
  "zones": {
    "status": "insufficient_information",
    "qualifications": [],
    "conflicts": [],
    "missing": [
      "Declared qualitative region or under-handle relation"
    ],
    "calendar_date": null,
    "handle_reference": "ChII:handle represents consultant,home or current abode when away;directly underneath denotes present/immediate circumstances.",
    "convention": "bottom_circle/bottom_centre are named subregions of source bottom,retaining FigureVIII circle/centre labels. No numeric boundaries,absolute dates or priority over under-handle present/immediate qualification."
  },
  "missing": [
    "Verified symbol in named catalog"
  ],
  "conflicts": [],
  "alternative_references": []
}
```

## Editorial symbolic synthesis

```json
[
  {
    "observation_id": "o1",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [],
    "time_qualifications": [],
    "unresolved": [
      "context.marital_status",
      "Declared qualitative region or under-handle relation"
    ],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  },
  {
    "observation_id": "o2",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [],
    "time_qualifications": [],
    "unresolved": [
      "context.musician",
      "Declared qualitative region or under-handle relation"
    ],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  },
  {
    "observation_id": "o3",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [],
    "time_qualifications": [],
    "unresolved": [
      "Verified symbol in named catalog",
      "Declared qualitative region or under-handle relation"
    ],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  }
]
```

## Coverage summary

```json
{
  "observations": 3,
  "counts": {
    "applicable": 0,
    "not_applicable": 0,
    "insufficient_information": 2,
    "conflicting_evidence": 0,
    "unsupported": 1
  },
  "text": "Each source account is evaluated against explicit manual conditions. Depth and handle timing remain separate;missing or competing evidence is not repaired."
}
```

## Original Kent example comparison

```json
null
```

## Separate method limits

```json
{
  "saucer": {
    "locator": "ChII:saucer paragraphs",
    "note": "Centre consultant;surrounding circle home/near events;more distant circle later;outer rim remote future. Not executable cup zones and not interchangeable."
  },
  "nelros": "Separate marked-cup method;unsupported here"
}
```

## User notes

```json
null
```

## Provenance matrix

```json
{
  "direct": "Selected Kent source statements,zones,conditions and documentary accounts",
  "user_attributed": "Manual identities,positions,relations,uncertainty,observations,associations and optional context",
  "editorial": "Structured predicates,adjacency bookkeeping,comparisons and synthesis;not general symbol grammar",
  "unsupported": "Objective future outcomes,clinical/personality conclusions,photo/shape recognition or physical leaf simulation"
}
```

## Application conventions

```json
[
  "Manual named positions only;no shape/coordinate/prose inference. Adjacency means user-declared association,not computed distance. A supplied neighbor list is complete for that observation;omitted list is unknown. One-sided positive declarations suffice unless contradicted by another supplied complete list.",
  "Symbol/multiplicity/size/motion/context selectors are user declarations;no identity,health or profession inferred. No numeric threshold defines several;user chooses the source quantifier.",
  "Distinct observations are never silently aggregated into multiplicity. Conflicting identity,heading/motion,region or adjacency evidence is retained without rule priority.",
  "Surrounding-dots predicate requires declared surrounding arrangement plus an associated symbol;generic adjacency alone does not suffice."
]
```

## Historical limits

```json
[
  "Saucer executable profile",
  "Nelros decorated method",
  "Turkish tea and coffee methods",
  "Modern copyrighted dictionary",
  "Seeded arrangements,geometry,photo recognition,fluid simulation",
  "Objective future,clinical or personality conclusions",
  "Qualitative timing only;no dates,probabilities or deadlines computed.",
  "Source fidelity is not independent predictive validation."
]
```

## Exact replay metadata

```json
{
  "request": {
    "schema_version": 1,
    "profile": "kent-pg6964-ordinary-cup-v2",
    "task": "symbolic_cup_reading",
    "mode": "manual",
    "vessel": "cup",
    "observations": [
      {
        "id": "o1",
        "symbol_id": "tea_cosy"
      },
      {
        "id": "o2",
        "symbol_id": "organ"
      },
      {
        "id": "o3",
        "symbol_id": "unknown",
        "observation": "  A🐍 Café\r\n猫 "
      }
    ]
  },
  "input_sha256": "aa81f58fd83d743a2976432de9a9aa307991c8540d158e1e77418e2eebd942ff",
  "profile_sha256": "cc078f560bceca9d59296a29e99070e9f82059829eb2ee7501b926c90b658541",
  "source_sha256": "f6b4b81e04e81ba0efcd91228b76c143ac3b7262484d96f3b3d669d379839c56",
  "serialization": "Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw content line endings retained",
  "external_calls": false,
  "rng": false,
  "generated_placements": false
}
```
