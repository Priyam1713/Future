import { chromium } from "@playwright/test";
import { writeFileSync, mkdirSync, readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import {
  align,
  button,
  journeys,
  openRoom,
  perform,
} from "./manuscript-journeys.mjs";

const origin = process.env.FATE_CAPTURE_ORIGIN || "http://127.0.0.1:8010";
const sm = { width: 390, height: 844 };
const devices = {
  mobile: { viewport: sm, isMobile: true, hasTouch: true },
  desktop: { viewport: { width: 1440, height: 1000 } },
};
const frame = (page, name) =>
  page.screenshot({
    path: `../screenshots/09-${name}.png`,
    animations: "disabled",
  });
const write = (name, data) =>
  writeFileSync(
    `../evidence/block09-${name}.json`,
    JSON.stringify(data, null, 2) + "\n",
  );
const raw = "../../tmp/block09-video";
const recorded = new Set([7, 8, 40]);
const requested = process.argv.find((arg) => arg.startsWith("--rooms="));
const selected = requested
  ? requested.slice(8).split(",").map(Number)
  : journeys.map(({ id }) => id);
if (selected.some((id) => !journeys.some((row) => row.id === id)))
  throw Error("Unknown room in --rooms");
const read = (name) =>
  JSON.parse(readFileSync(`../evidence/block09-${name}.json`, "utf8"));
const browser = await chromium.launch({
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
});
mkdirSync(raw, { recursive: true });

async function ready(page, journey) {
  await openRoom(page, journey, origin);
  await page.evaluate(async () => {
    await document.fonts.ready;
    await document.querySelector(".folio-entrance img").decode();
  });
}

async function frameCadence(page) {
  return page.evaluate(async () => {
    const sample = [];
    let last = await new Promise(requestAnimationFrame);
    for (let i = 0; i < 65; i++) {
      const now = await new Promise(requestAnimationFrame);
      if (i >= 5) sample.push(now - last);
      last = now;
    }
    sample.sort((a, b) => a - b);
    return { p95Ms: sample[56], maxMs: sample.at(-1) };
  });
}

async function exploreResult(page, id) {
  if (id === 6)
    await page.getByRole("button", { name: /Libra ingress/ }).click();
  if (id === 7) {
    await page
      .getByRole("combobox", { name: "Planet", exact: true })
      .selectOption("Mars");
    await button(page, "ASC · Rising").click();
  }
  if (id >= 8 && id < 16 && id !== 8) {
    await page.locator(".folio-desk summary").first().click();
  }
  await align(page);
}

async function stills() {
  const reports = requested ? read("native").reports : {};
  const profiles = requested
    ? read("performance").profiles.filter(
        (row) => !selected.includes(row.oracle),
      )
    : [];
  for (const journey of journeys.filter(({ id }) => selected.includes(id))) {
    for (const [device, config] of Object.entries(devices)) {
      const ctx = await browser.newContext({ ...config, deviceScaleFactor: 1 });
      const page = await ctx.newPage();
      const errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      const start = performance.now();
      await ready(page, journey);
      const entranceMs = Math.round(performance.now() - start);
      if (recorded.has(journey.id))
        await frame(page, `${journey.slug}-entrance-${device}`);
      await align(page);
      const result = await perform(page, journey);
      await exploreResult(page, journey.id);
      const timing = await frameCadence(page);
      await frame(page, `${journey.slug}-${device}`);
      if (device === "mobile" && (journey.id === 5 || journey.id === 6)) {
        await align(page, ".result-leaf");
        await frame(page, `${journey.slug}-reading-mobile`);
      }
      if (device === "mobile") reports[journey.id] = result;
      profiles.push({
        oracle: journey.id,
        device,
        entranceMs,
        actionMs: result.actionMs,
        ...timing,
      });
      if (errors.length) throw Error(errors.join("\n"));
      console.log(journey.slug, device, result.actionMs, timing.p95Ms);
      await ctx.close();
    }
  }
  write("native", {
    scope: "Actual browser requests and unmodified native responses.",
    reports,
  });
  write("performance", {
    scope:
      "Local Chromium emulator, DPR 1, 60 retained frame callback intervals at the result. Action includes Playwright click, HTTP and visible result.",
    profiles,
  });
}

function videoMetrics(path, out) {
  const frames = execFileSync(
    "ffmpeg",
    [
      "-v",
      "error",
      "-i",
      path,
      "-t",
      "8",
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
  const stride = 52 * 112 * 3;
  let trim = 0,
    count = 0;
  for (let offset = 0; offset + stride <= frames.length; offset += stride) {
    let gray = 0;
    for (let i = offset; i < offset + stride; i += 3) {
      const [r, g, b] = [frames[i], frames[i + 1], frames[i + 2]];
      if (r > 90 && r < 160 && Math.abs(r - g) < 3 && Math.abs(r - b) < 3)
        gray++;
    }
    count = gray > (stride / 3) * 0.62 ? 0 : count + 1;
    if (count === 2) {
      trim = (offset / stride - 1) / 8;
      break;
    }
  }
  if (count < 2) throw Error("No full viewport in the screencast");
  execFileSync("ffmpeg", [
    "-v",
    "error",
    "-y",
    "-ss",
    String(trim),
    "-i",
    path,
    "-an",
    "-c:v",
    "libx264",
    "-crf",
    "20",
    "-pix_fmt",
    "yuv420p",
    "-movflags",
    "+faststart",
    out,
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
        out,
      ],
      { encoding: "utf8" },
    ),
  );
}

async function videos() {
  const recordings = requested ? read("recordings").recordings : {};
  for (const journey of journeys.filter(
    ({ id }) => recorded.has(id) && selected.includes(id),
  )) {
    const ctx = await browser.newContext({
      ...devices.mobile,
      recordVideo: { dir: raw, size: sm },
    });
    const page = await ctx.newPage();
    await ready(page, journey);
    await align(page);
    const pause = () => page.waitForTimeout(650);
    await pause();
    if (journey.id === 40) {
      const dial = await page.locator(".compass-instrument svg").boundingBox();
      await page.touchscreen.tap(
        dial.x + dial.width * 0.5,
        dial.y + dial.height * 0.19,
      );
      await pause();
      await page.touchscreen.tap(
        dial.x + dial.width * 0.82,
        dial.y + dial.height * 0.49,
      );
      await pause();
      await page.getByLabel("Bearing (°)", { exact: true }).fill("97.5");
    }
    const result = await perform(page, journey, pause);
    await pause();
    await exploreResult(page, journey.id);
    if (journey.id === 7) {
      await pause();
      await button(page, "Zoom map in").click();
    }
    await page.waitForTimeout(2300);
    const video = page.video();
    await ctx.close();
    recordings[journey.slug] = {
      request: result.request,
      media: videoMetrics(
        await video.path(),
        `../evidence/block09-${journey.slug}.mp4`,
      ),
    };
    console.log(journey.slug, "recorded");
  }
  write("recordings", {
    scope: "Real browser interactions; gray startup frames trimmed.",
    recordings,
  });
}

try {
  await stills();
  await videos();
} finally {
  await browser.close();
}
