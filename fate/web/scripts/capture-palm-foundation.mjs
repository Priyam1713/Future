import { chromium } from "@playwright/test";
import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";

const origin = process.env.FATE_CAPTURE_ORIGIN ?? "http://127.0.0.1:8014";
const raw = "../../tmp/block13-media";
mkdirSync(raw, { recursive: true });
const browser = await chromium.launch({ channel: "chrome" });
const receipts = {};
try {
  for (const [name, width, height] of [
    ["mobile", 390, 844],
    ["desktop", 1440, 900],
  ]) {
    const viewport = { width, height };
    const context = await browser.newContext({
      viewport,
      isMobile: width === 390,
      hasTouch: width === 390,
      deviceScaleFactor: 1,
      recordVideo: { dir: raw, size: viewport },
    });
    const page = await context.newPage();
    await page.addInitScript(() => {
      const NativeAudio = window.Audio;
      window.palmQaAudio = [];
      window.Audio = class extends NativeAudio {
        constructor(url) {
          super(url);
          window.palmQaAudio.push(this);
        }
      };
    });
    const wait = (ms) => page.waitForTimeout(ms);
    const screenshot = async (stage) => {
      await page.screenshot({
        path: `../screenshots/13-palm-${stage}-${name}.png`,
        animations: "disabled",
      });
    };
    try {
      await page.goto(origin + "/#palmistry");
      await page.getByLabel("I have permission to review this photo").check();
      await page
        .getByLabel("Palm photograph")
        .setInputFiles("../../workbench/tests/assets/palm-cc0.png");
      const photo = page.getByAltText("Your selected palm for manual review");
      await photo.waitFor();
      await photo.scrollIntoViewIfNeeded();
      const box = await photo.boundingBox();
      for (const [x, y] of [
        [0.49, 0.52],
        [0.54, 0.59],
        [0.59, 0.64],
      ]) {
        await page.mouse.click(box.x + box.width * x, box.y + box.height * y);
        await wait(420);
      }
      await screenshot("overlay");
      await page.getByLabel("Photographed hand").selectOption("left");
      await page.getByLabel("Head line shape").selectOption("slight_slope");
      await page
        .getByLabel("Heart line endpoint toward the index finger")
        .selectOption("jupiter");
      await page
        .getByLabel("I confirmed these descriptions against the photo")
        .check();
      const pending = page.waitForResponse((r) =>
        r.url().endsWith("/api/palm-reading"),
      );
      await page.getByRole("button", { name: "Open my palm reading" }).click();
      const response = await pending;
      if (!response.ok()) throw Error(await response.text());
      const report = await response.json();
      await page.locator(".palm-report").waitFor();
      await page
        .locator(".palm-report")
        .evaluate((section) =>
          section.scrollIntoView({ block: "start", behavior: "instant" }),
        );
      await wait(650);
      await screenshot("reading");
      await wait(1450);
      const audio = await page.evaluate(() => {
        const stream = window.palmQaAudio.find((item) =>
          item.src.endsWith("/art/fate-ambient-v2.wav"),
        );
        return (
          stream && {
            playing: !stream.paused,
            loop: stream.loop,
            seconds: stream.currentTime,
            volume: stream.volume,
          }
        );
      });
      if (!audio?.playing || !audio.loop || audio.seconds <= 0)
        throw Error("Ambient playback did not advance");
      const wrappedAt = await page.evaluate(async () => {
        const stream = window.palmQaAudio.find((item) =>
          item.src.endsWith("/art/fate-ambient-v2.wav"),
        );
        const sought = new Promise((resolve) =>
          stream.addEventListener("seeked", resolve, { once: true }),
        );
        stream.currentTime = stream.duration - 0.15;
        await sought;
        await new Promise((resolve) => setTimeout(resolve, 430));
        return stream.currentTime;
      });
      if (wrappedAt >= 1.5)
        throw Error("Ambient playback did not wrap to the beginning");
      const video = page.video();
      await context.close();
      const path = `../evidence/block13-palm-${name}.mp4`;
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
        "20",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        path,
      ]);
      receipts[name] = {
        audio: { ...audio, wrappedAt },
        request: response.request().postDataJSON(),
        chapters: report.narrative,
        video: JSON.parse(
          execFileSync(
            "ffprobe",
            [
              "-v",
              "error",
              "-show_entries",
              "stream=codec_name,width,height:format=duration",
              "-of",
              "json",
              path,
            ],
            { encoding: "utf8" },
          ),
        ),
      };
    } finally {
      await context.close();
    }
  }
  writeFileSync(
    "../evidence/block13-palm-media.json",
    JSON.stringify(
      {
        scope:
          "Real browser workflow and known CC0 photo with scripted manual descriptors and overlays. The exercise does not establish recognition accuracy.",
        browser: browser.version(),
        receipts,
      },
      null,
      2,
    ) + "\n",
  );
} finally {
  await browser.close();
}
