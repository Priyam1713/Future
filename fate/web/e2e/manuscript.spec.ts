import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync, writeFileSync } from "node:fs";
import {
  align,
  button,
  journeys,
  openRoom,
  perform,
} from "../scripts/manuscript-journeys.mjs";

for (const journey of journeys) {
  test(
    journey.slug + " keeps its native result and declared scope",
    async ({ page }) => {
      await openRoom(page, journey);
      const observed = await perform(page, journey);
      expect(observed.result.technique_id).toBe(journey.id);
      if (journey.id === 5) {
        expect(observed.result.classification).toBe("indeterminate");
        expect(observed.result.judgment_certified).toBe(false);
        await expect(
          page.getByRole("heading", { name: "Judgment indeterminate" }),
        ).toBeVisible();
        await expect(page.locator("svg[data-chart-origin]")).toHaveAttribute(
          "data-chart-origin",
          String(observed.result.question_chart.angles.ascendant),
        );
      } else if (journey.id === 6) {
        expect(observed.result.events).toHaveLength(4);
        await page.getByRole("button", { name: /Libra ingress/ }).click();
        await expect(
          page.getByRole("heading", { name: "Libra ingress" }),
        ).toBeVisible();
        const event = observed.result.events.find(
          (row: { sign: string }) => row.sign === "Libra",
        );
        await expect(page.locator("svg[data-chart-origin]")).toHaveAttribute(
          "data-chart-origin",
          String(event.chart.angles.ascendant),
        );
      } else if (journey.id === 7) {
        const lines = observed.result.geojson.features;
        expect(lines).toHaveLength(40);
        await page
          .getByRole("combobox", { name: "Planet", exact: true })
          .selectOption("Mars");
        await button(page, "ASC · Rising").click();
        const line = lines.find(
          (item: { id: string }) => item.id === "Mars.ASC",
        );
        const path = line.geometry.coordinates
          .map(
            (segment: number[][]) =>
              "M" + segment.map(([lon, lat]) => `${lon},${-lat}`).join(" "),
          )
          .join(" ");
        await expect(page.locator('[data-line="Mars.ASC"]')).toHaveAttribute(
          "d",
          path,
        );
        await button(page, "Zoom map in").click();
        await expect(page.locator(".map-zoomed")).toBeVisible();
      } else if (journey.id === 40) {
        expect(observed.result.readings[0].uncertainty_crosses_boundary).toBe(
          true,
        );
        await expect(
          page.locator(".compass-instrument [data-active=true]"),
        ).toHaveCount(observed.references.length);
        expect(observed.result.readings[0].declination_conversion).toBeNull();
      } else if (journey.id === 8) {
        expect(observed.result.hands[0].observations.side).toBe("left");
      } else {
        expect(observed.result.inference_enabled).toBe(false);
      }
      const storageBeforeSave = await page.evaluate(() =>
        localStorage.getItem("fate.codex.v1"),
      );
      expect(storageBeforeSave).toBeNull();
      if (journey.id < 8) {
        await expect(
          button(page, "Save source bookmark to this device"),
        ).toHaveCount(0);
        return;
      }
      await button(page, "Save source bookmark to this device").click();
      const stored = await page.evaluate(() =>
        JSON.parse(localStorage.getItem("fate.codex.v1")!),
      );
      expect(stored.chapters[0].snapshot).toEqual({
        oracle: journey.id,
        profile: "fate-manuscript-reference-v1",
        entries: observed.references || [observed.reference],
      });
      const posts: string[] = [];
      page.on("request", (r) => {
        if (r.method() === "POST") posts.push(r.url());
      });
      await button(page, "Open in My Fate →").click();
      await expect(
        page.locator(".folio-bookmark .folio-heading"),
      ).toBeVisible();
      await page.reload();
      await button(page, "Open your Codex").click();
      await expect(
        page.locator(".folio-bookmark .folio-heading"),
      ).toBeVisible();
      const download = page.waitForEvent("download");
      await button(page, "Export this chapter").click();
      const path = (await (await download).path())!;
      const exported = JSON.parse(readFileSync(path, "utf8"));
      expect(exported.chapters[0].snapshot).toEqual(
        stored.chapters[0].snapshot,
      );
      expect(exported.chapters[0].source_readings.length).toBeGreaterThan(0);
      expect(posts).toEqual([]);
      writeFileSync(
        `../evidence/block09-privacy-${journey.id}.json`,
        JSON.stringify(
          { storageBeforeSave, stored, exported, reopenPostRequests: posts },
          null,
          2,
        ) + "\n",
      );
    },
  );
}

