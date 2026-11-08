# Future Lab v1 — acceptance report

Future Lab v1 is ready within its bounded offline scope. The existing 54 engines are unchanged. There is no new forecasting technique, frontend, cloud service, paid API or general multi-agent framework.

Acceptance: **2,522 tests**, **3,515 CLI cases**, **52 verifiers**. This retains all 2,402 tests, 3,453 CLI cases and 51 verifiers from Core v1, adding 120 tests, 62 CLI cases and one 26-family verifier. All **5,441 protected files** are unchanged; only README and PROGRESS are permitted existing edits.

The annotated `core-v1.0.0` tag remains at `685a329`. Registry/profile/source/acceptance hashes and original resource rights are retained. Registry revision 2 corrects overly broad type labels; revision 1 and all pre-production native/numeric fixture anchors remain preserved. No native capability or metric was expanded by that correction.

**Use**

```powershell
python -m future.lab list
python -m future.lab inspect 49
python -m future.lab evaluate data/future-lab-demo/final-ledger.json --format markdown
python -m future.lab noaa-reference
```

Python entry points are in `future.lab`: `invoke`, `create`, `forecast`, `resolve`, `persist`, `evaluate`, and `compare`, with discovery and native validation helpers. README contains a complete persistence example. All 54 native request examples are in `data/future-lab-invocation-examples.json`. CLI responses wrap results; experiment commands consume raw snapshots.

**Capabilities and limits**

- All 54 cores have source/profile/version and actual CLI/Python contract metadata. Forty-seven cores dispatch directly to request APIs; seven parameterized cores expose 15 operations through the unchanged CLI dispatcher in-process.
- Native structured outputs, original error class/message or CLI stdout/stderr/exit status, and native unsupported states remain separate from Lab provenance. Validation can cost the same as execution.
- Only #49/#51/#57 are admitted to Lab v1 experiment scoring. Historical, symbolic, appearance-based, causal, market and speculative outputs are not coerced into a common prediction score. #53/#55 empirical admission remains deferred.
- Plans bind dataset/source/rights/vintage information, target identities, cutoffs, splits, model selection and native request hashes. Forecasts precede separately recorded outcome evidence. Explicit synthetic native records cannot be relabeled as retrospective/prospective evidence.
- The ledger is a replayed SHA chain. Persistence exclusively binds each experiment ID/version to one plan and saves hash-named snapshots without overwriting different bytes. Local storage and declared clocks are not independently authenticated commitments.
- Model/baseline comparisons use identical eligible targets. Missing, excluded and unrecorded outcomes remain visible. Empty scores are not estimable. Calibration, coverage and dependence counts are descriptive; no confidence interval or effective independent sample size is invented.
- MAE/RMSE and binary Brier use exact rational components. RMSE retains an exact square-root expression plus a bounded Decimal display. Lab bias uses prediction minus actual; native #49 sign conventions are preserved in the native result.

**Complete first experiment**

The demonstration is visibly **synthetic**. It registers source information, freezes a three-question #51 protocol, executes the existing engine, commits its native output, records separate later outcome evidence, and emits JSON/Markdown research reports. Two targets are matched; one is missing. Model Brier is **17/50**, fixed-half baseline Brier **1/4**, and paired difference **9/100**: this toy model underperforms. No empirical skill is claimed. The full ledger and independent known answers are in `data/future-lab-experiment-demo.json`.

**Preserved retrospective evidence**

Validation selecteddrift. Test MAE2.537249963267ppm vs seasonal-naive2.1794ppm;ratio1.164196551008. Selected model underperformed on test and is not replaced by the diagnostic test winner.

The native NOAA benchmark is reproduced, not retuned. Source-vintage certification remains false; the exposed test interval is not new independent evidence. New superiority claims require a separately frozen untouched period and suitable rights, availability, comparison and dependence protocols.

**Measured local resources**

| Operation | In-process median seconds | Python traced peak bytes |
|---|---|---|
| discovery54 | 0.004830 | 2767859 |
| native51 | 0.019181 | 2768268 |
| complete_demo_report | 0.031488 | 2790995 |
| noaa_reference | 1.521179 | 60519956 |

Full CLI observations: demo 0.767735 s, noaa_reference 4.316062 s. Whole-helper native peak: 115658752 bytes, including imports, all workloads and tracing. This is not a per-operation or CLI-child peak, and timings are observations rather than universal guarantees.

**Next empirical studies, ranked**

1. #49: seal a separate untouched period, source vintage and selection protocol before opening new target values; preserve the exposed unfavorable result.
2. #51: preregister future binary questions, forecast commitments, independent resolution evidence and a prior-only matched baseline.
3. #57: compare individuals and fixed pools on those same questions, preserving consent, missing participation and dependency groups.
4. #53: first approve a rights-cleared scalar sensor/availability protocol; compare against persistence and open-loop predictions.
5. #55: first approve a lawful empirical trial-window profile with consent, subject/run/trial separation and preprocessing/interval leakage controls. Do not relabel real EEG as synthetic.

These are recommendations only. Details and prerequisites are in `data/future-lab-next-experiments.json`. No new empirical data was acquired.

**Traceability**

Source/registry/profile freeze `705ce84`; original fixtures `065fb02`; initial engine `f8241eb`; corrected metadata/CLI `95b38f7`; full acceptance `1fc048cd792f2236742bd07fd09745368e27cb97`. Full evidence, active profile/registry hashes and tag object ID are in `knowledge/future_lab_v1.json`. Resolve the completion commit with its recorded lookup command; final clean synchronized Git state is observed after publication.
