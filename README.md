# Future

## Feng Shui:24 Mountains source reference

`python -m future feng-shui data/feng-shui-input.json --format markdown`

Profile `yap2024-manual-24-mountain-tenths-v1` classifies all24 factual mountain
intervals in Joey Yap's supplemental2024 compass document,page2. This is separate
from the ranked Skinner and Flying Stars books. Tasks are `classify`, `reference`,
`compare` and `catalog`, with exact catalog/version/hash and manual mode.

Use integer `bearing_tenths`0..3599:75 is7.5°,76 is7.6°,920 is92.0°.
Both printed endpoints are included in this discrete domain;N2 wraps through0.
Floats,strings,booleans,negative values and3600+ are rejected without rounding or
normalization. Source labels and neighbors can be looked up without a heading.

Optional `uncertainty_tenths`0..1800 covers the entire symmetric discrete range.
`alternate_readings` add independently declared candidates;all possible mountains
are shown. Explicit `contradictory_assertions` block a definitive result.
`north_reference` distinguishes source_diagram,magnetic,true andunknown;
`bearing_role` distinguishes source_heading,building_facing,building_sitting,
door,observer andunknown. Omitted frames/roles remain unknown while numeric
lookup works. No declination,measurement calibration or physical interpretation
is inferred. Optional independent facing/sitting declarations are consistency
checks only;no opposite is generated. Shared building identity requires explicit
matching `building_id` values in the2–8 ordered comparison readings.

JSON/Markdown preserve raw Unicode,source provenance and immutable replay hashes.
No Qi,health/wealth,safety or compatibility outcome is computed. Other LuoPan
rings,Eight Mansions,Flying Stars andBTB remain outside this profile.
Source artwork and the originalPDF are not redistributed.

Run `python -m unittest tests.test_feng_shui`,
`python -m scripts.verify_feng_shui` and
`python -m scripts.smoke_feng_shui_core`.

## Haruspicy: Roman historical reference

`python -m future haruspicy data/haruspicy-input.json --format markdown`

Profile `cicero-falconer1923-roman-entrail-references-v1` compares four bounded
Falconer1923 source accounts and supplies five critical/contextual references.
Tasks are `compare`, `reference` and `catalog`, all in manual mode, with exact
catalog ID/version/hash. See `knowledge/haruspicy_roman_profile_v1.json` for enums
and `data/haruspicy-caesar-sequence-input.json` for a complete ordered example.

Lung cleft requires explicitly sound other vitals. An absent ancient liver-head
matches a reported practitioner belief in Marcus's critical discussion; present
does not imply favorable. Caesar's first account requires the named setting,
Spurinna attribution and source context. The following-day account requires
`prior_observation_id` linking an earlier matching heart record. Missing,
uncertain, contradictory and mismatched conditions remain explicit.

Use reference lookup without observations to compare source cases and criticism.
Historical source accounts, user declarations, editorial matching and unsupported
claims remain separate. Raw Unicode annotations and request hashes replay offline
in JSON and Markdown. These source labels do not certify modern anatomy, future
events or ritual authority. No animal, specimen, camera, RNG or network is needed.
Mesopotamian and Etruscan observations return unsupported under this Roman profile.

Run `python -m unittest tests.test_haruspicy`,
`python -m scripts.verify_haruspicy` and
`python -m scripts.smoke_haruspicy_core`.

Technique #17 **Oracle Cards — Researching**: resource-only audit in `knowledge/oracle_resource_audit.json`,begun after Tarot closurea036474 pushed. Original three rankings/five variations preserved. Deck/edition-specific inventories,source access,rights,spread/orientation gaps and reusable seeded-draw infrastructure recorded. Lenormand36 is distinct from the newer40-card extension;Kipper,Belline,Sibilla and contemporary decks do not inherit Tarot semantics. No Oracle engine implemented.

**Phase 2 complete — bounded Core v1 scopes** for techniques8-15;this does not imply exhaustive variations or scientific validation.

Technique #16 **Tarot — Core v1 Ready — Symbolic Reading Scope**: `waite-1922-text-v1` supports all78 cards/156 source-linked orientation meanings,56 separately retained additional accounts,one/three-card editorial layouts and Waite's ten-position Celtic layout with a removed significator and explicit facing. Manual draws and `future-cards-sha256-fy-v1` seeded draws produce replayable JSON/Markdown and explicitly compositional symbolic readings. All243 tests/205 CLI cases pass;six independently generated .NET seed vectors verify the protocol. Frozen scope/P1/P2 in `knowledge/tarot_core_v1.json`. Text-only;no modern artwork,other-deck rule blending,diagnosis or certain predictions.

```powershell
python -X utf8 -m future tarot data/tarot-one-input.json --format markdown
python -X utf8 -m future tarot data/tarot-three-input.json --format markdown
python -X utf8 -m future tarot data/tarot-celtic-input.json
python -X utf8 -m future tarot data/tarot-manual-input.json --format markdown
python -m scripts.verify_tarot
python -m scripts.smoke_tarot_core
```

Technique #15 **Iridology — Core v1 Ready — Historical/Educational Reference Scope**: `lindlahr-1922-legend-reference-v1` provides33 selected original schematic labels across both eyes,qualitative placements and fixed source-plate orientation. Manual selections and two teaching selections from the published plate produce JSON/Markdown with source traces. All222 tests/183 CLI cases pass;frozen scope and P1/P2 in `knowledge/iridology_core_v1.json`. No exact polar/radial geometry,patient images,diagnosis,disease-risk or personal-trait assessment. Jensen,Deck and Rayid remain separate unsupported profiles.

```powershell
python -X utf8 -m future iridology-reference data/iridology-reference-input.json --format markdown
python -X utf8 -m future iridology-reference data/iridology-source-example-input.json
python -m scripts.verify_iridology
python -m scripts.smoke_iridology_core
```

Technique #14 **Aura Reading — Core v1 Ready — Symbolic/Creative Reference Scope**: `besant-leadbeater-pg16269-symbolic-v1` provides21 historical color entries,three documentary context terms and four published teaching examples. Manual symbolic compositions include source-qualified motifs,unknown/conflict diagnostics and JSON/Markdown reports. All209 tests/169 CLI cases pass;frozen scope and P1/P2 in `knowledge/aura_core_v1.json`. This separate Thought-Forms profile does not implement Brennan/Kunz layers,chakras or physical aura detection. No personal emotion,personality,health,spiritual-status or outcome assessment.

```powershell
python -X utf8 -m future aura-reference data/aura-reference-input.json --format markdown
python -X utf8 -m future aura-reference data/aura-source-example-input.json
python -m scripts.verify_aura
python -m scripts.smoke_aura_core
```

Technique #13 **Graphology — Core v1 Ready — Historical/Descriptive Reference Scope**: `crepieux-schooling-1892-reference-v1` offers23 descriptive terms across11 feature dimensions and seven published examples from Handwriting and Expression. All196 tests/155 CLI cases pass;frozen scope/P1/P2 in `knowledge/graphology_core_v1.json`. This is a separately identified1892 translation/adaptation,not ABC de la graphologie. Optional baseline/slant angles and normalized spacing/proportions use supplied teaching vectors or measurements; geometry never selects historical meanings. True pressure and personal-trait,medical,employment or forensic-authorship assessments are unsupported.

```powershell
python -X utf8 -m future graphology-reference data/graphology-reference-input.json --format markdown
python -X utf8 -m future graphology-reference data/graphology-source-example-input.json
python -m scripts.verify_graphology
python -m scripts.smoke_graphology_core
```

JSON/Markdown reports and independent verification: `data/graphology-reference.*`, `data/graphology-source-example.*`, `data/graphology-verification.json`. Cartesian x-right/y-up coordinates and common mm/arbitrary units are explicit. Baseline vectors run left-to-right; upstrokes run base-to-tip above baseline. Slant is clockwise from the baseline normal. X-height,ascender height and descender depth have separate declared meanings; no size/spacing or pressure thresholds invented.

Technique #12 **Podomancy / Foot Reading — Core v1 Ready — Historical/Symbolic Reference Scope**: `anonymous-booksellers-pg67858-foot-reference-v1` provides six source-attributed foot-form,sole-line and sole-skin references across two regions. All182 tests/141 CLI cases pass; frozen bounded scope/P1/P2 in `knowledge/podomancy_core_v1.json`. The anonymous pseudo-Aristotle text is separate from Somogyi/Sheehan; individual toe rules,Indian methods and personal appearance-to-trait or medical inference are unsupported.

```powershell
python -m future podomancy-reference data/podomancy-reference-input.json --format markdown
python -m future podomancy-reference data/podomancy-source-example-input.json
python -m scripts.verify_podomancy
python -m scripts.smoke_podomancy_core
```

JSON/Markdown examples and independent transcription results: `data/podomancy-reference.*`, `data/podomancy-source-example.*`, `data/podomancy-verification.json`. Teaching examples are textual selections,not original numbered foot diagrams. Exact print year and matching page images remain unverified; primary transcription/edition limits are explicit.

Technique #11 **Moleosophy — Core v1 Ready — Historical/Symbolic Reference Scope**: offline historical-reference CLI under `fontaine-1862-bpl-reference-v1`,based on inspected Golden Wheel Dream-book containing work,original pp114-119.All170 tests/129 CLI cases pass; frozen scope/P1/P2 in `knowledge/moleosophy_core_v1.json`.27 selected summaries across19 regions; original inventory title/rankings remain distinct. No individualized appearance-to-trait,medical or future-outcome inference.

```powershell
python -m future moleosophy-reference data/moleosophy-reference-input.json --format markdown
python -m future moleosophy-reference data/moleosophy-source-example-input.json
python -m scripts.verify_moleosophy
python -m scripts.smoke_moleosophy_core
```

Reproducible JSON/Markdown reports and independent transcription results are in `data/moleosophy-reference.*`, `data/moleosophy-source-example.*` and `data/moleosophy-verification.json`. Examples select a software textual teaching index; no original numbered mole diagram is claimed.

Technique #10 **Phrenology — Core v1 Ready — Historical/Educational Reference Scope**: offline historical-reference CLI under `spurzheim-1833-second-american-v1`. All158 tests/117 CLI cases pass; frozen scope/P1/P2: `knowledge/phrenology_core_v1.json`. The original1833 legend supplies35 numbered faculties plus two unnumbered symbols; three printed views,15 selected passage summaries and22 legend-only descriptions. No individualized skull inference.

```powershell
python -m future phrenology-reference data/phrenology-reference-input.json --format markdown
python -m scripts.verify_phrenology
python -m scripts.smoke_phrenology_core
```

Example JSON/Markdown and source-transcription results: `data/phrenology-reference.json`, `data/phrenology-reference.md`, `data/phrenology-verification.json`. Input accepts only a named source profile,schematic,label/name/candidate selections and optional predefined browsing group; images,measurements and personal assessment tasks are rejected.

Technique #9 **Face Reading / Physiognomy â€” Core v1 Ready â€” Historical/Symbolic Reference Scope** under `lavater-hunter-1789-reference-v1`. All146 tests/105 CLI cases pass. Source pages/figures are recorded in `knowledge/face_reading_lavater_v1.json`; supported/experimental/unsupported scope and P1/P2 are frozen in `knowledge/face_reading_core_v1.json`. No individualized physiognomic inference is implemented.

Technique #8 **Palmistry â€” Core v1 Ready**: manual Western readings under `cheiro-ninth-manual-v1`. All134 tests/93 CLI cases pass. Source rules are in `knowledge/palmistry_cheiro_v1.json`; frozen supported/experimental/unsupported scope and P1/P2 are in `knowledge/palmistry_core_v1.json`. Original rankings/variations remain preserved.

Technique #7 **Astrocartography â€” Core v1 Ready**: angular geometry/relocation core and source conventions in `knowledge/astrocartography_conventions_v1.json`; frozen scope/P1/P2 in `knowledge/astrocartography_core_v1.json`. All122 tests/83 CLI cases pass. Original-book procedures remain unsupported; the historical resource audit preserves access/attribution limits.

Technique #6 **Mundane Astrology â€” Core v1 Ready** uses the named Green1911 profile below. Its frozen practical scope/P1/P2 backlog is in `knowledge/mundane_core_v1.json`; source/convention records are in `knowledge/mundane_resource_audit.json` and `knowledge/mundane_green_v1.json`. Acceptance:110 tests and71 CLI cases,including all101 prior tests/59 cases. Ready does not mean exhaustive historical coverage or verified future-event prediction.

```powershell
python -m future mundane-ingress 2026 Europe/London 51.5 0 --format markdown
python -m future mundane-ingress 2026 Australia/Sydney -33.8688 151.2093
python -m future mundane-cycle "2020-12-01T00:00:00+00:00" "2021-01-01T00:00:00+00:00" Europe/London 51.5 0 --format markdown
python -m scripts.smoke_mundane_core
python -m scripts.verify_mundane
```

All four apparent tropical Sun crossings are solved in the selected UTC calendar year1851â€“2148. Explicit coordinates and IANA display zone are required, with abs(latitude)<60 degrees; no capital inference or polar house substitution. Placidus is an explicit software realization, not a claimed named-system mandate in Green pp2â€“4. Charts include nine pre-Pluto planets, axes/cusps, classical-seven dignity facts, geometric motion and source-traced direct/compositional readings. Outer-planet dignity/interpretation gaps remain visible. Nearest-major-angle geometry has no invented within-orb threshold or aggregate strength score.

`--historical-duration` enables only the old Aries-ASC3/6/12-month context. Green questions close application and requires examining all four charts; no forecast expiry is inferred. `mundane-cycle` supports exact Jupiterâ€“Saturn conjunctions and their stations/ingresses in an offset-aware window of at most366 days. Slow repeated contacts amplify small ephemeris-coordinate differences into timing differences; root convergence is not absolute time accuracy. No unique national founding chart, eclipse classification or economic/geopolitical outcome is inferred.

Examples: `data/mundane-ingresses-2026-london.*`, `data/mundane-ingresses-2026-sydney.json`, `data/mundane-cycle-2020.*`. Independent USNO/Swiss comparisons and the preserved Saturn discrepancy in Green's1899 printed chart are in `data/mundane-validation.json`; the historical chart is only a partial comparison, not full predictive validation.

Numerology core: `python -m future numerology 1998-10-15 "Thomas Cruise Mapother" 2026-10-12 --basis birth --format markdown`. Use `--basis current` for explicitly labeled current-name overlays; `--y-roles vc` classifies two successive Y occurrences as vowel/consonant. ASCII names only; unsupported characters reject rather than silently transliterate. Calendar-year personal cycles are separate from master-preserving core reductions. Scope/backlog: `knowledge/numerology_core_v1.json`; reproducible report: `data/numerology-acceptance.md`.

## Chinese Astrology â€” bounded BaZi Core v1

```powershell
python -m future bazi "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209
python -m future bazi "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 --format markdown
python -m future bazi "1988-02-15T23:30" Asia/Shanghai 31.2 121.5 --profile civil-split-zi
python -m scripts.smoke_chinese_core
```

Four Pillars use solved apparent solar Li Chun/jie boundaries, a published continuous day epoch and explicit clock profiles. `civil-zi23` advances the day at23:00; `civil-split-zi` advances the day at00:00 but uses the following day's stem for the23:00 hour; `standard-zi23` subtracts IANA DST from civil time. Local solar-time correction is unsupported. Inputs use Gregorian local years1901â€“2100, pinned IANA zones and explicit DST folds. Hemisphere does not reverse the solar-month sequence.

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

Start requires an explicit offset. Windows are 1â€“30 days, start-inclusive/end-exclusive. Defaults scan all tradition-supported planets and five major aspects. `--orbs` selects angles and orbs as for natal. Orbs filter active contacts; exact crossings are listed even for zero-width orbs. Output includes current positions, active applying/separating/stationary contacts, chronological exact contacts to natal planets/ASC/MC, repeated-pass numbering, source-specific symbolic components and precision limits. All contacts are returned without an invented significance score.

