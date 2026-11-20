import { chromium, devices, firefox, webkit } from "@playwright/test";
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import {
  align,
  blindTrial,
  button,
  exchange,
  rooms,
  runPublic,
} from "./future-journeys.mjs";

const current = process.env.FATE_CAPTURE_ORIGIN ?? "http://127.0.0.1:8011";
const baseline = process.env.FATE_BASELINE_ORIGIN ?? "http://127.0.0.1:8012";
const dimensions = {
  mobile: { width: 390, height: 844 },
  desktop: { width: 1440, height: 1000 },
};
const raw = "../../tmp/block11-video";
mkdirSync(raw, { recursive: true });
const webkitOnly = process.argv.includes("--webkit-only");
const firefoxOnly = process.argv.includes("--firefox-only");
const browser = webkitOnly
  ? await webkit.launch()
  : firefoxOnly
    ? await firefox.launch()
    : await chromium.launch({
        args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
      });
const context = (mode, record = false) =>
  browser.newContext({
    viewport: dimensions[mode],
    deviceScaleFactor: 1,
    isMobile: mode === "mobile",
    hasTouch: mode === "mobile",
    ...(record && { recordVideo: { dir: raw, size: dimensions[mode] } }),
  });
const save = (name, value) =>
  writeFileSync(
    `../evidence/block11-${name}.json`,
    JSON.stringify(value, null, 2) + "\n",
  );
const clip = (name) => `../evidence/block11-${name}.mp4`;
const wait = (page, time = 600) => page.waitForTimeout(time);
const shot = async (page, name, mode, selector, fullPage = false) => {
  if (selector) await align(page, selector);
  await page.evaluate(async (includeBelowFold) => {
    await document.fonts.ready;
    const images = [...document.querySelectorAll("main picture img")].filter(
      (img) => {
        const b = img.getBoundingClientRect();
        return includeBelowFold || (b.bottom > 0 && b.top < innerHeight);
      },
    );
    await Promise.all(images.map((img) => img.decode()));
  }, fullPage);
  await wait(page, 370);
  await page.screenshot({
    path: `../screenshots/11-${name}-${mode}.png`,
    animations: "disabled",
    fullPage,
  });
};

async function matchLab(page, id, origin) {
  return runPublic(
    page,
    rooms.find((room) => room.id === id),
    origin,
  );
}

async function updateLab(page, id, before = false) {
  const action = async () => {
    if (id === 50) await button(page, "Independent H").click();
    if (id === 58) {
      await page.getByRole("slider").press("End");
      await button(page, before ? "Run model" : "Update market quote").click();
    }
    if (id === 59) await button(page, "21 units").click();
  };
  const change = await exchange(page, "/api/future-study", action);
  await page.locator('.future-apparatus[aria-busy="false"]').waitFor();
  return change;
}

async function fillWestern(page) {
  await page.goto(current + "/#western");
  await page.getByLabel("Date of birth", { exact: true }).fill("1990-07-15");
  await page.getByLabel("Recorded birth time").fill("14:30:00");
  await page.getByLabel("Birth city", { exact: true }).fill("London GB");
  await button(page, "Find city").click();
  await page
    .getByRole("button", { name: /^London · GB/ })
    .first()
    .click();
  await page
    .getByLabel("I’ve checked the coordinates and timezone for my birthplace.")
    .check();
  return exchange(page, "/api/western", () =>
    button(page, "Open my celestial chart").click(),
  );
}

async function num(page) {
  await page.goto(current + "/#numerology");
  await page.getByLabel("Your full name").fill("Ada Lovelace");
  await page.getByLabel("Date of birth", { exact: true }).fill("1815-12-10");
  await page.getByLabel("Date to explore").fill("2026-11-19");
  return exchange(page, "/api/numerology", () =>
    button(page, "Awaken my numbers").click(),
  );
}

