# Future

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

Sources retain author, edition, access and ingestion policy. Rules retain technique, variation, tradition, version, exact locator, operation, parameters, evidence type, verification state and fixture references. Different authorities use distinct IDs; changed rules use new versions. Only verified rules in the exact requested scope are selected. Verification here means procedural/example agreement, not predictive accuracy. The registry is a local trusted research store; ingesting arbitrary external rule JSON as verified is unsupported.
