# Bibliomancy: edition-pinned manual passage selection

Digital manual coarse-selection adaptation; one editorial shelf, one complete book, chapter logical pages and curated sentence units. No physical dice simulation or random draw.

Profile: mascaro2022-manual-coarse-webclassic-ruth-v1

## RUT.1.s030

[Ruth 1:16](https://ebible.org/eng-web/RUT01.htm#V16) — editorial logical page 2; path [1, 1, 2, 30]

```json
{
  "exact_source_text": "Your people will be my people, and your God my God.",
  "context_before": [
    {
      "sentence_id": "RUT.1.s028",
      "text": "Follow your sister-in-law.”",
      "verse_ids": [
        "RUT.1.15"
      ],
      "citation": "Ruth 1:15",
      "source_url": "https://ebible.org/eng-web/RUT01.htm#V15",
      "source_span": {
        "start": 2084,
        "end": 2111,
        "unit": "Unicode codepoints; half-open normalized chapter stream"
      }
    },
    {
      "sentence_id": "RUT.1.s029",
      "text": "Ruth said, “Don’t urge me to leave you, and to return from following you, for where you go, I will go; and where you stay, I will stay.",
      "verse_ids": [
        "RUT.1.16"
      ],
      "citation": "Ruth 1:16",
      "source_url": "https://ebible.org/eng-web/RUT01.htm#V16",
      "source_span": {
        "start": 2112,
        "end": 2247,
        "unit": "Unicode codepoints; half-open normalized chapter stream"
      }
    }
  ],
  "context_after": [
    {
      "sentence_id": "RUT.1.s031",
      "text": "Where you die, I will die, and there I will be buried.",
      "verse_ids": [
        "RUT.1.17"
      ],
      "citation": "Ruth 1:17",
      "source_url": "https://ebible.org/eng-web/RUT01.htm#V17",
      "source_span": {
        "start": 2300,
        "end": 2354,
        "unit": "Unicode codepoints; half-open normalized chapter stream"
      }
    },
    {
      "sentence_id": "RUT.1.s032",
      "text": "May Yahweh do so to me, and more also, if anything but death parts you and me.”",
      "verse_ids": [
        "RUT.1.17"
      ],
      "citation": "Ruth 1:17",
      "source_url": "https://ebible.org/eng-web/RUT01.htm#V17",
      "source_span": {
        "start": 2355,
        "end": 2434,
        "unit": "Unicode codepoints; half-open normalized chapter stream"
      }
    }
  ]
}
```

## Source procedure

```json
{
  "id": "bibliomancy-mascaro2022-audit-v1",
  "technique_id": 36,
  "rank": 2,
  "author": "J. R. Mascaro / Llewellyn Worldwide",
  "edition": "A Sorcerer in the Library: An Introduction to Integer Bibliomancy; December12,2022",
  "url": "https://www.llewellyn.com/journal/print.php?id=3066",
  "locator": "Paragraphs beginning Integer bibliomancy differs; The first step; If you are enacting; The next step; You will now; Upon selecting; Next; In the fine method",
  "ingestion": "facts_only",
  "rights_note": "Copyrighted modern practitioner article. Conditional free-website article republication policy is not a general software/corpus licence. Independently worded procedural facts only; no complete article or proprietary book text bundled.",
  "checked_on": "2026-11-06",
  "snapshot_sha256": null,
  "access": "Publisher-origin search-index rendering inspected; direct requests403. Fresh exact HTML source freeze still required before executable extraction."
}
```

## Corpus edition and rights

```json
{
  "id": "webclassic2020-ruth-v1",
  "version": 1,
  "title": "The Book of Ruth — World English Bible Classic",
  "edition": "World English Bible Classic,2020 stable American-English text; complete Book of Ruth, four chapter HTML witnesses downloaded2026-11-06",
  "source": {
    "id": "bibliomancy-webclassic-ruth-corpus-v1",
    "technique_id": 36,
    "rank": null,
    "author": "World English Bible translation contributors / eBible.org; ancient Book of Ruth author not independently identified",
    "edition": "World English Bible Classic,2020 stable American-English text; complete Book of Ruth, four chapter HTML witnesses downloaded2026-11-06",
    "url": "https://ebible.org/details.php?id=eng-web",
    "ingestion": "public_domain_text",
    "rights_note": "Publisher explicitly dedicates WEB translation to public domain. World English Bible trademark identifies faithful copies; editorial indexing is labeled separately, source wording/punctuation unchanged. Only complete Ruth subset supported, not whole canon.",
    "rights_url": "https://ebible.org/eng-web/copyright.htm",
    "checked_on": "2026-11-06",
    "rights_snapshot_sha256": "2e62eca4b32541181eff0917becbbc14213fba3ba417246e315bae9e4a6aaa35",
    "edition_snapshot_sha256": "65dbdf4333b99709c5ab65c5e4077f8d65338fc7638754298018fe35b66e2cf5"
  },
  "normalization": "Decode HTML entities; exclude verse labels, footnote marks/content, navigation, title headings and footer from selectable narrative. Collapse Unicode whitespace to one ASCII space; join consecutive verses with one ASCII space. No Unicode normalization, spelling or punctuation change. Retain exact raw HTML independently.",
  "scope": "Complete Ruth only:85 native verses,141 sentence units; not a full Bible or historical Christian lots procedure"
}
```

## Index boundaries

```json
{
  "id": "webclassic2020-ruth-sentences-v1",
  "version": 1,
  "ordering": "One shelf and one complete book; title-only logical page first, then chapters1–4. Source order within each chapter. One-based caller indices differ from stable IDs and native chapter/verse labels.",
  "boundaries": "141 manually reviewed punctuation-based sentence units. Speaker introductions remain attached. Closing quotation marks, including spaced nested closers, remain with the preceding terminal punctuation. A standalone unit need not contain a matching opening/closing quote; bounded neighboring context retains surrounding dialogue. Not a universal tokenizer.",
  "cross_page": "Content logical pages correspond to complete source chapters. All four end at sentence boundaries; no split sentence or cross-chapter unit. Future corpora crossing page boundaries require separately frozen ownership/ineligibility. Context never crosses chapter logical page.",
  "empty_page": "Title-only logical page1 contains genuine source heading, zero selectable sentences and explicit rejection. This is an editorial digital grouping, not a historical blank printed page.",
  "abbreviation": "Manual review found no abbreviation requiring an internal-full-stop exception in this Ruth subset. No general abbreviation/tokenizer support claimed."
}
```

## Complete selections and raw per-selection reflections

```json
[
  {
    "sentence_id": "RUT.1.s030",
    "text": "Your people will be my people, and your God my God.",
    "verse_ids": [
      "RUT.1.16"
    ],
    "citation": "Ruth 1:16",
    "source_url": "https://ebible.org/eng-web/RUT01.htm#V16",
    "source_span": {
      "start": 2248,
      "end": 2299,
      "unit": "Unicode codepoints; half-open normalized chapter stream"
    },
    "path": [
      1,
      1,
      2,
      30
    ],
    "stable_path": [
      "webclassic-ruth",
      "RUT",
      "ruth-chapter-1",
      "RUT.1.s030"
    ],
    "logical_page": {
      "index": 2,
      "id": "ruth-chapter-1",
      "label": "Editorial chapter logical page: Ruth1",
      "editorial": true,
      "printed_page": null,
      "native_chapter": 1
    },
    "context_before": [
      {
        "sentence_id": "RUT.1.s028",
        "text": "Follow your sister-in-law.”",
        "verse_ids": [
          "RUT.1.15"
        ],
        "citation": "Ruth 1:15",
        "source_url": "https://ebible.org/eng-web/RUT01.htm#V15",
        "source_span": {
          "start": 2084,
          "end": 2111,
          "unit": "Unicode codepoints; half-open normalized chapter stream"
        }
      },
      {
        "sentence_id": "RUT.1.s029",
        "text": "Ruth said, “Don’t urge me to leave you, and to return from following you, for where you go, I will go; and where you stay, I will stay.",
        "verse_ids": [
          "RUT.1.16"
        ],
        "citation": "Ruth 1:16",
        "source_url": "https://ebible.org/eng-web/RUT01.htm#V16",
        "source_span": {
          "start": 2112,
          "end": 2247,
          "unit": "Unicode codepoints; half-open normalized chapter stream"
        }
      }
    ],
    "context_after": [
      {
        "sentence_id": "RUT.1.s031",
        "text": "Where you die, I will die, and there I will be buried.",
        "verse_ids": [
          "RUT.1.17"
        ],
        "citation": "Ruth 1:17",
        "source_url": "https://ebible.org/eng-web/RUT01.htm#V17",
        "source_span": {
          "start": 2300,
          "end": 2354,
          "unit": "Unicode codepoints; half-open normalized chapter stream"
        }
      },
      {
        "sentence_id": "RUT.1.s032",
        "text": "May Yahweh do so to me, and more also, if anything but death parts you and me.”",
        "verse_ids": [
          "RUT.1.17"
        ],
        "citation": "Ruth 1:17",
        "source_url": "https://ebible.org/eng-web/RUT01.htm#V17",
        "source_span": {
          "start": 2355,
          "end": 2434,
          "unit": "Unicode codepoints; half-open normalized chapter stream"
        }
      }
    ],
    "context_policy": "Up to2 sentence units each side, clipped to the same chapter logical page; no wrap or crossing",
    "user_reflection": null
  }
]
```

## Historical indexing reference

```json
null
```

## Neutral selection comparison

```json
{
  "ordered_sentence_ids": [
    "RUT.1.s030"
  ],
  "repeated_ids": [],
  "combined_meaning": null,
  "policy": "Neutral identity comparison only; repeated selections retained in order, no inferred combined message"
}
```

## Raw user text

```json
{}
```

## Source numeric discrepancies

```json
{
  "seventeen_books": "00..07,10..17 includes invalid00 and omits08/09; conditioning away00 leaves15 reachable books, not17.",
  "fine_word_count": "Two0–9 faces sum0..18 triangular over100 ordered pairs; digital1..20 has a different domain/distribution. Neither implemented."
}
```

## Manual selection boundary

```json
{
  "kind": "user_supplied_manual",
  "generated_draw": false,
  "selection_probability": null,
  "distribution_policy": "No software-generated draw and no probability claim for user-supplied selections. Future hierarchical uniform child selection differs from flattened passage-uniform sampling."
}
```

## Evidence layers

```json
{
  "direct": "Source procedure attribution, exact rights-cleared text and edition/native citations",
  "editorial": "Manual digital adaptation, normalized display whitespace, logical pages, curated sentence spans, trace/context and identity comparison",
  "user_attributed": "Raw user question, reflection and notes, never edits to source text",
  "unsupported": "Objective predictions, verified divine selection, diagnoses, supernatural guarantees or unverified Homeric verses"
}
```

## Unsupported scope

```json
[
  "Fine-word synthesis",
  "Seeded or other generated random selection",
  "Unverified Homeric tuple-to-verse mappings or reconstructed text",
  "Physical/printed pagination inferred from HTML, screen lines substituted for sentences",
  "Other editions/corpora/canons/traditions under this profile",
  "Objective predictions, divine selection verification, psychological diagnoses or supernatural guarantees"
]
```

## Exact replay metadata

```json
{
  "request": {
    "schema_version": 1,
    "profile": "mascaro2022-manual-coarse-webclassic-ruth-v1",
    "mode": "manual_coarse",
    "corpus_id": "webclassic2020-ruth-v1",
    "corpus_version": 1,
    "corpus_sha256": "94361b1342cba7a6ac9e0eb2e2c9ab3d21c289eb1bc3213e2cec79eb859b4055",
    "index_id": "webclassic2020-ruth-sentences-v1",
    "index_version": 1,
    "index_sha256": "d4649b4478756780752170255ddfeea43aeb7998fa47b75da8b4c8b869951352",
    "selections": [
      {
        "path": [
          1,
          1,
          2,
          30
        ]
      }
    ],
    "context": 2
  },
  "input_sha256": "8d10f0c500d13a449409fecd0b95a5bfa0702c229425abfc9d97d56a4e608c6b",
  "profile_sha256": "8fb64b52b632362cfc9633d6c4a01cceebeed51a14beef84b384105dca12cf34",
  "corpus_sha256": "94361b1342cba7a6ac9e0eb2e2c9ab3d21c289eb1bc3213e2cec79eb859b4055",
  "index_sha256": "d4649b4478756780752170255ddfeea43aeb7998fa47b75da8b4c8b869951352",
  "raw_manifest_sha256": "03a7ac3f4ca4fa8b8a7edce0969aa30c5c1644cb2eae6eafedad0322e63aabd9",
  "raw_witnesses": [
    {
      "name": "RUT01.html",
      "url": "https://ebible.org/eng-web/RUT01.htm",
      "status": 200,
      "sha256": "aa66d1d71110c2fc4b42022860e375349535f4366f0ef2341fe258c8eed51667",
      "bytes": 7569,
      "encoding": "UTF-8",
      "path": "resources/corpora/webclassic-ruth-v1/RUT01.html"
    },
    {
      "name": "RUT02.html",
      "url": "https://ebible.org/eng-web/RUT02.htm",
      "status": 200,
      "sha256": "6bbb0a83bd577c751ccacadb0aa1a9b79b92b4d1df34435df0eadeb433661d7c",
      "bytes": 6988,
      "encoding": "UTF-8",
      "path": "resources/corpora/webclassic-ruth-v1/RUT02.html"
    },
    {
      "name": "RUT03.html",
      "url": "https://ebible.org/eng-web/RUT03.htm",
      "status": 200,
      "sha256": "ba3a5f715a2d9c7958b3b9b8ea8379f2c7965cbea9dc9b5099b88ec76023d26d",
      "bytes": 5007,
      "encoding": "UTF-8",
      "path": "resources/corpora/webclassic-ruth-v1/RUT03.html"
    },
    {
      "name": "RUT04.html",
      "url": "https://ebible.org/eng-web/RUT04.htm",
      "status": 200,
      "sha256": "026eef6466808747c81ad60308acbe57fe1e6dde56aea9074917aa7e4a4db624",
      "bytes": 6239,
      "encoding": "UTF-8",
      "path": "resources/corpora/webclassic-ruth-v1/RUT04.html"
    }
  ],
  "serialization": "SHA256 canonical UTF8 sorted-key compact JSON, unescaped Unicode, no terminal LF; raw user whitespace preserved",
  "external_calls": false,
  "rng": false,
  "integrity_checked": true
}
```
