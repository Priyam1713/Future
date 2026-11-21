import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";

const base = process.env.FATE_CAPTURE_URL ?? "http://127.0.0.1:8010";
const key = "fate.codex.v1";
const profile = mkdtempSync(resolve("../../tmp/block19-profile-"));
const launch = () => chromium.launchPersistentContext(profile, {
  channel: "chrome", headless: true, viewport: null, reducedMotion: "reduce",
  args: ["--window-size=1440,1000"],
});
const legacy = {
  id: "10000000-0000-4000-8000-000000000001", savedAt: "2026-11-19T02:00:00.000Z",
  reference: "fate-codex-reference-v1",
  snapshot: { oracle: 4, profile: "decoz-component-reduction", lifePath: 1, expression: 3, personalYear: 2 },
};
const media = [];
const layouts = [];

async function screenshot(page, label, anchor) {
  await anchor.evaluate((node) => node.scrollIntoView({ block: "start" }));
  const file = `../screenshots/19-personal-code-${label}.png`;
  await page.screenshot({ path: file, scale: "css", animations: "disabled" });
  media.push({ path: file.replace("../", "fate/"),
    sha256: createHash("sha256").update(readFileSync(file)).digest("hex") });
}

async function layout(page, label) {
  const axe = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa"]).analyze();
  assert.deepEqual(axe.violations.map(({ id, nodes }) => ({ id, targets: nodes.map((row) => row.target) })), []);
  const widths = await page.evaluate(() => ({
    width: innerWidth, scrollWidth: document.documentElement.scrollWidth, dpr: devicePixelRatio,
  }));
  assert(widths.scrollWidth <= widths.width);
  layouts.push({ label, ...widths, violations: 0 });
}

async function reading(page) {
  await page.goto(`${base}/#numerology`);
  await page.getByLabel("Your full name").fill("Maya Wynn");
  await page.getByLabel("Date of birth").fill("2000-02-29");
  await page.getByLabel("Date to explore").fill("2026-12-31");
  await page.getByRole("combobox").nth(0).selectOption("c");
  await page.getByRole("combobox").nth(1).selectOption("v");
  await page.getByRole("button", { name: "Awaken my numbers" }).click();
  await page.getByRole("button", { name: "Go straight to my reading" }).click();
  await page.getByRole("heading", { name: "Life Path", exact: true }).waitFor();
  assert.equal(await page.locator(".number-dial").count(), 0);
}

async function reopen(page, expected) {
  await page.goto(`${base}/#my-fate`);
  await page.getByRole("button", { name: "Open your Codex" }).press("Enter");
  await page.locator(".codex-current").getByText("A 3 / 2 constellation").waitFor();
  await page.getByRole("button", { name: "Next chapter", exact: true }).press("Enter");
  const folio = page.locator(".codex-current .narrative-folio");
  for (const [i, section] of expected.sections.entries()) {
    await folio.getByRole("combobox", { name: "Reading section" }).selectOption(String(i));
    assert.deepEqual(await folio.locator(".narrative-passage > p").allTextContents(),
      section.passages.map((passage) => passage.text));
  }
  await folio.getByRole("combobox", { name: "Reading section" }).selectOption("0");
  return folio;
}

let context = await launch();
try {
  let page = context.pages()[0];
  await page.goto(`${base}/#my-fate`);
  await page.evaluate(({ key, legacy }) => localStorage.setItem(key, JSON.stringify({ schemaVersion: 1, chapters: [legacy] })), { key, legacy });
  await reading(page);
  assert.equal(JSON.parse(await page.evaluate((key) => localStorage.getItem(key), key)).schemaVersion, 1);
  const nav = page.getByRole("navigation", { name: "Personal Code chapters" });
  await nav.getByRole("button", { name: /Soul Urge/ }).press("Enter");
  await layout(page, "desktop reading");
  await screenshot(page, "desktop", nav);
  await nav.getByRole("button", { name: /Personal cycles/ }).press("Enter");
  await screenshot(page, "cycles", nav);
  await page.getByRole("button", { name: "Save to this device", exact: true }).press("Enter");
  await page.getByRole("button", { name: "Saved to this device" }).waitFor();
  const raw = await page.evaluate((key) => localStorage.getItem(key), key);
  const document = JSON.parse(raw);
  assert.equal(document.schemaVersion, 2);
  assert.deepEqual(document.chapters[0], legacy);
  assert(!/Maya|Wynn|2000-02-29|2026-12-31|y_roles|tokens|receipt/.test(raw));
  const narrative = document.chapters[1].narrative;
  await context.close();

  context = await launch();
  page = context.pages()[0];
  const posts = [];
  page.on("request", (req) => { if (req.method() === "POST") posts.push(req.url()); });
  await reopen(page, narrative);
  assert.deepEqual(posts, []);
  assert.equal(await page.evaluate((key) => localStorage.getItem(key), key), raw);
  await layout(page, "desktop reopened");
  await screenshot(page, "saved", page.locator(".codex-spread"));

  const settings = await context.newPage();
  await settings.goto("chrome://settings/appearance");
  await settings.locator("#zoomLevel").selectOption({ label: "200%" });
  await settings.close();
  const zoomed = await context.newPage();
  await reopen(zoomed, narrative);
  await layout(zoomed, "reopened at 200% browser zoom");
  assert.equal(layouts.at(-1).dpr, 2 * layouts[0].dpr);

  const browser = await chromium.launch();
  try {
    const mobile = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: "reduce" });
    const phone = await mobile.newPage();
    await reading(phone);
    await layout(phone, "mobile reading");
    await screenshot(phone, "mobile", phone.getByRole("navigation", { name: "Personal Code chapters" }));
  } finally {
    await browser.close();
  }
  writeFileSync("../evidence/block19-personal-code-media.json", JSON.stringify({
    synthetic: true, persistentBrowserRestart: true, privateInputExclusion: true,
    reopenPosts: posts.length, savedCharacters: JSON.stringify(document.chapters[1]).length,
    layouts, media,
  }, null, 2) + "\n");
} finally {
  await context.close();
}
