# Future progress

## 2026-11-03 — #3 Pass3: sourced BaZi interpretations and Core v1 closure
- Calculation pass b2aa210 pushed first. Added all100 phase/polarity Ten Gods relations, twelve unweighted modern hidden-stem sets, ten classical Day Master imagery components, four pillar-topic components and explicit compositional readings. Source-specific classical/modern components labeled; seasonal allocations never merged or scored.
- All83 tests pass, preserving all73 Western/Vedic tests;15 Chinese,12 Vedic and23 Western CLI smoke cases pass. Independent100-cell relation/12-set checks and published teaching examples supplement Pass2 numerical fixtures. Pip check clean; pinned production dependencies unchanged, optional MIT oracle stays reference-only.
- Frozen chinese_core_v1.json marks **Core v1 Ready** for accurate Four Pillars, separately labeled festival animal and bounded source-grounded symbolic interpretation. Source/rule/clock/root traces remain reproducible. Examples: data/bazi-core-1990.md/json and bazi-published-1918.json. Numerical accuracy is distinct from historical fidelity and predictive validity.
- P1: independently verified luck onset/calendar-age convention, source-complete strength/combination rules, sourced local solar clocks. P2: Zi Wei Dou Shu, Nine Star Ki, difficult historical calendars and deeper direct interpretations. No luck timing or excluded variation claimed implemented. Research book PDFs/images removed locally; no copyrighted corpus redistributed.
- Next: commit/push closure before beginning Technique#4 Numerology resource audit. Commit: resolve with git log --grep="close BaZi Core v1".

## 2026-11-03 — #3 Pass2: Four Pillars calculation core
- Source/convention pass c3aea33 pushed first. Added independent DE440s solar-term root solving, continuous Gregorian day epoch, all four pillars, Day Master, symbolic element/polarity counts, three named clock/Zi profiles and bazi JSON/Markdown CLI. Existing Western/Vedic modules untouched.
- Six targeted tests pass:26 HKO published term times,45 independent diverse pillar cases, published complete-input and late-Zi examples, exact jie/zhongqi/day/hour boundaries, DST rejection/alternatives, both hemispheres, scope and provenance. All200 HKO CNY dates1901–2100 extracted as numerical facts with per-source hashes; cross-checked against independent lunar-python dates.
- Full79-test regression suite passes, preserving all73 prior tests. Reproducible calculation-only example in data/bazi-d1-1990.json/md; CLI Markdown smoke passes.
- Festival animal uses a separately named local-midnight HKO date profile; no full lunar calendar or worldwide conjunction convention implied. Clock inputs resolve through pinned IANA; no hidden solar-time correction or hemispheric sign reversal. Luck onset remains unsupported.
- Delhi1990 example: Geng-Wu / Gui-Wei / Xin-Si / Yi-Wei, Xin Yin Metal Day Master. Solar-root bracket <=.005 seconds; primary minute-rounded reference checks use65 seconds, not a predictive confidence claim.
- Next: source-scoped Ten Gods/hidden stems and compositional readings, full release acceptance and refinement backlog. Commit: resolve with git log --grep="implement verified Four Pillars".

## 2026-11-03 — #3 Pass1: source-checked BaZi conventions
- Resumed2f3ffa6. Checked San Ming vol2 digital witness (fixed revision), Tan's author-hosted Ten Gods excerpt, Yap's solar-calendar teaching and annotated workshop chart; no book corpus/images redistributed. Classical seasonal hidden-stem variants remain separate from named modern fixed sets.
- Named civil-zi23, civil-split-zi (day00:00 but late-Zi hour uses next day) and explicit standard-zi23 profiles. Exact apparent315-degree Li Chun and30-degree jie months; Gregorian Jia-Zi day epoch2026-08-18 from HKO. Civil/standard clock choices explicit; local solar corrections unsupported.
- Registered26 HKO term instants, published Vasiloiu Shanghai-settings chart (PDFp12), two software-author worked cases and45 independently generated lunar-python1.4.8 reference cases; oracle optional/MIT, not runtime. Shared IANA inputs do not independently validate timezone history.
- Luck-pillar direction/three-day-year/ten-year procedures located but complete independently checked onset convention deferred; no fabricated timings. Numerical algorithm agreement does not establish predictive validity.
- Next: implement independent DE440s Four Pillars and verify fixtures before readiness. Commit: resolve with git log --grep="verify BaZi sources and conventions".

