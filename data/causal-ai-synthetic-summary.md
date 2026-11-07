# Technique56 — finite causal DAG reference

Run `python -m future causal-ai data/causal-ai-cli/confounding-input.json --format markdown`.

The original synthetic structural model enumerates80 equally likely combinations of binary Z,four-state treatment noise and ten-state outcome noise. It supplies complete joint counts,not sampled estimates. Observational risks for X=0 and1 are1/5 and3/5. Independent intervention enumeration forces X before evaluating Y and gives3/10 and1/2. Exact back-door standardization over Z reproduces those interventional risks. Last-minus-first contrast is1/5; the separately named first-minus-last contrast is-1/5. The observational last-minus-first contrast is2/5.

The core checks a supplied adjustment set using the original sufficient back-door criterion. No adjustment variable may descend from treatment; the treatment and outcome must be d-separated after removing outgoing treatment arrows. This graph surgery differs from replacing the treatment assignment mechanism under an intervention. A direction-state active-trail implementation is verified against independent simple-path/collider enumeration on256 graph cases.

Complete categorical joint tables include zero cells and sum exactly to1. All-observed graphs must be exactly compatible with the table factorization. Every positive-mass adjustment stratum must contain every declared treatment level. Zero-mass strata are listed with undefined conditionals and skipped. No smoothing or extrapolation is applied. Descendant adjustment,open confounding/collider paths,incompatible distributions and missing positivity yield no interventional estimate. Latent graphs are diagnostic/unsupported in this release.

This software does not discover causality from correlations. The input causal graph,consistency,exchangeability and absence of selection bias are assumptions. Exact table/graph compatibility does not establish those assumptions or empirical validity. Failure of one supplied adjustment set does not prove that all identification methods fail. General do-calculus,front-door/instrumental-variable methods,continuous estimators and individual counterfactual uplift remain deferred.

Only self-authored synthetic data are supported. Source metadata/rights and access limitations are recorded in the source freeze and audit. No copyrighted book body,figure,third-party code or human dataset is redistributed. CPU/memory measurements are local complete-report observations; the native memory peak includes the whole helper and is not a CLI-child or per-workload measurement.
