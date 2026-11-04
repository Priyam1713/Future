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

### o1 — conflicting_evidence

```json
{
  "id": "o1",
  "user_record": {
    "id": "o1",
    "symbol_id": "aircraft",
    "motion": "stationary",
    "heading": "towards_handle",
    "alternatives": [
      "apron"
    ],
    "region": "side",
    "region_alternatives": [
      "bottom"
    ],
    "uncertainty": true
  },
  "status": "conflicting_evidence",
  "reference": {
    "id": "aircraft",
    "name": "Aircraft",
    "aliases": [],
    "definition": "Directional/motion-dependent account;no unconditional outcome.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "Dictionary A:Aircraft",
    "alternatives": [],
    "cases": [
      {
        "id": "approaching",
        "statement": "Kent associates approaching flight with rapid news or an unexpected journey.",
        "requires": {
          "motion": "flying",
          "heading": "towards_handle"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Aircraft"
      },
      {
        "id": "stationary",
        "statement": "Kent associates a stationary aircraft with limited success unless habits change.",
        "requires": {
          "motion": "stationary"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Aircraft"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "approaching",
        "statement": "Kent associates approaching flight with rapid news or an unexpected journey.",
        "requires": {
          "motion": "flying",
          "heading": "towards_handle"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Aircraft"
      },
      "status": "not_applicable",
      "intrinsic_status": "not_applicable",
      "condition_results": {
        "motion": "not_applicable",
        "heading": "applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.aircraft.approaching",
      "forecast": false
    },
    {
      "reference": {
        "id": "stationary",
        "statement": "Kent associates a stationary aircraft with limited success unless habits change.",
        "requires": {
          "motion": "stationary"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary A:Aircraft"
      },
      "status": "conflicting_evidence",
      "intrinsic_status": "applicable",
      "condition_results": {
        "motion": "applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.aircraft.stationary",
      "forecast": false
    }
  ],
  "zones": {
    "status": "conflicting_evidence",
    "qualifications": [
      {
        "region": "side",
        "association": "more_distant",
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChII:handle,near-rim,sides,bottom and intuitive timing qualification"
      },
      {
        "region": "bottom",
        "association": "far_distant",
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "ChII:handle,near-rim,sides,bottom and intuitive timing qualification"
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
    "Uncertain or competing manual symbol identities;no identity selected automatically",
    "Stationary motion and directional heading remain conflicting declarations",
    "Coexisting depth/handle timing qualifications;no source priority or exact date inferred"
  ],
  "alternative_references": [
    {
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
    }
  ],
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
    "source_accounts": [],
    "time_qualifications": [
      "more_distant",
      "far_distant"
    ],
    "unresolved": [
      "Uncertain or competing manual symbol identities;no identity selected automatically",
      "Stationary motion and directional heading remain conflicting declarations",
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
        "symbol_id": "aircraft",
        "motion": "stationary",
        "heading": "towards_handle",
        "alternatives": [
          "apron"
        ],
        "region": "side",
        "region_alternatives": [
          "bottom"
        ],
        "uncertainty": true
      }
    ]
  },
  "input_sha256": "a4e4a13491b7f6bd88564d293f596e9238aec8bbd42beeb6d143e36a4dca0e9d",
  "profile_sha256": "cc078f560bceca9d59296a29e99070e9f82059829eb2ee7501b926c90b658541",
  "source_sha256": "f6b4b81e04e81ba0efcd91228b76c143ac3b7262484d96f3b3d669d379839c56",
  "serialization": "Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw content line endings retained",
  "external_calls": false,
  "rng": false,
  "generated_placements": false
}
```