Current policy: **80/20 practical cores**, permanently recorded in `AGENTS.md`; exhaustive historical completion is superseded. **#1 Western Astrology — Core v1 Ready**, closed/pushed `ec5f69b`. **#2 Vedic Astrology — Core v1 Ready**, closed/pushed `1f2acc8`. **#3 Chinese Astrology — Core v1 Ready**, bounded BaZi source/local scope; #4 audit starts only after this closure is committed/pushed.

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
- Commit: `fe4b3d9` (pushed).

## 2026-11-02 — bounded Spirit/Fortune Zodiacal Releasing
- Inspected Valens/Riley IV.4 and IV.10 (Griscti edition), Brennan's 2019 handout and Brennan/Schaim episode 192. Versioned source rules register sign units, nested boundaries, 360-day years, single opposite-sign bond jump, coincident-lot Spirit adjustment and Fortune angularity. Named profile: `brennan-2019-360`; incompatible variants reject without substitution.
- Working Python/CLI `releasing` supports separate Spirit/Fortune outputs, L1–L4, half-open dates, parent truncation, query clipping, bond flags, source traces and profile digest. Natal Lots reuse astronomical sect and reversed night formulas. No favorable-outcome score or deterministic health/event interpretation.
- New verification: Valens's published Gemini 211-month circuit and clipped remainder; Brennan's L1–L4 period table; published Diana Fortune bond date July 22, 1997 (date precision only). Independent Swiss/Moshier starting-Lot fixtures cover northern day charts, southern night/leap day and explicit pre-1972 proleptic UTC. No published absolute L3/L4 chronology independently verified.
- Added reproducible July 1990 Spirit/Fortune November 2026 reports and full JSON, plus Diana reference JSON. Spirit example: L1 Pisces (from 2020-02-08), L2 Leo (from 2026-09-04); natal Fortune Leo remains the angular reference.
- Source gaps explicitly retained: Riley IV.10 prose/table mismatch and Taurus remainder mismatch, Egyptian/intercalary calendar reconstruction, qualitative cross-lot substitutions and full period delineations. Numeric agreement does not establish historical universality or predictive validity.
- Completion audit retains Developing and adds procedure statuses, remaining gaps and ordered v1 gates. No Technique #2 work. Lunar station sample velocities also normalized to the same degree/day units used during refinement (zero locations unchanged).
- All 59 tests pass (40.455s), retaining the original 48; CLI JSON/Markdown smoke checks and diff validation pass. Commit: resolve with `git log --grep="bounded source-named zodiacal releasing"`.

## 2026-11-02 — Western Core v1 readiness (80/20 Pass 1)
- Reviewed the original six inventory dimensions; froze supported configurations in knowledge/western_core_v1.json and P1/P2 refinement in western_refinement_backlog.json. Electional certification remains experimental; ZR L1/L2 core retained, L3/L4 available experimentally with chronology limits. No ancient-calendar expansion.
- Added 27 concise source-checked components: twelve modern houses, Sun/Moon/Mercury symbolism, eight progressed lunar phases and Shea return-house/inner-retrograde methodology. Connected natal CLI to existing and new catalog readings; traditional natal CLI now also includes calculated condition reports. Modern transit composition gains house topics. No invented direct natal/progression/return pairs.
- Regression checks enforce source locators, immutable records, computed placement linkage, tradition isolation, progressed phase and conditional return retrograde selection. Fixed modern progression context appearing under traditional selections; legacy interfaces retained.
- All 63 tests passed, retaining 59. Runtime versions fully pinned; installed license/notice metadata and hashes audited. Source/local CLI scope only; commercial/binary/kernel redistribution and full vulnerability automation deferred explicitly. No Swiss runtime or copyrighted book ingestion.
- Permanent root AGENTS.md now applies 80/20 gates across the inventory while preserving 54 retained/six excluded decisions, accuracy/provenance/rights and one-technique ordering.
- Next: final complete tests/CLI smoke checks, mark Core v1 Ready if acceptance passes, commit closure, then start #2 resource/variation audit. Commit: resolve with `git log --grep="freeze Western core scope"`.

