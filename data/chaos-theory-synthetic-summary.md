# Technique59 — finite Lorenz63 reference

The supported core integrates explicit synthetic initial states with fixed-step classical RK4. Default equations use sigma=10, rho=28, beta=8/3 and dimensionless model time. Original Lorenz RK2 runs are not reproduced.

At initial (1,1,1), the derivative is (0,26,-5/3). With h=1/100, the coarse next state is approximately (1.0125671910736112,1.2599177989452743,0.9848909717916053). Exact rational four-stage fixtures were committed before the engine.

A separate Taylor coefficient recurrence supplies a local t=1/100 reference. Orders80 and100 agree within1e-60; this stability check is not a rigorous remainder bound. RK4 errors at h=1/200 and1/400 are about1.52718e-7 and9.14818e-9, ratio16.6938. The independent lower-order Euler negative control has error0.0126622.

Reports distinguish initial-condition separation from h/h2 trajectory differences. Output stride never skips integration or maxima over the full aligned grid. Identical pairs, exact equilibria, sign symmetry, zero horizon and guarded unstable stages are verified. No certified global Lyapunov exponent, forecast horizon, weather skill, delay embedding or reservoir training is supported.

Measured complete reports include three untraced in-process repetitions, a separate traced report, and a full CLI call. Native peak covers the complete helper including all workloads and tracing, not each workload or the CLI child. See the versioned measurements for actual timings and scope.

Examples: `python -m future chaos-theory data/chaos-theory-cli/one-step-input.json`; append `--format markdown`. A rejected request is `data/chaos-theory-cli/solver-lyapunov-input.json` (exit2). Golden JSON/Markdown outputs preserve exact UTF8/LF bytes.

Sources retain their inventory rankings. Ranked Lorenz/Sugihara–May metadata/abstracts and Strogatz publisher metadata do not establish full-text method replication. Inspected UCAR DART10.10.1 model documentation and Moler2014 RK4 documentation support the equations and method. Only mathematical facts, original implementation and synthetic fixtures are redistributed. Full ranked-text access and rigorous bounds remain P1; advanced estimators/embedding/reservoir/empirical ensembles remain P2.
