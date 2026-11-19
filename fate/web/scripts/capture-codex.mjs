// Real completed readings, explicit saves, a refresh, a cover and real chapters.
// Only initial reading setup is trimmed from the live recording.
import { chromium } from "@playwright/test";
import { writeFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
const browser = await chromium.launch({
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
});
mkdirSync("../evidence/video-tmp", { recursive: true });
async function savePair(page, beforeSecondSave = async () => {}) {
  await page.goto("http://127.0.0.1:8010");
  await page.locator(".room-index button").first().click();
  const tarotResponse = page.waitForResponse((r) =>
    r.url().endsWith("/api/readings"),
  );
  await page.getByRole("button", { name: "Draw my three cards" }).click();
  const tarot = (await (await tarotResponse).json()).result;
  await page.getByRole("button", { name: "Skip reveal & read now" }).click();
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Explore Numerology", exact: true })
    .click();
  await page.getByLabel("Your full name").fill("Ada Lovelace");
  await page.getByLabel("Date of birth", { exact: true }).fill("1815-12-10");
  await page.getByLabel("Date to explore").fill("2026-11-19");
  const numberResponse = page.waitForResponse((r) =>
    r.url().endsWith("/api/numerology"),
  );
  await page.getByRole("button", { name: "Awaken my numbers" }).click();
  const numerology = (await (await numberResponse).json()).result;
  await page.getByRole("button", { name: "Go straight to my reading" }).click();
  await beforeSecondSave();
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  return { tarot, numerology };
}
async function open(page) {
  await page.getByRole("button", { name: "Open your Codex" }).click();
  await page.waitForTimeout(1000);
}
async function compare(page) {
  await page.locator(".perspective-picker input").nth(0).check();
  await page.locator(".perspective-picker input").nth(1).check();
  await page
    .getByRole("button", { name: "Compare Perspectives", exact: false })
    .click();
  await page.waitForTimeout(650);
}
async function pause(page) {
  await page.getByRole("button", { name: "About FATE and settings" }).click();
  await page
    .getByRole("dialog")
    .getByRole("button", { name: "Pause motion", exact: true })
    .click();
  await page.keyboard.press("Escape");
}
async function still(page, path, fullPage = false) {
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.screenshot({ path, fullPage, timeout: 90000 });
}
const receipt = {
  kind: "Silent live real-browser Codex recording. Actual native results and explicit device saves. Initial reading setup trimmed; no response mocks, composited UI or composed audio.",
  viewport: { width: 390, height: 844 },
  events: [],
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
  receipt.native = await savePair(page, async () => {
    await page.locator(".save-chapter").scrollIntoViewIfNeeded();
    await page.waitForTimeout(600);
    receipt.trimStartSeconds = (Date.now() - start) / 1000;
    mark("Explicit save disclosure");
    await page.waitForTimeout(900);
  });
  mark("Numerology chapter saved");
  await page.waitForTimeout(700);
  await page.getByRole("link", { name: /My Fate/ }).click();
  await page.waitForTimeout(800);
  mark("Illustrated Codex and growing collection");
  await page.waitForTimeout(1200);
  await open(page);
  mark("Cover opens to a real saved Tarot chapter");
  await page.waitForTimeout(900);
  await page.getByRole("button", { name: "Next chapter", exact: true }).click();
  mark("Turn to saved Numerology");
  await page.waitForTimeout(1500);
  const persisted = await page.evaluate(() =>
    JSON.parse(localStorage.getItem("fate.codex.v1")),
  );
  receipt.persisted = persisted;
  await page.reload();
  await page.waitForTimeout(800);
  await open(page);
  mark("Refresh retains both chapters");
  await page.waitForTimeout(800);
  await compare(page);
  mark("Compare cited source perspectives");
  await page.waitForTimeout(1500);
  const video = page.video();
  await context.close();
  await video.saveAs("../evidence/codex-interaction-source.webm");
  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-ss",
      String(receipt.trimStartSeconds),
      "-i",
      "../evidence/codex-interaction-source.webm",
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
      "../evidence/codex-interaction.mp4",
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
        "../evidence/codex-interaction.mp4",
      ],
      { encoding: "utf8" },
    ),
  );
  writeFileSync(
    "../evidence/codex-recording.json",
    JSON.stringify(receipt, null, 2),
  );
  console.log("Recorded real Codex interaction", receipt.media.format.duration);
  for (const device of [
    { name: "mobile", width: 390, height: 844, dpr: 2 },
    { name: "desktop", width: 1440, height: 1000, dpr: 1 },
  ]) {
    const c = await browser.newContext({
      viewport: { width: device.width, height: device.height },
      deviceScaleFactor: device.dpr,
      isMobile: device.name === "mobile",
      hasTouch: device.name === "mobile",
    });
    const p = await c.newPage();
    const errors = [];
    p.on("pageerror", (e) => errors.push(e.message));
    await savePair(p);
    await p.getByRole("link", { name: /My Fate/ }).click();
    await pageReady(p);
    await pause(p);
    await p.evaluate(() => scrollTo(0, 0));
    await still(p, `../screenshots/30-codex-cover-${device.name}.png`, true);
    await p.evaluate(() => scrollTo(0, 0));
    await still(p, `../screenshots/34-codex-cover-viewport-${device.name}.png`);
    await open(p);
    await still(p, `../screenshots/32-codex-tarot-${device.name}.png`, true);
    await p
      .locator(".celestial-book")
      .evaluate((el) =>
        el.scrollIntoView({ block: "start", behavior: "instant" }),
      );
    await still(p, `../screenshots/35-codex-tarot-viewport-${device.name}.png`);
    await p.getByRole("button", { name: "Next chapter", exact: true }).click();
    await p.waitForTimeout(800);
    await still(p, `../screenshots/31-codex-open-${device.name}.png`, true);
    await p
      .locator(".celestial-book")
      .evaluate((el) =>
        el.scrollIntoView({ block: "start", behavior: "instant" }),
      );
    await still(
      p,
      `../screenshots/36-codex-numerology-viewport-${device.name}.png`,
    );
    await compare(p);
    await still(p, `../screenshots/33-compare-${device.name}.png`, true);
    await p.getByRole("link", { name: "54 techniques", exact: true }).click();
    await pageReady(p);
    await still(p, `../screenshots/37-collection-${device.name}.png`, true);
    await p.evaluate(() => scrollTo(0, 0));
    await still(p, `../screenshots/38-collection-viewport-${device.name}.png`);
    if (errors.length) throw new Error(errors.join("\n"));
    console.log("Captured settled native", device.name);
    await c.close();
  }
} finally {
  await browser.close();
}
async function pageReady(page) {
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
}
