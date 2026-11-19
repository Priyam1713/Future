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
  ],
  outdir: "../../tmp/codex-tests",
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
    JSON.stringify({ schemaVersion: 2, chapters: [] }),
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
