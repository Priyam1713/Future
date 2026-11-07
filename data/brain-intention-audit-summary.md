# Technique 55 — Brain-Based Intention Prediction: audit only

Recommendation: a synthetic, exact-arithmetic offline classification reference with explicit leakage diagnostics. No Technique55 runtime, executable profile, production fixtures or empirical benchmark was built.

All three original ranked sources and all four variation names are preserved verbatim in the audit. Rank2 resolves to Soon et al., Nature Neuroscience11,543–545(2008), DOI10.1038/nn.2112, a journal article rather than the inventory's provisional book label. Full publisher methods/supplement were blocked by its identity gateway; no precise accuracy, split or lead-time certification follows. The Wolpaw2012 book and chapters10/25 were inspected through official metadata, TOC and abstracts only.

EEGMMIDB1.0.0 supplies64-channel160Hz cued motor tasks. T1/T2 labels depend on run family. MNE's published CSP/LDA example uses subject1,runs6/10/14 (imagined hands versus feet),post-cue1–2s training windows,7–30Hz noncausal filtering and trial-level shuffled splits. This does not demonstrate cross-subject generalization, online availability or prediction of unrestricted future decisions. No EDF files were downloaded. Readiness potentials, fMRI decoding and non-neural behavioral proxies retain separate measurement/interpretation boundaries.

Freeze train/validation/test blocks before processing; fit transformations only on train. Keep overlapping windows and dependent trials within one partition. Choose subject-disjoint or explicitly within-subject held-out-run claims; runs are not verified sessions. Use train-majority predictions on matched test IDs and name absent-class conventions. A balanced iid binomial null is not automatic EEG significance.

The proposed editorial reference uses exact mean/population variance and binary nearest arithmetic centroids with a named A tie, not CSP/LDA. Independent literal examples: variance([-1,1,-1,1])=1; centroidA=(1,3),B=(5,3); point(2,3) distances1/9,point(4,3)9/1,tie(3,3)4/4. Confusion[[1,1],[0,2]] gives accuracy/balanced accuracy3/4; train-majority tie baseline1/2. An iid toy8/10 upper tail is7/128, not empirical evidence. All28 future fixture families are plans only.

ODC-By1.0 licenses database rights with attribution, not blanket individual-content, consent or privacy rights. Original participant-use/IRB details and per-file hashes remain P1, together with lawful access to the full fMRI methods and a separate empirical EEG replication. No copyrighted body, figures, code or dataset is redistributed. CPU≤5s/peak≤128MiB and numerical size caps are unmeasured proposals. P2 retains RP/fMRI replication, larger studies and deployment validation.

Primary sources:
- [Brain–Computer Interfaces: Principles and Practice; 23 January 2012; DOI 10.1093/acprof:oso/9780195388855.001.0001](https://academic.oup.com/book/1700)
- [Unconscious Determinants of Free Decisions in the Human Brain; Nature Neuroscience 11,543–545; online 13 April 2008; DOI 10.1038/nn.2112](https://www.nature.com/articles/nn.2112)
- [EEG Motor Movement/Imagery Dataset 1.0.0; 9 September 2009; DOI 10.13026/C28G6P](https://www.physionet.org/content/eegmmidb/1.0.0/)
- [Chapter 10, Operating Protocols; pp189–196; 2012](https://academic.oup.com/book/1700/chapter-abstract/141290465)
- [Chapter 25, reliability and dissemination; pp387–392; 2012](https://academic.oup.com/book/1700/chapter-abstract/141298120)
- [Open Data Commons Attribution License 1.0](https://www.physionet.org/content/eegmmidb/view-license/1.0.0/)
- [MNE 1.13.2 documentation; eegbci.load_data](https://mne.tools/stable/generated/mne.datasets.eegbci.load_data.html)
- [MNE 1.13.2 Motor imagery decoding from EEG data using CSP](https://mne.tools/stable/auto_examples/decoding/decoding_csp_eeg.html)
- [Time of conscious intention to act in relation to onset of cerebral activity (readiness-potential); Brain106,623–642;1983; DOI10.1093/brain/106.3.623](https://training.incf.org/sites/default/files/2023-05/Libet%20-%20Time%20of%20Conscious%20Intention%20to%20Act.pdf)
- [An accumulator model for spontaneous neural activity prior to self-initiated movement;PNAS109,E2904–E2913;2012;DOI10.1073/pnas.1210467109](https://pmc.ncbi.nlm.nih.gov/articles/PMC3479453/)
- [NearestCentroid official documentation;1.9.1 observed](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestCentroid.html)
- [Common pitfalls: data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage)
- [GroupKFold official documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html)
- [balanced_accuracy_score official documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html)
- [scipy.stats.binomtest official documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html)
