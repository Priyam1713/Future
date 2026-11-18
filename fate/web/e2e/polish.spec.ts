import { test, expect } from "@playwright/test";
import { writeFileSync, mkdirSync } from "node:fs";

test("initial reduced motion avoids Pixi, preference can resume, rapid navigation cleans up", async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  const sceneRequests: string[] = [];
  page.on("request", (request) => {
    if (request.url().includes("/assets/createOrbScene-"))
      sceneRequests.push(request.url());
  });
  await page.goto("/");
  await expect(page.locator(".orb-poster")).toBeVisible();
  await page.waitForTimeout(500);
  expect(sceneRequests).toEqual([]);
  await page.emulateMedia({ reducedMotion: "no-preference" });
  await expect(page.locator(".orb")).toHaveAttribute("data-renderer", "pixi", {
    timeout: 20000,
  });
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  for (let i = 0; i < 3; i++) {
    await page
      .getByRole("button", { name: "Begin a reading", exact: true })
      .click();
    await expect(page.locator(".orb canvas")).toHaveCount(0);
    await page.getByRole("button", { name: "Explore", exact: true }).click();
    if (i === 2)
      await expect(page.locator(".orb")).toHaveAttribute(
        "data-renderer",
        "pixi",
        { timeout: 20000 },
      );
  }
  await expect(page.locator(".orb canvas")).toHaveCount(1);
  expect(errors).toEqual([]);
});

test("low-power policy, pixel allocation and pause actually stop the rendered frames", async ({
  page,
}) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator, "hardwareConcurrency", { get: () => 4 });
    Object.defineProperty(navigator, "deviceMemory", { get: () => 4 });
  });
  await page.goto("/");
  const orb = page.locator(".orb");
  await expect(orb).toHaveAttribute("data-renderer", "pixi", {
    timeout: 20000,
  });
  await expect(orb).toHaveAttribute("data-quality", "low");
  await expect(orb).toHaveAttribute("data-target-fps", "30");
  await expect.poll(() => orb.getAttribute("data-metrics")).toBeTruthy();
  const before = JSON.parse((await orb.getAttribute("data-metrics"))!);
  expect(before.bufferWidth).toBeLessThanOrEqual(600);
  await page
    .getByRole("button", { name: "Pause atmosphere", exact: true })
    .click();
  await expect(orb).toHaveAttribute("data-render-state", "still");
  const metrics = await orb.getAttribute("data-metrics");
  await page.waitForTimeout(1200);
  expect(await orb.getAttribute("data-metrics")).toBe(metrics);
});

test("desktop journey and matched illustrated faces remain source-backed", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto("/");
  await expect(page.locator(".orb")).toHaveAttribute("data-renderer", "pixi", {
    timeout: 20000,
  });
  await page.getByRole("link", { name: "Enter the oracle" }).click();
  await page.waitForTimeout(650);
  await page.screenshot({
    path: "../screenshots/10-ritual-desktop.png",
    fullPage: true,
  });
  const pending = page.waitForResponse((r) =>
    r.url().endsWith("/api/readings"),
  );
  await page.getByRole("button", { name: "Draw my three cards" }).click();
  const native = (await (await pending).json()).result;
  await expect(page.locator("h1")).toHaveText("A moment of revelation.");
  for (let i = 0; i < 3; i++) {
    await expect(
      page.locator(`[data-artwork-id="${native.readings[i].card.id}"] img`),
    ).toHaveAttribute(
      "src",
      new RegExp(`${native.readings[i].card.id}-360.webp`),
    );
    await page
      .getByRole("button", { name: `Reveal card ${i + 1}`, exact: true })
      .click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: "../screenshots/11-reveal-desktop.png",
    fullPage: true,
  });
  await page.getByRole("button", { name: "Open my reading" }).click();
  await page.waitForTimeout(650);
  await page.screenshot({
    path: "../screenshots/12-reading-desktop.png",
    fullPage: true,
  });
});

test("render cadence and local mobile/desktop performance profiles", async ({
  page,
}) => {
  const profiles = [];
  for (const [name, width, height] of [
    ["mobile", 390, 844],
    ["desktop", 1440, 1000],
  ] as const) {
    await page.setViewportSize({ width, height });
    await page.goto("/");
    const orb = page.locator(".orb");
    await expect(orb).toHaveAttribute("data-renderer", "pixi", {
      timeout: 20000,
    });
    const windows = [];
    for (let i = 0; i < 6; i++) {
      await page.waitForTimeout(1000);
      const value = await orb.getAttribute("data-metrics");
      if (value) windows.push(JSON.parse(value));
    }
    const resources = await page.evaluate(() =>
      performance
        .getEntriesByType("resource")
        .map((e) => ({
          name: e.name.split("/").pop(),
          bytes: (e as PerformanceResourceTiming).transferSize,
          durationMs: e.duration,
        })),
    );
    profiles.push({ name, viewport: { width, height }, windows, resources });
  }
  mkdirSync("../evidence", { recursive: true });
  writeFileSync(
    "../evidence/render-performance.json",
    JSON.stringify(
      {
        environment:
          "Local Chromium 60 Hz mobile/desktop emulation, DPR2, SwiftShader software WebGL; renderer callbacks measured, not physical-device or field certification. Actual device quality starts from capabilities and may reduce during sustained missed budgets.",
        profiles,
      },
      null,
      2,
    ),
  );
  expect(profiles.every((p) => p.windows.length >= 4)).toBe(true);
});
