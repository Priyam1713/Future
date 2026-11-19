# FATE · Block 03 — The Living Codex

An isolated consumer application over the unchanged Future Tarot and Numerology engines: **Explore → a distinct oracle ritual → source-grounded reading → explicitly saved local chapter**. React / TypeScript / Vite, the signature PixiJS orb and a stateless FastAPI boundary. Workbench, native calculations, source profiles and the master inventory remain independent.

## Block 03: My Fate

**My Fate** is an interactive celestial Codex. Its original illustrated cover, runtime title/count, moving light, binding, paper, chapter contents and turning leaf are separate layers. Opening the cover reveals actual saved chapters. Previous/next, swipe, keyboard arrows and the contents index change the real source chapter; there are no simulated page counts or invented entries. Bounded folios scroll within the paper and keep chapter controls on the binding. Reduced motion, shared settings, offscreen/hidden pause and low-capability light reduction are respected. Motion controls live in settings during Numerology’s ritual. Explore / 54 techniques / My Fate navigation provides direct access to the full retained Gallery.

**Explicit, minimal persistence:** Save to this device is the only reading-save action. The `fate.codex.v1` localStorage document has `schemaVersion: 1` and at most 50 allowlisted chapters (64 KiB character limit). Each chapter has a random UUID, UTC save time, frozen source-reference version and either card IDs/orientations/spread or Expression/Personal Year/Life Path numeric results. Names, birth/target dates, questions, letter tokens, arithmetic traces, replay seeds and Gemini commentary are never included in a Codex record. No free-text label or hashed personal input is stored. Opening the app reads existing records without creating or migrating them. Unknown versions, references, fields, invalid values, prototype-property card IDs and malformed records fail closed without overwrite. Failed/quota-blocked writes do not claim a save. Deleting the final chapter removes only the Codex key. A separate confirmation covers individual or all-Codex deletion; unrelated browser data and previously downloaded exports remain untouched.

**Reopening and source accuracy:** `python -m fate.build_codex` freezes `web/src/codex/reference-v1.json` from the existing source catalogs. The tool refuses to overwrite v1 with changed content. Saved chapters recover exact meanings/rule identities from their archived edition, without needing private inputs, API calls, Gemini or a new calculation. Source wording, references, alternatives and accessible limits remain in depth; shared editorial glosses/conclusions are distinct from native truth. Full native export continues to include the original calculation/replay context when explicitly downloaded. Codex export instead contains minimal chapters with their source references. There is no import UI in this block.

**Compare Perspectives:** choose two saved chapters. `fate-source-language-v1` uses a small explicit editorial vocabulary to group words already present in the cited Tarot glosses and the two direct Numerology summaries. It shows corresponding language and separate emphases, without a combined reading, agreement/confidence score, cross-engine probability, new meaning or prediction. Passages containing source alternatives (`OR`) are displayed in full and excluded from automatic matching. An identical pattern is labeled as repetition, not independent corroboration. Absent vocabulary matches do not establish disagreement. Comparison selections are not persisted and no LLM is involved.

**Privacy limits:** local records remain personal and unencrypted. Other people/software using the same browser profile can read, edit or erase them. Clearing site data, private browsing, quota or browser policy can remove/block them. The app and its artwork must be available to reopen them; normal resource requests still reach the host, while chapter records are not uploaded. There is no account, sync or automatic backup. Export before changing device/browser/site address. Storage events refresh other tabs and mutations read the latest document, but simultaneous tab writes can still conflict. User exports are the independent backup.

**Evidence:** 15 Node tests exercise storage/privacy/export/comparison invariants; three additional Python tests verify the frozen source edition and all 156 Tarot rule identities. Six new browser groups cover real native saves, private-field and Gemini exclusion, refresh/export/reopen, deletion, quota/unknown versions, cross-tab updates, actual book motion, keyboard/reduced-motion behavior, responsive geometry, accessibility and direct Gallery navigation. Original browser coverage is preserved; the Numerology pause check now uses settings, matching the relocated control. `evidence/codex-privacy.json`, `codex-recording.json`, `codex-performance.json` and the adjacent media bind the behavior to actual engine results and measured execution conditions. Original cover PNG and exact prompt: `design/block03-artwork.json`.

Run `npm --prefix fate/web run test:codex` for the Node invariants. Against a running built server, run `node scripts/capture-codex.mjs` from `fate/web`, then `node scripts/measure-codex.mjs` separately. The 50-chapter performance fixtures repeat actual native snapshots with test UUIDs and are explicitly labeled as load fixtures, not additional claimed native readings. RAF cadence measures scheduling, not hardware-presented compositor FPS or field INP. Physical iOS/Android, GPU/battery/thermal and simultaneous multi-tab write acceptance remain P1.

