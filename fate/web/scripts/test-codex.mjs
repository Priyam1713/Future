import { build } from "esbuild";
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";
process.chdir(fileURLToPath(new URL("../", import.meta.url)));
await build({
  entryPoints: [
    "src/codex/records.ts",
    "src/codex/reference.ts",
    "src/codex/compare.ts",
    "src/codex/projectNarrative.ts",
    "src/numerology/personalCode.ts",
    "src/astrology/contracts.ts",
    "src/astrology/geometry.ts",
    "src/astrology/source.ts",
    "src/turning/snapshot.ts",
    "src/turning/validation.ts",
  ],
  outdir: "../../tmp/codex-tests",
  entryNames: "[name]",
  outExtension: { ".js": ".mjs" },
  bundle: true,
  platform: "node",
  format: "esm",
  logLevel: "silent",
});
const r = await import(
  pathToFileURL(resolve("../../tmp/codex-tests/records.mjs"))
);
const ref = await import(
  pathToFileURL(resolve("../../tmp/codex-tests/reference.mjs"))
);
const compare = await import(
  pathToFileURL(resolve("../../tmp/codex-tests/compare.mjs"))
);
const { baziNarrative } = await import(
  pathToFileURL(resolve("../../tmp/codex-tests/projectNarrative.mjs"))
);
const { personalCode } = await import(pathToFileURL(resolve("../../tmp/codex-tests/personalCode.mjs")));
class Memory {
  data = new Map();
  writes = 0;
  getItem(k) {
    return this.data.get(k) ?? null;
  }
  setItem(k, v) {
    this.writes++;
    this.data.set(k, v);
  }
  removeItem(k) {
    this.writes++;
    this.data.delete(k);
  }
}
const tarot = {
  oracle: 16,
  profile: "waite-1922-text-v1",
  spread: "one",
  cards: [{ id: "wands-ace", orientation: "upright" }],
};
const number = {
  oracle: 4,
  profile: "decoz-component-reduction",
  expression: 1,
  personalYear: 3,
  lifePath: 8,
};
const chapter = (snapshot = tarot) => ({
  id: crypto.randomUUID(),
  savedAt: "2026-11-19T02:00:00.000Z",
  reference: r.REFERENCE,
  snapshot: structuredClone(snapshot),
});
test("opening an empty Codex performs no writes", () => {
  const s = new Memory();
  assert.deepEqual(r.readDocument(s), { schemaVersion: 1, chapters: [] });
  assert.equal(s.writes, 0);
});
test("Tarot projection excludes questions, composition, replay and commentary even when populated", () => {
  const native = JSON.parse(
    readFileSync("../engine-browser-evidence.json"),
  ).result;
  native.question = "PRIVATE_QUESTION";
  native.replay.seed = "PRIVATE_SEED";
  native.readings.forEach((row) => {
    row.composition.reflection = "PRIVATE_QUESTION";
    row.card.secret = "PRIVATE_NAME";
  });
  native.gemini = "PRIVATE_COMMENTARY";
  const projected = r.tarotSnapshot(native);
  assert(r.validSnapshot(projected));
  assert(!JSON.stringify(projected).includes("PRIVATE_"));
  assert.deepEqual(Object.keys(projected).sort(), [
    "cards",
    "oracle",
    "profile",
    "spread",
  ]);
});
test("Numerology projection excludes names, dates, letter tokens and arithmetic traces", () => {
  const native = JSON.parse(
    readFileSync("../evidence/numerology-engine.json"),
  ).result;
  native.name.original = "PRIVATE_NAME";
  native.birth = "PRIVATE_BIRTH";
  native.target = "PRIVATE_TARGET";
  native.expression.steps = ["PRIVATE_TRACE"];
  native.commentary = "PRIVATE_AI";
  const projected = r.numberSnapshot(native);
  assert.deepEqual(projected, {
    oracle: 4,
    profile: "decoz-component-reduction",
    expression: 9,
    personalYear: 5,
    lifePath: 1,
  });
  assert(!JSON.stringify(projected).includes("PRIVATE_"));
});
test("explicit save persists a versioned chapter and duplicate taps keep one chapter", () => {
  const s = new Memory(),
    c = chapter();
  r.saveChapter(s, c);
  r.saveChapter(s, c);
  assert.deepEqual(r.readDocument(s).chapters, [c]);
  assert.equal(s.writes, 1);
});
test("unknown versions and malformed records are retained byte-for-byte", () => {
  for (const raw of [
    "not json",
    JSON.stringify({ schemaVersion: 3, chapters: [] }),
    JSON.stringify({ schemaVersion: 1, chapters: [{ name: "PRIVATE" }] }),
  ]) {
    const s = new Memory();
    s.data.set(r.STORAGE_KEY, raw);
    assert.throws(() => r.saveChapter(s, chapter()));
    assert.equal(s.data.get(r.STORAGE_KEY), raw);
    assert.equal(s.writes, 0);
  }
});
test("unknown keys and private fields are rejected at every persisted level", () => {
  for (const mutate of [
    (d) => (d.name = "PRIVATE"),
    (d) => (d.chapters[0].question = "PRIVATE"),
    (d) => (d.chapters[0].snapshot.birth = "PRIVATE"),
    (d) => (d.chapters[0].snapshot.cards[0].commentary = "PRIVATE"),
  ]) {
    const d = { schemaVersion: 1, chapters: [chapter()] };
    mutate(d);
    assert.throws(() => r.parseDocument(JSON.stringify(d)));
  }
});
test("invalid identities, counts, duplicate cards, orientations, profiles and values fail closed", () => {
  const bad = [
    { ...tarot, profile: "other" },
    { ...tarot, cards: [{ id: "made-up", orientation: "upright" }] },
    { ...tarot, cards: [{ id: "__proto__", orientation: "upright" }] },
    { ...tarot, cards: [{ id: "toString", orientation: "upright" }] },
    { ...tarot, cards: [{ id: "wands-ace", orientation: "sideways" }] },
    {
      ...tarot,
      spread: "three",
      cards: [tarot.cards[0], tarot.cards[0], tarot.cards[0]],
    },
    { ...number, expression: 10 },
    { ...number, lifePath: null },
    { ...number, personalYear: 11 },
    { ...number, expression: true },
  ];
  for (const snapshot of bad) assert.equal(r.validSnapshot(snapshot), false);
});
test("master core numbers are retained and annual cycles stay single-digit", () => {
  assert(
    r.validSnapshot({
      ...number,
      expression: 33,
      lifePath: 22,
      personalYear: 9,
    }),
  );
  assert(!r.validSnapshot({ ...number, personalYear: 22 }));
});
test("quota and disabled storage never return a fabricated saved state", () => {
  const s = new Memory(),
    first = chapter();
  r.saveChapter(s, first);
  const before = s.getItem(r.STORAGE_KEY);
  s.setItem = () => {
    throw new DOMException("Quota", "QuotaExceededError");
  };
  assert.throws(() => r.saveChapter(s, chapter(number)));
  assert.equal(s.getItem(r.STORAGE_KEY), before);
  assert.throws(() =>
    r.readDocument({
      getItem() {
        throw new Error("blocked");
      },
    }),
  );
});
test("save reads the latest document and preserves another tab’s chapter", () => {
  const s = new Memory(),
    a = chapter(),
    b = chapter(number);
  r.saveChapter(s, a);
  const stale = r.readDocument(s);
  r.saveChapter(s, b);
  r.saveChapter(s, chapter());
  assert.equal(stale.chapters.length, 1);
  assert.equal(r.readDocument(s).chapters.length, 3);
});
test("the bounded collection rejects chapter 51 and leaves chapter 50 intact", () => {
  const s = new Memory();
  for (let i = 0; i < 50; i++) r.saveChapter(s, chapter());
  const raw = s.getItem(r.STORAGE_KEY);
  assert.throws(() => r.saveChapter(s, chapter()), /50 chapters/);
  assert.equal(s.getItem(r.STORAGE_KEY), raw);
});
test("delete touches only the Codex key and removes its final record", () => {
  const s = new Memory(),
    a = chapter(),
    b = chapter(number);
  s.data.set("unrelated", "keep");
  r.saveChapter(s, a);
  r.saveChapter(s, b);
  r.deleteChapter(s, a.id);
  assert.deepEqual(r.readDocument(s).chapters, [b]);
  r.deleteChapter(s, b.id);
  assert.equal(s.getItem(r.STORAGE_KEY), null);
  assert.equal(s.getItem("unrelated"), "keep");
});
test("export recovers exact frozen source references without original inputs", () => {
  const c = chapter(number),
    output = ref.exportChapters([c]);
  assert.equal(
    output.chapters[0].source_readings[0].quote,
    "Initiative and autonomy.",
  );
  assert.equal(
    output.chapters[0].source_readings[1].quote,
    "Expression and creative growth.",
  );
  assert.deepEqual(output.chapters[0].snapshot, number);
  assert(!Object.keys(output.chapters[0]).includes("name"));
});
test("comparison offers cited lexical echoes and does not assign scores or use Life Path meanings", () => {
  const result = compare.compareChapters(chapter(tarot), chapter(number));
  assert(result.echoes.some((g) => g.label === "Beginnings & initiative"));
  assert(result.echoes.some((g) => g.label === "Creativity & expression"));
  assert(!result.echoes.some((g) => g.label === "Work & resources"));
  assert(
    result.echoes.every(
      (g) =>
        g.left.every((e) => e.sourceId && e.quote) &&
        g.right.every((e) => e.sourceId && e.quote),
    ),
  );
  assert(!("score" in result));
  assert(!("probability" in result));
});
test("source alternatives are retained and excluded from automatic matching", () => {
  const star = {
    ...tarot,
    cards: [{ id: "major-17", orientation: "upright" }],
  };
  const result = compare.compareChapters(chapter(star), chapter(number));
  assert.equal(result.alternatives.length, 1);
  assert(result.alternatives[0].quote.includes(" OR "));
  assert.equal(result.echoes.length, 0);
  assert(compare.compareChapters(chapter(number), chapter(number)).samePattern);
});

