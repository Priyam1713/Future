import { chromium } from "@playwright/test";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";

const origin = "http://127.0.0.1:8010";
const rooms = ["vedic", "bazi", "iching", "runes"];
const requested = process.argv.find((arg) => arg.startsWith("--rooms="));
const selected = requested ? requested.slice(8).split(",") : rooms;
if (selected.some((room) => !rooms.includes(room)))
  throw new Error("Unknown chamber in --rooms");
const mobile = { width: 390, height: 844 };
const desktop = { width: 1440, height: 1000 };
const modes = {
  mobile: { viewport: mobile, isMobile: true, hasTouch: true },
  desktop: { viewport: desktop },
};
const screenshots = "../screenshots";
const evidence = "../evidence";
const captureDir = "../../tmp/block06-video";
mkdirSync(captureDir, { recursive: true });
const browser = await chromium.launch();

async function prepare(p, room) {
  await p.goto(origin + "/#" + room);
  await p.locator(".chamber-intro h1").waitFor();
  await p.evaluate(() => document.fonts.ready);
}
const press = (p, name) =>
  p.getByRole("button", { name, exact: !(name instanceof RegExp) }).click();
const scroll = (p, selector) =>
  p
    .locator(selector)
    .first()
    .evaluate((e) => e.scrollIntoView({ block: "start", behavior: "instant" }));
