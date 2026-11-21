import { chromium } from "@playwright/test";
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

process.chdir(fileURLToPath(new URL("../", import.meta.url)));
const origin = process.env.FATE_CAPTURE_ORIGIN ?? "http://127.0.0.1:8010";
const browser = await chromium.launch({channel:"chrome"});
const samples = [];
try {
  for (const [name, width, height] of [["mobile",390,844],["desktop",1440,900]]) {
    const context = await browser.newContext({
      viewport:{width,height}, isMobile:name==="mobile", hasTouch:name==="mobile", reducedMotion:"reduce",
    });
    try {
      const page = await context.newPage();
      const button = (name) => page.getByRole("button", {name,exact:true});
      await page.goto(origin + "/#vedic");
      await page.getByLabel("Date of birth", {exact:true}).fill("1990-07-15");
      await page.getByLabel("Recorded birth time").fill("14:30:00");
      await page.getByLabel("Birth city", {exact:true}).fill("London GB");
      await button("Find city").click();
      await page.getByRole("button",{name:/^London · GB/}).first().click();
      await page.getByLabel("I’ve checked the coordinates and timezone for my birthplace.").check();
      await page.getByLabel("Explore periods on this UTC day").fill("2026-11-20");
      const response = page.waitForResponse(r => r.url().endsWith("/api/chambers"));
      await button("Open my sidereal charts").click();
      const {result, snapshot, jyotish_reading: reading} = await (await response).json();
      await page.locator(".jyotish-opening").waitFor();
      await page.evaluate(() => document.fonts.ready);
      const capture = async (state, selector) => {
        await page.locator(selector).evaluate(el => el.scrollIntoView({block:"start",behavior:"instant"}));
        await page.screenshot({path:`../screenshots/16-jyotish-${state}-${name}.png`, animations:"disabled"});
      };
      await capture("reading", ".jyotish-opening");
      await button("D9 · Navamsa").click();
      await capture("dial", ".vedic-dial");
      await capture("comparison", ".jyotish-graha");
      await capture("periods", ".jyotish-timeline");
      samples.push({name,width,height,native:result,snapshot,reading, storage:await page.evaluate(()=>Object.keys(localStorage))});
    } finally {
      await context.close();
    }
  }
  writeFileSync("../evidence/block16-jyotish-media.json", JSON.stringify({
    fixture:"Synthetic London chart, mobile browser emulation",
    browser:browser.version(),
    verification:samples.map(({name,width,height,storage}) => ({name,width,height,storage})),
    native:samples[0].native, snapshot:samples[0].snapshot, reading:samples[0].reading,
  },null,2)+"\n");
} finally {
  await browser.close();
}