## Block 02 scope and architecture

- **Gallery:** two open rooms, six editorial collections, all 54 retained inventory IDs. Search names and real variations; expand each tradition for its evidence limits and rank-one reference. Four discredited assessment traditions (#9, #10, #13, #15) are historical references, with no assessment action. All other unopened consumer experiences are upcoming, without launch dates. Consumer availability does not imply a change to native engine readiness. Excluded IDs remain absent. `python -m fate.build_gallery` reproducibly projects the master inventory into `web/src/gallery/inventory.json`; tests require an exact match and source hash.
- **Numerology:** `POST /api/numerology` validates a bounded request and calls `future.numerology.readings(calculate(...))` directly. Full birth/current name basis, both dates and per-occurrence Y roles are explicit. No silent transliteration. Three seals reveal a completed result: Expression, Personal Year, then the birth-date framework. Skip goes directly to the same reading. Direct interpretations cover Expression and Personal Year only; other values and traces are expandable calculated context. Native JSON export is exact. The supported/experimental/unsupported matrix is frozen in `experience.json`, consistent with `knowledge/numerology_core_v1.json`.
- **Separate personalities:** Tarot retains physical illustrated cards and the orb. Numerology uses an original patinated brass instrument with layered teal glass, moving mist/caustics, counter-rotating geometry, numerical constellations, depth, light and touch/keyboard response. Its compositor layers allocate no extra WebGL context and run no per-frame React or JS animation loop. Offscreen/hidden/pause/reduced-motion stop continuous animation. Low-capability policy removes mist and quantizes ongoing transforms to 30 steps/second; this is not a hardware presentation guarantee.
- **Contracts:** `web/src/experiences/contracts.ts` defines available-room identity, entry metadata, endpoint/privacy contract and the typed native Numerology envelope. Native result, presentation, source depth, artwork and optional AI remain distinct. Tarot's concise primary prompts are editorial source-gloss transformations; immutable original motifs, engine composition, historical wording and alternatives remain available in depth and export. No new numerical rules or source meanings enter either engine.
- **Continuity:** completed-reading markers contain technique IDs in React memory. Return/next-room actions connect the two rooms. Markers reset on reload; no account, database, browser storage or analytics. Numerology input/results are discarded on leaving its component. Tarot retains its existing in-memory journey for this visit. Nothing is automatically persisted.
- **Optional Gemini:** Numerology's separate `/api/numerology/explain` requires literal boolean consent and a valid signed native-request receipt, recomputes the result, then sends only its two direct theme/source rows to the provider. Name and dates are omitted from the provider prompt. Scope/source identity, order, row count and length are checked; semantic faithfulness remains experimental. Native output is never replaced. Tarot's existing consent/receipt flow is preserved. API bodies/results remain `no-store` and are never written to disk by the application.
- **Art:** original brass and observatory source PNGs, exact built-in imagegen prompts and delivery paths are in `design/block02-artwork.json`. All UI text, numbers, labels, controls and geometry remain runtime layers. `python -m fate.build_visual_assets` creates responsive WebP deliveries; the complete historical Tarot edition remains unchanged.

## Block 02 evidence

`web/e2e/gallery.spec.ts` adds five browser groups to the 13 preserved FATE groups. Python boundary tests cover independent hand sums, exact native parity, strict inputs/Y roles, current names and absent vowels, signed consent/privacy, provider mismatch and the exact retained inventory projection. `evidence/numerology-engine.json` contains an actual browser result for the public historical example Ada Lovelace, not a mock visitor identity. `evidence/numerology-recording.json` binds its real engine result to the silent browser recording; only initial form setup is trimmed. No UI is composited into the recording.

Run `node scripts/capture-numerology.mjs` and `node scripts/measure-numerology.mjs` from `fate/web` against a running built server. Measurements record route readiness, native response timing, RAF scheduling, CLS, long tasks, resource delivery and heap under explicit profiles. RAF cadence is not compositor presentation FPS or field INP. Orb measurements remain separate in `evidence/host-performance.json`. Screenshots are real mobile/desktop browser captures. Physical iOS/Android, native date-picker behavior, GPU/battery/thermal acceptance and public deployment remain P1.

## Run

From the repository root, with Python 3.12 and Node.js 22.12+ or 24:

```powershell
python -m pip install -r fate/requirements.txt
python -m fate
```

Open **http://127.0.0.1:8010**. The first launch installs the exact npm lockfile and builds the frontend. Use `python -m fate --no-build` for later launches, or `--port` to change the default. Once installed, native readings and all bundled artwork work offline; Gemini is optional and requires internet access.

For development, run the Python service and `npm --prefix fate/web run dev` in separate terminals. Vite listens on 5174 and proxies `/api` to 8010. Production serves the compiled frontend with response compression. Workbench commands and ports are unchanged.

## The visual foundation

- **Living glass:** independently moving illustrated nebula layers, spherical refraction, procedural fog, depth/parallax, moving internal illumination, glass absorption, Fresnel rim lighting, specular reflections, near/far rings and restrained particles. A real touch light moves beneath the surface. This is a live Pixi scene, not a video or a baked image of the interface.
- **Coherent collectible cards:** all 78 identities now use one verified historical Pamela Colman Smith **Pam-A Archive Edition**, framed with a consistent mat, metallic bevel, subtle foil and tactile depth. An original illustrated FATE observatory back connects the cards to the orb's material language. No mixture of programmatic emblems, sample faces or unrelated placeholder art remains in live draws.
- **Reusable artwork architecture:** versioned identity registry, intrinsic dimensions, responsive WebP variants, credits, source URLs and immutable hashes. Image delivery, the frame, DOM caption, reversal pose, physical tilt and flip state are separate. A fully bespoke FATE figurative deck can replace the edition coherently after complete artwork review; incomplete previews are not inserted into readings.
- **Cinematic journey:** restrained route transitions, consistent focus management, a reachable mobile entrance action, weighted card turns, bounded pointer tilt, more readable interpretation typography and quieter opt-in sound. Reduced motion and explicit pause override the visual effects.
- **Small modules:** the app shell, three screens, intention form, reveal, reading details, Gemini commentary, settings and physical card are separate modules. Oracle state / cancellation remain in a hook. Shader, rendering policy, scene lifecycle and static poster are separate from React UI.

The full art / animation contract, replacement policy and asset build commands are in [design/README.md](design/README.md). Exact generation prompts, original PNGs and delivery recipes are retained under `design/`. The complete historical-image audit is [artwork-sources.json](artwork-sources.json).

## Preserved reading behavior

One- and three-card readings use the real immutable `future.tarot.read` engine, with an explicit seeded draw / reversal policy and optional question. The draw finishes before any card turn. Animations never select cards, change results, or wait to fabricate suspense. An immediate-result path remains available. Failed requests preserve the question and seed; rapid taps cannot submit duplicate draws.

The reading retains concise source-derived motifs, native compositional reflection, direct historical wording, source locators / rules, reversal references, separate additional accounts, ambiguities and limitations. JSON export includes the complete native result and replay request / full deck. Illustrations are independently attributed 1910 artwork; they do not change the **Waite 1922 text profile**. Source quotations are historical doctrine, never a diagnosis or certain forecast.

Nothing is saved automatically: no account, database, localStorage, analytics or reading sync. Reload ends the in-memory visit. Export is explicit. No new engines, Atlas, accounts, monetization or Arcade are included.

## Motion, performance and sound

The immediate poster is an exact still extracted from the actual orb renderer, with no React text or controls. It also serves reduced-motion, absent-WebGL and context-loss states. Pixi is imported only after a visible host has painted; initial reduced motion does not load it. Pending setup is cancelled on navigation, and asynchronous setup reapplies the latest pause preference. Event-driven visibility / resize / motion handling replaces polling. Offscreen, hidden, paused and reduced-motion scenes stop their ticker.

Rendering starts with a **60 Hz target**, allocating pixels for displayed size rather than a fixed oversized framebuffer. Capability hints can select low-power mode immediately. Sustained missed budgets reduce DPR / particles, then select a simpler 1 DPR economy tier that retains the 60 Hz target, and finally a **30 Hz low-power tier**. This is adaptation, not a promise of 60 FPS on every device. Render-callback timings, quality and buffer size are measured separately from browser RAF cadence.

Sound is off on every new visit. A user gesture enables the supplied ambience and cues, with independent volume controls and quieter defaults. Hidden tabs pause audio. The delivered recording is silent; it does not add a composed soundtrack to imply native audio capture.

See [performance.json](performance.json), [renderer observations](evidence/render-performance.json) and [host / throttled profiles](evidence/host-performance.json). These are local Chromium observations with explicit driver / emulation conditions. Physical iOS / Android, thermal / battery behavior, real-device GPU presentation, field Core Web Vitals and actual INP certification remain P1. Synthetic interaction durations are not field INP.

## Optional Gemini and API

Gemini behavior is unchanged. The existing server-side `workbench.gemini.generate` provider reads the ignored root `.env` or environment (`GEMINI_API_KEY`, optional `GEMINI_MODEL`). No credential reaches the browser, and no Workbench route or store is exposed.

Only explicit per-reading consent sends the question, cards, source meanings and qualifications to Google. Commentary remains experimental and separate. The server verifies a signed 24-hour request receipt and recomputes the native result; changed / expired / post-restart receipts are rejected. Exact card and rule references, order and bounded text shape are checked. These checks do **not** guarantee semantic faithfulness or predictive accuracy. Provider failures leave the native result intact. Ordinary tests never call the live provider; the prior Block 01 Tarot live synthetic check is retained. The new Numerology route has provider/reference/privacy and browser-consent tests; no new live-provider quality claim is made.

- `GET /api/health`: status, text profile and whether Gemini is configured.
- `POST /api/readings`: strict `{spread: "one" | "three", seed, question, reversals}` → full native result and commentary receipt. Questions are trimmed, with line breaks converted to spaces for the existing plain-text context contract.
- `POST /api/explain`: `{draw, receipt, cloud_consent: true}` → separate source-referenced commentary.

The launcher binds only to loopback. Host allowlisting (`FATE_HOSTS`), same-origin checks, a 16 KiB JSON limit, strict schemas, duplicate-key rejection, security headers, no-store API responses, bounded per-process request limits and two concurrent provider calls remain in place. No public deployment was performed. HTTPS / trusted-proxy setup, distributed limits and operational privacy / retention controls remain deployment work; do not expose Workbench as the consumer service.

## Verify and inspect

```powershell
python -m pip install -r fate/artwork-requirements.txt
python -m unittest discover -s fate/tests -v
npm --prefix fate/web run build
npm --prefix fate/web run test:e2e
python -m unittest discover -s tests -q
python -m unittest discover -s workbench/tests -q
python -m fate.verify_inherited
```

If needed, install Playwright's Chromium once with `npm --prefix fate/web exec playwright install chromium`. Asset tools use the existing Pillow foundation separately from the application runtime. Native Tarot still introduces no runtime arithmetic / LLM dependency.

Acceptance gate: **2,522 native tests, 77 Workbench tests, 24 FATE API / artwork / Gallery / source-reference tests plus 15 Codex Node tests, all nine original FATE browser groups plus four polish, five Gallery/Numerology and six Codex groups, nine Workbench browser groups, 3,515 CLI cases and 52 independent verifiers**. The artwork tests independently compare identity coverage / numbering to the engine catalog and verify all 156 delivery hashes. Accessibility scans, keyboard / skip focus, retry / export / replay, 320/390/430/768/1440 layouts, doubled text, reduced motion, low-power policy, rapid cleanup and absent WebGL are exercised. Software checks are not empirical symbolic prediction validation or comprehensive accessibility certification.

Real browser screenshots: [Gallery mobile](screenshots/20-gallery-mobile.png), [Gallery desktop](screenshots/24-gallery-desktop.png), [Numerology mobile ritual](screenshots/29-numerology-ritual-viewport-mobile.png), [Numerology desktop](screenshots/25-numerology-input-desktop.png), [Numerology reading](screenshots/23-numerology-reading-mobile.png), [Tarot reading mobile](screenshots/04-reading-mobile.png), [Tarot reading desktop](screenshots/12-reading-desktop.png).

Block 02 recording: [Numerology ritual MP4](evidence/numerology-ritual.mp4), [original browser WebM including setup](evidence/numerology-ritual-source.webm), [native calculation / event receipt](evidence/numerology-recording.json). [Numerology scheduling/interaction measurements](evidence/numerology-performance.json) and [actual native engine evidence](evidence/numerology-engine.json) accompany it.

Short unmodified screen recording: [MP4](evidence/orb-and-card-reveal.mp4), [original WebM](evidence/orb-and-card-reveal.webm), [native draw / event receipt](evidence/recording.json). Reproduction scripts are in `web/scripts/`; run them from `fate/web` against a running built FATE server. Performance collection is kept separate from video recording and regression workloads.

The frozen scope is [experience.json](experience.json). Checks and source / build / screenshot hashes are in [acceptance.json](acceptance.json) and adjacent browser / CLI receipts. Asset hashes and rights are in [assets.json](assets.json), [THIRD_PARTY.md](THIRD_PARTY.md) and [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt).
