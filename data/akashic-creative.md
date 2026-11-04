# Akashic source reference and reflection

Profile: howe-public-reference-reflection-v1

2026 revised book metadata and public author pages are distinct materials. Earlier editions and book/page differences remain uncollated;no full-book coverage claimed.

## Source identity and rights

```json
[
  {
    "id": "akashic-howe-public-ppp-facts-v2",
    "technique_id": 26,
    "author": "Linda Howe",
    "edition": "The Pathway Prayer Process;public author webpage snapshot2026-11-04;not a page-concordant book edition",
    "url": "https://lindahowe.com/ppp/",
    "locator": "Opening Prayer and Closing Prayer;silent-stanza instruction and repeated closing declaration",
    "ingestion": "facts_only",
    "rights_note": "Copyrighted author page. Only original short factual paraphrases and structural counts retained;no protected prayer,exercise,case history or page corpus redistributed. Public access/printable link is not a redistribution license.",
    "checked_on": "2026-11-04",
    "snapshot_sha256": "995b30f49b5810a4fcd07417806358b972b63543ee6bcc2e241f912a600ac6c2",
    "snapshot_bytes": 84425
  },
  {
    "id": "akashic-howe-public-expectations-facts-v2",
    "technique_id": 26,
    "author": "Linda Howe",
    "edition": "Akashic Studies: Appropriate Expectations;public author webpage snapshot2026-11-04;not a page-concordant book edition",
    "url": "https://lindahowe.com/appropriate-expectations/",
    "locator": "For Practitioners;Issues we do not address;Keep in mind;For a person having a reading;Please Note",
    "ingestion": "facts_only",
    "rights_note": "Copyrighted author page. Only original short factual paraphrases and structural counts retained;no protected prayer,exercise,case history or page corpus redistributed. Public access/printable link is not a redistribution license.",
    "checked_on": "2026-11-04",
    "snapshot_sha256": "9554c61582faaad676f362621d6a9b7a794da68a7139096cc135c28b808c4737",
    "snapshot_bytes": 83625
  },
  {
    "id": "akashic-howe-public-book-facts-v2",
    "technique_id": 26,
    "author": "Linda Howe",
    "edition": "How to Read the Akashic Records, Revised & Updated author description;public author webpage snapshot2026-11-04;not a page-concordant book edition",
    "url": "https://lindahowe.com/how-to-read-the-akashic-records-by-linda-howe/",
    "locator": "Book description,process/roles/exercises bullets;not complete book text",
    "ingestion": "facts_only",
    "rights_note": "Copyrighted author page. Only original short factual paraphrases and structural counts retained;no protected prayer,exercise,case history or page corpus redistributed. Public access/printable link is not a redistribution license.",
    "checked_on": "2026-11-04",
    "snapshot_sha256": "30a2c0bfdf47ae7dfcb94e970a84a0eb585e7eadcd963dd90b11d59cde541096",
    "snapshot_bytes": 88262
  }
]
```

## User question and scope

```json
{
  "user_record": {
    "text": "  A🐍 Café\r\n猫 ",
    "purpose": "creative_imagination"
  },
  "effective_purpose": "creative_imagination",
  "status": "user_imagination",
  "answer": null,
  "intent_inferred": false,
  "form_guidance": "not_assessed"
}
```

## Source-located concepts

### records — source_reference

```json
{
  "id": "records",
  "status": "source_reference",
  "reference": {
    "id": "records",
    "description": "Howe portrays the Records as a spiritual archive concerning souls and human journeys.",
    "attribution": "Linda Howe public-page practitioner account",
    "provenance": {
      "source_id": "akashic-howe-public-book-facts-v2",
      "edition": "How to Read the Akashic Records, Revised & Updated author description;public author webpage snapshot2026-11-04;not a page-concordant book edition",
      "url": "https://lindahowe.com/how-to-read-the-akashic-records-by-linda-howe/",
      "locator": "Book description"
    },
    "conditions": [
      "Applies to this named public-page reference profile only;no personal facts inferred"
    ],
    "limitations": [
      "Practitioner cosmology,not an independently verified information store."
    ],
    "unsupported_claims": [
      "Objective metaphysical access or supernatural information verification"
    ]
  },
  "rule_id": "akashic.howe.records",
  "answer": null,
  "coverage": "Practitioner attribution only;not supernatural verification",
  "selection_reasons": [
    "editorial_mapping_of_declared_purpose"
  ]
}
```

