// Actual browser frames and native-engine draws; no mocked reading or edited UI.
import { chromium } from "playwright";
import { mkdirSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
const base = process.env.FATE_CAPTURE_URL || "http://127.0.0.1:8010";
mkdirSync("../evidence/video-tmp", { recursive: true });
const browser = await chromium.launch({
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
});
const receipt = {
  kind: "Silent, unmodified real-browser screen recording. Real native three-card draw; no synthetic engine output or composed audio.",
  viewport: { width: 390, height: 844 },
  events: [],
};
try {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    recordVideo: {
      dir: "../evidence/video-tmp",
      size: { width: 390, height: 844 },
    },
  });
  const page = await context.newPage(),
    start = Date.now();
  const mark = (event) =>
    receipt.events.push({ event, seconds: (Date.now() - start) / 1000 });
  await page.goto(base);
  await page.locator('.orb[data-renderer="pixi"]').waitFor({ timeout: 20000 });
  mark("Orb ready");
  await page.waitForTimeout(2200);
  const r = await page.locator(".orb").boundingBox();
  await page.touchscreen.tap(r.x + r.width * 0.7, r.y + r.height * 0.48);
  mark("Touch light");
  await page.waitForTimeout(2200);
  await page
    .getByRole("button", { name: "Begin a reading", exact: true })
    .click();
  await page.locator(".ritual-deck").waitFor();
  await page.waitForTimeout(1400);
  mark("Ritual");
  const pending = page.waitForResponse((r) =>
    r.url().endsWith("/api/readings"),
  );
  await page.getByRole("button", { name: "Draw my three cards" }).click();
  receipt.nativeReading = (await (await pending).json()).result;
  mark("Native reading returned");
  await page.locator(".reveal-spread").scrollIntoViewIfNeeded();
  await page.waitForTimeout(600);
  for (let i = 1; i <= 3; i++) {
    await page
      .getByRole("button", { name: `Reveal card ${i}`, exact: true })
      .click();
    mark("Reveal " + i);
    await page.waitForTimeout(1350);
  }
  await page.waitForTimeout(1500);
  mark("Complete");
  const video = page.video();
  await context.close();
  await video.saveAs("../evidence/orb-and-card-reveal.webm");
  try {
    execFileSync(
      "ffmpeg",
      [
        "-y",
        "-i",
        "../evidence/orb-and-card-reveal.webm",
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
        "../evidence/orb-and-card-reveal.mp4",
      ],
      { stdio: "pipe" },
    );
    receipt.mp4 = true;
  } catch (error) {
    receipt.mp4 = false;
    console.log(
      "WebM saved. MP4 conversion unavailable:",
      error.message.split("\n")[0],
    );
  }
  writeFileSync("../evidence/recording.json", JSON.stringify(receipt, null, 2));
  console.log("Saved real orb / three-card reveal recording.");
} finally {
  await browser.close();
}
