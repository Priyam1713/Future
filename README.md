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

See `PROGRESS.md` for implemented scope and the next action. No complete prediction engine is available yet.

## Run the first knowledge/calculation slice

Runtime uses Python's standard library only. From the repository root:

```powershell
python -m unittest discover -s tests -v
python -m future --database knowledge.sqlite3 search "Gregorian UT1"
python -m future calendar 1877 8 11 7.5
```

The pipeline loads source metadata, ingests original UTF-8 research notes under an explicit rights policy, imports manually extracted typed rule records, checks published numerical fixtures, and stores immutable versions in SQLite. Full-text retrieval returns source locators and document hashes. Calendar results reference the applied rule and retrieved source. The three published USNO examples are independent reference values; date-boundary tests also compare Python calendar arithmetic.

Current extraction is manual and JSON-based. PDF/OCR extraction, LLM-proposed extraction, semantic embeddings, generated interpretations, API and UI are not implemented. This is a calendar component, not a birth-chart engine. Caller inputs must explicitly be UT1 in the supported Gregorian interval. Never relabel UTC or local birth time as UT1.

Sources retain author, edition, access and ingestion policy. Rules retain technique, variation, tradition, version, exact locator, operation, parameters, evidence type, verification state and fixture references. Different authorities use distinct IDs; changed rules use new versions. Only verified rules in the exact requested scope are selected. Verification here means procedural/example agreement, not predictive accuracy. The registry is a local trusted research store; ingesting arbitrary external rule JSON as verified is unsupported.
