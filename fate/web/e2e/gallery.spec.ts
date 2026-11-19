import { test, expect, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { writeFileSync, readFileSync } from "node:fs";
const input = {
  name: "Ada Lovelace",
  birth: "1815-12-10",
  target: "2026-11-19",
  basis: "birth",
  y_roles: "",
};
async function enter(page: Page) {
  await page.goto("/");
  await page
    .getByRole("button", { name: "Explore Numerology", exact: true })
    .click();
  await expect(page.locator(".number-form")).toBeVisible();
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(650);
}
async function fill(page: Page) {
  await page.getByLabel("Your full name").fill(input.name);
  await page.getByLabel("Date of birth", { exact: true }).fill(input.birth);
  await page.getByLabel("Date to explore").fill(input.target);
}
async function cast(page: Page) {
  await fill(page);
  const response = page.waitForResponse((r) =>
    r.url().endsWith("/api/numerology"),
  );
  await page.getByRole("button", { name: "Awaken my numbers" }).click();
  return (await response).json();
}
async function geometry(page: Page) {
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBeTruthy();
  expect(
    await page
      .locator("main button, main input, main select, main summary")
      .evaluateAll((nodes) =>
        nodes
          .filter((el) => {
            const r = el.getBoundingClientRect();
            return r.width > 0 && (r.left < -0.5 || r.right > innerWidth + 0.5);
          })
          .map((el) => el.textContent),
      ),
  ).toEqual([]);
}
async function accessible(page: Page) {
  const result = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(
    result.violations.map((v) => ({
      id: v.id,
      nodes: v.nodes.map((n) => n.target),
    })),
  ).toEqual([]);
}

test("gallery projects all 54 retained methods, separates availability and searches real variations", async ({
  page,
}) => {
  await page.goto("/");
  const ids = await page
    .locator("[data-technique-id]")
    .evaluateAll((nodes) =>
      nodes.map((n) => Number(n.getAttribute("data-technique-id"))),
    );
  expect(ids).toHaveLength(54);
  expect(new Set(ids).size).toBe(54);
  for (const excluded of [25, 27, 41, 42, 47, 48])
    expect(ids).not.toContain(excluded);
  await page
    .getByRole("searchbox", { name: "Find a tradition" })
    .fill("phrenology");
  await page.locator('[data-technique-id="10"]>summary').click();
  await expect(page.locator('[data-technique-id="10"]')).toContainText(
    "Historical reference",
  );
  await expect(page.locator('[data-technique-id="10"]')).toContainText(
    "Discredited",
  );
  expect(await page.locator('[data-technique-id="10"] button').count()).toBe(0);
  await page.getByRole("searchbox").fill("yarrow");
  await expect(page.locator('[data-technique-id="18"]')).toBeVisible();
  await page.getByRole("searchbox").fill("zzzzz");
  await expect(
    page.getByText("No tradition matches that search. Try another name."),
  ).toBeVisible();
  await page.getByRole("searchbox").fill("");
  await geometry(page);
});

test("complete mobile native Numerology ritual, exact export, session continuity and no automatic cloud", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  const cloud: string[] = [];
  page.on("request", (r) => {
    if (r.url().includes("explain")) cloud.push(r.url());
  });
  await enter(page);
  await accessible(page);
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: "../screenshots/21-numerology-input-mobile.png",
    fullPage: true,
  });
  const envelope = await cast(page);
  const result = envelope.result;
  expect(result.expression.result).toBe(9);
  expect(result.life_path.result).toBe(1);
  expect(result.cycles.year.result).toBe(5);
  await expect(page.locator(".dial-core strong")).toHaveText("9");
  await expect(page.locator(".seal-theme")).toHaveText(result.readings[0].text);
  await page.waitForTimeout(900);
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: "../screenshots/22-numerology-ritual-mobile.png",
    fullPage: true,
  });
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: "../screenshots/22-numerology-ritual-viewport.png",
  });
  await page.getByRole("button", { name: "Reveal the next seal" }).click();
  await expect(page.locator(".dial-core strong")).toHaveText("5");
  await page.getByRole("button", { name: "Reveal the next seal" }).click();
  await expect(page.locator(".dial-core strong")).toHaveText("1");
  await page.getByRole("button", { name: "Read my constellation" }).click();
  await expect(page.locator(".number-themes")).toContainText(
    result.readings[0].text.replace(/\.$/, ""),
  );
  await expect(page.locator(".number-themes")).toContainText(
    result.readings[1].text.replace(/\.$/, ""),
  );
  await page.locator(".number-calculations>summary").click();
  await expect(page.locator(".number-calculations")).toContainText(
    "does not supply direct number-specific interpretations",
  );
  await accessible(page);
  await geometry(page);
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: "../screenshots/23-numerology-reading-mobile.png",
    fullPage: true,
  });
  const pending = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export native reading" }).click();
  const download = await pending;
  expect(JSON.parse(readFileSync((await download.path())!, "utf8"))).toEqual(
    result,
  );
  expect(
    (await (await page.request.post("/api/numerology", { data: input })).json())
      .result,
  ).toEqual(result);
  writeFileSync(
    "../evidence/numerology-engine.json",
    JSON.stringify(
      {
        scope:
          "Real browser request and exact native export; public historical example, no private visitor data",
        input,
        result,
      },
      null,
      2,
    ),
  );
  expect(cloud).toEqual([]);
  await page
    .getByRole("button", { name: "Return to the Gallery", exact: true })
    .click();
  await expect(
    page.getByText("1 of 3 rooms explored this visit"),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Explore Numerology", exact: true })
    .click();
  await expect(page.getByLabel("Your full name")).toHaveValue("");
  await page.getByRole("button", { name: "The Gallery", exact: false }).click();
  await page.reload();
  await expect(
    page.getByText("0 of 3 rooms explored this visit"),
  ).toBeVisible();
  expect(
    await page.evaluate(() => ({
      local: localStorage.length,
      session: sessionStorage.length,
    })),
  ).toEqual({ local: 0, session: 0 });
  expect(errors).toEqual([]);
});