const astro = await import(
  pathToFileURL(resolve("../../tmp/codex-tests/contracts.mjs"))
);
const sources = await import(
  pathToFileURL(resolve("../../tmp/codex-tests/source.mjs"))
);
const geometry = await import(
  pathToFileURL(resolve("../../tmp/codex-tests/geometry.mjs"))
);
const nativeWestern = JSON.parse(
  readFileSync("../evidence/western-engine.json", "utf8"),
).native;
test("Western snapshots preserve exact geometry while excluding all raw birth and provider fields", () => {
  const s = astro.westernSnapshot({
    ...nativeWestern,
    gemini: "PRIVATE_SENTINEL",
  });
  assert(r.validSnapshot(s));
  const c = r.chapterFor(nativeWestern, s);
  assert(r.validChapter(c));
  assert.equal(c.reference, "fate-western-reference-v1");
  const g = astro.snapshotGeometry(s);
  assert.deepEqual(g.angles, nativeWestern.angles);
  assert.deepEqual(g.house_cusps, nativeWestern.house_cusps);
  assert.deepEqual(g.aspects, nativeWestern.aspects);
  for (const n of astro.BODY_NAMES)
    assert.deepEqual(g.planets[n], {
      longitude: nativeWestern.planets[n].longitude,
      retrograde: nativeWestern.planets[n].retrograde,
      house: nativeWestern.planets[n].house,
    });
  const encoded = JSON.stringify(c);
  for (const v of [
    "local",
    "utc",
    "birth",
    "latitude",
    "longitude",
    "zone",
    "receipt",
    "gemini",
    "PRIVATE_SENTINEL",
  ])
    assert(!encoded.includes('"' + v + '"'));
  const store = new Memory();
  assert.equal(store.writes, 0);
  r.saveChapter(store, c);
  assert.deepEqual(r.readDocument(store).chapters, [c]);
});
test("Western archived source components equal native composition and cannot leak into old chapter editions", () => {
  const s = astro.westernSnapshot(nativeWestern);
  const rows = sources.sourcePlacements(astro.snapshotGeometry(s));
  for (const row of rows)
    assert.deepEqual(
      row.components,
      nativeWestern.reading.placements.find((p) => p.planet === row.planet)
        .components,
    );
  assert.deepEqual(rows, nativeWestern.reading.placements);
  const c = r.chapterFor(nativeWestern, s);
  const exported = ref.exportChapters([c]);
  assert(
    exported.chapters[0].source_readings.every(
      (r) => r.sourceId && r.wording && r.locator,
    ),
  );
  assert.equal(r.validChapter({ ...c, reference: r.REFERENCE }), false);
  assert.equal(r.validSnapshot({ ...s, birth: nativeWestern.birth }), false);
  for (const mutate of [
    (x) => (x.planets[0][0] = 360),
    (x) => (x.planets[1][2] = 13),
    (x) => (x.planets[0][1] = "true"),
    (x) => x.angles.push(0),
    (x) => x.cusps.pop(),
    (x) => (x.aspects[0].bodies[0] = "Invented"),
    (x) => (x.aspects[0].private = "birth"),
  ]) {
    const bad = structuredClone(s);
    mutate(bad);
    assert.equal(r.validSnapshot(bad), false);
  }
});
test("Chart projection aligns the actual Ascendant and preserves relative ecliptic longitudes", () => {
  assert(Math.abs(geometry.point(123, 200, 123).x - 100) < 1e-9);
  assert(Math.abs(geometry.point(123, 200, 123).y - 300) < 1e-9);
  assert(Math.abs(geometry.point(213, 200, 123).x - 300) < 1e-9);
  assert(Math.abs(geometry.point(213, 200, 123).y - 500) < 1e-9);
  // For this independently defined near-meridian fixture, MC is above ASC.
  const mc = geometry.point(
    nativeWestern.angles.midheaven,
    200,
    nativeWestern.angles.ascendant,
  );
  assert(mc.y < 300);
  const a = geometry.point(359, 180, 100),
    b = geometry.point(-1, 180, 100);
  assert(Math.hypot(a.x - b.x, a.y - b.y) < 1e-9);
});
test("Cross-oracle comparisons cite Western components without adding unsupported planet meanings", () => {
  const s = astro.westernSnapshot(nativeWestern),
    c = r.chapterFor(nativeWestern, s),
    result = compare.compareChapters(c, chapter(number));
  assert(result.leftEvidence.every((e) => e.sourceId && e.wording));
  assert(!("score" in result));
  assert(!("probability" in result));
  assert(
    !result.leftEvidence.some((e) => /Venus|Uranus|Neptune/.test(e.label)),
  );
});

