import { chromium } from "@playwright/test";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { alignSign, journeys, openSign, perform } from "./sign-journeys.mjs";

const origin = process.env.FATE_CAPTURE_ORIGIN ?? "http://127.0.0.1:8010";
const mobile = { width: 390, height: 844 };
const modes = {
  mobile: { viewport: mobile, isMobile: true, hasTouch: true },
  desktop: { viewport: { width: 1440, height: 1000 } },
};
const raw = "../../tmp/block08-video";
const screenshots = "../screenshots";
const evidence = "../evidence";
const requested = process.argv.find((arg) => arg.startsWith("--rooms="));
const selected = requested
  ? requested.slice(8).split(",").map(Number)
  : journeys.map(({ id }) => id);
if (selected.some((id) => !journeys.some((journey) => journey.id === id)))
  throw new Error("Unknown technique in --rooms");
mkdirSync(raw, { recursive: true });
const browser = await chromium.launch({
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
});
const write = (name, data) =>
  writeFileSync(
    `${evidence}/block08-${name}.json`,
    JSON.stringify(data, null, 2) + "\n",
  );
const read = (name) =>
  JSON.parse(readFileSync(`${evidence}/block08-${name}.json`, "utf8"));
const shot = (page, name) =>
  page.screenshot({
    path: `${screenshots}/08-${name}.png`,
    animations: "disabled",
  });
const press = (page, name) =>
  page.getByRole("button", { name, exact: true }).click();

async function prepare(page, slug) {
  await openSign(page, slug, origin);
  await page.evaluate(() => document.fonts.ready);
  await alignSign(page);
}

async function cadence(page) {
  return page.evaluate(async () => {
    const intervals = [];
    let previous = await new Promise(requestAnimationFrame);
    for (let frame = 0; frame < 65; frame++) {
      const next = await new Promise(requestAnimationFrame);
      intervals.push(next - previous);
      previous = next;
    }
    const sample = intervals.slice(5).sort((a, b) => a - b);
    return { medianMs: sample[30], p95Ms: sample[56], maxMs: sample.at(-1) };
  });
}

async function stills() {
  const native = requested ? read("native").native : {};
  const profiles = requested
    ? read("performance").profiles.filter(
        (row) => !selected.includes(row.oracle),
      )
    : [];
  for (const journey of journeys.filter(({ id }) => selected.includes(id))) {
    for (const [mode, device] of Object.entries(modes)) {
      const ctx = await browser.newContext({ ...device, deviceScaleFactor: 1 });
      const page = await ctx.newPage();
      const errors = [];
      page.on("pageerror", (error) => errors.push(error.message));
      const start = performance.now();
      await prepare(page, journey.slug);
      const entranceMs = Math.round(performance.now() - start);
      if (mode === "desktop") {
        await alignSign(page, ".sign-intro");
        await shot(page, `${journey.slug}-entrance`);
        await alignSign(page);
      }
      const frames = await cadence(page);
      if (journey.id === 34 && mode === "mobile") {
        await press(page, "Onyx");
        await shot(page, "stone-table-placement-mobile");
        await page.reload();
        await prepare(page, journey.slug);
      }
      const reading = await perform(page, journey);
      await alignSign(page, ".sign-result");
      await shot(page, `${journey.slug}-${mode}`);
      if (mode === "mobile") native[journey.id] = reading;
      profiles.push({
        oracle: journey.id,
        mode,
        entranceMs,
        actionMs: reading.actionMs,
        ...frames,
      });
      if (errors.length) throw new Error(errors.join("\n"));
      await ctx.close();
      console.log(
        journey.slug,
        mode,
        entranceMs,
        reading.actionMs,
        frames.p95Ms,
      );
    }
  }
  write("native", {
    scope:
      "Unmocked local HTTP; categorical QA selections made through the mobile interface.",
    native,
  });
  write("performance", {
    scope:
      "Local Playwright Chromium, software rendering, DPR 1, 60 requestAnimationFrame intervals before interaction. Action time includes Playwright, HTTP, and the visible result. Frame intervals measure scheduling, not displayed GPU frames.",
    profiles,
  });
}

