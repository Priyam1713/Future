# FATE · Block 01.5 — Cinematic Polish & Visual Foundation

An isolated consumer application over the unchanged Future Tarot engine: **Explore → Tarot Ritual → Reading**. React / TypeScript / Vite, PixiJS and a stateless FastAPI boundary. Workbench, native calculations, source profiles and the inventory remain independent.

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

Only explicit per-reading consent sends the question, cards, source meanings and qualifications to Google. Commentary remains experimental and separate. The server verifies a signed 24-hour request receipt and recomputes the native result; changed / expired / post-restart receipts are rejected. Exact card and rule references, order and bounded text shape are checked. These checks do **not** guarantee semantic faithfulness or predictive accuracy. Provider failures leave the native result intact. Ordinary tests never call the live provider; the prior Block 01 live synthetic check is retained rather than repeated for a visual-only change.

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

Acceptance: **2,522 native tests, 77 Workbench tests, 16 FATE API / artwork tests, all nine original FATE browser groups plus four polish groups, nine Workbench browser groups, 3,515 CLI cases and 52 independent verifiers**. The artwork tests independently compare identity coverage / numbering to the engine catalog and verify all 156 delivery hashes. Accessibility scans, keyboard / skip focus, retry / export / replay, 320/390/430/768/1440 layouts, doubled text, reduced motion, low-power policy, rapid cleanup and absent WebGL are exercised. Software checks are not empirical Tarot validation or comprehensive accessibility certification.

Real browser screenshots: [Explore mobile](screenshots/01-explore-viewport.png), [Ritual mobile](screenshots/03-reveal-mobile.png), [Reading mobile](screenshots/04-reading-mobile.png), [Explore desktop](screenshots/07-explore-desktop.png), [Ritual desktop](screenshots/11-reveal-desktop.png), [Reading desktop](screenshots/12-reading-desktop.png).

Short unmodified screen recording: [MP4](evidence/orb-and-card-reveal.mp4), [original WebM](evidence/orb-and-card-reveal.webm), [native draw / event receipt](evidence/recording.json). Reproduction scripts are in `web/scripts/`; run them from `fate/web` against a running built FATE server. Performance collection is kept separate from video recording and regression workloads.

The frozen scope is [experience.json](experience.json). Checks and source / build / screenshot hashes are in [acceptance.json](acceptance.json) and adjacent browser / CLI receipts. Asset hashes and rights are in [assets.json](assets.json), [THIRD_PARTY.md](THIRD_PARTY.md) and [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt).