const transit = await import(
  pathToFileURL(resolve("../../tmp/codex-tests/snapshot.mjs"))
);
const validateTransit = await import(
  pathToFileURL(resolve("../../tmp/codex-tests/validation.mjs"))
);
const turningNative = JSON.parse(
  readFileSync("../evidence/turning-engine.json", "utf8"),
).result;
test("Transit snapshots preserve exact contacts, native phase samples and duration values", () => {
  const s = transit.transitSnapshot(turningNative);
  assert(validateTransit.validTransit(s));
  assert(r.validSnapshot(s));
  const restored = transit.restoreTransit(s);
  assert.equal(
    restored.report.exact_events.length,
    turningNative.report.exact_events.length,
  );
  for (let i = 0; i < s.events.length; i++) {
    const a = restored.report.exact_events[i],
      b = turningNative.report.exact_events[i];
    for (const k of [
      "transiting",
      "natal_target",
      "aspect_degrees",
      "branch_degrees",
      "exact_utc",
      "longitude",
      "retrograde",
      "near_station",
      "pass_in_window",
      "passes_in_window",
      "transit_natal_house",
      "angular_residual_degrees",
    ])
      assert.deepEqual(a[k], b[k], k);
    for (const kind of ["direct", "components"])
      assert.deepEqual(
        a.interpretations[kind].map((r) => [
          r.rule_id,
          r.version,
          r.text,
          r.source,
          r.locator,
        ]),
        b.interpretations[kind].map((r) => [
          r.rule_id,
          r.version,
          r.text,
          r.source,
          r.locator,
        ]),
      );
  }
  for (let i = 0; i < s.configs.length; i++) {
    assert.deepEqual(
      restored.report.configurations[i].intervals,
      turningNative.report.configurations[i].intervals,
    );
    assert.equal(
      restored.report.configurations[i].hours_in_window,
      turningNative.report.configurations[i].hours_in_window,
    );
  }
  for (let i = 0; i < s.frames.length; i++) {
    const a = restored.sky_samples[i],
      b = turningNative.sky_samples[i];
    assert.equal(a.utc, b.utc);
    for (const name of astro.BODY_NAMES) {
      assert.equal(a.planets[name].longitude, b.planets[name].longitude);
      assert.equal(a.planets[name].retrograde, b.planets[name].retrograde);
    }
    assert.deepEqual(
      a.contacts.map((x) => x.phase),
      b.contacts.map((x) => x.phase),
    );
  }
});
test("Transit storage excludes natal inputs, request proofs, raw report and commentary", () => {
  const s = transit.transitSnapshot({
      ...turningNative,
      birth: "PRIVATE_BIRTH",
      origin: "PRIVATE_PROOF",
      gemini: "PRIVATE_AI",
    }),
    c = r.chapterFor(turningNative, s),
    memory = new Memory();
  assert.equal(c.reference, "fate-transit-reference-v1");
  assert(r.validChapter(c));
  r.saveChapter(memory, c);
  const raw = memory.getItem(r.STORAGE_KEY);
  for (const word of [
    "PRIVATE",
    "birth",
    "latitude",
    "longitude",
    "proof",
    "receipt",
    "gemini",
    "natal_summary",
  ])
    assert(!raw.includes(word));
  assert.deepEqual(r.readDocument(memory).chapters, [c]);
  assert.equal(r.validChapter({ ...c, reference: r.REFERENCE }), false);
  assert.equal(
    r.validChapter({ ...c, reference: "fate-western-reference-v1" }),
    false,
  );
});
test("Malformed or private-extra-key transit records fail closed without overwrite", () => {
  const valid = transit.transitSnapshot(turningNative);
  for (const mutate of [
    (s) => (s.birth = "private"),
    (s) => (s.window[1] = s.window[0]),
    (s) => (s.targets[0] = 360),
    (s) => (s.configs[0][6] = [999]),
    (s) => (s.events[0][0] = 999),
    (s) => (s.events[0][5] = "2"),
    (s) => s.frames[0][1].pop(),
    (s) => (s.frames[0][3][0][1] = 9),
    (s) => (s.frames[0][2][0] = "false"),
    (s) => (s.configs[0][5][0][4] = -1),
  ]) {
    const bad = structuredClone(valid);
    mutate(bad);
    assert.equal(validateTransit.validTransit(bad), false);
  }
  const c = r.chapterFor(turningNative, valid);
  const store = new Memory();
  const broken = JSON.stringify({
    schemaVersion: 1,
    chapters: [{ ...c, snapshot: { ...valid, proof: "private" } }],
  });
  store.data.set(r.STORAGE_KEY, broken);
  assert.throws(() => r.readDocument(store));
  assert.equal(store.getItem(r.STORAGE_KEY), broken);
  assert.equal(store.writes, 0);
});
test("Transit export and comparison cite only actual matched archived rules", () => {
  const s = transit.transitSnapshot(turningNative),
    c = r.chapterFor(turningNative, s),
    evidence = ref.evidenceFor(s),
    ids = new Set();
  for (const e of turningNative.report.exact_events)
    for (const kind of ["direct", "components"])
      for (const x of e.interpretations[kind]) ids.add(x.rule_id);
  for (const x of turningNative.report.configurations)
    for (const kind of ["direct", "components"])
      for (const z of x.interpretations[kind]) ids.add(z.rule_id);
  assert(evidence.length > 0);
  assert(evidence.every((e) => ids.has(e.sourceId) && e.url && e.locator));
  assert.deepEqual(ref.exportChapters([c]).chapters[0].snapshot, s);
  const match = compare.compareChapters(c, chapter(number));
  assert(!("score" in match));
  assert(!("probability" in match));
});
test("Old Codex editions remain readable beside the new dated chapter", () => {
  const store = new Memory();
  const a = chapter(tarot),
    b = chapter(number),
    c = r.chapterFor(turningNative, transit.transitSnapshot(turningNative));
  r.saveChapter(store, a);
  r.saveChapter(store, b);
  r.saveChapter(store, c);
  assert.deepEqual(r.readDocument(store).chapters, [a, b, c]);
  r.deleteChapter(store, c.id);
  assert.deepEqual(r.readDocument(store).chapters, [a, b]);
});
test("Four Chambers snapshots reject private extras, false hexagram transformations and unsupported values", () => {
  const bazi = { oracle: 3, profile: "civil-zi23", pairs: [0, 1, 2, 3] };
  const coins = {
    oracle: 18,
    profile: "legge-1882-scan-text-v1",
    values: [7, 7, 7, 7, 7, 7],
    figures: [1, 1],
  };
  const rune = {
    oracle: 19,
    profile: "elder24-page-facts-snapshot-v1",
    runes: ["rune-01"],
  };
  for (const record of [bazi, coins, rune]) {
    assert.equal(r.validSnapshot(record), true);
    assert.equal(
      r.validSnapshot({ ...record, birth: "1990-07-15T14:30:00" }),
      false,
    );
    const chapter = r.chapterFor({}, record);
    assert.equal(chapter.reference, "fate-four-chambers-v1");
  }
  assert.equal(r.validSnapshot({ ...bazi, profile: ["civil-zi23"] }), false);
  assert.equal(r.validSnapshot({ ...bazi, pairs: [0, 1, 2, 60] }), false);
  assert.equal(r.validSnapshot({ ...coins, figures: [1, 2] }), false);
  assert.equal(
    r.validSnapshot({ ...rune, runes: ["rune-01", "rune-01", "rune-01"] }),
    false,
  );
});
test("Ritual Wing saves only a recognized public edition and verified figure values", () => {
  const guide = {
    oracle: 21,
    profile: "atkinson-pg43954-guided-journal-v1",
    values: [],
  };
  const book = {
    oracle: 36,
    profile: "mascaro2022-manual-coarse-webclassic-ruth-v1",
    values: ["2", "RUT.1.s001"],
  };
  const geomancy = {
    oracle: 33,
    profile: "turner1655-common-shield-v1",
    values: [
      "1111",
      "1111",
      "1111",
      "1111",
      "1111",
      "1111",
      "1111",
      "1111",
      "2222",
      "2222",
      "2222",
      "2222",
      "2222",
      "2222",
      "2222",
    ],
  };
  for (const value of [guide, book, geomancy]) {
    assert.equal(r.validSnapshot(value), true);
    assert.equal(r.validSnapshot({ ...value, notes: "private" }), false);
    assert.equal(r.chapterFor({}, value).reference, "fate-ritual-wing-v1");
  }
  assert.equal(
    r.validSnapshot({ ...guide, values: ["imagined_imagery"] }),
    false,
  );
  assert.equal(
    r.validSnapshot({ ...book, values: ["3", "RUT.1.s001"] }),
    false,
  );
  assert.equal(
    r.validSnapshot({
      ...geomancy,
      values: [...geomancy.values.slice(0, 14), "1111"],
    }),
    false,
  );
});
test("World of Signs Codex only accepts named, valid declarations and keeps hazards out of storage", () => {
  const sign = {
    oracle: 34,
    profile: "howard-cottage-web-general-set-v1",
    values: ["onyx", "2:-1"],
  };
  assert.equal(r.validSnapshot(sign), true);
  assert.equal(r.chapterFor({}, sign).reference, "fate-world-of-signs-v1");
  assert.equal(r.validSnapshot({ ...sign, values: ["onyx", "100:3"] }), false);
  assert.equal(r.validSnapshot({ ...sign, observation: "private" }), false);
  assert.equal(
    r.validSnapshot({
      oracle: 30,
      profile: "pamita-public2026-candle-observation-v1",
      values: ["high", "persistent", "hazard", "reported_real"],
    }),
    false,
  );
});

