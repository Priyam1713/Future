// Final settled real-browser stills; motion paused through the real control.
// The separate recording captures live motion. No response mocks or AI calls.
import { chromium } from "@playwright/test";
const browser = await chromium.launch({
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
});
async function settled(page) {
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  await page.evaluate(() => scrollTo(0, 0));
}
try {
  for (const device of [
    { name: "mobile", width: 390, height: 844, dpr: 2 },
    { name: "desktop", width: 1440, height: 1000, dpr: 1 },
  ]) {
    const context = await browser.newContext({
      viewport: { width: device.width, height: device.height },
      deviceScaleFactor: device.dpr,
      isMobile: device.name === "mobile",
      hasTouch: device.name === "mobile",
    });
    const page = await context.newPage();
    const errors = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await page.goto("http://127.0.0.1:8010");
    await page.locator(".gallery-intro").scrollIntoViewIfNeeded();
    await page.locator(".gallery-intro img").evaluate((el) => el.decode());
    await page
      .locator(".number-door .dial-brass")
      .evaluate((el) => el.decode());
    await page.locator(".motion-control").click();
    await settled(page);
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: `../screenshots/${device.name === "mobile" ? "20" : "24"}-gallery-${device.name}.png`,
      fullPage: true,
    });
    await page.screenshot({
      path: `../screenshots/28-gallery-viewport-${device.name}.png`,
    });
    await page
      .getByRole("button", { name: "Explore Numerology", exact: true })
      .click();
    await page.locator(".number-form").waitFor();
    await settled(page);
    await page.locator(".dial-brass").evaluate((el) => el.decode());
    await page.screenshot({
      path: `../screenshots/${device.name === "mobile" ? "21" : "25"}-numerology-input-${device.name}.png`,
      fullPage: true,
    });
    await page.getByLabel("Your full name").fill("Ada Lovelace");
    await page.getByLabel("Date of birth", { exact: true }).fill("1815-12-10");
    await page.getByLabel("Date to explore").fill("2026-11-19");
    await page.getByRole("button", { name: "Awaken my numbers" }).click();
    await page.locator(".number-seal").waitFor();
    await settled(page);
    await page.screenshot({
      path: `../screenshots/${device.name === "mobile" ? "22" : "26"}-numerology-ritual-${device.name}.png`,
      fullPage: true,
    });
    await page.screenshot({
      path: `../screenshots/29-numerology-ritual-viewport-${device.name}.png`,
    });
    await page
      .getByRole("button", { name: "Go straight to my reading" })
      .click();
    await page.locator(".number-themes").waitFor();
    await settled(page);
    await page.screenshot({
      path: `../screenshots/${device.name === "mobile" ? "23" : "27"}-numerology-reading-${device.name}.png`,
      fullPage: true,
    });
    if (errors.length) throw new Error(errors.join("\n"));
    console.log("Captured settled native", device.name);
    await context.close();
  }
} finally {
  await browser.close();
}
