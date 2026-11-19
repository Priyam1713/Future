// Real browser and real native result. Only the initial form setup is trimmed.
import { chromium } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
mkdirSync("../evidence/video-tmp", { recursive: true });
const browser = await chromium.launch({
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
});
const receipt = {
  kind: "Silent real-browser capture; initial form setup trimmed, no composited UI or fabricated engine output",
  viewport: { width: 390, height: 844 },
  events: [],
  input: {
    name: "Ada Lovelace",
    birth: "1815-12-10",
    target: "2026-11-19",
    basis: "birth",
    y_roles: "",
  },
};
try {
  const context = await browser.newContext({
    viewport: receipt.viewport,
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    recordVideo: { dir: "../evidence/video-tmp", size: receipt.viewport },
  });
  const page = await context.newPage();
  const start = Date.now();
  const mark = (event) =>
    receipt.events.push({ event, seconds: (Date.now() - start) / 1000 });
  await page.goto("http://127.0.0.1:8010");
  await page
    .getByRole("button", { name: "Explore Numerology", exact: true })
    .click();
  await page.getByLabel("Your full name").fill(receipt.input.name);
  await page
    .getByLabel("Date of birth", { exact: true })
    .fill(receipt.input.birth);
  await page.getByLabel("Date to explore").fill(receipt.input.target);
  const response = page.waitForResponse((r) =>
    r.url().endsWith("/api/numerology"),
  );
  await page.getByRole("button", { name: "Awaken my numbers" }).click();
  receipt.nativeReading = (await (await response).json()).result;
  await page.locator(".number-seal").waitFor();
  await page.waitForTimeout(650);
  await page.evaluate(() => scrollTo(0, 0));
  receipt.trimStartSeconds = (Date.now() - start) / 1000;
  mark("Expression seal, source theme and living dial");
  await page.waitForTimeout(2400);
  await page.getByRole("button", { name: "Turn the celestial dial" }).tap();
  mark("Tactile turn");
  await page.waitForTimeout(1800);
  await page.getByRole("button", { name: "Reveal the next seal" }).click();
  mark("Personal Year seal");
  await page.waitForTimeout(2600);
  await page.getByRole("button", { name: "Reveal the next seal" }).click();
  mark("Birth-date framework seal");
  await page.waitForTimeout(2500);
  await page.getByRole("button", { name: "Read my constellation" }).click();
  mark("Reading");
  await page.waitForTimeout(1200);
  await page.locator(".number-themes").scrollIntoViewIfNeeded();
  await page.waitForTimeout(2400);
  mark("Source-grounded payoff");
  const video = page.video();
  await context.close();
  await video.saveAs("../evidence/numerology-ritual-source.webm");
  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-ss",
      String(receipt.trimStartSeconds),
      "-i",
      "../evidence/numerology-ritual-source.webm",
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
      "../evidence/numerology-ritual.mp4",
    ],
    { stdio: "pipe" },
  );
  receipt.media = JSON.parse(
    execFileSync(
      "ffprobe",
      [
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        "../evidence/numerology-ritual.mp4",
      ],
      { encoding: "utf8" },
    ),
  );
  writeFileSync(
    "../evidence/numerology-recording.json",
    JSON.stringify(receipt, null, 2),
  );
  console.log(
    "Saved native Numerology ritual recording",
    receipt.media.format.duration,
  );
} finally {
  await browser.close();
}