### describe — source_reference

```json
{
  "id": "describe",
  "status": "source_reference",
  "reference": {
    "id": "describe",
    "description": "She recommends describing experience,including speech,writing or private thought.",
    "attribution": "Linda Howe public-page practitioner account",
    "provenance": {
      "source_id": "akashic-howe-public-expectations-facts-v2",
      "edition": "Akashic Studies: Appropriate Expectations;public author webpage snapshot2026-11-04;not a page-concordant book edition",
      "url": "https://lindahowe.com/appropriate-expectations/",
      "locator": "Keep in mind"
    },
    "conditions": [
      "Applies to this named public-page reference profile only;no personal facts inferred"
    ],
    "limitations": [
      "Recorded experiences stay user-attributed,not externally established facts."
    ],
    "unsupported_claims": [
      "Objective metaphysical access or supernatural information verification"
    ]
  },
  "rule_id": "akashic.howe.describe",
  "answer": null,
  "coverage": "Practitioner attribution only;not supernatural verification",
  "selection_reasons": [
    "editorial_mapping_of_declared_purpose"
  ]
}
```

## Source-aware question guidance

```json
{
  "evidence": "editorial_selection_of_source_references",
  "purpose_reference_ids": [
    "records",
    "describe"
  ],
  "form_reference_ids": [],
  "procedure": {
    "source_id": "akashic-howe-public-ppp-facts-v2",
    "url": "https://lindahowe.com/ppp/",
    "opening": {
      "silent_stanza_repetitions": 2,
      "locator": "Opening Prayer;silent-stanza instruction"
    },
    "closing": {
      "declaration_repetitions": 3,
      "locator": "Closing Prayer"
    },
    "prayer_reproduced": false,
    "caveat": "Public webpage structure only;no complete book procedure,ritual execution or access/closing verification. Link to original text if wanted;no invented substitute prayer."
  },
  "note": "These references describe source claims. They are not answers retrieved for the user;practitioner question restrictions do not establish supernatural access."
}
```

## Optional editorial reframing

```json
null
```

## Declared session stages

```json
{
  "user_record": {
    "state": "in_progress",
    "stages": [
      {
        "id": "notes",
        "status": "completed"
      }
    ]
  },
  "effective_state": "in_progress",
  "stage_reports": [
    {
      "user_declaration": {
        "id": "notes",
        "status": "completed"
      },
      "provenance": "editorial_application_tracking",
      "source_reference_ids": [
        "describe"
      ],
      "supernatural_compliance_verified": false
    }
  ],
  "unrecorded_stages": [
    "source_review",
    "preparation",
    "question",
    "concept_review",
    "finish",
    "reflection"
  ],
  "stage_origin": "All application stage tracking is editorial. preparation/finish link opening/closing facts but do not execute or certify a prayer.",
  "spiritual_records_opened": false,
  "spiritual_records_closed_verified": false
}
```

## User-supplied context

```json
{}
```

## User-attributed notes

