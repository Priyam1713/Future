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

Workbench does not save photo bytes. It saves reviewed observations and image/model/prompt hashes with the session. Model memory and operating-system remnants are outside that storage promise. Historical symbolic interpretation remains separate from image observation.

Tarot directly asks for your question and spread. AI Predictive Modeling accepts consecutive monthly observations, units, source and forecast method. Birth/name operations expose native input fields. Other methods ask relevant source-derived questions and offer experimental local transcription into native inputs. Demonstration data requires an explicit **Load verified sample** or **Reset to sample** action.

## Installation elsewhere

On another Windows machine, run `python -m workbench.setup_vision` once. It downloads the checksum-pinned Ollama runtime and Qwen3-VL 4B quantized weights into `%USERPROFILE%\.future-workbench-vision`, outside the repository. Allow several GB of downloads and disk space. The local runtime starts automatically on loopback port 11435. Ordinary deterministic forms and engines do not require the model. First analysis may take longer while the model initializes.

## Configuration boundaries

- Supported software workflow: photo selection and permission; strict image/enum validation; signed human-review receipt; unchanged native palm execution; direct tarot and monthly-series builders; source-derived questions covering all 54 retained techniques.
- Experimental: automatic visible-crease recognition and general answer-to-native-request transcription. Review every generated field. Neither has an independently measured extraction accuracy. Ledger commitments, provenance histories and complex simulations can still require an expert-built native request. All 54 methods are not claimed to have complete bespoke real-data builders.
- Unsupported: medical or character inference from appearance; arbitrary real-world ingestion where the underlying engine only supports bounded simulations; certified personal predictive accuracy.
- P1: more deterministic native builders, commitment-aware ledger construction, richer feature guidance and independently labeled image evaluation. Existing engine support matrices remain authoritative.

The local assistant may ask for missing information or produce a draft rejected by native validation. It must not supply missing observations or outcomes. Review is mandatory before its draft becomes an executable input.

## Checks

Run `python -m unittest discover -s workbench/tests -v` for backend checks. For the complete Workbench checks with installed Google Chrome, set `$env:FUTURE_TEST_BROWSER='chrome'`, then run `python -m workbench.accept`. Browser tests use synthetic inputs and temporary storage. These are software checks, not prediction-validation evidence.

After installing test dependencies, run `python -m workbench.live_vision_smoke` for an opt-in real local model check. It uses a public CC0 palm fixture and temporary storage; it is separate from deterministic regression tests.
