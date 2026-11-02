# Ephemeris selection — 2026-11-02

| Option | Accuracy / history | Astrology and Python | License / offline |
|---|---|---|---|
| Swiss Ephemeris | High precision; broad historical coverage, depending on files | Python wrapper; many house systems, zodiac and motion flags | AGPL or paid professional license. Offline files/Moshier. Not a product dependency. |
| Skyfield + JPL | High precision numerical JPL kernels; DE440s spans 1849–2150 | Native Python geocentric apparent coordinates and timescales; astrology houses/rules require separate code | MIT library; kernel terms separate. Offline after explicit download. Selected. |
| Astronomy Engine | Approximate analytical models, typically arcminute target; broad modeled dates | Pure Python, positions/events; no full astrology house layer | MIT, no large kernel required. Credible lightweight alternative. |

Sources: [Swiss API/license](https://www.astro.com/swisseph/swephprg.htm), [Skyfield coordinates](https://rhodesmill.org/skyfield/coordinates.html), [Skyfield MIT](https://raw.githubusercontent.com/skyfielders/python-skyfield/master/LICENSE), [Astronomy Engine](https://pypi.org/project/astronomy-engine/), [JPL kernels](https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/).

Selection avoids committing Future to AGPL or paying a professional license. It does not assign a license to Future itself. Preserve third-party notices when distributing. Swiss is used only as a local independent validation oracle. Frozen numerical reference facts and the generator are committed; no Swiss code is vendored or used by the product.

DE440s SHA-256: c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2. Charts are restricted to 1850–2149. A longer-range kernel requires explicit coverage testing. Skyfield built-in timescale data is pinned by package version; UT1 derives from modeled delta T. Pre-standard-time IANA offsets can differ from the actual town's local mean time. Do not interpret historical civil timestamps as guaranteed records of local astronomical time.

Tradition, application, zodiac, houses, rulership and aspect/orb settings are separate dimensions. Current traditions select seven classical versus ten modern bodies; only natal, tropical, traditional rulership, equal/whole-sign houses are enabled. Orbs are explicit project defaults, not attributed to every historical school. Further traditional algorithms remain pending. No tradition is complete.

Independent tests use Swiss Moshier (different planetary model) with 0.01-degree longitude and 0.02-degree angle/cusp tolerances. Astro-Databank Einstein example checks published Sun/Moon only because Ulm LMT differs from IANA Berlin historical time. Source: https://www.astro.com/astro-databank/Einstein%2C_Albert .
