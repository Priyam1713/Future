# Automatic Writing session

Profile: breton-bsb2016-writing-subset-v1

State: stopped

## Historical procedure

André Breton1896-1966, Sainte-Barbe bibliography2016, PDFp4; French excerpt attributed to first Manifeste du surréalisme1924. Underlying print edition of quotation not identified; not authenticated against BnF manuscript.

[automatic-breton-bsb2016-french-subset-v1](https://www.bsb.univ-paris3.fr/images/docs/10196/andrebreton.pdf)

PDF/printedp4 French primary excerpt; bibliographyp6 lists Gallimard1985 without identifying it as quotation source

- Prepare writing materials. [automatic.breton.materials]

- Breton asks the writer to adopt a receptive or passive attitude. [automatic.breton.receptive]

- Set aside judgments about personal or others&#x27; literary talent. [automatic.breton.talent]

- Compose rapidly. [automatic.breton.rapid]

- Do not preselect a subject. [automatic.breton.unplanned]

- Avoid rereading during initial composition. [automatic.breton.no_rereading]

- Breton acknowledges a conscious contribution after the first sentence; the procedure is not proof of unconscious origin. [automatic.breton.qualification]

French rapid/unplanned/no-rereading and conscious-contribution instructions corroborate essential Seaver/Lane1969 transcription facts. Not a full textual collation or manuscript authentication. French excerpt omits the concentration-setting clause and later continuation/arbitrary-letter restart passage; these are not frozen French-subset rules.

French original, institutional PDF/images and Seaver/Lane1969 English translation have distinct rights. Original factual paraphrases only; no passage, scans, cover art or literary corpus redistributed. No blanket reproduction permission established.

## Editorial application conventions

```json
[
  "All session states/events, optional timestamps/constraints, interruption/restart controls, draft assembly, revisions, metrics and review questions are application conventions.",
  "Stop, pause or omit participation freely; no fixed historical duration, mental-state compliance score or mandatory restart technique.",
  "Revision is a separately labeled creative extension; does not retroactively change the first draft or claim fidelity to a historical first-and-last-draft ideal."
]
```

## Session declarations

```json
{
  "id": "sample",
  "state": "stopped",
  "review_policy": "optional",
  "user_record": {}
}
```

## Event timeline

```json
[
  {
    "event": {
      "id": "e0",
      "type": "begin",
      "timestamp": "2026-11-04T10:00:00"
    },
    "before": "prepared",
    "after": "writing",
    "provenance": "user_declared_event",
    "event_sha256": "9a52b34dc55401a1abc6faf2a7cbe00e06b33f646b7bfdee5e46e7734aeca8a1"
  },
  {
    "event": {
      "id": "e1",
      "type": "append",
      "segment": {
        "id": "s1",
        "order": 1,
        "text": "Unfinished",
        "authorship": "user"
      }
    },
    "before": "writing",
    "after": "writing",
    "provenance": "user_declared_event",
    "event_sha256": "d28effb98c0020aa249227cf739f9018a9b33cdfe82ed7831677e8aae58f9d39"
  },
  {
    "event": {
      "id": "e2",
      "type": "stop",
      "timestamp": "2026-11-04T10:01:00Z"
    },
    "before": "writing",
    "after": "stopped",
    "provenance": "user_declared_event",
    "event_sha256": "4c869182cd9de5c3621d880f80d23d7cc5e336217ba90a1185b068836bf4c6af"
  }
]
```

## Original writing segments

```json
[
  {
    "record": {
      "id": "s1",
      "order": 1,
      "text": "Unfinished",
      "authorship": "user"
    },
    "event_id": "e1",
    "state": "writing",
    "content_sha256": "af428a54f964c20e2b7bfd70aca273f9310da623beac8cae75c8a27d76f202a7"
  }
]
```

## Original first draft

JSON string preserves exact whitespace and line endings:

```json
"Unfinished"
```

Original content SHA256: 3929fee797de8fc03ba41f48e2acca10690d596dbb62489b788c1c3273f97ed3

## Separate revision history

## Objective metrics

```json
{
  "characters": 10,
  "unicode_code_points": 10,
  "words": 1,
  "lines": 1,
  "segments": 1,
  "pauses": 0,
  "interruptions": 0,
  "restarts": 0,
  "revisions": 0,
  "duration": {
    "seconds": null,
    "microseconds": null,
    "status": "unavailable_missing_or_incompatible_endpoints"
  },
  "declared_segment_seconds": null
}
```

## Metric conventions

```json
{
  "characters": "Python Unicode code points; no normalization or grapheme counting",
  "words": "Maximal nonempty runs separated by Python str.isspace Unicode whitespace; punctuation/emoji remain in tokens",
  "lines": "Empty text0; otherwise1 plus CRLF/CR/LF delimiters; CRLF is one delimiter, final empty line counted",
  "duration": "Begin-to-stop declared compatible datetime endpoints only; includes pauses; exact integer microseconds authoritative, seconds is a floating display; no inferred active typing time",
  "segment_intervals": "Sum only when every segment declares an integer interval; not inferred or equated to wall duration"
}
```

## Evidence layers

```json
{
  "direct": "Seven attributed Breton French-excerpt procedure facts only",
  "user_authored": "Raw events, segments, revisions, comments, constraints and associations",
  "editorial": "State machine, controls, hashes, metrics, review and revision model; constraints may differ from historical procedure",
  "unsupported": "Spirit contact, trance/unconscious-origin/authorship verification, diagnosis, hidden memories, future prediction"
}
```

## Editorial review questions

```json
[
  "Which first-draft passages do you choose to retain?",
  "What did you change during review, if anything?"
]
```

## Limits

```json
[
  "No source-specific spiritualist, ideomotor or stream-of-consciousness procedure implemented.",
  "Moses and Breton/Soupault exemplar remain separate; no generated writing, extraordinary authorship, diagnosis, hidden memories or predictions.",
  "Events and authorship are declarations, not mental-state or historical-compliance verification.",
  "Append-only validation applies within each supplied session log; no persistent database, authentication or cross-file tamper protection. Preserve replay files to retain versions."
]
```

## Exact replay metadata

```json
{
  "request": {
    "schema_version": 1,
    "profile": "breton-bsb2016-writing-subset-v1",
    "task": "guided_writing",
    "mode": "manual",
    "session_id": "sample",
    "state": "stopped",
    "events": [
      {
        "id": "e0",
        "type": "begin",
        "timestamp": "2026-11-04T10:00:00"
      },
      {
        "id": "e1",
        "type": "append",
        "segment": {
          "id": "s1",
          "order": 1,
          "text": "Unfinished",
          "authorship": "user"
        }
      },
      {
        "id": "e2",
        "type": "stop",
        "timestamp": "2026-11-04T10:01:00Z"
      }
    ]
  },
  "input_sha256": "b4e8ede8a52eef465bcfed33cfceff69c2561c83fbf36291dd43ca5e4cbf8eb3",
  "profile_sha256": "17c6c89d3c1fd64dccef8da6750c9e302b6597d237cc3480cd147ee172f6ed10",
  "serialization": "Canonical UTF8 sorted-key compact JSON, unescaped Unicode, no terminal LF; exact text line endings retained",
  "external_calls": false,
  "rng": false,
  "generated_text": false
}
```
