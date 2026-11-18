# FATE Asset Pack 01 — original procedural artwork

Use in the Phase 1 Explore entrance. All artwork here was created specifically for this project and contains no third-party stock imagery.

- fate_atmosphere.webp — responsive dark-starfield backdrop (1200x1600)
- fate_orb_core.png — alpha-transparent glass / fog sphere (1200x1200)
- fate_orrery.svg / .png — separately animated golden orbits, transparent (1200x1200)
- fate_sigil.svg / .png — original FATE emblem (512x512)
- preview.jpg — visual composition reference only; not for direct use as UI

Recommended composition: atmosphere as background, orb at center, orrery above orb; apply separate subtly staggered motion. Do NOT animate all layers together. PixiJS or CSS transforms and filters are both acceptable; use restrained glow and parallax. Respect reduced-motion and preserve sharp text as real DOM UI. Reuse the original independent assets, not the preview screenshot.

This is a starter art kit, not the final approved hero. Review on real mobile screens and iterate art direction against target quality.

Original synthesized audio:
- fate_ambient_loop.wav — quiet ethereal ambience, optional sound-on experience
- fate_oracle_select.wav — short selection chime
- fate_card_reveal.wav — card reveal SFX
Music and SFX must be off by default on initial visit, with independently controllable volume and user gesture unlocking playback. Treat these as initial sound prototypes and replace if audio-direction QA calls for more refined production.
