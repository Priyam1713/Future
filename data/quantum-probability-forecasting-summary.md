# Technique50 numerical review

Profile: `montanaro-ibm-small-circuit-cpu-probability-v1` (SHA256 `abe755a144bf38b228ebbd0e6eb313b93405ff2d90fda75e1bcb2295196852dd`).

Standalone classical CPU execution;no quantum hardware or amplitude estimation. Gates:id,x,h,ry,cx;1–4qubits,64gates,100000shots. q0LSB;identity terminal mapping. All matrices in this gate set are real;the engine retains signed complex coefficients.

## Independent controls

79pre-engine dense-matrix/symbolic circuits and300frozen PRNG words pass. Maximum amplitude difference: 1.7763568394002505e-15. HH returns |0>;Bell probabilities [1/2,0,0,1/2];reversing CX in that example leaves q1zero. Xq1 produces10/index2. Negative RY preserves its negative coefficient.

For p=1/4,N=100:E[K]=25,VarK=75/4,Varfrequency=3/1600,SE=sqrt(3)/40. Seed1 yielded33successes;the ideal p is0.24999999999999994 in float64. Shared-stream comparator also gives33by construction. Controlled uniforms[1/4,3/4,1/4] yield absolute error0 atN2 and1/6 atN3. No confidence interval is certified.

## Actual local resource evidence

Five repetitions per phase;table shows median seconds. CLI is a separately measured subprocess wall time.

| Circuit | Qubits / gates | Statevector s | CPU shots s | Bernoulli s | CLI s | Counts circuit / classical |
|---|---|---|---|---|---|---|
| bernoulli | 1 / 1 | 0.00000470 | 0.03048550 | 0.01959600 | 0.80049560 | 24978 / 24823 |
| bell | 2 / 2 | 0.00000660 | 0.03100710 | 0.01984090 | 0.80725440 | 50053 / 49767 |
| bounded64 | 4 / 64 | 0.00028860 | 0.04391590 | 0.02035200 | 1.11917580 | 51413 / 51109 |

Each case used100000shots,independent circuit seed1 and comparator seed2. Classical sampling was faster in every measured case. Direct known-p lookup was faster than either sampler. This is an equal-p/equal-N classical implementation comparison;it provides no coherent-query or quantum advantage evidence.

Native measurement-process peak working set: 26726400bytes (25.488MiB). This includes imports/tracing and is not isolated kernel/CLI-child memory. Per-phase tracemalloc peaks are Python allocations only;see resource JSON for all repetitions/environment.

## Replay examples

`python -m future quantum-probability-forecasting data/quantum-probability-forecasting-cli/compare-common-input.json --format markdown`

`python -m future quantum-probability-forecasting data/quantum-probability-forecasting-cli/reject-qae-input.json --format json` (exit2).

Other saved examples:bell,bell-shots,hh,h1,rynegative,endian,compare-independent,unicode-whitespace,reference-montanaro and rejected backend-aer,noise,rights. Raw input and both exact output hashes are in the CLI replay manifest.

## Boundaries

Theoretical quantum results require coherent state preparation/inverse,projector/reflections and cost accounting;they are not ordinary measurement shots. Aer/SDK/Algorithms are absent and uninstalled. Montanaro2015journal and subsequent revisions are distinct;Woerner/Egger is a2019journal article despite historical inventory Book label. Facts-only attribution is retained;no PDF/source/figures redistributed.

The finite-state xorshift32 stream is deterministic and noncryptographic,with32bit uniform resolution and dependent sequential draws. Analytical iid moments describe the ideal repeated-preparation model,not a theorem about the finite PRNG stream. Tiny Born probabilities remain untruncated but finite-grid sampling cannot faithfully resolve arbitrarily rare events. Rare-event refinements and confidence intervals remainP1. Float64 libm and serialization are runtime-scoped;independent cross-platform comparisons use1e-12 absolute tolerance.

P1:Aer CPU parity with an explicitly pinned environment;coherent oracle and phase/query conventions before QAE;IQAE/MLAE inference validation;rare-event sampling and risk toy reproduction. P2:variational/quantum-inspired extensions,noise,larger/GPU/hardware experiments under separate scope and evidence. No unknown-future market skill is established.
