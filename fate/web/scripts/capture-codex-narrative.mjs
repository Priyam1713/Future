import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";

const base = process.env.FATE_CAPTURE_URL ?? "http://127.0.0.1:8010";
const key = "fate.codex.v1";
const legacy = JSON.parse(readFileSync("../evidence/block06-privacy-2.json")).stored;
const profile = mkdtempSync(resolve("../../tmp/block18-codex-profile-"));
const launch = () => chromium.launchPersistentContext(profile, {
  channel: "chrome", headless: true, viewport: null, reducedMotion: "reduce",
  args: ["--window-size=1440,1000"],
});
const captures = [];
const checks = [];
const readingNames = { 1: "western", 2: "jyotish", 3: "bazi" };
const captureSection = { 1: "emotion", 2: "periods", 3: "month" };

async function save(page, room) {
  await page.goto(`${base}/#${room}`);
  await page.getByLabel("Date of birth", { exact: true }).fill("1990-07-15");
  await page.getByLabel("Recorded birth time").fill("14:30:00");
  await page.getByLabel("Birth city", { exact: true }).fill("London GB");
  await page.getByRole("button", { name: "Find city", exact: true }).click();
  await page.getByRole("button", { name: /^London · GB/ }).first().click();
  await page.getByLabel("I’ve checked the coordinates and timezone for my birthplace.").check();
  if (room === "vedic") await page.getByLabel("Explore periods on this UTC day").fill("2026-11-20");
  const open = { western: "Open my celestial chart", vedic: "Open my sidereal charts", bazi: "Open my Four Pillars" };
  await page.getByRole("button", { name: open[room], exact: true }).click();
  if (room === "western") await page.getByRole("button", { name: "Skip reveal & read my chart" }).click();
  await page.getByRole("button", {
    name: room === "western" ? "Save to this device" : "Save chamber chapter to this device",
    exact: true,
  }).click();
  await page.getByRole("button", { name: "Open in My Fate", exact: false }).waitFor();
}

async function openLibrary(page) {
  await page.goto(`${base}/#my-fate`);
  await page.getByRole("button", { name: "Open your Codex", exact: true }).click();
  await page.locator(".codex-current h2").waitFor();
}

async function openContents(page) {
  const contents = page.locator(".codex-contents");
  if (!(await contents.evaluate((node) => node.open))) {
    await contents.locator("summary").click();
  }
  return contents.getByRole("button");
}

