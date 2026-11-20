import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import {
  button,
  exchange,
  rooms,
  runPublic,
} from "../scripts/future-journeys.mjs";

test("six illustrated doors cover all 54 rooms once and return keyboard focus", async ({
  page,
}) => {
  await page.setViewportSize({ width: 320, height: 744 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/#gallery");
  const doors = page.locator(".world-door");
  await expect(doors).toHaveCount(6);
  const names = await doors.locator("strong").allTextContents();
  const seen: number[] = [];
  for (const name of names) {
    const next = page.getByRole("button", { name, exact: true });
    await next.focus();
    await page.keyboard.press("Enter");
    await expect(
      page.getByRole("heading", { name, exact: true }),
    ).toBeFocused();
    expect(
      await page
        .locator(".world-interior")
        .evaluate((el) => getComputedStyle(el).animationName),
    ).toBe("none");
    seen.push(
      ...(await page
        .locator("[data-technique-id]")
        .evaluateAll((nodes) =>
          nodes.map((n) => Number((n as HTMLElement).dataset.techniqueId)),
        )),
    );
    await button(page, "All worlds").click();
    await expect(next).toBeFocused();
  }
  expect(seen).toHaveLength(54);
  expect(new Set(seen).size).toBe(54);
  const search = page.getByRole("searchbox");
  await search.fill("lorenz");
  await expect(search).toBeFocused();
  const room = page.getByRole("link", { name: "Enter Lorenz Chaos" });
  await expect(room).toHaveAttribute("href", "#lorenz-chaos");
  await room.click();
  await expect(page.locator(".future-room h1")).toHaveText(
    "The Lorenz Chamber",
  );
});

test("circuit, market and Lorenz controls report the actual new native numbers", async ({
  page,
}) => {
  await runPublic(
    page,
    rooms.find(({ id }) => id === 50)!,
  );
  const circuit = await exchange(page, "/api/future-study", () =>
    button(page, "Independent H").click(),
  );
  const outputs = circuit.response.view.instrument.bars;
  expect(outputs).toHaveLength(4);
  for (const row of outputs) expect(row.value).toBeCloseTo(0.25, 12);
  await expect(page.locator(".lab-payoff h2")).toHaveText(
    "4 equally likely outcomes",
  );
  await expect(page.locator(".circuit-outcomes dd b")).toHaveText([
    "25.0%",
    "25.0%",
    "25.0%",
    "25.0%",
  ]);
  await runPublic(
    page,
    rooms.find(({ id }) => id === 58)!,
  );
  await page
    .getByRole("slider", { name: /Yes shares in this example/ })
    .press("End");
  const market = await exchange(page, "/api/future-study", () =>
    button(page, "Update market quote").click(),
  );
  expect(market.wire.option).toBe(8);
  expect(market.response.result.final.q.YES).toBe("8");
  const yes = market.response.view.instrument.bars.find(
    ({ label }: { label: string }) => label === "YES",
  ).value;
  await expect(page.locator(".market-prices strong").first()).toHaveText(
    (100 * yes).toFixed(2) + "%",
  );
  await runPublic(
    page,
    rooms.find(({ id }) => id === 59)!,
  );
  const orbit = await exchange(page, "/api/future-study", () =>
    button(page, "9 units").click(),
  );
  await page
    .getByRole("slider", { name: /Explore simulation time/ })
    .press("Home");
  const sample = orbit.response.view.instrument;
  await expect(page.locator(".lab-scrubber strong")).toHaveText(
    `0.00 units · gap ${sample.counts[0].toFixed(3)}`,
  );
  await expect(page.locator(".lab-orbit-plot .orbit-reference")).toHaveCount(2);
  expect(await page.evaluate(() => Object.keys(localStorage))).toEqual([]);
});

test("a sealed-room protocol error explains the next step without a raw status", async ({
  page,
}) => {
  await page.goto("/#remote-viewing");
  await page.route("**/api/archive-session", (route) =>
    route.fulfill({
      status: 422,
      json: { detail: "Protocol_invalid" },
    }),
  );
  await page.getByRole("checkbox", { name: /share my transcript/ }).check();
  await button(page, "Seal a new target").click();
  await expect(page.getByRole("alert")).toContainText(
    "The recorded steps could not be verified.",
  );
  await expect(page.getByText("Protocol_invalid", { exact: true })).toHaveCount(
    0,
  );
});

test("Tarot keeps original motifs in depth and edits their labels in the payoff", async ({
  page,
}) => {
  await page.route("**/api/readings", (route) =>
    route.continue({
      postData: JSON.stringify({
        ...route.request().postDataJSON(),
        seed: "2f".padStart(64, "0"),
      }),
    }),
  );
  await page.goto("/#ritual");
  const draw = await exchange(page, "/api/readings", () =>
    button(page, "Draw my three cards").click(),
  );
  const third = draw.response.result.readings[2];
  expect(third.card.id).toBe("wands-four");
  expect(third.orientation).toBe("reversed");
  expect(third.direct_component.symbolic_focus).toBe(
    "unchanged:prosperity;increase;beauty",
  );
  await button(page, "Reveal card 3").click();
  await expect(page.locator(".reveal-insight")).toContainText(
    "prosperity, increase, beauty",
  );
  await button(page, "Skip reveal & read now").click();
  await expect(page.locator(".tarot-payoff")).toContainText(
    "prosperity, increase, beauty",
  );
  await expect(page.locator(".tarot-payoff")).not.toContainText("unchanged:");
  await page.locator(".native-motifs summary").click();
  await expect(page.locator(".native-motifs")).toContainText(
    "unchanged:prosperity",
  );
});

test("the narrow reduced-motion Gallery and key instruments pass accessibility scanning", async ({
  page,
}) => {
  await page.setViewportSize({ width: 320, height: 744 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  for (const hash of [
    "gallery",
    "remote-viewing",
    "prediction-market",
    "lorenz-chaos",
    "quantum-circuit",
  ]) {
    await page.goto("/#" + hash);
    await expect(page.locator("h1")).toBeVisible();
    if (["prediction-market", "lorenz-chaos", "quantum-circuit"].includes(hash))
      await expect(page.locator(".lab-payoff h2")).toBeVisible();
    expect(
      await page.evaluate(() => document.documentElement.scrollWidth),
    ).toBeLessThanOrEqual(320);
    const report = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(
      report.violations.map(({ id, nodes }) => [
        id,
        nodes.map(({ target }) => target),
      ]),
    ).toEqual([]);
  }
});
