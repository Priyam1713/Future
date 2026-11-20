import { test, expect, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { writeFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";

const shots = "../screenshots";
mkdirSync(shots, { recursive: true });
async function noOverflow(page: Page) {
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBeTruthy();
  expect(
    await page
      .locator("main button, main input, main textarea, main summary")
      .evaluateAll((elements) =>
        elements
          .filter((el) => {
            const r = el.getBoundingClientRect();
            return r.width > 0 && (r.left < -0.5 || r.right > innerWidth + 0.5);
          })
          .map((el) => el.textContent?.slice(0, 60)),
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
async function start(page: Page) {
  await page.goto("/");
  await page
    .getByRole("button", { name: "Begin a reading", exact: true })
    .click();
}
async function draw(page: Page, one = false) {
  if (one) await page.getByRole("radio", { name: /One card/ }).check();
  await page
    .getByLabel("What’s on your mind?")
    .fill("What themes might help me reflect on a creative project?");
  const pending = page.waitForResponse((r) =>
    r.url().endsWith("/api/readings"),
  );
  await page
    .getByRole("button", { name: one ? "Draw my card" : "Draw my three cards" })
    .click();
  const response = await pending;
  expect(response.status()).toBe(200);
  return response.json();
}

test("mobile complete real three-card journey, progressive reveal, source details and native export", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  await page.goto("/");
  await expect(page.locator(".orb")).toHaveAttribute("data-renderer", "pixi", {
    timeout: 20000,
  });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: `${shots}/01-explore-mobile.png`,
    fullPage: true,
  });
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: `${shots}/01-explore-viewport.png`,
  });
  await noOverflow(page);
  await accessible(page);
  await page.locator("h1").focus();
  await page
    .getByRole("button", { name: "Begin a reading", exact: true })
    .click();
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: `${shots}/02-intention-mobile.png`,
    fullPage: true,
  });
  await accessible(page);
  await page.locator("h1").focus();
  const envelope = await draw(page);
  const native = envelope.result;
  expect(native.factual_prediction).toBe(false);
  expect(native.profile).toBe("waite-1922-text-v1");
  expect(native.readings).toHaveLength(3);
  for (let i = 0; i < 3; i++) {
    await page
      .getByRole("button", { name: `Reveal card ${i + 1}`, exact: true })
      .click();
    await expect(
      page.getByRole("button", {
        name: `${native.readings[i].card.name}, ${native.readings[i].orientation}`,
        exact: true,
      }),
    ).toHaveAttribute("aria-pressed", "true");
  }
  await expect(page.getByRole("status")).toHaveText(
    "Your cards are open.",
  );
  await page.waitForTimeout(850);
  await page.evaluate(() => (document.activeElement as HTMLElement)?.blur());
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: `${shots}/03-reveal-mobile.png`,
    fullPage: true,
  });
  await noOverflow(page);
  await accessible(page);
  await page.getByRole("button", { name: "Open my reading" }).click();
  await page.getByRole("link", { name: "Skip to content" }).focus();
  await page.keyboard.press("Enter");
  await expect(page.locator("main")).toBeFocused();
  await expect(
    page.getByRole("heading", { name: "The story in your cards." }),
  ).toBeVisible();
  for (const r of native.readings) {
    await expect(
      page.locator(".theme-row").filter({ hasText: r.position.label }),
    ).toContainText(r.direct_component.symbolic_focus.split(";").join(" · "));
  }
  await page
    .locator(".interpretation")
    .first()
    .getByText("The traditional meaning", { exact: true })
    .click();
  await expect(page.locator("blockquote").first()).toHaveText(
    native.readings[0].direct_component.text,
  );
  if (native.readings[0].upright_reference)
    await expect(page.locator(".interpretation").first()).toContainText(
      native.readings[0].upright_reference.text,
    );
  await page.evaluate(() => (document.activeElement as HTMLElement)?.blur());
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: `${shots}/04-reading-mobile.png`,
    fullPage: true,
  });
  await noOverflow(page);
  await accessible(page);
  const downloading = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export native reading" }).click();
  const file = await downloading;
  const exported = JSON.parse(readFileSync((await file.path())!, "utf8"));
  expect(exported.replay).toEqual(native.replay);
  expect(exported.readings).toEqual(native.readings);
  const replay = await page.request.post("/api/readings", {
    data: {
      spread: native.spread,
      seed: native.replay.seed,
      question: native.question,
      reversals: true,
    },
  });
  expect((await replay.json()).result).toEqual(native);
  writeFileSync(
    "../engine-browser-evidence.json",
    JSON.stringify(
      {
        scope:
          "Real native engine, browser-generated random seed; software verification only",
        result: native,
      },
      null,
      2,
    ),
  );
  await page.getByRole("button", { name: "Begin another chapter" }).click();
  await expect(
    page.getByRole("button", { name: "Draw my three cards" }),
  ).toBeVisible();
  expect(errors).toEqual([]);
});

