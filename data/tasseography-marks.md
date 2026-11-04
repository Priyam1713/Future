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
    "symbol_id": "letter",
    "mark": "M",
    "size": "small",
    "region": "rim"
  },
  "status": "applicable",
  "reference": {
    "id": "letter",
    "name": "Alphabetic initial",
    "aliases": [],
    "definition": "Source letter-size convention;no person or place identified from an initial.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "ChIII:large/small initials and exceptions",
    "alternatives": [],
    "cases": [
      {
        "id": "large",
        "statement": "Kent generally associates larger initials with places.",
        "requires": {
          "size": "large",
          "mark_present": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChIII:large/small initials and exceptions"
      },
      {
        "id": "small",
        "statement": "Kent generally associates small initials with people;first,surname or pet-name possibilities remain open.",
        "requires": {
          "size": "small",
          "mark_present": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChIII:large/small initials and exceptions"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "large",
        "statement": "Kent generally associates larger initials with places.",
        "requires": {
          "size": "large",
          "mark_present": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChIII:large/small initials and exceptions"
      },
      "status": "not_applicable",
      "intrinsic_status": "not_applicable",
      "condition_results": {
        "size": "not_applicable",
        "mark_present": "applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.letter.large",
      "forecast": false
    },
    {
      "reference": {
        "id": "small",
        "statement": "Kent generally associates small initials with people;first,surname or pet-name possibilities remain open.",
        "requires": {
          "size": "small",
          "mark_present": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChIII:large/small initials and exceptions"
      },
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {
        "size": "applicable",
        "mark_present": "applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.letter.small",
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

### o2 — applicable

```json
{
  "id": "o2",
  "user_record": {
    "id": "o2",
    "symbol_id": "numeral",
    "numeral": 90,
    "adjacent_to": [
      "o3"
    ]
  },
  "status": "applicable",
  "reference": {
    "id": "numeral",
    "name": "Numeral",
    "aliases": [],
    "definition": "Only explicit money-quantity pairing is implemented;no date conversion.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "ChIII:numbers beside dots",
    "alternatives": [],
    "cases": [
      {
        "id": "money_quantity",
        "statement": "Kent treats a numeral beside dots as an amount in a money-related account;actual amount/currency/outcome is not verified.",
        "requires": {
          "numeral_present": true,
          "adjacent_symbol": "dots"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChIII:numbers beside dots"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "money_quantity",
        "statement": "Kent treats a numeral beside dots as an amount in a money-related account;actual amount/currency/outcome is not verified.",
        "requires": {
          "numeral_present": true,
          "adjacent_symbol": "dots"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChIII:numbers beside dots"
      },
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {
        "numeral_present": "applicable",
        "adjacent_symbol": "applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.numeral.money_quantity",
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
  "missing": [],
  "conflicts": [],
  "alternative_references": [],
  "alternatives_scope": "Source organ alternatives are retained without selecting wedding/death/ambition from unspecified surrounding signs",
  "observed_quantity": 90,
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
    "symbol_id": "dots",
    "arrangement": "surrounding"
  },
  "status": "applicable",
  "reference": {
    "id": "dots",
    "name": "Dots",
    "aliases": [],
    "definition": "Only explicit associated-symbol money account;no inference from unlocated dots.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "ChIII:dots around a symbol",
    "alternatives": [],
    "cases": [
      {
        "id": "money_context",
        "statement": "Kent associates dots surrounding a symbol with money in a source-dependent form.",
        "requires": {
          "adjacent_any": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChIII:dots around a symbol"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "money_context",
        "statement": "Kent associates dots surrounding a symbol with money in a source-dependent form.",
        "requires": {
          "adjacent_any": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChIII:dots around a symbol"
      },
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {
        "adjacent_any": "applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.dots.money_context",
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

## Editorial symbolic synthesis

```json
[
  {
    "observation_id": "o1",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [
      "Kent generally associates small initials with people;first,surname or pet-name possibilities remain open."
    ],
    "time_qualifications": [
      "comparatively_soon"
    ],
    "unresolved": [],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  },
  {
    "observation_id": "o2",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [
      "Kent treats a numeral beside dots as an amount in a money-related account;actual amount/currency/outcome is not verified."
    ],
    "time_qualifications": [],
    "unresolved": [
      "Declared qualitative region or under-handle relation"
    ],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  },
  {
    "observation_id": "o3",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [
      "Kent associates dots surrounding a symbol with money in a source-dependent form."
    ],
    "time_qualifications": [],
    "unresolved": [
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
"No person,calendar date,currency or actual gain inferred."
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
        "symbol_id": "letter",
        "mark": "M",
        "size": "small",
        "region": "rim"
      },
      {
        "id": "o2",
        "symbol_id": "numeral",
        "numeral": 90,
        "adjacent_to": [
          "o3"
        ]
      },
      {
        "id": "o3",
        "symbol_id": "dots",
        "arrangement": "surrounding"
      }
    ],
    "notes": "No person,calendar date,currency or actual gain inferred."
  },
  "input_sha256": "8d15c48c1b941943e8bbb529601fa552ac01fc7c53b5645440628952840b8814",
  "profile_sha256": "cc078f560bceca9d59296a29e99070e9f82059829eb2ee7501b926c90b658541",
  "source_sha256": "f6b4b81e04e81ba0efcd91228b76c143ac3b7262484d96f3b3d669d379839c56",
  "serialization": "Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw content line endings retained",
  "external_calls": false,
  "rng": false,
  "generated_placements": false
}
```