async function tarot(page) {
  await page.route("**/api/readings", (route) =>
    route.continue({
      postData: JSON.stringify({
        ...route.request().postDataJSON(),
        seed: "2f".padStart(64, "0"),
      }),
    }),
  );
  await page.goto(current + "/#ritual");
  return exchange(page, "/api/readings", () =>
    button(page, "Draw my three cards").click(),
  );
}

const tasks = {
  gallery: async (page, mode, record) => {
    await page.goto(current + "/#gallery");
    await page.locator(".world-door").first().waitFor();
    await shot(page, "gallery", mode);
    await align(page, ".world-door:last-child");
    await page
      .locator(".world-door:last-child img")
      .evaluate((image) => image.decode());
    await page.evaluate(() => window.scrollTo({ top: 0, behavior: "instant" }));
    await shot(page, "gallery-doors", mode, undefined, true);
    await button(page, "The Tomorrow Machine").click();
    await shot(page, "world", mode, ".interior-heading");
    if (record) {
      await button(page, "All worlds").click();
      await page.getByRole("searchbox").fill("lorenz");
      await wait(page, 700);
      await page.getByRole("link", { name: "Enter Lorenz Chaos" }).click();
      await page.locator(".lab-payoff").waitFor();
    }
  },
  tarot: async (page, mode, record) => {
    const drawn = await tarot(page);
    await align(page, ".card-table");
    for (let i = 1; i <= drawn.response.result.readings.length; i++) {
      await button(page, `Reveal card ${i}`).click();
      if (record) await wait(page, 680);
    }
    await shot(page, "tarot-turn", mode, ".card-table");
    await button(page, "Open my reading").click();
    await shot(page, "tarot", mode, ".page-heading");
    return {
      cards: drawn.response.result.readings.map(({ card, orientation }) => [
        card.id,
        orientation,
      ]),
    };
  },
  numerology: async (page, mode, record) => {
    const drawn = await num(page);
    await align(page, ".number-room-layout");
    await button(page, "Turn the celestial dial").click();
    if (record) await wait(page, 650);
    await button(page, "Reveal the next seal").click();
    if (record) await wait(page, 700);
    await shot(page, "numerology", mode, ".number-room-layout");
    await button(page, "Reveal the next seal").click();
    await button(page, "Read my constellation").click();
    if (record) await align(page, ".number-themes");
    return { expression: drawn.response.result.expression.result };
  },
  western: async (page, mode, record) => {
    const natal = await fillWestern(page);
    await page.locator(".chart-reveal").waitFor();
    if (record) await wait(page, 500);
    await button(page, "Reveal the next light").click();
    if (record) await wait(page, 650);
    await button(page, "Reveal the next light").click();
    await button(page, "Enter my reading").click();
    await button(page, "Explore Moon").click();
    await shot(page, "western", mode, ".western-chart-layout");
    if (record) {
      await page
        .getByRole("slider", { name: "Turn the instrument" })
        .press("ArrowRight");
      await button(page, "Explore Venus").click();
      await align(page, ".placement-focus");
    }
    return { moon: natal.response.result.planets.Moon.longitude };
  },
  remote: async (page, mode, record) => {
    const second = await context(mode, record);
    try {
      const judge = await second.newPage();
      const trial = await blindTrial(
        page,
        judge,
        current,
        record ? (p) => wait(p, 540) : undefined,
      );
      await shot(page, "remote", mode, ".future-stage");
      if (record) {
        await wait(judge, 2400);
        await renderClip(judge, second, "remote-judge", 2.1);
      }
      return {
        commitment: trial.revealed.response.result.commitment,
        rank: trial.revealed.response.result.judge_results[0]
          .actual_target_rank,
      };
    } finally {
      await second.close();
    }
  },
  circuit: async (page, mode, record) => {
    await matchLab(page, 50, current);
    await align(page, ".future-stage");
    if (record) await wait(page);
    const data = await updateLab(page, 50);
    await shot(page, "circuit", mode, ".future-stage");
    return { request: data.wire, bars: data.response.view.instrument.bars };
  },
  market: async (page, mode, record) => {
    await matchLab(page, 58, current);
    await align(page, ".future-stage");
    if (record) await wait(page);
    const data = await updateLab(page, 58);
    await shot(page, "market", mode, ".future-stage");
    return {
      request: data.wire,
      holdings: data.response.result.final.q,
      quotes: data.response.result.final.modeled_prices,
    };
  },
  lorenz: async (page, mode, record) => {
    await matchLab(page, 59, current);
    await align(page, ".future-stage");
    if (record) await wait(page);
    const data = await updateLab(page, 59);
    const scrubber = page.getByRole("slider", {
      name: /Explore simulation time/,
    });
    if (record) {
      await scrubber.press("Home");
      await wait(page);
      for (let i = 0; i < 4; i++) {
        await scrubber.press("PageUp");
        await wait(page, 360);
      }
    }
    await scrubber.press("End");
    await shot(page, "lorenz", mode, ".future-stage");
    return {
      request: data.wire,
      endGap: data.response.view.instrument.counts.at(-1),
    };
  },
};

