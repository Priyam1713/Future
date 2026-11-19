import { chromium } from "@playwright/test";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";

const origin = "http://127.0.0.1:8010";
const rooms = [
  "oracle",
  "pendulum",
  "crystal",
  "mirror",
  "dream",
  "geomancy",
  "bibliomancy",
];
const mobile = { width: 390, height: 844 };
const modes = {
  mobile: { viewport: mobile, isMobile: true, hasTouch: true },
  desktop: { viewport: { width: 1440, height: 1000 } },
};
const requested = process.argv.find((arg) => arg.startsWith("--rooms="));
const selected = requested ? requested.slice(8).split(",") : rooms;
if (selected.some((room) => !rooms.includes(room)))
  throw new Error("Unknown ritual in --rooms");
const evidence = "../evidence",
  screenshots = "../screenshots";
const out = "../../tmp/block07-video";
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
});
const hold = (page, ms) => (ms ? page.waitForTimeout(ms) : Promise.resolve());
const press = (page, name) =>
  page.getByRole("button", { name, exact: !(name instanceof RegExp) }).click();
const align = (page, selector = ".ritual-stage") =>
  page
    .locator(selector)
    .first()
    .evaluate((e) => e.scrollIntoView({ block: "start", behavior: "instant" }));

async function prepare(page, room) {
  await page.goto(origin + "/#" + room);
  await page.locator(".ritual-intro h1").waitFor();
  await page.evaluate(() => document.fonts.ready);
}

async function read(page, action) {
  const wait = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/ritual-wing") && r.request().method() === "POST",
  );
  const start = performance.now();
  await press(page, action);
  const r = await wait;
  if (!r.ok()) throw new Error("Native ritual failed: " + (await r.text()));
  const body = await r.json();
  const nativeActionMs = Math.round(performance.now() - start);
  await page.locator(".ritual-result").waitFor();
  return { ...body, request: r.request().postDataJSON(), nativeActionMs };
}

async function interact(
  page,
  room,
  { delay = 0, onArtifact = () => Promise.resolve() } = {},
) {
  await align(page);
  let native;
  if (room === "oracle") {
    await press(page, "Five");
    native = await read(page, "Draw the oracle cards");
    for (let i = 1; i <= 5; i++) {
      await press(page, "Reveal card " + i);
      await hold(page, delay);
    }
  } else if (room === "pendulum") {
    await press(page, "Swing the display model");
    await hold(page, delay ? 1250 : 0);
    await press(page, "My observed movement");
    await page.getByLabel("My yes movement").selectOption("vertical");
    await page.getByLabel("My no movement").selectOption("horizontal");
    await page.getByLabel("Movement observed").selectOption("vertical");
    await onArtifact(page);
    await hold(page, delay);
    native = await read(page, "Read my reported movement");
  } else if (room === "crystal" || room === "mirror") {
    await page.locator(".ritual-glass").waitFor();
    await hold(page, delay ? 950 : 200);
    await onArtifact(page);
    await press(page, "Open my journal");
    await page
      .getByLabel("My own observation")
      .fill("Synthetic QA note: a pale light at the rim.");
    await page
      .getByLabel("How I describe it")
      .selectOption("observed_reflection");
    await hold(page, delay);
    native = await read(page, "Close the journal");
  } else if (room === "dream") {
    await page
      .getByLabel("My dream notes")
      .fill("Synthetic QA note: a serpent beside an empty plate.");
    await press(page, "Serpent");
    await press(page, "Eating");
    await page.getByLabel("Were you hungry?").selectOption("yes");
    await hold(page, delay);
    native = await read(page, "Open my selected references");
    await page.locator(".dream-reference summary").first().click();
  } else if (room === "geomancy") {
    const mothers = ["1212", "2112", "1122", "2121"];
    for (const [i, mother] of mothers.entries())
      for (const [j, n] of [...mother].entries()) {
        const button = page.getByRole("button", {
          name: new RegExp("^Mother " + (i + 1) + ", row " + (j + 1) + ":"),
        });
        for (let times = 0; times < Number(n); times++) await button.click();
        if (j === 3) await hold(page, delay > 0 ? 250 : 0);
      }
    native = await read(page, "Form the shield");
    await hold(page, 1300);
    await page.getByText("Trace the rows and parents", { exact: true }).click();
  } else {
    await press(page, "Ruth 2");
    await page.locator(".book-selection button").nth(3).click();
    await page.getByLabel("Nearby sentences on each side").selectOption("2");
    await onArtifact(page);
    await hold(page, delay);
    native = await read(page, "Read this passage");
    await page.getByText("Nearby sentences & edition", { exact: true }).click();
  }
  await align(page, ".ritual-result");
  await page.evaluate(() => document.fonts.ready);
  return native;
}

