# Dependency and source notices

Future Core v1 runs from source with separately installed Python packages. No third-party runtime, kernel, textbook or full modern translation is vendored. `knowledge/dependency_audit.json` records installed versions, declared licenses and notice-file hashes; `requirements.txt` pins the complete runtime dependency set used for validation.

Skyfield, jplephem and sgp4 declare MIT; NumPy declares BSD-3-Clause and bundled component licenses; tzdata declares Apache-2.0 (IANA data and its wrapper have separate notices); certifi declares MPL-2.0. Retain upstream license and notice files when distributing dependencies. This record does not replace those files or grant a license to Future.

JPL DE440s is downloaded explicitly from NASA/JPL and checked against its frozen SHA-256. Credit the JPL ephemeris team. The kernel is excluded from Git. Source: [JPL download](https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de440s.bsp); [SSD publication policy](https://ssd.jpl.nasa.gov/faq.html); [NAIF kernel rules](https://naif.jpl.nasa.gov/naif/rules.html). Rules applicable to one distributor are not assumed to cover another. Kernel/binary packaging requires a separate distribution review.

Swiss Ephemeris is an optional local validation oracle, never a product dependency or runtime import. Its AGPL/professional-license conditions are not bypassed by its technical usefulness. Independent numerical fixtures do not include Swiss implementation code.

Modern source material is limited to links, provenance and short original summaries. Public accessibility does not authorize wholesale ingestion, redistribution or copying copyrighted Hand, Arroyo, Shea, Brennan or translated Valens text. No author or data provider endorsement is claimed.