async function renderClip(page, c, name, trim) {
  const video = page.video();
  await c.close();
  execFileSync("ffmpeg", [
    "-y",
    "-v",
    "error",
    "-ss",
    String(trim),
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
    clip(name),
  ]);
}
async function media() {
  const only = process.argv
    .find((arg) => arg.startsWith("--journey="))
    ?.split("=")[1];
  if (only && !Object.hasOwn(tasks, only))
    throw Error("Unknown capture journey: " + only);
  const data = only
    ? JSON.parse(readFileSync("../evidence/block11-media.json", "utf8"))
        .captures
    : {};
  for (const mode of ["mobile", "desktop"]) {
    for (const [name, action] of Object.entries(tasks)) {
      if (only && name !== only) continue;
      const record = mode === "mobile";
      const c = await context(mode, record);
      const page = await c.newPage();
      const errors = [];
      page.on("pageerror", (error) => errors.push(error.message));
      try {
        data[`${name}-${mode}`] = (await action(page, mode, record)) ?? {};
        if (errors.length) throw Error(errors.join("; "));
        if (record) {
          await wait(page, 2200);
          await renderClip(page, c, name, name === "remote" ? 0.7 : 0.4);
        }
        console.log("captured", name, mode);
      } finally {
        await c.close();
      }
    }
  }
  save("media", {
    profiles: dimensions,
    captures: data,
    recordings: Object.keys(tasks).concat("remote-judge"),
  });
}

function cadence(page) {
  return page.evaluate(async () => {
    const frames = [];
    let previous = await new Promise(requestAnimationFrame);
    for (let i = 0; i < 40; i++) {
      const next = await new Promise(requestAnimationFrame);
      frames.push(next - previous);
      previous = next;
    }
    frames.sort((a, b) => a - b);
    return Math.round(frames[37] * 10) / 10;
  });
}