const legacyVedic = () => JSON.parse(readFileSync("../evidence/block06-privacy-2.json")).stored.chapters[0];
function savedBazi() {
  const native = JSON.parse(readFileSync("../../data/bazi-core-1990.json"));
  const snapshot = {
    oracle: 3,
    profile: native.profile,
    pairs: ["year", "month", "day", "hour"].map((name) => native.pillars[name].sexagenary_index),
  };
  return r.chapterFor(native, snapshot, baziNarrative(snapshot, native));
}

test("first narrative save upgrades a mixed document atomically and preserves legacy IDs and exports", () => {
  const storage = new Memory();
  const legacy = legacyVedic();
  const original = JSON.stringify({ schemaVersion: 1, chapters: [legacy] });
  storage.data.set(r.STORAGE_KEY, original);
  assert.deepEqual(r.readDocument(storage).chapters, [legacy]);
  assert.equal(storage.writes, 0);
  const reading = savedBazi();
  assert(reading.narrative);
  const next = r.saveChapter(storage, reading);
  assert.deepEqual(next, { schemaVersion: 2, chapters: [legacy, reading] });
  assert.deepEqual(r.readDocument(storage), next);
  assert.equal(storage.writes, 1);
  assert.deepEqual(r.saveChapter(storage, reading), next);
  assert.equal(storage.writes, 1);
  assert.throws(() => r.saveChapter(storage, { ...chapter(), id: reading.id }), /identifier/);
  assert.throws(() => r.parseDocument(JSON.stringify({ ...next, chapters: [reading, reading] })));
  const oldExport = ref.exportChapters([legacy]);
  assert.equal(oldExport.schemaVersion, 1);
  const combined = ref.exportChapters(next.chapters);
  assert.equal(combined.schemaVersion, 2);
  assert.deepEqual(combined.chapters[0], oldExport.chapters[0]);
  assert.deepEqual(combined.chapters[1].narrative, reading.narrative);
  const comparison = compare.compareChapters(legacy, reading);
  assert(comparison.leftEvidence.every((e) => !e.rules));
  assert(comparison.rightEvidence.every((e) => e.rules.every((rule) => rule.id.startsWith("chinese."))));
  assert.deepEqual(r.deleteChapter(storage, reading.id), { schemaVersion: 2, chapters: [legacy] });
});

