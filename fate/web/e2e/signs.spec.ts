import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync, writeFileSync } from "node:fs";
import {
  alignSign,
  journeys,
  openSign,
  perform,
} from "../scripts/sign-journeys.mjs";

for (const journey of journeys) {
  test(
    journey.slug +
      " follows the declared inputs, preserves native scope, and reopens with archived sources",
    async ({ page }) => {
      await openSign(page, journey.slug);
      const native = await perform(page, journey);
      expect(native.request).toEqual({
        oracle: journey.id,
        values: journey.values,
      });
      expect(native.result.technique_id).toBe(journey.id);
      expect(native.result.mode).toBe(
        journey.id === 35 ? "documentary" : "manual",
      );
      expect(native.snapshot.values).toEqual(journey.values);
      await expect(page.locator(".sign-interpretation .eyebrow")).toHaveText(
        native.view.status,
      );
      if (journey.id === 34)
        await expect(page.locator(".sign-metric")).toHaveAttribute(
          "data-distance",
          "5",
        );
      if (journey.id === 37)
        expect(native.result.selection.generated).toBe(false);
      if (journey.id === 35)
        expect(native.result.selected_case_ids).toEqual(["9A", "9B"]);
      if (journey.id === 39)
        expect(native.result.observations[0].declared.origin).toBe(
          "source_description",
        );
      expect(
        await page.evaluate(() => localStorage.getItem("fate.codex.v1")),
      ).toBeNull();
      await page
        .getByRole("button", {
          name: "Save sign chapter to this device",
          exact: true,
        })
        .click();
      const raw = await page.evaluate(() =>
        localStorage.getItem("fate.codex.v1"),
      );
      expect(raw).not.toBeNull();
      const stored = JSON.parse(raw!);
      expect(stored.chapters[0].snapshot).toEqual(native.snapshot);
      expect(stored.chapters[0].reference).toBe("fate-world-of-signs-v1");
      expect(raw).not.toMatch(
        /"(notes|commentary|observations|replay|declared|sourceRecord)"/,
      );
      const posts: string[] = [];
      page.on("request", (r) => {
        if (r.method() === "POST") posts.push(r.url());
      });
      await page.getByRole("button", { name: /Open in My Fate/ }).click();
      await expect(page.locator(".sign-folio")).toBeVisible({ timeout: 15000 });
      await page.reload();
      await page
        .getByRole("button", { name: "Open your Codex", exact: true })
        .click();
      await expect(
        page.locator(".sign-folio .sign-interpretation .eyebrow"),
      ).toHaveText(native.view.status);
      const download = page.waitForEvent("download");
      await page
        .getByRole("button", { name: "Export this chapter", exact: true })
        .click();
      const exported = JSON.parse(
        readFileSync((await (await download).path())!, "utf8"),
      );
      expect(exported.chapters[0].snapshot).toEqual(native.snapshot);
      expect(
        exported.chapters[0].source_readings.map(
          (row: { wording: string }) => row.wording,
        ),
      ).toEqual(native.view.excerpts.map((row: { text: string }) => row.text));
      expect(posts).toEqual([]);
      writeFileSync(
        "../evidence/block08-privacy-" + journey.id + ".json",
        JSON.stringify(
          {
            oracle: journey.id,
            storageBeforeSave: null,
            stored,
            exported,
            reopenPostRequests: posts,
          },
          null,
          2,
        ) + "\n",
      );
    },
  );
}

test("a reported candle hazard suppresses the symbolic reading and save", async ({
  page,
}) => {
  await openSign(page, "candle-lore");
  const native = await perform(page, {
    ...journeys[2],
    picks: ["High", "Persistent", "Active hazard reported", "Past observation"],
  });
  expect(native.result.safety.symbolic_hold).toBe(true);
  expect(native.snapshot).toBeNull();
  await expect(page.locator(".sign-interpretation .eyebrow")).toHaveText(
    "Safety hold",
  );
  await expect(page.locator(".sign-depth")).toHaveCount(0);
  await expect(
    page.getByRole("button", { name: "Save sign chapter to this device" }),
  ).toHaveCount(0);
});

test("all three World of Signs entrances respect 320px, reduced motion, and accessible controls", async ({
  page,
}) => {
  await page.setViewportSize({ width: 320, height: 744 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/#gallery");
  await page.getByText("The World of Signs", { exact: false }).first().click();
  await page
    .getByRole("navigation", { name: "The World of Signs rooms" })
    .getByRole("link", { name: "Enter Lithomancy", exact: true })
    .click();
  await expect(page.locator(".sign-intro h1")).toHaveText("The Stone Plan");
  for (const journey of journeys) {
    await openSign(page, journey.slug);
    await alignSign(page);
    await expect(page.locator(".sign-room")).toHaveAttribute(
      "data-sign-still",
      "true",
    );
    expect(
      await page
        .locator(".sign-stage")
        .evaluate(
          (e) => e.scrollWidth <= Math.ceil(e.getBoundingClientRect().width),
        ),
    ).toBeTruthy();
    const audit = await new AxeBuilder({ page })
      .include(".sign-room")
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(
      audit.violations.map((v) => [v.id, v.nodes.map((n) => n.target)]),
    ).toEqual([]);
  }
});
