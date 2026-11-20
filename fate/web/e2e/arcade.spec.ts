import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { button, exchange } from "../scripts/future-journeys.mjs";

const dimensions = [
  [390, 844],
  [768, 1024],
  [1440, 900],
  [1920, 1080],
  [2560, 1440],
  [3440, 1440],
];

for (const [width, height] of dimensions) {
  test(`the Gallery and Play Hall fit ${width}×${height}`, async ({ page }) => {
    await page.setViewportSize({ width, height });
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/#gallery");
    await expect(page.locator(".world-door")).toHaveCount(6);
    await button(page, "The Tomorrow Machine").click();
    if (width >= 1000)
      await expect(
        page.getByRole("navigation", { name: "Switch worlds" }),
      ).toBeVisible();
    await expect(
      page.locator(".world-interior").locator("[data-technique-id]"),
    ).toHaveCount(12);
    await page.getByRole("link", { name: "Play", exact: true }).click();
    await expect(
      page.getByRole("heading", { name: "The Play Hall", exact: true }),
    ).toBeVisible({ timeout: 15000 });
    await expect(
      page.getByRole("navigation", { name: "Arcade games" }).locator("a"),
    ).toHaveCount(3);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBeTruthy();
    await page
      .getByRole("link", { name: "54 techniques", exact: true })
      .click();
    await expect(
      page.getByRole("heading", { name: "The Tomorrow Machine", exact: true }),
    ).toBeVisible();
  });
}

test("cell loom supports keyboard editing, exact native generations and replay", async ({
  page,
}) => {
  await page.goto("/#play-loom");
  await button(page, "Begin round").focus();
  await page.keyboard.press("Enter");
  const board = page.getByRole("group", { name: "Starting cell pattern" });
  // Focus starts somewhere on the instrument. Home plus four arrows selects the solution cell.
  const cell = board.getByRole("button", { name: "Cell 1,1", exact: true });
  await board.locator("button[tabindex='0']").focus();
  await page.keyboard.press("Home");
  await expect(cell).toBeFocused();
  for (let i = 0; i < 4; i++) await page.keyboard.press("ArrowRight");
  await page.keyboard.press("Space");
  await expect(
    board.getByRole("button", { name: "Cell 1,5", exact: true }),
  ).toHaveAttribute("aria-pressed", "true");
  const native = await exchange(page, "/api/future-study", () =>
    button(page, "Advance four generations").press("Enter"),
  );
  expect(native.wire).toMatchObject({ oracle: 54, option: 4 });
  expect(native.wire.cells[4]).toBe(1);
  expect(native.response.view.instrument.counts.at(-1)).toBe(6);
  await expect(
    page.getByRole("heading", { name: "6 living cells" }),
  ).toBeFocused();
  await expect(page.locator(".arcade-score")).toHaveText("100 / 100");
  await page.getByRole("slider", { name: /Generation/ }).press("Home");
  await expect(page.locator(".arcade-loom [data-alive=true]")).toHaveCount(6);
  await button(page, "Play next round").press("Enter");
  await expect(
    page.getByRole("heading", { name: "Keep 8 cells alive" }),
  ).toBeVisible();
});

test("touch selects a real circuit, reveals exact native bars and returns focus to its door", async ({
  page,
}) => {
  await page.goto("/#play");
  const link = page.getByRole("link", { name: /The Signal Switch/ });
  await link.tap();
  await button(page, "Begin round").tap();
  await expect(button(page, "Send the pulse")).toBeDisabled();
  await page.getByRole("button", { name: /Bell pair/ }).tap();
  const native = await exchange(page, "/api/future-study", () =>
    button(page, "Send the pulse").tap(),
  );
  expect(native.wire).toEqual({ oracle: 50, option: 0 });
  expect(native.response.view.instrument.bars[0].value).toBeCloseTo(0.5, 12);
  await expect(page.locator(".arcade-score")).toHaveText("100 / 100");
  await expect(page.locator(".circuit-outcomes dd b")).toHaveText([
    "50.0%",
    "0.0%",
    "0.0%",
    "50.0%",
  ]);
  await button(page, "Play hall").tap();
  await expect(link).toBeFocused();
});