test("one card, immediate result, upright-only, back navigation and no automatic AI", async ({
  page,
}) => {
  let cloud = 0;
  page.on("request", (r) => {
    if (r.url().endsWith("/api/explain")) cloud++;
  });
  await start(page);
  await page.getByLabel("Include reversed cards").uncheck();
  const native = (await draw(page, true)).result;
  expect(native.readings[0].orientation).toBe("upright");
  await page.getByRole("button", { name: "Skip reveal & read now" }).click();
  await expect(
    page.getByRole("heading", { name: "The story in your cards." }),
  ).toBeVisible();
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: `${shots}/05-one-card-mobile.png`,
    fullPage: true,
  });
  await page.goBack();
  await expect(
    page.getByRole("button", {
      name: `${native.readings[0].card.name}, upright`,
      exact: true,
    }),
  ).toHaveAttribute("aria-pressed", "true");
  expect(cloud).toBe(0);
});

test("retry preserves question and seed, rapid taps send one draw", async ({
  page,
}) => {
  await start(page);
  const seeds: string[] = [];
  let requests = 0;
  await page.route("**/api/readings", async (route) => {
    requests++;
    seeds.push(route.request().postDataJSON().seed);
    if (requests === 1)
      await route.fulfill({
        status: 503,
        contentType: "application/json",
        body: JSON.stringify({
          detail: "Connection interrupted. Please retry.",
        }),
      });
    else {
      await new Promise((r) => setTimeout(r, 300));
      await route.continue();
    }
  });
  await page.getByLabel("What’s on your mind?").fill("My question stays here.");
  await page.getByRole("button", { name: "Draw my three cards" }).click();
  await expect(page.getByRole("alert")).toContainText("Please retry");
  await expect(page.getByLabel("What’s on your mind?")).toHaveValue(
    "My question stays here.",
  );
  const button = page.getByRole("button", { name: "Draw my three cards" });
  await button.evaluate((el: HTMLButtonElement) => {
    el.click();
    el.click();
    el.click();
  });
  await expect(
    page.getByRole("button", { name: "Reveal card 1" }),
  ).toBeVisible();
  expect(requests).toBe(2);
  expect(seeds[0]).toBe(seeds[1]);
});

test("living Pixi fog moves, responds to touch, and pauses for reduced motion", async ({
  page,
}) => {
  await page.goto("/");
  const orb = page.locator(".orb");
  await expect(orb).toHaveAttribute("data-renderer", "pixi", {
    timeout: 20000,
  });
  await page.waitForTimeout(1200);
  const a = await orb.screenshot();
  await page.waitForTimeout(700);
  const b = await orb.screenshot();
  expect(createHash("sha256").update(a).digest("hex")).not.toBe(
    createHash("sha256").update(b).digest("hex"),
  );
  const bounds = (await orb.boundingBox())!;
  await page.touchscreen.tap(
    bounds.x + bounds.width * 0.7,
    bounds.y + bounds.height * 0.4,
  );
  await page.waitForTimeout(200);
  await page
    .getByRole("button", { name: "Pause atmosphere", exact: true })
    .click();
  await page.waitForTimeout(650);
  const c = await orb.screenshot();
  await page.waitForTimeout(550);
  expect(await orb.screenshot()).toEqual(c);
  await page
    .getByRole("button", { name: "Resume atmosphere", exact: true })
    .click();
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.waitForTimeout(650);
  const d = await orb.screenshot();
  await page.waitForTimeout(550);
  expect(await orb.screenshot()).toEqual(d);
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: `${shots}/06-reduced-motion-mobile.png`,
    fullPage: true,
  });
});

