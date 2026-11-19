import { chromium } from "@playwright/test";
import { readFileSync, writeFileSync } from "node:fs";
const actual = JSON.parse(
  readFileSync("../evidence/codex-recording.json", "utf8"),
).persisted;
const browser = await chromium.launch();
const receipt = {
  date: "2026-11-19",
  browserVersion: browser.version(),
  scope:
    "Isolated local Chromium emulation. Seeded local records are the actual saved native snapshots from codex-recording.json; the 50-chapter stress profile repeats these snapshots with unique test IDs, not additional claimed native readings. RAF measures main-thread scheduling rather than hardware-presented compositor FPS or field INP.",
  timingDefinitions: {
    coverReadyMs: "Navigation start to cover image decoded and available",
    openReadyMs:
      "Automated cover click start to visible source content and two animation frames",
    turnReadyMs:
      "Automated Next click start to completed 720 ms intentional leaf transition; includes automation/actionability",
  },
  profiles: [],
};
try {
  for (const profile of [
    { name: "mobile-two-chapters", width: 390, height: 844, dpr: 2, count: 2 },
    {
      name: "desktop-50-chapters",
      width: 1440,
      height: 1000,
      dpr: 1,
      count: 50,
    },
    {
      name: "mobile-low-capability",
      width: 390,
      height: 844,
      dpr: 2,
      count: 50,
      low: true,
    },
    {
      name: "mobile-4x-1.6Mbps",
      width: 390,
      height: 844,
      dpr: 2,
      count: 50,
      throttle: true,
    },
    {
      name: "mobile-reduced-motion",
      width: 390,
      height: 844,
      dpr: 2,
      count: 2,
      reduced: true,
    },
  ]) {
    if (
      process.env.FATE_PERF_PROFILE &&
      profile.name !== process.env.FATE_PERF_PROFILE
    )
      continue;
    const c = await browser.newContext({
      viewport: { width: profile.width, height: profile.height },
      deviceScaleFactor: profile.dpr,
      isMobile: profile.width < 700,
      hasTouch: profile.width < 700,
      reducedMotion: profile.reduced ? "reduce" : "no-preference",
    });
    const document = {
      schemaVersion: 1,
      chapters: Array.from({ length: profile.count }, (_, i) => ({
        ...actual.chapters[i % actual.chapters.length],
        id: `${(i + 1).toString(16).padStart(8, "0")}-1111-4111-8111-111111111111`,
      })),
    };
    await c.addInitScript(
      ({ document, low }) => {
        localStorage.setItem("fate.codex.v1", JSON.stringify(document));
        if (low) {
          Object.defineProperty(navigator, "hardwareConcurrency", { value: 4 });
          Object.defineProperty(navigator, "deviceMemory", { value: 4 });
        }
        window.__codexMetrics = { cls: 0, lcp: 0, longTasks: [], shifts: [] };
        new PerformanceObserver((list) => {
          for (const e of list.getEntries()) {
            if (!e.hadRecentInput) window.__codexMetrics.cls += e.value;
            window.__codexMetrics.shifts.push({
              value: e.value,
              at: e.startTime,
              recent: e.hadRecentInput,
              sources: e.sources.map((s) => ({
                tag: s.node?.tagName,
                className: String(s.node?.className),
                previous: s.previousRect.toJSON(),
                current: s.currentRect.toJSON(),
              })),
            });
          }
        }).observe({ type: "layout-shift", buffered: true });
        new PerformanceObserver((list) => {
          for (const e of list.getEntries())
            window.__codexMetrics.lcp = e.startTime;
        }).observe({ type: "largest-contentful-paint", buffered: true });
        new PerformanceObserver((list) => {
          for (const e of list.getEntries())
            window.__codexMetrics.longTasks.push(e.duration);
        }).observe({ type: "longtask", buffered: true });
      },
      { document, low: profile.low },
    );
    const p = await c.newPage(),
      posts = [];
    p.on("request", (r) => {
      if (r.method() === "POST") posts.push(r.url());
    });
    if (profile.throttle) {
      const cdp = await c.newCDPSession(p);
      await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
      await cdp.send("Network.enable");
      await cdp.send("Network.emulateNetworkConditions", {
        offline: false,
        downloadThroughput: 200000,
        uploadThroughput: 94000,
        latency: 150,
      });
    }
    const start = Date.now();
    await p.goto("http://127.0.0.1:8010/#my-fate");
    await p.locator(".codex-cover img").evaluate((el) => el.decode());
    const coverReadyMs = Date.now() - start;
    const frames = p.evaluate(async () => {
      const samples = [];
      let last = performance.now();
      for (let i = 0; i < 360; i++) {
        const now = await new Promise(requestAnimationFrame);
        samples.push(now - last);
        last = now;
      }
      const sorted = samples.slice(2).sort((a, b) => a - b);
      return {
        frames: sorted.length,
        meanHz: 1000 / (sorted.reduce((a, b) => a + b, 0) / sorted.length),
        p50Ms: sorted[Math.floor(sorted.length * 0.5)],
        p95Ms: sorted[Math.floor(sorted.length * 0.95)],
        maxMs: sorted.at(-1),
      };
    });
    const opened = Date.now();
    await p.getByRole("button", { name: "Open your Codex" }).click();
    await p.locator(".codex-current").waitFor();
    await p.evaluate(
      () =>
        new Promise((resolve) =>
          requestAnimationFrame(() => requestAnimationFrame(resolve)),
        ),
    );
    const openReadyMs = Date.now() - opened;
    await p.waitForTimeout(950);
    const turn = Date.now();
    await p.getByRole("button", { name: "Next chapter", exact: true }).click();
    await p.locator(".folio-turn").waitFor({ state: "detached" });
    const turnReadyMs = Date.now() - turn;
    await p
      .getByRole("button", { name: "Previous chapter", exact: true })
      .click();
    const raf = await frames;
    const metrics = await p.evaluate(() => ({
      ...window.__codexMetrics,
      canvases: document.querySelectorAll("canvas").length,
      book: { ...document.querySelector(".celestial-book").dataset },
      heap: performance.memory
        ? {
            usedBytes: performance.memory.usedJSHeapSize,
            totalBytes: performance.memory.totalJSHeapSize,
          }
        : null,
      resources: performance.getEntriesByType("resource").map((r) => ({
        name: r.name.replace(location.origin, ""),
        transferBytes: r.transferSize,
        durationMs: r.duration,
      })),
      recordBytes: localStorage.getItem("fate.codex.v1").length,
    }));
    receipt.profiles.push({
      profile,
      coverReadyMs,
      openReadyMs,
      turnReadyMs,
      raf,
      metrics,
      posts,
    });
    console.log(
      profile.name,
      "cover",
      coverReadyMs,
      "open",
      openReadyMs,
      "turn",
      turnReadyMs,
      "RAF",
      raf.meanHz.toFixed(1),
      "p95",
      raf.p95Ms.toFixed(1),
      "CLS",
      metrics.cls,
      "bytes",
      metrics.recordBytes,
    );
    await c.close();
  }
  writeFileSync(
    "../evidence/codex-performance.json",
    JSON.stringify(receipt, null, 2),
  );
} finally {
  await browser.close();
}
