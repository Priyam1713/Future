# Technique58 — offline binary LMSR play credits

Run `python -m future prediction-markets data/prediction-markets-cli/settle-yes-input.json --format markdown`.

This is a single synthetic binary market with fixed positive liquidity,zero initial quantities and play-credit endowments. It never deposits,wagers,trades or settles actual money or contacts an external service. Mathematical mechanism/accounting correctness does not establish market efficiency or calibrated real-world probabilities.

With b=1 and initial quantities(0,0),prices are1/2 and1/2. Buying one YES share charges0.620114506958277524631763 play credits on the frozen10^-24 cash grid. Reversing that trade at unchanged intervening state refunds the identical amount. Buying one of each outcome costs1 in total; either outcome then pays1,leaving the maker's net profit0. Cash values telescope because charges are differences of rounded total cost potentials,not separately rounded incremental analytic charges.

Prices/costs use an explicit80-digit Decimal context and max-shift log-sum-exp. Independent verification uses145 direct-exp120-digit vectors and a200-term exact rational atanh-series interval for ln(2). The absolute price/cost tolerance is10^-60; ledger cash-grid equality is exact. Both softmax numerators are evaluated separately,so an extreme complement stays positive even when its dominant partner rounds to1. Normalization is tolerance-based,not an exact-real representation claim.

The ideal zero-initial binary maker loss is at most b ln(2). A separately computed synthetic reserve covers that bound plus an explicit rounding/numerical margin. Every accepted trace is independently checked for exact rational cash conservation,position/quantity equality,total-potential charges and funded exposure. Initial user credits and the maker reserve are separate fictional endowments. There are no later deposits,fees,transfers,shorting or leverage.

Quotes show hypothetical charges/feasibility without reserving cash or executing. Confirmed execution requires the same actor and current economic revision; stale/used quotes,budget failures and unowned sales refuse without financial mutation. Intent identifiers exclude delivery timestamp for retries; identical intent repeats have no duplicated financial effect,while conflicting reuse refuses. Local hash-chained successful entries are separate from refused/duplicate attempts. File ownership still permits history rewriting without an external anchor.

Trades/quotes stop strictly before close. At/after close,the clock closes the market; declared-resolver equality permits one-time settlement. This is an offline identity declaration,not authenticated external authority. Historical recorded positions remain after settlement with zero remaining payout liability. Final modeled prices are historical diagnostics,not executable post-resolution quotes. Strict-before-close differs from51/57's inclusive forecast cutoff and requires explicit integration mapping.

The source record distinguishes Hanson2007journal content,2012web upload metadata and the2002author draft. The unranked Chen/Vaughan2010 primary supplement supplies cost-function equations and the loss bound. Copyright bodies,figures,third-party code and participant data are not redistributed. Continuous double auction,combinatorial markets,live user services and empirical validation remain P1/P2 or unsupported.

Measurements cover complete reports and full CLI calls. Native memory is the whole helper peak across imports,all workloads and allocation tracing; it is not a CLI-child or per-workload measurement. Exact inputs,environment and hashes are in `data/prediction-markets-resource-measurements.json`.