`data/sample-natal.json` is the **August 1, 2000, London** demonstration. `data/sample-transits-1990.json` is the **July 15, 1990, Delhi** demonstration forecast for November 2â€“December 2, 2026, using Mercury/Saturn and 3-degree conjunction/square/opposition orbs. These are distinct fictional example inputs.

The curated `knowledge/western_rules.json` contains source-checked summaries of twelve houses, seven classical planets with sign-level dignities, twelve sign descriptions, major-aspect symbolism and methodological differences. The build script preserves their individual authorities and locators. Computational verification is separate from checking a traditional text. Classical symbolism is not silently substituted into modern interpretations. No copyrighted book text is ingested. Hand's accessible indexed Saturn methodology is retained with an access limitation; full planet-pair delineations from *Planets in Transit* remain pending authorized access.

Transit roots use 3-hour scans, refined sampled stations and bisection to a 0.25-second bracket. This numerical resolution does not imply equivalent absolute accuracy. Swiss/Moshier independent fixtures verify Mercury positions and both retrograde/direct passes; analytical trajectories test boundaries, wraps and close station contacts. Kernel, model and birth-time uncertainty still affect absolute timing, especially at slow motion.

## Read a complete forecast

The new complete example is `data/forecast-1990-november-2026.md`, with all underlying data in the adjacent JSON. It uses the July 15, 1990 Delhi birth and November 2â€“December 2, 2026 window. The older August 2000 natal example is separate.

```powershell
python -m future forecast "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00" --format markdown
```

JSON retains the full event list and adds clipped intervals within the selected orb, ongoing configurations, brief contacts, active/applying contacts and recurrence groups referencing canonical event IDs. Same-target-house themes are geometric groupings; they do not imply corroboration or merged predictions. The 24-hour duration bins and 0.01Â°/day near-station flag are explicit display conventions, not predictive scores. A clipped duration is only time inside this forecast window; it is not a claim about total transit duration.