test("sound off by default, independent levels, settings focus trap and keyboard dismissal", async ({
  page,
}) => {
  await page.goto("/");
  await page.getByRole("link", { name: "Skip to content" }).focus();
  await page.keyboard.press("Tab");
  await page.keyboard.press("Shift+Tab");
  await expect(
    page.getByRole("link", { name: "Skip to content" }),
  ).toBeFocused();
  expect(
    await page.locator(".skip").evaluate((el) => getComputedStyle(el).clipPath),
  ).toBe("none");
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("button", { name: "Enable sound" }),
  ).toHaveAttribute("aria-pressed", "false");
  await page.getByRole("button", { name: "About FATE and settings" }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog).toBeVisible();
  await accessible(page);
  await page.getByLabel("Ambient volume").fill("0.1");
  await page.getByLabel("Card & selection volume").fill("0.2");
  await page.getByRole("button", { name: "Turn on", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Mute sound" }),
  ).toHaveAttribute("aria-pressed", "true");
  for (let i = 0; i < 12; i++) await page.keyboard.press("Tab");
  expect(
    await page.evaluate(() => !!document.activeElement?.closest("dialog")),
  ).toBe(true);
  await page.keyboard.press("Escape");
  await expect(dialog).not.toBeVisible();
  await page.getByRole("button", { name: "Mute sound" }).click();
  await expect(
    page.getByRole("button", { name: "Enable sound" }),
  ).toHaveAttribute("aria-pressed", "false");
});

test("Gemini opt-in, native result retained after cloud failure, commentary visibly separate", async ({
  page,
}) => {
  await page.route("**/api/health", (r) =>
    r.fulfill({ json: { status: "ok", gemini_available: true } }),
  );
  await start(page);
  const native = (await draw(page, true)).result;
  await page.getByRole("button", { name: "Skip reveal & read now" }).click();
  const explain = page.getByRole("button", { name: "Explain my reading" });
  await expect(explain).toBeDisabled();
  let calls = 0;
  await page.route("**/api/explain", async (r) => {
    calls++;
    expect(r.request().postDataJSON().cloud_consent).toBe(true);
    if (calls === 1)
      await r.fulfill({
        status: 503,
        json: {
          detail: "Cloud unavailable. Your native reading is still available.",
        },
      });
    else
      await r.fulfill({
        json: {
          cards: native.readings.map((x: any) => ({
            card_id: x.card.id,
            rule_id: x.direct_component.rule_id,
            reflection:
              "Test commentary grounded in the supplied symbolic motifs.",
          })),
          provenance: { provider: "gemini", model: "browser-test-double" },
          coverage: "experimental_ai_commentary",
        },
      });
  });
  await page.getByRole("checkbox", { name: /I agree to send/ }).check();
  await explain.click();
  await expect(page.getByRole("alert")).toContainText("Cloud unavailable");
  await expect(page.locator(".interpretation h2").first()).toHaveText(
    native.readings[0].card.name,
  );
  await explain.click();
  await expect(page.locator(".commentary")).toContainText(
    "browser-test-double",
  );
  expect(calls).toBe(2);
});

