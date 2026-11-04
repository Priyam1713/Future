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
    "musician": true
  }
}
```

## Ordered manual placements

### f0 — applicable

```json
{
  "id": "f0",
  "user_record": {
    "symbol_id": "coal_scoop",
    "size": "small",
    "region": "unknown",
    "id": "f0"
  },
  "status": "applicable",
  "reference": {
    "id": "coal_scoop",
    "name": "Coal scoop",
    "aliases": [],
    "definition": "Only a FigureVIII documentary account is supported;do not substitute Coal Scuttle.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "Example Cups FigureVIII:interpretation/principal symbols",
    "alternatives": [],
    "cases": [
      {
        "id": "figure_viii_domestic",
        "statement": "FigureVIII groups coal scoop and beetle with domestic worries/cares.",
        "requires": {},
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Example Cups FigureVIII:interpretation/principal symbols",
        "scope": "figure_viii"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "figure_viii_domestic",
        "statement": "FigureVIII groups coal scoop and beetle with domestic worries/cares.",
        "requires": {},
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Example Cups FigureVIII:interpretation/principal symbols",
        "scope": "figure_viii"
      },
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {
        "FigureVIII beetle present": "applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.coal_scoop.figure_viii_domestic",
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

### f1 — applicable

```json
{
  "id": "f1",
  "user_record": {
    "symbol_id": "organ",
    "region": "bottom_circle",
    "id": "f1"
  },
  "status": "applicable",
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
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {
        "context.musician": "applicable"
      },
      "missing": [],
      "rule_id": "tasseography.kent.organ.musician",
      "forecast": false
    }
  ],
  "zones": {
    "status": "applicable",
    "qualifications": [
      {
        "region": "bottom_circle",
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

### f2 — applicable

```json
{
  "id": "f2",
  "user_record": {
    "symbol_id": "acorn",
    "region": "bottom_circle",
    "id": "f2",
    "adjacent_to": [
      "f1"
    ]
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
        "region": "bottom_circle",
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

### f3 — applicable

```json
{
  "id": "f3",
  "user_record": {
    "symbol_id": "beetle",
    "region": "bottom_circle",
    "id": "f3"
  },
  "status": "applicable",
  "reference": {
    "id": "beetle",
    "name": "Beetle",
    "aliases": [],
    "definition": "Domestic unrest/disagreement;several add an account about supposed friends.",
    "source_id": "tasseography-kent-pg6964-cup-facts-v2",
    "locator": "Dictionary B:Beetle",
    "alternatives": [],
    "cases": [
      {
        "id": "general",
        "statement": "Kent associates beetle with unrest,household trouble or disagreement.",
        "requires": {},
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary B:Beetle"
      },
      {
        "id": "several",
        "statement": "Kent associates several beetles with risk of slander by supposed friends.",
        "requires": {
          "multiplicity": "several"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary B:Beetle"
      }
    ]
  },
  "cases": [
    {
      "reference": {
        "id": "general",
        "statement": "Kent associates beetle with unrest,household trouble or disagreement.",
        "requires": {},
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary B:Beetle"
      },
      "status": "applicable",
      "intrinsic_status": "applicable",
      "condition_results": {},
      "missing": [],
      "rule_id": "tasseography.kent.beetle.general",
      "forecast": false
    },
    {
      "reference": {
        "id": "several",
        "statement": "Kent associates several beetles with risk of slander by supposed friends.",
        "requires": {
          "multiplicity": "several"
        },
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Dictionary B:Beetle"
      },
      "status": "insufficient_information",
      "intrinsic_status": "insufficient_information",
      "condition_results": {
        "multiplicity": "insufficient_information"
      },
      "missing": [
        "multiplicity"
      ],
      "rule_id": "tasseography.kent.beetle.several",
      "forecast": false
    }
  ],
  "zones": {
    "status": "applicable",
    "qualifications": [
      {
        "region": "bottom_circle",
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

### f4 — insufficient_information

```json
{
  "id": "f4",
  "user_record": {
    "symbol_id": "tea_cosy",
    "region": "bottom_centre",
    "id": "f4"
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
    "status": "applicable",
    "qualifications": [
      {
        "region": "bottom_centre",
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

## Editorial symbolic synthesis

```json
[
  {
    "observation_id": "f0",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [
      "FigureVIII groups coal scoop and beetle with domestic worries/cares."
    ],
    "time_qualifications": [],
    "unresolved": [
      "Declared qualitative region or under-handle relation"
    ],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  },
  {
    "observation_id": "f1",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [
      "Kent gives an achievement account for a musician."
    ],
    "time_qualifications": [
      "far_distant"
    ],
    "unresolved": [],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  },
  {
    "observation_id": "f2",
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
  },
  {
    "observation_id": "f3",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [
      "Kent associates beetle with unrest,household trouble or disagreement."
    ],
    "time_qualifications": [
      "far_distant"
    ],
    "unresolved": [
      "multiplicity"
    ],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  },
  {
    "observation_id": "f4",
    "evidence": "editorial_composition_of_source_and_user_declarations",
    "source_accounts": [],
    "time_qualifications": [
      "far_distant"
    ],
    "unresolved": [
      "context.marital_status"
    ],
    "note": "Historically attributed accounts under declared conditions;not an actual event prediction."
  }
]
```

## Coverage summary

```json
{
  "observations": 5,
  "counts": {
    "applicable": 4,
    "not_applicable": 0,
    "insufficient_information": 1,
    "conflicting_evidence": 0,
    "unsupported": 0
  },
  "text": "Each source account is evaluated against explicit manual conditions. Depth and handle timing remain separate;missing or competing evidence is not repaired."
}
```

## Original Kent example comparison

```json
{
  "coverage": "explicit_documentary_comparison",
  "reference": {
    "id": "figure_viii",
    "locator": "Example Cups FigureVIII:interpretation/principal symbols",
    "placements": [
      {
        "symbol_id": "coal_scoop",
        "size": "small",
        "region": "unknown"
      },
      {
        "symbol_id": "organ",
        "region": "bottom_circle"
      },
      {
        "symbol_id": "acorn",
        "region": "bottom_circle",
        "beside": "organ"
      },
      {
        "symbol_id": "beetle",
        "region": "bottom_circle"
      },
      {
        "symbol_id": "tea_cosy",
        "region": "bottom_centre"
      }
    ],
    "accounts": [
      "Organ/acorn on lower circle:delayed hope/ultimate success account",
      "Musician condition:professional success account",
      "Coal scoop/beetle:household worries",
      "Tea cosy centrally:compensating affection/comfort"
    ],
    "limits": "Documentary comparison only when explicitly requested;not a generally applicable universal organ/acorn grammar. Dictionary marital/organ alternatives remain separate."
  },
  "placement_checks": [
    {
      "expected": {
        "symbol_id": "coal_scoop",
        "size": "small",
        "region": "unknown"
      },
      "status": "declared_fields_match",
      "original_shape_recognition": false
    },
    {
      "expected": {
        "symbol_id": "organ",
        "region": "bottom_circle"
      },
      "status": "declared_fields_match",
      "original_shape_recognition": false
    },
    {
      "expected": {
        "symbol_id": "acorn",
        "region": "bottom_circle",
        "beside": "organ"
      },
      "status": "declared_fields_match",
      "original_shape_recognition": false
    },
    {
      "expected": {
        "symbol_id": "beetle",
        "region": "bottom_circle"
      },
      "status": "declared_fields_match",
      "original_shape_recognition": false
    },
    {
      "expected": {
        "symbol_id": "tea_cosy",
        "region": "bottom_centre"
      },
      "status": "declared_fields_match",
      "original_shape_recognition": false
    }
  ],
  "cases": [
    {
      "reference": {
        "id": "pair",
        "requires": {
          "adjacent_pair": [
            "organ",
            "acorn"
          ],
          "both_region": "bottom_circle"
        },
        "statement": "FigureVIII compares the adjacent lower-circle organ/acorn with delayed hope and eventual success.",
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Example Cups FigureVIII:interpretation/principal symbols"
      },
      "rule_id": "tasseography.kent.figure_viii.pair",
      "status": "applicable"
    },
    {
      "reference": {
        "id": "musician",
        "requires": {
          "adjacent_pair": [
            "organ",
            "acorn"
          ],
          "both_region": "bottom_circle",
          "musician": true
        },
        "statement": "The FigureVIII musician-specific professional-success account applies only as a historical comparison to the declared musician context.",
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Example Cups FigureVIII:interpretation/principal symbols"
      },
      "rule_id": "tasseography.kent.figure_viii.musician",
      "status": "applicable"
    },
    {
      "reference": {
        "id": "cosy",
        "requires": {
          "symbol": "tea_cosy",
          "region": "bottom_centre"
        },
        "statement": "FigureVIII central tea cosy is described as compensating small comforts and affection,independently of unprovided marital context.",
        "source_id": "tasseography-kent-pg6964-cup-facts-v2",
        "locator": "Example Cups FigureVIII:interpretation/principal symbols"
      },
      "rule_id": "tasseography.kent.figure_viii.cosy",
      "status": "applicable"
    }
  ],
  "adjacency_convention": "Original beside-organ placement is checked through explicit user adjacency;not inferred from circle membership.",
  "assurance": "Source example account compared with user declarations,not a newly published historical cup or verified fortune. Dictionary contexts remain separate."
}
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
"Original Kent FigureVIII comparison from independently transcribed source facts;not a synthetic cup advertised as historical."
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
        "symbol_id": "coal_scoop",
        "size": "small",
        "region": "unknown",
        "id": "f0"
      },
      {
        "symbol_id": "organ",
        "region": "bottom_circle",
        "id": "f1"
      },
      {
        "symbol_id": "acorn",
        "region": "bottom_circle",
        "id": "f2",
        "adjacent_to": [
          "f1"
        ]
      },
      {
        "symbol_id": "beetle",
        "region": "bottom_circle",
        "id": "f3"
      },
      {
        "symbol_id": "tea_cosy",
        "region": "bottom_centre",
        "id": "f4"
      }
    ],
    "source_example": "figure_viii",
    "context": {
      "musician": true
    },
    "notes": "Original Kent FigureVIII comparison from independently transcribed source facts;not a synthetic cup advertised as historical."
  },
  "input_sha256": "356c955e0c54e6ad35e9e832625246bc4283860eacade0b06b29c01d7ec684eb",
  "profile_sha256": "cc078f560bceca9d59296a29e99070e9f82059829eb2ee7501b926c90b658541",
  "source_sha256": "f6b4b81e04e81ba0efcd91228b76c143ac3b7262484d96f3b3d669d379839c56",
  "serialization": "Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no terminal LF;raw content line endings retained",
  "external_calls": false,
  "rng": false,
  "generated_placements": false
}
```
