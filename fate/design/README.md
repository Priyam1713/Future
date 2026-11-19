# FATE visual contract · Block 01.5

The visual foundation separates **engine identity**, **artwork**, **physical presentation**, and **motion**. No illustration or animation chooses a card or supplies a meaning.

## The Archive Edition

Every one of the 78 engine card IDs maps to a verified historical Pamela Colman Smith Pam-A illustration, from one complete Wikimedia Commons image set. No modern recolored deck, mixed edition, generated face or incomplete substitute is used. Source text remains the frozen Waite **1922 text profile**; images are independently attributed **1910 Pam-A** illustrations.

`web/src/artwork/deck-manifest.json` is the lean runtime contract: version, identity, source URL, credit, intrinsic dimensions and 360/720 WebP variants. `artwork-sources.json` retains the per-file Commons metadata, public-domain designation, original SHA1, revision timestamp, downloaded SHA256 and delivery hashes. The fetcher rejects a changed author, date, restriction, license or collection. Delivery derivatives only resize and encode the complete scan: no cropping, recoloring or generative changes.

The registry is complete and checked against the immutable native catalog, including Strength VIII, Justice XI and all court identities. New art must be a **complete, reviewed, versioned collection** before becoming a runtime edition. Individually commissioned previews stay outside live draws; never fill missing cards with a different style. If an asset fails to load, show its real engine name and an explicit availability message rather than substitute another image.

## The shared material system

- Midnight ink, smoky teal glass, subdued indigo depth, warm champagne foil and quiet ivory typography.
- The original FATE observatory back repeats the orb's astrolabe, mist and metal vocabulary. It is one consistent back for the whole Archive Edition, not an invented historical card face.
- Readable captions, sources and controls are DOM text. The frame/bevel, foil sheen, 3D flip and pointer tilt are independent of the image asset. Full historical scans remain visible inside the mat; reversal rotates the artwork while the DOM name remains readable.
- `PhysicalCard` owns bounded pointer feedback. `CardArtwork` resolves identity and delivery variants. Reveal state lives in `useOracle`; touching a card cannot redraw it.

## Orb layers and lifecycle

`orb/shaders.ts` owns the spherical lens, depth-dependent cloud layers, moving internal light, glass absorption, Fresnel rim, specular reflections and touch light. The nebula is an original generated texture, sampled through independently moving distorted depth layers; it is not a pre-rendered orb video. Procedural noise and particles provide additional movement. Far/near celestial rings remain separate scene objects.

`orb/createOrbScene.ts` owns Pixi initialization, resources, events, resize, context recovery and disposal. `orb/policy.ts` owns capability tiers, bounded display-sized buffers and adaptive quality. React's small `Orb` wrapper defers imports until a visible host has painted, applies motion changes even during asynchronous setup, and cancels pending work on navigation. Initial reduced motion skips loading Pixi altogether. Pause, hidden/offscreen state and reduced motion stop the ticker; there is no polling timer.

The initial target is 60 Hz with 1.75 DPR maximum, adjusted to displayed size. Sustained misses reduce to 1.25 DPR / fewer particles, then to a 1 DPR economy tier that still targets 60 Hz. A final 1 DPR / 30 Hz tier bounds weak-device load; low-memory, low-core and data-saving devices start there. Samples record **renderer callback cadence**, resolution and quality, separately from browser RAF. They are not GPU-presentation, thermal, battery or field-performance certification.

`OrbPoster` uses an exact still extracted from this scene. It contains no React UI and is the same artifact for initial paint, reduced motion, context loss and absent WebGL.

## Reproduce assets and evidence

```powershell
python -m pip install -r fate/artwork-requirements.txt
python -m fate.fetch_deck
python -m fate.build_visual_assets
# Start the built FATE server, then from fate/web:
node scripts/capture-poster.mjs
node scripts/capture-evidence.mjs
```

The deck fetcher is a deliberate network acquisition tool, not part of startup/build. Normal operation uses checked-in delivery images offline. Keep versioned files immutable after approval. A refresh should receive a new directory / manifest version and repeat rights, identity and visual review.

Original generated back and nebula PNGs are in `sources/`; exact prompts, generation method and derivative paths are in `generated-artwork.json`. The renderer-derived poster PNG is also retained. PNG→WebP is a delivery conversion, not a second creative generation. Built-in image generation was used; no API-key script or external artist's modern deck was substituted.

The evidence script records actual browser frames, an actual native draw and real taps. The MP4 is a silent H.264 delivery conversion of the original WebM. No AI result, composed soundtrack, artificial touch effect or edited UI is added to the recording.
# Block 02 material layers

`block02-artwork.json` records the exact built-in imagegen prompts and retained source PNGs for `number-dial-v1` and `gallery-hall-v1`. They are original project assets, not stock icons or interface mockups. `build_visual_assets.py` performs delivery resizing/encoding only. The brass ring preserves generated transparency, including its open center. Live glass, mist, light, geometry, numbers, pointer depth and controls are independent runtime layers in `web/src/numerology/NumberDial.tsx` and `gallery.css`. The environment illustration contains no baked UI; its collection copy and discovery controls are semantic HTML. Existing Tarot image identities and artwork provenance remain unchanged.
# Block 03 living Codex

`block03-artwork.json` records the original built-in imagegen cover prompt and retained `sources/codex-cover-v1.png`. Responsive WebP conversion is delivery-only. The cover contains no title, page contents, counts or controls. Its runtime title/count, cloth binding, moving light, cover hinge, paper surfaces, source illustrations, chapter reader and real turning leaf are separate layers. Chapters come only from completed readings explicitly saved by the visitor. Paper scroll stays within bounded folios; chapter controls remain on the binding. Reduced motion removes the turn and light while retaining all chapter actions. The actual live interaction is recorded separately from settled stills. No stock book mockup or baked-image interface is used.

## Block 04 · Astral Observatory

The supplied Western Observatory Art 01 is an environmental illustration, not a chart. Source PNG, exact original prompt and package README are retained; the manifest records all delivered WebP SHA-256 values and the original archive hash. The 4:5 mobile crop preserves the armillary; landscape variants preserve negative space. No new generated raster art is needed for this milestone. Live native geometry, glyphs, twelve houses, aspect paths, physical rim, selected light and all readable labels/controls are separate React/SVG layers. Pointer parallax and engraved-ring/material-light animations never change the calculated chart. The small ritual instrument expands into a full touch-explorable reading instrument. Codex and comparison use the same saved geometry, with no zodiac template or invented sky.
