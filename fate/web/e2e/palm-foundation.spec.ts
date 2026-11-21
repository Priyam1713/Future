import { chromium, expect, test } from "@playwright/test";
import { writeFileSync } from "node:fs";

const fixture = "../../workbench/tests/assets/palm-cc0.png";
test("photo workflow keeps image private, records only selected descriptors, and presents depth", async ({
  page,
}) => {
  await page.goto("/#palmistry");
  const file = page.getByLabel("Palm photograph");
  await expect(file).toBeDisabled();
  await page.getByLabel("I have permission to review this photo").check();
  await file.setInputFiles(fixture);
  await expect(
    page.getByAltText("Your selected palm for manual review"),
  ).toBeVisible();
  await expect(page.getByRole("button", { name: "Head line", exact: true })).toHaveCount(0);
  await page.getByRole("button", { name: "Left hand" }).click();
  await page.getByRole("button", { name: "Continue", exact: true }).click();
  await expect(page.locator(".palm-guide [data-active=true]")).toHaveCount(1);
  await page.getByRole("button", { name: "Gently sloping", exact: true }).click();
  await page.getByRole("button", { name: "Continue", exact: true }).click();
  await page.getByRole("button", { name: "Below the index finger", exact: true }).click();
  await page.getByRole("button", { name: "Continue", exact: true }).click();
  await page.getByRole("button", { name: "Skip this feature" }).click();
  await page.getByRole("button", { name: "Review observations", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Open my palm reading" }),
  ).toBeDisabled();
  await page
    .getByLabel("I confirm these observations")
    .check();
  const waiting = page.waitForResponse((r) =>
    r.url().endsWith("/api/palm-reading"),
  );
  await page.getByRole("button", { name: "Open my palm reading" }).click();
  const response = await waiting;
  expect(response.ok()).toBeTruthy();
  expect(response.request().postDataJSON()).toEqual({
    confirmed: true,
    hand: {
      side: "left",
      shape: {},
      lines: {
        head: { presence: "present", curvature: "slight_slope" },
        heart: { presence: "present", origin: "jupiter" },
      },
      mounts: {},
    },
    fingertips: "unknown",
    mount_lean: "unknown",
  });
  const r = await response.json();
  await expect(page.locator(".palm-report")).toContainText(
    "gentle slope of the head line",
  );
  await expect(page.locator(".palm-report")).toContainText(
    "below your index finger",
  );
  expect(await page.evaluate(() => Object.keys(localStorage))).toEqual([]);
  writeFileSync(
    "../evidence/block14-palm-browser.json",
    JSON.stringify(
      {
        scope:
          "Scripted manual descriptors on the CC0 intake fixture; not ground truth for recognition.",
        request: response.request().postDataJSON(),
        narrative: r.narrative,
        nativeMatches: r.native.hands[0].readings,
      },
      null,
      2,
    ) + "\n",
  );
  await page.getByRole("button", { name: "Remove photo and start over" }).click();
  await expect(page.locator(".palm-report")).toHaveCount(0);
  await page.reload();
  await expect(
    page.getByAltText("Your selected palm for manual review"),
  ).toHaveCount(0);
});

test("local quality gates reject corrupt and flat images without calling the reading API", async ({
  page,
}) => {
  await page.goto("/#palmistry");
  await page.getByLabel("I have permission to review this photo").check();
  const file = page.getByLabel("Palm photograph");
  let sent = 0;
  page.on("request", (r) => {
    if (r.url().endsWith("/api/palm-reading")) sent++;
  });
  await file.setInputFiles({
    name: "broken.png",
    mimeType: "image/png",
    buffer: Buffer.from("not an image"),
  });
  await expect(page.locator(".palm-studio [role=alert]")).toBeVisible();
  const blank = await page.evaluate(() => {
    const c = document.createElement("canvas");
    c.width = c.height = 350;
    c.getContext("2d")!.fillRect(0, 0, 350, 350);
    return c.toDataURL().split(",")[1];
  });
  await file.setInputFiles({
    name: "flat.png",
    mimeType: "image/png",
    buffer: Buffer.from(blank, "base64"),
  });
  await expect(page.locator(".palm-studio [role=alert]")).toContainText(
    "too dark, bright or flat",
  );
  expect(sent).toBe(0);
});

test("ambient playback starts on a touch activation and mute survives a fresh load", async ({
  page,
}) => {
  await page.goto("/#palmistry");
  const wav = page.waitForResponse((r) =>
    r.url().endsWith("/art/fate-ambient-v2.wav"),
  );
  await page.getByLabel("I have permission to review this photo").tap();
  expect((await wav).ok()).toBeTruthy();
  const mute = page.getByRole("button", { name: "Mute sound" });
  await expect(mute).toBeVisible();
  await mute.tap();
  await page.reload();
  await page.getByLabel("I have permission to review this photo").tap();
  await expect(
    page.getByRole("button", { name: "Enable sound" }),
  ).toBeVisible();
});

test("manual fallback, keyboard confirmation, and narrow layouts support incomplete evidence", async ({page}) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  for (const [width, height] of [[320, 700], [390, 844], [768, 1024], [1440, 900]]) {
    await page.setViewportSize({ width, height });
    await page.goto("/#palmistry");
    const manual = page.getByRole("button", {name: "Examine without a photo"});
    await expect(manual).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
  }
  await page.locator("html").evaluate((el) => { el.style.zoom = "2"; });
  const manual = page.getByRole("button", {name: "Examine without a photo"});
  await manual.focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", {name: "Which hand are you looking at?"})).toBeFocused();
  await page.getByRole("button", {name: "Right hand"}).press("Enter");
  await page.getByRole("button", {name: "Continue", exact: true}).press("Enter");
  await page.getByRole("button", {name: "Review observations", exact: true}).press("Enter");
  await page.getByLabel("I confirm these observations").press("Space");
  await page.getByRole("button", {name: "Open my palm reading"}).press("Enter");
  await expect(page.getByRole("heading", {name: "A reading needs clearer observations"})).toBeFocused();
  await page.getByRole("button", {name: "Explore the illustrated archive"}).click();
  await expect(page.locator(".palm-studio")).toHaveCount(0);
  await page.getByRole("button", {name: "Return to palm reading"}).click();
  await expect(manual).toBeVisible();
});

test("camera consent and local capture close the stream", async ({baseURL}) => {
  const browser = await chromium.launch({args: [
    "--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream",
  ]});
  try {
    const page = await browser.newPage({baseURL});
    await page.addInitScript(() => {
      const open = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);
      navigator.mediaDevices.getUserMedia = async (constraints) => {
        const stream = await open(constraints);
        Object.assign(window, { palmTestTrack: stream.getTracks()[0] });
        return stream;
      };
    });
    await page.goto("/#palmistry");
    const camera = page.getByRole("button", {name: "Use camera"});
    await expect(camera).toBeDisabled();
    await page.getByLabel("I have permission to review this photo").check();
    await camera.click();
    await expect.poll(() => page.locator("video").evaluate((el) => el.videoWidth)).toBeGreaterThanOrEqual(320);
    await page.getByRole("button", {name: "Take photo"}).click();
    await expect(page.getByAltText("Your selected palm for manual review")).toBeVisible();
    expect(await page.evaluate(() => (window as unknown as {palmTestTrack: MediaStreamTrack}).palmTestTrack.readyState)).toBe("ended");
  } finally {
    await browser.close();
  }
});
