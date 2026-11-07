# Technique56 — causal AI resource audit only

Recommend a finite, exact back-door reference: validate a small assumed causal DAG and supplied adjustment set, exclude descendants of treatment, check d-separation in the graph with outgoing treatment edges removed, check overlap and standardize. Graph learning, general do-calculus and individual counterfactual prediction remain unsupported. A failed supplied set is not a universal nonidentifiability proof.

Independent toy: enumerate80 equally likely structural cases (Z binary,E_X four states,E_Y ten states). The frozen audit records full original equations and joint counts. Observational risks are1/5 and3/5; forcing X gives3/10 and1/2,so observational contrast2/5 differs from causal contrast1/5. Later independent fixtures must reproduce this through structural enumeration before implementing adjustment.

All-observed finite tables should pass exact graph-factorization compatibility checks. Positivity must hold at every positive-mass adjustment stratum. Zero-mass strata are explicit; no smoothing. Latent graphs remain diagnostic/unsupported in the first core. Compatibility does not establish that the causal graph or consistency/exchangeability assumptions are true.

Original3ranked sources and5variation names remain verbatim in the audit. Pearl second-edition2009 metadata and author/excerpt witnesses were inspected; repeated deeper chapter retrieval timed out. What If latest author link points to19August2026,whose11.3MB PDF exceeds the web retrieval limit; indexed dated primary passages support standardization/identification conditions without claiming full latest-book access. DoWhy versioned docs distinguish identification from estimation and back-door surgery from interventions. No copyrighted body,figures,code or data redistributed; no runtime or benchmark executed. Resource caps and≤5s/128MiB are proposals. Source access,empirical assumptions and latent identification remain P1; general identification,counterfactual and continuous extensions P2.

Primary sources:
- [Causality,2nd edition;2009;DOI10.1017/CBO9780511803161;digital2013](https://www.cambridge.org/core/books/causality/B0046844FAE10CBF274D4ACBDAEB5F5B)
- [Causal Inference: What If;2020 citation;latest author link19August2026](https://miguelhernan.org/whatifbook)
- [DoWhy project; established2018](https://www.microsoft.com/en-us/research/project/dowhy/)
- [Causality2nd edition2009 author page](https://bayes.cs.ucla.edu/BOOK-2K/)
- [Causality chapter3 corrected June2013;42PDFpages](https://web.cs.ucla.edu/~kaoru/CAUSALITY-REPRINTED-W-CORRECTIONS-2013/causality-ch3-june2013.pdf)
- [DoWhy0.13 Backdoor criterion documentation](https://www.pywhy.org/dowhy/v0.13/user_guide/causal_tasks/estimating_causal_effects/identifying_causal_effect/backdoor.html)
- [DoWhy0.14 graph documentation](https://www.pywhy.org/dowhy/v0.14/_modules/dowhy/graph.html)
- [NetworkX3.7 D-Separation documentation](https://networkx.org/documentation/stable/reference/algorithms/d_separation.html)
- [What If author2January2025 edition,indexed chapters2/3](https://miguelhernan.org/s/hernanrobins_WhatIf_2jan25.pdf)
