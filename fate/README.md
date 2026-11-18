# FATE · Block 01 — The Living Oracle

A separate consumer application over the unchanged Future Tarot engine. Explore → intention → progressive Tarot reveal → reading. React 19 / TypeScript / Vite, PixiJS 8, and a stateless FastAPI boundary. Workbench remains an independent application.

## Run

From the repository root (Python 3.12, Node.js 22.12+ or 24):

```powershell
python -m pip install -r fate/requirements.txt
python -m fate
```

Open **http://127.0.0.1:8010**. First launch installs the exact npm lockfile and builds the frontend. Subsequent launches can use `python -m fate --no-build`. `--port` changes the default 8010 port. Native Tarot and all locally bundled assets work without an internet connection after installation; Gemini requires internet access.

For frontend development, run the Python service and `npm --prefix fate/web run dev` in separate terminals. Vite uses port 5174 and proxies the consumer `/api` to port 8010. The production Python service serves the compiled frontend directly. Existing Workbench commands and ports are unchanged.

## The experience

- A living crystal orb uses the supplied independent artwork layers, WebGL refraction and procedural moving mist, rotating near/far celestial orbits, particles, and touch parallax / a subtle touch pulse. Pixi is dynamically imported after the immediately available artwork composition. React renders every reading and control.
- Original FATE celestial card illustrations cover all 78 identities, with distinct Major Arcana emblems, suit pips and court ornament. This is a contemporary celestial edition, **not** historical Waite–Smith artwork. Waite's immutable 1922 text profile supplies meanings independently of these designs.
- One- and three-card seeded readings, optional reversals, optional question, source-derived concise motifs, progressive CSS 3D flips and an immediate-reading path. One native draw happens before any reveal; interactions never redraw or change its output. Failed requests preserve the question and seed; duplicate submissions are blocked.
- The reading separates native compositional reflection, direct historical wording, source locators / rule IDs, reversal cross-references, separate additional accounts and ambiguities. All native fields remain available in the exported JSON, including the exact replay request, full deck and limitations.
- Sound starts off on every visit. A user gesture enables supplied ambience / cues, with independent volumes. Hidden tabs pause audio. Ambient motion can be paused explicitly; reduced-motion settings disable transitions and continuous Pixi rendering. Offscreen / hidden orbs stop their ticker. Static original artwork remains available without WebGL.
- No accounts, analytics, database, automatic saving, storage APIs, Arcade or payments. Export is an explicit native JSON download. Reloading ends the in-memory visit; a direct reading URL cannot restore a prior result.

The frozen application contract is [experience.json](experience.json). It does not expand the native engine's supported scope or change the inventory.

## Optional Gemini

The server reuses the existing server-side `workbench.gemini.generate` REST provider and its ignored root `.env` / environment configuration (`GEMINI_API_KEY`, optional `GEMINI_MODEL`). No credentials reach the frontend. FATE exposes no Workbench endpoints or stores.

Only checking the reading-specific consent box and requesting commentary sends the question, native cards, source meanings and qualifications to Google. Gemini is optional and billed according to the configured provider account. No automatic AI request occurs. Commentary is explicitly experimental and visually separate from the authoritative reading; errors leave that reading intact.

The API signs a draw request for 24 hours and recomputes it server-side before sending anything to the provider. Changed, expired and post-restart receipts are rejected. Output must reference exactly the supplied card IDs and rule IDs, in order, with bounded reflection lengths. These checks establish reference integrity, **not semantic faithfulness or predictive accuracy**. Commentary may still be wrong; native source text remains available. Provider identity / model and the prompt hash are returned separately. No commentary is persisted.

## API boundary

- `GET /api/health`: service / profile and whether Gemini is configured.
- `POST /api/readings`: strict `{spread: "one" | "three", seed, question, reversals}` → full native result and a signed commentary receipt. Questions are trimmed and line breaks become spaces to satisfy the native plain-text context contract. Other control characters remain invalid.
- `POST /api/explain`: `{draw, receipt, cloud_consent: true}` → separate source-referenced commentary.

The default launcher binds only to loopback. Host allowlisting (`FATE_HOSTS`), same-origin checks, a 16 KiB JSON body limit, strict schemas, duplicate-key rejection, security headers, no-store API responses, bounded per-process request buckets and two concurrent provider calls protect this boundary. It accepts no arbitrary engine operation, files or user-supplied native result.

Public deployment is a separate operational step: run the built app behind HTTPS, set the intended host allowlist and trusted proxy settings, and supply provider secrets through the server environment. The included limiter is per process; distributed limits, deployment-specific privacy / retention controls and managed secrets are P1 work before a multi-instance public launch. Do not expose the Workbench server as the consumer API. No public deployment was performed for this block.

## Verification and evidence

```powershell
python -m unittest discover -s fate/tests -v
npm --prefix fate/web run build
npm --prefix fate/web run test:e2e
python -m unittest discover -s tests -q
python -m unittest discover -s workbench/tests -q
python -m fate.verify_inherited
```

Install Chromium once with `npm --prefix fate/web exec playwright install chromium` if Playwright's browser is not already installed. `python -m fate.live_gemini_smoke` is an **explicit live provider call** using only a synthetic developer question; it incurs a provider request. The ordinary test suites never call the live provider.

See [acceptance.json](acceptance.json), [browser-acceptance.json](browser-acceptance.json), [inherited-cli-acceptance.json](inherited-cli-acceptance.json), [workbench-browser-acceptance.json](workbench-browser-acceptance.json), [performance.json](performance.json) and [live-gemini-acceptance.json](live-gemini-acceptance.json). Browser screenshots in [screenshots/](screenshots/) come from the real app, real native engine calls, and Chromium mobile emulation, not mockups. Browser failure / cloud interaction tests use labeled transport test doubles only for those failure / consent paths.

Automated accessibility checks cover Explore, intention, reveal, reading and settings. Keyboard / dialog focus, 320/390/430/768/1440 CSS-pixel layouts, doubled actual text sizes, sound consent, absent WebGL and reduced motion are exercised. These are automated checks, not comprehensive accessibility certification.

## Limits and next work

1. **P1 — physical devices and performance:** Safari / iOS and representative Android GPU, thermal, memory and throttled network checks; actual INP / field CWV. Recorded LCP, CLS, RAF cadence, heap and long tasks are local emulation observations. RAF cadence is not the orb's frame rate; the orb ticker is capped at 45 FPS. Initial Pixi setup can create long tasks. No real-device performance target is certified.
2. **P1 — artwork / sound review:** supplied original pack plus the original celestial vector deck are the shipped visual direction; no licensed historical illustrated deck is included. The pack itself calls its hero and audio a starter kit. Further art / audio approval and bespoke figurative card illustration can refine this foundation.
3. **P1 — interpretation:** additional source-qualified contextual composition and more Gemini semantic evaluation. One successful live synthetic check does not validate explanation quality across 78 cards, personal questions or harmful source language. Historical vocabulary is clearly attributed, never a personal finding.
4. **Later blocks:** Atlas / persistence, account consent, additional oracle families. Celtic/manual consumer flows and other traditions remain out of scope, even where the underlying engine has broader support.

Asset provenance / hashes: [assets.json](assets.json). Rights and dependency notices: [THIRD_PARTY.md](THIRD_PARTY.md), [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt), and the original pack README and font licenses under `web/public/`.
