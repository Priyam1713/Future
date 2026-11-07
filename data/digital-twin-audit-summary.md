# Digital Twin Simulation — Technique 53 resource audit

Status: **Researching — Audit Only**. Technique 52 closed at `e2189fb`, its push succeeded, and clean synchronized `main` was observed before this audit. No Technique 53 engine, executable profile, CLI, filter run or benchmark was created.

The two original resource ranks and four variation rows remain unchanged. Rank 1 is the National Academies' 2024 consensus report, DOI10.17226/26894. Its definition combines physical-data updates, prediction and decision feedback; its VVUQ discussion distinguishes software verification from empirical validation. Chapter 4 addresses measurement quality and governance, while Chapter 5 explains why assimilation alone does not constitute a complete twin. See the [publisher's landscape chapter](https://www.nationalacademies.org/read/26894/chapter/4) and [physical-to-virtual chapter](https://www.nationalacademies.org/read/26894/chapter/7).

Rank 2's exact title resolves to Michael Grieves's **2014 whitepaper**, not a verified book with an ISBN. The inspected author paper, hosted by USP for teaching, has a cover plus seven numbered pages and a 2014 author copyright notice. It describes the physical product, virtual product and their information connections, with manufacturing comparison examples. A NASA search hit cites the paper but is a different document; it was not substituted for the ranked source. No universal quantitative transition law was extracted from Grieves. See the [institutional witness](https://edisciplinas.usp.br/pluginfile.php/8935104/mod_resource/content/1/MichaelGrieves-white-paper-2014.pdf).

The recommended first scope is **Offline Scalar State-Space Assimilation Replay and Scenario Scope**. One scalar asset proxy, declared linear dynamics, timestamped observations, explicit measurement/process variances and future control scenarios offer a useful bounded core. A synthetic replay would be labeled a state-estimation/scenario model. Archival observations would require their own rights and measurement review. Real-time twin status, physical synchronization and decision feedback remain unimplemented.

The numerical supplement is Welch and Bishop's primary technical report, inspected through an [MIT course witness](https://www.mit.edu/course/16/16.070/www/project/PF_kalman_intro.pdf). That PDF explicitly says **March 11, 2002**. The author-hosted URL associated with the indexed 2006 update returned404 through both access methods; these versions are not conflated. Tables1-1/1-2,p5 provide the linear prediction/correction equations. A scalar exact-rational implementation is an editorial recommendation, not code copied from the tutorial.

Original known-answer arithmetic includes:

| Original example | Exact result |
|---|---|
| Prior mean0, variance1; A=H=1,Q=0,R=1; first observation2 | Gain1/2, posterior mean1, variance1/2 |
| Second observation2 under the same model | Gain1/3, posterior mean4/3, variance1/3 |
| Independent constant-state batch precision check | Precision3, information4; mean4/3, variance1/3 |
| First update with measurement variance3 | Gain1/4, mean1/2, variance3/4 |
| First update with H=2,R=1 | Gain2/5, mean4/5, variance1/5 |
| Missing observation after the first update | Skip correction; mean1, variance1/2 |
| Second-target error: filter prediction1 versus last observation2, target2 | Squared errors1 versus0; no guaranteed filter superiority |

Only literal Fraction identities and the independent batch calculation were evaluated. There is no recursive state-space simulator or production fixture corpus in this audit. The fixture plan contains27 families, covering prediction/correction, noise assumptions, missing data, unobservable measurements, chronology, availability, leakage, identities/units, baselines, scenario forks, rights, bit-growth limits and deterministic reports.

The proposed CPU-only budget is one scalar asset, up to256 observation rows,128 forecast steps and8 scenarios, subject to combined2048-step,20000-cell and8192-bit intermediate-integer caps. These are recommendations to freeze and test before implementation. The proposed5-second/128-MiB targets remain **unmeasured for #53**.

Both ranked sources retain copyright. The National Academies explicitly restricts PDF redistribution; free reading does not grant reuse rights. No books, article bodies, figures, tutorial code, contact traces or asset datasets are redistributed. No specific real-asset dataset's rights, consent, calibration or predictive suitability was certified. See the [publisher's permissions policy](https://www.nationalacademies.org/request-rights-and-permissions).

P1: freeze the executable contract, chronology and units; freeze independent fixtures; implement and measure the bounded filter/baselines/scenarios; resolve source-version access; review any exact empirical dataset and validation design. P2: multivariate/nonlinear filters, delayed observations, learned parameters, urban or personal twins, coupled populations, live telemetry and physical control. Those variations remain in the inventory with their original names and rankings.
