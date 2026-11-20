import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync, writeFileSync } from "node:fs";
import {
  align,
  blindTrial,
  button,
  exchange,
  open,
  rooms,
  runPublic,
  vault,
} from "../scripts/future-journeys.mjs";

for (const room of rooms.filter(({ id }) => id !== 43)) {
  test(`${room.slug} opens the native public instrument`, async ({ page }) => {
    const proof = await runPublic(page, room);
    expect(proof.oracle).toBe(room.id);
    expect(proof.request).toBeTruthy();
    expect(proof.private).toBe(false);
    const heading = page.locator(".future-reading h2");
    if (room.id === 50) await expect(heading).toHaveText(/likely outcomes|every time|Unequal outcomes/);
    else if (room.id === 58) await expect(heading).toHaveText(/^Yes trades at \d/);
    else if (room.id === 59) await expect(heading).toHaveText(/^\d+\.\d+ apart at the final sample$/);
    else await expect(heading).toHaveText(proof.view.title);
    expect(proof.sources.length).toBeGreaterThan(0);
    expect(
      await page.evaluate(() => localStorage.getItem("fate.codex.v1")),
    ).toBeNull();
  });
}

test("remote target reveals after a separate browser locks the complete judge ranking", async ({
  page,
  browser,
  baseURL,
}) => {
  const context = await browser.newContext({ baseURL });
  try {
    const judge = await context.newPage();
    const proof = await blindTrial(page, judge);
    const { started, locked, opened, revealed, retrieved } = proof;
    expect(started.response.packet.visibility).toBe("blind_viewer");
    const prior = [started.response, locked.response, opened.response];
    expect(JSON.stringify(prior)).not.toMatch(
      /"nonce"|"actual_target_id"|"selection"|"preimage"/,
    );
    expect(opened.response.packet.candidates).toHaveLength(5);
    expect(revealed.response.result.commitment).toBe(
      started.response.packet.commitment,
    );
    expect(retrieved.response.result).toEqual(revealed.response.result);
    expect(retrieved.response.result.commitment_verified).toBe(true);
    await expect(
      page.getByRole("heading", { name: /Target ranked \d of 5/ }),
    ).toBeVisible();
    expect(
      await page.evaluate(() => localStorage.getItem("fate.codex.v1")),
    ).toBeNull();
    writeFileSync(
      "../evidence/block10-blind-browser.json",
      JSON.stringify(
        {
          packetFields: Object.keys(started.response.packet),
          judgePacketFields: Object.keys(opened.response.packet),
          phases: [
            started.response.phase,
            locked.response.phase,
            opened.response.phase,
            revealed.response.phase,
          ],
          report: retrieved.response.result,
        },
        null,
        2,
      ) + "\n",
    );
  } finally {
    await context.close();
  }
});

test("a prospective dream locks in the browser and rejects an event dated in the future", async ({
  page,
}) => {
  await open(page, rooms.find(({ id }) => id === 44)!);
  await page.getByLabel("Feature to record").fill("A silver key");
  await page
    .getByRole("checkbox", { name: /Process this private diary/ })
    .check();
  await button(page, "Open recording slot").click();
  await page
    .getByLabel("Dream as remembered")
    .fill("QA original: a key under a blue cloth.");
  const locked = await vault(page, () =>
    button(page, "Lock dream text").click(),
  );
  expect(locked.response.phase).toBe("awaiting");
  expect(locked.response.result).toBeUndefined();
  await expect(
    page.getByRole("heading", { name: "Awaiting your observation" }),
  ).toBeVisible();
  const response = await page.request.post("/api/archive-session", {
    data: {
      action: "dream_observe",
      code: locked.wire.code,
      at: "2099-06-01T01:00Z",
      text: "A future event",
      consent: true,
    },
  });
  expect(response.status()).toBe(422);
  expect(
    await page.evaluate(() => localStorage.getItem("fate.codex.v1")),
  ).toBeNull();
  writeFileSync(
    "../evidence/block10-dream-browser.json",
    JSON.stringify(
      {
        lock: locked.response.originalLock,
        lockedAt: locked.response.lockedAt,
        phase: locked.response.phase,
        futureObservationStatus: response.status(),
        anticipatedResultsShown: false,
      },
      null,
      2,
    ) + "\n",
  );
});

test("grid edits recalculate native generations and only the public preset can reopen", async ({
  page,
}) => {
  const room = rooms.find(({ id }) => id === 54)!;
  await runPublic(page, room);
  await button(page, "Cell 1,1").click();
  const custom = await exchange(page, "/api/future-study", () =>
    button(page, "Advance the cells").click(),
  );
  expect(custom.wire.cells[0]).toBe(1);
  expect(custom.response.view.instrument.frames[0][0]).toBe(1);
  await expect(button(page, "Save public study to this device")).toHaveCount(0);
  await page.reload();
  await expect(page.locator(".future-reading .result-leaf")).toBeVisible();
  await button(page, "Save public study to this device").click();
  const stored = await page.evaluate(() =>
    JSON.parse(localStorage.getItem("fate.codex.v1")!),
  );
  expect(stored.chapters[0].snapshot).toEqual({
    oracle: 54,
    profile: "fate-future-studies-v1",
    option: 4,
  });
  const requests: string[] = [];
  page.on("request", (r) => {
    if (r.method() === "POST") requests.push(r.url());
  });
  await button(page, "Open in My Fate →").click();
  await expect(page.locator(".future-bookmark .folio-heading")).toBeVisible();
  await page.reload();
  await button(page, "Open your Codex").click();
  await expect(page.locator(".future-bookmark .folio-heading")).toBeVisible();
  const check = page.waitForEvent("download");
  await button(page, "Export this chapter").click();
  const exported = JSON.parse(
    readFileSync((await (await check).path())!, "utf8"),
  );
  expect(exported.chapters[0].snapshot).toEqual(stored.chapters[0].snapshot);
  expect(exported.chapters[0].source_readings.length).toBeGreaterThan(0);
  expect(requests).toEqual([]);
  writeFileSync(
    "../evidence/block10-privacy-browser.json",
    JSON.stringify(
      { stored, exported, reopenPostRequests: requests },
      null,
      2,
    ) + "\n",
  );
});

test("all retained rooms are searchable and representative instruments fit 320px with reduced motion", async ({
  page,
}) => {
  await page.setViewportSize({ width: 320, height: 744 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/#gallery");
  for (const [name, count] of [["The Dream Archive", 7], ["The Tomorrow Machine", 12]] as const) {
    await button(page, name).click();
    await expect(page.getByRole("region", { name, exact: true }).locator("[data-technique-id]")).toHaveCount(count);
    await button(page, "All worlds").click();
  }
  for (const id of [24, 43, 44, 50, 54, 59, 60]) {
    const room = rooms.find((r) => r.id === id)!;
    await open(page, room);
    await align(page);
    if (id >= 49)
      await expect(page.locator(".future-reading .result-leaf")).toBeVisible();
    await expect(page.locator(".future-room")).toHaveAttribute(
      "data-still",
      "true",
    );
    expect(
      await page.evaluate(() => document.documentElement.scrollWidth),
    ).toBeLessThanOrEqual(320);
    const audit = await new AxeBuilder({ page })
      .include(".future-room")
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(audit.violations.map((v) => v.id)).toEqual([]);
  }
});
