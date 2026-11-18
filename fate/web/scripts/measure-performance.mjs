// A separate, quiet-browser observation, run after regression jobs finish.
// Host GPU/ANGLE identity is recorded rather than assuming hardware acceleration.
import { chromium } from "playwright";
import { mkdirSync, writeFileSync } from "node:fs";
const base = process.env.FATE_CAPTURE_URL || "http://127.0.0.1:8010";
const browser = await chromium.launch();
const profiles = [];
try {
  for (const profile of [
    {
      name: "mobile-host-renderer",
      width: 390,
      height: 844,
      dpr: 2,
      mobile: true,
      windows: 10,
    },
    {
      name: "desktop-host-renderer",
      width: 1440,
      height: 1000,
      dpr: 1,
      mobile: false,
      windows: 10,
    },
    {
      name: "low-power-capability-simulation",
      width: 390,
      height: 844,
      dpr: 2,
      mobile: true,
      low: true,
      windows: 6,
    },
    {
      name: "mobile-4x-cpu-1.6Mbps-150ms",
      width: 390,
      height: 844,
      dpr: 2,
      mobile: true,
      throttle: true,
      windows: 6,
    },
  ]) {
    const context = await browser.newContext({
      viewport: { width: profile.width, height: profile.height },
      deviceScaleFactor: profile.dpr,
      isMobile: profile.mobile,
      hasTouch: profile.mobile,
    });
    const page = await context.newPage();
    if (profile.low)
      await page.addInitScript(() => {
        Object.defineProperty(navigator, "hardwareConcurrency", {
          get: () => 4,
        });
        Object.defineProperty(navigator, "deviceMemory", { get: () => 4 });
      });
    await page.addInitScript(() => {
      window.__fateObservation = {
        lcpMs: null,
        cls: 0,
        longTasks: [],
        events: [],
      };
      new PerformanceObserver((list) => {
        window.__fateObservation.lcpMs = list.getEntries().at(-1)?.startTime;
      }).observe({ type: "largest-contentful-paint", buffered: true });
      new PerformanceObserver((list) => {
        for (const e of list.getEntries())
          if (!e.hadRecentInput) window.__fateObservation.cls += e.value;
      }).observe({ type: "layout-shift", buffered: true });
      new PerformanceObserver((list) =>
        window.__fateObservation.longTasks.push(
          ...list.getEntries().map((e) => e.duration),
        ),
      ).observe({ type: "longtask", buffered: true });
      new PerformanceObserver((list) =>
        window.__fateObservation.events.push(
          ...list
            .getEntries()
            .filter((e) => e.interactionId)
            .map((e) => ({
              name: e.name,
              durationMs: e.duration,
              processingDelayMs: e.processingStart - e.startTime,
            })),
        ),
      ).observe({ type: "event", durationThreshold: 16, buffered: true });
    });
    if (profile.throttle) {
      const cdp = await context.newCDPSession(page);
      await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
      await cdp.send("Network.enable");
      await cdp.send("Network.emulateNetworkConditions", {
        offline: false,
        latency: 150,
        downloadThroughput: (1.6 * 1024 * 1024) / 8,
        uploadThroughput: 75000,
      });
    }
    await page.goto(base);
    const orb = page.locator(".orb");
    await page
      .locator('.orb[data-renderer="pixi"]')
      .waitFor({ timeout: 45000 });
    const windows = [];
    for (let i = 0; i < profile.windows; i++) {
      await page.waitForTimeout(1000);
      const data = await orb.getAttribute("data-metrics");
      if (data) windows.push(JSON.parse(data));
    }
    const driver = await page.evaluate(() => {
      const canvas = document.createElement("canvas"),
        gl = canvas.getContext("webgl2") || canvas.getContext("webgl");
      if (!gl) return null;
      const info = gl.getExtension("WEBGL_debug_renderer_info");
      const value = {
        vendor: info
          ? gl.getParameter(info.UNMASKED_VENDOR_WEBGL)
          : gl.getParameter(gl.VENDOR),
        renderer: info
          ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL)
          : gl.getParameter(gl.RENDERER),
      };
      gl.getExtension("WEBGL_lose_context")?.loseContext();
      return value;
    });
    if (profile.mobile) {
      const r = await orb.boundingBox();
      await page.touchscreen.tap(r.x + r.width * 0.6, r.y + r.height * 0.5);
    } else await orb.click();
    await page
      .getByRole(profile.mobile ? "button" : "link", {
        name: profile.mobile ? "Begin a reading" : "Enter the oracle",
        exact: true,
      })
      .click();
    await page
      .getByRole("heading", { name: "Make room for a little clarity." })
      .waitFor();
    await page.waitForTimeout(700);
    const observation = await page.evaluate(() => ({
      ...window.__fateObservation,
      resources: performance
        .getEntriesByType("resource")
        .map((e) => ({
          name: e.name.split("/").pop(),
          transferBytes: e.transferSize,
          decodedBytes: e.decodedBodySize,
          durationMs: e.duration,
        })),
      heap: performance.memory
        ? {
            usedBytes: performance.memory.usedJSHeapSize,
            totalBytes: performance.memory.totalJSHeapSize,
          }
        : null,
    }));
    profiles.push({ profile, driver, windows, observation });
    console.log(
      profile.name,
      "LCP",
      Math.round(observation.lcpMs),
      "CLS",
      observation.cls,
      "last renderer",
      windows.at(-1)?.fps,
      windows.at(-1)?.quality,
    );
    await context.close();
  }
  mkdirSync("../evidence", { recursive: true });
  writeFileSync(
    "../evidence/host-performance.json",
    JSON.stringify(
      {
        scope:
          "Local Chromium host-renderer emulation. Driver identity recorded. CPU/network and low-power profiles are simulations, not physical-device, field CWV, battery/thermal or INP certification. Event durations are synthetic developer gestures; renderer callback intervals are distinct from presentation timing.",
        profiles,
      },
      null,
      2,
    ),
  );
} finally {
  await browser.close();
}
