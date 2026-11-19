import { chromium } from "@playwright/test";
import { writeFileSync, mkdirSync, copyFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { enterTurning } from "./turning-helpers.mjs";
const browser = await chromium.launch();
mkdirSync("../../tmp/turning-video", { recursive: true });
const c = await browser.newContext({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
  recordVideo: {
    dir: "../../tmp/turning-video",
    size: { width: 390, height: 844 },
  },
});
try {
  const p = await c.newPage(),
    errors = [],
    events = [];
  p.on("pageerror", (e) => errors.push(e.message));
  const started = Date.now();
  const data = await enterTurning(p, 30);
  await p
    .locator(".turning-layout")
    .evaluate((e) => e.scrollIntoView({ block: "start", behavior: "instant" }));
  await p.waitForTimeout(400);
  const trim = (Date.now() - started) / 1000;
  const mark = (action) =>
    events.push({ action, seconds: (Date.now() - started) / 1000 - trim });
  mark("Native 30-day window");
  await p.waitForTimeout(1000);
  const slider = p.getByRole("slider", { name: "Explore the daily sky" });
  await slider.focus();
  for (let i = 0; i < 4; i++) {
    await p.keyboard.press("ArrowRight");
    await p.waitForTimeout(450);
  }
  mark("Scrubbed actual daily ephemeris samples");
  await p.getByRole("checkbox", { name: "Show the entire window" }).check();
  await p.locator(".event-track").nth(6).click();
  mark("Selected an exact native contact");
  await p.waitForTimeout(1700);
  await p.getByRole("button", { name: "Staying in orb", exact: true }).click();
  await p
    .locator(".turning-timeline")
    .evaluate((e) => e.scrollIntoView({ block: "start", behavior: "smooth" }));
  await p.waitForTimeout(1300);
  mark("Native orb-duration bands");
  await p.getByRole("button", { name: "Repeated paths", exact: true }).click();
  await p.waitForTimeout(1200);
  if (data.result.report.presentation.repeated_patterns.length) {
    await p
      .locator(".repeated-tracks article")
      .first()
      .getByRole("button")
      .last()
      .click();
    await p
      .locator(".turning-layout")
      .evaluate((e) =>
        e.scrollIntoView({ block: "start", behavior: "smooth" }),
      );
    mark("A repeated pass inside the same window");
    await p.waitForTimeout(1800);
  }
  const duration = (Date.now() - started) / 1000 - trim;
  const video = p.video();
  await c.close();
  copyFileSync(await video.path(), "../evidence/turning-sky-source.webm");
  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-ss",
      String(trim),
      "-i",
      "../evidence/turning-sky-source.webm",
      "-t",
      String(duration),
      "-c:v",
      "libx264",
      "-preset",
      "slow",
      "-crf",
      "18",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      "-an",
      "../evidence/turning-sky.mp4",
    ],
    { stdio: "pipe" },
  );
  const media = JSON.parse(
    execFileSync(
      "ffprobe",
      [
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        "../evidence/turning-sky.mp4",
      ],
      { encoding: "utf8" },
    ),
  );
  if (errors.length) throw new Error(errors.join("\n"));
  writeFileSync(
    "../evidence/turning-recording.json",
    JSON.stringify(
      {
        scope:
          "Actual native 30-day transit calculation over synthetic QA natal moment. Live UI, no mocked results or compositing. Only initial input/computation setup trimmed; no soundtrack.",
        trim,
        events,
        natal: data.natal,
        result: data.result,
        media,
      },
      null,
      2,
    ) + "\n",
  );
  console.log(
    "Recorded",
    media.format.duration,
    "seconds;",
    data.result.report.presentation.repeated_patterns.length,
    "real repeated sequences",
  );
} finally {
  await browser.close();
}