```json
[
  {
    "user_record": {
      "id": "scene1",
      "kind": "imagined_scene",
      "text": "  A blue library\t\n",
      "uncertainty": true,
      "concept_ids": [
        "records"
      ]
    },
    "coverage": "user_attributed_imagined_scene",
    "references": [
      {
        "id": "records",
        "status": "source_reference",
        "reference": {
          "id": "records",
          "description": "Howe portrays the Records as a spiritual archive concerning souls and human journeys.",
          "attribution": "Linda Howe public-page practitioner account",
          "provenance": {
            "source_id": "akashic-howe-public-book-facts-v2",
            "edition": "How to Read the Akashic Records, Revised & Updated author description;public author webpage snapshot2026-11-04;not a page-concordant book edition",
            "url": "https://lindahowe.com/how-to-read-the-akashic-records-by-linda-howe/",
            "locator": "Book description"
          },
          "conditions": [
            "Applies to this named public-page reference profile only;no personal facts inferred"
          ],
          "limitations": [
            "Practitioner cosmology,not an independently verified information store."
          ],
          "unsupported_claims": [
            "Objective metaphysical access or supernatural information verification"
          ]
        },
        "rule_id": "akashic.howe.records",
        "answer": null,
        "coverage": "Practitioner attribution only;not supernatural verification"
      }
    ],
    "historical_record_retrieved": false
  },
  {
    "user_record": {
      "id": "association1",
      "kind": "association",
      "text": "My own association."
    },
    "coverage": "user_attributed_association",
    "references": [],
    "historical_record_retrieved": false
  }
]
```

## Unknowns and missing information

```json
{
  "application_observations": [
    "Optional background not supplied",
    "Optional focus not supplied"
  ],
  "user_declared": [],
  "permanent_limits": [
    "No independent verification of metaphysical records or source abilities",
    "Book/page procedure differences and other traditions remain incomplete"
  ]
}
```

## Documentary comparison coverage

```json
[]
```

## Editorial reflection questions

```json
[
  "What do I know from my own experience, and what remains uncertain?",
  "Which personal associations differ from the selected source description?"
]
```

## Provenance matrix

```json
{
  "direct": "Ten source-located practitioner concepts and public procedure structural facts only",
  "user_attributed": "Original question,background,focus,intention,notes,associations,imagined scenes and declared stages",
  "editorial": "Purpose/form mapping,reframing,stage tracking,missing-field observations and reflective questions",
  "unsupported": "Metaphysical access,hidden histories,verified past lives,predictions,deceased contact,clinical conclusions"
}
```

## Limits

```json
[
  "Actual metaphysical record access",
  "Hidden personal histories or externally verified past lives",
  "Predictions,deceased-person contact or clinical conclusions",
  "Fabricated retrieved records or source answers",
  "Unified Howe/Steiner/Cayce doctrine",
  "Source-backed means the author made the claim,not that the claimed archive exists.",
  "No prayer copied or invented;no legal name,religious commitment,altered state or experience required."
]
```

## Exact replay metadata

```json
{
  "request": {
    "schema_version": 1,
    "profile": "howe-public-reference-reflection-v1",
    "task": "reference_reflection",
    "mode": "manual",
    "question": {
      "text": "  A🐍 Café\r\n猫 ",
      "purpose": "creative_imagination"
    },
    "notes": [
      {
        "id": "scene1",
        "kind": "imagined_scene",
        "text": "  A blue library\t\n",
        "uncertainty": true,
        "concept_ids": [
          "records"
        ]
      },
      {
        "id": "association1",
        "kind": "association",
        "text": "My own association."
      }
    ],
    "session": {
      "state": "in_progress",
      "stages": [
        {
          "id": "notes",
          "status": "completed"
        }
      ]
    }
  },
  "input_sha256": "2aa405b8d26cb44a45079ab3a3750da64f5391d1173c0f0bf49373f20ed0940b",
  "profile_sha256": "1830aa54231ae1c8cdaaf7dc04e3fbf580c895530ac3cb72456983a16f7aaa83",
  "source_sha256": {
    "akashic-howe-public-ppp-facts-v2": "995b30f49b5810a4fcd07417806358b972b63543ee6bcc2e241f912a600ac6c2",
    "akashic-howe-public-expectations-facts-v2": "9554c61582faaad676f362621d6a9b7a794da68a7139096cc135c28b808c4737",
    "akashic-howe-public-book-facts-v2": "30a2c0bfdf47ae7dfcb94e970a84a0eb585e7eadcd963dd90b11d59cde541096"
  },
  "serialization": "Canonical UTF8 sorted-key compact JSON,unescaped Unicode,no final LF;raw text preserved with exact content line endings",
  "external_calls": false,
  "generated_narrative": false,
  "rng": false
}
```