function captureWarmup(path) {
  // Chromium can emit a gray, partially resized viewport before the screencast settles.
  const sample = execFileSync(
    "ffmpeg",
    [
      "-v",
      "error",
      "-i",
      path,
      "-t",
      "10",
      "-vf",
      "fps=8,scale=52:112",
      "-f",
      "rawvideo",
      "-pix_fmt",
      "rgb24",
      "-",
    ],
    { maxBuffer: 4 * 1024 * 1024 },
  );
  const pixels = 52 * 112,
    length = pixels * 3;
  let streak = 0;
  for (let offset = 0; offset + length <= sample.length; offset += length) {
    let gray = 0;
    for (let i = offset; i < offset + length; i += 3) {
      const [r, g, b] = [sample[i], sample[i + 1], sample[i + 2]];
      if (r > 90 && r < 160 && Math.abs(r - g) < 3 && Math.abs(r - b) < 3)
        gray++;
    }
    streak = gray / pixels > 0.62 ? 0 : streak + 1;
    if (streak >= 2) return Math.max(0, (offset / length - 1) / 8);
  }
  throw new Error("No stable full viewport found in the recording");
}
async function saveClip(ctx, page, room) {
  const record = page.video();
  await ctx.close();
  const path = await record.path();
  const trim = captureWarmup(path);
  const file = evidence + "/block07-" + room + ".mp4";
  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-ss",
      String(trim),
      "-i",
      path,
      "-c:v",
      "libx264",
      "-crf",
      "19",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      "-an",
      file,
    ],
    { stdio: "pipe" },
  );
  const media = JSON.parse(
    execFileSync(
      "ffprobe",
      [
        "-v",
        "error",
        "-show_entries",
        "stream=width,height,codec_name:format=duration",
        "-of",
        "json",
        file,
      ],
      { encoding: "utf8" },
    ),
  );
  return { media, trim };
}

async function media() {
  const native = requested
    ? JSON.parse(readFileSync(evidence + "/block07-native.json", "utf8")).native
    : {};
  const recordings = requested
    ? JSON.parse(readFileSync(evidence + "/block07-recordings.json", "utf8"))
        .recordings
    : {};
  const artifactRooms = new Set([
    "pendulum",
    "crystal",
    "mirror",
    "bibliomancy",
  ]);
  for (const room of selected) {
    for (const [mode, device] of Object.entries(modes)) {
      const ctx = await browser.newContext({ ...device, deviceScaleFactor: 1 });
      const page = await ctx.newPage(),
        errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await prepare(page, room);
      if (mode === "desktop")
        await page.screenshot({
          path: `${screenshots}/07-${room}-entrance.png`,
          animations: "disabled",
        });
      const saveShot = async () => {
        await align(page);
        await page.screenshot({
          path: `${screenshots}/07-${room}-${mode}.png`,
          animations: "disabled",
        });
      };
      const reading = await interact(page, room, {
        onArtifact: artifactRooms.has(room) ? saveShot : undefined,
      });
      if (!artifactRooms.has(room)) await saveShot();
      else if (mode === "mobile")
        await page.screenshot({
          path: `${screenshots}/07-${room}-reading-mobile.png`,
          animations: "disabled",
        });
      if (mode === "mobile") native[room] = reading;
      if (errors.length) throw new Error(errors.join("\n"));
      await ctx.close();
    }
    const ctx = await browser.newContext({
      ...modes.mobile,
      deviceScaleFactor: 1,
      recordVideo: { dir: out, size: mobile },
    });
    const page = await ctx.newPage();
    await prepare(page, room);
    await align(page);
    await hold(page, 400);
    const reading = await interact(page, room, { delay: 600 });
    await hold(page, 2900);
    const clip = await saveClip(ctx, page, room);
    recordings[room] = {
      ...clip,
      snapshot: reading.snapshot,
      request: reading.request,
    };
    console.log(room, "recorded", clip.media.format.duration);
  }
  writeFileSync(
    evidence + "/block07-native.json",
    JSON.stringify(
      {
        scope: "Unmocked browser native results and synthetic QA entries.",
        native,
      },
      null,
      2,
    ) + "\n",
  );
  writeFileSync(
    evidence + "/block07-recordings.json",
    JSON.stringify(
      {
        scope:
          "Real mobile Chromium interactions. Gray screencast startup frames removed where present. No compositing.",
        recordings,
      },
      null,
      2,
    ) + "\n",
  );
}

