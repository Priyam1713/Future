# Automatic Writing session

Profile: breton-bsb2016-writing-subset-v1

State: completed

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
  "state": "completed",
  "review_policy": "no_review",
  "user_record": {
    "intention": "A voluntary writing exercise."
  }
}
```

## Event timeline

```json
[
  {
    "event": {
      "id": "e0",
      "type": "begin",
      "timestamp": "2026-11-04T10:00:00Z"
    },
    "before": "prepared",
    "after": "writing",
    "provenance": "user_declared_event",
    "event_sha256": "78c0e20db1724818f3e01c19e8fead8b1510c40ee594a0f39bde1886b9d747eb"
  },
  {
    "event": {
      "id": "e1",
      "type": "append",
      "segment": {
        "id": "s1",
        "order": 1,
        "text": "The blue door opens.",
        "authorship": "user"
      }
    },
    "before": "writing",
    "after": "writing",
    "provenance": "user_declared_event",
    "event_sha256": "ee1d778d0f0c009fad34a7383e3f88e11d9a7908206632c9058e1a496e54cfae"
  },
  {
    "event": {
      "id": "e2",
      "type": "stop",
      "timestamp": "2026-11-04T10:02:00Z"
    },
    "before": "writing",
    "after": "stopped",
    "provenance": "user_declared_event",
    "event_sha256": "b3f473694d4280979b71621e15d7d2fddd18cef223514162884de6e66b1f604a"
  },
  {
    "event": {
      "id": "e3",
      "type": "complete"
    },
    "before": "stopped",
    "after": "completed",
    "provenance": "user_declared_event",
    "event_sha256": "37a7e415ef6dbc4ef892d88b253719dfe1bd93c195bfc9a1a1d9c8ee0e759392"
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
      "text": "The blue door opens.",
      "authorship": "user"
    },
    "event_id": "e1",
    "state": "writing",
    "content_sha256": "07aa358f71b8c53e15650048b6424c9348d1b629d1ff8631de6bf50ad1314ae1"
  }
]
```

## Original first draft

JSON string preserves exact whitespace and line endings:

```json
"The blue door opens."
```

Original content SHA256: b944f7315af2c122b80d8a2f9c9f572f49abd11ffbe3f7dadbcdab9432680033

## Separate revision history

## Objective metrics

```json
{
  "characters": 20,
  "unicode_code_points": 20,
  "words": 4,
  "lines": 1,
  "segments": 1,
  "pauses": 0,
  "interruptions": 0,
  "restarts": 0,
  "revisions": 0,
  "duration": {
    "seconds": 120.0,
    "microseconds": 120000000,
    "status": "declared_endpoints_only"
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
    "state": "completed",
    "events": [
      {
        "id": "e0",
        "type": "begin",
        "timestamp": "2026-11-04T10:00:00Z"
      },
      {
        "id": "e1",
        "type": "append",
        "segment": {
          "id": "s1",
          "order": 1,
          "text": "The blue door opens.",
          "authorship": "user"
        }
      },
      {
        "id": "e2",
        "type": "stop",
        "timestamp": "2026-11-04T10:02:00Z"
      },
      {
        "id": "e3",
        "type": "complete"
      }
    ],
    "intention": "A voluntary writing exercise.",
    "review_policy": "no_review"
  },
  "input_sha256": "df17eed3093c90bd2861c39202ccf9c63ac6eec3e8cc421cf64b4d7c3adac67c",
  "profile_sha256": "17c6c89d3c1fd64dccef8da6750c9e302b6597d237cc3480cd147ee172f6ed10",
  "serialization": "Canonical UTF8 sorted-key compact JSON, unescaped Unicode, no terminal LF; exact text line endings retained",
  "external_calls": false,
  "rng": false,
  "generated_text": false
}
```