async function refinements() {
  const ctx = await browser.newContext({
    ...modes.mobile,
    deviceScaleFactor: 1,
  });
  const page = await ctx.newPage();
  for (const slug of ["crystal", "mirror", "geomancy", "bibliomancy"]) {
    await page.goto(`${origin}/#${slug}`);
    await page.locator(".ritual-intro h1").waitFor();
    await page.evaluate(() => document.fonts.ready);
    if (slug === "geomancy") {
      for (const [i, mother] of ["1212", "2112", "1122", "2121"].entries()) {
        for (const [j, n] of [...mother].entries()) {
          const target = page.getByRole("button", {
            name: new RegExp(`^Mother ${i + 1}, row ${j + 1}:`),
          });
          for (let k = 0; k < Number(n); k++) await target.click();
        }
      }
      await press(page, "Form the shield");
      await page.locator(".ritual-result").waitFor();
      await alignSign(page, ".ritual-result");
    } else {
      if (slug === "bibliomancy") {
        await press(page, "Ruth 2");
        await page.locator(".book-selection button").nth(3).click();
      } else {
        await page
          .locator('.ritual-glass[data-renderer="volumetric"]')
          .waitFor();
      }
      await alignSign(page, ".ritual-stage");
    }
    await shot(page, `refined-${slug}-mobile`);
    console.log(slug, "updated mobile stage");
  }
  await ctx.close();
}

async function overview() {
  const mobilePage = await browser.newPage(modes.mobile);
  for (const slug of ["tea-leaves", "weather-lore", "bone-archive"]) {
    await openSign(mobilePage, slug, origin);
    await mobilePage.evaluate(async () => {
      await document.fonts.ready;
      await document.querySelector(".sign-hero img").decode();
    });
    await alignSign(mobilePage, ".sign-hero");
    await shot(mobilePage, `${slug}-entrance-mobile`);
  }
  await mobilePage.close();
  const gallery = await browser.newPage(modes.desktop);
  await gallery.goto(`${origin}/#gallery`);
  await gallery.locator(".sign-gallery-wing summary").click();
  await gallery.evaluate(() => document.fonts.ready);
  await alignSign(gallery, ".sign-gallery-wing");
  await shot(gallery, "gallery-desktop");
  await gallery.close();
}

function encode(path, file) {
  const sample = execFileSync(
    "ffmpeg",
    [
      "-v",
      "error",
      "-i",
      path,
      "-t",
      "10",
      "-vf",
      "fps=8,scale=52:112",
      "-f",
      "rawvideo",
      "-pix_fmt",
      "rgb24",
      "-",
    ],
    { maxBuffer: 4 * 1024 * 1024 },
  );
  const pixels = 52 * 112;
  let streak = 0,
    trim;
  for (
    let offset = 0;
    offset + pixels * 3 <= sample.length;
    offset += pixels * 3
  ) {
    let gray = 0;
    for (let i = offset; i < offset + pixels * 3; i += 3) {
      const [r, g, b] = [sample[i], sample[i + 1], sample[i + 2]];
      if (r > 90 && r < 160 && Math.abs(r - g) < 3 && Math.abs(r - b) < 3)
        gray++;
    }
    streak = gray / pixels > 0.62 ? 0 : streak + 1;
    if (streak >= 2) {
      trim = (offset / (pixels * 3) - 1) / 8;
      break;
    }
  }
  if (trim === undefined) throw new Error("No stable recorded viewport");
  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-ss",
      String(trim),
      "-i",
      path,
      "-c:v",
      "libx264",
      "-crf",
      "20",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      "-an",
      file,
    ],
    { stdio: "pipe" },
  );
  const media = JSON.parse(
    execFileSync(
      "ffprobe",
      [
        "-v",
        "error",
        "-show_entries",
        "stream=width,height,codec_name:format=duration",
        "-of",
        "json",
        file,
      ],
      { encoding: "utf8" },
    ),
  );
  return { trim, media };
}

async function clips() {
  const recordings = requested ? read("recordings").recordings : {};
  for (const journey of journeys.filter(
    ({ id }) => selected.includes(id) && [28, 32, 34, 35].includes(id),
  )) {
    const ctx = await browser.newContext({
      ...modes.mobile,
      deviceScaleFactor: 1,
      recordVideo: { dir: raw, size: mobile },
    });
    const page = await ctx.newPage();
    await prepare(page, journey.slug);
    await page.waitForTimeout(750);
    const reading = await perform(page, journey, () =>
      page.waitForTimeout(700),
    );
    await alignSign(page, ".sign-result");
    await page.waitForTimeout(2500);
    const video = page.video();
    await ctx.close();
    recordings[journey.slug] = {
      ...encode(await video.path(), `${evidence}/block08-${journey.slug}.mp4`),
      request: reading.request,
      snapshot: reading.snapshot,
    };
    console.log(
      journey.slug,
      "recorded",
      recordings[journey.slug].media.format.duration,
    );
  }
  write("recordings", {
    scope:
      "Real mobile Chromium sessions. Only gray startup frames trimmed. No compositing or audio.",
    recordings,
  });
}

try {
  if (!process.argv.includes("--clips-only")) {
    await stills();
    if (!requested) {
      await refinements();
      await overview();
    }
  }
  if (!process.argv.includes("--stills-only")) await clips();
} finally {
  await browser.close();
}
