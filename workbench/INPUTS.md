# Testing your own inputs

The pinned local model is installed on this machine. Restart Workbench from PowerShell:

```powershell
cd D:\Future
python -m workbench
```

Open http://127.0.0.1:8000 and refresh any old browser tab.

1. Select **Palmistry**. Upload a clear open-palm photo, choose the photographed hand and dominant hand, and confirm permission.
2. Click **Analyze palm photo**. Review the suggested visible line features. Leave unclear features unknown.
3. Check the review confirmation, then **Run technique**. Inspect results and the local model receipt in Provenance.

The Palmistry flow does not save palm photo bytes. It saves reviewed observations and image/model/prompt hashes with the session. Model memory and operating-system remnants are outside that storage promise. Historical symbolic interpretation remains separate from image observation.

Tarot asks for your question and spread. AI Predictive Modeling accepts consecutive monthly observations, units, source and forecast method. Birth/name operations expose native fields. The other 43 retained techniques now have deterministic, engine-specific input builders: enter the requested observations or data, click **Prepare these inputs**, review the native request, then click **Run technique**. They do not require an LLM. Verified demonstration inputs are loaded only with **Load verified sample**.

Every builder covers the native core scope, not every variation. Historical reference engines return documented source comparisons; journals return recorded observations; simulations return results conditional on your model. A relevant input form does not turn those engines into empirically validated personal predictors. In particular #52, #54, #55, #56 and #58 accept synthetic data only. #53 permits declared independently reviewed archival scalar replay; live sensors and empirical twin certification remain unsupported.

### New dedicated core flows

| ID | Input flow |
|---|---|
| 9 | Describe the region you want to inspect |
| 10 | Inspect a historical schematic label |
| 11 | Choose a historical body-region reference |
| 12 | Choose a documented foot or sole feature |
| 13 | Describe your handwriting observations |
| 14 | Select your symbolic colors and context |
| 15 | Inspect a historical iris-chart label |
| 17 | Ask your oracle-card question |
| 18 | Enter your I Ching question and lines |
| 19 | Ask your rune-casting question |
| 20 | Record your pendulum observation |
| 21 | Record your crystal-gazing session |
| 22 | Record your mirror session |
| 23 | Describe your dream |
| 24 | Record a completed writing session |
| 26 | Frame your reference or reflection question |
| 28 | Record the symbols in your tea cup |
| 29 | Record your coffee-ground symbols |
| 30 | Record a candle observation |
| 31 | Record a water observation |
| 32 | Record atmospheric observations |
| 33 | Enter the four mother figures |
| 34 | Enter your stone layout |
| 35 | Inspect or compare documented bone inscriptions |
| 36 | Choose a passage from the supported corpus |
| 37 | Record the mark on your selected lot |
| 38 | Record your bird observation |
| 39 | Compare a documentary organ-feature account |
| 40 | Enter your measured compass bearing |
| 43 | Review a recorded five-target viewing trial |
| 44 | Review a dream and independently recorded event |
| 45 | Compare two alternatives using your ordered cues |
| 46 | Record your deja reve experience |
| 50 | Simulate your quantum circuit |
| 52 | Simulate a hypothetical threshold network |
| 53 | Replay your scalar digital-twin measurements |
| 54 | Run your cellular-agent grid |
| 55 | Test a synthetic feature classifier |
| 56 | Evaluate your declared causal model |
| 57 | Pool forecasts for your binary question |
| 58 | Simulate a play-credit prediction market |
| 59 | Explore your Lorenz initial conditions |
| 60 | Calculate your branching scenario tree |

CSV fields take one row per observation, with no header unless the label explicitly requests one. Fractions such as `1/2` preserve exact arithmetic where requested. Timestamp fields state whether a time zone or UTC `Z` is required. Unknown observations stay unknown; do not invent missing source records or event times.

#43 and #44 reconstruct **declared completed records**, with actual user-supplied action times, roles and human judgments. They are not prospective or independently blind certification. Target images are normalized and retained in `D:\Future\tmp\workbench-targets`; #44 evidence text is retained in `D:\Future\tmp\workbench-evidence`. These assets are separate from the session database, are not bundled in JSON exports, and are not removed by deleting a session or case. Keep them for replay; deleting them makes dependent records unreplayable. Do not treat database-only exports as complete backups for these two flows.

## Installation elsewhere

On another Windows machine, run `python -m workbench.setup_vision` once. It downloads the checksum-pinned Ollama runtime and Qwen3-VL 4B quantized weights into `%USERPROFILE%\.future-workbench-vision`, outside the repository. Allow several GB of downloads and disk space. The local runtime starts automatically on loopback port 11435. Ordinary deterministic forms and engines do not require the model. First analysis may take longer while the model initializes.

## Configuration boundaries

- Supported software: all 43 new dedicated core builders plus the existing 11 entry paths, native validation, computation and replay. The frozen native support matrices remain authoritative.
- Experimental: automatic palm crease recognition; historical/symbolic interpretations; declared human evidence and retrospective trial reconstruction. These have no newly certified extraction or predictive accuracy.
- Unsupported: raw EEG decoding, medical or character inference from appearance, arbitrary real-world ingestion where a native engine requires synthetic inputs, and certified personal predictive accuracy.
- P1: richer table editors, expanded native variations, prospective multi-user #43/#44 collection, bundled retained assets and reference-aware asset deletion, independently labeled image evaluation.

## Checks

Run `python -m unittest discover -s workbench/tests -v` for backend checks. For the complete Workbench checks with installed Google Chrome, set `$env:FUTURE_TEST_BROWSER='chrome'`, then run `python -m workbench.accept`. Browser tests use synthetic inputs and temporary storage. These are software checks, not prediction-validation evidence.

After installing test dependencies, run `python -m workbench.live_vision_smoke` for an opt-in real local model check. It uses a public CC0 palm fixture and temporary storage; it is separate from deterministic regression tests.

## Optional Gemini assistance (all 54 flows)

Set `GEMINI_API_KEY` in `D:\Future\.env` and restart Workbench. The file is ignored by Git; the key remains on the backend. Optional `GEMINI_MODEL=gemini-2.5-flash` selects a model. The live connection was checked without personal data.

Every Studio flow includes **Get input help from Gemini**. Enter facts and optionally attach images, PDF, text or CSV; confirm cloud permission and click **Prepare with Gemini**. Answer any follow-up questions, inspect the draft and native validation, then confirm review and use the inputs. Execution remains a separate action. The manual forms remain available. Complex source commitments may still require the dedicated builder; the assistant must ask rather than fabricate missing records.

Palmistry also offers **Photo processing provider → Gemini** with separate cloud consent and the existing visible-feature review. Completed saved results offer **Explain this result with Gemini**. Explanations are experimental commentary, separate from native calculations; unrevealed blind runs cannot request cloud explanations. The explanation endpoint reads the saved native output, not a client-substituted result.

Only explicitly submitted content is sent to Google; there is no automatic cloud fallback. API charges, internet access and Google's processing policies apply. AI drafts/explanations appear in the current UI and are not separate persisted study evidence; reviewed native requests are stored with runs. Native values, historical/synthetic scope and unknown observations remain authoritative. Keep API keys out of uploaded documents and exports.