test("unavailable editions, missing rules, forged direct passages and private fields fail closed", () => {
  for (const mutate of [
    (n) => (n.edition = "unknown-edition"),
    (n) => (n.technique = 2),
    (n) => n.sections.reverse(),
    (n) => (n.sections[0].passages[0].rules = []),
    (n) => (n.sections[0].passages[0].rules = ["vedic.houses"]),
    (n) => (n.sections[1].passages[0].text = "Changed direct source passage."),
    (n) => (n.sections[0].passages[0].text = "<script>invalid</script>"),
    (n) => (n.sections[0].passages[0].text = "x".repeat(1801)),
    (n) => (n.sections[0].passages[0].url = "javascript:invalid"),
    (n) => (n.sections[0].birth = "private"),
  ]) {
    const reading = savedBazi();
    mutate(reading.narrative);
    const raw = JSON.stringify({ schemaVersion: 2, chapters: [legacyVedic(), reading] });
    const storage = new Memory();
    storage.data.set(r.STORAGE_KEY, raw);
    assert.throws(() => r.saveChapter(storage, chapter()), /unrecognized chapter or source edition/);
    assert.equal(storage.getItem(r.STORAGE_KEY), raw);
    assert.equal(storage.writes, 0);
  }
  assert.throws(() => r.parseDocument(JSON.stringify({ schemaVersion: 1, chapters: [savedBazi()] })));
});

