# Technique57 — versioned binary linear pool reference

Run `python -m future collective-intelligence data/collective-intelligence-cli/weighted-input.json --format markdown`.

Two forecasts1/5 and4/5 average to1/2. Declared weights1 and3 normalize to1/4 and3/4,giving13/20. With outcome1,the weighted binary Brier loss is49/400 and the separately named two-category score is49/200. The equal pool and fixed1/2 baseline both score1/4 on that question. Individual losses are16/25 and1/25,compared on the identical question ID.

Changing that weighted example's outcome to0 leaves its model identity and13/20 forecast unchanged while changing binary loss to169/400. Outcome labels score predictions; they do not select weights or probabilities. The symmetric1/2 equal-pool control also remains invariant under a label flip,including its1/4 squared loss.

The independent four-question decomposition uses probabilities1/5,1/5,4/5,4/5 and outcomes0,1,0,1. Mean binary Brier is17/50,reliability9/100,resolution0 and uncertainty1/4. Their exact identity holds; the two-category mean is17/25. Exact identical-probability grouping is separate from the ten descriptive calibration bins. Read-only numerical comparison matches the frozen Technique51 scoring conventions; no51interface or release was changed.

One latest eligible revision is selected per question/forecaster. Late or outcome-informed amendments cannot displace an earlier eligible record. The latest eligible abstention withdraws that forecaster without restoring an older probability. Missing and declared-zero-weight participants remain visible. Zero available contributing weight returns not_estimable,not an invented probability. Only matched resolved TEST questions enter the primary score; TRAIN summaries remain separate. Cross-partition question-dependency groups reject.

Dependent and LLM-simulated forecasters remain explicitly labeled. Roster size is not an independently verified sample size. Local hash chains cannot prove truthful timestamps or prevent an owner from rewriting all history; retain external anchors if that assurance matters. Question-definition hashes exclude later resolution labels. Forecaster/group/rights declarations are not independent certifications.

This release verifies pooling/scoring and declared chronology. It does not reproduce the full Mellers tournament,daily/question-standardized analyses or team-median leaderboards. It does not learn weights from current outcomes,run Delphi rounds,call LLM APIs or establish empirical crowd superiority. The repository corpus is self-authored synthetic; user-supplied participant records remain unvalidated and require rights/consent review before publication or empirical claims.

Measurements cover complete in-process reports,separate Python allocation tracing and full CLI invocations. Native peak memory covers the whole helper and all workloads; it is not a CLI-child or per-workload memory measurement. See `data/collective-intelligence-resource-measurements.json` for exact inputs,hashes and environment. Source access,advanced weighting,real datasets and integrations remain P1/P2.
