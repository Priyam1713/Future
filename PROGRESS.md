# Future progress

## 2026-11-02 — inventory and research pass
- Repository was empty. Cloned the requested remote successfully through Git; connector access returns 404.
- Imported all six worksheets losslessly as cell values, preserving the original XLSX and SHA-256.
- Validated 60 ordered IDs, 54 retained, six exclusions, 260 variations, 151 ranked sources, 91 edges and 12 forward-only prerequisites. Source ranks and cross-sheet technique names match.
- Added ordered gap records for all 60 methods. 86 source leads lack URLs. This is structural coverage, not completed external verification of all techniques.
- #1 Western Astrology: checked Lilly access and alternative page leads, Hand publisher scope, Arroyo catalog lead, USNO calendar procedure/examples and Swiss Ephemeris licensing.
- All six Western variations remain incomplete. Hellenistic and electional procedural sources are material gaps; transit coverage does not establish progression coverage.
- Next: implement a small provenance-preserving local knowledge pipeline and verify calendar arithmetic against USNO examples. Continue external source verification in ID order.
- Commit: `71cc061` (pushed to `main`).

## 2026-11-02 — #1 knowledge/calculation slice
- Implemented source registry, policy-gated UTF-8 note ingestion, document hashes, immutable typed rule versions, exact tradition/variation selection and SQLite FTS5 retrieval.
- Manually extracted one calendar rule with three source-located USNO examples. Fixture checks run before the CLI imports it as verified. Calculations remain independent of retrieval or text generation.
- Implemented Gregorian-to-Julian-date conversion for 1801–2099 with explicit UT1 input and structured provenance-bearing output. No natal chart or variation marked complete.
- Tests: 9 passing, including three published examples, independent date arithmetic, boundary/invalid inputs, scope isolation, immutable versions, rights gates and idempotent persistent ingestion.
- Added per-variation Western coverage and unresolved configuration conflicts. Source ranking and workbook content remain unchanged.
- Unresolved: external verification for techniques #2–60; full-text rights and chapters; automatic extraction; ephemeris/license choice; timezone conversion; planets/houses/aspects; interpretations; API/UI. No paid dependencies added.
- Next: inspect Western procedural chapters and integrate an established ephemeris with independent reference positions. Continue initial source verification in numerical order; do not advance to Engine #2.
- Commit: this feature commit (resolve with `git log --grep="feat(01)"`).
