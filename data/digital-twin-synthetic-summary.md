# Digital Twin — original scalar replay examples

These calculations verify bounded software arithmetic and chronology. They do not establish empirical state accuracy, calibrated uncertainty or a complete real-time twin.

| Example | Exact result |
|---|---|
| m0=0,P0=1,A=H=1,Q=0,R=1; first z=2 | Innovation2,S2,K1/2; posterior mean1,variance1/2 |
| Second z=2 | Innovation1,S3/2,K1/3; posterior mean4/3,variance1/3 |
| Independent constant-state batch oracle | Precision3,information4; mean4/3,variance1/3 |
| First update with R=3 | K1/4,mean1/2,variance3/4 |
| First update with H=2,R=1 | S5,K2/5,mean4/5,variance1/5 |
| Missing second observation | Correction skipped; mean1,variance1/2 |
| A=1/2,B=1,u=1,m0=4,P0=4,z=4 | Prior mean3,variance1; posterior mean7/2,variance1/2 |
| Same posterior, next u=0 versus1 | Means7/4 versus11/4; difference1; both variances1/8 |
| Second target2, filter prediction1 / persistence2 / open-loop0 | Squared errors1 /0 /4; no automatic filter superiority |

The independent fixture oracle uses information-form updates; its scenario moments use closed-form powers and control convolution. The separate batch precision check does not call either production recursion or the sequential oracle. Source editions remain NASEM2024, Grieves2014 whitepaper and the inspected Welch–Bishop2002 technical report.

`delayed` and `delayed-changed` demonstrate that changing a measurement unavailable at its scheduled update cannot alter the filter history. `not-yet-known` and `later-evaluation` change score eligibility without changing the accepted posterior or scenario fork. Delayed earlier observations may become eligible for persistence at a later origin, but are never assimilated retrospectively.

All-target filter/open-loop scores and common three-way scores have explicit target IDs, exclusions and denominators. The first observation has no previous-observation persistence forecast. Future scenarios contain controls only and never change history. H=0, zero prior variance and gains above1 are explicit supported numerical boundaries; R=0 is rejected.

Accepted/rejected JSON and Markdown reports live in `data/digital-twin-cli/`. Representative files are `sequential-markdown.md`, `missing-markdown.md`, `scaled-markdown.md`, `controls-markdown.md`, `delayed-markdown.md`, `cell-cap-markdown.md` and `bit-growth-markdown.md`. Rejections include explicit reasons. Integer growth and combined output limits are checked before expensive arithmetic or report generation.