async function measure() {
  const samples = [];
  for (const mode of ["mobile", "desktop"]) {
    for (const [release, origin] of [
      ["block10", baseline],
      ["block11", current],
    ]) {
      const before = release === "block10";
      for (let run = 1; run <= 3; run++) {
        for (const id of [0, 50, 58, 59]) {
          const c = await context(mode);
          try {
            const page = await c.newPage();
            if (mode === "mobile") {
              const cdp = await c.newCDPSession(page);
              await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
            }
            let entryMs, actionMs, roomMs, imageKiB, heading;
            if (id === 0) {
              const begun = performance.now();
              await page.goto(origin + "/#gallery");
              await page.getByRole("searchbox").waitFor();
              entryMs = performance.now() - begun;
              const select = before
                ? page
                    .locator(".future-gallery summary")
                    .filter({ hasText: "The Tomorrow Machine" })
                : button(page, "The Tomorrow Machine");
              const leaf = before
                ? button(page, "Quantum Simulation")
                : page.getByRole("link", { name: "Enter Quantum Simulation" });
              const start = performance.now();
              await select.click();
              await leaf.waitFor();
              actionMs = performance.now() - start;
              [imageKiB, heading] = await page.evaluate(() => [
                performance
                  .getEntriesByType("resource")
                  .filter((r) => r.initiatorType === "img")
                  .reduce((size, r) => size + r.encodedBodySize, 0) / 1024,
                document.querySelector("h1").textContent,
              ]);
              const roomStarted = performance.now();
              await leaf.click();
              await page.locator(".future-reading .result-leaf").waitFor();
              roomMs = performance.now() - roomStarted;
            } else {
              const init = await matchLab(page, id, origin);
              entryMs = init.actionMs;
              const start = performance.now();
              await updateLab(page, id, before);
              actionMs = performance.now() - start;
              heading = await page.locator(".future-reading h2").innerText();
            }
            samples.push({
              mode,
              release,
              run,
              target: id || "gallery",
              heading,
              entryMs: Math.round(entryMs),
              actionMs: Math.round(actionMs),
              roomMs: roomMs === undefined ? undefined : Math.round(roomMs),
              imageKiB:
                imageKiB === undefined
                  ? undefined
                  : Math.round(imageKiB * 10) / 10,
              frameP95Ms: await cadence(page),
            });
          } finally {
            await c.close();
          }
        }
        console.log("measured", mode, release, run);
      }
    }
  }
  save("performance", {
    method:
      "Production builds from two releases, with matching native route actions on one Windows host. Fresh Chromium contexts. Mobile is 390×844 with CDP 4× CPU slowdown; desktop is 1440×1000, unthrottled. Network is loopback. Frames measure requestAnimationFrame callbacks following an action.",
    samples,
  });
}

async function narrowSmoke() {
  const engine = webkitOnly ? "webkit" : "firefox";
  const profile = webkitOnly
    ? devices["iPhone 13"]
    : { viewport: dimensions.mobile };
  const c = await browser.newContext({
    ...profile,
    reducedMotion: "reduce",
  });
  const page = await c.newPage();
  const checks = [];
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  try {
    await page.goto(current + "/#gallery");
    await button(page, "The Ritual Wing").click();
    const entry = page.getByRole("link", { name: "Enter Tarot" });
    await entry.waitFor();
    if ((await entry.getAttribute("href")) !== "#ritual")
      throw Error("Missing Tarot link");
    await button(page, "All worlds").click();
    await shot(page, "gallery-" + engine, "mobile");
    for (const [hash, expected] of [
      ["gallery", ".world-door"],
      ["ritual", ".intention"],
      ["numerology", ".number-form"],
      ["western", ".birth-form"],
      ["remote-viewing", ".sealed-display"],
      ["quantum-circuit", ".circuit-board"],
      ["prediction-market", ".market-register"],
      ["lorenz-chaos", ".lab-orbit-plot"],
    ]) {
      await page.goto(current + "/#" + hash);
      await page.locator(expected).first().waitFor();
      const width = await page.evaluate(() => ({
        document: document.documentElement.scrollWidth,
        window: innerWidth,
      }));
      if (width.document > width.window)
        throw Error("Horizontal overflow: " + hash);
      checks.push({
        hash,
        heading: await page.locator("h1").innerText(),
        width,
      });
    }
    if (errors.length) throw Error(errors.join("; "));
    save(engine, {
      engine: browser.version(),
      profile:
        (webkitOnly
          ? "Playwright iPhone 13 touch emulation"
          : "390×844 narrow viewport") + " · reduced motion",
      checks,
    });
  } finally {
    await c.close();
  }
}

try {
  if (webkitOnly || firefoxOnly) await narrowSmoke();
  else {
    if (!process.argv.includes("--measure-only")) await media();
    if (
      !process.argv.includes("--media-only") &&
      !process.argv.some((arg) => arg.startsWith("--journey="))
    )
      await measure();
  }
} finally {
  await browser.close();
}
