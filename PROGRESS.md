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

## 2026-11-02 — quadrant houses
- Original Porphyry ecliptic trisection, Regiomontanus equator projection, Campanus prime-vertical projection and iterative Placidus semi-arc constructions integrated in natal/forecast CLI. Corrected transit assignments to use unequal cusp sectors.
- All twelve cusps, exact cusp boundaries and longitude-wrap assignments verified. Frozen Swiss references: 36 spherical frames x four systems (both hemispheres, equator, 65 degrees) plus five astronomical dates including 1879 and leap day 2000. Spherical agreement <0.000001 degree; date-based agreement <0.02 degree with explicit UT1 alignment.
- All 27 tests pass, retaining earlier 24. Found and fixed an overly narrow Placidus right-ascension bracket. Historical UTC/UT1 differences are not hidden in reference comparisons.
- Quadrants reject abs(latitude) >= 90 - true obliquity. Placidus semi-arcs fail there; the other systems' polar orientation is outside this release's validation. No substitute system. Equal and whole-sign remain available.
- Knowledge: knowledge/house_methods.json; example: data/house-comparison-1990.json. Swiss remains a development oracle only.
- Next: secondary progressions with explicit year-length and angle conventions, followed by independent tests.
- Commit: `baa00be` (pushed).

## 2026-11-02 — secondary progressions
- Implemented secondary planets using continuous TT day-for-year scaling, explicit tropical/Julian year keys, signs, retrogrades, progressed-to-natal and mutual aspects, lunar phase sectors, next-year sign ingresses, progressed Moon contacts and lunation boundaries.
- Angle choices: none, Naibod RA, true solar-arc MC, or actual secondary rotation. Directed-angle options are explicitly distinguished from secondary planetary motion and from solar-arc/primary planetary directions. All six house systems supported within their declared domains.
- Knowledge: six separately scoped source records registered with provenance. Calculated Moon natal-house and Sun-sign context linked to sources. Pair readings remain compositional; no transit delineations silently reused as direct progression readings.
- All 32 tests pass, preserving original 24. Swiss/Moshier independent references cover eight age/year-key cases, 96 angle/house combinations, planetary longitudes (<0.01 degree), cusps (<0.02 degree), aspect selections, historical/leap-year inputs, lunar sign ingress and a progressed new Moon (real-date tolerance one hour). Root and grouping tests remain passing.
- Corrected reference clock mismatch for future leap-second assumptions; fixed known offset is explicit. Historical pre-1972 proleptic UTC is declared, not conflated with reconstructed UT1.
- Examples: data/house-comparison-1990.{md,json}; data/progressed-1990-2026.{md,json}. July 1990 example at Nov 2, 2026: progressed Moon 29.253959 Leo; Virgo ingress Nov 22, 2026 ~04:42 UTC. Naibod/Placidus progressed ASC 18.585770 Sagittarius, MC 1.031850 Libra.
- Remaining #1 scope: Hellenistic sect/time-lords/lots and traditional bounds/triplicities/reception remain incomplete; interpretive tradition presets currently have limited scope. Expand direct progression readings, validate more historical time conventions, then other documented timing methods and electional applications. No Technique #2 work started.
- Commit: secondary pass (resolve with `git log --grep="verified secondary progressions"`).

## 2026-11-02 — Hellenistic/traditional planetary conditions
- Implemented astronomical sect from topocentric solar center altitude (unrefracted horizon); classical sect affiliations, explicitly phase-based Mercury convention, domicile/exaltation/triplicity/bounds/faces, detriment/fall, reception policies, motion/proximity and Fortune/Spirit.
- Distinct Egyptian vs Lilly-Ptolemaic tables transcribed from identified diagrams. Dorothean vs Lilly triplicity and Hellenistic 15-degree beams vs Lilly CA113 conditions are not merged. Ptolemaic manuscript differences and Lilly CA300 conflicting thresholds retained as source exceptions.
- Doctrine records registered by source/tradition, with examples, locators and exceptions; no book ingestion, invented strength total or observed-visibility claim. Demetra George/Brennan book scope checked; accessible practitioner/original-author resources used for actual rules.
- All 37 tests pass, preserving earlier 32. Independent Swiss solar altitude references cover 12 modern/historical UT1 cases across hemispheres; source examples verify Sun 25 Libra reception and Lilly cazimi; boundary/table/Lot checks included. No ancient-date numerical claim.
- Examples: data/hellenistic-1990.json and data/traditional-1990.json. July 1990 day chart: Fortune 136.800094 degrees, Spirit 319.045817 degrees.
- Next: annual whole-sign profections with explicit civil-birthday convention and leap-day policy; traditional context integration.
- Commit: doctrine pass (resolve with `git log --grep="traditional planetary doctrines"`).

