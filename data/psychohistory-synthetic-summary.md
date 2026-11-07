# Psychohistory — original synthetic worked examples

These examples verify bounded software mathematics, not population laws or real-world forecasting.

| Example | Exact result |
|---|---|
| Path 0–1–2, phi=1/2, seed0 | 100 → 110 → 111; counts1,2,3 |
| Forward in-place path sweep | Can produce111 immediately; different update convention |
| Star4, center seed, phi=2/3 | Final4 |
| Complete4, same seed and phi | Final1; extra links need not increase fractional-threshold adoption |
| Two linked nodes, all four equiprobable initial states | Final counts0,2,2,2 |
| Exhaustive final count | Mean3/2, population variance3/4 |
| Exhaustive final fraction | Mean3/4, population variance3/16 |
| Same-state persistence gains | 0,1,1,0; mean1/2, population variance1/4 |
| Path threshold1/2 versus2/3 | Final3 versus1; hypothetical model sensitivity |

The two-node calculation enumerates a supplied equal-weight initial-state design. It is not a Monte Carlo estimate. Ideal iid Bernoulli initial moments are E=N*rho, Var=N*rho*(1-rho) before fixed overrides; those formulas do not describe correlated final cascade counts.

Every accepted report records input, graph, model, schema/profile, source, code and shared-stream identities. The corpus contains accepted and rejected JSON/Markdown pairs, including an isolated count-budget refusal and strict PRNG threshold equality. Fixed points are distinguished from truncation with a bounded next-state check. No-change states are not duplicated in actual trajectories; aggregate trajectories hold absorbing states to the requested horizon.

Reports are in `data/psychohistory-cli/`: `path-markdown.md`, `topology-markdown.md`, `exhaustive-markdown.md`, `threshold-comparison-markdown.md`, `identical-markdown.md`, `unknown-field-markdown.md` and `count-only-cap-markdown.md`.
