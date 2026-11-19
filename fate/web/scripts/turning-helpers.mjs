import { fillBirth } from "./western-helpers.mjs";
export async function enterTurning(page, days = 7) {
  await fillBirth(page);
  const natalResponse = page.waitForResponse((r) =>
    r.url().endsWith("/api/western"),
  );
  await page
    .getByRole("button", { name: "Open my celestial chart", exact: true })
    .click();
  const envelope = await (await natalResponse).json();
  await page
    .getByRole("button", { name: "Skip reveal & read my chart" })
    .click();
  await page
    .getByRole("button", { name: "Enter The Turning Sky", exact: false })
    .click();
  await page.getByLabel("Start date and time · UTC").fill("2026-11-19T00:00");
  await page.getByLabel("Days to explore").selectOption(String(days));
  const response = page.waitForResponse((r) =>
    r.url().endsWith("/api/western/transits"),
  );
  await page.getByRole("button", { name: "Turn my sky", exact: false }).click();
  const reply = await response;
  const result = await reply.json();
  if (!reply.ok()) throw new Error(JSON.stringify(result));
  await page.locator(".turning-experience").waitFor();
  return { natal: envelope.result, origin: envelope.transit_origin, result };
}