test("320px, 430px, tablet, desktop and 200% text layouts", async ({
  page,
}) => {
  for (const width of [320, 430, 768, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto("/");
    await page.evaluate(() => document.fonts.ready);
    await noOverflow(page);
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    if (width === 1440)
      await page.screenshot({
        animations: "disabled",
        scale: "css",
        path: `${shots}/07-explore-desktop.png`,
        fullPage: true,
      });
  }
  await page.setViewportSize({ width: 320, height: 740 });
  await page.goto("/");
  await page
    .getByRole("button", { name: "Begin a reading", exact: true })
    .click();
  await noOverflow(page);
  await draw(page);
  await noOverflow(page);
  await page.getByRole("button", { name: "Skip reveal & read now" }).click();
  await noOverflow(page);
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: `${shots}/08-reading-small-mobile.png`,
    fullPage: true,
  });
  await page.evaluate(() => {
    const elements = [
      ...document.querySelectorAll<HTMLElement>("main *"),
    ].filter((el) => el instanceof HTMLElement);
    const sizes = elements.map((el) =>
      parseFloat(getComputedStyle(el).fontSize),
    );
    elements.forEach((el, i) => (el.style.fontSize = `${sizes[i] * 2}px`));
  });
  await noOverflow(page);
  await page.screenshot({
    animations: "disabled",
    scale: "css",
    path: `${shots}/09-enlarged-text-mobile.png`,
    fullPage: true,
  });
});

test("artwork fallback still permits a real reading without WebGL", async ({
  page,
}) => {
  await page.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (
      this: HTMLCanvasElement,
      ...args: any[]
    ) {
      if (String(args[0]).startsWith("webgl")) return null;
      return original.apply(this, args as any);
    } as typeof original;
  });
  await page.goto("/");
  await expect(page.locator(".orb-fallback img").first()).toBeVisible();
  await page
    .getByRole("button", { name: "Begin a reading", exact: true })
    .click();
  const native = (await draw(page, true)).result;
  await page.getByRole("button", { name: "Skip reveal & read now" }).click();
  await expect(page.locator(".interpretation h2")).toHaveText(
    native.readings[0].card.name,
  );
});

test("local mobile performance observation and asset health", async ({
  page,
}) => {
  await page.addInitScript(() => {
    (window as any).__metrics = { lcp: 0, cls: 0, longTasks: [] };
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      (window as any).__metrics.lcp = entries.at(-1)?.startTime;
    }).observe({ type: "largest-contentful-paint", buffered: true });
    new PerformanceObserver((list) => {
      for (const e of list.getEntries() as any) {
        if (!e.hadRecentInput) (window as any).__metrics.cls += e.value;
      }
    }).observe({ type: "layout-shift", buffered: true });
    new PerformanceObserver((list) => {
      (window as any).__metrics.longTasks.push(
        ...list.getEntries().map((e) => e.duration),
      );
    }).observe({ type: "longtask", buffered: true });
  });
  const failures: string[] = [];
  page.on("response", (r) => {
    if (r.status() >= 400) failures.push(`${r.status()} ${r.url()}`);
  });
  await page.goto("/");
  await expect(page.locator(".orb")).toHaveAttribute("data-renderer", "pixi", {
    timeout: 20000,
  });
  await page.waitForTimeout(1200);
  const metrics = await page.evaluate(async () => {
    const samples: number[] = [];
    let last = performance.now();
    await new Promise<void>((resolve) => {
      const frame = (t: number) => {
        samples.push(t - last);
        last = t;
        if (samples.length < 90) requestAnimationFrame(frame);
        else resolve();
      };
      requestAnimationFrame(frame);
    });
    return {
      ...(window as any).__metrics,
      rafMedianMs: samples.sort((a, b) => a - b)[45],
      heapObservation: (performance as any).memory
        ? {
            usedBytes: (performance as any).memory.usedJSHeapSize,
            totalBytes: (performance as any).memory.totalJSHeapSize,
            note: "Chromium coarse heap observation, not peak-memory profiling",
          }
        : null,
      navigation: performance
        .getEntriesByType("navigation")
        .map((e) => e.toJSON()),
      resources: performance.getEntriesByType("resource").map((e) => ({
        name: e.name,
        transferSize: (e as PerformanceResourceTiming).transferSize,
        duration: e.duration,
      })),
    };
  });
  writeFileSync(
    "../performance.json",
    JSON.stringify(
      {
        environment:
          "Local Chromium mobile emulation, 390×844 DPR2; SwiftShader software WebGL, warm server, no network throttling. Not real-device CWV certification or INP.",
        ...metrics,
      },
      null,
      2,
    ),
  );
  expect(failures).toEqual([]);
  expect(metrics.cls).toBeLessThanOrEqual(0.1);
});