## 2026-11-02 — Western Core v1 closure (80/20 Pass 2)
- Readiness pass `adb841e` pushed. All 63 regression tests pass (42.346s), preserving all prior 59, plus 23 public CLI smoke cases; pip check and diff validation pass. Independent numerical/source fixtures retained.
- Every command exercised: calendar/retrieval, three natal traditions and optional annual context, transit JSON/Markdown, modern/traditional progressions, relocated/alternative-house Solar Returns JSON/Markdown, doctrines, profections, both releasing Lots and experimental election profiles. Invalid DST/configuration inputs reject.
- Fixed hardcoded July-1990 heading in generic Solar Return Markdown; added readable composed house/retrograde context. Reproducible July-1990 examples: data/core-v1-natal-1990.json, core-v1-progressions-1990.json, core-v1-return-1990.*; acceptance trace: western-core-v1-smoke.json. Run `python -m scripts.smoke_western_core` to regenerate.
- Marked **Core v1 Ready** in matrix, completion/variation audit and technique gap tracker. This is the practical verified source/local scope, not exhaustive completion, empirical validation or binary/commercial-distribution certification. Electional certification and absolute L3/L4 chronology remain explicitly experimental; P1/P2 backlog preserves deferred work.
- Next: after committing closure, begin #2 resource/variation audit only, in exact inventory order. No #2 implementation in this closure. Commit: resolve with `git log --grep="close Western Core v1"`.

## 2026-11-02 — #2 Vedic Astrology resource/variation audit
- Started only after Western closure `ec5f69b` was committed/pushed. Preserved all seven inventory variations and three ranked sources. No #2 executable engine/rules added.
- Located BPHS Santhanam/Ranjan catalog evidence, Raman publisher Vol.1/2 listings and K.N. Rao title/author in BVB p.23. Bibliographic scope is not chapter/rule verification. Registered supplemental author-hosted P.V.R. Narasimha Rao textbook link; PDF access is blocked (406/timeout), so no text inspection or ingestion claimed.
- Structured source/variation audit: knowledge/vedic_resource_audit.json and vedic_sources.json; same source metadata registered in the shared source library. Primary Bisaria article supplies Jaimini/Moon-degree methodology leads, not verified example calculations.
- Proposed 80/20 first slice: named sidereal D1 with explicit nodes, Moon nakshatra/pada, Vimshottari main/subperiods, D9 and selected sourced interpretation. Ayanamsha/precession/nutation, node choice, dasha year and lineage conventions must be verified before coding. Jaimini, additional vargas, KP and prashna remain prioritized refinement candidates, not silently merged or claimed implemented.
- Next: inspect legitimate procedural sources and worked examples for that first slice, keeping Swiss reference-only unless licensing decisions change. Existing Western acceptance remains 63 tests / 23 smoke cases; research metadata validated against inventory and registry. Commit: resolve with `git log --grep="audit Vedic sources and variations"`.

## 2026-11-02 — #2 Pass 1: verified procedures and named conventions
- Read author-hosted PVR textbook via non-www URL (2000 text, 2010 update); prior access gap resolved. Inspected chart images with PDF skill. BPHS digital Sanskrit 6.12 corroborates D9; machine translation not treated as scholarly authority. Raman worked-page access remains a source gap, not fabricated coverage.
- Fixed bounded profile in vedic_conventions.json: revised true Lahiri1956 anchor transported with pinned Skyfield precession/nutation; IERS mean-node polynomial; whole-sign D1, 27 nakshatras/four padas, classical sign dignities/full graha drishti; savana360 default versus explicit solar365.2425 Vimshottari year; full-first-MD AD subdivisions and half-open elapsed-time boundaries.
- No executable rule implementation before these conventions. Exploratory ayanamsha comparison across 1850–2149 differs ~0.14 arcsecond from Swiss default model; named realization is explicit, no fitted offset. Swiss stays reference-only.
- Factual fixtures transcribed from PVR Chart1 and Chart54 (complete birth inputs/Lahiri/rounded positions), D9 Example16, and dasha Example50. Preserved source discrepancies: Mars moolatrikona prose/table mismatch and Example50 civil-date arithmetic; unsupported details will not be silently corrected. No book prose/images committed.
- Next: implement/independently verify D1 and nakshatra core. Commit: resolve with `git log --grep="verify Vedic procedures and conventions"`.

