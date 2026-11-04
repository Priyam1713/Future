# Dream — historical andreflective interpretation

Profile: artemidorus-attalus-context-v1

Historical accounts below are attributed references,not predictions ordiagnoses.

## Original user record

```json
{
  "coverage": "user_attributed",
  "record": {
    "timestamp": "2026-11-04T18:30:00+05:30",
    "scenes": [
      {
        "sequence": 1,
        "description": "I drank from a cup.",
        "objects": [
          "cup"
        ]
      },
      {
        "sequence": 2,
        "description": "A serpent crossed the path.",
        "uncertainty": true
      }
    ],
    "context": {
      "thirsty": true
    }
  },
  "narrative_state": "missing",
  "scene_order": "input list;never sorted"
}
```

Scene 1 verbatim:

```text
I drank from a cup.
```

Scene 2 verbatim:

```text
A serpent crossed the path.
```

## Historical taxonomy

Stable Greek/transliterated category IDs avoid the differing English dream/vision labels inmodern translations. GreekBook1.1/1.2 terms inspected;not a full original-language collation.

- enypnion ἐνύπνιον: Present-state experience during sleep in the author&#x27;s framework;not a forecast. Status: conditional_historical_comparison.

Source: dream-artemidorus-attalus-context-facts-v1; Oneirocritica 1.1; Naphtali Lewis1976; dream.artemidorus.category.enypnion.

Missing/limits: No additional selected-case condition;predictive validity remains unverified

- oneiros ὄνειρος: The author&#x27;s future-signifying class;the application cannot verify predictive significance. Status: undetermined.

Source: dream-artemidorus-attalus-context-facts-v1; Oneirocritica 1.1; Naphtali Lewis1976; dream.artemidorus.category.oneiros.

Missing/limits: predictive significance cannot be established by this application

- theorematic θεωρηματικοί: Within oneiros,the represented form directly corresponds to an event in the historical account. Status: undetermined.

Source: dream-artemidorus-attalus-context-facts-v1; Oneirocritica 1.2; Robert J.White1975; dream.artemidorus.category.theorematic.

Missing/limits: user-reported exact correspondence;not independently verified

- allegorical ἀλληγορικοί: Within oneiros,one thing is represented through another in the author&#x27;s theory. Status: undetermined.

Source: dream-artemidorus-attalus-context-facts-v1; Oneirocritica 1.2; Robert J.White1975; dream.artemidorus.category.allegorical.

Missing/limits: No additional selected-case condition;predictive validity remains unverified

Classification conflicts: none

## Historical context qualifications

- Common andindividual/cultural customs can change a reading;the author&#x27;s generalizations are historical claims. [dream-artemidorus-attalus-context-facts-v1; Oneirocritica 1.8; dream.artemidorus.1_8]

- Circumstances andsmall narrative details matter;the app makes all such context optional andnever invents it. [dream-artemidorus-attalus-context-facts-v1; Oneirocritica 1.9; dream.artemidorus.1_9]

## Explicit motif references

### drinking — conditional_reference

The thirsty person&#x27;s drinking dream is treated as an echo of present need.

Source: dream-artemidorus-attalus-context-facts-v1; Oneirocritica 1.1; Naphtali Lewis1976; dream.artemidorus.motif.drinking.

Historical case present_state: The thirsty person&#x27;s drinking dream is treated as an echo of present need.

Case conditions anduser evidence:

```json
{
  "motif_id": "drinking",
  "status": "conditional_reference",
  "reference": {
    "id": "drinking",
    "provenance": {
      "source_id": "dream-artemidorus-attalus-context-facts-v1",
      "locator": "Oneirocritica 1.1",
      "translator": "Naphtali Lewis1976",
      "rule_id": "dream.artemidorus.1_1",
      "version": 1
    },
    "condition_kind": "boolean",
    "cases": [
      {
        "id": "present_state",
        "requires": {
          "thirsty": true
        },
        "historical_account": "The thirsty person's drinking dream is treated as an echo of present need.",
        "category": "enypnion"
      }
    ],
    "definition": "The thirsty person's drinking dream is treated as an echo of present need.",
    "coverage": "bounded_historical_reference",
    "forecast": false
  },
  "selected_cases": [
    {
      "id": "present_state",
      "requires": {
        "thirsty": true
      },
      "historical_account": "The thirsty person's drinking dream is treated as an echo of present need.",
      "category": "enypnion"
    }
  ],
  "provided_context": {
    "thirsty": true
  },
  "missing_context": [],
  "not_met": [],
  "rule_id": "dream.artemidorus.motif.drinking",
  "interpretation_scope": "Author-attributed historical reference only;not an event forecast ordiagnosis",
  "forecast": false
}
```

## Manual annotations

```json
[]
```

## Editorial comparison

1 explicit historical lookups;1 fit declared case conditions,0 lack context. These are source comparisons,not forecasts. User associations remain separate.

- What meanings do you personally give your recorded details?

- Which details remain uncertain or incomplete?

## Source scope andlimits

Historical omen accounts are not empirically validated forecasts No diagnosis,hidden-memory inference,latent-wish analysis oruniversal symbol dictionary All personal/cultural/situational facts are optional,user declared andnot inferred fromnarrative words Freud,Jung,Faraday andother cultural dictionaries remain separate unsupported profiles Automatic literal tagging deferred;manual exact-span annotations only;no external calls,LLM orclock

[Selected historical excerpts](https://www.attalus.org/translate/artemidorus.html)

[Greek terminology witness](https://www.tha.de/~harsch/graeca/Chronologia/S_post02/Artemidor/art_oni1.html)

Ancient work andmodern White/Lewis translations/site rendering have separate rights. Only original short factual research paraphrases,category/motif facts andlocators retained;no translated passage,whole corpus orsite assets copied. No blanket translation reproduction permission claimed.

## Exact replay metadata

```json
{
  "request": {
    "schema_version": 1,
    "profile": "artemidorus-attalus-context-v1",
    "task": "historical_reflection",
    "mode": "manual",
    "scenes": [
      {
        "sequence": 1,
        "description": "I drank from a cup.",
        "objects": [
          "cup"
        ]
      },
      {
        "sequence": 2,
        "description": "A serpent crossed the path.",
        "uncertainty": true
      }
    ],
    "timestamp": "2026-11-04T18:30:00+05:30",
    "lookups": [
      "drinking"
    ],
    "context": {
      "thirsty": true
    }
  },
  "profile": "artemidorus-attalus-context-v1",
  "profile_sha256": "85149f9759a16cd724d089d48ecc7d75b1027c6e0dcdade555c2c157b0cb4847",
  "source_snapshot_sha256": "66f52323cbd6783c53f45b2c3db9ae5157a01b5798f7f7b714ebb1f61873c072",
  "policy": "artemidorus-explicit-context-v1",
  "annotations": "manual-codepoint-spans-v1",
  "clock_used": false,
  "automatic_matching": false,
  "external_calls": false
}
```

