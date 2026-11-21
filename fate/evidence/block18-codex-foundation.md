# Block 18 · My Fate

| Room | Live reading | Legacy chapter |
|---|---|---|
| Western | Ordered natal chapters, sourced aspect passages, editorial connections, and chart details with rule exceptions. | Tropical geometry and the older separate Sun, Moon and Mercury components. The legacy edition cannot identify which editorial passages the live edition selected or preserve their order. |
| Jyotish | Lagna and lunar readings, D1/D9 comparisons, dignity and house relationships, and context for the chosen Vimshottari periods. | D1/D9 geometry, mansion, period lords and UTC boundary days. The selected instant and exact epochs are absent. Recomputing dignity, disputed conditions and editorial wording against a future ruleset would change the saved reading. |
| BaZi | Day Master and selected pillar topics, visible and hidden stem relationships, and a solar-month interval with boundary sensitivity. | Clock convention, four pair IDs and frozen reference components. The pairs cannot recover a particular year’s solar-term instants or whether the recorded moment was close to one. |

## Storage and compatibility

The browser key stays `fate.codex.v1`. Reading a schema-1 document performs no writes. The first explicit narrative save validates the complete prospective schema-2 document, then replaces the value with one atomic browser storage operation. A blocked write leaves the original available. Legacy records retain their chapter IDs, order, save times, source editions and exact snapshot shapes. Schema 2 can contain both kinds of chapter. Deleting the last narrative leaves a valid schema-2 document containing its preceding legacy chapters.

A narrative contains the technique ID, interpretation edition and ordered sections. Each section contains titled plain-text passages with coverage and a short list of rule IDs. Direct passages must match the frozen edition’s wording. Compositional passages come from the live reading projection. Links, original source summaries, editions and exceptions resolve through the bundled rule catalog. Geometry has its own reference edition. A missing or unrecognized edition fails closed with a message and preserves the stored bytes for recovery.

Western keeps the exact ordered natal chapters and adds uncaptured supported inspector passages under Chart details. Jyotish keeps Lagna, lunar context, both chart geometries, all nine grahas and their supported dignity, house and drishti context. It keeps the selected period passage and the other subperiod topics without the timing target, epoch or calendar days. BaZi keeps the Day Master, clock convention and four pillars with sourced visible and hidden relationships. Solar-term times and the live proximity flag stay in the reading session.

The 50-record and 65,536-character limits apply to the complete library. A full library can be exported before a visitor removes records to free space. Writes consult the current value and other tabs refresh on storage events. Simultaneous writes in separate tabs can race under browser local storage. The library and its backups are unencrypted. Calculated positions and pillar combinations can still reveal inferred birth information.

Legacy-only exports retain schema 1 and the existing source fields. Narrative exports use schema 2 and include their frozen source references. The browser provides downloads. File import is deferred pending a separate review of provenance and collision recovery. Compare Perspectives applies its existing vocabulary to each passage in its own tradition and displays the supporting references for both sides.

Run `python -m fate.build_narrative_refs` to verify the bundled edition against the frozen rules. With the built app running, run `node scripts/capture-codex-narrative.mjs` from `fate/web` to reproduce the mixed-library restart, keyboard and browser zoom checks using synthetic inputs.