test("Numerology preserves input on failure, guards double submit, requires every Y role and supports current names", async ({
  page,
}) => {
  await enter(page);
  await fill(page);
  await page.getByLabel("Your full name").fill("Amy Young");
  await page.getByRole("radio", { name: "Current name", exact: true }).check();
  await expect(page.getByRole("combobox")).toHaveCount(2);
  expect(
    await page
      .locator("form")
      .evaluate((form: HTMLFormElement) => form.checkValidity()),
  ).toBe(false);
  await page.getByRole("combobox").nth(0).selectOption("v");
  await page.getByRole("combobox").nth(1).selectOption("c");
  let attempts = 0;
  const requests: unknown[] = [];
  await page.route("**/api/numerology", async (route) => {
    attempts++;
    requests.push(route.request().postDataJSON());
    if (attempts === 1)
      await route.fulfill({
        status: 503,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Temporary connection failure" }),
      });
    else {
      await new Promise((resolve) => setTimeout(resolve, 300));
      await route.continue();
    }
  });
  await page.getByRole("button", { name: "Awaken my numbers" }).click();
  await expect(page.getByRole("alert")).toHaveText(
    "Temporary connection failure",
  );
  await expect(page.getByLabel("Your full name")).toHaveValue("Amy Young");
  await page
    .getByRole("button", { name: "Awaken my numbers" })
    .evaluate((b: HTMLButtonElement) => {
      b.click();
      b.click();
    });
  await expect(page.locator(".number-seal")).toBeVisible();
  expect(attempts).toBe(2);
  expect(requests[0]).toEqual(requests[1]);
  await page.getByRole("button", { name: "Go straight to my reading" }).click();
  await page.getByRole("button", { name: "Explore another name" }).click();
  await expect(page.getByLabel("Your full name")).toHaveValue("Amy Young");
});

