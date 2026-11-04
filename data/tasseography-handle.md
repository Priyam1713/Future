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
  "context": {
    "abode": "away"
  }
}
```

## Ordered manual placements

### o1 — conflicting_evidence

```json
{
  "id": "o1",
  "user_record": {
    "id": "o1",
    "symbol_id": "cross",
    "region": "bottom",
    "handle_relation": "under_handle",
    "size": "small",
    "multiplicity": "single"
  },
  "status": "conflicting_evidence",
  "reference": {
    "id": "cross",
    "name": "Cross",
    "aliases": [],
    "definition": "Obstacles/misfortune account with a specific small-bottom qualification.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "Dictionary C:Cross;ChIII:small cross at bottom",
    "alternatives": [],
    "cases": [
      {
        "id": "general",
        "statement": "Kent associates cross with hindrance,sorrow or misfortune.",
        "requires": {},
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary C:Cross;ChIII:small cross at bottom"
      },
      {
        "id": "small_bottom",
        "statement": "Kent gives a trifling delay/vexation account for a lone small cross at the bottom.",
        "requires": {
          "size": "small",
          "multiplicity": "single",
          "bottom_region": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChIII:small single cross at bottom"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "general",
        "statement": "Kent associates cross with hindrance,sorrow or misfortune.",
        "requires": {},
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary C:Cross;ChIII:small cross at bottom"
      },
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {},
      "missing": [],
      "rule_id": "tasseography.kent.cross.general",
      "forecast": false
    },
    {
      "reference": {
        "id": "small_bottom",
        "statement": "Kent gives a trifling delay/vexation account for a lone small cross at the bottom.",
        "requires": {
          "size": "small",
          "multiplicity": "single",
          "bottom_region": true
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChIII:small single cross at bottom"
      },
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {
        "size": "applicable",
        "multiplicity": "applicable",
        "bottom_region": "applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.cross.small_bottom",
      "forecast": false
    }
  ],
  "zones": {
    "status": "conflicting_evidence",
    "qualifications": [
      {
        "region": "bottom",
        "association": "far_distant",
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChII:handle,near-rim,sides,bottom and intuitive timing qualification"
      },
      {
        "region": "under_handle",
        "association": "present_immediate",
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChII:directly beneath handle"
      }
    ],
    "conflicts": [
      "Coexisting depth/handle timing qualifications;no source priority or exact date inferred"
    ],
    "missing": [],
    "calendar_date": null,
    "handle_reference": "ChII:handle represents consultant,home or current abode when away;directly underneath denotes present/immediate circumstances.",
    "convention": "bottom_circle/bottom_centre are named subregions of source bottom,retaining FigureVIII circle/centre labels. No numeric boundaries,absolute dates or priority over under-handle present/immediate qualification."
  },
  "missing": [],
  "conflicts": [
    "Coexisting depth/handle timing qualifications;no source priority or exact date inferred"
  ],
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
      "Kent associates cross with hindrance,sorrow or misfortune.",
      "Kent gives a trifling delay/vexation account for a lone small cross at the bottom."
    ],
    "time_qualifications": [
      "far_distant",
      "present_immediate"
    ],
    "unresolved": [
      "Coexisting depth/handle timing qualifications;no source priority or exact date inferred"
    ],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  }
]
```

## Coverage summary

```json
{
  "observations": 1,
  "counts": {
    "applicable": 0,
    "not_applicable": 0,
    "insufficient_information": 0,
    "conflicting_evidence": 1,
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
        "symbol_id": "cross",
        "region": "bottom",
        "handle_relation": "under_handle",
        "size": "small",
        "multiplicity": "single"
      }
    ],
    "context": {
      "abode": "away"
    }
  },
  "input_sha256": "78d3e60ada1ec98359770348a33b5a574e0f91cde61e34423669cf6cdb46b2c3",
  "profile_sha256": "cc078f560bceca9d59296a29e99070e9f82059829eb2ee7501b926c90b658541",
  "source_sha256": "f6b4b81e04e81ba0efcd91228b76c143ac3b7262484d96f3b3d669d379839c56",
  "serialization": "Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw content line endings retained",
  "external_calls": false,
  "rng": false,
  "generated_placements": false
}
```