async function inspect(page, library, size) {
  const posts = [];
  page.on("request", (req) => { if (req.method() === "POST") posts.push(req.url()); });
  await openLibrary(page);
  assert.equal(await page.locator(".celestial-book").getAttribute("data-render-state"), "paused");
  await page.getByText("UTC boundary days", { exact: false }).first().waitFor();
  for (const [index, entry] of library.chapters.entries()) {
    if (!entry.narrative) continue;
    await (await openContents(page)).nth(index).press("Enter");
    const folio = page.locator(".codex-current .narrative-folio");
    await folio.waitFor();
    const control = folio.getByRole("combobox", { name: "Reading section", exact: true });
    for (const [position, section] of entry.narrative.sections.entries()) {
      await control.selectOption(String(position));
      assert.deepEqual(await folio.locator(".narrative-passage > p").allTextContents(),
        section.passages.map((passage) => passage.text));
    }
    const technique = entry.narrative.technique;
    const position = entry.narrative.sections.findIndex((section) => section.id === captureSection[technique]);
    await control.selectOption(String(position));
    await folio.getByText("Sources and scope", { exact: true }).press("Enter");
    assert((await folio.textContent()).includes(entry.narrative.sections[position].passages[0].rules[0]));
    const accessibility = await new AxeBuilder({ page }).include(".narrative-folio")
      .withTags(["wcag2a", "wcag2aa"]).analyze();
    assert.deepEqual(accessibility.violations.map((v) => v.id), []);
    const widths = await page.evaluate(() => ({
      inner: innerWidth, scroll: document.documentElement.scrollWidth, dpr: devicePixelRatio,
    }));
    assert(widths.scroll <= widths.inner);
    checks.push({ size, technique, ...widths, violations: 0 });
    if (size !== "zoom200") {
      await folio.getByText("Sources and scope", { exact: true }).press("Enter");
      const path = `../screenshots/18-codex-${readingNames[technique]}-${size}.png`;
      await folio.locator("h2").focus();
      await page.locator(".codex-current").evaluate((node) => { node.scrollTop = 0; });
      await page.locator(".codex-contents ol").evaluate((node) => { node.scrollTop = 0; });
      await page.locator(".codex-spread").evaluate((node) => node.scrollIntoView({ block: "start" }));
      await page.screenshot({ path, scale: "css", animations: "disabled" });
      captures.push({ path: path.replace("../", "fate/"),
        sha256: createHash("sha256").update(readFileSync(path)).digest("hex") });
    }
  }
  if (size === "desktop") {
    const choices = page.locator(".perspective-picker").getByRole("checkbox");
    await choices.nth(1).check();
    await choices.nth(3).check();
    await page.getByRole("button", { name: "Compare Perspectives", exact: false }).click();
    const comparison = page.locator(".perspectives");
    await comparison.getByText("How this comparison works", { exact: true }).click();
    const text = await comparison.locator(".comparison-method").textContent();
    assert(text.includes("fate-western-natal-v1"));
    assert(text.includes("fate-bazi-reading-v1"));
  }
  assert.deepEqual(posts, []);
}

let context = await launch();
let raw;
let storage;
try {
  let page = context.pages()[0];
  await page.goto(`${base}/#my-fate`);
  await page.evaluate(({ key, legacy }) => localStorage.setItem(key, JSON.stringify(legacy)), { key, legacy });
  for (const room of ["western", "vedic", "bazi"]) await save(page, room);
  raw = await page.evaluate((name) => localStorage.getItem(name), key);
  const library = JSON.parse(raw);
  assert.equal(library.schemaVersion, 2);
  assert.deepEqual(library.chapters[0], legacy.chapters[0]);
  assert.deepEqual(library.chapters.slice(1).map((entry) => entry.narrative.technique), [1, 2, 3]);
  storage = await context.storageState();
  await context.close();

  context = await launch();
  page = context.pages()[0];
  await page.goto(`${base}/#my-fate`);
  assert.equal(await page.evaluate((name) => localStorage.getItem(name), key), raw);
  await inspect(page, library, "desktop");
  const settings = await context.newPage();
  await settings.goto("chrome://settings/appearance");
  await settings.locator("#zoomLevel").selectOption({ label: "200%" });
  await settings.close();
  await inspect(await context.newPage(), library, "zoom200");
  for (const row of checks.filter((row) => row.size === "zoom200")) {
    assert.equal(row.dpr, 2 * checks.find((match) => match.size === "desktop" &&
      match.technique === row.technique).dpr);
  }
  const browser = await chromium.launch();
  try {
    const phone = await browser.newContext({ storageState: storage, viewport: { width: 390, height: 844 },
      isMobile: true, hasTouch: true, deviceScaleFactor: 2, reducedMotion: "reduce" });
    await inspect(await phone.newPage(), library, "mobile");
  } finally {
    await browser.close();
  }
  writeFileSync("../evidence/block18-codex-media.json", JSON.stringify({
    syntheticInput: "1990-07-15 14:30 London; Jyotish timing day 2026-11-20",
    persistentBrowserRestart: true, narrativeComparison: true, reopenPosts: 0, totalCharacters: raw.length,
    chapterCharacters: library.chapters.map((chapter) => JSON.stringify(chapter).length),
    checks, captures,
  }, null, 2) + "\n");
} finally {
  await context.close();
}
