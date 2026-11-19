import { expect, test, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { writeFileSync } from "node:fs";

type Env = {
  snapshot: any;
  result: any;
};
async function loadRoom(page: Page, room: string) {
  await page.goto("/#" + room);
  await expect(page.locator(".chamber-" + room + " h1")).toBeVisible();
}
async function calculate(page: Page, button: string): Promise<Env> {
  const response = page.waitForResponse(
    (r) => r.url().endsWith("/api/chambers") && r.request().method() === "POST",
  );
  await page.getByRole("button", { name: button, exact: true }).click();
  const native = await response;
  expect(native.ok()).toBeTruthy();
  return native.json();
}
async function birth(page: Page, room: "vedic" | "bazi") {
  await loadRoom(page, room);
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
  if (room === "vedic")
    await page.getByLabel("Explore periods on this UTC day").fill("2026-11-20");
  return calculate(
    page,
    room === "vedic" ? "Open my sidereal charts" : "Open my Four Pillars",
  );
}
async function save(page: Page, native: Env) {
  expect(
    await page.evaluate(() => localStorage.getItem("fate.codex.v1")),
  ).toBeNull();
  await page
    .getByRole("button", {
      name: "Save chamber chapter to this device",
      exact: true,
    })
    .click();
  const raw = await page.evaluate(() => localStorage.getItem("fate.codex.v1"));
  if (!raw) throw new Error("No explicit chapter saved");
  const document = JSON.parse(raw);
  expect(document.chapters[0].snapshot).toEqual(native.snapshot);
  expect(document.chapters[0].reference).toBe("fate-four-chambers-v1");
  expect(raw).not.toMatch(
    /"(birth|local|zone|latitude|longitude|target|seed|replay|receipt|commentary|casting|question)"/,
  );
  const posts: string[] = [];
  page.on("request", (req) => {
    if (req.method() === "POST") posts.push(req.url());
  });
  await page
    .getByRole("button", { name: "Open in My Fate", exact: false })
    .click();
  await expect(page.locator(".chamber-folio")).toBeVisible();
  await page.reload();
  await page
    .getByRole("button", { name: "Open your Codex", exact: true })
    .click();
  await expect(page.locator(".chamber-folio")).toBeVisible();
  const event = page.waitForEvent("download");
  await page
    .getByRole("button", { name: "Export this chapter", exact: true })
    .click();
  const dl = await event,
    path = await dl.path();
  const { readFile } = await import("node:fs/promises");
  const exported = JSON.parse(await readFile(path!, "utf8"));
  expect(exported.chapters[0].snapshot).toEqual(native.snapshot);
  expect(exported.chapters[0].source_readings.length).toBeGreaterThan(0);
  expect(posts).toEqual([]);
  writeFileSync(
    `../evidence/block06-privacy-${native.snapshot.oracle}.json`,
    JSON.stringify(
      {
        oracle: native.snapshot.oracle,
        storageBeforeSave: null,
        stored: document,
        exported,
        reopenPostRequests: posts,
      },
      null,
      2,
    ) + "\n",
  );
}
test("Vedic D1 and D9 geometry, birth star and dasha controls round-trip through Codex", async ({
  page,
}) => {
  const native = await birth(page, "vedic");
  const longitudes = () =>
    page
      .locator("[data-graha]")
      .evaluateAll((nodes) =>
        Object.fromEntries(
          nodes.map((n) => [
            n.getAttribute("data-graha"),
            Number(n.getAttribute("data-longitude")),
          ]),
        ),
      );
  expect(await longitudes()).toEqual(
    Object.fromEntries(
      Object.entries(native.result.planets).map(
        ([name, row]: [string, any]) => [name, row.longitude],
      ),
    ),
  );
  await page.getByRole("button", { name: "D9 · Navamsa", exact: true }).click();
  expect(await longitudes()).toEqual(
    Object.fromEntries(
      Object.entries(native.result.d9.planets).map(
        ([name, row]: [string, any]) => [name, row.longitude_symbolic],
      ),
    ),
  );
  await page
    .getByRole("button", { name: "Reveal my birth star", exact: true })
    .click();
  await expect(page.locator(".moon-mansion")).toContainText(
    native.result.moon_nakshatra.name,
  );
  const sub = native.snapshot.sub.at(-1);
  await page.getByRole("button", { name: sub[0], exact: true }).last().click();
  await expect(page.locator(".dasha-rail .chamber-measure")).toContainText(
    sub[1],
  );
  await save(page, native);
  await page.getByRole("button", { name: "D9 · Navamsa", exact: true }).click();
  await expect(
    page.locator(".chamber-folio [data-graha=Moon]"),
  ).toHaveAttribute(
    "data-longitude",
    String(native.result.d9.planets.Moon.longitude_symbolic),
  );
});
test("Jade Hall shows native pillar characters, selected stem relationships and sourced Day Master", async ({
  page,
}) => {
  const native = await birth(page, "bazi");
  for (const [name, pillar] of Object.entries(native.result.pillars) as [
    string,
    any,
  ][]) {
    await expect(page.locator('[data-pillar="' + name + '"]')).toHaveAttribute(
      "data-pair",
      String(pillar.sexagenary_index),
    );
    await expect(page.locator('[data-pillar="' + name + '"]')).toContainText(
      pillar.branch.character,
    );
  }
  await expect(page.locator(".jade-reading")).toContainText(
    native.result.reading.day_master.text,
  );
  await page.getByRole("button", { name: /^month pillar/ }).click();
  await expect(page.locator(".jade-reading h3")).toHaveText(
    native.result.pillars.month.ten_god.name,
  );
  await save(page, native);
  await expect(page.locator(".chamber-folio .jade-reading h3")).toContainText(
    native.result.day_master.name,
  );
});
test("six native coin strokes reveal bottom-up, preserve values, and reopen the relating figure", async ({
  page,
}) => {
  await loadRoom(page, "iching");
  const native = await calculate(page, "Begin the six-line cast");
  const { calculation, replay } = native.result;
  for (let i = 0; i < 6; i++) {
    await page
      .getByRole("button", { name: "Cast line " + (i + 1), exact: true })
      .click();
    await expect(page.locator('[data-line="' + (i + 1) + '"]')).toHaveAttribute(
      "data-value",
      String(calculation.values[i]),
    );
    await expect(page.locator(".three-coins")).toHaveAttribute(
      "aria-label",
      replay.casting.raw[i]
        .map((bit: number) => (bit ? "Heads" : "Tails"))
        .join(", "),
    );
  }
  await expect(page.locator(".chamber-quote")).toHaveText(
    calculation.initial.judgment.text,
  );
  if (calculation.moving_lines.length) {
    await page
      .getByRole("button", { name: "Relating figure", exact: true })
      .click();
    for (const i of calculation.moving_lines) {
      await expect(page.locator('[data-line="' + i + '"]')).toHaveAttribute(
        "data-state",
        calculation.trace[i - 1].resulting_yang ? "yang" : "yin",
      );
    }
    await expect(page.locator(".chamber-quote")).toHaveText(
      calculation.resulting.judgment.text,
    );
  }
  await save(page, native);
  await expect(page.locator(".chamber-folio .ink-caption")).toContainText(
    calculation.initial.name,
  );
});
test("Elder Futhark stones reveal actual IDs, with history separate from modern prompts", async ({
  page,
}) => {
  await loadRoom(page, "runes");
  await page.getByRole("button", { name: "One rune", exact: true }).click();
  const one = await calculate(page, "Draw the runestones");
  await page.getByRole("button", { name: /Reveal stone 1/ }).click();
  expect(one.snapshot.runes).toHaveLength(1);
  await expect(page.locator(".rune-stone")).toHaveCount(1);
  await page.getByRole("button", { name: /Start a fresh draw/ }).click();
  await page.getByRole("button", { name: "Three runes", exact: true }).click();
  const three = await calculate(page, "Draw the runestones");
  for (let i = 0; i < 3; i++) {
    await page
      .getByRole("button", { name: new RegExp("Reveal stone " + (i + 1)) })
      .click();
    const r = three.result.readings[i];
    await expect(page.locator(".rune-stone").nth(i)).toHaveAttribute(
      "data-rune",
      r.rune.id,
    );
    await expect(page.locator(".rune-reading h3")).toHaveText(r.rune.name);
    await expect(page.locator(".rune-reading")).toContainText(
      r.rune.composition.reflection,
    );
  }
  await page
    .getByText("Historical and linguistic evidence", { exact: true })
    .click();
  await expect(page.locator(".rune-reading details a").first()).toBeVisible();
  await save(page, three);
  await expect(page.locator(".chamber-folio [data-rune]")).toHaveCount(3);
});
test("chambers fit small screens, support reduced motion and declare accessible reading controls", async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.setViewportSize({ width: 320, height: 740 });
  for (const room of ["vedic", "bazi", "iching", "runes"] as const) {
    if (room === "vedic" || room === "bazi") await birth(page, room);
    else {
      await loadRoom(page, room);
      await calculate(
        page,
        room === "iching" ? "Begin the six-line cast" : "Draw the runestones",
      );
    }
    const section = page.locator(".chamber-result");
    await expect(section).toBeVisible();
    expect(
      await page.locator(".chamber-room").getAttribute("data-motion"),
    ).toBe("still");
    expect(
      await section.evaluate(
        (e) => e.scrollWidth <= Math.ceil(e.getBoundingClientRect().width),
      ),
    ).toBeTruthy();
    const audit = await new AxeBuilder({ page })
      .include(".chamber-room")
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(
      audit.violations.map((x) => [x.id, x.nodes.map((n) => n.target)]),
    ).toEqual([]);
  }
});