async function profile() {
  const profiles = requested
    ? JSON.parse(
        readFileSync(evidence + "/block07-performance.json", "utf8"),
      ).profiles.filter((row) => !selected.includes(row.room))
    : [];
  for (const room of selected)
    for (const [mode, device] of Object.entries(modes)) {
      const ctx = await browser.newContext({ ...device, deviceScaleFactor: 2 });
      await ctx.addInitScript(() => {
        window.metrics = { cls: 0, longTasks: [] };
        new PerformanceObserver((list) => {
          for (const row of list.getEntries())
            if (!row.hadRecentInput) window.metrics.cls += row.value;
        }).observe({ type: "layout-shift", buffered: true });
        new PerformanceObserver((list) => {
          for (const row of list.getEntries())
            window.metrics.longTasks.push(row.duration);
        }).observe({ type: "longtask", buffered: true });
      });
      const page = await ctx.newPage(),
        start = performance.now();
      await prepare(page, room);
      const entranceMs = Math.round(performance.now() - start);
      await align(page);
      if (room === "crystal" || room === "mirror")
        await page
          .locator('.ritual-glass[data-renderer="volumetric"]')
          .waitFor({ timeout: 10000 });
      const cadence = page.evaluate(async () => {
        const intervals = [];
        let old = performance.now();
        for (let i = 0; i < 125; i++) {
          const now = await new Promise(requestAnimationFrame);
          intervals.push(now - old);
          old = now;
        }
        const sorted = intervals.slice(3).sort((a, b) => a - b);
        return {
          p95Ms: sorted[Math.floor(sorted.length * 0.95)],
          maxMs: sorted.at(-1),
        };
      });
      const first = performance.now();
      const actions = {
        oracle: "Five",
        pendulum: "Swing the display model",
        crystal: "Open my journal",
        mirror: "Open my journal",
        dream: "Serpent",
        geomancy: /^Mother 1, row 1:/,
        bibliomancy: "Ruth 2",
      };
      await press(page, actions[room]);
      await page.evaluate(
        () =>
          new Promise((r) =>
            requestAnimationFrame(() => requestAnimationFrame(r)),
          ),
      );
      const interactionMs = Math.round(performance.now() - first);
      const frames = await cadence;
      const metrics = await page.evaluate(() => ({
        ...window.metrics,
        renderer:
          document
            .querySelector(".ritual-glass")
            ?.getAttribute("data-renderer") ?? "dom",
        canvases: document.querySelectorAll("canvas").length,
        glassQuality:
          document
            .querySelector(".ritual-glass")
            ?.getAttribute("data-quality") ?? null,
        glassBuffer: document.querySelector(".glass-fog")?.width ?? null,
        resources: performance
          .getEntriesByType("resource")
          .filter((r) => r.name.includes("ritual-"))
          .map((r) => ({
            name: r.name.split("/").at(-1),
            bytes: r.encodedBodySize,
          })),
      }));
      await page.reload();
      await page.locator(".ritual-intro h1").waitFor();
      const data = await interact(page, room);
      profiles.push({
        room,
        profile: mode,
        entranceMs,
        interactionMs,
        frames,
        metrics,
        nativeActionMs: data.nativeActionMs,
      });
      console.log(room, mode, interactionMs, frames.p95Ms, data.nativeActionMs);
      await ctx.close();
    }
  writeFileSync(
    evidence + "/block07-performance.json",
    JSON.stringify(
      {
        scope:
          "Local Chromium profiles. Main-thread animation callback intervals with external display presentation unmeasured. Action timings include automation.",
        profiles,
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