test("failed upgrade and narrative capacity overflow keep previous records recoverable", () => {
  const storage = new Memory();
  const original = JSON.stringify({ schemaVersion: 1, chapters: [legacyVedic()] });
  storage.data.set(r.STORAGE_KEY, original);
  storage.setItem = () => { throw new DOMException("Quota", "QuotaExceededError"); };
  const reading = savedBazi();
  assert.throws(() => r.saveChapter(storage, reading), { name: "QuotaExceededError" });
  assert.equal(storage.getItem(r.STORAGE_KEY), original);
  storage.setItem = Memory.prototype.setItem;
  assert.equal(r.saveChapter(storage, reading).chapters.length, 2);
  let overflow = false;
  for (let i = 0; i < 49; i++) {
    const before = storage.getItem(r.STORAGE_KEY);
    try {
      r.saveChapter(storage, savedBazi());
    } catch (error) {
      assert.match(error.message, /Codex is full/);
      assert.equal(storage.getItem(r.STORAGE_KEY), before);
      assert.equal(r.readDocument(storage).chapters[0].id, legacyVedic().id);
      overflow = true;
      break;
    }
  }
  assert(overflow);
  assert.throws(() => r.parseDocument(" ".repeat(65537)), /safe reading limit/);
});

function numberFixture(value = 1, day = 1, year = 1) {
  return {
    profile: "decoz-component-reduction", name: { basis: "birth", original: "PRIVATE_NAME", tokens: ["PRIVATE_TOKENS"] },
    birth: "2000-02-29", target: "2026-12-31",
    life_path: { result: value }, expression: { result: value },
    soul_urge: { result: value }, personality: { result: value },
    birthday: { original_day: day, companion: { result: day === 29 ? 11 : 1 } },
    cycles: { year: { result: year }, month: { result: 4 }, day: { result: 8 } },
  };
}

