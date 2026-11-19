import { chromium } from "@playwright/test";
import { writeFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
process.chdir(fileURLToPath(new URL("../", import.meta.url)));
mkdirSync("../screenshots", { recursive: true });
const browser = await chromium.launch({ headless: true });
import { fillBirth } from "./western-helpers.mjs";
for (const [name, viewport] of [
  ["mobile", { width: 390, height: 844 }],
  ["desktop", { width: 1440, height: 1000 }],
]) {
  const context = await browser.newContext({
    viewport,
    deviceScaleFactor: 1,
    isMobile: name === "mobile",
    hasTouch: name === "mobile",
  });
  const page = await context.newPage();
  await fillBirth(page);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({
    path: `../screenshots/40-western-input-${name}.png`,
    fullPage: true,
    animations: "disabled",
    scale: "css",
  });
  const response = page.waitForResponse((r) =>
    r.url().endsWith("/api/western"),
  );
  await page
    .getByRole("button", { name: "Open my celestial chart", exact: true })
    .click();
  const native = await (await response).json();
  await page.locator(".chart-reveal").waitFor();
  await page.waitForTimeout(400);
  await page.screenshot({
    path: `../screenshots/41-western-ritual-${name}.png`,
    fullPage: true,
    animations: "disabled",
    scale: "css",
  });
  await page.evaluate(() => scrollTo(0, 0));
  await page.screenshot({
    path: `../screenshots/45-western-ritual-viewport-${name}.png`,
    animations: "disabled",
    scale: "css",
  });
  await page
    .getByRole("button", { name: "Skip reveal & read my chart" })
    .click();
  await page.waitForTimeout(500);
  await page.getByRole("button", { name: "Explore Moon", exact: true }).click();
  await page.screenshot({
    path: `../screenshots/42-western-reading-${name}.png`,
    fullPage: true,
    animations: "disabled",
    scale: "css",
  });
  await page
    .locator(".western-chart-layout")
    .evaluate((e) => e.scrollIntoView({ block: "start", behavior: "instant" }));
  await page.screenshot({
    path: `../screenshots/43-western-chart-viewport-${name}.png`,
    animations: "disabled",
    scale: "css",
  });
  const before = await page.evaluate(() => ({ ...localStorage }));
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  const saved = await page.evaluate(() =>
    JSON.parse(localStorage.getItem("fate.codex.v1")),
  );
  await page
    .getByRole("button", { name: "Open in My Fate", exact: false })
    .click();
  await page.locator(".book-open").waitFor();
  await page.waitForTimeout(950);
  await page
    .locator(".celestial-book")
    .evaluate((e) => e.scrollIntoView({ block: "start" }));
  await page.screenshot({
    path: `../screenshots/44-western-codex-${name}.png`,
    animations: "disabled",
    scale: "css",
  });
  if (name === "mobile")
    writeFileSync(
      "../evidence/western-engine.json",
      JSON.stringify(
        {
          input: {
            local: "1990-07-15T14:30:00",
            zone: "Europe/London",
            latitude: native.result.birth.latitude,
            longitude: native.result.birth.longitude,
            houses: "whole-sign",
            fold: null,
          },
          native: native.result,
          beforeSaveStorage: before,
          saved,
        },
        null,
        2,
      ) + "\n",
    );
  await page.getByRole("link", { name: "Explore", exact: true }).click();
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
  const numberNative = (await (await numberResponse).json()).result;
  await page.getByRole("button", { name: "Go straight to my reading" }).click();
  await page
    .getByRole("button", { name: "Save to this device", exact: true })
    .click();
  await page.getByRole("link", { name: /My Fate/ }).click();
  await page.locator(".perspective-picker input").nth(0).check();
  await page.locator(".perspective-picker input").nth(1).check();
  await page
    .getByRole("button", { name: "Compare Perspectives", exact: false })
    .click();
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(600);
  await page.screenshot({
    path: `../screenshots/46-western-perspectives-${name}.png`,
    fullPage: true,
    animations: "disabled",
    scale: "css",
  });
  if (name === "mobile")
    writeFileSync(
      "../evidence/western-comparison.json",
      JSON.stringify(
        {
          scope:
            "Real UI comparison of explicitly saved native Western and Numerology snapshots; synthetic/public QA moments, no mocked outputs",
          western: native.result,
          numerology: numberNative,
          saved: await page.evaluate(() =>
            JSON.parse(localStorage.getItem("fate.codex.v1")),
          ),
          headings: await page.locator(".comparison-echo h4").allTextContents(),
        },
        null,
        2,
      ) + "\n",
    );
  await context.close();
}
await browser.close();
