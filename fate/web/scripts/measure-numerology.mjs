import { chromium } from "@playwright/test";
import { writeFileSync } from "node:fs";
const browser = await chromium.launch();
const receipt = {
  date: "2026-11-19",
  browserVersion: browser.version(),
  timingDefinitions: {roomReadyMs:"Start of automated room click to visible input form, including actionability/route work",responseMs:"Start of automated submit click to response headers, including scrolling/actionability/network; not isolated engine CPU time"},
  scope:
    "Local Chromium emulation. RAF callback cadence observes main-thread scheduling, not hardware-presented compositor FPS or field INP. No physical-device or battery certification.",
  profiles: [],
};
try {
  for (const profile of [
    { name: "mobile", width: 390, height: 844, dpr: 2 },
    { name: "desktop", width: 1440, height: 1000, dpr: 1 },
    { name: "low-capability", width: 390, height: 844, dpr: 2, low: true },
    {
      name: "mobile-4x-1.6Mbps",
      width: 390,
      height: 844,
      dpr: 2,
      throttle: true,
    },
    { name: "reduced-motion", width: 390, height: 844, dpr: 2, reduced: true },
  ]) {
    const context = await browser.newContext({
      viewport: { width: profile.width, height: profile.height },
      deviceScaleFactor: profile.dpr,
      isMobile: profile.width < 700,
      hasTouch: profile.width < 700,
      reducedMotion: profile.reduced ? "reduce" : "no-preference",
    });
    if (profile.low)
      await context.addInitScript(() => {
        Object.defineProperty(navigator, "hardwareConcurrency", { value: 4 });
        Object.defineProperty(navigator, "deviceMemory", { value: 4 });
      });
    const page = await context.newPage();
    await page.addInitScript(() => {
      window.__numberMetrics = { cls: 0, longTasks: [], lcp: 0 };
      new PerformanceObserver((list) => {
        for (const e of list.getEntries())
          if (!e.hadRecentInput) window.__numberMetrics.cls += e.value;
      }).observe({ type: "layout-shift", buffered: true });
      new PerformanceObserver((list) => {
        for (const e of list.getEntries())
          window.__numberMetrics.longTasks.push(e.duration);
      }).observe({ type: "longtask", buffered: true });
      new PerformanceObserver((list) => {
        for (const e of list.getEntries())
          window.__numberMetrics.lcp = e.startTime;
      }).observe({ type: "largest-contentful-paint", buffered: true });
    });
    if (profile.throttle) {
      const cdp = await context.newCDPSession(page);
      await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
      await cdp.send("Network.enable");
      await cdp.send("Network.emulateNetworkConditions", {
        offline: false,
        downloadThroughput: 200000,
        uploadThroughput: 94000,
        latency: 150,
      });
    }
    await page.goto("http://127.0.0.1:8010");
    const entryStart = Date.now();
    await page.locator(".room-index button").nth(1).click();
    await page.locator(".number-form").waitFor();
    const roomReadyMs = Date.now() - entryStart;
    await page.getByLabel("Your full name").fill("Ada Lovelace");
    await page.getByLabel("Date of birth", { exact: true }).fill("1815-12-10");
    await page.getByLabel("Date to explore").fill("2026-11-19");
    const pending = page.waitForResponse((r) =>
      r.url().endsWith("/api/numerology"),
    );
    const requestStart = Date.now();
    await page.getByRole("button", { name: "Awaken my numbers" }).click();
    const response = await pending;
    const responseMs = Date.now() - requestStart;
    const native = await response.json();
    await page.locator(".number-seal").waitFor();
    await page.evaluate(() => scrollTo(0, 0));
    await page.waitForTimeout(700);
    const metrics = await page.evaluate(async () => {
      const times = [];
      let last = performance.now();
      for (let i = 0; i < 360; i++) {
        const now = await new Promise(requestAnimationFrame);
        times.push(now - last);
        last = now;
      }
      const sorted = [...times.slice(2)].sort((a, b) => a - b);
      const sum = sorted.reduce((a, b) => a + b, 0);
      const dial = document.querySelector(".number-dial");
      const rect = dial.getBoundingClientRect();
      return {
        ...window.__numberMetrics,
        raf: {
          frames: sorted.length,
          meanFps: 1000 / (sum / sorted.length),
          p50Ms: sorted[Math.floor(sorted.length * 0.5)],
          p95Ms: sorted[Math.floor(sorted.length * 0.95)],
          maxMs: sorted.at(-1),
        },
        dial: {
          ...dial.dataset,
          width: rect.width,
          layers: dial.querySelectorAll("*").length,
        },
        heap: performance.memory
          ? {
              usedBytes: performance.memory.usedJSHeapSize,
              totalBytes: performance.memory.totalJSHeapSize,
            }
          : null,
        resources: performance
          .getEntriesByType("resource")
          .map((r) => ({
            name: r.name.replace(location.origin, ""),
            transferBytes: r.transferSize,
            durationMs: r.duration,
          })),
        canvases: document.querySelectorAll("canvas").length,
        capabilities: {cores:navigator.hardwareConcurrency,memoryGiB:navigator.deviceMemory??null,dpr:devicePixelRatio,userAgent:navigator.userAgent},
      };
    });
    receipt.profiles.push({
      profile,
      roomReadyMs,
      responseMs,
      actualExpression: native.result.expression.result,
      metrics,
    });
    console.log(
      profile.name,
      "room",
      roomReadyMs,
      "native",
      responseMs,
      "RAF",
      metrics.raf.meanFps.toFixed(1),
      "p95",
      metrics.raf.p95Ms.toFixed(1),
      "CLS",
      metrics.cls,
    );
    await context.close();
  }
  writeFileSync(
    "../evidence/numerology-performance.json",
    JSON.stringify(receipt, null, 2),
  );
} finally {
  await browser.close();
}
