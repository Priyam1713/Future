import { expect, test, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync, writeFileSync } from "node:fs";
import type { RitualEnvelope } from "../src/ritual/contracts";

const notes =
  "Synthetic QA note: lavender light at the edge. Keep this private.";
async function room(page: Page, slug: string) {
  await page.goto("/#" + slug);
  await expect(page.locator(".ritual-intro h1")).toBeVisible();
}
async function report(page: Page, action: string): Promise<RitualEnvelope> {
  const pending = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/ritual-wing") && r.request().method() === "POST",
  );
  await page.getByRole("button", { name: action, exact: true }).click();
  const response = await pending;
  expect(response.ok(), await response.text()).toBeTruthy();
  const result = await response.json();
  await expect(page.locator(".ritual-result")).toBeVisible();
  return result;
}
async function save(page: Page, data: RitualEnvelope) {
  expect(
    await page.evaluate(() => localStorage.getItem("fate.codex.v1")),
  ).toBeNull();
  await page
    .getByRole("button", {
      name: "Save ritual chapter to this device",
      exact: true,
    })
    .click();
  const raw = await page.evaluate(() => localStorage.getItem("fate.codex.v1"));
  expect(raw).not.toBeNull();
  const stored = JSON.parse(raw!);
  expect(stored.chapters[0].snapshot).toEqual(data.snapshot);
  expect(stored.chapters[0].reference).toBe("fate-ritual-wing-v1");
  expect(raw).not.toMatch(
    /"(seed|replay|journal|narrative|context|description|observations|calibration|session)"/,
  );
  expect(raw).not.toContain(notes);
  const posts: string[] = [];
  page.on("request", (req) => {
    if (req.method() === "POST") posts.push(req.url());
  });
  await page.getByRole("button", { name: /Open in My Fate/ }).click();
  await expect(page.locator(".ritual-folio")).toBeVisible({ timeout: 15000 });
  await page.reload();
  await page
    .getByRole("button", { name: "Open your Codex", exact: true })
    .click();
  await expect(page.locator(".ritual-folio")).toBeVisible();
  const download = page.waitForEvent("download");
  await page
    .getByRole("button", { name: "Export this chapter", exact: true })
    .click();
  const output = JSON.parse(
    readFileSync((await (await download).path())!, "utf8"),
  );
  expect(output.chapters[0].snapshot).toEqual(data.snapshot);
  expect(posts).toEqual([]);
  expect(JSON.stringify(output)).not.toContain(notes);
  writeFileSync(
    "../evidence/block07-privacy-" + data.snapshot.oracle + ".json",
    JSON.stringify(
      {
        oracle: data.snapshot.oracle,
        storageBeforeSave: null,
        stored,
        exported: output,
        reopenPostRequests: posts,
      },
      null,
      2,
    ) + "\n",
  );
}
test("opening Lenormand line shows five actual cards and their original illustrations", async ({
  page,
}) => {
  await room(page, "oracle");
  await page.getByRole("button", { name: "Five", exact: true }).click();
  const native = await report(page, "Draw the oracle cards");
  expect(new Set(native.snapshot.values).size).toBe(5);
  for (let i = 0; i < 5; i++) {
    await page
      .getByRole("button", { name: "Reveal card " + (i + 1), exact: true })
      .click();
    const expected = native.snapshot.values[i];
    await expect(page.locator(".oracle-card").nth(i)).toHaveAttribute(
      "data-card",
      expected,
    );
    await expect(
      page.locator(".oracle-card").nth(i).locator("img"),
    ).toHaveAttribute("src", "/art/ritual-deck/" + expected + ".webp");
  }
  await expect(page.locator(".oracle-reading h2")).toBeVisible();
  await save(page, native);
  await expect(page.locator(".ritual-folio [data-card]")).toHaveCount(5);
});
test("Pendulum motion model does not feed either native response mode", async ({
  page,
}) => {
  await room(page, "pendulum");
  await page
    .getByRole("button", { name: "Swing the display model", exact: true })
    .click();
  expect(
    await page
      .locator(".pendulum-rig")
      .evaluate((e) => e.getAnimations().length),
  ).toBeGreaterThan(0);
  const generated = await report(page, "Draw a digital symbol");
  expect(generated.snapshot.values[0]).toBe("seeded");
  expect((generated.result as any).generated_signal).toBeNull();
  await expect(
    page.getByText("Seeded digital symbol", { exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: /Start a fresh visit/ }).click();
  await page
    .getByRole("button", { name: "My observed movement", exact: true })
    .click();
  await page.getByLabel("My yes movement").selectOption("vertical");
  await page.getByLabel("My no movement").selectOption("horizontal");
  await page.getByLabel("Movement observed").selectOption("vertical");
  await page.getByLabel("Observation quality").selectOption("partial");
  const manual = await report(page, "Read my reported movement");
  expect(manual.snapshot.values).toEqual(["manual", "unresolved"]);
  await expect(page.locator(".pendulum-answer h2")).toHaveText("Unresolved");
  await save(page, manual);
});
for (const [slug, oracle] of [
  ["crystal", 21],
  ["mirror", 22],
] as const) {
  test(
    slug + " journal preserves user authorship and saves the guide only",
    async ({ page }) => {
      await room(page, slug);
      await page.locator(".ritual-glass").scrollIntoViewIfNeeded();
      await expect(page.locator(".ritual-glass")).toHaveAttribute(
        "data-renderer",
        "volumetric",
        { timeout: 12000 },
      );
      await page
        .getByRole("button", { name: "Open my journal", exact: true })
        .click();
      await page.getByLabel("My own observation").fill(notes);
      await page
        .getByLabel("How I describe it")
        .selectOption("observed_reflection");
      const native = await report(page, "Close the journal");
      expect(native.snapshot.oracle).toBe(oracle);
      expect(native.snapshot.values).toEqual([]);
      expect((native.result as any).perception_detected).toBe(false);
      await expect(page.locator(".private-quote")).toContainText(notes);
      await save(page, native);
      await expect(page.locator(".ritual-folio")).not.toContainText(notes);
      await expect(page.locator(".ritual-folio")).toContainText(
        "This bookmark keeps the reference guide only.",
      );
    },
  );
}
test("Dream references follow explicit choices and omit private journal material", async ({
  page,
}) => {
  await room(page, "dream");
  await page
    .getByLabel("My dream notes")
    .fill(notes + " I saw a serpent and remembered a meal.");
  await page.getByRole("button", { name: "Eating", exact: true }).click();
  await page.getByLabel("Were you hungry?").selectOption("yes");
  const native = await report(page, "Open my selected references");
  expect(native.snapshot.values).toEqual(["eating"]);
  await expect(page.locator("[data-motif=eating]")).toContainText(
    "Matches chosen context",
  );
  await expect(page.locator("[data-motif=serpent]")).toHaveCount(0);
  await save(page, native);
  await expect(page.locator(".ritual-folio")).toContainText(
    "Reference bookmark",
  );
  await expect(page.locator(".ritual-folio")).not.toContainText(notes);
});
test("Geomancy builds fifteen exact figures from untouched manual Mothers", async ({
  page,
}) => {
  await room(page, "geomancy");
  await expect(
    page.getByRole("button", { name: "Form the shield" }),
  ).toBeDisabled();
  const mothers = ["1212", "2112", "1122", "2121"];
  for (let m = 0; m < 4; m++)
    for (let row = 0; row < 4; row++) {
      const button = page.getByRole("button", {
        name: new RegExp("^Mother " + (m + 1) + ", row " + (row + 1) + ":"),
      });
      for (let n = 0; n < Number(mothers[m][row]); n++) await button.click();
    }
  const native = await report(page, "Form the shield");
  expect(native.snapshot.values.slice(0, 4)).toEqual(mothers);
  expect(native.snapshot.values).toHaveLength(15);
  for (const [i, pattern] of native.snapshot.values.entries())
    await expect(
      page.locator('[data-position="' + (i + 1) + '"]'),
    ).toHaveAttribute("data-pattern", pattern);
  await page.getByText("Trace the rows and parents", { exact: true }).click();
  await expect(page.locator(".shield-view details ol li")).toHaveCount(4);
  await save(page, native);
  await expect(page.locator(".ritual-folio .shield-figure")).toHaveCount(15);
});
test("Bibliomancy requires a deliberate pinned sentence selection", async ({
  page,
}) => {
  await room(page, "bibliomancy");
  await expect(
    page.getByRole("button", { name: "Read this passage" }),
  ).toBeDisabled();
  await page.getByRole("button", { name: "Ruth 2", exact: true }).click();
  expect(
    await page
      .locator(".book-selection button")
      .evaluateAll((rows) =>
        rows.every((row) => row.scrollHeight <= row.clientHeight + 1),
      ),
  ).toBeTruthy();
  await page.locator(".book-selection button").nth(3).click();
  await page.getByLabel("Nearby sentences on each side").selectOption("2");
  const native = await report(page, "Read this passage");
  const chosen = native.result.selections![0];
  expect(native.snapshot.values).toEqual(["2", chosen.sentence_id]);
  await expect(page.locator(".book-leaf blockquote")).toHaveText(chosen.text);
  await save(page, native);
  await expect(page.locator(".ritual-folio .book-leaf blockquote")).toHaveText(
    chosen.text,
  );
});
test("Ritual Wing navigation, narrow screens, reduced motion and glass fallback", async ({
  page,
}) => {
  await page.setViewportSize({ width: 320, height: 744 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/#gallery");
  await page.getByText("The Ritual Wing", { exact: false }).first().click();
  await page
    .getByRole("navigation", { name: "The Ritual Wing rooms" })
    .getByRole("link", { name: /Crystal Ball/ })
    .click();
  await expect(page.locator(".ritual-intro h1")).toHaveText(
    "The Veil of Glass",
  );
  for (const slug of [
    "oracle",
    "pendulum",
    "crystal",
    "mirror",
    "dream",
    "geomancy",
    "bibliomancy",
  ]) {
    await room(page, slug);
    await expect(page.locator(".ritual-room")).toHaveAttribute(
      "data-ritual-still",
      "true",
    );
    await expect(page.locator(".ritual-room canvas")).toHaveCount(0);
    const stage = page.locator(".ritual-stage");
    expect(
      await stage.evaluate(
        (e) => e.scrollWidth <= Math.ceil(e.getBoundingClientRect().width),
      ),
    ).toBeTruthy();
    const audit = await new AxeBuilder({ page })
      .include(".ritual-room")
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(
      audit.violations.map((v) => [v.id, v.nodes.map((n) => n.target)]),
    ).toEqual([]);
  }
  await page.emulateMedia({ reducedMotion: "no-preference" });
  await page.addInitScript(() => {
    const getContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (type, ...args) {
      if (String(type).startsWith("webgl")) return null;
      return Reflect.apply(getContext, this, [type, ...args]);
    } as typeof getContext;
  });
  await room(page, "mirror");
  await page.reload();
  await expect(page.locator(".ritual-glass")).toHaveAttribute(
    "data-renderer",
    "static",
  );
  await report(page, "Finish without an entry");
  await expect(page.locator(".journal-reading h2")).toHaveText(
    "An open, unmarked page",
  );
});
