import { test, expect, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync, writeFileSync } from "node:fs";
const KEY = "fate.codex.v1";
const fixture = {
  schemaVersion: 1,
  chapters: [
    {
      id: "11111111-1111-4111-8111-111111111111",
      savedAt: "2026-11-19T02:00:00.000Z",
      reference: "fate-codex-reference-v1",
      snapshot: {
        oracle: 16,
        profile: "waite-1922-text-v1",
        spread: "one",
        cards: [{ id: "wands-ace", orientation: "upright" }],
      },
    },
    {
      id: "22222222-2222-4222-8222-222222222222",
      savedAt: "2026-11-19T02:00:00.000Z",
      reference: "fate-codex-reference-v1",
      snapshot: {
        oracle: 4,
        profile: "decoz-component-reduction",
        expression: 1,
        personalYear: 3,
        lifePath: 8,
      },
    },
  ],
};
async function seeded(page: Page, document: unknown = fixture) {
  await page.addInitScript(
    ({ key, document }) => {
      if (localStorage.getItem(key) === null)
        localStorage.setItem(key, JSON.stringify(document));
    },
    { key: KEY, document },
  );
  await page.goto("/#my-fate");
  await page.waitForTimeout(650);
}
async function tarot(
  page: Page,
  question = "A private question for this visit",
) {
  await page.goto("/");
  await page.locator(".room-index button").first().click();
  await page.getByLabel("What’s on your mind?").fill(question);
  const response = page.waitForResponse((r) =>
    r.url().endsWith("/api/readings"),
  );
  await page.getByRole("button", { name: "Draw my three cards" }).click();
  const result = (await (await response).json()).result;
  await page.getByRole("button", { name: "Skip reveal & read now" }).click();
  return result;
}
async function number(page: Page) {
  await page
    .getByRole("button", { name: "Explore Numerology", exact: true })
    .click();
  await page.getByLabel("Your full name").fill("Ada Lovelace");
  await page.getByLabel("Date of birth", { exact: true }).fill("1815-12-10");
  await page.getByLabel("Date to explore").fill("2032-05-06");
  const response = page.waitForResponse((r) =>
    r.url().endsWith("/api/numerology"),
  );
  await page.getByRole("button", { name: "Awaken my numbers" }).click();
  const result = (await (await response).json()).result;
  await page.getByRole("button", { name: "Go straight to my reading" }).click();
  return result;
}
async function accessible(page: Page) {
  await page.waitForTimeout(600);
  const result = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(
    result.violations.map((v) => ({
      id: v.id,
      nodes: v.nodes.map((n) => ({ target: n.target, why: n.failureSummary })),
    })),
  ).toEqual([]);
}
async function geometry(page: Page) {
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBeTruthy();
  expect(
    await page
      .locator("main button,main input,main summary")
      .evaluateAll((nodes) =>
        nodes
          .filter((el) => {
            const r = el.getBoundingClientRect();
            return r.width > 0 && (r.left < -0.5 || r.right > innerWidth + 0.5);
          })
          .map((el) => el.textContent?.slice(0, 60)),
      ),
  ).toEqual([]);
}

