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

## 2026-11-02 — working natal chart foundation
- Selected MIT Skyfield 1.54 + checksum-pinned local JPL DE440s after comparing Swiss licensing/features and Astronomy Engine. Replaceable ephemeris protocol; no network during chart calculation.
- Implemented IANA historical offsets/DST with gap rejection and explicit fold resolution, UTC/TT/UT1 metadata, apparent geocentric tropical positions, speeds/retrogrades, ASC/MC, whole-sign/equal cusps and assignments, major aspects/configurable orbs, independent tradition/application/configuration dimensions.
- Connected two sourced traditional domicile examples to calculated placements through the existing registry and FTS retrieval. Interpretation scope remains deliberately small.
- Verified three charts against independent Swiss/Moshier planetary positions and equal-house cusps/angles; checked published Einstein Sun/Moon placements. Fifteen tests pass, including original nine. CLI emits usable structured JSON; sample saved in data/sample-natal.json.
- Limits: 1850–2149, nonpolar locations, modeled delta T, traditional rulership only, no quadrant houses, timing applications or complete interpretation system. Historical IANA offsets may differ from town LMT. Western Astrology remains Developing, not Complete.
- Next: expand independent published chart fixtures and traditional rules, then quadrant houses and transit/progression calculations.
- Commit: natal foundation commit (resolve with `git log --grep="integrate offline"`).

## 2026-11-02 — natal transit forecasting
- Implemented offline 1–30-day forecast CLI: natal planets/ASC/MC targets, current positions, configurable aspects/orbs, applying/exact/separating/stationary states, vectorized scanning, refined stations, exact-contact bisection and chronological repeated-pass events.
- Extracted source-specific Lilly/Houlding house and planetary/dignity summaries, twelve Houlding sign summaries, Campion and traditional aspect interpretations, application/orb conventions. Catalog records preserve author/edition/locator/rights/exceptions. Computational rules and symbolic source review states remain distinct.
- Forecast interpretation uses selected-tradition aspect components and available planetary/house context. Detailed planet-pair transit delineations remain incomplete; Hand article access blocked, indexed methodology recorded only. No fabricated Hand interpretations.
- Independent Swiss/Moshier November 2026 fixture covers Mercury positions and retrograde/direct crossings of 225 degrees; numerical roots agree within 120 seconds. All 20 tests pass, including original tests. Full default 30-day CLI run yields 133 exact contacts and 32 active contacts for the July 1990 example. Catalog: 44 records.
- Distinct examples: sample-natal.json = August 1, 2000 London; sample-transits-1990.json = July 15, 1990 Delhi, November 2–December 2, 2026 forecast.
- Limits: source coverage still partial, three-hour sampling cannot guarantee detection of multiple unseen reversals in one cell; numerical root tolerance is not absolute accuracy or predictive validity. No calibrated life-event probabilities.
- Next: deepen authorized planet-pair transit interpretations and historical validation; then quadrant houses, progressions, expanded traditions and electional. Technique #1 remains Developing.
- Commit: transit milestone (resolve with `git log --grep="source-grounded natal transit"`).

## 2026-11-02 — source-grounded interpretation and forecast presentation
- Added 29 concise source-checked transit records: Cafe Astrology practitioner compilation and Robert Hand's indexed Jupiter discussion, with individual locators, exceptions, aspect sets and condition fields. Hand's general pair scope remains explicit; no aspect-specific Hand text invented.
- Matcher distinguishes documented / compositional / unsupported, exact condition matches and source/tradition isolation. Traditional house-ruler/dignity calculation metadata is separate from modern interpretive records.
- Added numerical orb-entry/exit intervals, clipped duration reporting, canonical event IDs, non-destructive themes, ongoing/brief views, active/applying views and repeated-contact groups. No probability or importance scores.
- Complete Delhi 1990 birth example: 133 exact contacts preserved; 143 configurations, 32 active at start, 15 repeated patterns. Direct pair coverage: 28 exact contacts; remaining 105 compositional. Markdown report plus full JSON saved as forecast-1990-november-2026.*.
- All 24 tests pass: conditional selection/provenance, isolation, dates/locations, event partition completeness, repeated retrograde groups, station tangencies and clipped orb durations; existing independent Swiss reference tests retained. Existing registry rule versions remain unchanged.
- Gaps: direct coverage remains sparse; no full historical/Hellenistic transit pair library, complete licensed book ingestion, or verified house/dignity-specific transit delineations. Numerical precision remains separate from symbolic predictive validity.
- Next: quadrant houses, secondary progressions, and deeper Western source coverage. Technique #1 remains Developing.
- Commit: forecast presentation pass (resolve with `git log --grep="enrich transit interpretations"`).