test("Personal Code covers every declared direct value within its own section and keeps short cycles numerical", () => {
  for (const value of [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33]) {
    const result = numberFixture(value);
    const narrative = personalCode(result);
    const rows = narrative.sections.slice(0, 4);
    assert.equal(new Set(rows.map((row) => row.passages[0].text)).size, 4);
    for (const row of rows) {
      assert.equal(row.passages[0].coverage, "direct");
      assert.deepEqual(row.passages[0].rules, [`decoz.${row.id}.${value}`]);
    }
    assert(r.validChapter(r.chapterFor(result, r.numberSnapshot(result), narrative)));
  }
  for (let day = 1; day <= 31; day++) {
    const result = numberFixture(5, day, (day - 1) % 9 + 1);
    const narrative = personalCode(result);
    assert.deepEqual(narrative.sections[4].passages[0].rules, [`decoz.birthday.${day}`]);
    assert.equal(narrative.sections[4].passages[1].coverage, "calculated");
    assert.deepEqual(narrative.sections[5].passages.map((p) => p.coverage), ["direct", "calculated", "calculated"]);
    assert.deepEqual(narrative.sections[5].passages[0].rules, [`decoz.year.${result.cycles.year.result}`]);
    assert(r.validChapter(r.chapterFor(result, r.numberSnapshot(result), narrative)));
  }
});