test("explicit native saves exclude private inputs and Gemini, survive refresh, reopen and export without engine calls", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.route("**/api/health", (route) =>
    route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({ status: "ok", gemini_available: true }),
    }),
  );
  const nativeTarot = await tarot(page, "PRIVATE_QUESTION_ONLY_FOR_THIS_VISIT");
  expect(await page.evaluate(() => localStorage.length)).toBe(0);
  await page.route("**/api/explain", (route) =>
    route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        cards: nativeTarot.readings.map((row: any) => ({
          card_id: row.card.id,
          rule_id: row.direct_component.rule_id,
          reflection: "PRIVATE_GEMINI_COMMENTARY",
        })),
        provenance: { provider: "gemini", model: "test-provider" },
        coverage: "experimental_ai_commentary",
      }),
    }),
  );
  await page.getByRole("checkbox", { name: /I agree to send/ }).check();
  await page.getByRole("button", { name: "Explain my reading" }).click();
  await expect(page.locator(".commentary")).toContainText(
    "PRIVATE_GEMINI_COMMENTARY",
  );
  const saveStarted = await page.evaluate(() => Date.now());
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .evaluate((b: HTMLButtonElement) => {
      b.click();
      b.click();
    });
  await expect(
    page.getByRole("button", { name: "Saved to this device" }),
  ).toBeDisabled();
  const nativeNumber = await number(page);
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  const raw = await page.evaluate((key) => localStorage.getItem(key)!, KEY);
  for (const secret of [
    "PRIVATE_QUESTION",
    "PRIVATE_GEMINI",
    "Ada",
    "Lovelace",
    "1815-12-10",
    "2032-05-06",
    "tokens",
    "replay",
    "commentary",
  ])
    expect(raw).not.toContain(secret);
  const document = JSON.parse(raw);
  expect(Date.parse(document.chapters[0].savedAt)).toBeGreaterThanOrEqual(
    saveStarted,
  );
  expect(document.chapters).toHaveLength(2);
  expect(document.chapters[0].snapshot.cards).toEqual(
    nativeTarot.readings.map((r: any) => ({
      id: r.card.id,
      orientation: r.orientation,
    })),
  );
  expect(document.chapters[1].snapshot).toEqual({
    oracle: 4,
    profile: nativeNumber.profile,
    expression: nativeNumber.expression.result,
    personalYear: nativeNumber.cycles.year.result,
    lifePath: nativeNumber.life_path.result,
  });
  await page.getByRole("button", { name: "Open in My Fate" }).click();
  await expect(page.locator(".codex-current")).toContainText(
    nativeNumber.readings[0].text,
  );
  await page.reload();
  const requests: string[] = [];
  page.on("request", (r) => {
    if (r.method() === "POST") requests.push(r.url());
  });
  await page.getByRole("button", { name: "Open your Codex" }).click();
  await expect(page.locator(".codex-current .folio-heading h2")).toHaveText(
    nativeTarot.readings.map((row: any) => row.card.name).join(" · "),
  );
  await page.getByRole("button", { name: "Next chapter", exact: true }).click();
  await expect(page.locator(".codex-current")).toContainText(
    nativeNumber.readings[0].text,
  );
  const downloading = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export Codex", exact: true }).click();
  const exported = JSON.parse(
    readFileSync((await (await downloading).path())!, "utf8"),
  );
  expect(exported.chapters).toHaveLength(2);
  expect(exported.chapters[1].source_readings[0].quote).toBe(
    nativeNumber.readings[0].text,
  );
  for (const secret of [
    "PRIVATE_QUESTION",
    "PRIVATE_GEMINI",
    "Ada Lovelace",
    "1815-12-10",
    "2032-05-06",
  ])
    expect(JSON.stringify(exported)).not.toContain(secret);
  expect(requests).toEqual([]);
  expect(errors).toEqual([]);
  writeFileSync(
    "../evidence/codex-privacy.json",
    JSON.stringify(
      {
        scope:
          "Real native browser saves; private sentinel inputs and mocked Gemini commentary excluded. Raw records contain only selected card IDs/orientations or numeric results, edition, random chapter ID and save time.",
        persisted: document,
        exported,
        postRequestsDuringReopen: requests,
      },
      null,
      2,
    ),
  );
});