`knowledge/transit_rules.json` contains 29 short, source-specific planet-pair records keyed by tradition, transiting body, natal target, aspect set, conditions and source. Records distinguish direct delineation scope (including Hand's general across-aspect pair discussion) from compositional context. Missing condition context cannot satisfy a constrained rule. No rule is silently reversed or transferred to another tradition. Source review status does not imply empirical predictive verification. Traditional sign rulership/dignity calculations are separately labeled even when the reading school is modern. Detailed historical/Hellenistic pair rules, house/dignity-specific transit delineations and full authorized book coverage remain gaps.

## Quadrant houses and secondary progressions

Natal and forecast commands accept `--houses porphyry`, `placidus`, `regiomontanus`, or `campanus`, in addition to `whole-sign` and `equal`. Each uses a distinct original mathematical construction. Placidus solves semi-arcs; Regiomontanus projects equator divisions; Campanus projects prime-vertical divisions; Porphyry trisects ecliptic quadrants. Runtime never imports Swiss Ephemeris. Quadrants explicitly reject the polar domain without substitution. Details are in `knowledge/house_methods.json`.

```powershell
python -m future natal "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 --houses regiomontanus
python -m future progressions "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00" --houses placidus --angles naibod-ra
```

Progressions map elapsed TT age into symbolic ephemeris days. `--year-key tropical` uses 365.24219 days; `julian` uses 365.25. This is an explicit continuous-year convention, not calendar-birthday interpolation. Physical ephemeris speeds, symbolic-year speeds and civil-day speeds are labeled separately. The output includes progressed planets, natal/progressed house placements, progressed-to-natal and mutual progressed aspects, eight-sector lunar phase, upcoming sign ingresses, progressed Moon contacts and lunation boundaries. `--window-days` selects 1â€“366 civil days; `--orbs` configures major aspects, default one degree.

`--angles none` omits progressed axes/houses. `naibod-ra` adds 0.98564733 degrees per symbolic year to natal ARMC. `solar-arc-mc` adds the true progressed solar longitude arc to natal MC before recalculating the other cusps. These two options explicitly combine secondary planets with directed angles. `secondary-rotation` uses actual sidereal rotation at the progressed epoch. All three use progressed-epoch true obliquity and the natal location. None applies a solar arc to every planet, and primary directions are not implemented.

Examples: `data/house-comparison-1990.md` and its JSON compare all six systems. `data/progressed-1990-2026.md` and its JSON include the progressed chart and structured aspect report. Independent frozen Swiss fixtures and generators are in `tests/fixtures/house_reference.json`, `tests/fixtures/progression_reference.json` and the corresponding scripts. Before 1972, civil inputs follow Skyfield's proleptic UTC model (TTâˆ’UTC 42.184 seconds); do not mistake this for reconstructed historical UT1. Future leap seconds are not forecast. Symbolic procedures and interpretations, with distinct authority scopes, are stored in `knowledge/progression_methods.json` and registered separately from the transit rules.

## Hellenistic / traditional conditions and annual profections

```powershell
python -m future doctrines "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209
python -m future doctrines "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 --tradition medieval/traditional --houses regiomontanus
python -m future profections "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00"
```

`doctrines` returns astronomical sect, seven classical planetary conditions, dignity owners, reception edges and Fortune/Spirit. `--bounds egyptian` and `--bounds lilly-ptolemaic` preserve distinct factual tables. Hellenistic defaults use Dorothean triplicities, 15-degree beams, domicile dispositorship and reversed night Lots. Medieval defaults use Lilly's two-ruler triplicities, same-sign CA113 combustion (8.5Â°), 17Â° beams and 17â€² cazimi, dignity occupancy and fixed-day Fortune. Spirit remains independently sourced. Alternative reception/solar/Lot settings are available through `DoctrineSettings`; incompatible Hellenistic profile combinations are rejected. Source conflicts (including CA300 thresholds and Ptolemy transmissions) are recorded in `knowledge/doctrine_sources.json` rather than silently reconciled. Participating triplicity rulership is reported separately from primary dignity. No score is calculated.

Sect uses topocentric apparent solar center altitude without atmospheric refraction or terrain. Near-horizon cases are flagged. Planetary altitude, solar separation, speed and longitude phase are geometric data; actual naked-eye or heliacal visibility is not inferred. Mercury's sect uses the declared morning/evening longitude-phase convention; an application-based alternative remains unimplemented.

`profections` starts at whole-sign house 1 at birth and advances one sign each completed year. Its sign ruler is the traditional lord of the year. `--boundary birth-time` (default) changes at the local birth-time anniversary; `midnight` instead changes at the beginning of the birthday. These are explicit software timing conventions. `--leap-day march-1` (default) or `february-28` resolves non-leap birthdays. A nonexistent DST anniversary is rejected; repeated anniversaries require `--anniversary-fold 0` or `1`. Solar-return boundaries are not calculated. Targets before birth or without an offset are rejected.

Natal `--profections-date <offset-aware datetime>` and forecast `--profections` append explicitly labeled Hellenistic timing context. Forecasts crossing a birthday also expose the changed annual context. Natal quadrant placement is retained alongside the independent whole-sign annual activation. Examples: `data/hellenistic-1990.md`, `data/traditional-1990.json`, and `data/profections-1990-2026.md`, with JSON companions and a year-by-year timeline.

## Solar Returns and source-driven elections

```powershell
python -m future solar-return "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 2026
python -m future solar-return "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 2026 --return-latitude -33.9 --return-longitude 151.2 --format markdown
python -m future election retain-received-money "2026-11-01T00:00:00+00:00" "2026-11-03T00:00:00+00:00" 28.6139 77.209
```

Solar Returns find the apparent geocentric tropical Sun-longitude crossing in a selected UTC calendar year, not a civil anniversary. Supported years: 1850â€“2148. All six houses are selectable. Return-to-natal aspects and geometric T-square/grand-trine patterns are reported. Mary Fortier Shea's accessible FAQ method is registered as tropical/nonprecessed/Placidus; other houses are not attributed to that method. Specific copyrighted book delineations remain unsupported. See `data/solar-return-1990-2026.md` and its JSON.

Electional profiles and rule parameters are in `knowledge/electional_profiles.json`. The two Ramesey profiles distinguish retaining received money (fixed signs) from rapidly circulating it (preferred movable signs). Select the latter using category `rapid-use-received-money` and `--profile ramesey-rapid-use-money`. They evaluate the specifically implemented sign/motion predicates; they do not claim complete source compliance. `--require` selects supported rule IDs with omissions reported. Constraints include `--utc-hours 18 19`, `--min-minutes 5` and `--ascendant-signs 1,4,7,10` (zero-based signs). Conflicting constraints are exposed, not scored or averaged.

Searches are bounded to seven days and latitudes within Â±60Â°. The solver partitions at planet sign ingresses/stations and ASC/MC/second-cusp sign changes, checks quarter points and guards internal boundaries by one second. Unresolved cells are reported. There is no formal global proof against unseen multiple reversals; minimum-duration constraints can exclude brief intervals. A denser five-minute angle scan and independent Swiss minute-grid fixtures test the sample for missed/extra candidates. Diagnostics report Moon phases/aspects, angular benefics/malefics, dignity/debility, reception and retrogradation separately from hard selection rules. Comparative dignity diagnostics explicitly identify their Lilly profile. Unknown criteria are never counted as satisfied.

See `data/election-retention-2026.md` and its JSON for candidates, representative charts, satisfied/violated rules, unresolved criteria and source conflicts. These symbolic profiles are not calibrated financial advice or success forecasts. Dorotheus Book V procedural coverage, complete lunar perfection and wider electional categories remain refinement gaps. Horary stays out of scope. `knowledge/western_completion_audit.json` records the **Core v1 Ready** scope; incomplete electional certification remains experimental.

Sources retain author, edition, access and ingestion policy. Rules retain technique, variation, tradition, version, exact locator, operation, parameters, evidence type, verification state and fixture references. Different authorities use distinct IDs; changed rules use new versions. Only verified rules in the exact requested scope are selected. Verification here means procedural/example agreement, not predictive accuracy. The registry is a local trusted research store; ingesting arbitrary external rule JSON as verified is unsupported.

## Classified elections and Zodiacal Releasing

Election output preserves `candidates` as legacy partial-rule matches. Use `assessed_windows` for `eligible`, `rejected` or `indeterminate` classifications, timestamped rule traces and exact lunar-house/contact boundaries. `eligible_windows` is currently empty: full radix/revolution, fortification, nodes/lunation and historical prohibition exceptions are incomplete. An intervening lunar aspect is reported numerically; it is not automatically a historical prohibition. `knowledge/electional_requirements_v2.json` separates unused-money retention from investment and lists the precise blockers.

```powershell
python -m future releasing "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00" "2026-12-02T00:00:00+00:00" --lot Spirit
python -m future releasing "1990-07-15T14:30" Asia/Kolkata 28.6139 77.209 "2026-11-02T00:00:00+00:00" "2026-12-02T00:00:00+00:00" --lot Fortune --format markdown
python -m scripts.write_releasing_examples
```

The named `brennan-2019-360` profile computes L1â€“L4 using fixed 360-day years, parent-truncated periods and one Loosing of the Bond per parent. Spirit moves forward one sign when the Lots coincide; Fortune's natal sign remains the angular reference. Full JSON contains period/parent IDs, actual and query-clipped boundaries, bond flags, source rules and limitations. Queries cover at most five civil years within 120 symbolic years after birth. Existing natal ephemeris/time-zone restrictions apply; historical Egyptian calendar reconstruction is unsupported.

Examples: `data/releasing-spirit-1990-2026.*`, `data/releasing-fortune-1990-2026.*` and `data/releasing-diana-reference.json`. Published Gemini durations, L1â€“L4 tables and Diana's July 22, 1997 bond date are checked separately from independent Swiss/Moshier starting Lots. No published absolute L3/L4 chronology is claimed verified. Discrepancies in Valens/Riley IV.10 remain explicit in `knowledge/zodiacal_releasing.json`. Symbolic peaks describe Fortune-based angularity in the named school; they imply neither favorable outcomes nor established predictive validity.

## Technique5 Horary â€” Core v1 Ready, Diagnostic Scope

```powershell
python -m future horary "Was this advice given with honest intent?" advice-intent "2026-11-03T12:00:00" Asia/Kolkata 28.6139 77.209 --protocol advice-begins --format markdown
python -m scripts.smoke_horary
python -m scripts.verify_horary
```

This illustrative example uses Lilly1647 p194: the chart moment is when the adviser first begins disclosing advice. Supply the actual moment/location; the program does not infer them from question text. Named profile `lilly-1647-advice-intent` fixes tropical Regiomontanus, seven classical planets and explicit mean nodes, with IANA folds required for ambiguous clocks. The motion window is four days within1851â€“2148, abs(latitude)<60 degrees. JSON includes the full chart, significators, dignities/receptions, exact contacts, stations/ingresses, source pages and rule diagnostics; Markdown presents the assessment and timeline.

The supported diagnostic product includes the chart, significators, dignities, receptions, planetary conditions, exact contacts and source-traceable testimonies. JSON labels it **Core v1 Ready â€” Diagnostic Scope**, with **Question Judgment â€” Experimental** and `judgment_certified: false`. Advice-intent remains `indeterminate`: seventh-cusp/lord caution clearance and a matching complete-input published validation are incomplete. A favorable testimony cannot override that gap. `unsupported_question` covers other categories; Frawley/Barclay methods are not substituted.

`knowledge/horary_engine_v1.json` freezes configurations and P1/P2 refinement. The targeted source attempt in `horary_judgment_attempt_v1.json` distinguishes explicit pp122â€“123 cautions from the general p115 table; not every table row is automatically a mandatory category veto. Cambridge1643 is documentary evidence outside current ephemeris support and a different category. Synthetic cases and Swiss fixtures verify boundaries/astronomy, not published question judgments. See `data/horary-advice-2026.*` and `data/horary-validation.json`; run `python -m unittest discover -s tests -q` and all five smoke scripts. Numerical agreement does not establish predictive validity. Technique6's resource audit follows the committed diagnostic closure.


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

## Oracle Cards — named Lenormand36 profile

```powershell
python -m future oracle data/oracle-lenormand-input.json --format markdown
python -m future oracle data/oracle-manual-input.json
python -m scripts.verify_oracle
python -m scripts.smoke_oracle_core
```

`lenormand-evening-world-1903-text-v1` uses the complete36-card text inventory in The Evening World's Home Magazine, October19,1903. All36 entries have original numbers,aliases,source locators,paraphrased motifs and conditional context. It is a distinct historical edition;its Bird,Child,Tower and Moon meanings differ from common modern keywords. No Rana George dictionary,40-card extension,Tarot semantics or artwork is included.

Inputs require `schema_version:1`,the exact `profile`, `task:"symbolic_reading"`, `mode:"seeded"` or `"manual"`, `spread:"one"`, `"three"` or `"five"`,and `orientation_policy:"upright_only"`. Seeded inputs require the existing `future-cards-sha256-fy-v1` protocol and1–256 UTF-8 seed bytes. Manual inputs supply `cards:[{"card_id":"lenormand-01"}]` with the exact spread count and no repeats. Optional `question` is context only. Unknown fields,decks,orientations,duplicate JSON keys and nonfinite values reject.

One/three/five-card lines are editorial adaptations,ordered left to right. Adjacent motifs are combined transparently;the reports distinguish source-published conditions from editorial juxtaposition and unsupported exact pair meanings. The Star/Clouds near-condition and Ring/person direction condition are displayed separately. Adjacency-as-near and page-right are experimental application conventions;no condition is certified because distance,perspective and reference-person questions remain unresolved. The newspaper's worked example calls page-left “right”;this discrepancy is preserved. Its full8+8+8+8+4 procedure is documented but Grand Tableau judgment is deferred.

JSON and Markdown include the exact request,canonical order/hash,portable canonical-JSON catalog hash,full seeded permutation,draw and shuffle trace. The canonical IDs are `lenormand-01` through `lenormand-36`,hashed as UTF-8 joined by LF without a final LF. One shuffle,no cuts,no replacement and no orientation stream are used. Existing Tarot outputs are unchanged. Six independent .NET full-deck fixtures,source transcriptions and CLI examples can be regenerated offline;the reference generator is `tests/reference/generate_oracle_vectors.ps1`.

Examples: `data/oracle-one.md`, `data/oracle-three.md`, `data/oracle-five.md`, `data/oracle-manual.md`. Scope is symbolic reflection,not verified predictions or factual judgments. Unsupported distance,cloud image-facing,medical,moral and financial claims remain explicit. Source/rights and release details are in `knowledge/oracle_core_v1.json`;P1 covers documented combinations and advanced layouts,P2 separate Kipper,Belline,Sibilla and contemporary profiles.

## I Ching — Legge1882 symbolic readings

```powershell
python -m future iching data/iching-input.json --format markdown
python -m future iching data/iching-manual-known-input.json
python -m scripts.verify_iching
python -m scripts.smoke_iching_core
```

The immutable `legge-1882-scan-text-v1` profile contains all64 King Wen hexagrams,64 judgments,384 ordinary line entries and2 special paragraphs from the original1882 Michigan/Internet Archive scan. Main text and commentary remain separate. Text is scan-OCR transcription with recorded normalization and selected independent scan fixtures;complete diplomatic collation is P1. No restricted Sacred Texts transcription or modern copyrighted interpretation corpus is included. Names omit Legge's diacritics;hexagram numbers and stable IDs disambiguate repeated romanizations. Pinyin aliases are editorial lookup labels.

Inputs require `schema_version:1`, `profile:"legge-1882-scan-text-v1"`, `reading_policy:"all_moving_lines_v1"`, `task:"symbolic_reading"`,and `line_order:"bottom_to_top"`. Manual input uses `mode:"manual"`, `method:"manual"`,and six `lines`,for example `[6,7,8,9,7,8]`. This example is47→60 with lines1 and4 changing. Values6/8 are yin,7/9 yang;6 and9 change simultaneously. Seeded input uses `mode:"seeded"`, `method:"three-coin"` or `"yarrow-marginal"`, `protocol:"future-iching-sha256-v1"`,and an explicit1–256-byte UTF-8 `seed`. Manual and seeded fields cannot be mixed. An optional plain-text `question` is context only. Unknown methods/profiles,ambiguous order,invalid counts/states,duplicate JSON keys and nonfinite JSON reject.

Three-coin casting consumes18 unbiased binary draws:0=tail2,1=head3,three coins per line,lines1→6. Exact single-line weights for6/7/8/9 are1/3/3/1 out of8. The separate yarrow-marginal method consumes six uniform indices0..15 mapped0→6,1..5→7,6..12→8,13..15→9. Its conventional weights1/5/7/3 depend on the stated residue assumptions;it is a digital marginal sampler,not a49-stalk physical-partition simulation. Probabilities describe casts only,never the likelihood of events.

The SHA256 protocol frames `FutureIChing NUL v1 NUL method NUL uint32be(seed byte length) UTF8seed uint64be(counter)`. Blocks begin at counter0 and are consumed as eight32-bit big-endian words. The existing verified word/rejection-sampling primitives are reused;the card kernel,deck shuffle,cut and reversal behavior are unchanged. Independent PowerShell/.NET fixtures cover14 method/seed combinations,including Unicode normalization differences and byte-length boundaries. Exact request,raw casts,line values,mask,source/convention hashes and transformed numbers are included in both JSON and Markdown. Hashes use canonical UTF-8 JSON with sorted keys,compact separators,unescaped Unicode and no terminal LF,so LF/CRLF checkouts agree.

`all_moving_lines_v1` is an editorial reading policy:show initial judgment,all moving-line texts in bottom-up order,and the relating judgment. No line silently overrides another. With zero changes,the figures coincide;with all six changes in1/2,the additional source paragraph is appended while retaining six ordinary lines. Hexagram64 line3 retains the printed affirmative crossing passage and separately reports the commentary's missing-negative conjecture. Summaries are transparent composition,not historical priority rules or certain predictions.

Examples cover no/one/multiple/all changes,both special cases,seeded coins,yarrow marginal,11→26 manual transformation,and the64.3 variant: `data/iching-*.md`. `knowledge/iching_conventions_v1.json` freezes procedure;`knowledge/iching_core_v1.json` records acceptance and limits. Exhaustive verification checks all4096 six-value states and64×64 masks against independent reference logic,all64 source patterns,eight trigrams,and exact coin/yarrow outcome enumeration. Physical yarrow,other selection traditions and text collation remain P1;Mei Hua and Wen Wang Gua remain separate P2 engines.
# Rune Casting Core v1

Run `python -m future runes data/runes-input.json --format markdown` (or `--format json`).
The immutable `elder24-page-facts-snapshot-v1` profile supplies all 24 identities,
normalized Unicode glyphs with text fallbacks, source locators and original reflection prompts.
It distinguishes alphabet evidence, comparative reconstructed name associations and modern
editorial composition. Twenty-one lexical associations are qualified reconstructions;
Kenaz, Perthro and Algiz retain unresolved literal meanings. Eihwaz's early sound remains
uncertain. Later Old English poem contexts retain their separate Futhorc tradition.

The source is an inspected, SHA-identified digital teaching extract of R. I. Page's
*Runes*: Figure 1 / printed p8, name list / p15 and variants / p18. The exact print
reissue is unverified; the profile identifies the digital snapshot rather than inventing
print metadata. Reconstructed names are not attested Elder labels or ancient divination
rules. No Page prose/diagrams, modern English poem translations, commercial guidebook
corpus, font or artwork is distributed.

Input uses schema_version `1`, exact `profile`, task `symbolic_reading`, mode `seeded`
or `manual`, spread `one` or `three`, and orientation_policy `upright_only`.
Seeded mode requires protocol `future-runes-elder24-draw-v1` and a 1..256-byte UTF-8
`seed`; manual mode requires `runes: [{"rune_id":"rune-01"}]` with the spread's
exact count, without seed/protocol. Three-rune layouts optionally accept three distinct
`positions` labels; `question` supplies optional plain-text context. See the checked
[one-rune](data/runes-one-input.json), [three-rune](data/runes-three-input.json),
[manual](data/runes-manual-input.json), [uncertain meanings](data/runes-unknown-input.json)
and [custom positions](data/runes-custom-input.json) examples.

The rune wrapper reuses unchanged `future-cards-sha256-fy-v1`: canonical 24 IDs,
one unbiased Fisher–Yates shuffle, no cuts/replacement/orientation stream, first 1 or 3
entries. Reports include full permutation, request, trace, catalog/order hashes and exact
replay metadata. Six independent PowerShell/.NET full-set vectors verify the draw.
Digital selection does not reproduce physical stone throwing. Blank runes, other alphabets,
reversal interpretation, universal combinations and factual predictions are unsupported.
Three-rune positions are editorial reflection roles. Source fidelity is not predictive validation.

Run `python -m scripts.verify_runes`, `python -m scripts.smoke_runes_core` and
`python -m unittest tests.test_runes -q` for the bounded acceptance checks.
# Pendulum Divination Core v1

Run `python -m future pendulum data/pendulum-input.json --format markdown` (or
`--format json`). The named `lonegren-web-symbolic-response-v1` profile uses factual
procedural notes from the author-associated *The Pendulum* website. It is separate
from the print Kit, its 19 uninspected charts, Lethbridge's rate tables and experimental
research protocols. The website was inspected during the source audit; fresh access
returned errors/403, recorded in `knowledge/pendulum_pass1_findings.json`. No fresh
source snapshot is claimed. Only original short factual notes are bundled.

All inputs require schema_version `1`, exact `profile`, task `symbolic_response`,
and mode `manual` or `seeded`. Optional `question` is plain UTF-8 context (1..1000
characters); its meaning is never used to determine a response.

Manual mode requires explicit `calibration: [{"signal":"clockwise","response":"yes"},
{"signal":"counterclockwise","response":"no"}]` and `observations: [{"signal":"clockwise"}]`.
Clockwise has no default meaning. Circular and linear mappings may be reversed or
reassigned explicitly. Full yes and no signals must both be declared for a resolved
session. Search/rethink/unresolved mappings remain unresolved. Irregular movement
cannot supply a full yes/no calibration. Duplicate or contradictory mapping entries
are rejected without producing a reading (CLI exit 2 with JSON/Markdown rejection).

Observation categories include clockwise, counterclockwise, vertical (to-and-fro),
horizontal (side-to-side), searching, still, irregular, partial, conflicting and unknown.
Unknown plain-text categories are retained as unrecognized. Optional `quality` is
`full`, `partial`, `conflicting` or `unknown`. One to 64 user-reported observations
are supported. Every observation must resolve fully to the same symbolic category;
there is no majority vote, signal-strength inference or confidence score. This
conservative aggregation is editorial application policy. No motion is inferred.

Seeded mode requires protocol `future-pendulum-sha256-v1`, distribution
`editorial-2-2-1-v1` and a strict UTF-8 `seed` of 1..256 bytes, without normalization.
It excludes manual calibration/observations. A separate `FuturePendulum` framing
inherits unchanged SHA-256 word generation and integer rejection sampling from
`card_random.Stream`. One unbiased index 0..4 selects yes at 0/1, no at 2/3, unresolved
at 4. The exact 2/5, 2/5, 1/5 allocation is editorial digital sampling, with no claim
about historical frequencies or truth. No physical signal or sensor data is generated.
Reports include the source profile hash, input, exact distribution, index, stream trace
and replay. Six independent .NET vectors verify 192 draws and initial digest blocks.

See checked [yes](data/pendulum-manual-yes.md), [no](data/pendulum-manual-no.md),
[ambiguous](data/pendulum-ambiguous.md), [contradictory calibration](data/pendulum-contradictory.md),
[seeded](data/pendulum-seeded.md) and [identical replay](data/pendulum-replay.md) reports.
Direct procedural context and modern reflection remain separate. No factual prediction,
hidden-event detection, emotional diagnosis or physical ideomotor simulation is supported.
Charts, maps, letter wheels and sensors are deferred. Run `python -m scripts.verify_pendulum`,
`python -m scripts.smoke_pendulum_core` and `python -m unittest tests.test_pendulum -q`.
# Crystal Ball Scrying Core v1

Run `python -m future scrying data/scrying-input.json --format markdown` (or
`--format json`). The `atkinson-pg43954-guided-journal-v1` profile selects the
Gutenberg digital text updated 2024-10-23, with its displayed Yoga Publication
Society imprint/ISBN and 1908 copyright. Its exact print reissue is unverified;
it is distinct from the Library of Congress Lyal1908 catalog record. Selected
Lessons II/VI procedural passages were inspected and the digital source bytes
hashed. Only original factual notes and editorial workflow are distributed.

Inputs require schema_version `1`, exact `profile`, task `guided_journal` and mode
`manual`. Optional `session` supports `surface`, `lighting`, `background`,
`intention`, `timestamp`, `practice`, `visualization_subject` and `status`.
Surface IDs are `crystal`, `glass`, `dark_backed_glass`, `polished_metal`, `ink`,
`water_black_vessel`, `water_glass`, `precious_stone`, `unknown` and `unspecified`.
Lighting/background are user-entered text or null; missing values stay unspecified.
The app records these declarations without detecting conditions or claiming
compliance with historical recommendations. Status is `planned` (default),
`completed` or `discontinued`, as declared by the user.

The six-stage workflow covers preparation, intention, relaxed gaze, raw recording,
personal associations and neutral reflection. Each historical component has a rule
ID and original section locator. The overall journal sequence is an editorial
arrangement, not a verbatim historical ritual. Blinking is allowed, strain is
discouraged, and the session may stop at any point without an imagery requirement.
Practice defaults to `gazing`; optional `familiar_visualization` may include a
`visualization_subject` and explicitly distinguishes deliberate imagination.

Optional `journal` may be absent, null, empty, or contain up to128 entry objects.
Each entry supports `experience_type`, `description`, `sequence`, `timestamp`,
`uncertainty`, `associations` (up to32 strings) and `personal_reflection`.
Types are `observed_reflection`, `subjective_imagery`, `imagined_imagery`,
`uncertain` and `no_imagery`. A missing type stays unclassified. Raw descriptions,
associations and reflections preserve whitespace, Unicode and wording. Empty and
missing descriptions are explicit. User uncertainty remains a declaration rather
than engine verification. Optional root `personal_reflection` records overall notes.

List order is preserved; explicit positive sequence annotations must strictly
increase and never trigger sorting. Optional timestamps are ISO dates or
dateTtime with seconds and optional offset; there is no automatic clock/timezone.
Reports retain original records, exact input, source/profile hashes and deterministic
replay. JSON records preserve all raw strings; Markdown also displays them in fenced
blocks with fence lengths adjusted for embedded backticks.

Direct guidance, historical beliefs, user-authored meanings and modern open-ended
editorial questions stay separate. There is no universal symbol lookup, inferred
emotion/entity/hidden event, perception detector or prediction. Generated creative
scenes and seeded prompts are deferred; their category cannot be submitted as a
user observation. No random protocol, camera, frontend or external LLM is required.

Examples: [guided](data/scrying-guided.md), [dark surface](data/scrying-dark.md),
[personal associations](data/scrying-associations.md), [no imagery](data/scrying-no-imagery.md),
[uncertain](data/scrying-uncertain.md), [multiple entries](data/scrying-multiple.md),
[visualization](data/scrying-visualization.md) and [empty journal](data/scrying-empty.md).
Run `python -m scripts.verify_scrying`, `python -m scripts.smoke_scrying_core`
and `python -m unittest tests.test_scrying -q` for bounded acceptance checks.
# Mirror Scrying Core v1

Run `python -m future mirror-scrying data/mirror-input.json --format markdown`
(or `--format json`). The immutable `moody1992-mirror-subset-journal-v1` profile
uses selected original pages108–110 of Raymond Moody's1992 *Family Reunions*
article, inspected in the UNT39-page scan with a frozen byte hash. It is distinct
from the complete1993 book, Atkinson's guidance, Dee/Casaubon and obsidian artifacts.
Only original factual notes and an explicitly qualified workflow are distributed.

The source-specific reference covers a wall mirror/facing chair, a view excluding
the sitter's reflection, a lamp behind the chair, relaxed gazing, no pressure for
an experience, voluntary completion and discussion afterward. Historical hardware
dimensions and the article's25W lamp are reference facts, not equipment requirements.
No numeric mirror-tilt angle is verified. This core omits the full induction sequence,
required blackout/watch removal and expectation of an apparition. Blinking, avoiding
strain and written journaling are explicit editorial adaptations. No encounter,
therapeutic benefit or factual answer is expected or verified.

Inputs require schema_version `1`, exact `profile`, task `guided_mirror_journal`
and mode `manual`. Optional `session` accepts `surface`, `view`, `lighting`,
`background`, `intention`, `personal_context`, `timestamp` and `status`.
Surface is `ordinary_mirror`, `unknown` or `unspecified`; other traditions are
rejected. View is `self_reflection_excluded`, `self_reflection_visible`, `unknown`
or `unspecified`. A declared difference remains recorded rather than silently
changed. No actual environmental measurement occurs. Status is `planned`,
`in_progress`, `completed` or `discontinued`.

The guide stages are `arrange`, `context`, `gaze`, `finish`, `journal` and `reflect`.
Optional `stages: [{"stage_id":"gaze","status":"skipped"}]` records skipped or
completed stages. Duplicate/conflicting declarations are rejected. Completed
stages require an explicitly compatible session status. Guidance and declarations
remain distinct from observed action;users may skip stages or stop at any point.

The compatible journal contract supports up to128 raw entries, five user-declared
experience categories, sequence annotations, ISO timestamps, uncertainty, associations
and personal reflections. Missing/null/empty entries and no imagery remain valid.
Raw Unicode, whitespace and user memories/presence descriptions are preserved and
attributed;there is no automatic person/spirit identification or symbol dictionary.
Reports include source/rule locators, exact input, portable profile/source hashes
and deterministic replay. No camera, sensors, seeded visions or new dependency.

Technique21's engine/profile remains unchanged. Mirror reuses only its pure UTF8,
timestamp, object validation, strict JSON and canonical-serialization utilities;
Mirror configuration, stage logic, source rules and reports are separate.

Examples: [guided](data/mirror-guided.md), [personal associations](data/mirror-associations.md),
[no imagery](data/mirror-no-imagery.md), [uncertain](data/mirror-uncertain.md),
[discontinued](data/mirror-discontinued.md), [multiple entries](data/mirror-multiple.md),
[skipped stage](data/mirror-skipped.md) and [invalid configuration](data/mirror-invalid.md).
Run `python -m scripts.verify_mirror`, `python -m scripts.smoke_mirror_core`
and `python -m unittest tests.test_mirror -q` for bounded acceptance checks.
# Dream Interpretation Core v1

Run `python -m future dream data/dream-input.json --format markdown` (or
`--format json`). The immutable `artemidorus-attalus-context-v1` profile contains
four historical categories, nine bounded motif references and two contextual
qualifications. Selected Attalus excerpts were checked against their named
White1975/Lewis1976 attribution;GreekBook1.1/1.2 terminology was checked in the
Pack1963 digital witness. These are original factual notes, not a modern English
translation corpus or an exhaustive five-book dictionary.

Stable IDs distinguish `enypnion` (present-state experience), `oneiros` (the author's
future-signifying class), and its `theorematic`/`allegorical` branches. Reports
compare user-selected lenses and explicit contextual cases;they cannot establish
predictive significance. The modern translations' varying English dream/vision
labels do not collapse these categories. Freud, Jung and Faraday remain separate
unsupported profiles in this core.

Inputs require schema_version `1`, exact `profile`, task `historical_reflection`
and mode `manual`. All personal material is optional. Root fields include
`narrative`, `timestamp`, `recall`, `scenes`, `people`, `objects`, `places`, `events`,
`feelings`, `associations` and `personal_reflection`. Narratives preserve raw Unicode,
whitespace and wording (up to20000 characters);reflections up to10000. Missing,
null and blank narratives remain distinct. Recall may be `complete`, `fragmented`,
`uncertain` or `no_recall`. Up to64 scene records accept `description`, timestamp,
strictly increasing optional sequence, uncertainty, recall and the user-authored
entity/event/feeling/association lists. No current clock or inferred chronology.

Explicit `lookups` select `eating`, `drinking`, `feared_object`, `desired_person`,
`shipwreck`, `serpent`, `lost_nose`, `broken_staff` or `myth_variants`. Unknown lookup
IDs return unsupported rather than a substitute meaning. Conditions are supplied
in optional `context`: `hungry`, `thirsty`, `current_fear`, `current_desire`, `at_sea`
and `exact_correspondence_reported` are booleans or null. These are declarations,
not facts inferred from the narrative. `circumstances` selects any of `perfume_trade`,
`civic_standing`, `illness`; `staff_cases` selects `initial_account` and/or
`repeat_during_paralysis` as historical comparison accounts, not a health assessment.
`myth_versions` retains alternative user-entered stories. `cultural_context`,
`situational_context` and `notes` are optional raw text.

Each lookup returns source/translator/section, conditions, provided and missing
context, selected author-attributed accounts, alternatives and explicit limits.
Opposite staff/nose accounts stay visible when multiple selectors are supplied.
The serpent reference retains several associations without choosing a universal
meaning. Historical illness/death/recovery accounts are not medical forecasts.
`taxonomy_claims` optionally selects category IDs;conflicting lenses are reported
without silently resolving them.

Manual `annotations` accept a known `motif_id`, optional `target` (`narrative` or
`scene` with1-based `scene_index`), paired `start`/`end`, and `decision` (`include`
or `exclude`). Spans are half-open Unicode code-point offsets into original text;
there is no normalization, case conversion or word-boundary inference. Distinct
overlaps remain;duplicate/conflicting identical annotations reject. Tags and their
corrections never trigger source lookups. Automatic literal matching is deferred P1.

Optional `preferences` controls `historical_references` and `editorial_questions`.
Opting out of historical references conflicts with explicit lookups/category claims.
Reports separate historical reference, raw user meaning, editorial questions and
unsupported conclusions, with portable profile/source hashes and exact replay.
No diagnosis, hidden memories, latent-wish inference, universal symbolism, remote
service, LLM, database or factual prediction. Existing journal engines remain unchanged;
only narrow pure text/timestamp/JSON/hash utilities are reused.

Examples: [complete](data/dream-complete.md), [multiple scenes](data/dream-multiple.md),
[taxonomy](data/dream-taxonomy.md), [context](data/dream-context.md),
[missing context](data/dream-missing.md), [personal associations](data/dream-associations.md),
[fragmented recall](data/dream-fragmented.md), [competing references](data/dream-conflicting.md)
and [manual spans](data/dream-annotated.md). Run `python -m scripts.verify_dream`,
`python -m scripts.smoke_dream_core` and `python -m unittest tests.test_dream -q`.

## Automatic Writing: guided creative sessions and revisions

`python -m future automatic-writing data/automatic-writing-input.json --format markdown`

Profile `breton-bsb2016-writing-subset-v1` presents seven historical facts from
the French primary excerpt in Bibliothèque Sainte-Barbe's2016 bibliography,p4.
The quotation's underlying print edition is unidentified; this is an institutional
excerpt subset, not an authenticated BnF manuscript or complete manifesto edition.
The English Seaver/Lane1969 transcription and its arbitrary-letter restart passage
remain qualified references. No fixed historical duration is imposed. Pause/restart,
review, revision and metric controls are editorial software conventions.

Input requires integer `schema_version:1`, the exact `profile`, `task:"guided_writing"`,
`mode:"manual"`, a plain `session_id` and declared `state`. Optional `intention`,
`start_time`, `constraints`, `comments`, `associations` and `editorial_questions`
remain user supplied. Constraints are recorded, not interpreted as historical compliance.
No personal identity or belief data is required.

`events` is an ordered list with unique plain `id`, `type`, optional `timestamp`
and `comment`. Replay starts `prepared`. `begin` starts `writing`; `append` is legal
while `writing` or `resumed`; `pause`/`interruption` enter `paused`; `resume`/`restart`
return to `resumed`. `stop` enters `stopped` from any pre-review state, including
an unused prepared session. `review` enters `under_review` from `stopped`; `revise`
is legal only during review; `complete` is legal from stopped or under review.
No events follow completed. Final state must match the declared state.
`review_policy` is `optional` (default), `required` or `no_review`.

Every append event requires `segment:{id,order,text,authorship:"user"}` with optional
`timestamp` and integer `elapsed_seconds` (0..604800 or null). Segment orders strictly
increase without sorting. The original draft concatenates raw segment texts using
**an empty separator**, with no Unicode, whitespace or punctuation normalization.
An optional segment timestamp must equal its event timestamp if both are declared.
Comparable declared timestamps cannot decrease; naive and offset-aware clocks are
not implicitly equated. Dates and missing values do not imply a time of day.

Every revise event requires `revision:{id,parent,text,authorship:"user"}` and optional
`comment`. Parent is `first_draft` initially, then the immediately preceding revision
ID. Text and parent hashes remain independent; revisions never replace original
segments. Limits:512 events,256 segments,20000 code points per segment,200000 original
draft code points,32 revisions of up to200000 code points each. IDs are ASCII letters,
digits, dot, underscore or hyphen, max64, beginning with a letter or digit.
Append-only validation is within a supplied log; this CLI has no persistent storage
or cross-file authentication. Keep replay files to preserve a version history.

Character counts use Unicode code points, not visual graphemes. Words are maximal
non-whitespace runs under Python's Unicode whitespace convention; punctuation and
emoji stay in tokens. Empty text has zero lines; otherwise line count is one plus
CRLF/CR/LF delimiters (CRLF counts once; trailing empty line counts). Duration uses
declared begin/stop datetimes only, including pauses. Missing endpoints, dates or
mixed timezone awareness yield unavailable. Integer microseconds retain exact
duration; the seconds field is a floating display. A separately declared interval sum is
available only when every segment supplies it; no typing speed or active duration
is inferred. Events/authorship are declarations, not mental-state measurements.

JSON and Markdown contain the guided source subset, full event timeline, raw
segments, reconstructed original draft, revision history, objective metrics,
user reflection, evidence layers and portable canonical hashes/exact replay.
Markdown uses JSON string blocks for draft text so trailing spaces and original
line endings remain explicit and recoverable without trimming.
There is no generation, LLM, network call, diagnosis or supernatural-authorship test.
Moses's spiritualist accounts, the Breton/Soupault literary exemplar, ideomotor
methods and stream-of-consciousness remain distinct unsupported executable profiles.

Examples: [complete](data/automatic-writing-complete.md),
[interruption/restart](data/automatic-writing-interrupted.md),
[multiple revisions](data/automatic-writing-revisions.md),
[empty](data/automatic-writing-empty.md), [Unicode](data/automatic-writing-unicode.md),
[partial timing](data/automatic-writing-partial-timing.md),
[procedure](data/automatic-writing-procedure.md) and
[invalid ordering](data/automatic-writing-invalid.md).
Run `python -m scripts.verify_automatic_writing`,
`python -m scripts.smoke_automatic_writing_core` and
`python -m unittest tests.test_automatic_writing -q`.

## Akashic literature reference and reflection

`python -m future akashic-reference data/akashic-input.json --format markdown`

Profile `howe-public-reference-reflection-v1` supplies ten independently checked
Linda Howe public-page concept references: `records`, `pathway`, `opening`,
`closing`, `roles`, `conscious`, `question_framing`, `scope_limits`, `describe`
and `clinical_boundary`. Each includes source identity, exact webpage section,
practitioner attribution, conditions, limitations and unsupported claims. Unknown
IDs return explicit unsupported results without a substitute meaning.

The public procedure reference records two silent stanza repetitions and three
closing declarations. It links to the author's original prayer; no prayer text or
invented replacement is included. These webpages are distinct from the complete
2026 revised book and uncollated earlier editions. Author claims are documentary
evidence of her account, not evidence that a metaphysical archive exists.

Input requires integer `schema_version:1`, `task:"reference_reflection"` and
`mode:"manual"`. `profile` may select the exact profile or be omitted for that
default. Optional `concept_ids` selects references. Optional `question` contains
raw `text`, explicit `purpose` and explicit `form`; text never determines purpose.
Purposes are `personal_reflection`, `historical_research`, `creative_imagination`,
`factual_prediction`, `medical_clinical`, `unspecified` or `unknown`. Forms are
`open`, `yes_no`, `time_based` or `unspecified`. Declared purpose/form selects
relevant references through a transparent editorial mapping. Prediction and
clinical purposes return unsupported scope; the answer field remains null.

`reframe` is `none` (default), `open_reflection` or `source_research`. The selected
editorial alternative never replaces the original question or changes its purpose.
Optional `background`, `focus`, `intention` and `unknowns` remain user supplied.
`editorial_questions:false` suppresses optional reflective prompts.

Optional `session` contains a plain `id`, declared `state`, `timestamp` and ordered
`stages`. States are `prepared`, `in_progress`, `completed` or `discontinued`.
Stage IDs follow this order without duplicates or sorting: `source_review`,
`preparation`, `question`, `notes`, `concept_review`, `finish`, `reflection`.
Each declares `status` (`pending`, `completed`, `skipped`), optional `timestamp`
and `comment`. Stages may be omitted; omissions remain explicitly unrecorded.
Prepared sessions cannot contain completed stages. Completed sessions require an
explicit completed/skipped `finish` and no pending recorded stages. Discontinued
sessions may be empty. Comparable stage datetimes cannot decrease; naive and
offset-aware clocks are never implicitly equated.

All application stage tracking is editorial. Preparation/finish link source facts
without executing or certifying spiritual opening/closing. Participation, prayer,
legal names, religious commitment and extraordinary experiences are optional;
no personal identity, birth, medical or third-party information is required.

Up to64 `notes` preserve optional raw `text`, unique `id`, user-selected `kind`
(`reflection`, `association`, `imagined_scene`, `unanswered`), optional `timestamp`,
boolean `uncertainty` and up to16 source `concept_ids`. Imagined scenes are always
user-attributed, never retrieved historical records. Questions and note text allow
up to20000 Unicode code points; context fields10000; unknown entries2000, up to32.
Concept/comparison lists allow32 unique plain IDs, max80 ASCII letters/digits/dot/
underscore/hyphen, beginning with a letter or digit. All raw Unicode, whitespace,
nulls and omissions survive replay. No normalization or intent/emotion inference.

`comparisons` may record requested documentary profiles, but returns explicit
unsupported comparison coverage: separate Steiner/Cayce/Theosophical executable
profiles are deferred. Their traditions are not blended into Howe's procedure.
JSON and Markdown separate source, user, editorial and unsupported evidence,
include source/profile/content hashes and exact request replay. Markdown uses
JSON blocks so raw spaces and line endings remain recoverable. No LLM, generated
narrative, random component, remote service, new dependency or database is used.

Examples: [concepts](data/akashic-concepts.md), [guided reflection](data/akashic-guided.md),
[reframing](data/akashic-reframed.md), [user imagination](data/akashic-creative.md),
[unknown concepts](data/akashic-unknown.md), [prediction scope](data/akashic-prediction.md),
[empty/discontinued](data/akashic-empty.md), [deferred comparison](data/akashic-comparison.md)
and [clinical scope](data/akashic-clinical.md).
Run `python -m scripts.verify_akashic`, `python -m scripts.smoke_akashic_core`
and `python -m unittest tests.test_akashic -q`.

## Augury: Roman bird-sign source-condition reference

`python -m future augury data/augury-input.json --format markdown`

Profile `cicero-falconer1923-roman-bird-signs-v1` compares manual observations with14 frozen source/context records from Falconer's1923 *De Divinatione*. Four main conditions separate crow-left/raven-right calls inI.7.12 from explicitly favorable flight examples inI.39.85. A fifth condition represents conflicting translator note226. Nine contextual references retain Quintus's defense, Marcus's criticism, note133 classifications, public authority and weather-analogy limits.

Copy the profile/catalog ID/version/hash from `data/augury-input.json`. `task:"observe"` takes one to8 ordered `observations`, each with a distinct `observation_id`. Bird labels are source English labels (`crow`,`raven`) or raw unsupported/unknown labels; no Latin-name or scientific-species inference. Declare `phenomenon`, `relative_side`, `relation` and `reference_frame` explicitly when known. Missing values remain unknown. Calls require `located_on_side`; Falconer's flight-to examples require `moving_to_side`. `moving_from_side` and merely located-on flight are not silently equivalent. LatinI.39.85 itself has no explicit flight verb; this translation-specific convention is recorded separately.

The supported comparison frame is declared `observer_relative`. Unknown frame remains insufficient; `cardinal` is retained as an unsupported declaration, without conversion. `observer_facing` is optional declared N/NE/E/SE/S/SW/W/NW/unknown and never fills a missing frame. Explicit `side_reports` can expose conflicting declarations; named `uncertain_fields` prevent those required fields from producing a confident match. Raw prose is not interpreted to infer observations or contradictions.

Results distinguish applicable,not_applicable,insufficient_evidence,conflicting_evidence and unsupported. Applicable means source-condition compatibility. Calls never inherit flight polarity. A crow-left call can match the main text while overall evidence remains conflicting because note226 gives crow-right; a matching note never becomes consensus. No unmatched/opposite input is labeled unfavorable. Main-text favorable IDs identify quoted historical wording, not predictions.

Optional origin (`reported_real`,`hypothetical`,`unknown`), user-attributed modern species, setting, sequence, uncertainty, description and reflection stay separate from source facts. Request question/reflection/notes preserve raw Unicode/whitespace. No observation confers Roman public authority, including a user-declared public setting. `task:"reference"` takes exact `reference_ids`; `task:"catalog"` lists all14 records without observations. Multiple observations receive neutral comparison only, never a combined omen.

Pinned profile/catalog/source hashes and full requests support exact offline JSON/Markdown replay. Greek narrative runtime, Kynes symbolism, compass conversion, weather forecasting, bird identification, generation and factual prediction are unsupported. Source/Latin notes and independent fixtures: `knowledge/augury_source_freeze_v1.json`, `knowledge/augury_translation_notes_v1.json`, `tests/fixtures/augury_reference_v1.json`. Checks: `python -m scripts.verify_augury` and `python -m scripts.smoke_augury_core`.

## Cleromancy: Greek Alphabet Oracle single declared lot

`python -m future cleromancy data/cleromancy-input.json --format markdown`

Profile `opsopaus-greek-alphabet-manual-lot-v1` provides all24 source-order Greek marked lots from John Opsopaus's public *A Greek Alphabet Oracle*. Each mark has an original concise source-attributed account, lexical qualifications and exact row locator. This supplementary webpage is distinct from the ranked *The Oracles of Homer and the Bones* and the2017 *Oracles of Apollo*. Full author-origin indexed text was inspected; fresh canonical/www requests failed TLS certificate verification, so the raw HTML hash is explicitly unavailable. Original inscription attribution remains author-attributed pending epigraphic collation. No full modern translation/commentary is bundled.

Copy the exact profile/catalog ID/version/hash from `data/cleromancy-input.json`. Use `mode:"manual"` and `task:"reading"` with one `mark`, such as `gao-alpha`, `Alpha`, `Α` or `α`. `task:"lookup"` returns the same source record; `task:"catalog"` omits `mark` and lists the full ordered catalog. The runtime verifies pinned profile/catalog hashes before lookup. Changed meanings, ordering, editions or aliases require a new profile.

Alias policy is versioned: ASCII edge whitespace trim, NFC only, ASCII-name/ID case normalization and explicit Greek glyph aliases. There is no NFKC or visual-confusable folding: Latin `A` and Cyrillic lookalikes do not mean Greek Alpha. Source display `Khi` is preserved; same-author `Chi` is accepted. Ordinary/final sigma `σ`/`ς` both resolve to Sigma, with final sigma labeled an editorial orthographic alias rather than a separate lot.

`observation_origin` is `reported_real`, `hypothetical` or `unknown` (default). This is user-reported provenance, never a verified physical or generated draw. Optional `question`, `association`, `reflection`, `notes` and `uncertainty` preserve raw UTF8/whitespace separately from the source account. No selection probability or automatic application is generated. Questions do not change the declared mark or its meaning.

Numeric and multiple-draw modes remain unsupported. The source's impossible five-astragaloi face5 example, reversed numeric-column wording, missing five-d6 sums25/13 and distinct tuple/multiset/sum spaces are retained explicitly. No full56-outcome Astragalomanteion, Homeric passage mapping, seeded selector, diagnosis or factual prediction is supplied.

Source/fixtures precede executable lookup: `knowledge/cleromancy_source_freeze_v1.json`, `tests/fixtures/cleromancy_reference_v1.json`. Standalone catalog check: `python -m scripts.verify_cleromancy --catalog-only`; full independent check: `python -m scripts.verify_cleromancy`; CLI/replay check: `python -m scripts.smoke_cleromancy_core`.

## Bibliomancy: edition-pinned manual sentence selection

`python -m future bibliomancy data/bibliomancy-input.json --format markdown`

Profile `mascaro2022-manual-coarse-webclassic-ruth-v1` is a **digital manual coarse-selection adaptation** of J. R. Mascaro's sentence-selection procedure. It contains the complete Book of Ruth from World English Bible Classic 2020: 85 native verses and 141 independently reviewed sentence units. Four original public-domain HTML witnesses are retained byte-for-byte. WEB's faithful-copy trademark condition is separate from the public-domain text; editorial whitespace/indexing does not change source wording or punctuation.

Requests must provide the exact profile, corpus/index IDs, integer versions and canonical hashes shown in `data/bibliomancy-input.json`. A selection is `{"path":[1,1,2,1]}`: one-based shelf, book, **editorial logical page**, sentence. This first profile has one shelf and one book. Page1 contains the source heading and no selectable sentence; pages2–5 correspond to Ruth chapters1–4. They are not printed pages. A sentence can cross verse lines, and multiple sentences can cite the same verse. An optional `sentence_id` asserts the exact identity at a path.

Supply one to32 ordered `selections`; repeats remain separate. `context` is0–2 neighboring sentence units on each side, clipped to the same chapter page, default1. Optional `question`, `reflection`, `notes` and per-selection `reflection` preserve raw Unicode/whitespace separately from exact source text. Invalid/empty paths, booleans, floats, unknown editions, hash mismatches and changed corpus/index/raw witnesses are rejected without rerolling. The runtime verifies pinned source/index/profile identities on every report and requires no network or RNG. User-entered choices carry no generated-draw probability claim.

`mode:"homeric_index_reference"` instead takes three ordered `faces` in1..6, using the same profile but without corpus selectors. It reports an editorial one-based ordinal and historical witness context. All216 indices are verified; **zero tuple-to-verse mappings are supplied**, so the passage remains unavailable. This supplemental numerical reference is distinct from a complete Homeric oracle or general Cleromancy engine.

Fine-word synthesis, seeded draws, other corpora/editions, rendered-line selection and automatic predictions are unsupported. Mascaro's seventeen-book digit example and fine-word-count dice/digital discrepancy remain documented rather than silently repaired. Fresh publisher requests returned403; the procedural reference is explicitly publisher-indexed text, with no invented successful snapshot hash.

Corpus/index/source freezes: `knowledge/bibliomancy_corpus_freeze_v1.json`, `knowledge/bibliomancy_index_v1.json`, `knowledge/bibliomancy_source_freeze_v1.json`. Independent verification: `python -m scripts.verify_bibliomancy`; CLI/replay checks: `python -m scripts.smoke_bibliomancy_core`.

## Osteomancy: historical Shang inscription references and comparisons

`python -m future osteomancy data/osteomancy-input.json --format markdown`

`columbia-afe1999-shang-charges-v1` covers thirteen labelled AFE excerpts citing
the 1999 second-edition anthology *Sources of Chinese Tradition*, volume 1,
compiled by Wm. Theodore de Bary and Irene Bloom. It retains short original factual
annotations and source references. These specific translations are not attributed
to Keightley's book, and the complete translated excerpt collection is not bundled.

```json
{
  "schema_version": 1,
  "profile": "columbia-afe1999-shang-charges-v1",
  "mode": "documentary",
  "task": "compare",
  "case_ids": ["19A", "19B"]
}
```

Tasks are `reference` (1–13 ordered distinct exact labels), `compare` (2–13 labels,
all selected pairs), `group` (one named verified group) and `topic` (one frozen
editorial topic). Group/topic requests use only their corresponding selector.
Groups are `ancestor-harm`, `settlement`, `royal-approval`, `harvest` and `warfare`.
Topic names and groups are included in reports. Unknown IDs, mixed selectors,
duplicate selections and unsupported tasks are rejected with CLI exit 2.

Dates, diviners, charge/condition, translation uncertainty, prognostication and
recorded verification remain distinct components. Missing excerpt fields do not
establish absence on the original artifact; a charge does not demonstrate that
an event occurred. Both 20A and 20B preserve an unresolved action. The settlement
pair has different conditions and day labels; 24A/24B concern distinct propositions.
No relationship is inferred from A/B suffixes. Uncatalogued pair relationships remain
unresolved even when editorial topic tags overlap. Canonical comparison facts are
stable when selection order reverses; original request order remains in replay.

Optional `notes`, `research_question`, `research_id` and `annotations` preserve
user text separately. An annotation names a selected `case_id` and supplies a
`note` and/or `association`; source fields cannot be overridden. JSON and Markdown
include source/profile/request hashes and complete deterministic offline replay.
No modern charm toss, Southern African executable method, original-script/crack
classification, physical reenactment, artifact authentication, outcome prediction
or absolute date conversion is supported.

Independent checks: `python -m scripts.verify_osteomancy`. CLI and saved replays:
`python -m scripts.smoke_osteomancy_core`.

## Lithomancy: Howard general-set manual spatial reading

`python -m future lithomancy data/lithomancy-input.json --format markdown`

The `howard-cottage-web-general-set-v1` profile covers all twelve objects in
Jessica Howard's public example general set, with source-located associations and
nearest-to-personal-stone or nearest-to-reader priority. The web guide is a separate
witness from her book. Its adjustable set and distant-object exception remain explicit.

```json
{
  "schema_version": 1,
  "profile": "howard-cottage-web-general-set-v1",
  "task": "manual_spatial_reading",
  "mode": "manual",
  "reading_id": "example",
  "frame": "integer-centers-x-right-y-up-v1",
  "coverage": "subset",
  "origin": "hypothetical",
  "stones": [
    {"id": "self", "role_id": "lodestone", "position": {"x": 0, "y": 0}},
    {"id": "caution", "role_id": "onyx", "position": {"x": 3, "y": 4}}
  ],
  "anchor": {"kind": "personal_stone", "stone_id": "self"}
}
```

Declare `coverage: "full_example"` for all twelve unique roles, or explicitly use
`subset` for 1–12 roles. A reader anchor uses `{"kind":"reader","position":{"x":0,"y":0}}`.
An omitted/null anchor or omitted/null position remains unknown. Personal-anchor
selection is explicit; the source's Lodestone example is not an automatic default.
Objects have unique instance IDs and unique source-role IDs. Source associations
and optional raw user associations remain separate.

The named integer grid, center-point model and squared Euclidean metric are
editorial conventions. Both axes share an arbitrary unit, bounded to ±1,000,000.
The alternate `integer-centers-x-right-y-down-v1` frame changes descriptive vertical
direction; it adds no symbolic meaning. All equal distances retain priority together;
coincident centers imply no physical overlap. Unknown eligible positions make the
nearest-known result partial. Far objects are retained in the reading.

Reports show exact proximity groups, source associations, pairwise distances, ties,
unknown/conflicting evidence and full replay with hashes. Optional `groups` contain
user-selected ID/member lists and associations; no combined fortune is generated.
Optional `relations` declare from/to IDs and left/right/above/below/coincident/near/far/unknown;
direction claims are checked against coordinates, while near/far remain unquantified.
Question/intention/commentary and stone associations preserve raw Unicode/whitespace.

No universal thirteen-stone system, sea-set direction symbolism, Wimmer circle
rules, automatic clusters, seeded casting, image recognition or physics is supported.
Exact geometry does not establish divinatory accuracy. Independent checks:
`python -m scripts.verify_lithomancy`; CLI/replay checks:
`python -m scripts.smoke_lithomancy_core`.

## Western Geomancy: historical mathematical shield construction

`python -m future geomancy data/geomancy-input.json --format markdown`

The manual `turner1655-common-shield-v1` profile implements the sixteen identities
in Turner's 1655 printed figure table and the complete fifteen-position common
shield. Four Mothers produce four Daughters by row transposition, four Nieces,
two Witnesses and a Judge by line-by-line parity addition. Reports name every
figure and show its parent dependencies, source locators and row-level trace.
A correct Judge does not establish a reliable yes/no answer or prediction.

```json
{
  "schema_version": 1,
  "profile": "turner1655-common-shield-v1",
  "task": "shield",
  "mode": "manual",
  "input_mode": "patterns",
  "mothers": ["2121", "1221", "1121", "2122"]
}
```

Rows run top-to-bottom: `1` means one dot/odd, `2` means two dots/even.
Repeated Mothers are allowed. Instead of patterns, `input_mode: "mark_counts"`
accepts `mark_counts` with sixteen positive integers, grouped by Mother then row;
original counts remain in the report. `input_mode: "figure_ids"` accepts four
`figure_ids` using exact IDs, names or listed aliases, case-insensitively.
Counts must be 1–1,000,000; booleans, floats and mixed modes are rejected.

The optional `figure_convention` is `turner1655-p3-top-down-v1`. This convention
assigns Puella `1211` and Puer `1121`; other traditional tables remain separate.
`layout` accepts `right_to_left` (default) or `left_to_right`, changing display
only. Optional question/commentary/association text preserves Unicode and whitespace.
For all sixteen figures, use `task: "figure_catalog"` without shield input fields;
an optional `lookup` array selects 1–16 exact names, IDs, aliases or patterns.

JSON and Markdown include full deterministic replay and source/profile/request
hashes. Source evidence is the original Wellcome 1655 scan, collated with Princeton;
Bennett's published chart is an independent numerical fixture. Greer and Skinner
remain ranked references with procedural access gates. House charts, Arabic-specific
profiles, horary judgment, dignities, seeded generation and a sixteenth super-judge
are unsupported in this release. No new dependency or random protocol is introduced.

`python -m scripts.verify_geomancy` checks all 65,536 Mother combinations against
an independent bit-matrix reference, all 256 figure pairs and 4,096 associativity
triples. `python -m scripts.smoke_geomancy_core` checks the CLI and saved replays.

## Aeromancy: regional historical atmospheric-lore comparisons

`python -m future aeromancy data/aeromancy-input.json --format markdown`

`inwards1898-atmospheric-lore-subset-v1` uses the exact inventory Commons scan
of Richard Inwards's *Weather Lore*, third edition, revised and augmented,
London: Elliot Stock, 1898. Thirteen cases retain individual/regional
attributions. Inwards is the compiler; the collection includes differing
sayings rather than one unified theory. Tyson's atmospheric chapters remain
access-gated and supply no executable rules here.

```json
{
  "schema_version": 1,
  "profile": "inwards1898-atmospheric-lore-subset-v1",
  "task": "atmospheric_lore_comparison",
  "mode": "manual",
  "origin": "hypothetical",
  "region": "scotland",
  "observations": [{
    "id": "o1", "phenomenon": "smoke",
    "features": {"smoke_drift_towards": "east"}
  }]
}
```

Cases cover Scottish smoke travel, Wing's continued south wind, the qualified
Texas south-wind sequence, Bedfordshire hake-cloud axes, the complete Scottish
fleecy-cloud pattern, mackerel sky with mares-tails, and five separate
mackerel-sky accounts. Printed source pages and historical horizons accompany
every case. No actual weather or forecast is established.

Direction fields are independent: `named_wind_direction` and
`prior_wind_direction` use an explicitly declared
`wind_direction_convention: "from"`; `smoke_drift_towards` is the direction
smoke travels; `cloud_axis` is an undirected east-west or north-south axis.
The engine never converts among them. Cloud motion does not determine axis.

The Texas entry requires dry weather, current light south wind lasting five
or six days, and prior strong wind from the same direction. The interval is
the current light-wind duration, **not a delay after the prior strong wind**.
Use `light_wind_duration_days`, `prior_wind_direction` and
`prior_wind_strength`. Wing's `wind_continuity: "considerable_time"` remains
qualitative without a generated numerical threshold.

Fleecy-cloud matching requires `cloud_appearance: "fleecy"`, `cloud_light: true`,
`cloud_motion: "rapid"`, `relative_cloud_layer: "below"`,
`upper_cloud_type: "cirro_stratus"`, `upper_cloud_dark: true` and
`upper_cloud_compact: true`. The mackerel combination requires both
`mackerel_sky: true` and `mares_tails: true`. False explicitly denies a feature;
absence/null/unknown does not. Bounded feature alternatives retain conflicts.

Reports distinguish observational matching, regional applicability and
unestablished empirical validity. An observational match can retrieve a
historical account while its regional qualification is unknown or mismatched.
Unknown region never becomes Scotland, Bedfordshire, Texas or Britain.
Unspecified source origin is not worldwide applicability. Competing mackerel
sayings remain separate without averaging, priority, confidence or a winner.

Inputs preserve ordered unique IDs, optional increasing sequence, declared
origin/region/timestamp, raw descriptions, uncertainty and personal associations.
No text, image, location or present-weather inference occurs. Optional
`include_reference_catalog: true` produces a source-reference report without
observations. JSON/Markdown include exact replay and canonical request/profile
hashes plus the original PDF byte hash. No API, RNG, renderer, LLM or new
dependency was added. Historical sailing/storm statements are documentary
folklore and supply no operational navigation or safety guidance.

Run `python -m scripts.verify_aeromancy`,
`python -m scripts.smoke_aeromancy_core` and
`python -m unittest tests.test_aeromancy`. Examples:
[smoke](data/aeromancy-smoke-east.md), [cloud axis](data/aeromancy-hake-ew.md),
[compound clouds](data/aeromancy-fleecy-full.md),
[competing sayings](data/aeromancy-mackerel-competing.md),
[Texas sequence](data/aeromancy-texas.md) and
[regional mismatch](data/aeromancy-region-mismatch.md).

## Hydromancy: water-specific observation and reference conditions

`python -m future hydromancy data/hydromancy-input.json --format markdown`

`andrews-spees2005-water-reference-v1` uses the **Ted Andrews** Water Scrying
excerpt within Jennifer Spees's July 1, 2005 publisher article. The excerpt
is distinct from the article's discussion of Donald Tyson. Tyson and Betz
retain their inventory rankings; their full methods remain access/rights gaps.

```json
{
  "schema_version": 1,
  "profile": "andrews-spees2005-water-reference-v1",
  "task": "water_observation_reference",
  "mode": "manual",
  "origin": "hypothetical",
  "session": {
    "medium": "water", "container": "dark_bowl", "rainwater": true,
    "gaze": "soft", "observer_undisturbed": true, "surface_visible": true
  },
  "observations": [{
    "id": "o1", "sequence": 1,
    "category": "perceived_fogginess", "basis": "subjective",
    "description": "My own voluntary observation"
  }]
}
```

Eight source cases compare three rainwater contexts (dark bowl, cauldron,
natural pool), observer positioning, relaxation, soft/half-focused gaze,
explicit subjective fogginess and subjective imagery. Results use
`source_supported`, `context_mismatch`, `insufficient_information`,
`conflicting_evidence` or `unsupported`. Source conformity concerns declarations;
it establishes no ritual success, physical cause or extraordinary ability.

Water-only context, rain provenance and vessel are explicit. Oil-on-water
and oil-only contexts remain distinct. Unknown medium never defaults to water.
The source's undisturbed-observer instruction does not require still water:
surface motion is separately recorded. Intense gaze mismatches its recommendation.

Observations require unique IDs and increasing explicit sequence numbers.
Categories separate physical ripples, reflections, glare, physical mist,
subjective fogginess/images, deliberate imagination, no imagery and oil layers
or drops. Optional `basis`, origin, uncertainty, category alternatives, raw
description and association remain user declarations. Per-observation `context`
overrides only supplied session fields. No prose or image inference occurs.
Scalar context fields can carry bounded evidence alternatives or null/unknown.
Color and drop counts can be recorded without receiving invented omen meanings.

Optional session intention/question, lighting, timestamp, discomfort and status
are preserved without a clock default. Discontinued/discomfort/stopped declarations
hold displayed subjective symbolism and reflection prompts. No unusual imagery,
physical water, collection of rainwater or special equipment is required.

`documentary_comparison: true` requests a separate comparison with Kyprianos
T1085 (fragmentary Coptic witness catalogued 901–1100). Its uncertain medium
identification, editorial layers and gaps remain explicit. It is neither an
executable ritual nor a verified Betz corpus alignment. NOAA oil/water context
is educational physical material, separate from practitioner symbolism.

Reports preserve direct-source, user-attributed, editorial and unsupported
evidence layers, exact source locators/rights and full deterministic replay.
Canonical request/profile hashes and original source-byte hashes are included.
No renderer, fluid model, recognition, LLM, RNG or new dependency was added.

Run `python -m scripts.verify_hydromancy`,
`python -m scripts.smoke_hydromancy_core` and
`python -m unittest tests.test_hydromancy`. Examples:
[water bowl](data/hydromancy-water-bowl.md),
[perceived fog](data/hydromancy-fog.md),
[physical mist](data/hydromancy-mist.md),
[oil/water](data/hydromancy-oil-water.md) and
[historical comparison](data/hydromancy-coptic.md).

## Pyromancy: public-source candle and jar-soot observations

`python -m future pyromancy data/pyromancy-input.json --format markdown`

The immutable `pamita-public2026-candle-observation-v1` profile uses three
Parlour of Wonders practitioner articles dated July 14, 2026. They are separate
public witnesses from Pamita's ranked 2020 book. Six selected source cases
cover persistent high/low candle flames and narrow glass-jar soot patterns.
The software works with hypothetical or previously recorded observations.

```json
{
  "schema_version": 1,
  "profile": "pamita-public2026-candle-observation-v1",
  "task": "symbolic_candle_observation",
  "mode": "manual",
  "origin": "hypothetical",
  "observations": [{
    "id": "flame1",
    "phenomenon": "flame",
    "attributes": {
      "substrate": "candle_flame",
      "height": "high",
      "persistence": "persistent"
    },
    "physical": {
      "explanation": "addressed",
      "correction": "reported_completed",
      "after_correction": "persisted"
    }
  }]
}
```

Physical explanations use `known`, `possible`, `not_noticed`,
`checked_no_issue`, `addressed` or unknown evidence. Known/possible unresolved
causes prevent the conditional symbolic account. No cause noticed remains
insufficient evidence. Current wick, draft, dressing or construction concerns
cannot be cleared by a contradictory favorable summary. All checks and
corrections remain user declarations; the software verifies no physical cause.

The tall-flame case requires reported correction and persistence afterward.
The low-flame case also permits an explicit checked/no-issue declaration with
`not_needed_after_check`. In this schema, `improved`/`changed` means the
selected abnormal height resolved; it conflicts with a current `persistent`
declaration. Missing or competing evidence remains explicit.

Soot requires a declared `glass_jar` substrate. Upper black deposits with clear
lower glass have a selected source account; dense upper deposits and light
grey haze have narrower qualifications. Dense full-jar black deposits remain
distinct. Unknown density never supplies a density-specific account. Live
smoke, embers, ancient lamp rites and flame-color meanings are unsupported.
`flame_color`, `wax_color` and `soot_color` are separate declarations.

Optional safety flags are `unsafe_burning`, `overheating`, `active_hazard` and
`stopped`, at session or observation level. Any hazard declaration holds all
displayed symbolic accounts and reflection prompts, prioritizing stopping
safely or keeping a stopped activity stopped. Reports give no hot-equipment
handling instructions. Unknown safety is not clearance for physical activity.

Observations preserve input order, unique IDs, optional increasing sequence,
origin, uncertainty, feature alternatives and exact raw Unicode/whitespace.
The four evidence layers distinguish source accounts, user declarations,
editorial comparisons and unsupported factual claims. JSON/Markdown carry
complete replay requests and portable request/profile/source hashes. No RNG,
renderer, LLM, image recognition or runtime dependency was added.

Run `python -m scripts.verify_pyromancy`,
`python -m scripts.smoke_pyromancy_core` and
`python -m unittest tests.test_pyromancy`. Examples include
[persistent flame](data/pyromancy-tall-persistent.md),
[physical explanation](data/pyromancy-tall-physical.md),
[upper soot](data/pyromancy-upper-soot.md),
[full jar](data/pyromancy-full-soot.md),
[safety hold](data/pyromancy-unsafe-stopped.md) and
[documentary lamp context](data/pyromancy-lamp.md).

## Coffee grounds: Turkish historical symbolic comparisons

`python -m future coffee-reading data/coffee-input.json --format markdown`

The immutable `coffee-ayvazoglu-seyhun2011-subset-v1` profile uses Beşir
Ayvazoğlu's *Turkish Coffee Culture*, translated by Melis Şeyhun (2011),
Chapter XIV, printed pages 103–104. It is a bounded historical reference:
seven motif identities and eight conditional vessel cases. Bal's full book,
Balkan profiles and regional charts remain separate source/access gaps.

```json
{
  "schema_version": 1,
  "profile": "coffee-ayvazoglu-seyhun2011-subset-v1",
  "task": "symbolic_coffee_reading",
  "mode": "manual",
  "vessel": "cup",
  "rotation": "clockwise",
  "intention": "self",
  "observations": [
    {"id": "camel1", "symbol_id": "camel", "half": "subject_facing",
     "attributes": {"humps": 2}}
  ]
}
```

The subject-facing cup half has the source association `subject_abode`;
the opposite half has `others_abode`. Rotation expresses a separate reported
stirring convention, clockwise/self and counterclockwise/another. Neither
determines orientation from a handle. Unknown orientation remains unresolved.

Motifs: `adhered_grounds` requires declared adhesion after inversion;
`line` requires flat shape, three dots and `at_line_end` arrangement;
`bird` requires a stain at `peak_of_bird_figure` (literal translation,
without a silent correction to beak); `camel` requires two humps;
`horse` and `fish` have the selected cup associations. `moon_patch` requires
`moon_shaped` shape and white color, plus bottom location for a cup. The
saucer moon case has no source-defined finer location requirement. Other
selected motifs on a saucer are unsupported.

Each observation may override the request vessel. Optional `half`, shape
attributes, raw `observation`, `association`, identity `alternatives` and
boolean `uncertainty` retain user declarations. Attribute values can be
scalars or up to four distinct alternatives; null/unknown evidence stays
unresolved, contradictory known alternatives are explicit conflicts.
Fields and bounds are validated; no shapes or preparation are inferred
from raw text. Optional `preparation` flags, `context` and `notes` remain
user-attributed. There is no turn count or cooling timer.

Reports separate direct source accounts, user declarations, editorial
matching and unsupported claims. Three travel periods retain days/months/years
as alternatives without selecting a unit or computing a deadline. JSON and
Markdown carry exact replay data, canonical request/profile hashes and the
original PDF byte hash. Public hosting does not license redistribution of
the booklet, English translation, photographs or source charts.

Run `python -m scripts.verify_coffee`, `python -m scripts.smoke_coffee_core`
and `python -m unittest tests.test_coffee`. Examples include
[conditions](data/coffee-camel.md), [cup halves](data/coffee-halves.md),
[saucer](data/coffee-moon-saucer.md), [timing](data/coffee-timing.md) and
[documentary comparisons](data/coffee-documentary.md).

## Tasseography: Kent ordinary-cup symbolic reading

`python -m future tasseography data/tasseography-input.json --format markdown`

Profile `kent-pg6964-ordinary-cup-v2` implements14 manually selected identities and
23 source cases from Kent's PG6964 digital witness (posted2013-03-21),plus an
explicit FigureVIII documentary comparison. Print pagination is not authenticated.
The original source-only v1 freeze is retained for provenance and is unsupported
by the engine: v2 distinguishes a postal-letter mark from an alphabetic initial.
No whole book,modern copyrighted dictionary,scan or source artwork is bundled.

Required fields: integer `schema_version:1`, exact `profile`,
`task:"symbolic_cup_reading"`, `mode:"manual"`, `vessel:"cup"`.
Optional `handle_orientation` is `top`, `right`, `bottom`, `left` or `unknown`.
It is recorded only;no absolute position or sector is calculated. Optional
`context` contains declared `musician`/`sailor` booleans or null,
`marital_status` (`married`, `unmarried`, `unknown`) and `abode` (`home`, `away`,
`unknown`). These personal facts are optional and never inferred from prose.

Up to64 ordered `observations` require unique plain `id` and `symbol_id`.
IDs: `aircraft`, `apron`, `acorn`, `anchor`, `organ`, `beetle`, `tea_cosy`,
`coal_scoop`, `bird`, `letter`, `numeral`, `dots`, `cross`, `postal_mark`.
Other plain IDs return unsupported references. Organ is not Barrel Organ;
the coal-scoop documentary case is not Coal Scuttle's dictionary meaning.
Postal marks have no standalone meaning in this subset;they participate in the
selected bird/telegram account.

Named `region` values are `rim`, `side`, `bottom`, `bottom_circle`,
`bottom_centre`, `unknown`. Up to3 distinct `region_alternatives` preserve
ambiguous placement. The bottom subregions retain FigureVIII circle/centre
labels;no numeric boundary is invented. Optional `handle_relation` is
`under_handle`, `near_handle`, `opposite` or `unknown`;`proximity` is `near`,
`far` or `unknown`. Source depth timing is qualitative. Under-handle
present/immediate and depth timing remain separate when they overlap;no priority
or calendar date is computed. Saucer/Nelros/coffee methods reject explicitly.

Optional conditions include `heading` (`towards_handle`, `away_from_handle`,
`other`, `unknown`), `motion` (`flying`, `stationary`, `unknown`), `size`
(`small`, `large`, `unknown`), `clarity` (`clear`, `indistinct`, `unknown`),
`multiplicity` (`single`, `several`, `unknown`) and `arrangement`
(`surrounding`, `other`, `unknown`). Several is an observer-declared source
quantifier,not an invented numeric threshold;separate observations are not
silently aggregated. Source clarity/size qualifications produce no confidence or
personality score. A lone-cross declaration conflicting with another selected
cross remains unresolved.

`adjacent_to` lists existing observation IDs. A supplied list is a complete
neighbor declaration;omission means unknown. One-sided positive assertions
suffice unless contradicted by another supplied list. No distance or relationship
is inferred from coordinates,region membership or prose. Surrounding dots require
both declared `arrangement:"surrounding"` and an associated symbol;ordinary
adjacency alone is insufficient. Bird cases require the postal mark,not an initial.
Alphabetic `letter` may carry `mark`: one Latin letter,blank or null. Other glyphs
can remain raw observations. `numeral` may carry integer `numeral`0..1000000000;
only the documented dots/quantity association is supported,no deadline,currency
or actual gain inferred.

`uncertainty:true` or up to4 competing identity `alternatives` block definitive
case selection. Statuses are `applicable`, `not_applicable`,
`insufficient_information`, `conflicting_evidence`, `unsupported`. Reports retain
condition results,missing inputs,competing accounts and independent zone
qualifications. An unconditional case does not fill missing conditions for a
different case. Unknown source contexts never trigger invented defaults.

Optional `source_example:"figure_viii"` compares explicitly entered placements
with Kent's original example. Its organ/acorn adjacency,lower-circle positions and
musician qualification remain separate from general dictionary alternatives.
The example's central tea-cosy account does not imply a user's marital status.
The diagram was inspected as an original source;the program does not recognize
its shapes. FigureVIII coal-scoop account also requires the observed beetle.

Optional raw `observation`/`association` fields allow10000 Unicode code points;
root `notes` allows10000. IDs allow80 ASCII letters/digits/dot/underscore/hyphen,
beginning with a letter or digit. Raw whitespace,Unicode,omissions and nulls are
preserved. JSON/Markdown include historical accounts,conditions,qualitative timing,
editorial synthesis,four evidence layers,source/profile hashes and exact replay.
Historical fortune claims are attributed statements,not empirically verified
events,medical conclusions or personality assessments. Geometry,seeds,photographic
recognition,fluid simulation,Nelros,Turkish methods and modern dictionary remain
unsupported and are not release prerequisites.

Examples: [basic](data/tasseography-basic.md), [zones](data/tasseography-zones.md),
[handle overlap](data/tasseography-handle.md), [direction](data/tasseography-direction.md),
[multiplicity](data/tasseography-multiplicity.md), [adjacency](data/tasseography-adjacency.md),
[competing evidence](data/tasseography-conflicting.md), [missing context](data/tasseography-missing.md),
[Kent FigureVIII comparison](data/tasseography-figure-viii.md),
[initials/numerals](data/tasseography-marks.md) and [empty](data/tasseography-empty.md).
Run `python -m scripts.verify_tasseography`, `python -m scripts.smoke_tasseography_core`
and `python -m unittest tests.test_tasseography -q`.

## Remote Viewing: offline blinded trial protocol

`rv-air1995-five-choice-blind-trial-v1` implements a five-candidate experiment
record workflow. It supplies no hidden information, visions, predictions or
psychic proficiency score. Historical CRV Stage I–VI labels are optional record
annotations; AIR1995 supplies the blind-rank reference. Packet schemas, hashes,
state transitions and exclusion rules are explicit Future editorial policies.

Use `python -m future remote-viewing REQUEST.json --asset-root D:/Future`.
Requests have `schema_version:1`, `profile:"rv-air1995-five-choice-blind-trial-v1"`
and a `task`. `--format markdown` renders the same exact result JSON.
See `knowledge/remote_viewing_profile_v1.json` for frozen fields and policies.
The checked examples under `data/remote-viewing-*-input.json` are runnable requests.

1. `task:"create"` takes `plan`, and either a simulated-only `seed` or a manual
   `target_id`. OS-uniform assignments take neither. A plan fixes all five assets,
   rights, participants, knowledge, presentation order, trial IDs, stopping,
   scoring and reuse policies before assignment. The result contains a **private**
   `trial`. Save it separately; transfer only designated blind packets.
2. `task:"apply"` takes `trial`, `action`, `actor`, timezone-aware `at`, and exact
   `payload`. Actions follow `commit`, `start`, `entry`, `lock_viewer`,
   `start_judge`, `rank`, `lock_judge`, `reveal`, `report`. Entries preserve raw
   UTF8 text/whitespace. Obtain lock payloads with the Python API
   `lock_digest(trial,"viewer")` / `lock_digest(trial,"judge")`. Every planned
   judge must submit a complete alias-to-rank permutation before the judge lock.
3. After `commit`, `task:"viewer_packet"` takes only the private trial and returns
   an allowlisted blind packet. After viewer lock, `task:"judge_packet"` also takes
   `judge_id`. `--export-dir NEW_DIRECTORY` writes only `packet.json` and neutral
   PNG names, with exact hashes; it refuses private results or an existing directory.
   Never transfer the private request, tasker package, original paths or source folder.
4. `reveal` requires the tasker and `payload:{"preimage":...}` from the private
   `preimage(trial)` API. It opens the commitment only after both locks. `report`
   requests return public status before reveal; after reveal they return a clearly
   **private** report with exact trial replay, full history and each judge’s rank.
   Manual assignments receive no verified uniform/chance-qualified designation.
5. `task:"summary"` requires **every** trial in the predeclared `trial_ids` ledger.
   It retains aborted, invalid, leaked, excluded, conflicted and rejected attempts,
   reports descriptive metrics separately for every judge, and computes no p-value.
   Reuse is rejected unless dependence was declared before the sessions.

An invalid action returns exit2 with an updated **private** trial containing the
hashed rejected attempt. Persist that returned trial, even on exit2. Rejected
creation/corrupt-input requests have a generic public error and no trusted trial
to amend. `terminate` records an explicit terminal `status` and `reason`; terminal
trials cannot restart. Rejected reveal attempts do not mean an actual disclosure
occurred. If exposure occurred outside the tool, record `terminate`/`leaked`.

The supported asset subset is metadata-free, noninterlaced 8-bit RGB PNG with
filter0 and exactly IHDR/one IDAT/IEND. All five candidates must have equal image
dimensions and distinct bytes. EXIF, textual/ancillary chunks, unsupported filters,
trailing bytes and corrupt CRCs are rejected. Prepare permission-cleared derivatives
externally when necessary; Core v1 does not claim automatic sanitization. Source
sidecars and filenames are never copied into the packet. Optional sketch attachments
use the same bounded PNG/rights checks and receive neutral exported names.

For OS selection, private one-byte entropy draws reject250..255 before modulo5;
all draws and a 256-bit nonce are logged privately. Fixed seeds are simulated only.
Digests use canonical sorted-key compact UTF8 JSON, preserve original text values,
and are domain separated. Commitments bind protocol, plan, pool, target/asset,
selection and nonce. Public transcript derivatives have their own checkable digest
in addition to the original private lock anchor. The owner can still rewrite an
entire local history; retain an independently held commitment and transfer packets
between separate participants/accounts/machines. Timestamps, identity, rights and
knowledge remain declarations. No externally witnessed status is certified.

Examples include `remote-viewing-rank1.md`, `remote-viewing-rank3.md`,
`remote-viewing-rank5.md`, `remote-viewing-multiple-judges.md`,
`remote-viewing-human-manual.md` and `remote-viewing-failure-retained.md` in `data/`.
Human-origin examples demonstrate a declared record schema; no human study was
conducted. Simulated sessions verify software only. Training feedback is explicitly
unblinded and ineligible for blind scoring; N retains its historical meaning Near
Site. ERV, ARV and naturalistic/dream protocols remain outside the supported core.

Run `python -m unittest tests.test_remote_viewing`,
`python -m scripts.verify_remote_viewing` and
`python -m scripts.smoke_remote_viewing_core` for new checks. The independent oracle
was committed before production and covers120rankings x5targets x120display orders.

## Prophetic Dreams: prospective evidence ledger

`dunne-revised-prospective-dream-ledger-v1` implements manual prospective records,
original locks, append-only amendments and complete human comparison accounting.
Its historical witness is the later Faber text transcribed in FadedPage20181016,
with publication history through1939 and1934third-edition additions. It does not
certify the inaccessible1927scan wording or reproduce Dunne's entire experiment.
Wargo's fixed picture and later associations remain separate; modern full-book
exercise access remains a source gap. No prophecy, universal chance baseline,
semantic confidence model or automatic interpretation is supplied.

Use `python -m future prophetic-dreams REQUEST.json --asset-root D:/Future`
and optionally `--format markdown`. Every request has `schema_version:1`, the
exact `profile`, and a `task`. The immutable schema/policy is in
`knowledge/prophetic_dreams_profile_v1.json`; runnable requests are in
`data/prophetic-dreams-*-input.json`.

1. `create` takes a complete `plan`. Fix pseudonymous participants, recording
   slots, finite event-ID manifest and collection rule, universe hash, closed
   comparison window, human feature definitions, judges and stopping/exclusion
   policies before recording. The output is a **private** `ledger`.
2. `apply` takes `ledger`, `action`, `actor`, timezone-aware `at` and `payload`.
   Actions include `record`, `slot_status`, `lock_entry`, `amend` and `event`.
   A dream occurrence interval can be unknown; first-record and lock times are
   distinct. Preserve the original UTF8 narrative and user-selected details.
   The `original_lock(entry, at)` Python API supplies the expected lock digest.
3. `amend` requires the latest parent version hash, new raw text, reason and
   outcome-knowledge declaration. It appends a version and retains the original.
   Comparisons always use the original locked entry; a later clarification cannot
   improve the original endpoint. `slot_status` retains nonrecall, missing,
   withdrawn, invalid and excluded entries. Unsubmitted slots are accounted for
   after their declared deadline; no occurrence timestamp is invented.
4. Collect every prespecified event slot with occurrence/publication/discovery
   times, deduplication group, common-event flag, coverage declaration and local
   permission-cleared evidence bytes/hash. `seal` requires all events, all
   submitted original locks and the completed recording schedule.
5. Every locked original dream is paired with every manifest event. Excluded
   pairs remain visible with reasons. Exact closed-window boundaries are included;
   partially overlapping/unknown intervals remain uncertain. Equal lock/endpoint
   times are not prospective. An existing event discovered after recording remains
   distinct from a future event. Publication/discovery analyses are labeled as
   information endpoints; they do not change actual-event chronology.
6. `expose` records each judge's knowledge declaration. `judge_packet` takes the
   private ledger and `judge_id`; consent is required. `--export-dir NEW_DIRECTORY`
   writes only allowlisted `packet.json`. The content-rating task retains exact
   original text and features while masking private chronology, source paths,
   answer indicators and prior decisions. Attachments are verified privately and
   are outside this first text-only judge export. Semantic clues and familiarity
   with public events cannot be certified absent.
7. Each judge `rate`s the complete pair-ID map using `match`, `nonmatch`,
   `insufficient_information`, `unscorable` or `protocol_invalid`. All planned
   judges must submit before `lock_judges` with `judge_lock(ledger)`. Explicit
   coordinator `reveal` follows the lock. `commentary` then records feedback or
   external free associations separately; `finish` records study completion.

`report` returns a **private** full report, including the exact ledger for replay,
all original versions, schedule statuses, events, pairs, exclusions, judge ratings
and disagreements. A declared match is a human rating, not a probability or proof
of precognition. Duplicate-group representatives follow manifest order; duplicates
stay visible but are excluded from eligible counts. Collection omissions and
common-event flags remain visible. No best pair/judge selection or p-value is used.
`reference` takes exact IDs `martinique`, `lecture-nonmatch`, `wargo-envelope` and
returns source-attributed historical notes, including the lecture nonmatch.

Rejected actions return exit2 with an updated private ledger containing the failed
attempt. Persist that output even on exit2. Corrupt/incomplete root inputs return a
generic error and cannot amend an untrusted ledger. `terminate` records an aborted
or excluded terminal study. Never overwrite the previous input with an output shell
redirection before the command has read it.

All clocks, dream occurrence, knowledge, identities, rights and witness statements
are declarations. Hash chains detect inconsistency relative to independently held
anchors; a file owner can rewrite an entire local history. No independently trusted
timestamp, human participation or psychological blinding is certified. Only
synthetic project-authored examples are distributed; do not publish private dream
narratives or protected event/book material without appropriate permission.

Run `python -m unittest tests.test_prophetic_dreams`,
`python -m scripts.verify_prophetic_dreams` and
`python -m scripts.smoke_prophetic_dreams_core`. The pre-engine specification
freezes300integer interval/chronology cases, timezone cases, original/version lock
known answers, eight manually enumerated pairs and18procedural fixture families.

## Intuitive Prediction: explicit heuristics and forecast evaluation

`python -m future intuitive-prediction data/intuitive-prediction-exact-brier-input.json --format markdown`

The named `goldstein-gigerenzer2002-recognition-subset-v1` profile implements the
isolated recognition rule with declared ecological direction. The separate
`gigerenzer-goldstein1996-ttb-deterministic-v1` profile preserves recognition
precedence and searches supplied cues until positive opposes negative or unknown.
Negative versus unknown does not discriminate. Its historical random-choice
branches return explicit editorial abstentions. Cue order, validity, provenance
and tie conventions are declared before evaluation; the engine does not learn
them from outcomes. Heuristic choices never generate probabilities.

Requests use `schema_version: 1` and a `task`. See the committed examples for
`recognition`, `take-the-best`, `decision-reference`, `create`, `decision-record`,
`forecast-record`, `forecast-amend`, `resolve`, `forecast-score`, `calibration`,
`baseline-compare`, `report` and `reference`. Each result contains exact protocol,
source, request, result and optional ledger hashes. `--asset-root` bounds local
evidence paths. Reports contain private inputs; store and share them accordingly.

Create a plan with a finite event/forecast-slot manifest, then retain the returned
`ledger` for the next request. Forecast probabilities are **plain decimal strings**
such as `"0.8"`, preserving their exact values. Amendments require the previous
version hash and retain originals. The cutoff is inclusive; eligible forecasts
must strictly precede actual occurrence and declare outcome knowledge false.
Latest eligible versions are selected once per forecaster/event at the plan's
fixed horizon. Late or contaminated revisions remain visible and cannot displace
an eligible original. Missing occurrence/evidence, unresolved, disputed and void
outcomes remain unscored. Local evidence bytes and permission declarations are
checked on replay. Do not overwrite the input before a command finishes reading it.

Binary Brier loss is `mean((p-y)^2)`, lower is better, in `[0,1]`. Reduced rational
values are authoritative; decimal displays use twelve places and half-even
rounding. The complementary two-category positive sum is twice this loss.
`N=0` gives null. Ten fixed calibration bins retain empty bins and sample counts;
calibration does not establish discrimination or expertise. An optional baseline
requires separate earlier training outcomes/evidence, compatible scope and no
evaluation IDs; comparisons use identical resolved pairs. Log loss, Brier skill
ratios, decomposition and inferential statistics are deferred.

The linked synthetic CLI demonstration is in `data/intuitive-prediction-demo.json`.
Run `python -m unittest tests.test_intuitive_prediction`,
`python -m scripts.verify_intuitive_prediction` and
`python -m scripts.smoke_intuitive_prediction_core` for verification and exact
accepted/rejected JSON/Markdown replay. The independent verifier checks all nine
cue pairs, 729 three-cue traces and 42 actual-ledger rational scoring cases.

RPD notes and learning-context reviews are human declarations, not optimal action
selection or expert certification. Counts of forecasts, unique events and
dependency groups are separate. Local clocks, knowledge, identities, training
validity and rights remain declarations; owners can rewrite complete local hash
chains. No real human forecasting benchmark or paranormal capability is validated.
Full ranked-book/1993 RPD chapters and historical dataset rights remain P1 gaps;
only original synthetic evidence and concise source facts are distributed.


## Déjà Rêvé (#46)

The named `curot2018-phenomenology-and-dream-record-provenance-v1` profile
supports human-guided experience annotations and exact prior-dream record
comparison. Curot's episodic-like, familiarity-like, dreamy-state and
unclassifiable documentary categories remain distinct from the four original
inventory variations. Source examples are Table1 cases4a,6a,5a and Table2
Penfield H.N.; the last remains unclassifiable. The inspected institutional
proof uses pages1–11; final journal pages875–885 are bibliographic metadata,
without a verified final-layout comparison. Dunne's later recording guidance
supplies no neurological or prophetic classification rules here.

```powershell
python -m future deja-reve data/deja-reve-reference-input.json
python -m future deja-reve data/deja-reve-specific-prior-dream-input.json --format markdown
python -m future deja-reve data/deja-reve-post-event-amendment-input.json
python -m future deja-reve data/deja-reve-multiple-candidates-input.json --format markdown
python -m future deja-reve data/deja-reve-post-hoc-search-input.json
python -m future deja-reve data/deja-reve-version-hash-input.json
```

The final command intentionally rejects a conflicting version hash with exit2.
Requests have `schema_version:1` and an explicit `task`: `reference`, `annotate`,
`record`, `amend`, `freeze-candidates`, `link-dream`, `compare` or `report`.
The saved synthetic requests document each strict schema. Retain returned records
and analysis objects for subsequent requests. Original and narrative hashes use
SHA256; canonical objects use UTF8 JSON with sorted keys, no optional whitespace,
`ensure_ascii=False`, and no nonfinite values. Raw narratives preserve Unicode,
newlines and whitespace without normalization. Originals include timing, consent,
source and profile commitments. Amendments preserve parents, versions, reasons,
new narratives, timing and declared knowledge; they cannot edit the original.

Annotation reads explicit declarations only. Unknown details remain
unclassifiable, conflicts/explicit uncertainty require review, and familiarity
without dream association stays outside the source scope. Subjective confidence
and the reviewer's source-category proposal are retained separately. The
software does not infer experience type from narrative keywords or replicate
the paper's expert clinical consensus.

Freeze the finite candidate manifest before comparisons. Exact dream IDs and
original hashes are required; every match, nonmatch, insufficient, unscorable,
unreviewed, excluded or missing-original candidate remains in the ledger.
Later searches have separate post-hoc manifests and denominators. Each manual
comparison names the actual narrative version; later precise details retain
their later timing. Original locks are compared separately to current experience,
first written report and optional external event. Equal boundaries, overlaps,
unknown times and conflicting assertions remain explicit. An earlier record
establishes documentary order under declared clocks, not the truth of a memory.

All participant outputs are **private local records**, including CLI stdout and
Markdown/JSON reports. Consent and declared rights are required. Public narrative
export, automatic import of #44 ledgers, restricted attachment references and
journal-wide semantic retrieval are outside v1. Optional event evidence
references/hashes are declarations; this engine does not authenticate external
event bytes. Local owners can rewrite complete hash chains. The CC BY-NC-ND4.0
article is represented by concise original factual notes, without interviews,
figures, article PDF or clinical dataset redistribution. All demonstrations use
original synthetic inputs. No diagnosis, localization, stimulation advice,
memory-authenticity determination, resemblance probability or prediction is
produced.

```powershell
python -m unittest tests.test_deja_reve
python -m scripts.verify_deja_reve
python -m scripts.smoke_deja_reve_core
python -m scripts.accept_deja_reve_core
```

Independent source/category fixtures were committed before production. They
include all16audit families,648conservative declaration combinations and11fixed
chronology constants. These checks establish bounded computational behavior;
they are not empirical or clinical validation. Release evidence and P1/P2 limits
are in `knowledge/deja_reve_core_v1.json`.


## AI Predictive Modeling (#49)

The offline `fpp3-noaa-monthly-rolling-origin-baselines-v1` workbench supports
seven fixed CPU configurations: seasonal naive m12, naive, drift, mean, and SES
with alpha0.2/0.5/0.8, initialized at the first training observation. SES consumes
subsequent observations in order;it does not optimize alpha or fit an ETS
predictive distribution. ARIMA,trees,neural models,Chronos inference and automatic
prediction intervals remain outside this release.

```powershell
python -m future ai-predictive-modeling data/ai-predictive-modeling-drift-input.json
python -m future ai-predictive-modeling data/ai-predictive-modeling-rolling-input.json --format markdown
python -m future ai-predictive-modeling data/ai-predictive-modeling-noaa-benchmark-input.json --format markdown
python -m future ai-predictive-modeling data/ai-predictive-modeling-source-distribution-score-input.json
python -m future ai-predictive-modeling data/ai-predictive-modeling-alpha-input.json
```

The last command is an intentional rejected fixed-alpha request (exit2).
JSON requests specify `schema_version:1`,the exact `profile`/`profile_version`,
and `task`: `reference`, `forecast`, `evaluate`, `benchmark`, `metrics`,
`score-distribution`, or `report`. `report` takes a saved original request and
recomputes the same deterministic result. The saved examples define the strict
schemas. Generic datasets accept multiple series with unique IDs,complete
ordered monthly grids,units,rights/provenance and explicit availability/vintage
information or unknown status. Values are finite plain decimal strings;null
marks missing data. A supplied canonical dataset hash must match all metadata
and observations. Manual seasonal-naive periods use explicit IDs such as
`seasonal_naive_m4`;only m12 enters the frozen NOAA benchmark.

Every fit receives only its origin's training prefix. Missing training values
fail that candidate/origin;missing outcomes remain unscored. Every planned cell
and failure is retained. Validation selects lowest macro per-series MAE,with
exact ties resolved by frozen order and complete forecast coverage required.
The selected configuration stays fixed for test;all-candidate test scores are
reported as diagnostics. Macro weights series equally;micro weights cells
 equally,so they coincide for the single NOAA series. Forecast windows overlap;
300cells per model/partition represent36distinct outcome months.

Decimal input is converted directly to exact Fractions. Output preserves exact
rational values plus12-place HALF_EVEN decimal displays. RMSE retains its exact
rational radicand and uses an80-digit Decimal square root. Bias is actual minus
forecast. MASE averages absolute errors divided by each origin's training-only
seasonal scale,with separate defined-scale counts. Paired seasonal-naive MAE
differences/ratios use common eligible cells. Empty or zero denominators produce
null with a reason,never NaN/Infinity or an invented perfect score. Optional
absolute-denominator sMAPE is a manual diagnostic limited to20scored pairs;
benchmark aggregates omit it to avoid impractical exact denominator growth.
This convention differs from FPP3's signed denominator. Manual quantile scoring
reports ordinary pinball and FPP3 twice-pinball separately;manual central
interval scores use inclusive endpoint coverage. These functions do not generate
model prediction intervals. WIS/CRPS and empirical calibration remain deferred.

The pinned NOAA subset contains288months from2000-01through2023-12. The protocol
uses25monthly validation origins2017-12through2019-12 and25test origins2020-12
through2022-12,each forecasting h1–12. All4,200candidate cells succeeded in the
recorded benchmark. Drift won validation (MAE2.59897ppm),then had test MAE2.53725
versus seasonal-naive2.17940ppm,about16.42%higher error. The software preserves
that worse held-out result and the horizon-wise comparisons. Results describe
**retrospective evaluation on a fixed revised snapshot**,not certified original
as-of historical forecasts. NOAA QC/calibration/midmonth adjustments,station
substitution and missing publication vintages remain explicit limitations.

Measured resource evidence is separate from pure calculation and frozen by hash
in the benchmark request. On the recorded machine,warm core median was1.1594s,
fresh CLI wall time2.6805s andpeak working set132526080bytes. Definitions and
measurement limitations accompany the record;these are not universal latency
claims. A normal replay does not remeasure or invent timings. Run the explicit
measurement script only when intentionally creating new resource evidence.

```powershell
python -m unittest tests.test_ai_predictive_modeling
python -m scripts.verify_ai_predictive_modeling
python -m scripts.smoke_ai_predictive_modeling_core
python -m scripts.accept_ai_predictive_modeling_core
```

The independent oracle was committed before production and checks all4,200cell
predictions,exact aggregate/horizon scores and672sentinel predictions. No model
weights,forecasting framework,cloud service or additional runtime dependency is
required. Full reports are in `data/ai-predictive-modeling-noaa-benchmark.*`;
release scope and P1/P2 are in `knowledge/ai_predictive_modeling_core_v1.json`.


### Quantum Probability Forecasting (#50)

Offline standalone CPU reference profile `montanaro-ibm-small-circuit-cpu-probability-v1`: 1–4 qubits, at most64 primitive `id/x/h/ry/cx` gates, up to100000 terminal shots. Signed complex amplitudes retain interference and Bell correlations. q0 is the least significant bit;measurement mapping is identity only. Float64 results use1e-12 independent comparison tolerance. No Qiskit installation required.

Run `python -m future quantum-probability-forecasting data/quantum-probability-forecasting-cli/compare-common-input.json --format json` (or `markdown`). Requests explicitly pin profile/catalog hashes, circuit, event, shots, xorshift32-v1 seeds and provenance. Tasks: simulate, sample, compare, reference, report. Unknown fields,unsupported backends,noise,QAE and variational requests reject with exit2.

Reports distinguish raw Born probabilities, verified norm and explicit CDF normalization, finite-shot frequencies and analytical iid Bernoulli moments. No tiny probabilities are clipped. Event-first CDF uses strict u<boundary;common streams match direct Bernoulli event counts by construction. Independent streams use distinct declared seeds. Known p is already directly available;sampling does not discover it. Population standard errors are not certified confidence intervals.

Independent pre-engine dense matrices cover79circuits and three100word PRNG sequences;all20fixture families are exercised by `python -m scripts.verify_quantum_probability_forecasting`. Exact accepted/rejected CLI JSON/Markdown corpus is in `data/quantum-probability-forecasting-cli/`;manifest records raw input hashes. Replay uses recorded runtime and normalized-LF code commitment;cross-platform libm equality is tolerance scoped.

Actual timings and memory are separate in `data/quantum-probability-forecasting-resource-measurements.json`. For100000shots,classical Bernoulli sampling was faster in all three local cases;known-p lookup was fastest. Peak memory covers the whole measurement helper,not an isolated kernel or CLI child;tracemalloc phase peaks cover Python allocations only. No practical quantum advantage,hardware execution,QAE,financial forecast skill,VaR/CVaR or operational Aer compatibility is certified. Source facts and original code only;article/source licenses and edition distinctions are frozen separately. Full acceptance and capability matrix are in the #50core record when closure passes.


### Superforecasting (#51)

Profile `tetlock-mellers-binary-forecast-updates-v1` is an offline binary question, reference-class and forecast ledger. The standard command is `python -m future superforecasting INPUT.json --format json` (or `markdown`). The JSON task selects `question`, `reference-class`, `create`, `forecast`, `update`, `resolve`, `attempt`, `score`, `report` or factual `reference`. Successful ledger operations return `result.ledger`, which becomes the next request's ledger. Input objects are copied; no file is silently replaced.

Start with `data/superforecasting-cli/create-input.json`; the saved original/manual/Bayes/late/resolve inputs show each actual transition. `data/superforecasting-cli/lifecycle-report-input.json` contains the complete original synthetic example. This validates software mechanics, not human forecasting expertise or a historical tournament ranking.

Plans freeze precise user-confirmed question wording, half-open observation windows, fixed cutoffs, source snapshots, historical member records, baseline and group partitions. The software checks schema and chronology; semantic clarity, rights, timestamps and representativeness remain declarations. Local hashes cannot stop a file owner rewriting all history; independent prospective anchoring remains P1.

Probabilities and likelihoods use bounded exact rational strings such as `1/5` or `0.2`. Reference rates are unweighted k/n over included resolved distinct historical members; every excluded, ambiguous or unresolved member remains visible. Empty rates are not estimable; observed zero/full rates do not imply population certainty. Documentary outside-view or decomposition notes never generate probabilities.

Bayes updates compute Lp/(1-p+Lp) exactly. One new evidence item is required per update. Repeated IDs, underlying facts or snapshots reject. Further updates require an explicit complete conditional history or independence declarations under both H and its complement with distinct evidence groups. Likelihoods and dependence declarations are assumptions unless separately established; a measured-status label is not validation. Manual revisions remain distinct. The `attempt` task preserves rejected candidates and reasons without changing accepted state or version ancestry.

Selection takes the latest accepted eligible forecast at or before cutoff, strictly before declared outcome information/positive occurrence. Late and post-outcome revisions remain visible. Positive occurrences lie within [window_start,window_end); nonoccurrence has no occurrence timestamp and is established only after the window closes. Resolution corrections require a visible dispute/void step.

Primary scoring gives equal forecast-slot weight on selected resolved TEST questions. Train summaries, event-average and participant-average losses are separate; team aggregation is unimplemented. Binary Brier is (p-y)^2 on0–1; two-category loss is twice this value on0–2. Neither reproduces the paper's daily/question-standardized tournament protocol. Natural-log losses use Decimal80 and12-place HALF_EVEN display; contradicted certain forecasts return a structured positive-infinity status, never JSON Infinity or clipping. Rational displays use exact integer HALF_EVEN projection, including very large relative ratios.

Ten frozen calibration bins are descriptive. Exact identical-probability groups support verified Brier reliability/resolution/uncertainty decomposition; coarse bins do not replace those groups. Baseline comparisons use precisely matched selected outcomes, show exclusions, and omit relative skill when baseline loss is zero. Forecast slots, events and dependency groups have separate denominators.

Run `python -m scripts.verify_superforecasting` for all23 independent families. The accepted/rejected JSON/Markdown corpus includes source hashes, raw Unicode/whitespace commitments and corpus-local byte preservation. See `data/superforecasting-synthetic-summary.md` for worked values. Full-book later chapters, GJP file rights/codebooks/complete revisions, empirical held-out skill, stronger dependence inference and prospective timestamp anchoring remain P1. Multinomial questions, team aggregation and daily tournament reproduction remain P2. No source book/article bodies or participant corpus are redistributed.

Question lead times use exact rational seconds, including fractional-second boundaries. Reference-period extrema compare parsed UTC times;the frozen timestamp-precision fixture covers lexical-order and truncation controls.

### Psychohistory (#52)

Profile `psychohistory-synthetic-threshold-dynamics-v1` provides bounded synthetic population threshold dynamics and static scenario comparisons. It uses explicit simple undirected graphs, exact rational node thresholds and irreversible synchronous rounds. Every node reads the previous snapshot. Unseeded isolates remain inactive, including at zero threshold; zero-threshold nodes with neighbors can activate without an active neighbor. This is an editorial finite-graph variant of Watts's threshold rule; his source schedule is random asynchronous. Asimov is fictional inspiration; Pentland and Page supply measurement/model-comparison context, without invented book formulas.

Run `python -m future psychohistory data/psychohistory-cli/path-input.json --format markdown`. Worked inputs/reports also include `topology`, `exhaustive`, `threshold-comparison`, `identical`, `overrides`, `unknown-field` and `count-only-cap` in that directory. The exhaustive two-node example supplies all four equally weighted initial states; it is an exact design, not Monte Carlo. Every scenario includes the same-initial-state no-influence persistence baseline.

Fixed, Bernoulli and explicit-per-run initialization are supported. The frozen xorshift32 stream consumes one word for every run/node even under overrides; scenarios share those words by semantic identity. Population/sample variances explicitly divide by R/R−1; sample variance for R=1 is not estimable. Ideal iid initial-seed moments are separate from finite deterministic PRNG summaries and correlated final cascade outcomes. Paired differences are hypothetical sensitivity; shared randomness does not guarantee variance reduction. Relabeling fixed initial-state systems preserves physical dynamics; changing sorted semantic IDs in a stochastic request changes the draw assignment.

Limits are N≤128, E≤2048, R≤256 and ≤8 scenarios, subject to stricter combined preflight work/count/state reservations. Individual maxima cannot be combined freely. Run `python -m scripts.verify_psychohistory` for all23 independently frozen families and boundary addenda. See `knowledge/psychohistory_profile_v1.json` for exact schema/budget equations, `data/psychohistory-resource-measurements.json` for local measured scope, and `data/psychohistory-synthetic-summary.md` for original analytical examples.

Only original synthetic data and declared permitted snapshots are accepted. No books, contact traces or restricted datasets are redistributed. Empirical calibration, held-out prediction, causal inference, adaptive agents, demographics and real civilization forecasts are unsupported; rounds are dimensionless steps. Detailed book methods, dataset-specific rights/consent/calibration and prospective external validation remain P1; asynchronous source replication, weighted/dynamic graphs and learning remain P2.

### Digital Twin Simulation (#53)

Profile `digital-twin-offline-scalar-state-replay-v1` supports one asset, a scalar linear state model and exact rational prediction/correction, with declared units and parameter versions. It implements offline state-estimation replay and hypothetical future control scenarios. NASEM2024 supplies definition/VVUQ boundaries, Grieves2014 is a whitepaper about physical/virtual product connections, and the separately identified Welch–Bishop2002 numerical supplement supplies linear filter equations. No copyrighted source bodies or code are redistributed.

Run `python -m future digital-twin data/digital-twin-cli/sequential-input.json --format markdown`. The corpus also includes `missing`, `scaled`, `controls`, `delayed`, `later-evaluation`, `cell-cap` and `bit-growth` accepted/rejected report pairs. Run `python -m scripts.verify_digital_twin` for all27 independent families, the batch-precision crosscheck, chronology, covariance and scenario checks.

Whole-second UTC grid times are explicit. Each prior forecast originates at the preceding grid time and is computed before its current measurement is read. On-time measurements correct the state; missing or delayed measurements skip correction, with no backfill. Delayed targets can be evaluated once available at the declared evaluation cutoff. Last-observation persistence uses the latest earlier sample available at the forecast origin, on the observation scale. Exact pre-update squared errors are reported on all eligible targets and a common three-way target set; empty denominators are not estimable. Posterior fit is never scored as prediction, and measured sensor values are not latent-state truth.

Future controls fork from the same accepted historical posterior without future observations. The model does not learn parameters, smooth, impute, delete outliers or send actuator commands. Exact arithmetic checks conservative8192-bit reservations before operations; requests also have combined step/output caps. See `knowledge/digital_twin_profile_v1.json` for the complete contract and `data/digital-twin-resource-measurements.json` for local measurements with their scope.

Synthetic numerical replay is supported. Archival replay requires independently reviewed source, units, timestamps and rights, recorded as declarations that the engine cannot certify. Empirical accuracy and uncertainty calibration require real data and held-out validation. There is no live physical synchronization or decision feedback, so this is not certified as a complete real-time digital twin. P1 retains calibration, validation, source access, timestamp provenance and counterpart documentation; P2 retains nonlinear/multivariate filters, learning, asynchronous correction, urban/behavioral twins and live feedback.
