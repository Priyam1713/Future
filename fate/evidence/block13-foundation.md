# Palmistry release evidence and boundaries

- **Source.** The pinned Library of Congress Ninth Edition scan SHA-256 is `37f492cd2ec3df8ad840e17782c92f10ccded2ce370fbb4f59679e2e937cf4d0`. The underlying edition has 37 bounded rules covering three major lines, six hand outlines and eight normal mounts. Four consumer supplement rules were checked against printed p. 30 (scan page 56) and p. 65 (scan page 113). The previous independent edition fixtures are in `tests/fixtures/palmistry_cheiro_examples.json`. [Original scan](https://www.loc.gov/resource/gdcmassbookdig.cheiroslanguageo00chei_1/?st=gallery)
- **Photo path.** The browser accepts JPEG, PNG and WebP with consent and applies decode, dimension and basic exposure/contrast checks. The visitor declares the hand and any visible features. Optional overlaid points are entirely manual; photo bytes and points stay in the tab. The reading request contains only confirmed descriptors. Reload and removal clear the local image.
- **Recognition blocker.** Workbench has a pinned experimental Qwen3-VL adapter and a license-cleared smoke image. It lacks an independent ground-truth corpus with annotated crease paths, hand orientation and markings, stratified by image conditions, alongside a verified localization and abstention benchmark. The model emits enum suggestions without landmarks. Automatic hand recognition, blur scoring, hand orientation, crease/mark detection and automatic overlays remain unverified and disabled in this consumer path.
- **Source gaps.** Broader outline subtypes, minor markings, several line procedures and combinations remain open. The current scope does not use historic health, longevity, deterministic event or protected-trait claims. A mark shown on a photo adds no interpretation by itself.
- **Media fixture.** The photo is the existing CC0 Wikimedia intake fixture credited to Lezlie Rewatch. Scripted descriptors illustrate the review and reporting flow, with no recognition accuracy claim. [Photo license and credit](https://commons.wikimedia.org/wiki/File:Left_Hand_of_a_Female_Human.png)
- **Audio.** The new 15.5-second loop is a half-second cosine-overlap remaster of the existing FATE ambience, at −20 dBFS RMS. Start, mute and route transitions use volume fades. The only stored audio value is the visitor's explicit mute preference.

## Acceptance fixtures

| Fixture | Acceptance |
|---|---|
| Multi-feature hand | The report covers the matched sections, names the confirmed features and links each chapter back to its exact applicable rules. Native output remains identical to a direct replay. |
| Clear but incomplete evidence | Isolated confirmed features yield bounded chapters. Missing and uncertain observations produce no additional rule match. |
| Contradictory evidence | Report the conflict, suppress the affected interpretation and leave unrelated matches intact. |
| Exact supplement and reversed relationship | Printed Cheiro locators accompany each added combination. A missing prerequisite or unspecified direction yields no supplementary rule. |
| Corrupt / dark / flat image | Browser rejects the file before there is a reading request. Consent, removal, refresh and the outbound payload are checked separately. |
| Recognition release gate | An independent reviewer must label hand orientation, crease paths and visible markings on held-out phone photos and non-palm negatives. Record per-feature precision/recall, missed features, localization error, subgroup/lighting breakdowns and abstention, with no claimed automatic coverage for untested features. Compare recognition to human labels, not a model-generated transcript. Recognition has no passing result in this block. |

Research leads: [Diff-Palm’s annotated principal-line ROIs](https://openaccess.thecvf.com/content/CVPR2025/papers/Jin_Diff-Palm_Realistic_Palmprint_Generation_with_Polynomial_Creases_and_Intra-Class_Variation_Controllable_Diffusion_Models_CVPR_2025_paper.pdf) and the [Tsinghua scanner dataset](https://ivg.au.tsinghua.edu.cn/dataset/THUPALMLAB.php). They were not used as consumer recognition evidence. Product rights, phone-photo domain fit and coverage of mounts and markings still need review.