## 2026-11-02 — #2 Pass 2: working D1/nakshatra core
- Source/convention pass `2966657` pushed first. Added independent Vedic module and `jyotish` JSON/Markdown CLI; Western calculations/settings untouched. Nine grahas include explicit IERS mean Rahu/Ketu, sidereal motion, whole-sign houses/Lagna, Moon mansion/pada, classical ownership/dignity intervals and full Parashari graha aspects. No arbitrary strength score.
- All 68 tests pass (37.196s), retaining the prior 63. Independent Swiss/Moshier fixtures cover six dates (1879–2149), both hemispheres, day/night, nodes, retrogrades, historical IANA input and rational sector boundaries. Positions <0.01 degree, ASC <0.02 degree, ayanamsha <1 arcsecond; house comparisons share explicit UT1 inputs and do not validate delta-T independently.
- PVR Chart1 planets agree within 0.04 degree and Lagna sign agrees. Printed exact Ascendant differs ~8.9 arcminutes from both independent engines: preserved as unresolved source discrepancy, never fitted away. Existing pre-1972 and future UTC assumptions explicit.
- Reproducible Delhi July1990 D1 in data/vedic-d1-1990.*. Named profile and source traces accompany output; nodes' contested dignity/aspect/co-rule schools and degree-specific Mars moolatrikona remain unsupported. Domain: 1850–2149 astronomical epochs, abs(latitude)<66 degrees.
- Next: source-verified Vimshottari/D9, published examples and core release acceptance. Commit: resolve with `git log --grep="implement verified sidereal D1"`.

## 2026-11-03 — #2 Pass 3: Vimshottari/D9 and Core v1 closure
- D1 pass `77f6807` pushed separately. Added Moon-birthstar MD/AD sequence, full-parent initial ADs, remaining birth balance, exact half-open transitions and current/upcoming reports. Explicit savana360 and solar365.2425 options; no alternative dasha schools silently imported.
- Added Parashari D9 modality mapping, symbolic longitudes/Lagna, D9 house frame and classical sign flags; no D1 degree-specific dignities or independent physical retrograde interpretation applied to D9. D9 meanings and active-lord context are source-scoped/compositional, not event forecasts.
- All 73 tests pass, retaining all 63 prior Western tests. Independent Swiss/Moshier D9 harmonic references, twelve separate rational-arithmetic dasha cases, PVR D9 Example16 and complete Chart54 birth/position/D9-sign comparison pass. Source fixture Jupiter transcription corrected by revisiting image (15 Li29, not 6 Li29).
- PVR Example50 fraction 257/800, balance2.24875 years and Venus AD durations verified. Stated savana arithmetic gives 2002-07-16 23:02 UTC; printed approximate July15 date inconsistent, explicitly preserved as a source discrepancy. No forced date match or fabricated Raman example. Moon error bound .0005 degree implies a derived dasha-date bound up to ~6.6h at 20 solar years; source rounding/birth-time uncertainty separate from arithmetic resolution.
- 12 Vedic and 23 Western public CLI smoke cases pass; pip check clean. Full July1990 report: data/vedic-core-1990.*; at 2026-11-03 UTC: D1 Libra Lagna, Revati pada4, D9 Taurus Lagna, Moon/Mars under savana profile. Source book/images inspected locally only; temporary files removed, none redistributed. No new runtime dependency or Swiss runtime.
- Frozen knowledge/vedic_core_v1.json marks **Core v1 Ready**, with supported/experimental/unsupported matrix and P1/P2 backlog for Jaimini, KP, Prashna, other vargas, advanced dashas, direct interpretations and historical/source gaps. Ready is practical source/local scope, not exhaustive coverage or empirical validity.
- Next: commit/push this closure before #3 Chinese Astrology resource/variation audit. Commit: resolve with `git log --grep="close Vedic Core v1"`.

## 2026-11-03 — #3 Chinese Astrology resource/variation audit
- Began only after Vedic closure `1f2acc8` was committed/pushed. Preserved all five variations/four ranked sources; no Chinese executable engine or rule added.
- Checked Yap publisher scope and Ng catalog metadata; Quan Shu link403 and San Ming edition/access unresolved. No invented book passages or Nine Star Ki coverage from Zi Wei titles.
- Registered HKO primary solar-term/sexagenary tables and1901–2100 conversion references. Exact calendar/day-rollover/clock, luck-pillar and school conventions remain pending in chinese_resource_audit.json.
- Proposed efficient first slice: named BaZi calendar/four pillars, independently verified solar terms, separately labeled animal year and source-verified ten-god relations. Zi Wei/Nine Star Ki remain distinct systems; rights and worked-example access checked before rule extraction.
- Vedic release remains73 passing tests,12 Vedic/23 Western CLI cases. Metadata-only handoff validated against inventory/source registry; no runtime dependency change. Next: verify BaZi procedural passages/conventions before coding. Commit: resolve with `git log --grep="audit Chinese sources and variations"`.
