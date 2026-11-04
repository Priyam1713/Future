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

### o1 — applicable

```json
{
  "id": "o1",
  "user_record": {
    "id": "o1",
    "symbol_id": "anchor",
    "region": "rim"
  },
  "status": "applicable",
  "reference": {
    "id": "anchor",
    "name": "Anchor",
    "aliases": [],
    "definition": "Loyal friends,constancy,wishes and a sailor-specific association.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "Dictionary A:Anchor",
    "alternatives": [],
    "cases": [
      {
        "id": "general",
        "statement": "Kent associates anchor with loyal friends,constancy in love and realised wishes.",
        "requires": {},
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Anchor"
      },
      {
        "id": "sailor",
        "statement": "Kent calls anchor a safety emblem for a sailor.",
        "requires": {
          "context.sailor": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Anchor"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "general",
        "statement": "Kent associates anchor with loyal friends,constancy in love and realised wishes.",
        "requires": {},
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Anchor"
      },
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {},
      "missing": [],
      "rule_id": "tasseography.kent.anchor.general",
      "forecast": false
    },
    {
      "reference": {
        "id": "sailor",
        "statement": "Kent calls anchor a safety emblem for a sailor.",
        "requires": {
          "context.sailor": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Anchor"
      },
      "status": "insufficient_information",
      "intrinsic_status": "insufficient_information",
      "condition_results": {
        "context.sailor": "insufficient_information"
      },
      "missing": [
        "context.sailor"
      ],
      "rule_id": "tasseography.kent.anchor.sailor",
      "forecast": false
    }
  ],
  "zones": {
    "status": "applicable",
    "qualifications": [
      {
        "region": "rim",
        "association": "comparatively_soon",
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChII:handle,near-rim,sides,bottom and intuitive timing qualification"
      }
    ],
    "conflicts": [],
    "missing": [],
    "calendar_date": null,
    "handle_reference": "ChII:handle represents consultant,home or current abode when away;directly underneath denotes present/immediate circumstances.",
    "convention": "bottom_circle/bottom_centre are named subregions of source bottom,retaining FigureVIII circle/centre labels. No numeric boundaries,absolute dates or priority over under-handle present/immediate qualification."
  },
  "missing": [
    "context.sailor"
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

### o2 — applicable

```json
{
  "id": "o2",
  "user_record": {
    "id": "o2",
    "symbol_id": "apron",
    "region": "side",
    "proximity": "far"
  },
  "status": "applicable",
  "reference": {
    "id": "apron",
    "name": "Apron",
    "aliases": [],
    "definition": "Meaning depends on proximity to the consultant.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "Dictionary A:Apron",
    "alternatives": [],
    "cases": [
      {
        "id": "near",
        "statement": "Kent associates nearby apron with a new friend.",
        "requires": {
          "proximity": "near"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Apron"
      },
      {
        "id": "far",
        "statement": "Kent associates distant apron with new work or acquaintances.",
        "requires": {
          "proximity": "far"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Apron"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "near",
        "statement": "Kent associates nearby apron with a new friend.",
        "requires": {
          "proximity": "near"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Apron"
      },
      "status": "not_applicable",
      "intrinsic_status": "not_applicable",
      "condition_results": {
        "proximity": "not_applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.apron.near",
      "forecast": false
    },
    {
      "reference": {
        "id": "far",
        "statement": "Kent associates distant apron with new work or acquaintances.",
        "requires": {
          "proximity": "far"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Apron"
      },
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {
        "proximity": "applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.apron.far",
      "forecast": false
    }
  ],
  "zones": {
    "status": "applicable",
    "qualifications": [
      {
        "region": "side",
        "association": "more_distant",
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChII:handle,near-rim,sides,bottom and intuitive timing qualification"
      }
    ],
    "conflicts": [],
    "missing": [],
    "calendar_date": null,
    "handle_reference": "ChII:handle represents consultant,home or current abode when away;directly underneath denotes present/immediate circumstances.",
    "convention": "bottom_circle/bottom_centre are named subregions of source bottom,retaining FigureVIII circle/centre labels. No numeric boundaries,absolute dates or priority over under-handle present/immediate qualification."
  },
  "missing": [],
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

### o3 — applicable

```json
{
  "id": "o3",
  "user_record": {
    "id": "o3",
    "symbol_id": "acorn",
    "region": "bottom"
  },
  "status": "applicable",
  "reference": {
    "id": "acorn",
    "name": "Acorn",
    "aliases": [],
    "definition": "Industry,gain,strength and a potentially fruitful short journey;several add a qualification.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "Dictionary A:Acorn",
    "alternatives": [],
    "cases": [
      {
        "id": "general",
        "statement": "Kent associates acorn with health/strength,results of effort and possible gain from a short journey.",
        "requires": {},
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Acorn"
      },
      {
        "id": "several",
        "statement": "Kent adds good fortune and ease for several acorns.",
        "requires": {
          "multiplicity": "several"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Acorn"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "general",
        "statement": "Kent associates acorn with health/strength,results of effort and possible gain from a short journey.",
        "requires": {},
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Acorn"
      },
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {},
      "missing": [],
      "rule_id": "tasseography.kent.acorn.general",
      "forecast": false
    },
    {
      "reference": {
        "id": "several",
        "statement": "Kent adds good fortune and ease for several acorns.",
        "requires": {
          "multiplicity": "several"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Acorn"
      },
      "status": "insufficient_information",
      "intrinsic_status": "insufficient_information",
      "condition_results": {
        "multiplicity": "insufficient_information"
      },
      "missing": [
        "multiplicity"
      ],
      "rule_id": "tasseography.kent.acorn.several",
      "forecast": false
    }
  ],
  "zones": {
    "status": "applicable",
    "qualifications": [
      {
        "region": "bottom",
        "association": "far_distant",
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChII:handle,near-rim,sides,bottom and intuitive timing qualification"
      }
    ],
    "conflicts": [],
    "missing": [],
    "calendar_date": null,
    "handle_reference": "ChII:handle represents consultant,home or current abode when away;directly underneath denotes present/immediate circumstances.",
    "convention": "bottom_circle/bottom_centre are named subregions of source bottom,retaining FigureVIII circle/centre labels. No numeric boundaries,absolute dates or priority over under-handle present/immediate qualification."
  },
  "missing": [
    "multiplicity"
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

## Editorial symbolic synthesis

```json
[
  {
    "observation_id": "o1",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [
      "Kent associates anchor with loyal friends,constancy in love and realised wishes."
    ],
    "time_qualifications": [
      "comparatively_soon"
    ],
    "unresolved": [
      "context.sailor"
    ],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  },
  {
    "observation_id": "o2",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [
      "Kent associates distant apron with new work or acquaintances."
    ],
    "time_qualifications": [
      "more_distant"
    ],
    "unresolved": [],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  },
  {
    "observation_id": "o3",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [
      "Kent associates acorn with health/strength,results of effort and possible gain from a short journey."
    ],
    "time_qualifications": [
      "far_distant"
    ],
    "unresolved": [
      "multiplicity"
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
    "applicable": 3,
    "not_applicable": 0,
    "insufficient_information": 0,
    "conflicting_evidence": 0,
    "unsupported": 0
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
        "symbol_id": "anchor",
        "region": "rim"
      },
      {
        "id": "o2",
        "symbol_id": "apron",
        "region": "side",
        "proximity": "far"
      },
      {
        "id": "o3",
        "symbol_id": "acorn",
        "region": "bottom"
      }
    ]
  },
  "input_sha256": "62d0f44f8da46a6617b52c3fc236eceb96c0db42de2f9504b7cd4ddc8d21a0e0",
  "profile_sha256": "cc078f560bceca9d59296a29e99070e9f82059829eb2ee7501b926c90b658541",
  "source_sha256": "f6b4b81e04e81ba0efcd91228b76c143ac3b7262484d96f3b3d669d379839c56",
  "serialization": "Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw content line endings retained",
  "external_calls": false,
  "rng": false,
  "generated_placements": false
}
```
