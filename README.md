# Future

Technique #9 **Face Reading / Physiognomy — Core v1 Ready — Historical/Symbolic Reference Scope** under `lavater-hunter-1789-reference-v1`. All146 tests/105 CLI cases pass. Source pages/figures are recorded in `knowledge/face_reading_lavater_v1.json`; supported/experimental/unsupported scope and P1/P2 are frozen in `knowledge/face_reading_core_v1.json`. No individualized physiognomic inference is implemented.

Technique #8 **Palmistry — Core v1 Ready**: manual Western readings under `cheiro-ninth-manual-v1`. All134 tests/93 CLI cases pass. Source rules are in `knowledge/palmistry_cheiro_v1.json`; frozen supported/experimental/unsupported scope and P1/P2 are in `knowledge/palmistry_core_v1.json`. Original rankings/variations remain preserved.

Technique #7 **Astrocartography — Core v1 Ready**: angular geometry/relocation core and source conventions in `knowledge/astrocartography_conventions_v1.json`; frozen scope/P1/P2 in `knowledge/astrocartography_core_v1.json`. All122 tests/83 CLI cases pass. Original-book procedures remain unsupported; the historical resource audit preserves access/attribution limits.

Technique #6 **Mundane Astrology — Core v1 Ready** uses the named Green1911 profile below. Its frozen practical scope/P1/P2 backlog is in `knowledge/mundane_core_v1.json`; source/convention records are in `knowledge/mundane_resource_audit.json` and `knowledge/mundane_green_v1.json`. Acceptance:110 tests and71 CLI cases,including all101 prior tests/59 cases. Ready does not mean exhaustive historical coverage or verified future-event prediction.

```powershell
python -m future mundane-ingress 2026 Europe/London 51.5 0 --format markdown
python -m future mundane-ingress 2026 Australia/Sydney -33.8688 151.2093
python -m future mundane-cycle "2020-12-01T00:00:00+00:00" "2021-01-01T00:00:00+00:00" Europe/London 51.5 0 --format markdown
python -m scripts.smoke_mundane_core
python -m scripts.verify_mundane
```

All four apparent tropical Sun crossings are solved in the selected UTC calendar year1851–2148. Explicit coordinates and IANA display zone are required, with abs(latitude)<60 degrees; no capital inference or polar house substitution. Placidus is an explicit software realization, not a claimed named-system mandate in Green pp2–4. Charts include nine pre-Pluto planets, axes/cusps, classical-seven dignity facts, geometric motion and source-traced direct/compositional readings. Outer-planet dignity/interpretation gaps remain visible. Nearest-major-angle geometry has no invented within-orb threshold or aggregate strength score.

`--historical-duration` enables only the old Aries-ASC3/6/12-month context. Green questions close application and requires examining all four charts; no forecast expiry is inferred. `mundane-cycle` supports exact Jupiter–Saturn conjunctions and their stations/ingresses in an offset-aware window of at most366 days. Slow repeated contacts amplify small ephemeris-coordinate differences into timing differences; root convergence is not absolute time accuracy. No unique national founding chart, eclipse classification or economic/geopolitical outcome is inferred.

Examples: `data/mundane-ingresses-2026-london.*`, `data/mundane-ingresses-2026-sydney.json`, `data/mundane-cycle-2020.*`. Independent USNO/Swiss comparisons and the preserved Saturn discrepancy in Green's1899 printed chart are in `data/mundane-validation.json`; the historical chart is only a partial comparison, not full predictive validation.

Numerology core: `python -m future numerology 1998-10-15 "Thomas Cruise Mapother" 2026-10-12 --basis birth --format markdown`. Use `--basis current` for explicitly labeled current-name overlays; `--y-roles vc` classifies two successive Y occurrences as vowel/consonant. ASCII names only; unsupported characters reject rather than silently transliterate. Calendar-year personal cycles are separate from master-preserving core reductions. Scope/backlog: `knowledge/numerology_core_v1.json`; reproducible report: `data/numerology-acceptance.md`.

## Chinese Astrology — bounded BaZi Core v1

