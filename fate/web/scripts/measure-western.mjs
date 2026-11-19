import { chromium } from "@playwright/test";
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { fillBirth, turnInstrument } from "./western-helpers.mjs";
process.chdir(fileURLToPath(new URL("../", import.meta.url)));
const browser = await chromium.launch();
const receipt = {
  date: "2026-11-19",
  browser: browser.version(),
  scope:
    "Isolated local Chromium emulation; RAF scheduling is not compositor FPS, physical-device performance or field INP. Synthetic QA moment. No native-response mocks.",
  definitions: {
    roomReadyMs:
      "Navigation to visible date input, decoded background and fonts, including automation",
    chartReadyMs:
      "Submit action start to native chart present and two animation frames, including automation and local server",
    selectionMs: "Planet button action to two animation frames; not field INP",
  },
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
    {
      name: "mobile-reduced-motion",
      width: 390,
      height: 844,
      dpr: 2,
      reduced: true,
    },
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
        window.__westernMetrics = { cls: 0, lcp: 0, longTasks: [], shifts: [] };
        new PerformanceObserver((l) => {
          for (const e of l.getEntries()) {
            if (!e.hadRecentInput) window.__westernMetrics.cls += e.value;
            window.__westernMetrics.shifts.push({
              value: e.value,
              recent: e.hadRecentInput,
              sources: e.sources.map((s) => ({
                tag: s.node?.tagName,
                className: String(s.node?.className),
              })),
            });
          }
        }).observe({ type: "layout-shift", buffered: true });
        new PerformanceObserver((l) => {
          for (const e of l.getEntries())
            window.__westernMetrics.lcp = e.startTime;
        }).observe({ type: "largest-contentful-paint", buffered: true });
        new PerformanceObserver((l) => {
          for (const e of l.getEntries())
            window.__westernMetrics.longTasks.push(e.duration);
        }).observe({ type: "longtask", buffered: true });
      },
      { low: profile.low },
    );
    const p = await c.newPage(),
      posts = [];
    p.on("request", (r) => {
      if (r.method() === "POST") posts.push(r.url());
    });
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
    await p.goto("http://127.0.0.1:8010/#western");
    await p.getByLabel("Date of birth", { exact: true }).waitFor();
    await p.locator(".western-environment img").evaluate((e) => e.decode());
    await p.evaluate(() => document.fonts.ready);
    const roomReadyMs = Date.now() - start;
    await fillBirth(p);
    const response = p.waitForResponse((r) => r.url().endsWith("/api/western"));
    const submitted = Date.now();
    await p
      .getByRole("button", { name: "Open my celestial chart", exact: true })
      .click();
    const native = (await (await response).json()).result;
    await p.locator('[data-planet="Sun"]').waitFor();
    await p.evaluate(
      () =>
        new Promise((r) =>
          requestAnimationFrame(() => requestAnimationFrame(r)),
        ),
    );
    const chartReadyMs = Date.now() - submitted;
    await p
      .getByRole("button", { name: "Skip reveal & read my chart" })
      .click();
    await p
      .locator(".western-chart-layout")
      .evaluate((e) => e.scrollIntoView({ block: "start" }));
    const frames = p.evaluate(async () => {
      const xs = [];
      let last = performance.now();
      for (let i = 0; i < 240; i++) {
        const now = await new Promise(requestAnimationFrame);
        xs.push(now - last);
        last = now;
      }
      const sorted = xs.slice(2).sort((a, b) => a - b);
      return {
        samples: sorted.length,
        meanHz: 1000 / (sorted.reduce((a, b) => a + b, 0) / sorted.length),
        p95Ms: sorted[Math.floor(sorted.length * 0.95)],
        maxMs: sorted.at(-1),
      };
    });
    const selected = Date.now();
    await p.getByRole("button", { name: "Explore Moon", exact: true }).click();
    await p.evaluate(
      () =>
        new Promise((r) =>
          requestAnimationFrame(() => requestAnimationFrame(r)),
        ),
    );
    const selectionMs = Date.now() - selected;
    await turnInstrument(p);
    const cadence = await frames;
    const liveRenderState = await p
      .locator(".birth-chart")
      .getAttribute("data-render-state");
    await p
      .getByRole("button", { name: "Save to this device", exact: true })
      .click();
    const saved = await p.evaluate(() => localStorage.getItem("fate.codex.v1"));
    const snapshotBytes = new TextEncoder().encode(saved).length;
    const metrics = await p.evaluate(() => ({
      ...window.__westernMetrics,
      canvases: document.querySelectorAll("canvas").length,
      heap: performance.memory?.usedJSHeapSize,
      renderState: document
        .querySelector(".birth-chart")
        ?.getAttribute("data-render-state"),
      resources: performance
        .getEntriesByType("resource")
        .map((r) => ({
          name: r.name.split("/").at(-1),
          bytes: r.transferSize,
          duration: r.duration,
        })),
    }));
    receipt.profiles.push({
      profile,
      roomReadyMs,
      chartReadyMs,
      selectionMs,
      cadence,
      liveRenderState,
      snapshotBytes,
      planets: Object.keys(native.planets).length,
      aspects: native.aspects.length,
      metrics,
      posts,
    });
    console.log(profile.name, {
      roomReadyMs,
      chartReadyMs,
      selectionMs,
      cls: metrics.cls,
      p95: cadence.p95Ms,
      snapshotBytes,
    });
    await c.close();
  }
  writeFileSync(
    "../evidence/western-performance.json",
    JSON.stringify(receipt, null, 2) + "\n",
  );
} finally {
  await browser.close();
}
