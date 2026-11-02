# Future

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
