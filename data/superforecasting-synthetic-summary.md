# Technique 51 synthetic lifecycle review

Profile: `tetlock-mellers-binary-forecast-updates-v1`. All records are original synthetic software fixtures. No actual person, team or geopolitical skill is represented.

The frozen class has ten distinct historical members and three positive outcomes: exact observed rate **3/10**. The linked reference baseline is frozen before the target study. This is an observed frequency, not population certainty.

| Action | Forecast version | Probability | Primary selection |
|---|---|---|---|
| Original, Jan 1 | 1 | 1/5 | Preserved |
| Manual amendment, Jan 2 noon | 2 | 2/5 | Preserved |
| Assumed LR=3 update, Jan 2 evening | 3 | 2/3 | Selected |
| Duplicate evidence attempt | Rejected | Candidate retained only | Does not alter version 3 |
| Late amendment, Jan 4 | 4 | 9/10 | Preserved; after Jan 3 cutoff |

The positive event occurs Jan 5; outcome knowledge, source availability and resolution recording have separately retained times. The latest eligible pre-cutoff version is version 3. Its exact probability is 2/3.

| Metric | Exact result |
|---|---|
| Binary Brier | 1/9 |
| Two-category sum of squares | 2/9 |
| Paired baseline Brier | 49/100 |
| Paired absolute improvement | 341/900 |
| Relative loss ratio convention | 341/441 |

These are arithmetic results on a synthetic pair, not demonstrated forecasting skill. A separate frozen paired example gives model13/200 versus baseline1/4, difference37/200 and relative37/50.

Independent exact-category decomposition: probabilities[1/5,1/5,4/5,4/5], outcomes[0,1,1,1] give binary Brier19/100, reliability13/200, resolution1/16 and uncertainty3/16. The identity is19/100=13/200−1/16+3/16. Coarse calibration bins are separate.

Natural-log examples: p1/2 gives0.693147180560; a correct certain forecast gives0; a contradicted certain forecast returns `positive_infinity` with null numeric value. Empty/unresolved scoring returns `not_estimable`, never zero by default. Negative outcomes retain a null occurrence timestamp and require outcome knowledge at or after window end.

Replay accepted examples:

`python -m future superforecasting data/superforecasting-cli/lifecycle-report-input.json --format markdown`

`python -m future superforecasting data/superforecasting-cli/conditional-likelihoods-input.json --format json`

Replay a rejected update (exit2):

`python -m future superforecasting data/superforecasting-cli/reject-duplicate-evidence-input.json --format json`

The rejection corpus also covers duplicated historical events, source/catalog hashes, missing rights, class/baseline leakage, missing conditional history, both likelihoods zero, impossible certain priors, ancestry changes and unsupported expertise certification. Raw input hashes and both output hashes are saved in the CLI replay manifest.

Source guidance is attributed separately from editorial schema, bins, cutoff and display rules. The 2016 paperback and separately listed2015eBook are not conflated; later book chapters remain uninspected. No GJP dataset was acquired or its file-level rights certified. User-supplied source ownership, availability and independence are declarations. Local hash history needs an independent anchor for prospective integrity.

P1: full-book chapter locators, primary dataset rights/codebooks/revisions, empirical held-out protocol, stronger conditional-evidence safeguards, uncertainty/selection-bias analysis and independently anchored timestamps. P2: multinomial questions, team/ensemble aggregation, daily/tournament scoring and stronger dependence-aware inference.
