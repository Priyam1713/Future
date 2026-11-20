import { chromium, firefox, webkit } from "@playwright/test";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { execFileSync } from "node:child_process";
import { align, button } from "./future-journeys.mjs";

const origin = process.env.FATE_CAPTURE_ORIGIN || "http://127.0.0.1:8011";
const raw = resolve("../../tmp/block12-video");
mkdirSync(raw, { recursive: true });
const dimensions = [
  [390, 844],
  [768, 1024],
  [1440, 900],
  [1920, 1080],
  [2560, 1440],
  [3440, 1440],
];
const games = ["loom", "switch", "signal"];
const mode = process.argv[2] || "media";
const software = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"];
const save = (key, value) =>
  writeFileSync(
    `../evidence/block12-${key}.json`,
    JSON.stringify(value, null, 2) + "\n",
  );
const label = {
  loom: "Advance four generations",
  switch: "Send the pulse",
  signal: "Seal my forecast",
};
const hold = (page, wait = 500) => page.waitForTimeout(wait);
const screenshot = async (page, name) => {
  await page.evaluate(() => document.fonts.ready);
  await hold(page, 250);
  await page.screenshot({
    path: `../screenshots/12-${name}.png`,
    animations: "disabled",
  });
};
async function screen(page, hash) {
  await page.goto(origin + "/#" + hash);
  await page.locator("h1").waitFor();
}
async function start(page, game, touch = false) {
  await screen(page, "play-" + game);
  const begin = button(page, "Begin round");
  await (touch ? begin.tap() : begin.click());
}
async function choose(page, game, touch = false) {
  if (game === "loom") {
    const cell = button(page, "Cell 1,5");
    await (touch ? cell.tap() : cell.click());
  } else if (game === "switch") {
    const gate = page.getByRole("button", { name: /Bell pair/ });
    await (touch ? gate.tap() : gate.click());
  } else {
    const dial = page.getByRole("slider", {
      name: "Your probability of a signal",
    });
    const box = await dial.boundingBox();
    const handle = {
      x: box.x + Math.round(box.width * 0.46),
      y: box.y + box.height * 0.5,
    };
    if (touch) await page.touchscreen.tap(handle.x, handle.y);
    else await page.mouse.click(handle.x, handle.y);
  }
}
async function resolveRound(page, game, touch = false) {
  const waiting = page.waitForResponse(
    (response) =>
      response.url().endsWith("/api/future-study") &&
      response.request().method() === "POST",
  );
  const before = performance.now();
  const action = button(page, label[game]);
  await (touch ? action.tap() : action.click());
  const response = await waiting;
  if (!response.ok()) throw Error(await response.text());
  const native = await response.json();
  await page.locator(".arcade-score").waitFor();
  const timing = response.request().timing();
  return {
    request: response.request().postDataJSON(),
    native: {
      counts: native.view.instrument.counts,
      bars: native.view.instrument.bars,
      digest: native.result.report_sha256,
    },
    score: await page.locator(".arcade-score").innerText(),
    visibleResultMs: Math.round(performance.now() - before),
    requestMs: Math.round(timing.responseEnd - timing.requestStart),
  };
}
async function closeVideo(page, context, name) {
  const video = page.video();
  await context.close();
  const path = `../evidence/block12-${name}.mp4`;
  execFileSync("ffmpeg", [
    "-y",
    "-v",
    "error",
    "-ss",
    "0.25",
    "-i",
    await video.path(),
    "-an",
    "-c:v",
    "libx264",
    "-crf",
    "21",
    "-pix_fmt",
    "yuv420p",
    "-movflags",
    "+faststart",
    path,
  ]);
  return JSON.parse(
    execFileSync(
      "ffprobe",
      [
        "-v",
        "error",
        "-show_entries",
        "stream=width,height,codec_name:format=duration",
        "-of",
        "json",
        path,
      ],
      { encoding: "utf8" },
    ),
  );
}
async function fillBirth(page) {
  await screen(page, "western");
  await page.getByLabel("Date of birth", { exact: true }).fill("1990-07-15");
  await page.getByLabel("Recorded birth time").fill("14:30");
  await page.getByLabel("Birth city", { exact: true }).fill("London GB");
  await button(page, "Find city").click();
  await page
    .getByRole("button", { name: /^London · GB/ })
    .first()
    .click();
  await page
    .getByLabel("I’ve checked the coordinates and timezone for my birthplace.")
    .check();
  await button(page, "Open my celestial chart").click();
  await button(page, "Skip reveal & read my chart").click();
  await button(page, "Explore Moon").click();
}
async function media(browser) {
  const records = {};
  for (const [name, width, height] of [
    ["mobile", 390, 844],
    ["desktop", 1440, 900],
  ]) {
    const viewport = { width, height },
      touch = name === "mobile";
    const options = {
      viewport,
      isMobile: touch,
      hasTouch: touch,
      deviceScaleFactor: 1,
    };
    const scene = await browser.newContext(options);
    const page = await scene.newPage();
    await screen(page, "play");
    await screenshot(page, `play-hall-${name}`);
    await screen(page, "gallery");
    await button(page, "The Tomorrow Machine").click();
    await align(page, ".gallery-map");
    await screenshot(page, `gallery-${name}`);
    await fillBirth(page);
    await align(page, ".western-chart-layout");
    await screenshot(page, `observatory-${name}`);
    await scene.close();
    for (const game of games) {
      const ctx = await browser.newContext({
        ...options,
        recordVideo: { dir: raw, size: viewport },
      });
      const p = await ctx.newPage();
      const errors = [];
      p.on("pageerror", (e) => errors.push(e.message));
      try {
        await screen(p, "play-" + game);
        await hold(p, 700);
        await button(p, "Begin round").click();
        await choose(p, game, touch);
        await hold(p, 650);
        await align(p, ".arcade-layout");
        await screenshot(p, `${game}-${name}`);
        const proof = await resolveRound(p, game, touch);
        await hold(p, 650);
        await screenshot(p, `${game}-result-${name}`);
        if (game === "loom") {
          const slider = p.getByRole("slider", { name: /Generation/ });
          await slider.press("Home");
          await hold(p, 440);
          await slider.press("End");
        }
        await hold(p, 1400);
        await button(p, "Play next round").click();
        await hold(p, 1250);
        if (errors.length) throw Error(errors.join("; "));
        records[`${game}-${name}`] = {
          ...proof,
          recording: await closeVideo(p, ctx, `${game}-${name}`),
        };
        console.log(
          game,
          name,
          records[`${game}-${name}`].recording.format.duration,
        );
      } finally {
        await ctx.close();
      }
    }
  }
  const wide = await browser.newContext({
    viewport: { width: 3440, height: 1440 },
  });
  const p = await wide.newPage();
  await screen(p, "gallery");
  await screenshot(p, "gallery-ultrawide");
  await wide.close();
  save("media", { browser: browser.version(), records });
}
async function installProbes(context) {
  await context.addInitScript(() => {
    const entries = [];
    const longFrames = [];
    if (PerformanceObserver.supportedEntryTypes.includes("layout-shift")) {
      new PerformanceObserver((list) =>
        entries.push(
          ...list
            .getEntries()
            .filter((x) => !x.hadRecentInput)
            .map((x) => [x.startTime, x.value]),
        ),
      ).observe({ type: "layout-shift", buffered: true });
    }
    if (
      PerformanceObserver.supportedEntryTypes.includes("long-animation-frame")
    ) {
      new PerformanceObserver((list) =>
        longFrames.push(...list.getEntries().map((x) => x.duration)),
      ).observe({ type: "long-animation-frame", buffered: true });
    }
    window.fateQA = { entries, longFrames };
  });
}
async function observe(page) {
  return page.evaluate(async () => {
    const frames = [];
    let previous = await new Promise(requestAnimationFrame);
    for (let i = 0; i < 50; i++) {
      const next = await new Promise(requestAnimationFrame);
      frames.push(next - previous);
      previous = next;
    }
    frames.sort((a, b) => a - b);
    const probe = window.fateQA;
    let shift = 0,
      start = -Infinity,
      last = -Infinity,
      cls = 0;
    for (const [when, value] of probe.entries) {
      if (when - last > 1000 || when - start > 5000) {
        shift = 0;
        start = when;
      }
      shift += value;
      last = when;
      cls = Math.max(cls, shift);
    }
    const resources = performance.getEntriesByType("resource");
    return {
      callbackP95Ms: Math.round(frames[47] * 10) / 10,
      callbacksOver25Ms: frames.filter((ms) => ms > 25).length,
      longAnimationFrameCount: probe.longFrames.length,
      longAnimationFrameMaxMs: Math.max(0, ...probe.longFrames),
      cumulativeLayoutShift: cls,
      transferBytes: resources.reduce(
        (sum, entry) => sum + entry.transferSize,
        0,
      ),
      imageTransferBytes: resources
        .filter((x) => x.initiatorType === "img")
        .reduce((sum, entry) => sum + entry.transferSize, 0),
      firstContentfulPaintMs:
        performance.getEntriesByName("first-contentful-paint")[0]?.startTime ??
        null,
    };
  });
}
async function benchmark(browser) {
  const profiles = [];
  const galleryProfiles = [];
  for (const [width, height] of dimensions) {
    const touch = width === 390;
    const ctx = await browser.newContext({
      viewport: { width, height },
      deviceScaleFactor: 1,
      isMobile: touch,
      hasTouch: touch,
    });
    await installProbes(ctx);
    try {
      const p = await ctx.newPage();
      if (touch) {
        const cdp = await ctx.newCDPSession(p);
        await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
      }
      const t = performance.now();
      await start(p, "switch", touch);
      const readyMs = Math.round(performance.now() - t);
      await choose(p, "switch", touch);
      const round = await resolveRound(p, "switch", touch);
      if (
        await p.evaluate(
          () => document.documentElement.scrollWidth > innerWidth,
        )
      )
        throw Error("Overflow " + width);
      profiles.push({
        width,
        height,
        touch,
        readyMs,
        visibleResultMs: round.visibleResultMs,
        requestMs: round.requestMs,
        ...(await observe(p)),
      });
      console.log(width, profiles.at(-1));
    } finally {
      await ctx.close();
    }
    const galleryContext = await browser.newContext({
      viewport: { width, height },
      deviceScaleFactor: 1,
      isMobile: touch,
      hasTouch: touch,
    });
    await installProbes(galleryContext);
    try {
      const page = await galleryContext.newPage();
      if (touch) {
        const cdp = await galleryContext.newCDPSession(page);
        await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
      }
      const begun = performance.now();
      await screen(page, "gallery");
      const search = page.getByRole("searchbox", { name: "Find a tradition" });
      await search.waitFor();
      const readyMs = Math.round(performance.now() - begun);
      await search.fill("lorenz");
      const openStarted = performance.now();
      const link = page.getByRole("link", { name: "Enter Lorenz Chaos" });
      await (touch ? link.tap() : link.click());
      await page.locator(".future-room h1").waitFor();
      const headingMs = Math.round(performance.now() - openStarted);
      await page.locator(".lab-payoff h2").waitFor();
      const resultMs = Math.round(performance.now() - openStarted);
      galleryProfiles.push({
        width,
        height,
        touch,
        readyMs,
        headingMs,
        resultMs,
        ...(await observe(page)),
      });
    } finally {
      await galleryContext.close();
    }
  }
  save("performance", {
    browser: browser.version(),
    method:
      "Installed Chrome on local loopback in fresh contexts. 390px touch emulation uses Chromium CDP 4× CPU slowdown; other sizes unthrottled. Arcade profiles time Signal Switch. Gallery profiles time search readiness and opening Lorenz Chaos from a search link. Action time includes automation dispatch. requestMs is request start through response end, and visibleResultMs includes the rendered score. Callback cadence and long animation frames are paint scheduling diagnostics rather than displayed frame rates. CLS excludes recent input shifts.",
    profiles,
    galleryProfiles,
  });
}
async function secondEngine(engine, name) {
  let browser;
  try {
    browser = await engine.launch();
  } catch (error) {
    return {
      engine: name,
      status: "unavailable",
      reason: String(error).split("\n").slice(0, 6).join(" "),
    };
  }
  const checks = [];
  try {
    for (const [width, height] of [dimensions[0], dimensions.at(-1)]) {
      const ctx = await browser.newContext({
        viewport: { width, height },
        reducedMotion: "reduce",
      });
      try {
        const page = await ctx.newPage();
        await screen(page, "gallery");
        await button(page, "The Celestial Court").click();
        if (
          await page.evaluate(
            () => document.documentElement.scrollWidth > innerWidth,
          )
        )
          throw Error("Gallery overflow");
        for (const game of games) {
          await start(page, game);
          await choose(page, game);
          const summary = await resolveRound(page, game);
          if (
            await page.evaluate(
              () => document.documentElement.scrollWidth > innerWidth,
            )
          )
            throw Error("Arcade overflow");
          checks.push({ width, height, game, score: summary.score });
        }
      } finally {
        await ctx.close();
      }
    }
    return {
      engine: name,
      version: browser.version(),
      status: "passed",
      checks,
    };
  } finally {
    await browser.close();
  }
}
async function zoom() {
  const profile = mkdtempSync(resolve("../../tmp/block12-zoom-profile-"));
  const ctx = await chromium.launchPersistentContext(profile, {
    channel: "chrome",
    headless: true,
    viewport: null,
    args: ["--window-size=1440,900"],
  });
  try {
    const page = ctx.pages()[0];
    const settings = await ctx.newPage();
    await settings.goto("chrome://settings/appearance");
    const control = settings.locator("#zoomLevel");
    const samples = [];
    for (const factor of [1, 1.25, 2]) {
      await control.selectOption({ label: factor * 100 + "%" });
      for (const hash of ["gallery", "play"]) {
        await screen(page, hash);
        const widths = await page.evaluate(() => ({
          inner: innerWidth,
          scroll: document.documentElement.scrollWidth,
          dpr: devicePixelRatio,
        }));
        const baseDpr = samples[0]?.dpr ?? widths.dpr;
        if (
          Math.abs(widths.dpr / baseDpr - factor) > 0.03 ||
          widths.scroll > widths.inner
        )
          throw Error(
            `Chrome zoom check failed at ${factor}: ${JSON.stringify(widths)}`,
          );
        samples.push({ factor, hash, ...widths });
      }
    }
    return samples;
  } finally {
    await ctx.close();
  }
}
if (mode === "engines") {
  save("compatibility", {
    firefox: await secondEngine(firefox, "Firefox"),
    webkit: await secondEngine(webkit, "WebKit"),
    zoom: await zoom(),
  });
} else {
  const browser = await chromium.launch({ channel: "chrome", args: software });
  try {
    await (mode === "benchmark" ? benchmark(browser) : media(browser));
  } finally {
    await browser.close();
  }
}