test("dial live transforms, tactile keyboard turn, pause, initial reduced motion and low-power policy", async ({
  page,
}) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator, "hardwareConcurrency", { value: 4 });
    Object.defineProperty(navigator, "deviceMemory", { value: 4 });
  });
  await enter(page);
  const dial = page.locator(".number-dial");
  await dial.scrollIntoViewIfNeeded();
  await expect(dial).toHaveAttribute("data-quality", "low");
  await expect(dial).toHaveAttribute("data-render-state", "running");
  const ring = page.locator(".dial-brass");
  const first = await ring.evaluate((el) => getComputedStyle(el).transform);
  await page.waitForTimeout(500);
  expect(await ring.evaluate((el) => getComputedStyle(el).transform)).not.toBe(
    first,
  );
  await page.getByRole("button", { name: "Turn the celestial dial" }).focus();
  await page.keyboard.press("Enter");
  await expect(dial).toHaveCSS("--dial-turn", "23deg");
  await page.getByRole("button", { name: "About FATE and settings" }).click();
  await page
    .getByRole("dialog")
    .getByRole("button", { name: "Pause motion", exact: true })
    .click();
  await page.keyboard.press("Escape");
  await expect(dial).toHaveAttribute("data-render-state", "paused");
  await page.waitForTimeout(200);
  const stopped = await ring.evaluate((el) => getComputedStyle(el).transform);
  await page.waitForTimeout(400);
  expect(await ring.evaluate((el) => getComputedStyle(el).transform)).toBe(
    stopped,
  );
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.getByRole("button", { name: "About FATE and settings" }).click();
  await page
    .getByRole("dialog")
    .getByRole("button", { name: "Resume motion", exact: true })
    .click();
  await page.keyboard.press("Escape");
  await expect(dial).toHaveAttribute("data-render-state", "paused");
  const reducedBefore = await ring.evaluate(
    (el) => getComputedStyle(el).transform,
  );
  await page.getByRole("button", { name: "Turn the celestial dial" }).click();
  expect(await ring.evaluate((el) => getComputedStyle(el).transform)).not.toBe(
    reducedBefore,
  );
  await cast(page);
  await page.getByRole("button", { name: "Go straight to my reading" }).click();
  await expect(page.locator(".number-themes")).toBeVisible();
});

test("Numerology desktop composition, responsive geometry and separately consented commentary", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.route("**/api/health", (route) =>
    route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({ status: "ok", gemini_available: true }),
    }),
  );
  await page.goto("/");
  await page.waitForTimeout(1000);
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: "../screenshots/24-gallery-desktop.png",
    fullPage: true,
  });
  await page
    .getByRole("button", { name: "Explore Numerology", exact: true })
    .click();
  await expect(page.locator(".number-form")).toBeVisible();
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: "../screenshots/25-numerology-input-desktop.png",
    fullPage: true,
  });
  await cast(page);
  await page.waitForTimeout(600);
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: "../screenshots/26-numerology-ritual-desktop.png",
    fullPage: true,
  });
  await page.getByRole("button", { name: "Go straight to my reading" }).click();
  const commentary = page.getByRole("button", {
    name: "Request Gemini commentary",
  });
  await expect(commentary).toBeDisabled();
  let cloud = 0;
  await page.route("**/api/numerology/explain", (route) => {
    cloud++;
    return route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        themes: [
          {
            scope: "expression",
            source_id: "numerology-decoz-expression-v1",
            reflection: "Test commentary, separate from the native theme.",
          },
          {
            scope: "personal_year",
            source_id: "numerology-decoz-year-symbols-v1",
            reflection: "A separate reflection on the supplied annual theme.",
          },
        ],
        provenance: { provider: "gemini", model: "test-provider" },
        coverage: "experimental_ai_commentary",
      }),
    });
  });
  expect(cloud).toBe(0);
  await page.getByRole("checkbox", { name: /I consent/ }).check();
  await commentary.click();
  await expect(page.locator(".ai-commentary")).toContainText(
    "NOT NATIVE ENGINE OUTPUT",
  );
  expect(cloud).toBe(1);
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: "../screenshots/27-numerology-reading-desktop.png",
    fullPage: true,
  });
  await accessible(page);
  for (const width of [320, 430, 768, 1440]) {
    await page.setViewportSize({ width, height: 1000 });
    await geometry(page);
  }
  await page.setViewportSize({ width: 390, height: 844 });
  await page.addStyleTag({ content: "body{font-size:200%}" });
  await geometry(page);
});
