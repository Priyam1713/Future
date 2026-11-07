# Technique58 — prediction-market audit only

Recommend a single offline binary LMSR play-credit market with fixed positive liquidity,zero initial quantities and one-credit winning-share payouts. No real-money deposits,trading,services or external settlement. Mechanism correctness does not establish calibrated probabilities or empirical forecasting accuracy.

All2original ranked sources and4variation names remain verbatim. Wolfers/Zitzewitz2004 provides economic/design context. Hanson's official journal PDF is2007,JPM1,3–15; its web page shows a2012upload field,and the author working draft is January2002. These are distinct provenance records. Primary Chen/Vaughan2010 Section2 explicitly supplies cost differences,gradient prices,LMSR log-sum-exp potential and b log N worst-case maker loss; it remains an unranked supplement. Copyright bodies,figures,code and data are not redistributed.

Use Decimal80 stable max-shift production with an independent Decimal120 direct-exp oracle. Transcendentals are approximate. Proposed monetary quantum1e-24 applies to total cost potentials; executed charges are differences of rounded potentials,so cash accounting and unchanged-state reversals telescope exactly. With zero initial q,the ideal binary bound is b ln2. Rounding/numerical margins must be explicit; propose reserve ceiling(b ln2+2quanta) and independently verify before production.

Quotes do not reserve cash or execute. Confirmed trades bind quote intent,actor and economic revision; recheck balances/positions and refuse stale quotes. Long-only holdings prohibit naked shorting. Intent IDs bind payloads independently of delivery time; retries have no duplicate financial effect,while conflicting reuse refuses. Explicit ordered action refusals leave financial state unchanged. Trades stop strictly before close; declared-authority resolution at/after close settles once. Local identity checks are not external authentication.

Literal Decimal120 anchors are stored in the audit,including initial1/2prices,the exact cash-grid buy/reverse charges and balanced one-share-each total charge/payout1. No production model or market was executed. Planned31fixture families cover numerical stability,prices,quotes,ledger/funding,duplicate effects,cutoff/authority/settlement and provenance. Proposed≤5s/128MiB and size/precision limits are unmeasured. Larger markets,advanced scoring/auctions and interfaces remain P1/P2; real-money/external trading is unsupported.

Primary sources:
- [Prediction Markets;Journal of Economic Perspectives18(2),107–126;Spring2004;DOI10.1257/0895330041371321](https://www.aeaweb.org/articles?id=10.1257%2F0895330041371321)
- [Logarithmic Market Scoring Rules for Modular Combinatorial Information Aggregation;Journal of Prediction Markets1(1),3–15;2007;DOI10.5750/jpm.v1i1.417](https://www.ubplj.org/index.php/jpm/article/view/417)
- [Official2007journal PDF;13pages;JPM1,3–15](https://www.ubplj.org/index.php/jpm/article/download/417/448)
- [Author working draft;January2002;12pages](https://hanson.gmu.edu/mktscore.pdf)
- [Published2004JEP author witness;20pages](https://users.nber.org/~jwolfers/papers/Predictionmarkets.pdf)
- [Connections Between Markets and Learning;ACM SIGecom Exchanges9(1),June2010;5pages](https://econcs.seas.harvard.edu/sites/g/files/omnuum6346/files/econcs/files/chensigecom10.pdf)
- [Python3.12 Decimal documentation;3.12.16docs observed,runtime3.12.10 tested separately](https://docs.python.org/3.12/library/decimal.html)