test("360-degree input and compass pointer preserve the live bearing before exact classification", async ({
  page,
}) => {
  const journey = journeys.find(({ id }) => id === 40)!;
  await openRoom(page, journey);
  await align(page);
  const slider = page.getByRole("slider", { name: "Turn bearing" });
  await slider.focus();
  await page.keyboard.press("Home");
  await expect(page.getByLabel("Bearing (°)", { exact: true })).toHaveValue(
    "0.0",
  );
  const dial = page.locator(".compass-instrument svg");
  const box = (await dial.boundingBox())!;
  await page.touchscreen.tap(
    box.x + box.width * 0.85,
    box.y + box.height * 0.5,
  );
  const angle = Number(
    await page.getByLabel("Bearing (°)", { exact: true }).inputValue(),
  );
  expect(angle).toBeGreaterThan(89);
  expect(angle).toBeLessThan(91);
  await expect(button(page, "Classify the bearing")).toBeDisabled();
});

test("recorded moment requires a confirmed site and exposes a repeated local hour", async ({
  page,
}) => {
  await openRoom(page, journeys.find(({ id }) => id === 7)!);
  await button(page, "Use a recorded moment").click();
  await page
    .getByLabel("Recorded birth date and time")
    .fill("2024-10-27T01:30");
  await expect(button(page, "Calculate the sky")).toBeDisabled();
  await button(page, "Enter exact coordinates").click();
  await page.getByLabel("Latitude", { exact: true }).fill("51.5072");
  await page.getByLabel("Longitude", { exact: true }).fill("-0.1276");
  await page.getByLabel("IANA timezone").fill("Europe/London");
  await button(page, "Confirm coordinates").click();
  await button(page, "Calculate the sky").click();
  await expect(page.getByRole("alert")).toContainText(/ambiguous|repeated/i);
  await page.getByText("Repeated local hour", { exact: true }).click();
  await page.getByLabel("Occurrence").selectOption("1");
  const pending = page.waitForResponse((r) =>
    r.url().endsWith("/api/sky-manuscript"),
  );
  await button(page, "Calculate the sky").click();
  const response = await pending;
  expect(response.ok()).toBe(true);
  const native = await response.json();
  expect(native.result.birth.utc).toBe("2024-10-27T01:30:00+00:00");
  await expect(
    page.getByRole("heading", { name: "Sun · Upper meridian" }),
  ).toBeVisible();
  expect(
    await page.evaluate(() => localStorage.getItem("fate.codex.v1")),
  ).toBeNull();
});

test("Jupiter–Saturn study displays the native contact and stations", async ({
  page,
}) => {
  await openRoom(page, journeys.find(({ id }) => id === 6)!);
  await button(page, "Jupiter–Saturn conjunctions").click();
  const start = performance.now();
  const native = await perform(page, { id: 6, entry: "" });
  expect(native.request.year).toBe(2020);
  expect(native.result.events).toHaveLength(1);
  expect(native.result.events[0].utc).toMatch(/^2020-12-21T/);
  expect(native.result.events[0].bodies).toEqual(["Jupiter", "Saturn"]);
  await expect(
    page.getByRole("heading", { name: "Jupiter–Saturn conjunction" }),
  ).toBeVisible();
  await page.getByText("Stations and sign crossings", { exact: true }).click();
  await expect(page.getByText(/Jupiter · Station/).first()).toBeVisible();
  writeFileSync(
    "../evidence/block09-conjunction.json",
    JSON.stringify(
      {
        ...native,
        browserMs: Math.round(performance.now() - start),
      },
      null,
      2,
    ) + "\n",
  );
});

test("the three environments fit 320px and honor reduced motion", async ({
  page,
}) => {
  await page.setViewportSize({ width: 320, height: 744 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/#gallery");
  await page
    .getByRole("button", { name: "The Human Manuscript", exact: true })
    .click();
  await expect(
    page
      .getByRole("region", { name: "The Human Manuscript", exact: true })
      .locator("[data-technique-id]"),
  ).toHaveCount(8);
  for (const journey of journeys) {
    await openRoom(page, journey);
    await expect(page.locator(".folio-room")).toHaveAttribute(
      "data-still",
      "true",
    );
    expect(
      await page.evaluate(() => document.documentElement.scrollWidth),
    ).toBeLessThanOrEqual(320);
  }
  for (const id of [7, 8, 15, 40]) {
    await openRoom(page, journeys.find((room) => room.id === id)!);
    const report = await new AxeBuilder({ page })
      .include(".folio-room")
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(report.violations.map(({ id }) => id)).toEqual([]);
  }
});
