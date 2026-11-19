import { chromium } from "@playwright/test";
import { writeFileSync } from "node:fs";
import { enterTurning } from "./turning-helpers.mjs";
const browser = await chromium.launch();
try {
  for (const [name, viewport] of [
    ["mobile", { width: 390, height: 844 }],
    ["desktop", { width: 1440, height: 1000 }],
  ]) {
    const c = await browser.newContext({
      viewport,
      deviceScaleFactor: 1,
      isMobile: name === "mobile",
      hasTouch: name === "mobile",
    });
    const p = await c.newPage(),
      errors = [];
    p.on("pageerror", (e) => errors.push(e.message));
    const data = await enterTurning(p);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({
      path: `../screenshots/50-turning-overview-${name}.png`,
      fullPage: true,
      animations: "disabled",
      scale: "css",
    });
    await p
      .locator(".turning-layout")
      .evaluate((e) =>
        e.scrollIntoView({ block: "start", behavior: "instant" }),
      );
    await p.screenshot({
      path: `../screenshots/51-turning-instrument-${name}.png`,
      animations: "disabled",
      scale: "css",
    });
    await p.getByRole("checkbox", { name: "Show the entire window" }).check();
    await p.locator(".event-track").first().click();
    await p.waitForTimeout(500);
    await p.screenshot({
      path: `../screenshots/52-turning-contact-${name}.png`,
      animations: "disabled",
      scale: "css",
    });
    await p
      .getByRole("button", { name: "Staying in orb", exact: true })
      .click();
    await p
      .locator(".turning-timeline")
      .evaluate((e) =>
        e.scrollIntoView({ block: "start", behavior: "instant" }),
      );
    await p.screenshot({
      path: `../screenshots/53-turning-durations-${name}.png`,
      animations: "disabled",
      scale: "css",
    });
    await p
      .getByRole("button", {
        name: "Save transit chapter to this device",
        exact: false,
      })
      .click();
    const saved = await p.evaluate(() =>
      JSON.parse(localStorage.getItem("fate.codex.v1")),
    );
    await p
      .getByRole("button", { name: "Open in My Fate", exact: false })
      .click();
    await p.locator(".book-open").waitFor();
    await p.waitForTimeout(950);
    await p
      .locator(".celestial-book")
      .evaluate((e) =>
        e.scrollIntoView({ block: "start", behavior: "instant" }),
      );
    await p.screenshot({
      path: `../screenshots/54-turning-codex-${name}.png`,
      animations: "disabled",
      scale: "css",
    });
    if (errors.length) throw new Error(errors.join("\n"));
    if (name === "mobile")
      writeFileSync(
        "../evidence/turning-engine.json",
        JSON.stringify(
          {
            scope:
              "Synthetic QA natal moment and explicit UTC transit window; actual native responses, not a personal-event prediction.",
            natal: data.natal,
            result: data.result,
            saved,
            originShape: Object.keys(data.origin),
            birthFieldsExcludedFromBasis: !("birth" in data.origin.natal),
          },
          null,
          2,
        ) + "\n",
      );
    console.log(
      "Captured",
      name,
      "events",
      data.result.report.exact_events.length,
      "saved bytes",
      JSON.stringify(saved).length,
    );
    await c.close();
  }
} finally {
  await browser.close();
}
