import { test, expect, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { writeFileSync } from "node:fs";
async function form(page: Page) {
  await page.goto("/#western");
  await page.getByLabel("Date of birth", { exact: true }).fill("1990-07-15");
  await page.getByLabel("Recorded birth time").fill("14:30:00");
  await page.getByLabel("Birth city", { exact: true }).fill("London GB");
  await page.getByRole("button", { name: "Find city", exact: true }).click();
  await page
    .getByRole("button", { name: /^London · GB/ })
    .first()
    .click();
  await page
    .getByLabel("I’ve checked the coordinates and timezone for my birthplace.")
    .check();
}
async function calculate(page: Page) {
  const response = page.waitForResponse((r) =>
    r.url().endsWith("/api/western"),
  );
  await page
    .getByRole("button", { name: "Open my celestial chart", exact: true })
    .click();
  return (await (await response).json()).result;
}
async function reading(page: Page) {
  await form(page);
  const r = await calculate(page);
  await page
    .getByRole("button", { name: "Skip reveal & read my chart" })
    .click();
  await expect(page.locator(".chart-reading")).toBeVisible();
  return r;
}
test("real chart, exact SVG geometry, progressive lights and immediate reading", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await form(page);
  const r = await calculate(page);
  for (const [name, p] of Object.entries(r.planets) as [
    string,
    { longitude: number },
  ][])
    await expect(page.locator(`[data-planet="${name}"]`)).toHaveAttribute(
      "data-longitude",
      String(p.longitude),
    );
  await expect(page.locator("[data-house]")).toHaveCount(12);
  await expect(page.locator("[data-bodies]")).toHaveCount(r.aspects.length);
  await expect(page.locator(".chart-reveal h2")).toContainText("Sun");
  const button = await page
    .getByRole("button", { name: "Reveal the next light" })
    .boundingBox();
  const nav = await page.locator(".fate-navigation").boundingBox();
  expect(button!.y + button!.height).toBeLessThan(nav!.y);
  const skip=await page.getByRole('button',{name:'Skip reveal & read my chart'}).boundingBox();
  expect(skip!.y+skip!.height).toBeLessThan(nav!.y);
  await page.getByRole("button", { name: "Reveal the next light" }).click();
  await expect(page.locator(".chart-reveal h2")).toContainText("Moon");
  await page.getByRole("button", { name: "Reveal the next light" }).click();
  await expect(page.locator(".chart-reveal h2")).toContainText("Ascendant");
  await page.getByRole("button", { name: "Enter my reading" }).click();
  await expect(page.locator(".chart-core-lights article")).toHaveCount(3);
  await expect(page.locator(".chart-core-lights")).toContainText("Cancer");
  expect(errors).toEqual([]);
  expect(await page.evaluate(() => Object.keys(localStorage))).toEqual([]);
  writeFileSync(
    "../evidence/western-browser-native.json",
    JSON.stringify(
      { fixture: "Synthetic QA moment, not a visitor identity", native: r },
      null,
      2,
    ),
  );
});
test("unknown birth time, real place confirmation and DST ambiguity fail honestly", async ({
  page,
}) => {
  await page.goto("/#western");
  await page.getByLabel("I don’t know my birth time").check();
  await expect(page.getByLabel("Recorded birth time")).toBeDisabled();
  await expect(
    page.getByRole("button", { name: "Open my celestial chart", exact: true }),
  ).toBeDisabled();
  await expect(page.locator(".birth-warning")).toContainText(
    "won’t substitute noon",
  );
  await page.reload();
  await form(page);
  await page.getByLabel("Date of birth", { exact: true }).fill("2024-11-03");
  await page.getByLabel("Recorded birth time").fill("01:30:00");
  await page.getByLabel("IANA timezone").fill("America/New_York");
  await page
    .getByLabel("I’ve checked the coordinates and timezone for my birthplace.")
    .check();
  await page
    .getByRole("button", { name: "Open my celestial chart", exact: true })
    .click();
  await expect(page.locator(".birth-error")).toContainText("Ambiguous");
  await page.locator(".birth-conventions summary").click();
  await page
    .getByLabel("Repeated local time at a clock change")
    .selectOption("1");
  const r = await calculate(page);
  expect(r.birth.utc).toBe("2024-11-03T06:30:00+00:00");
});
test("Western Codex keeps the exact natal narrative and geometry, reopens without POST and exports sources", async ({
  page, context,
}) => {
  await page.route('**/CodexScreen-*.js',async route=>{await new Promise(resolve=>setTimeout(resolve,1000));await route.continue();});
  const response = page.waitForResponse((r) => r.url().endsWith("/api/western"));
  const native = await reading(page);
  const { natal_reading: live } = await (await response).json();
  expect(await page.evaluate(() => localStorage.length)).toBe(0);
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Saved to this device", exact: true }),
  ).toBeDisabled();
  const raw = await page.evaluate(() => localStorage.getItem("fate.codex.v1"));
  const saved = JSON.parse(raw!);
  expect(saved.schemaVersion).toBe(2);
  const narrative = saved.chapters[0].narrative;
  expect(narrative.edition).toBe(live.profile);
  expect(narrative.sections.slice(0, live.chapters.length)).toEqual(live.chapters.map(
    ({ id, title, passages }: any) => ({ id, title, passages: passages.map((p: any) => ({
      title: p.title, text: p.body, coverage: p.coverage === "direct" ? "direct" : "compositional", rules: p.rule_ids,
    })) }),
  ));
  expect(saved.chapters[0].snapshot.oracle).toBe(1);
  expect(saved.chapters[0].snapshot.angles).toEqual([
    native.angles.ascendant,
    native.angles.midheaven,
  ]);
  for (const key of [
    "birth",
    "local",
    "utc",
    "zone",
    "latitude",
    "longitude",
    "receipt",
    "gemini",
  ])
    expect(raw).not.toContain(`"${key}"`);
  await page
    .getByRole("button", { name: "Open in My Fate", exact: false })
    .click();
  // This test deliberately delays the lazy Codex module; allow its dependency
  // graph to finish loading on the software-rendered regression runner.
  await expect(page.locator(".book-open")).toBeVisible({ timeout: 15000 });
  const posts: string[] = [];
  page.on("request", (r) => {
    if (r.method() === "POST") posts.push(r.url());
  });
  await page.reload();
  await page
    .getByRole("button", { name: "Open your Codex", exact: true })
    .click();
  await expect(page.locator(".codex-current")).toContainText(
    "WESTERN ASTROLOGY",
  );
  await expect(page.locator(".codex-current .birth-chart")).toHaveCount(1);
  const folio = page.locator(".narrative-folio");
  for (const [i, section] of narrative.sections.entries()) {
    await folio.getByRole("combobox", { name: "Reading section", exact: true }).selectOption(String(i));
    await expect(folio.locator(".narrative-passage > p")).toHaveText(section.passages.map((p: any) => p.text));
  }
  await folio.getByText("Sources and scope", { exact: true }).click();
  await expect(folio.getByText("fate.natal.v1", { exact: false }).first()).toBeVisible();
  const tab = await context.newPage();
  try {
    await tab.goto("/#my-fate");
    await tab.getByRole("button", { name: "Open your Codex", exact: true }).click();
    await expect(tab.locator(".narrative-folio")).toContainText(narrative.sections[0].passages[0].text);
  } finally {
    await tab.close();
  }
  const download = page.waitForEvent("download");
  await page
    .getByRole("button", { name: "Export this chapter", exact: true })
    .click();
  const dl = await download;
  expect(dl.suggestedFilename()).toContain(".json");
  const { readFile } = await import("node:fs/promises");
  const exported = JSON.parse(await readFile((await dl.path())!, "utf8"));
  expect(exported.schemaVersion).toBe(2);
  expect(exported.chapters[0].narrative).toEqual(narrative);
  expect(exported.chapters[0].source_readings.flatMap((row: any) => row.rules).length).toBeGreaterThan(0);
  expect(posts).toEqual([]);
  expect(await page.evaluate(() => localStorage.getItem("fate.codex.v1"))).toBe(
    raw,
  );
  writeFileSync(
    "../evidence/western-privacy.json",
    JSON.stringify(
      {
        saved,
        postsOnReopen: posts,
        originalInputKeysExcluded: [
          "birth",
          "local",
          "utc",
          "zone",
          "latitude",
          "longitude",
          "receipt",
          "gemini",
        ],
        assertionsPassed: true,
      },
      null,
      2,
    ),
  );
});
test("tactile planet selection, keyboard turn, pause, reduced motion and low-power do not alter geometry", async ({
  page,
  browser,
}) => {
  await reading(page);
  const coordinates = await page
    .locator("[data-planet]")
    .evaluateAll((es) => es.map((e) => e.getAttribute("data-longitude")));
  await page
    .getByRole("button", { name: "Explore Venus", exact: true })
    .click();
  await expect(page.locator(".placement-focus")).toContainText(
    "no planet-specific symbolic meaning for Venus",
  );
  const range = page.getByRole("slider", { name: "Turn the instrument" });
  await range.focus();
  await page.keyboard.press("ArrowRight");
  expect(await range.inputValue()).toBe("1");
  await page.getByRole("button", { name: "Align Ascendant" }).click();
  expect(await range.inputValue()).toBe("0");
  expect(
    await page
      .locator("[data-planet]")
      .evaluateAll((es) => es.map((e) => e.getAttribute("data-longitude"))),
  ).toEqual(coordinates);
  await page.locator(".western-instrument").scrollIntoViewIfNeeded();
  const transform = () =>
    page
      .locator(".chart-engraving")
      .evaluate((e) => getComputedStyle(e).transform);
  const a = await transform();
  await page.waitForTimeout(300);
  expect(await transform()).not.toBe(a);
  await page.getByRole("button", { name: "About FATE and settings" }).click();
  await page.getByRole("button", { name: "Pause motion", exact: true }).click();
  await page.getByRole("button", { name: "Close settings" }).click();
  await expect(page.locator(".birth-chart")).toHaveAttribute(
    "data-render-state",
    "paused",
  );
  const b = await transform();
  await page.waitForTimeout(250);
  expect(await transform()).toBe(b);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await expect(page.locator(".birth-chart")).toHaveAttribute(
    "data-render-state",
    "paused",
  );
  const c = await browser.newContext({
    viewport: { width: 390, height: 844 },
    reducedMotion: "reduce",
  });
  await c.addInitScript(() => {
    Object.defineProperty(navigator, "hardwareConcurrency", { get: () => 2 });
    Object.defineProperty(navigator, "deviceMemory", { get: () => 2 });
  });
  const p = await c.newPage();
  await reading(p);
  await expect(p.locator(".birth-chart")).toHaveClass(/chart-economy/);
  await expect(p.locator("canvas")).toHaveCount(0);
  await c.close();
});
test("responsive chart, source reading and refined Codex pass accessibility and geometry checks", async ({
  page,
}) => {
  await reading(page);
  for (const width of [320, 390, 768, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    await expect(
      page.getByRole("button", { name: "Explore Sun", exact: true }),
    ).toBeVisible();
  }
  await page.setViewportSize({ width: 390, height: 844 });
  await page.evaluate(() => document.fonts.ready);
  const results = await new AxeBuilder({ page }).analyze();
  expect(
    results.violations.filter(
      (v) => v.impact === "critical" || v.impact === "serious",
    ),
  ).toEqual([]);
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Open in My Fate", exact: false })
    .click();
  await page.waitForTimeout(950);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  const codex = await new AxeBuilder({ page }).analyze();
  expect(
    codex.violations.filter(
      (v) => v.impact === "critical" || v.impact === "serious",
    ),
  ).toEqual([]);
});
test("failed calculation keeps inputs, duplicate clicks produce one native request and consent is separate", async ({
  page,
}) => {
  await page.route("**/api/health", (r) =>
    r.fulfill({ json: { status: "ok", gemini_available: true } }),
  );
  await form(page);
  let calls = 0;
  await page.route("**/api/western", async (route) => {
    calls++;
    if (calls === 1)
      await route.fulfill({
        status: 503,
        json: { detail: "Temporary calculation failure" },
      });
    else await route.continue();
  });
  await page
    .getByRole("button", { name: "Open my celestial chart", exact: true })
    .click();
  await expect(page.locator(".birth-error")).toContainText(
    "Temporary calculation failure",
  );
  await expect(page.getByLabel("Recorded birth time")).toHaveValue("14:30:00");
  await calculate(page);
  expect(calls).toBe(2);
  await page
    .getByRole("button", { name: "Skip reveal & read my chart" })
    .click();
  let explains = 0;
  await page.route("**/api/western/explain", (r) => {
    explains++;
    expect(r.request().postDataJSON().cloud_consent).toBe(true);
    return r.fulfill({
      json: {
        themes: [{ id: "fixture", reflection: "PRIVATE_GEMINI_SENTINEL" }],
        provenance: { provider: "mock", model: "test" },
        coverage: "experimental_ai_commentary",
      },
    });
  });
  await expect(
    page.getByRole("button", { name: "Request optional commentary" }),
  ).toBeDisabled();
  expect(explains).toBe(0);
  await page.getByLabel("I agree to send these source components").check();
  await page
    .getByRole("button", { name: "Request optional commentary" })
    .click();
  await expect(page.locator(".chart-ai")).toContainText(
    "PRIVATE_GEMINI_SENTINEL",
  );
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  expect(
    await page.evaluate(() => localStorage.getItem("fate.codex.v1")),
  ).not.toContain("PRIVATE_GEMINI_SENTINEL");
  expect(explains).toBe(1);
});

test("natal chapters and the instrument connect only supported meanings to native contacts", async ({page}) => {
  await reading(page);
  const story = page.getByRole("region", {name: "Natal reading"});
  await expect(story.getByRole("heading", {name: "Purpose and presence"})).toBeVisible();
  await story.getByRole("button", {name: "Feelings", exact: true}).press("Enter");
  await expect(story).toContainText("Warmth and reserve");
  await story.getByRole("button", {name: "Themes", exact: true}).press("Enter");
  await expect(story).toContainText("Room to grow, room for limits");
  await expect(story).toContainText("Purpose and need pull differently");
  await story.getByText("Sources and scope", {exact: true}).click();
  await expect(story).toContainText("fate.natal.v1.aspect.sun.jupiter.0");
  await story.getByRole("link", {name: "Explore the chart"}).press("Enter");
  await expect(page.getByRole("heading", {name: "Explore your chart"})).toBeFocused();
  const inspector = page.getByRole("region", {name: "Selected chart detail"});
  await inspector.getByLabel("Choose a house").selectOption("10");
  await expect(inspector).toContainText("A voice in public work");
  await inspector.getByLabel("Choose an aspect").selectOption("aspect:Sun-Moon:90");
  await expect(inspector).toContainText("Purpose and need pull differently");
  await inspector.getByLabel("Choose an aspect").selectOption("aspect:Neptune-Pluto:60");
  await expect(inspector).toContainText("A direct reading for this pair and angle is outside this edition");
  await inspector.getByRole("button", {name: "Ascendant", exact: true}).press("Enter");
  await expect(inspector).toContainText("Mars in Taurus");
  await expect(page.locator(".western-chart-layout [data-bodies=Sun-Moon]")).toHaveCount(1);
  expect(await page.evaluate(() => Object.keys(localStorage))).toEqual([]);
});
