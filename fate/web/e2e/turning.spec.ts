import { test, expect, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { writeFileSync, readFileSync } from "node:fs";
async function enter(page: Page, days = 7) {
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
  const natal = page.waitForResponse((r) => r.url().endsWith("/api/western"));
  await page
    .getByRole("button", { name: "Open my celestial chart", exact: true })
    .click();
  const env = await (await natal).json();
  await page
    .getByRole("button", { name: "Skip reveal & read my chart" })
    .click();
  await page
    .getByRole("button", { name: "Enter The Turning Sky", exact: false })
    .click();
  await page.getByLabel("Start date and time · UTC").fill("2026-11-19T00:00");
  await page.getByLabel("Days to explore").selectOption(String(days));
  return env;
}
async function turn(page: Page) {
  const response = page.waitForResponse((r) =>
    r.url().endsWith("/api/western/transits"),
  );
  await page.getByRole("button", { name: "Turn my sky", exact: false }).click();
  const res = await response;
  expect(res.status()).toBe(200);
  const result = await res.json();
  await expect(page.locator(".turning-experience")).toBeVisible();
  return result;
}
test("live timeline reuses one natal calculation and steps through actual native daily positions", async ({
  page,
}) => {
  const posts: { url: string; body: any }[] = [];
  const errors: string[] = [];
  page.on("request", (r) => {
    if (r.method() === "POST")
      posts.push({ url: r.url(), body: r.postDataJSON() });
  });
  page.on("pageerror", (e) => errors.push(e.message));
  await enter(page);
  const result = await turn(page);
  expect(posts.filter((p) => p.url.endsWith("/api/western"))).toHaveLength(1);
  const q = posts.find((p) => p.url.endsWith("/api/western/transits"))!.body;
  expect(Object.keys(q)).toEqual(["origin", "start", "days"]);
  expect(q.origin.natal.birth).toBeUndefined();
  expect(await page.evaluate(() => localStorage.length)).toBe(0);
  expect(result.report.exact_events).toHaveLength(31);
  await page.getByRole("button", { name: "Next day", exact: false }).click();
  for (const [name, p] of Object.entries(result.sky_samples[1].planets) as [
    string,
    { longitude: number },
  ][])
    await expect(page.locator(`[data-sky-body="${name}"]`)).toHaveAttribute(
      "data-native-longitude",
      String(p.longitude),
    );
  await page.getByRole("slider", { name: "Explore the daily sky" }).focus();
  await page.keyboard.press("End");
  await expect(page.locator(".time-scrub")).toContainText("DAY 7 / 7");
  expect(errors).toEqual([]);
  await expect(page.locator("canvas")).toHaveCount(0);
  writeFileSync(
    "../evidence/turning-browser-native.json",
    JSON.stringify(
      {
        scope:
          "Actual synthetic QA native response; signed basis excludes birth inputs.",
        request: {
          start: q.start,
          days: q.days,
          basisKeys: Object.keys(q.origin.natal),
        },
        result,
      },
      null,
      2,
    ),
  );
});
test("exact contact selection, source limits, clipped duration and repeated views use canonical events", async ({
  page,
}) => {
  await enter(page);
  const r = await turn(page);
  await page.getByRole("checkbox", { name: "Show the entire window" }).check();
  await expect(page.locator(".event-track")).toHaveCount(
    r.report.exact_events.length,
  );
  await page.locator(".event-track").first().click();
  const e = r.report.exact_events[0];
  await expect(page.locator("[data-exact-longitude]")).toHaveAttribute(
    "data-exact-longitude",
    String(e.longitude),
  );
  await expect(page.locator(".contact-reading")).toContainText(e.transiting);
  await page.locator(".contact-duration>summary").click();
  await expect(page.locator(".contact-duration")).toContainText(e.exact_utc);
  await page.locator(".transit-sources>summary").first().click();
  await expect(page.locator(".transit-sources").first()).toContainText(
    e.interpretations.components[0].text,
  );
  await page
    .getByRole("button", { name: "Staying in orb", exact: true })
    .click();
  await expect(page.locator(".duration-tracks")).toContainText(
    "not strength, probability or personal importance",
  );
  expect(await page.locator(".duration-tracks article").count()).toBe(
    r.report.configurations.filter((c: any) => c.hours_in_window >= 24).length,
  );
  await page
    .getByRole("button", { name: "Repeated paths", exact: true })
    .click();
  if (r.report.presentation.repeated_patterns.length)
    await expect(page.locator(".repeated-tracks article")).toHaveCount(
      r.report.presentation.repeated_patterns.length,
    );
  else
    await expect(page.locator(".repeated-tracks")).toContainText(
      "No repeated exact sequence",
    );
});
test("dated chapter saves minimal native records, restores after refresh without POSTs and exports citations", async ({
  page,
}) => {
  await enter(page);
  const r = await turn(page);
  await page
    .getByRole("button", {
      name: "Save transit chapter to this device",
      exact: false,
    })
    .click();
  await expect(
    page.getByRole("button", { name: "Saved to this device", exact: false }),
  ).toBeDisabled();
  const raw = await page.evaluate(() => localStorage.getItem("fate.codex.v1"));
  const saved = JSON.parse(raw!);
  expect(saved.chapters[0].snapshot.profile).toBe("turning-sky-v1");
  for (const word of [
    "birth",
    "latitude",
    "longitude",
    "proof",
    "receipt",
    "gemini",
  ])
    expect(raw).not.toContain('"' + word + '"');
  await page
    .getByRole("button", { name: "Open in My Fate", exact: false })
    .click();
  await expect(page.locator(".transit-folio")).toBeVisible();
  const posts: string[] = [];
  page.on("request", (r) => {
    if (r.method() === "POST") posts.push(r.url());
  });
  await page.reload();
  await page
    .getByRole("button", { name: "Open your Codex", exact: true })
    .click();
  await expect(page.locator(".codex-current")).toContainText("THE TURNING SKY");
  await expect(page.locator(".transit-folio .time-instrument")).toBeVisible();
  await page
    .locator(".transit-folio")
    .getByRole("button", { name: "Next day", exact: false })
    .click();
  await expect(page.locator(".transit-folio .time-scrub")).toContainText(
    "DAY 2 / 7",
  );
  const download = page.waitForEvent("download");
  await page
    .getByRole("button", { name: "Export this chapter", exact: true })
    .click();
  const d = await download;
  const exported = JSON.parse(readFileSync((await d.path())!, "utf8"));
  expect(exported.chapters[0].snapshot).toEqual(saved.chapters[0].snapshot);
  expect(
    exported.chapters[0].source_readings.every(
      (e: any) => e.sourceId && e.url && e.locator,
    ),
  ).toBe(true);
  expect(posts).toEqual([]);
  writeFileSync(
    "../evidence/turning-privacy.json",
    JSON.stringify(
      {
        scope:
          "Actual explicit save/reopen/export. Raw birth fields and session proof excluded.",
        saved,
        postRequestsOnReopen: posts,
        exported,
        events: r.report.exact_events.length,
      },
      null,
      2,
    ),
  );
});
test("failed and cancelled searches retain the natal session and never fabricate a result", async ({
  page,
}) => {
  await enter(page);
  let calls = 0;
  await page.route("**/api/western/transits", async (route) => {
    calls++;
    if (calls === 1)
      return route.fulfill({
        status: 504,
        json: { detail: "Computation budget reached. Try fewer days." },
      });
    return route.continue();
  });
  await page.getByRole("button", { name: "Turn my sky", exact: false }).click();
  await expect(page.locator(".turning-status")).toContainText(
    "Computation budget reached",
  );
  await expect(page.locator(".turning-experience")).toHaveCount(0);
  await expect(page.getByLabel("Start date and time · UTC")).toHaveValue(
    "2026-11-19T00:00",
  );
  await turn(page);
  expect(calls).toBe(2);
  await page.route("**/api/western/transits", async (route) => {
    await new Promise((r) => setTimeout(r, 1000));
    await route
      .fulfill({ status: 499, json: { detail: "cancelled" } })
      .catch(() => {});
  });
  await page
    .getByRole("button", { name: "Calculate this window", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Stop calculation", exact: true })
    .click();
  await expect(page.locator(".turning-status")).toContainText(
    "Calculation stopped",
  );
  await page
    .getByRole("button", { name: "Your natal observatory", exact: false })
    .click();
  await expect(page.locator(".chart-reading")).toBeVisible();
});
test("timeline instrument respects pause/reduced motion and 320/390/768/1440 layouts with accessible controls", async ({
  page,
}) => {
  await enter(page, 2);
  await turn(page);
  for (const width of [320, 390, 768, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
  }
  await page.setViewportSize({ width: 390, height: 844 });
  await page
    .locator(".turning-layout")
    .evaluate((e) => e.scrollIntoView({ block: "start" }));
  const transform = () =>
    page.locator(".time-orbit").evaluate((e) => getComputedStyle(e).transform);
  const a = await transform();
  await page.waitForTimeout(300);
  expect(await transform()).not.toBe(a);
  await page.getByRole("button", { name: "About FATE and settings" }).click();
  await page.getByRole("button", { name: "Pause motion", exact: true }).click();
  await page.getByRole("button", { name: "Close settings" }).click();
  await expect(page.locator(".time-instrument")).toHaveAttribute(
    "data-render-state",
    "paused",
  );
  const b = await transform();
  await page.waitForTimeout(200);
  expect(await transform()).toBe(b);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await expect(page.locator(".time-instrument")).toHaveAttribute(
    "data-render-state",
    "paused",
  );
  const axe = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(
    axe.violations.map((v) => ({
      id: v.id,
      nodes: v.nodes.map((n) => n.target),
    })),
  ).toEqual([]);
});
test("mobile natal glyphs fan apart without moving native markers and comparison citations stay on demand", async ({
  page,
}) => {
  await enter(page, 1);
  await page
    .getByRole("button", { name: "Your natal observatory", exact: false })
    .click();
  const before = await page
    .locator("[data-planet]")
    .evaluateAll((es) =>
      Object.fromEntries(
        es.map((e) => [
          e.getAttribute("data-planet"),
          e.getAttribute("data-longitude"),
        ]),
      ),
    );
  await page
    .getByRole("button", { name: "Explore Mercury", exact: true })
    .click();
  await expect(page.locator(".chart-current")).toContainText("Mercury");
  const after = await page
    .locator("[data-planet]")
    .evaluateAll((es) =>
      Object.fromEntries(
        es.map((e) => [
          e.getAttribute("data-planet"),
          e.getAttribute("data-longitude"),
        ]),
      ),
    );
  expect(after).toEqual(before);
  const glyphs = await page
    .locator("[data-planet]>g>circle")
    .evaluateAll((es) =>
      es.map((e) => ({
        x: Number(e.getAttribute("cx")),
        y: Number(e.getAttribute("cy")),
      })),
    );
  for (let i = 0; i < glyphs.length; i++)
    for (let j = i + 1; j < glyphs.length; j++)
      expect(
        Math.hypot(glyphs[i].x - glyphs[j].x, glyphs[i].y - glyphs[j].y),
      ).toBeGreaterThanOrEqual(33.9);
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Visit the room of numbers", exact: false })
    .click();
  await page.getByLabel("Your full name").fill("Ada Lovelace");
  await page.getByLabel("Date of birth", { exact: true }).fill("1815-12-10");
  await page.getByLabel("Date to explore").fill("2026-11-19");
  await page.getByRole("button", { name: "Awaken my numbers" }).click();
  await page.getByRole("button", { name: "Go straight to my reading" }).click();
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  await page.getByRole("link", { name: /My Fate/ }).click();
  await page.locator(".perspective-picker input").nth(0).check();
  await page.locator(".perspective-picker input").nth(1).check();
  await page
    .getByRole("button", { name: "Compare Perspectives", exact: false })
    .click();
  await expect(page.locator(".perspective-constellation")).toBeVisible();
  const numerologyDifference = page
    .locator(".comparison-differences > div")
    .filter({ hasText: "NUMEROLOGY" });
  await expect(numerologyDifference).toContainText("Change & flexibility");
  await expect(
    numerologyDifference.locator(":scope > .comparison-quote"),
  ).toContainText(/\b(change|adaptability|flexibility|mutation|renewal)\b/i);
  const cite = page.locator(".comparison-citation").first();
  await expect(cite).not.toHaveAttribute("open", "");
  await cite.locator("summary").click();
  await expect(cite.getByRole("link", { name: "Sun in Cancer", exact: true }))
    .toHaveAttribute("href", /cafeastrology\.com/);
  await expect(cite).toContainText("fate.natal.v1.sign.sun.cancer");
});
