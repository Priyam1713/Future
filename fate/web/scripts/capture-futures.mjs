import { chromium } from "@playwright/test";
import { writeFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import {
  align,
  blindTrial,
  button,
  exchange,
  open,
  rooms,
  runPublic,
  vault,
} from "./future-journeys.mjs";

const target = process.env.FATE_CAPTURE_ORIGIN ?? "http://127.0.0.1:8010";
const small = { width: 390, height: 844 };
const modes = {
  mobile: {
    viewport: small,
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 1,
  },
  desktop: { viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 },
};
const raw = "../../tmp/block10-video";
const browser = await chromium.launch({
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
});
const shots = (page, name) =>
  page.screenshot({
    path: `../screenshots/10-${name}.png`,
    animations: "disabled",
  });
const write = (name, value) =>
  writeFileSync(
    `../evidence/block10-${name}.json`,
    JSON.stringify(value, null, 2) + "\n",
  );
mkdirSync(raw, { recursive: true });

const stable = async (page) => {
  await page.evaluate(async () => {
    await document.fonts.ready;
    await document.querySelector(".future-entrance img").decode();
  });
};

async function cadence(page) {
  return page.evaluate(async () => {
    const values = [];
    let before = await new Promise(requestAnimationFrame);
    for (let i = 0; i < 65; i++) {
      const next = await new Promise(requestAnimationFrame);
      if (i >= 5) values.push(next - before);
      before = next;
    }
    values.sort((a, b) => a - b);
    return { p95Ms: values[56], maxMs: values.at(-1) };
  });
}

function encode(src, dst) {
  const sample = execFileSync(
    "ffmpeg",
    [
      "-v",
      "error",
      "-i",
      src,
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
  const size = 52 * 112 * 3;
  let offset = 0,
    streak = 0;
  for (; offset + size <= sample.length; offset += size) {
    let blank = 0;
    for (let i = offset; i < offset + size; i += 3) {
      const [r, g, b] = [sample[i], sample[i + 1], sample[i + 2]];
      if (r > 90 && Math.abs(r - g) < 3 && Math.abs(r - b) < 3) blank++;
    }
    streak = blank > (size / 3) * 0.62 ? 0 : streak + 1;
    if (streak === 2) break;
  }
  if (streak !== 2) throw Error("Screencast never showed a full viewport");
  execFileSync("ffmpeg", [
    "-y",
    "-v",
    "error",
    "-ss",
    String((offset / size - 1) / 8),
    "-i",
    src,
    "-an",
    "-c:v",
    "libx264",
    "-crf",
    "20",
    "-pix_fmt",
    "yuv420p",
    "-movflags",
    "+faststart",
    dst,
  ]);
  return JSON.parse(
    execFileSync(
      "ffprobe",
      [
        "-v",
        "error",
        "-show_entries",
        "stream=codec_name,width,height:format=duration",
        "-of",
        "json",
        dst,
      ],
      { encoding: "utf8" },
    ),
  );
}
async function closeVideo(page, context, name) {
  const file = page.video();
  await context.close();
  return encode(await file.path(), `../evidence/block10-${name}.mp4`);
}

async function stills() {
  const reports = {},
    profiles = [];
  let calls = 0,
    windowStart = 0;
  async function capacity() {
    if (!windowStart) windowStart = Date.now();
    if (calls >= 27) {
      const wait = 61000 - (Date.now() - windowStart);
      if (wait > 0) await new Promise((resolve) => setTimeout(resolve, wait));
      calls = 0;
      windowStart = Date.now();
    }
    calls++;
  }
  for (const room of rooms) {
    for (const [mode, options] of Object.entries(modes)) {
      const ctx = await browser.newContext(options);
      const page = await ctx.newPage();
      const errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      let report;
      if (room.id === 43) {
        const independent = await browser.newContext(options);
        const judge = await independent.newPage();
        const start = performance.now();
        const response = await blindTrial(page, judge, target);
        report = {
          oracle: 43,
          result: response.retrieved.response.result,
          actionMs: Math.round(performance.now() - start),
        };
        await independent.close();
      } else {
        await capacity();
        report = await runPublic(page, room, target);
      }
      await stable(page);
      if ([24, 43, 49, 50].includes(room.id)) {
        await align(page, ".future-entrance");
        await shots(page, `${room.slug}-entrance-${mode}`);
      }
      await align(page);
      const timing = await cadence(page);
      await shots(page, `${room.slug}-${mode}`);
      if (mode === "mobile") reports[room.id] = report;
      profiles.push({
        oracle: room.id,
        mode,
        actionMs: report.actionMs,
        ...timing,
      });
      if (errors.length) throw Error(errors.join("\n"));
      console.log(room.slug, mode, report.actionMs, timing.p95Ms);
      await ctx.close();
    }
  }
  await capacity();
  const context = await browser.newContext(modes.desktop);
  const page = await context.newPage();
  await runPublic(
    page,
    rooms.find((r) => r.id === 49),
    target,
  );
  await capacity();
  const benchmark = await exchange(page, "/api/future-study", () =>
    button(page, "NOAA benchmark").click(),
  );
  const native = benchmark.response.result;
  await page
    .getByRole("heading", { name: benchmark.response.view.title })
    .waitFor();
  await align(page);
  await shots(page, "noaa-evaluation-desktop");
  await context.close();
  write("historical", {
    request: benchmark.wire,
    reportHash: native.report_sha256,
    view: benchmark.response.view,
    actionMs: benchmark.elapsedMs,
  });
  write("native", {
    scope:
      "Public synthetic examples and a real two-context blind test with a synthetic QA transcript.",
    reports,
  });
  write("performance", {
    scope:
      "Chromium emulation on local loopback. Action includes navigation, native request and visible result. Room 43 includes the full two-context workflow. Frame samples measure callbacks.",
    profiles,
  });
}

const pause = (page) => page.waitForTimeout(360);
const video = () =>
  browser.newContext({
    ...modes.mobile,
    recordVideo: { dir: raw, size: small },
  });
async function recordings() {
  const out = {};
  const owner = await video(),
    observer = await video();
  const viewer = await owner.newPage(),
    judge = await observer.newPage();
  const trial = await blindTrial(viewer, judge, target, pause);
  await viewer.waitForTimeout(2400);
  const hash = trial.retrieved.response.result.commitment;
  out.viewer = {
    commitment: hash,
    media: await closeVideo(viewer, owner, "viewer"),
  };
  out.judge = {
    commitment: hash,
    media: await closeVideo(judge, observer, "judge"),
  };
  const dream = await video(),
    diary = await dream.newPage();
  await open(
    diary,
    rooms.find((r) => r.id === 44),
    target,
  );
  await align(diary);
  await diary.getByLabel("Feature to record").fill("A blue square");
  await diary
    .getByRole("checkbox", { name: /Process this private diary/ })
    .check();
  await pause(diary);
  await button(diary, "Open recording slot").click();
  await diary
    .getByLabel("Dream as remembered")
    .fill("QA draft: a blue square above a door.");
  await pause(diary);
  const record = await vault(diary, () =>
    button(diary, "Lock dream text").click(),
  );
  await align(diary);
  await diary.waitForTimeout(3500);
  out.dream = {
    phase: record.response.phase,
    media: await closeVideo(diary, dream, "dream"),
  };
  for (const id of [50, 54]) {
    const ctx = await video(),
      page = await ctx.newPage();
    const room = rooms.find((r) => r.id === id);
    await runPublic(page, room, target);
    await align(page);
    await pause(page);
    let record;
    if (id === 50)
      record = await exchange(page, "/api/future-study", () =>
        button(page, "Independent H").click(),
      );
    else {
      await button(page, "Cell 1,1").click();
      await pause(page);
      record = await exchange(page, "/api/future-study", () =>
        button(page, "Advance the cells").click(),
      );
      await page.locator(".cell-loom").waitFor();
      await page.locator(".cell-instrument").getByRole("slider").press("End");
    }
    await align(page);
    await page.waitForTimeout(3500);
    out[room.slug] = {
      request: record.wire,
      media: await closeVideo(page, ctx, room.slug),
    };
  }
  write("recordings", {
    scope: "Real mobile test-browser interactions. Blank start frames trimmed.",
    recordings: out,
  });
}

try {
  if (!process.argv.includes("--recordings-only")) await stills();
  if (!process.argv.includes("--stills-only")) await recordings();
} finally {
  await browser.close();
}