```powershell
python -m future bazi "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209
python -m future bazi "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 --format markdown
python -m future bazi "1988-02-15T23:30" Asia/Shanghai 31.2 121.5 --profile civil-split-zi
python -m scripts.smoke_chinese_core
```

Four Pillars use solved apparent solar Li Chun/jie boundaries, a published continuous day epoch and explicit clock profiles. `civil-zi23` advances the day at23:00; `civil-split-zi` advances the day at00:00 but uses the following day's stem for the23:00 hour; `standard-zi23` subtracts IANA DST from civil time. Local solar-time correction is unsupported. Inputs use Gregorian local years1901–2100, pinned IANA zones and explicit DST folds. Hemisphere does not reverse the solar-month sequence.

The separately labeled lunar-year animal uses HKO's published New Year date at local civil midnight. It is a festival-date profile, not a full lunar calendar or conjunction calculation. Source-grounded components include Ten Gods, unweighted modern hidden-stem sets, classical Day Master imagery and pillar topics. Composed readings are labeled; raw element counts do not measure strength or prescribe favorable elements. Luck-pillar onset, Zi Wei Dou Shu and Nine Star Ki remain unsupported/deferred.

Examples: `data/bazi-core-1990.md/json`, published Shanghai-settings chart `data/bazi-published-1918.json`. The frozen scope, source limits, independent checks and P1/P2 backlog are in `knowledge/chinese_core_v1.json`. The optional MIT lunar-python1.4.8 oracle is used only by reference-generation scripts; production uses the existing Skyfield/DE440s stack. No book PDFs/images or third-party implementation code are redistributed.

