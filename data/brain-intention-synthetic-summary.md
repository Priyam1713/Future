# Technique 55: synthetic offline classification reference

Profile: `brain-intention-synthetic-offline-classification-v1`.

This implementation verifies synthetic classification and declared leakage diagnostics. It does not ingest EEG/fMRI, reproduce CSP/LDA, read intentions, establish clinical accuracy or certify cross-session generalization.

Run the worked example:

```powershell
python -m future brain-intention data/brain-intention-cli/worked-input.json --format markdown
```

The declared two-feature training table contains A=(0,2),(2,4) and B=(4,2),(6,4). The exact fitted centroids are A=(1,3), B=(5,3). Squared distances at (2,3) are 1 and 9; at (4,3), 9 and 1. At (3,3), both are 4 and the frozen tie convention selects A.

The worked TEST labels A,A,B,B and predictions A,B,B,B produce confusion matrix `[[1,1],[0,2]]`, with actual classes as rows and predicted classes as columns. Accuracy and balanced accuracy are both 3/4. TRAIN class counts tie, so the majority baseline predicts A and scores 1/2 on the same four TEST IDs. If a true TEST class is absent, fixed-binary balanced accuracy is explicitly not estimable.

For raw synthetic windows, feature order is channel-major mean then population variance. The window [-1,1,-1,1] has mean 0 and population variance 1. Its sample variance 4/3 is an independent denominator check, not the classifier feature. Adding 5 preserves variance 1; doubling amplitude makes variance 4. Constant windows have variance 0. These are mathematical features, not band-specific neural signal features.

The ideal independent fair-binary toy tail for at least 8 correct out of 10 is 7/128. This arithmetic is not an empirical EEG significance result and does not account for correlation, selection or multiplicity.

TRAIN-only centroids and baseline selection exclude TEST labels/features. Split diagnostics require either disjoint subjects or one subject with disjoint runs. Source files map to one subject/run; dependent trials and overlapping source intervals cannot cross partitions. Units, task/run annotations, availability and label timing are explicit declarations. All session fields are null; no session claim is inferred from run IDs. Only unfiltered, self-authored synthetic data are supported. T1/T2 annotations in the optional synthetic hands/feet task are tied specifically to runs6/10/14.

The independent corpus was frozen before production. Its original accepted validation-only example accidentally reused a TEST subject. Versioned errata correct that identity and its original-corpus hash binding, preserving the original fixture and every numerical expectation. The original leaking input still rejects. See `knowledge/brain_intention_fixture_errata_v2.json` and the independent verifier.

Measurements in `data/brain-intention-resource-measurements.json` cover complete in-process reports, separate Python allocation tracing and one full CLI invocation per workload. The native process peak includes the whole helper, imports and all workloads; it is not a CLI-child or per-workload memory bound. Measurements apply to the recorded local examples only.

Source access and rights gaps remain recorded in the audit: full Soon methods/supplement, original participant-use restrictions, immutable EEG file manifests and an independently designed empirical replication. Public database access does not waive consent or privacy rights. No raw human data, copyrighted book/article bodies, figures or third-party code are redistributed.
