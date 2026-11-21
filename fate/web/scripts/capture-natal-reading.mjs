import { chromium } from "@playwright/test";
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { fillBirth } from "./western-helpers.mjs";

process.chdir(fileURLToPath(new URL("../", import.meta.url)));
const origin = process.env.FATE_CAPTURE_ORIGIN ?? "http://127.0.0.1:8010";
const browser = await chromium.launch({ channel: "chrome" });
const receipts = [];
try {
  for (const [name, width, height] of [["mobile", 390, 844], ["desktop", 1440, 900]]) {
    const context = await browser.newContext({
      viewport: { width, height },
      isMobile: name === "mobile",
      hasTouch: name === "mobile",
      reducedMotion: "reduce",
    });
    try {
      const page = await context.newPage();
      await fillBirth(page, origin);
      const response = page.waitForResponse((item) => item.url().endsWith("/api/western"));
      await page.getByRole("button", { name: "Open my celestial chart", exact: true }).click();
      const { result, natal_reading } = await (await response).json();
      await page.getByRole("button", { name: "Skip reveal & read my chart" }).click();
      await page.evaluate(() => document.fonts.ready);
      const screenshot = (stage) => page.screenshot({
        path: `../screenshots/15-natal-${stage}-${name}.png`,
        animations: "disabled",
      });
      await screenshot("opening");
      const story = page.getByRole("region", { name: "Natal reading" });
      await story.getByRole("button", { name: "Themes", exact: true }).click();
      await story.locator(".natal-chapters").evaluate((el) => el.scrollIntoView({ block: "start" }));
      await screenshot("themes");
      await story.getByRole("link", { name: "Explore the chart" }).click();
      const inspector = page.getByRole("region", { name: "Selected chart detail" });
      await inspector.getByLabel("Choose an aspect").selectOption("aspect:Sun-Moon:90");
      if (name === "mobile") await inspector.locator("h2").evaluate((el) => el.scrollIntoView({ block: "center" }));
      else await page.locator("#western-instrument").evaluate((el) => el.scrollIntoView({ block: "start" }));
      await screenshot("aspect");
      receipts.push({
        name, width, height, profile: natal_reading.profile,
        angles: result.angles, houseCusps: result.house_cusps, aspects: result.aspects,
        chapterIds: natal_reading.chapters.map((chapter) => chapter.id),
        selected: natal_reading.focuses["aspect:Sun-Moon:90"],
        patterns: natal_reading.patterns,
        storageKeys: await page.evaluate(() => Object.keys(localStorage)),
      });
    } finally {
      await context.close();
    }
  }
  writeFileSync("../evidence/block15-western-media.json", JSON.stringify({
    browser: browser.version(),
    fixture: "Synthetic QA moment; mobile browser emulation.",
    receipts,
  }, null, 2) + "\n");
} finally {
  await browser.close();
}
