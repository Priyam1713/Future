# NOAA CPU forecasting benchmark

Retrospective evaluation on a fixed revised data snapshot;historical publication vintages are unverified. Software prefix isolation does not prove as-of historical data availability.

Validation selected **drift**. Its held-out MAE is higher than seasonal naive;the selected configuration remains fixed. All-candidate test results below are diagnostic.

| Candidate | Validation MAE (ppm) | Test MAE (ppm) | Test RMSE (ppm) | Test MASE | Test MAE / seasonal naive |
|---|---:|---:|---:|---:|---:|
| seasonal_naive_m12 | 2.619466666667 | 2.179400000000 | 2.252416184160 | 0.980588339942 | 1.000000000000 |
| naive | 2.938033333333 | 2.738600000000 | 3.350477975852 | 1.232289588957 | 1.256584381022 |
| drift | 2.598969559090 | 2.537249963267 | 3.091598646287 | 1.141503439620 | 1.164196551008 |
| mean | 23.115995560943 | 26.617450437309 | 26.718852519489 | 11.975161744635 | 12.213201081632 |
| ses_alpha0.2_initial_y1 | 2.953697850852 | 2.636690628054 | 3.098201330135 | 1.186256023421 | 1.209824092894 |
| ses_alpha0.5_initial_y1 | 2.925810405202 | 2.679586316256 | 3.180210861440 | 1.205676193299 | 1.229506431245 |
| ses_alpha0.8_initial_y1 | 2.942001317647 | 2.730401966354 | 3.311477752152 | 1.228595209645 | 1.252822779827 |

All4,200planned cells succeeded:seven candidates ×25origins ×12horizons ×2partitions. Each partition has36distinct target months and300cells per model;overlapping errors are dependent. No significance or universal-superiority claim.

## Selected drift: held-out horizon scores

| Horizon (months) | MAE (ppm) | RMSE (ppm) | Bias actual−forecast (ppm) | Scored cells |
|---:|---:|---:|---:|---:|
| 1 | 1.107809952044 | 1.290585271175 | 0.027837373578 | 25 |
| 2 | 2.003428605532 | 2.332456816300 | 0.038474747155 | 25 |
| 3 | 2.708880854591 | 3.127798077716 | 0.027112120733 | 25 |
| 4 | 3.295777399374 | 3.696408906554 | 0.074549494311 | 25 |
| 5 | 3.638811644064 | 4.015842447030 | 0.091986867888 | 25 |
| 6 | 3.714163994018 | 4.134350718794 | 0.093424241466 | 25 |
| 7 | 3.618376511540 | 4.047163226634 | 0.027261615043 | 25 |
| 8 | 3.326297168569 | 3.805831052587 | -0.043701011379 | 25 |
| 9 | 2.972084314641 | 3.331118101882 | -0.062663637801 | 25 |
| 10 | 2.223138095162 | 2.511809746432 | -0.022426264224 | 25 |
| 11 | 1.244361755424 | 1.481571173630 | 0.057811109354 | 25 |
| 12 | 0.593869264251 | 0.677455350916 | 0.151248482932 | 25 |

## Resource evidence

Cold first core call: 1.1808s. Warm median of3core calls: 1.1594s. Fresh CLI wall: 2.6805s. Peak native working set: 132526080bytes (126.4MiB).

Core calls include full fitting,evaluation,metrics and deterministic report construction before outer JSON/Markdown serialization. CLI time includes process/imports and stdout capture. OS caches were not flushed. Measurements apply to the recorded Windows machine;see the frozen resource record for native memory sampling and environment details.

## Provenance and full evidence

- NOAA dataset: `303c231dd00ba7cf6302e02dbb25525b91e226008a71b15856f25f775aa9645c`.
- Source snapshot: `0ce4e7749217b4af2cca8e0bdf263856ad59b0a2946d4e98c7b22ccfbff21cad`.
- Profile: `ed2490bf3ddc5861b3a406e2ba8aa93b3f2b2fe33e0b7917371e5c26875e7fdb`.
- Frozen full report: `9a07847595bc61d0f9816a2f40dc67972fe79ebd52f739e9851ce9ff9ba1931e`.
- Full ledger: [JSON](ai-predictive-modeling-noaa-benchmark.json) and [Markdown](ai-predictive-modeling-noaa-benchmark.md).
- [Measured resources](ai-predictive-modeling-resource-measurements.json) and [independent verification](ai-predictive-modeling-verification.json).

NOAA attribution and data-use conditions accompany the full report. QC/calibration revisions,midmonth correction,Maunakea substitution and missing historical publication vintages prevent certification as original as-of-real-time forecasts. No Chronos,ARIMA,optimized ETS,tree or neural forecasting was run.