test("chapters can be deleted individually or together with explicit confirmation and unrelated storage survives", async ({
  page,
}) => {
  await seeded(page);
  await page.evaluate(() => localStorage.setItem("unrelated", "keep"));
  await page.getByRole("button", { name: "Open your Codex" }).click();
  await page
    .getByRole("button", { name: "Delete this chapter", exact: true })
    .click();
  await expect(page.getByRole("dialog")).toContainText("Let this chapter go?");
  await page
    .getByRole("button", { name: "Keep this chapter", exact: true })
    .click();
  expect(
    await page.evaluate(
      (key) => JSON.parse(localStorage.getItem(key)!).chapters.length,
      KEY,
    ),
  ).toBe(2);
  await page
    .getByRole("button", { name: "Delete this chapter", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Delete chapter", exact: true })
    .click();
  expect(
    await page.evaluate(
      (key) => JSON.parse(localStorage.getItem(key)!).chapters.length,
      KEY,
    ),
  ).toBe(1);
  await expect(page.locator(".codex-current")).toContainText(
    "A 1 / 3 constellation",
  );
  await page.locator(".codex-privacy>summary").click();
  await page
    .getByRole("button", { name: "Delete all local Codex data" })
    .click();
  await page.getByRole("button", { name: "Delete all saved chapters" }).click();
  expect(
    await page.evaluate((key) => localStorage.getItem(key), KEY),
  ).toBeNull();
  expect(await page.evaluate(() => localStorage.getItem("unrelated"))).toBe(
    "keep",
  );
  await expect(page.locator(".empty-folio")).toBeVisible();
});

test("storage failures and unknown versions preserve the original record and never claim a save", async ({
  page,
  context,
}) => {
  await page.addInitScript(() => {
    const original = Storage.prototype.setItem;
    Storage.prototype.setItem = function (key, value) {
      if (key === "fate.codex.v1")
        throw new DOMException("Storage full", "QuotaExceededError");
      return original.call(this, key, value);
    };
  });
  await tarot(page);
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  await expect(page.locator(".save-status")).toContainText("could not change");
  expect(
    await page.evaluate((key) => localStorage.getItem(key), KEY),
  ).toBeNull();
  await expect(
    page.getByRole("heading", { name: "The story in your cards." }),
  ).toBeVisible();
  const second = await context.newPage();
  await second.addInitScript(() => {
    const raw = JSON.stringify({
      schemaVersion: 88,
      chapters: [{ private: "PRIVATE_CORRUPT_RECORD" }],
    });
    Object.defineProperty(window, "__futureRaw", { value: raw });
    localStorage.setItem("fate.codex.v1", raw);
  });
  await second.goto("/#my-fate");
  await expect(second.getByRole("alert")).toContainText("unavailable version");
  expect(await second.locator("main").textContent()).not.toContain(
    "PRIVATE_CORRUPT_RECORD",
  );
  const before = await second.evaluate((key) => localStorage.getItem(key), KEY);
  await second.getByRole("link", { name: "Explore", exact: true }).click();
  await second.locator(".room-index button").first().click();
  await second.getByRole("button", { name: "Draw my three cards" }).click();
  await second.getByRole("button", { name: "Skip reveal & read now" }).click();
  await second
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  await expect(second.locator(".save-status")).toContainText(
    "unavailable version",
  );
  expect(await second.evaluate((key) => localStorage.getItem(key), KEY)).toBe(
    before,
  );
  await second.close();
});

test("a second tab observes saves and deletion without retaining stale chapter content", async ({
  page,
  context,
}) => {
  await page.goto("/");
  const second = await context.newPage();
  await second.goto("/#my-fate");
  await second.getByRole("button", { name: "Open your Codex" }).click();
  const native = await tarot(page);
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  await expect(second.locator(".codex-current")).toContainText(
    native.readings[0].card.name,
  );
  await page.getByRole("button", { name: "Open in My Fate" }).click();
  await page.locator(".codex-privacy>summary").click();
  await page
    .getByRole("button", { name: "Delete all local Codex data" })
    .click();
  await page.getByRole("button", { name: "Delete all saved chapters" }).click();
  await expect(second.locator(".empty-folio")).toBeVisible();
  await expect(second.locator(".codex-current")).not.toContainText(
    native.readings[0].card.name,
  );
  await second.close();
});

test("the cover and real chapter leaf move, keyboard navigation works, reduced motion and low power stay usable", async ({
  page,
}) => {
  await seeded(page);
  const beam = page.locator(".codex-beam");
  await expect(page.locator(".celestial-book")).toHaveAttribute(
    "data-render-state",
    "running",
  );
  const first = await beam.evaluate((el) => getComputedStyle(el).transform);
  await page.waitForTimeout(400);
  expect(await beam.evaluate((el) => getComputedStyle(el).transform)).not.toBe(
    first,
  );
  await page.getByRole("button", { name: "Open your Codex" }).click();
  await page.waitForTimeout(900);
  await page.locator(".codex-spread").focus();
  await page.keyboard.press("ArrowRight");
  await expect(page.locator(".codex-current .folio-heading h2")).toHaveText(
    "A 1 / 3 constellation",
  );
  await expect(page.locator(".folio-turn")).toHaveAttribute("inert", "");
  await page.waitForTimeout(750);
  await expect(page.locator(".folio-turn")).toHaveCount(0);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.locator(".codex-spread").focus();
  await page.keyboard.press("ArrowLeft");
  await expect(page.locator(".codex-current .folio-heading h2")).toHaveText(
    "Ace of Wands",
  );
  await expect(page.locator(".celestial-book")).toHaveAttribute(
    "data-render-state",
    "paused",
  );
  await expect(page.locator(".folio-turn")).toHaveCount(0);
  // Single-finger horizontal turns remain usable; a pinch must not turn a leaf.
  await page.locator(".codex-spread").evaluate((el) => {
    const start = new Touch({
      identifier: 1,
      target: el,
      clientX: 250,
      clientY: 300,
    });
    const end = new Touch({
      identifier: 1,
      target: el,
      clientX: 80,
      clientY: 302,
    });
    el.dispatchEvent(
      new TouchEvent("touchstart", { bubbles: true, touches: [start] }),
    );
    el.dispatchEvent(
      new TouchEvent("touchend", {
        bubbles: true,
        touches: [],
        changedTouches: [end],
      }),
    );
  });
  await expect(page.locator(".codex-current .folio-heading h2")).toHaveText(
    "A 1 / 3 constellation",
  );
  await page.locator(".codex-spread").evaluate((el) => {
    const a = new Touch({
      identifier: 1,
      target: el,
      clientX: 80,
      clientY: 300,
    });
    const b = new Touch({
      identifier: 2,
      target: el,
      clientX: 200,
      clientY: 300,
    });
    const end = new Touch({
      identifier: 1,
      target: el,
      clientX: 260,
      clientY: 300,
    });
    el.dispatchEvent(
      new TouchEvent("touchstart", { bubbles: true, touches: [a, b] }),
    );
    el.dispatchEvent(
      new TouchEvent("touchend", {
        bubbles: true,
        touches: [],
        changedTouches: [end],
      }),
    );
  });
  await expect(page.locator(".codex-current .folio-heading h2")).toHaveText(
    "A 1 / 3 constellation",
  );
  await page.reload();
  await page.addInitScript(() => {
    Object.defineProperty(navigator, "hardwareConcurrency", { value: 4 });
    Object.defineProperty(navigator, "deviceMemory", { value: 4 });
  });
  await page.reload();
  await expect(page.locator(".celestial-book")).toHaveClass(/book-economy/);
  await page.getByRole("button", { name: "Open your Codex" }).click();
  await expect(page.locator(".codex-current")).toContainText("creation");
});

test("Codex mobile/desktop accessibility, bounded folios, real sourced comparison and one-tap collection navigation", async ({
  page,
}) => {
  await seeded(page);
  await accessible(page);
  await geometry(page);
  await page.getByRole("button", { name: "Open your Codex" }).click();
  await accessible(page);
  expect(
    await page
      .locator(".codex-spread")
      .evaluate((el) => el.getBoundingClientRect().height),
  ).toBeLessThanOrEqual(700);
  await geometry(page);
  await page.locator(".perspective-picker input").nth(0).check();
  await page.locator(".perspective-picker input").nth(1).check();
  await page
    .getByRole("button", { name: "Compare Perspectives", exact: false })
    .click();
  await expect(page.locator(".comparison-echo")).toContainText([
    "Beginnings & initiative",
    "Creativity & expression",
  ]);
  await expect(page.locator(".perspectives")).toContainText(
    "Initiative and autonomy.",
  );
  await expect(page.locator(".perspectives")).toContainText(
    "creation;enterprise;beginning",
  );
  await accessible(page);
  await geometry(page);
  for (const width of [320, 430, 768, 1440]) {
    await page.setViewportSize({ width, height: 1000 });
    await geometry(page);
  }
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page
    .getByRole("button", { name: "Back to your Codex", exact: false })
    .click();
  await expect(page.locator(".codex-spread")).toBeVisible();
  await accessible(page);
  await geometry(page);
  await page.getByRole("link", { name: "54 techniques", exact: true }).click();
  await expect(
    page.getByRole("searchbox", { name: "Find a tradition" }),
  ).toBeInViewport();
  expect(await page.locator("[data-technique-id]").count()).toBe(54);
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole("link", { name: "Explore", exact: true }).click();
  await page.getByRole("link", { name: "54 techniques", exact: true }).click();
  await expect(
    page.getByRole("searchbox", { name: "Find a tradition" }),
  ).toBeInViewport();
  await geometry(page);
});
