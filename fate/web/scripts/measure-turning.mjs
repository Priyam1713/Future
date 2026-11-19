import { chromium } from "@playwright/test";
import { writeFileSync } from "node:fs";
import { enterTurning } from "./turning-helpers.mjs";
const browser = await chromium.launch();
const receipt = {
  date: "2026-11-19",
  browser: browser.version(),
  scope:
    "Quiet local Chromium emulation; native 7-day API calculation, no mocked ephemeris. RAF is main-thread scheduling, not presented compositor FPS or field INP. Automation timings include actionability.",
  profiles: [],
};
try {
  for (const profile of [
    { name: "mobile", width: 390, height: 844, dpr: 2 },
    { name: "desktop", width: 1440, height: 1000, dpr: 1 },
    {
      name: "mobile-low-capability",
      width: 390,
      height: 844,
      dpr: 2,
      low: true,
    },
    {
      name: "mobile-4x-1.6Mbps",
      width: 390,
      height: 844,
      dpr: 2,
      throttle: true,
    },
    { name: "mobile-reduced", width: 390, height: 844, dpr: 2, reduced: true },
  ]) {
    const c = await browser.newContext({
      viewport: { width: profile.width, height: profile.height },
      deviceScaleFactor: profile.dpr,
      isMobile: profile.width < 700,
      hasTouch: profile.width < 700,
      reducedMotion: profile.reduced ? "reduce" : "no-preference",
    });
    await c.addInitScript(
      ({ low }) => {
        if (low) {
          Object.defineProperty(navigator, "hardwareConcurrency", { value: 2 });
          Object.defineProperty(navigator, "deviceMemory", { value: 2 });
        }
        window.__turningMetrics = { cls: 0, longTasks: [] };
        new PerformanceObserver((l) => {
          for (const e of l.getEntries())
            if (!e.hadRecentInput) window.__turningMetrics.cls += e.value;
        }).observe({ type: "layout-shift", buffered: true });
        new PerformanceObserver((l) => {
          for (const e of l.getEntries())
            window.__turningMetrics.longTasks.push(e.duration);
        }).observe({ type: "longtask", buffered: true });
      },
      { low: profile.low },
    );
    const p = await c.newPage();
    if (profile.throttle) {
      const s = await c.newCDPSession(p);
      await s.send("Emulation.setCPUThrottlingRate", { rate: 4 });
      await s.send("Network.enable");
      await s.send("Network.emulateNetworkConditions", {
        offline: false,
        downloadThroughput: 200000,
        uploadThroughput: 94000,
        latency: 150,
      });
    }
    const start = Date.now();
    const native = await enterTurning(p);
    const journeyMs = Date.now() - start;
    await p
      .locator(".turning-layout")
      .evaluate((e) => e.scrollIntoView({ block: "start" }));
    const frames = p.evaluate(async () => {
      const xs = [];
      let last = performance.now();
      for (let i = 0; i < 240; i++) {
        const now = await new Promise(requestAnimationFrame);
        xs.push(now - last);
        last = now;
      }
      const a = xs.slice(2).sort((a, b) => a - b);
      return {
        samples: a.length,
        meanHz: 1000 / (a.reduce((a, b) => a + b, 0) / a.length),
        p95Ms: a[Math.floor(a.length * 0.95)],
        maxMs: a.at(-1),
      };
    });
    const changed = Date.now();
    await p.getByRole("button", { name: "Next day", exact: false }).click();
    await p.evaluate(
      () =>
        new Promise((r) =>
          requestAnimationFrame(() => requestAnimationFrame(r)),
        ),
    );
    const scrubMs = Date.now() - changed;
    const cadence = await frames;
    const metrics = await p.evaluate(() => ({
      ...window.__turningMetrics,
      canvases: document.querySelectorAll("canvas").length,
      heap: performance.memory?.usedJSHeapSize,
      renderState: document
        .querySelector(".time-instrument")
        ?.getAttribute("data-render-state"),
      resources: performance
        .getEntriesByType("resource")
        .map((r) => ({
          name: r.name.split("/").at(-1),
          bytes: r.transferSize,
          duration: r.duration,
        })),
    }));
    await p
      .getByRole("button", {
        name: "Save transit chapter to this device",
        exact: false,
      })
      .click();
    const savedBytes = await p.evaluate(
      () =>
        new TextEncoder().encode(localStorage.getItem("fate.codex.v1")).length,
    );
    receipt.profiles.push({
      profile,
      journeyMs,
      worker: native.result.computation,
      scrubMs,
      cadence,
      metrics,
      savedBytes,
    });
    console.log(profile.name, {
      scrubMs,
      p95: cadence.p95Ms,
      cls: metrics.cls,
      savedBytes,
    });
    await c.close();
  }
  writeFileSync(
    "../evidence/turning-performance.json",
    JSON.stringify(receipt, null, 2) + "\n",
  );
} finally {
  await browser.close();
}