test("sealed forecast uses actual native update and a separately sampled virtual outcome", async ({
  page,
}) => {
  await page.addInitScript(() => {
    const random = crypto.getRandomValues.bind(crypto);
    crypto.getRandomValues = ((array: Uint32Array) =>
      array instanceof Uint32Array && array.length === 1
        ? (array.fill(0), array)
        : random(array)) as typeof crypto.getRandomValues;
  });
  await page.goto("/#play-signal");
  await button(page, "Begin round").click();
  const dial = page.getByRole("slider", {
    name: "Your probability of a signal",
  });
  await dial.press("Home");
  for (let i = 0; i < 3; i++) await dial.press("PageUp");
  const chosen = Number(await dial.inputValue());
  const native = await exchange(page, "/api/future-study", () =>
    button(page, "Seal my forecast").click(),
  );
  expect(native.wire).toEqual({ oracle: 51, option: 0 });
  expect(native.response.view.instrument.bars[1].value).toBeCloseTo(3 / 7, 12);
  await expect(
    page.getByRole("heading", { name: "Signal received", exact: true }),
  ).toBeVisible();
  await expect(page.locator(".arcade-score")).toHaveText(
    Math.round(100 * (1 - (chosen / 100 - 1) ** 2)) + " / 100",
  );
  expect(await page.evaluate(() => Object.keys(localStorage))).toEqual([]);
});

test("a room round-trip keeps the Gallery query and restores the link focus", async ({
  page,
}) => {
  await page.goto("/#gallery");
  const query = page.getByRole("searchbox", { name: "Find a tradition" });
  await query.fill("lorenz");
  const link = page.getByRole("link", { name: "Enter Lorenz Chaos" });
  await link.click();
  await expect(page.locator(".future-room h1")).toHaveText(
    "The Lorenz Chamber",
    { timeout: 15000 },
  );
  await page.getByRole("button", { name: /Oracle Gallery/ }).click();
  await expect(query).toHaveValue("lorenz");
  await expect(link).toBeFocused();
});

test("desktop chart drag and scoped wheel rotate the instrument without changing native targets", async ({
  browser,
  baseURL,
}) => {
  const context = await browser.newContext({
    baseURL,
    viewport: { width: 1920, height: 1080 },
  });
  try {
    const page = await context.newPage();
    await page.goto("/#western");
    await page.getByLabel("Date of birth", { exact: true }).fill("1990-07-15");
    await page.getByLabel("Recorded birth time").fill("14:30");
    await page.getByLabel("Birth city", { exact: true }).fill("London GB");
    await button(page, "Find city").click();
    await page
      .getByRole("button", { name: /^London · GB/ })
      .first()
      .click();
    await page
      .getByLabel(
        "I’ve checked the coordinates and timezone for my birthplace.",
      )
      .check();
    await button(page, "Open my celestial chart").click();
    await button(page, "Skip reveal & read my chart").click();
    const grip = page.locator(".chart-grip");
    await grip.scrollIntoViewIfNeeded();
    const box = (await grip.boundingBox())!;
    const slider = page.getByRole("slider", { name: "Turn the instrument" });
    const moon = page.locator('[data-planet="Moon"]');
    const longitude = await moon.getAttribute("data-longitude");
    await page.mouse.move(box.x + 50, box.y + 20);
    await page.mouse.down();
    await page.mouse.move(box.x + 120, box.y + 20, { steps: 5 });
    await page.mouse.up();
    await expect(slider).toHaveValue("70");
    await page.keyboard.down("Shift");
    await page.mouse.wheel(0, 100);
    await page.keyboard.up("Shift");
    await expect(slider).toHaveValue("78");
    await expect(moon).toHaveAttribute("data-longitude", longitude!);
    await button(page, "Align Ascendant").click();
    await expect(slider).toHaveValue("0");
  } finally {
    await context.close();
  }
});

test("three mobile game instruments honor reduced motion and pass WCAG A and AA scans", async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  for (const hash of ["play-loom", "play-switch", "play-signal"]) {
    await page.goto("/#" + hash);
    await button(page, "Begin round").click();
    const report = await new AxeBuilder({ page })
      .include(".arcade")
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(
      report.violations.map(({ id, nodes }) => [
        id,
        nodes.map(({ target }) => target),
      ]),
    ).toEqual([]);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBeTruthy();
  }
});
