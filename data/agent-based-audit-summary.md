# Agent-Based Simulation — Technique 54 resource audit

Status: **Researching — Audit Only**. Technique53 closed at `2595ed8`, was pushed, and clean synchronized `main` was observed before this audit. No Technique54 runtime, executable profile, production fixtures, CLI, model run or benchmark was created.

All **four original ranked sources** and **five variation rows** remain unchanged: Epstein; Railsback/Grimm; Park et al.; Mesa. The original rank1 missing URL remains preserved in the inventory; a primary chapter witness is recorded separately as its resolved research source.

Epstein's 2006 Chapter1 discusses how local interactions can generate aggregate patterns, and explicitly separates explanation from prediction. The inspected [educational chapter witness](https://ocw.tudelft.nl/wp-content/uploads/GenerativeScienceEpstein_01.pdf) includes a publisher copyright notice permitting web reading/browsing while prohibiting redistribution. Detailed later chapters and CD-ROM models were not extracted.

Railsback and Grimm's authors site identifies the second edition as a 2019 release. Authorized publisher Chapter1/preface samples emphasize model purpose, documentation, testing and analysis. The currently indexed 2025 eBook format retains the 2019 copyright; it was not treated as a third edition. Later quantitative chapters and individual exercise/code licenses remain uninspected. See the [authors site](https://www.railsback-grimm-abm-book.com/) and [publisher preface](https://assets.press.princeton.edu/releases/p14270.pdf).

Mesa source was inspected at commit `fe24c24ee34762de2ff85d487af14bfb5cd1dbb2` dated2026-11-06. Its version file says **4.0.0a0**; this is an alpha source reference, not stable-release certification. The repository has moved to `mesa/mesa`; original inventory links are unchanged. Its Apache2 LICENSE and separate NOTICE were inspected, and no framework or source code was installed or vendored.

The primary [Life cell implementation](https://github.com/mesa/mesa/blob/fe24c24ee34762de2ff85d487af14bfb5cd1dbb2/mesa/examples/basic/conways_game_of_life/agents.py) uses B3/S23 and separates state calculation from commitment. The [model](https://github.com/mesa/mesa/blob/fe24c24ee34762de2ff85d487af14bfb5cd1dbb2/mesa/examples/basic/conways_game_of_life/model.py) uses a torus and random initial cells. The proposed first core instead uses explicit binary inputs and a named finite zero-exterior boundary. That boundary difference must remain visible.

A material Schelling discrepancy was found: documentation prose describes a minimum similar-neighbor count, but the [pinned agent code](https://github.com/mesa/mesa/blob/fe24c24ee34762de2ff85d487af14bfb5cd1dbb2/mesa/examples/basic/schelling/agents.py) compares the **fraction of occupied neighbors** with a threshold. The pinned default is0.4; no-neighbor similarity is0. Happiness is assigned before shuffled empty-cell moves, then recomputed. Fraction/count and simultaneous/sequential variants must not be merged. Source scheduling, vacancy behavior and random draws need a separate freeze before relocation support.

The recommended first core is **Finite-Grid Synchronous Binary Cellular Automata — B3/S23 Reference Scope**. It offers exact local rules and transparent CPU calculations with no new framework, LLM, GPU or external service. The five retained variations remain separate; this recommendation does not claim coverage of all their mechanisms.

Original literal and combinatorial examples include:

| Example | Exact expectation |
|---|---|
| Local Life rule |18 center-state/neighbor-count cases;3 yield an alive cell |
| Nine-bit center/neighborhood configurations |512 possibilities;56 birth,84 survival,140 next-alive configurations |
| Uniform local configuration fraction |140/512=35/128; combinatorial identity, not empirical probability |
| One isolated live cell | Dies; count1→0 |
| Centered2×2 block on4×4 board | Fixed point with4 live cells |
|3×3 horizontal blinker | `000/111/000` → `010/010/010` → initial state; period2, not fixed |
| Blinker count balance | Each transition has2 births and2 deaths; count remains3 in this example |
| In-place negative control | Early birth at[0,1] changes later[0,2] from2 to3 neighbors; different schedule |

Only literal tables, Fraction identities and binomial coefficients were evaluated. No cellular-automaton transition function or executable fixture was written. Twenty-six fixture families are planned, including edge/center rules, synchrony, counts, cycles versus fixed points, symmetry, scenario identity, rejection, resources and raw report replay. Active population is generally **not conserved or irreversible** in Life; that Technique52 assumption must not be imported.

The remaining variation audit found distinct mechanisms. Mesa's Sugarscape G1Mt example has capped sugar/spice growback, vision and welfare-based movement, metabolism/death and optional trade. A one-resource balance toy would not reproduce that model. The virus example can return infected agents to susceptible before optional resistance; its SIR summary is insufficient to specify the code. Neither example supplies empirical economic or clinical validity.

Park et al.'s [2023 paper, arXivv2](https://arxiv.org/html/2304.03442v2) describes memory retrieval, reflection and planning for a25-agent sandbox. Its believability evaluations and reported memory failures do not establish real-human forecast accuracy. The [author repository](https://github.com/joonspk-research/generative_agents/tree/fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4) has Apache2 source licensing, while the paper uses arXiv's non-exclusive distribution license and the README separately acknowledges external artists. Code licensing does not certify every sprite, map or dataset. No assets, prompts, memory traces or model calls were copied or run.

Proposed bounds are grids up to64×64,256 ticks and8 scenarios, subject to combined1million cell-tick,9million neighbor/cell-work,100000 returned-state-cell and20000 count-cell reservations. Individual maxima cannot be combined freely. Proposed5-second/128-MiB targets are **unmeasured for #54**.

P1: freeze the exact executable conventions and independent oracles; resolve source/version conflicts; inspect legitimate later chapters and per-resource rights; measure CPU/memory; design any empirical calibration and held-out evaluation. P2: Schelling scheduling variants, full Sugarscape, calibrated epidemiological/social models, LLM architecture, stochastic ensembles and larger coupled simulations. No real human, clinical, urban or book-landscape dataset was acquired or certified.
