import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";

const base = process.env.FATE_CAPTURE_URL ?? "http://127.0.0.1:8010";
const key = "fate.codex.v1";
const seed = "2f".padStart(64, "0");
const privateQuestion = "PRIVATE_BLOCK20_QUESTION";
const profile = mkdtempSync(join(tmpdir(), "fate-connected-tarot-"));
const launch = () => chromium.launchPersistentContext(profile, {
  channel: "chrome", headless: true, viewport: null, reducedMotion: "reduce",
  args: ["--window-size=1440,1000"],
});
const legacy = {
  id: "10000000-0000-4000-8000-000000000001", savedAt: "2026-11-19T02:00:00.000Z",
  reference: "fate-codex-reference-v1",
  snapshot: { oracle: 16, profile: "waite-1922-text-v1", spread: "one",
    cards: [{ id: "wands-ace", orientation: "upright" }] },
};
const media = [];
const layouts = [];
const button = (page, name) => page.getByRole("button", { name, exact: true });
const spread = (page) => page.locator(".connected-spread");

async function capture(page, label, anchor) {
  await anchor.evaluate((node) => node.scrollIntoView({ block: "start" }));
  await page.evaluate(() => document.activeElement?.blur());
  await page.locator(".connected-card-art img").evaluateAll((images) =>
    Promise.all(images.map((image) => image.decode())));
  await page.evaluate(() => document.fonts.ready);
  const file = `../screenshots/20-connected-${label}.png`;
  await page.screenshot({ path: file, scale: "css", animations: "disabled" });
  media.push({ path: file.replace("../", "fate/"),
    sha256: createHash("sha256").update(readFileSync(file)).digest("hex") });
}

async function layout(page, label) {
  const axe = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa"]).analyze();
  assert.deepEqual(axe.violations.map(({ id, nodes }) => ({ id, targets: nodes.map((row) => row.target) })), []);
  const dimensions = await page.evaluate(() => ({
    width: innerWidth, scrollWidth: document.documentElement.scrollWidth, dpr: devicePixelRatio,
  }));
  assert(dimensions.scrollWidth <= dimensions.width);
  layouts.push({ label, ...dimensions, violations: axe.violations.length });
}

async function reading(page, question) {
  await page.goto(`${base}/#ritual`);
  if (question) await page.getByLabel("What’s on your mind?").fill(question);
  await page.route("**/api/readings", (route) => route.continue({
    postData: JSON.stringify({ ...route.request().postDataJSON(), seed }),
  }));
  const response = page.waitForResponse("**/api/readings");
  await button(page, "Draw my three cards").press("Enter");
  const native = (await (await response).json()).result;
  await button(page, "Skip reveal & read now").press("Enter");
  await spread(page).waitFor();
  return native;
}

async function verifyPassages(page, chapter) {
  const table = spread(page).locator(".connected-table");
  const [overview, ...sections] = chapter.narrative.sections;
  assert.equal(await spread(page).locator(".spread-overview > p").textContent(), overview.passages[0].text);
  const relationships = sections.find(({ id }) => id === "relationships");
  assert.deepEqual(await spread(page).locator(".spread-connection > p").allTextContents(),
    relationships.passages.map(({ text }) => text));
  assert.equal(await spread(page).locator(".spread-closing > p").textContent(), sections.at(-1).passages[0].text);
  for (const [index, pick] of chapter.snapshot.cards.entries()) {
    const card = table.getByRole("button").nth(index);
    assert.equal(await card.getAttribute("data-card"), pick.id);
    assert.equal(await card.getAttribute("data-orientation"), pick.orientation);
    assert.equal(await card.locator("[data-artwork-id]").getAttribute("data-artwork-id"), pick.id);
    assert.equal(await card.locator(".reversed-art").count(), Number(pick.orientation === "reversed"));
    await card.press("Enter");
    const detail = spread(page).locator(".connected-position");
    assert.equal(await card.getAttribute("aria-pressed"), "true");
    assert.equal(await detail.locator(".position-reading").textContent(), sections[index].passages[0].text);
    await detail.getByText("The traditional meaning", { exact: true }).press("Enter");
    assert.equal(await detail.locator("blockquote").first().textContent(), sections[index].passages[1].text);
    assert((await detail.locator(".rule-reference").textContent()).includes(sections[index].passages[1].rules[0]));
    await detail.getByText("The traditional meaning", { exact: true }).press("Enter");
  }
}