test("Personal Code keeps missing letters and Minor names separate from birth-name delineations", () => {
  const result = numberFixture(11, 29, 3);
  result.soul_urge.result = null;
  assert.equal(personalCode(result).sections[2].passages[0].coverage, "unsupported");
  result.name.basis = "current";
  const narrative = personalCode(result);
  assert(narrative.sections.slice(1, 4).every((row) => row.passages[0].coverage === "unsupported"));
  assert.equal(narrative.sections[6].passages.length, 1);
  assert.match(narrative.sections[4].passages[1].text, /records 11/);
  assert(r.validChapter(r.chapterFor(result, r.numberSnapshot(result), narrative)));
});

test("Personal Code reopens schema 2 with legacy numbers and rejects edition, rule and scope mismatches", () => {
  const result = numberFixture(22, 24, 9);
  const reading = r.chapterFor(result, r.numberSnapshot(result), personalCode(result));
  const legacy = chapter(number);
  const storage = new Memory();
  r.saveChapter(storage, legacy);
  const written = r.saveChapter(storage, reading);
  assert.equal(written.schemaVersion, 2);
  assert.deepEqual(r.readDocument(storage).chapters, [legacy, reading]);
  assert.equal(ref.exportChapters([legacy]).schemaVersion, 1);
  const exported = ref.exportChapters(written.chapters);
  assert.deepEqual(exported.chapters[1].narrative, reading.narrative);
  assert(!JSON.stringify(exported).match(/PRIVATE_|2000-02-29|2026-12-31|tokens/));
  for (const mutate of [
    (c) => { c.narrative.edition = "unavailable"; },
    (c) => { c.narrative.sections[0].passages[0].rules = ["missing"]; },
    (c) => { c.narrative.sections[0].passages = c.narrative.sections[1].passages; },
    (c) => { c.snapshot.lifePath = 7; },
  ]) {
    const invalid = structuredClone(reading);
    mutate(invalid);
    assert(!r.validChapter(invalid));
  }
  assert.throws(() => r.parseDocument(" ".repeat(65537)), /safe reading limit/);
});
