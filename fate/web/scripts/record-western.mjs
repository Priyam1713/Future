import { chromium } from "@playwright/test";
import { writeFileSync, mkdirSync, copyFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { fillBirth, turnInstrument } from "./western-helpers.mjs";
process.chdir(fileURLToPath(new URL("../", import.meta.url)));
mkdirSync("../../tmp/western-video", { recursive: true });
const browser = await chromium.launch();
const c = await browser.newContext({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
  recordVideo: {
    dir: "../../tmp/western-video",
    size: { width: 390, height: 844 },
  },
});
try {
  const p = await c.newPage(),
    events = [],
    errors = [];
  p.on("pageerror", (e) => errors.push(e.message));
  const started = Date.now();
  await fillBirth(p);
  const response = p.waitForResponse((r) => r.url().endsWith("/api/western"));
  await p
    .getByRole("button", { name: "Open my celestial chart", exact: true })
    .click();
  const native = (await (await response).json()).result;
  await p.locator(".chart-reveal").waitFor();
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  const trim = (Date.now() - started) / 1000;
  const event = (action) =>
    events.push({ action, seconds: (Date.now() - started) / 1000 - trim });
  event("Native chart / Sun revealed");
  await p.waitForTimeout(1600);
  await p.getByRole("button", { name: "Reveal the next light" }).click();
  event("Moon");
  await p.waitForTimeout(1400);
  await p.getByRole("button", { name: "Reveal the next light" }).click();
  event("Ascendant");
  await p.waitForTimeout(1400);
  await p.getByRole("button", { name: "Enter my reading" }).click();
  await p
    .locator(".western-chart-layout")
    .evaluate((e) => e.scrollIntoView({ block: "start", behavior: "instant" }));
  await p.waitForTimeout(500);
  await p.getByRole("button", { name: "Explore Moon", exact: true }).click();
  event("Selected actual Moon");
  await p.waitForTimeout(800);
  await turnInstrument(p);
  event("Turned the actual instrument");
  await p.getByRole("button", { name: "Explore Venus", exact: true }).click();
  await p.waitForTimeout(600);
  await p
    .locator(".placement-focus")
    .evaluate((e) => e.scrollIntoView({ block: "center", behavior: "smooth" }));
  event("Source scope visible");
  await p.waitForTimeout(1700);
  const duration = (Date.now() - started) / 1000 - trim;
  const video = p.video();
  await c.close();
  copyFileSync(await video.path(), "../evidence/western-chart-source.webm");
  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-ss",
      trim.toFixed(3),
      "-i",
      "../evidence/western-chart-source.webm",
      "-t",
      duration.toFixed(3),
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
      "../evidence/western-chart.mp4",
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
        "../evidence/western-chart.mp4",
      ],
      { encoding: "utf8" },
    ),
  );
  if (errors.length) throw new Error(errors.join("\n"));
  writeFileSync(
    "../evidence/western-recording.json",
    JSON.stringify(
      {
        scope:
          "Actual native chart from an explicitly synthetic QA moment, not a person’s asserted birth. Real UI, live motion and direct interaction. Only initial form entry/calculation setup trimmed; no compositing, mocked native responses or soundtrack.",
        input: {
          local: "1990-07-15T14:30:00",
          zone: "Europe/London",
          latitude: native.birth.latitude,
          longitude: native.birth.longitude,
          houses: "whole-sign",
          fold: null,
        },
        native,
        trim,
        events,
        media,
      },
      null,
      2,
    ) + "\n",
  );
  console.log("Recorded", media.format.duration, "seconds");
} finally {
  await browser.close();
}