async function reopen(page, chapter) {
  await page.goto(`${base}/#my-fate`);
  await button(page, "Open your Codex").press("Enter");
  await page.locator(".codex-current").getByRole("heading", { name: "Ace of Wands", exact: true }).waitFor();
  await button(page, "Next chapter").press("Enter");
  await page.locator(".codex-current .connected-spread").waitFor();
  await verifyPassages(page, chapter);
}

let context = await launch();
try {
  let page = context.pages()[0];
  await page.goto(`${base}/#my-fate`);
  await page.evaluate(({ key, legacy }) => localStorage.setItem(key, JSON.stringify({ schemaVersion: 1, chapters: [legacy] })), { key, legacy });
  const native = await reading(page, privateQuestion);
  await layout(page, "desktop reading");
  await capture(page, "desktop", spread(page));
  await button(page, "Save to this device").press("Enter");
  await button(page, "Saved to this device").waitFor();
  const raw = await page.evaluate((key) => localStorage.getItem(key), key);
  const stored = JSON.parse(raw);
  assert.equal(stored.schemaVersion, 2);
  assert.deepEqual(stored.chapters[0], legacy);
  for (const secret of [privateQuestion, seed, '"replay":', '"question":', '"provider":']) {
    assert(!raw.includes(secret), secret);
  }
  const chapter = stored.chapters[1];
  assert.equal(chapter.narrative.edition, "fate-waite-connected-v1");
  assert.deepEqual(chapter.snapshot.cards, native.readings.map((r) => ({ id: r.card.id, orientation: r.orientation })));
  await verifyPassages(page, chapter);
  await context.close();

  context = await launch();
  page = context.pages()[0];
  const requests = [];
  const trackApi = (request) => {
    if (new URL(request.url()).pathname.startsWith("/api/")) requests.push(request.url());
  };
  context.on("request", trackApi);
  await reopen(page, chapter);
  assert.deepEqual(requests, []);
  assert.equal(await page.evaluate((key) => localStorage.getItem(key), key), raw);
  await layout(page, "desktop reopened");
  await page.locator(".codex-current").evaluate((chapter) => { chapter.scrollTop = 178; });
  await capture(page, "saved", page.locator(".codex-spread"));

  const settings = await context.newPage();
  await settings.goto("chrome://settings/appearance");
  await settings.locator("#zoomLevel").selectOption({ label: "200%" });
  await settings.close();
  const zoomed = await context.newPage();
  await reopen(zoomed, chapter);
  await layout(zoomed, "reopened at 200% browser zoom");
  assert.equal(layouts.at(-1).dpr, 2 * layouts[0].dpr);
  assert.deepEqual(requests, []);
  context.off("request", trackApi);
  await reading(zoomed);
  await layout(zoomed, "live reading at 200% browser zoom");

  const browser = await chromium.launch();
  try {
    const mobile = await browser.newContext({ viewport: { width: 390, height: 844 },
      isMobile: true, hasTouch: true, reducedMotion: "reduce" });
    const phone = await mobile.newPage();
    await reading(phone);
    await layout(phone, "mobile reading");
    await capture(phone, "mobile", spread(phone));
  } finally {
    await browser.close();
  }
  writeFileSync("../evidence/block20-tarot-media.json", JSON.stringify({
    synthetic: true, persistentChromeRestart: true, privateInputExclusion: true,
    reopenApiRequests: requests.length, savedCharacters: JSON.stringify(chapter).length, layouts, media,
  }, null, 2) + "\n");
} finally {
  await context.close();
  rmSync(profile, { recursive: true, force: true, maxRetries: 3, retryDelay: 150 });
}