## 2026-11-02 — annual profections
- Added deterministic twelve-year whole-sign annual activation, traditional lord of year, exact offset-aware civil-birthday boundaries, explicit birth-time/midnight options and March-1/February-28 leap-day policies. DST gaps reject and ambiguous anniversaries require a declared fold. Solar-return boundaries remain separate/unimplemented.
- Lord-of-year natal conditions and source-backed house-topic context included. Quadrant natal house placements remain separate from whole-sign annual activation. Optional natal/forecast context works with birthday transitions inside forecast windows.
- All 42 tests pass, preserving earlier 32. Published age/house examples, year/lord transitions, microsecond birthday boundaries, leap birthdays, DST folds, profile isolation and registry idempotency tested. Existing independent astronomical/reference tests retained.
- Doctrine geometry now also reports unrefracted planetary altitude/azimuth and true angular solar separation, with explicit visibility-model limitations.
- July 1990 example at Nov 2, 2026: age 36, house 1, Scorpio, Mars; period Jul 15, 2026 09:00 UTC through Jul 15, 2027 09:00 UTC. Condition and profection Markdown/JSON reports plus adjacent-year timeline saved under data/.
- Remaining #1: full primary textbook chapter verification, genuine heliacal visibility/station doctrine, application-sensitive horary reception/perfection, other bounds transmissions, additional Lots/time-lords and electional rules. Doctrine outputs are procedural/symbolic, not empirical predictive validation. No Technique #2 work started.
- Next: assess bounded electional criteria and additional advanced timing methods using these verified computations; retain explicit source/profile coverage gaps.
- Commit: annual pass (resolve with `git log --grep="annual profections and time-lord"`).

## 2026-11-02 — Solar Returns
- Implemented exact apparent geocentric tropical solar-longitude crossing within a selected UTC calendar year, full relocated return chart with all existing houses, return-to-natal planet/angle aspects and geometric aspect configurations.
- Shea's accessible FAQ methodology registered separately: tropical/nonprecessed/Placidus, explicit location choice. Specific copyrighted book delineations not ingested or invented. Other houses are computed but not labeled Shea methodology.
- All 44 tests pass, retaining earlier 42. Independent Swiss/Moshier fixtures cover five return charts/years including a leap-day birth and Dec-31 year-boundary births, positions and Placidus cusps; relocation invariance verified. Root-time tolerance 120 seconds; placement tolerance 0.01 degree.
- July 1990 return in 2026: July 15 01:49:59.625 UTC. Solar residual ~0.000000314 degree. Report and full JSON: data/solar-return-1990-2026.*.
- Distinct from civil birthday/profection boundary. UTC return years 1850–2148; no precession correction or unsupported predictive precision claim.
- Next: narrowly sourced electional category with explicit rule traces and search-resolution guarantees/limitations.
- Commit: Solar Return pass (resolve with `git log --grep="verified Solar Return"`).

## 2026-11-02 — source-driven electional search and completion audit
- Implemented narrow Ramesey retention/rapid-circulation profiles from Liber III second-house chapter II pp.135–136, plus explicit Ascendant-lord direct-motion condition. Event categories and source profiles must match; no merged tradition or auspiciousness score.
- Boundary-based search partitions at planetary ingresses/stations and ASC/MC/second-cusp sign changes, with quarter-point checks, one-second guards, minimum duration and explicit unresolved cells. Supports required-rule selection, UTC-hour and Ascendant constraints; contradictory constraints exposed.
- Candidate representative charts include rule/source traces and separately labeled Moon application, angular benefic/malefic, comparative Lilly dignity/reception diagnostics. Source-complete fortification, radix/revolution prerequisites, nodes and lunar perfection remain unknown; candidate means selected predicates passed, not a complete favorable election.
- All 48 tests pass, retaining previous 44. Independent Swiss/Moshier verification agrees at 2,880 minute-grid instants; 5-vs-10-minute angle scans agree on count and boundaries within 0.5 seconds. Tests cover source/profile isolation, constraints/conflicts and source-rule sign/motion examples.
- Example Delhi Nov 1–3, 2026: three partial-rule candidate windows; full JSON/Markdown in data/election-retention-2026.*. No unresolved cells in this example. No formal global completeness guarantee beyond declared scan/domain assumptions.
- Dorotheus Book V remains an authorized procedural-text coverage gap; no unverified Dorothean rules implemented. Horary stays Technique #5, out of scope.
- Added knowledge/western_completion_audit.json covering each original variation and proposed bounded completion gates. #1 remains Developing; priorities are complete lunar perfection/electional core criteria, direct interpretation gaps and assessing a bounded zodiacal-releasing implementation. No Technique #2 work.
- Commit: electional pass (resolve with `git log --grep="source-driven electional search"`).

## 2026-11-02 — retention election certification and lunar sequence
- Versioned Ramesey requirements distinguish unused-money retention (p.135) from investment (p.136). Source-located exceptions, computation coverage and blockers are explicit; no new category or borrowed Horary rules.
- Added moving-target lunar aspect roots, ingress boundaries, target stations, phase checks and intervening contacts. First-house prohibition assessments partition legacy candidates at lunar-house/contact boundaries. Existing CLI and partial-candidate fields remain available; every assessment is rejected or indeterminate, with timestamps and source traces. Eligible windows remain empty while mandatory coverage is incomplete.
- All 51 tests pass, retaining 48. Independent Swiss/Moshier TT fixtures verify 29 contacts/ingresses/stations across 2000 leap day, April 2024 Mercury station and November 2026 (120-second cross-ephemeris tolerance; numerical residual <0.0001 degree). Existing independent 2,880-minute search comparison still passes.
- Delhi example retains three legacy matches, partitioned into five assessments: two rejected for Moon in first house, three indeterminate. Regenerated full JSON and report. No complete election claimed.
- Exact blockers: radix/world-revolution assessment, full fortification/priorities, nodes/lunation conditions and source-complete prohibition/exception adjudication. Geometry alone cannot resolve these. Hourly lunar and 5/10-minute angular scans retain bounded-completeness limitations; no real-world success probability implied.
- Commit: resolve with `git log --grep="classify retention elections"`.
