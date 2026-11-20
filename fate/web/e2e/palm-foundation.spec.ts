import { expect, test } from "@playwright/test";
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
  const box = (await page
    .getByAltText("Your selected palm for manual review")
    .boundingBox())!;
  await page.mouse.click(box.x + box.width * 0.49, box.y + box.height * 0.52);
  await expect(page.locator(".palm-photo-frame circle")).toHaveCount(1);
  await page.getByLabel("Photographed hand").selectOption("left");
  await page.getByLabel("Head line shape").selectOption("slight_slope");
  await page
    .getByLabel("Heart line endpoint toward the index finger")
    .selectOption("jupiter");
  await expect(
    page.getByRole("button", { name: "Open my palm reading" }),
  ).toBeDisabled();
  await page
    .getByLabel("I confirmed these descriptions against the photo")
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
    "../evidence/block13-palm-browser.json",
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