Vedic core CLI (Technique #2): `python -m future jyotish "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 --d9 --target "2026-11-03T00:00:00+00:00" --format markdown`. The fixed profile, supported scope and P1/P2 refinements are in `knowledge/vedic_core_v1.json`; exact calculation conventions and source locators are in `knowledge/vedic_conventions.json`. Savana 360-day years are the default; `--year-key solar-365.2425` selects the documented alternative. Neither is silently mixed with Western timing methods.

**Technique #2: Core v1 Ready** for its bounded Parashari D1/nakshatra/Vimshottari MD-AD/D9 source/local scope. Acceptance: 73 tests (all prior 63 retained), 12 Vedic and 23 Western CLI smoke cases. Run `python -m scripts.smoke_vedic_core` for `data/vedic-core-1990.json` and its Markdown report. Source discrepancies, year-length differences and period-date sensitivity are reported explicitly; a microsecond-formatted computed boundary is not real-world precision or predictive confidence. Jaimini, KP, Prashna and other vargas/dashas remain in P1/P2 refinement.

Development follows the permanent **80/20 directive** in `AGENTS.md`: stabilize a verified practical core, label experimental/unsupported features, record P1/P2 refinement, and then continue in inventory order. Exhaustive historical completion is not the release gate. Western Core v1 scope is frozen in `knowledge/western_core_v1.json`; `knowledge/western_refinement_backlog.json` preserves deferred work.

**Technique #1: Core v1 Ready** for its documented source/local CLI scope. Acceptance: 63 tests and 23 CLI smoke cases. Run `python -m unittest discover -s tests -q` and `python -m scripts.smoke_western_core`. New July-1990 natal/progression/return examples are under `data/core-v1-*`; results expose composed and missing interpretation coverage. See `THIRD_PARTY_NOTICES.md` for the lightweight dependency audit and distribution limits.

Knowledge-driven prediction research and specialized computational engines. Traditional procedures and interpretations are separate from evidence of predictive accuracy.

The immutable workbook in `resources/` is the taxonomy authority. `knowledge/inventory.json` preserves all six worksheets; `inventory_audit.json` records structural checks; `gaps.json` tracks the initial ordered gap pass. Curated source research is separate in `sources.json` so provisional rankings are never silently rewritten.

## Reproduce the inventory audit

Python 3.11+:

```powershell
python -m pip install -r requirements-dev.txt
python scripts/import_inventory.py
```

The evolving knowledge base is a permanent asset: source records, scoped versioned rules, examples and relationships remain independently reusable by future engines. Start with JSON and SQLite full-text retrieval. Add semantic retrieval only after measuring a need. Engines own calculations; retrieval supplies provenance and interpretation context.

See `PROGRESS.md` for implemented scope and the next action. The natal calculation foundation is available; Western Astrology remains incomplete.

## Run the first knowledge/calculation slice

Runtime uses Python's standard library only. From the repository root:

```powershell
python -m unittest discover -s tests -v
python -m future --database knowledge.sqlite3 search "Gregorian UT1"
python -m future calendar 1877 8 11 7.5
```

The pipeline loads source metadata, ingests original UTF-8 research notes under an explicit rights policy, imports manually extracted typed rule records, checks published numerical fixtures, and stores immutable versions in SQLite. Full-text retrieval returns source locators and document hashes. Calendar results reference the applied rule and retrieved source. The three published USNO examples are independent reference values; date-boundary tests also compare Python calendar arithmetic.

Current extraction is manual. PDF/OCR extraction, LLM-proposed extraction, semantic embeddings, API and UI remain pending. The `calendar` command requires explicit UT1; the `natal` command below accepts local civil birth time.

## Calculate a natal chart

```powershell
python -m pip install -r requirements.txt
python scripts/fetch_ephemeris.py
python -m future natal "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209
python -m future natal "2000-08-01T12:00" Europe/London 51.5 0 --tradition medieval/traditional --houses equal
```

JSON includes planetary placements, speeds/retrograde states, Ascendant/MC, house cusps and assignments, major aspects, timescales, configuration and provenance. `--fold 0` or `--fold 1` resolves repeated DST times; nonexistent times are rejected. `--orbs '{"0":8,"90":5,"180":8}'` selects aspect angles/orbs. Offline calculation requires the validated local DE440s kernel. See `knowledge/ephemeris-decision.md` for accuracy, scope, license research and independent validation. Sample output is in `data/sample-natal.json`.

## Forecast natal transits

```powershell
python -m future forecast "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00" --days 30 --bodies Mercury,Saturn
```

Start requires an explicit offset. Windows are 1–30 days, start-inclusive/end-exclusive. Defaults scan all tradition-supported planets and five major aspects. `--orbs` selects angles and orbs as for natal. Orbs filter active contacts; exact crossings are listed even for zero-width orbs. Output includes current positions, active applying/separating/stationary contacts, chronological exact contacts to natal planets/ASC/MC, repeated-pass numbering, source-specific symbolic components and precision limits. All contacts are returned without an invented significance score.

`data/sample-natal.json` is the **August 1, 2000, London** demonstration. `data/sample-transits-1990.json` is the **July 15, 1990, Delhi** demonstration forecast for November 2–December 2, 2026, using Mercury/Saturn and 3-degree conjunction/square/opposition orbs. These are distinct fictional example inputs.

The curated `knowledge/western_rules.json` contains source-checked summaries of twelve houses, seven classical planets with sign-level dignities, twelve sign descriptions, major-aspect symbolism and methodological differences. The build script preserves their individual authorities and locators. Computational verification is separate from checking a traditional text. Classical symbolism is not silently substituted into modern interpretations. No copyrighted book text is ingested. Hand's accessible indexed Saturn methodology is retained with an access limitation; full planet-pair delineations from *Planets in Transit* remain pending authorized access.

Transit roots use 3-hour scans, refined sampled stations and bisection to a 0.25-second bracket. This numerical resolution does not imply equivalent absolute accuracy. Swiss/Moshier independent fixtures verify Mercury positions and both retrograde/direct passes; analytical trajectories test boundaries, wraps and close station contacts. Kernel, model and birth-time uncertainty still affect absolute timing, especially at slow motion.

## Read a complete forecast

The new complete example is `data/forecast-1990-november-2026.md`, with all underlying data in the adjacent JSON. It uses the July 15, 1990 Delhi birth and November 2–December 2, 2026 window. The older August 2000 natal example is separate.

```powershell
python -m future forecast "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00" --format markdown
```

JSON retains the full event list and adds clipped intervals within the selected orb, ongoing configurations, brief contacts, active/applying contacts and recurrence groups referencing canonical event IDs. Same-target-house themes are geometric groupings; they do not imply corroboration or merged predictions. The 24-hour duration bins and 0.01°/day near-station flag are explicit display conventions, not predictive scores. A clipped duration is only time inside this forecast window; it is not a claim about total transit duration.

`knowledge/transit_rules.json` contains 29 short, source-specific planet-pair records keyed by tradition, transiting body, natal target, aspect set, conditions and source. Records distinguish direct delineation scope (including Hand's general across-aspect pair discussion) from compositional context. Missing condition context cannot satisfy a constrained rule. No rule is silently reversed or transferred to another tradition. Source review status does not imply empirical predictive verification. Traditional sign rulership/dignity calculations are separately labeled even when the reading school is modern. Detailed historical/Hellenistic pair rules, house/dignity-specific transit delineations and full authorized book coverage remain gaps.

## Quadrant houses and secondary progressions

Natal and forecast commands accept `--houses porphyry`, `placidus`, `regiomontanus`, or `campanus`, in addition to `whole-sign` and `equal`. Each uses a distinct original mathematical construction. Placidus solves semi-arcs; Regiomontanus projects equator divisions; Campanus projects prime-vertical divisions; Porphyry trisects ecliptic quadrants. Runtime never imports Swiss Ephemeris. Quadrants explicitly reject the polar domain without substitution. Details are in `knowledge/house_methods.json`.

```powershell
python -m future natal "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 --houses regiomontanus
python -m future progressions "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00" --houses placidus --angles naibod-ra
```

Progressions map elapsed TT age into symbolic ephemeris days. `--year-key tropical` uses 365.24219 days; `julian` uses 365.25. This is an explicit continuous-year convention, not calendar-birthday interpolation. Physical ephemeris speeds, symbolic-year speeds and civil-day speeds are labeled separately. The output includes progressed planets, natal/progressed house placements, progressed-to-natal and mutual progressed aspects, eight-sector lunar phase, upcoming sign ingresses, progressed Moon contacts and lunation boundaries. `--window-days` selects 1–366 civil days; `--orbs` configures major aspects, default one degree.

`--angles none` omits progressed axes/houses. `naibod-ra` adds 0.98564733 degrees per symbolic year to natal ARMC. `solar-arc-mc` adds the true progressed solar longitude arc to natal MC before recalculating the other cusps. These two options explicitly combine secondary planets with directed angles. `secondary-rotation` uses actual sidereal rotation at the progressed epoch. All three use progressed-epoch true obliquity and the natal location. None applies a solar arc to every planet, and primary directions are not implemented.

Examples: `data/house-comparison-1990.md` and its JSON compare all six systems. `data/progressed-1990-2026.md` and its JSON include the progressed chart and structured aspect report. Independent frozen Swiss fixtures and generators are in `tests/fixtures/house_reference.json`, `tests/fixtures/progression_reference.json` and the corresponding scripts. Before 1972, civil inputs follow Skyfield's proleptic UTC model (TT−UTC 42.184 seconds); do not mistake this for reconstructed historical UT1. Future leap seconds are not forecast. Symbolic procedures and interpretations, with distinct authority scopes, are stored in `knowledge/progression_methods.json` and registered separately from the transit rules.

## Hellenistic / traditional conditions and annual profections

```powershell
python -m future doctrines "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209
python -m future doctrines "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 --tradition medieval/traditional --houses regiomontanus
python -m future profections "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00"
```

`doctrines` returns astronomical sect, seven classical planetary conditions, dignity owners, reception edges and Fortune/Spirit. `--bounds egyptian` and `--bounds lilly-ptolemaic` preserve distinct factual tables. Hellenistic defaults use Dorothean triplicities, 15-degree beams, domicile dispositorship and reversed night Lots. Medieval defaults use Lilly's two-ruler triplicities, same-sign CA113 combustion (8.5°), 17° beams and 17′ cazimi, dignity occupancy and fixed-day Fortune. Spirit remains independently sourced. Alternative reception/solar/Lot settings are available through `DoctrineSettings`; incompatible Hellenistic profile combinations are rejected. Source conflicts (including CA300 thresholds and Ptolemy transmissions) are recorded in `knowledge/doctrine_sources.json` rather than silently reconciled. Participating triplicity rulership is reported separately from primary dignity. No score is calculated.

Sect uses topocentric apparent solar center altitude without atmospheric refraction or terrain. Near-horizon cases are flagged. Planetary altitude, solar separation, speed and longitude phase are geometric data; actual naked-eye or heliacal visibility is not inferred. Mercury's sect uses the declared morning/evening longitude-phase convention; an application-based alternative remains unimplemented.

`profections` starts at whole-sign house 1 at birth and advances one sign each completed year. Its sign ruler is the traditional lord of the year. `--boundary birth-time` (default) changes at the local birth-time anniversary; `midnight` instead changes at the beginning of the birthday. These are explicit software timing conventions. `--leap-day march-1` (default) or `february-28` resolves non-leap birthdays. A nonexistent DST anniversary is rejected; repeated anniversaries require `--anniversary-fold 0` or `1`. Solar-return boundaries are not calculated. Targets before birth or without an offset are rejected.

Natal `--profections-date <offset-aware datetime>` and forecast `--profections` append explicitly labeled Hellenistic timing context. Forecasts crossing a birthday also expose the changed annual context. Natal quadrant placement is retained alongside the independent whole-sign annual activation. Examples: `data/hellenistic-1990.md`, `data/traditional-1990.json`, and `data/profections-1990-2026.md`, with JSON companions and a year-by-year timeline.

## Solar Returns and source-driven elections

```powershell
python -m future solar-return "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 2026
python -m future solar-return "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 2026 --return-latitude -33.9 --return-longitude 151.2 --format markdown
python -m future election retain-received-money "2026-11-01T00:00:00+00:00" "2026-11-03T00:00:00+00:00" 28.6139 77.209
```

Solar Returns find the apparent geocentric tropical Sun-longitude crossing in a selected UTC calendar year, not a civil anniversary. Supported years: 1850–2148. All six houses are selectable. Return-to-natal aspects and geometric T-square/grand-trine patterns are reported. Mary Fortier Shea's accessible FAQ method is registered as tropical/nonprecessed/Placidus; other houses are not attributed to that method. Specific copyrighted book delineations remain unsupported. See `data/solar-return-1990-2026.md` and its JSON.

Electional profiles and rule parameters are in `knowledge/electional_profiles.json`. The two Ramesey profiles distinguish retaining received money (fixed signs) from rapidly circulating it (preferred movable signs). Select the latter using category `rapid-use-received-money` and `--profile ramesey-rapid-use-money`. They evaluate the specifically implemented sign/motion predicates; they do not claim complete source compliance. `--require` selects supported rule IDs with omissions reported. Constraints include `--utc-hours 18 19`, `--min-minutes 5` and `--ascendant-signs 1,4,7,10` (zero-based signs). Conflicting constraints are exposed, not scored or averaged.

Searches are bounded to seven days and latitudes within ±60°. The solver partitions at planet sign ingresses/stations and ASC/MC/second-cusp sign changes, checks quarter points and guards internal boundaries by one second. Unresolved cells are reported. There is no formal global proof against unseen multiple reversals; minimum-duration constraints can exclude brief intervals. A denser five-minute angle scan and independent Swiss minute-grid fixtures test the sample for missed/extra candidates. Diagnostics report Moon phases/aspects, angular benefics/malefics, dignity/debility, reception and retrogradation separately from hard selection rules. Comparative dignity diagnostics explicitly identify their Lilly profile. Unknown criteria are never counted as satisfied.

See `data/election-retention-2026.md` and its JSON for candidates, representative charts, satisfied/violated rules, unresolved criteria and source conflicts. These symbolic profiles are not calibrated financial advice or success forecasts. Dorotheus Book V procedural coverage, complete lunar perfection and wider electional categories remain refinement gaps. Horary stays out of scope. `knowledge/western_completion_audit.json` records the **Core v1 Ready** scope; incomplete electional certification remains experimental.

Sources retain author, edition, access and ingestion policy. Rules retain technique, variation, tradition, version, exact locator, operation, parameters, evidence type, verification state and fixture references. Different authorities use distinct IDs; changed rules use new versions. Only verified rules in the exact requested scope are selected. Verification here means procedural/example agreement, not predictive accuracy. The registry is a local trusted research store; ingesting arbitrary external rule JSON as verified is unsupported.

## Classified elections and Zodiacal Releasing

Election output preserves `candidates` as legacy partial-rule matches. Use `assessed_windows` for `eligible`, `rejected` or `indeterminate` classifications, timestamped rule traces and exact lunar-house/contact boundaries. `eligible_windows` is currently empty: full radix/revolution, fortification, nodes/lunation and historical prohibition exceptions are incomplete. An intervening lunar aspect is reported numerically; it is not automatically a historical prohibition. `knowledge/electional_requirements_v2.json` separates unused-money retention from investment and lists the precise blockers.

```powershell
python -m future releasing "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00" "2026-12-02T00:00:00+00:00" --lot Spirit
python -m future releasing "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00" "2026-12-02T00:00:00+00:00" --lot Fortune --format markdown
python -m scripts.write_releasing_examples
```

The named `brennan-2019-360` profile computes L1–L4 using fixed 360-day years, parent-truncated periods and one Loosing of the Bond per parent. Spirit moves forward one sign when the Lots coincide; Fortune's natal sign remains the angular reference. Full JSON contains period/parent IDs, actual and query-clipped boundaries, bond flags, source rules and limitations. Queries cover at most five civil years within 120 symbolic years after birth. Existing natal ephemeris/time-zone restrictions apply; historical Egyptian calendar reconstruction is unsupported.

Examples: `data/releasing-spirit-1990-2026.*`, `data/releasing-fortune-1990-2026.*` and `data/releasing-diana-reference.json`. Published Gemini durations, L1–L4 tables and Diana's July 22, 1997 bond date are checked separately from independent Swiss/Moshier starting Lots. No published absolute L3/L4 chronology is claimed verified. Discrepancies in Valens/Riley IV.10 remain explicit in `knowledge/zodiacal_releasing.json`. Symbolic peaks describe Fortune-based angularity in the named school; they imply neither favorable outcomes nor established predictive validity.

## Technique5 Horary — Core v1 Ready, Diagnostic Scope

```powershell
python -m future horary "Was this advice given with honest intent?" advice-intent "2026-11-03T12:00:00" Asia/Kolkata 28.6139 77.209 --protocol advice-begins --format markdown
python -m scripts.smoke_horary
python -m scripts.verify_horary
```

This illustrative example uses Lilly1647 p194: the chart moment is when the adviser first begins disclosing advice. Supply the actual moment/location; the program does not infer them from question text. Named profile `lilly-1647-advice-intent` fixes tropical Regiomontanus, seven classical planets and explicit mean nodes, with IANA folds required for ambiguous clocks. The motion window is four days within1851–2148, abs(latitude)<60 degrees. JSON includes the full chart, significators, dignities/receptions, exact contacts, stations/ingresses, source pages and rule diagnostics; Markdown presents the assessment and timeline.

The supported diagnostic product includes the chart, significators, dignities, receptions, planetary conditions, exact contacts and source-traceable testimonies. JSON labels it **Core v1 Ready — Diagnostic Scope**, with **Question Judgment — Experimental** and `judgment_certified: false`. Advice-intent remains `indeterminate`: seventh-cusp/lord caution clearance and a matching complete-input published validation are incomplete. A favorable testimony cannot override that gap. `unsupported_question` covers other categories; Frawley/Barclay methods are not substituted.

`knowledge/horary_engine_v1.json` freezes configurations and P1/P2 refinement. The targeted source attempt in `horary_judgment_attempt_v1.json` distinguishes explicit pp122–123 cautions from the general p115 table; not every table row is automatically a mandatory category veto. Cambridge1643 is documentary evidence outside current ephemeris support and a different category. Synthetic cases and Swiss fixtures verify boundaries/astronomy, not published question judgments. See `data/horary-advice-2026.*` and `data/horary-validation.json`; run `python -m unittest discover -s tests -q` and all five smoke scripts. Numerical agreement does not establish predictive validity. Technique6's resource audit follows the committed diagnostic closure.


## Technique7 Astrocartography

```powershell
python -m future astrocartography "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 --query 28.6139 77.209 --uncertainty-minutes 5 --format markdown
python -m future astrocartography "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 --format geojson
python -m scripts.smoke_astrocartography_core
python -m scripts.verify_astrocartography
```

`--destinations` takes a JSON array of objects with `name`, `latitude`, `longitude`, `zone`; the smoke script demonstrates London/Sydney. Every relocation uses the same absolute birth instant. `--houses` supports the existing six systems; Placidus is the software default, not an asserted book mandate. Charts are supported inside |latitude|<60; higher-latitude chart requests return explicit unsupported status without suppressing valid global lines.

`geocentric-apparent-geometric-v1` calculates all ten existing ephemeris targets (Mars through Pluto system barycenters), apparent RA/declination at the true equator/equinox of date and GAST. MC/IC mean upper/lower meridian, ASC/DSC mean increasing/decreasing geocentric geometric center altitude at zero. No observer parallax, refraction, limb or elevation model; these are not observed rise/set predictions. Actual planetary latitude is retained, so physical angularity need not match longitude-only chart axes/houses.

GeoJSON contains 40 MultiLineString features with source IDs, exact target names, numerical diagnostics and compositional readings. Adaptive geographic-linear sampling defaults to 0.01 degrees residual tolerance; dateline splits lie on the analytic curve. Grazing junctions/poles are excluded from mapped branches. Selected-point distances are exact shortest spherical distances to semicircle closures using mean radius6371.0088km, with grazing/polar endpoint flags. They sort geometry, not desirability; no influence-radius probability is implied. Uncertainty is explicit +/- minute sensitivity, not a statistical confidence interval.

Samples `data/astrocartography-july1990.*` use July15,1990 14:30 Asia/Kolkata (09:00UTC). The independent1990 fixture uses a deliberately separate06:30UTC instant; the2000 leap-day fixture is another case. `data/astrocartography-verification.json` reports measured errors against Swiss/Moshier over four epochs,452 horizon roots,54 circumpolar cases and96 relocation charts. Optional Swiss fixture regeneration is reference-only; production never imports Swiss.

All40 planet-axis interpretations are explicitly modern compositional symbolism, sourced to separate planet meanings and angular-house topics. No direct Lewis/Davis text, branded certification, location ranking or established predictive validity is claimed. Original Book of Maps title-page attribution and all three ranked books' coordinate conventions remain unverified; inventory metadata is preserved. Parans/local-space and deeper original interpretations remain refinement work.


## Technique8 Palmistry: manual Western core

```powershell
python -m future palmistry data/palmistry-observations.json --format markdown
python -m future palmistry data/palmistry-observations.json
python -m scripts.smoke_palmistry_core
```

Supply one or both hands in validated JSON. The complete worked input is `data/palmistry-observations.json`; reports are `data/palmistry-reading.json` and `.md`. It is an explicitly constructed usage example, not a historical person or independently verified photograph. The input reference at `knowledge/palmistry_input_reference_v1.json` lists allowed fields,source-defined shapes and mount positions. Unsupported keys and duplicate JSON keys are rejected; optional `markings`/`unsupported_features` lists retain unimplemented observations without interpreting them.

`schema_version:1`, `profile:"cheiro-ninth-manual-v1"` and a `hands` list are required. Each hand needs a unique `side:"left"` or `"right"`. Optional `dominance` is left/right/ambidextrous/unknown. Unknown and uncertain are explicit values; omitted fields remain unknown. Major lines use a presence value and qualitative length/depth/clarity/curvature/continuity/branch properties. Heart branch readings require the source's commencement location. Positive millimeter proportions produce descriptive ratios only; they never classify a hand automatically.

The named Western profile uses Cheiro's inspected Ninth Edition: six hand types,eight mount sites,selected Life/Head/Heart rules and explicit exceptions. It preserves the author's pp77-78 left/natural,right/acquired convention without silently reversing for dominance. Single-hand readings disclose missing comparison context. Contradictory observations suppress affected rules; differing symbolic themes coexist without a score or invented synthesis. Full JSON includes every rule's match/unknown/conflict diagnostic,source,printed locator and observed/required conditions.

Readings are attributed historic symbolism,not evidence of personality,medical conditions,longevity or future outcomes. Life-line depth/length/breaks are retained without medical/death readings. A fully observed hand can still contain unsupported properties; coverage does not mean all historical doctrines are implemented. No image is loaded or retained. Benham/Saint-Germain,Indian Samudrika,dermatoglyphics,minor markings and timing scales are not substituted.

Six source fixtures were independently transcribed from visually inspected published types/labeled schematic details: Plates II,III,V,XVI and XVIII with the corresponding printed passages. These validate faithful mapping of selected features,not a full historical person's palm reading or predictive validity. The original scan's title says Ninth Edition,copyright1897,with a1900 LOC receipt stamp; the earlier catalog1898 label is preserved separately. Original PDF/pages are research references,not bundled product data.


## Technique9 historical face-reading reference

```powershell
python -m future face-reference data/face-reference-observations.json --format markdown
python -m future face-reference data/face-reference-example-input.json
python -m scripts.smoke_face_reading_core
python -m scripts.verify_face_reading
```

`face-reference` is a historical/symbolic reference engine. The named profile uses visually inspected Lavater/Hunter1789 Volume I: six regional labels on p18,two terminology records on pp20/23,and three numbered schematic constructions on pp265-266. Original scans and contemporary Yap/Bridges books are not bundled. Chinese Mian Xiang,five-element and12-palace mappings are unsupported; publisher descriptions are not treated as procedural evidence.

Required JSON fields are `schema_version:1`,the exact `profile`, `task:"historical_reference"`,and `mode:"manual"` or `"source_example"`. Manual mode requires orientation and1-24 region observations; example mode selects an exact published schematic ID and rejects manual overrides. The complete input reference is `knowledge/face_reading_input_reference_v1.json`. Unknown/uncertain values remain explicit; invalid fields,duplicate JSON keys and nonfinite/out-of-range points are rejected. Unknown region identifiers remain unsupported rather than receiving another school's association.

Orientation is an explicit software annotation convention. `left_profile` means the anatomical left side is visible; `side_frame` declares subject versus displayed-viewer labels. With a known frontal,nonmirrored display,viewer-left maps to subject-right; mirrored displays preserve side labels. Optional normalized coordinates map x to1-x in the same nonmirrored frontal conversion; subject-frame x increases toward anatomical right. Unknown mirroring and profile projections are not guessed. No pixels are read,so users remain responsible for the declared view and observations.

Geometry and markings are descriptive only. Historical context is looked up by region,not by shape; every row exposes `geometry_used_for_association:false`, `association_applied_to_individual:false` and a null individual assessment. Changing outline,proportion or markings cannot produce an intelligence,honesty,morality,criminality,personality,medical,ethnicity,protected-trait or life-outcome conclusion. Such inference requests are rejected. Conflicting observations remain flagged without reconciliation; archival region text remains available independently of the conflict.

The historical region associations record what Lavater claimed,with attribution and printed/canvas locators; they are not valid statements about the annotated person. His three forehead constructions are documented as an example of discredited capacity-ranking claims,without reproducing a ranking algorithm or applying it to a person. Hunter translation terminology stays separate from Holcroft and Chinese schools.

Samples: `data/face-reference-observations.json` is constructed manual usage data,not a photograph or historical individual; `data/face-reference-manual.json`/`.md` contain eight descriptive annotations covering all six regions. `data/face-reference-schematic.json`/`.md` document the published second schematic. `data/face-reference-verification.json` checks six independently transcribed regional entries and three original numbered figures. These checks establish selected source fidelity and interface behavior,not physiognomic validity or image-recognition accuracy.