async function begin(p, room) {
  if (room === "vedic" || room === "bazi") {
    await p.getByLabel("Date of birth", { exact: true }).fill("1990-07-15");
    await p.getByLabel("Recorded birth time").fill("14:30:00");
    await p.getByLabel("Birth city", { exact: true }).fill("London GB");
    await press(p, "Find city");
    await p
      .getByRole("button", { name: /^London · GB/ })
      .first()
      .click();
    await p
      .getByLabel(
        "I’ve checked the coordinates and timezone for my birthplace.",
      )
      .check();
    if (room === "vedic")
      await p.getByLabel("Explore periods on this UTC day").fill("2026-11-20");
  }
  const response = p.waitForResponse((r) => r.url().endsWith("/api/chambers"));
  const t0 = performance.now();
  await press(
    p,
    {
      vedic: "Open my sidereal charts",
      bazi: "Open my Four Pillars",
      iching: "Begin the six-line cast",
      runes: "Draw the runestones",
    }[room],
  );
  const res = await response;
  if (!res.ok())
    throw new Error("Native request failed: " + (await res.text()));
  const { receipt: _, ...body } = await res.json();
  const request = res.request().postDataJSON();
  const apiMs = Math.round(performance.now() - t0);
  await p.locator(".chamber-result").waitFor();
  await scroll(p, ".chamber-result");
  return { ...body, request, apiMs };
}
async function beginForMedia(p, room) {
  for (let attempt = 0; attempt < 8; attempt++) {
    const data = await begin(p, room);
    if (
      room !== "iching" ||
      data.snapshot.figures[0] !== data.snapshot.figures[1]
    )
      return data;
    // Choose a native cast with moving lines so the recording shows the transformation.
    await press(p, /Start a fresh cast/);
  }
  throw new Error("The captured I Ching casts had no moving lines");
}
async function explore(p, room, body, hold = 0) {
  const wait = () => (hold ? p.waitForTimeout(hold) : Promise.resolve());
  if (room === "vedic") {
    await press(p, "D9 · Navamsa");
    await wait();
    await p
      .getByRole("group", { name: "Explore the nine grahas" })
      .getByRole("button", { name: "Mars", exact: true })
      .click();
    await wait();
    await press(p, "Reveal my birth star");
    await wait();
    if (hold) {
      await scroll(p, ".dasha-rail");
      await p.locator(".dasha-rail button").last().click();
      await wait();
    } else await scroll(p, ".chamber-result");
  } else if (room === "bazi") {
    await press(p, /^month pillar/);
    await wait();
    await press(p, /^hour pillar/);
    await wait();
    await press(p, /^day pillar/);
    await wait();
    await scroll(p, ".chamber-result");
  } else if (room === "iching") {
    for (let i = 1; i <= 6; i++) {
      await press(p, "Cast line " + i);
      await wait();
    }
    if (body.snapshot.figures[0] !== body.snapshot.figures[1]) {
      await press(p, "Relating figure");
      await wait();
    }
    await scroll(p, ".chamber-result");
  } else {
    for (let i = 1; i <= 3; i++) {
      await press(p, new RegExp("^Reveal stone " + i));
      await wait();
    }
    await scroll(p, ".chamber-result");
  }
}
async function stopRecording(ctx, page, trim, duration, room) {
  const raw = page.video();
  await ctx.close();
  const source = await raw.path();
  const output = evidence + "/block06-" + room + ".mp4";
  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-ss",
      String(trim),
      "-i",
      source,
      "-t",
      String(duration),
      "-c:v",
      "libx264",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      "-crf",
      "19",
      "-an",
      output,
    ],
    { stdio: "pipe" },
  );
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
        output,
      ],
      { encoding: "utf8" },
    ),
  );
}
async function media() {
  const native = requested
    ? JSON.parse(readFileSync(evidence + "/block06-native.json", "utf8")).native
    : {};
  const recordings = requested
    ? JSON.parse(readFileSync(evidence + "/block06-recordings.json", "utf8"))
        .recordings
    : {};
  for (const room of selected) {
    for (const [name, device] of Object.entries(modes)) {
      const ctx = await browser.newContext({ ...device, deviceScaleFactor: 1 });
      const p = await ctx.newPage();
      await prepare(p, room);
      if (name === "desktop")
        await p.screenshot({
          path: `${screenshots}/06-${room}-entrance.png`,
          animations: "disabled",
        });
      const data = await beginForMedia(p, room);
      await explore(p, room, data);
      await p.screenshot({
        path: `${screenshots}/06-${room}-${name}.png`,
        animations: "disabled",
      });
      if (name === "mobile") native[room] = data;
      await ctx.close();
    }
    const ctx = await browser.newContext({
      ...modes.mobile,
      deviceScaleFactor: 1,
      recordVideo: { dir: captureDir, size: mobile },
    });
    const t0 = performance.now();
    const p = await ctx.newPage();
    await prepare(p, room);
    const data = await beginForMedia(p, room);
    await p.waitForTimeout(420);
    const trim = (performance.now() - t0) / 1000;
    await p.waitForTimeout(800);
    await explore(p, room, data, 670);
    await p.waitForTimeout(1400);
    const duration = (performance.now() - t0) / 1000 - trim;
    const codec = await stopRecording(ctx, p, trim, duration, room);
    recordings[room] = {
      media: codec,
      trim,
      snapshot: data.snapshot,
      request: data.request,
    };
    console.log(room, "recorded", codec.format.duration);
  }
  writeFileSync(
    evidence + "/block06-native.json",
    JSON.stringify(
      {
        scope:
          "Real browser API responses; synthetic natal inputs and seeded visitor-independent casts.",
        native,
      },
      null,
      2,
    ) + "\n",
  );
  writeFileSync(
    evidence + "/block06-recordings.json",
    JSON.stringify(
      {
        scope:
          "Uncomposited 390×844 Chromium captures. Only input setup and processing trimmed.",
        recordings,
      },
      null,
      2,
    ) + "\n",
  );
}
async function profile() {
  const entries = [];
  for (const room of rooms)
    for (const [name, device] of Object.entries(modes)) {
      const ctx = await browser.newContext({ ...device, deviceScaleFactor: 2 });
      await ctx.addInitScript(() => {
        window.chamberMetrics = { cls: 0, longTasks: [] };
        new PerformanceObserver((list) => {
          for (const entry of list.getEntries())
            if (!entry.hadRecentInput) window.chamberMetrics.cls += entry.value;
        }).observe({ type: "layout-shift", buffered: true });
        new PerformanceObserver((list) => {
          for (const entry of list.getEntries())
            window.chamberMetrics.longTasks.push(entry.duration);
        }).observe({ type: "longtask", buffered: true });
      });
      const p = await ctx.newPage(),
        errors = [];
      p.on("pageerror", (error) => errors.push(error.message));
      const start = performance.now();
      await prepare(p, room);
      const entranceMs = Math.round(performance.now() - start);
      const data = await begin(p, room);
      const cadence = p.evaluate(async () => {
        const frames = [];
        let previous = performance.now();
        for (let i = 0; i < 125; i++) {
          const now = await new Promise(requestAnimationFrame);
          frames.push(now - previous);
          previous = now;
        }
        const sorted = frames.slice(3).sort((a, b) => a - b);
        return {
          samples: sorted.length,
          p95Ms: sorted[Math.floor(sorted.length * 0.95)],
          maxMs: sorted.at(-1),
        };
      });
      const t0 = performance.now();
      await press(
        p,
        {
          vedic: "D9 · Navamsa",
          bazi: /^month pillar/,
          iching: "Cast line 1",
          runes: /^Reveal stone 1/,
        }[room],
      );
      await p.evaluate(
        () =>
          new Promise((r) =>
            requestAnimationFrame(() => requestAnimationFrame(r)),
          ),
      );
      const interactionMs = Math.round(performance.now() - t0);
      const frames = await cadence;
      const metrics = await p.evaluate(() => ({
        ...window.chamberMetrics,
        canvases: document.querySelectorAll("canvas").length,
        assets: performance
          .getEntriesByType("resource")
          .filter((r) => /chamber/i.test(r.name))
          .map((r) => ({
            asset: r.name.split("/").at(-1),
            bytes: r.encodedBodySize,
          })),
      }));
      if (errors.length) throw new Error(errors.join("\n"));
      entries.push({
        room,
        profile: name,
        entranceMs,
        nativeActionMs: data.apiMs,
        interactionMs,
        frames,
        metrics,
      });
      console.log(room, name, data.apiMs, interactionMs, frames.p95Ms);
      await ctx.close();
    }
  writeFileSync(
    evidence + "/block06-performance.json",
    JSON.stringify(
      {
        scope:
          "Isolated local Chromium profiles with real native requests. Action timings include browser automation. RAF intervals are main-thread scheduling.",
        profiles: entries,
      },
      null,
      2,
    ) + "\n",
  );
}
try {
  if (process.argv.includes("--performance")) await profile();
  else await media();
} finally {
  await browser.close();
}
