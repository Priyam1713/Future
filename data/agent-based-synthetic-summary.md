# Agent-Based Simulation — original finite-grid B3/S23 examples

The profile uses explicit binary inputs, finite zero-exterior boundaries and synchronous updates. These are synthetic mathematical examples, not human/social forecasting evidence. The pinned Mesa source uses toroidal boundaries and random initialization; this implementation deliberately names its different conventions.

| Independent example | Verified expectation |
|---|---|
|18 center-state/neighbor-count cases | Only dead+3,alive+2,alive+3 produce a live cell |
|512 local binary configurations |56birth+84survival=140next-alive;372next-dead |
| Exact local fraction |140/512=35/128; combinatorial identity, not empirical probability |
| Empty3×3 board | Fixed after the first observed transition |
| Single isolated live cell | Dies; later empty state is fixed |
| Centered2×2 block on4×4 |4live cells, period1 fixed point |
|3×3 blinker |000/111/000 →010/010/010 →initial; period2, not fixed |
| Blinker transitions |2births and2deaths per tick |
|7×7 glider after4ticks | Exact initial live coordinates shift by(1,1) |
| Equal-count horizontal/vertical blinkers | Count difference0, Hamming distance4 |
| Row-major in-place negative control | Cell(0,2) can becomealive; synchronous result isdead |

Initial glider coordinates are(1,2),(2,3),(3,1),(3,2),(3,3). At tick4 they are(2,3),(3,4),(4,2),(4,3),(4,4). The independent pre-engine oracle uses sparse live-coordinate sets and neighbor Counters; production uses complete byte snapshots and explicit neighbor-index lists. Interior translations and rectangular rotations/reflections transform geometry as well as coordinates. Arbitrary node permutations are not valid grid symmetries.

Execution always reaches the requested tick, including after detecting a repeat. `blinker-odd` returns the correct vertical phase at tick5. `full-horizon-fixed` executes256 ticks of a fixed block without early stopping. A zero-tick request fabricates no transition: births/deaths are null, classification is unclassified, and the classification horizon is marked truncated. A one-tick blinker is also unclassified despite unchanged counts.

Scenario comparisons hold geometry, rule, neighborhood, boundary, schedule and horizon fixed. Identical inputs have zero count differences and Hamming distances. Initial and final states are always included; full traces are optional and bounded. Exact full-state equality establishes a cycle; aggregate counts or hash equality alone do not.

Strict rejection reports include toroidal/wrapped boundaries, in-place scheduling, other rules/variations, nonbinary or ragged boards, unsupported empirical inputs and targeted combined work/state/count-cap violations. All saved reports use raw UTF8/LF bytes and corpus-local Git attributes.

Representative pairs are in `data/agent-based-cli/`: `block-markdown.md`, `blinker-markdown.md`, `glider-markdown.md`, `scenario-comparison-markdown.md`, `identical-markdown.md`, `torus-markdown.md` and `work-cap-markdown.md`. P1/P2 retain the other four ABM variations and their source-specific rules, rights, numerical verification and empirical validation requirements.
