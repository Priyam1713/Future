export const journeys = [
  {
    id: 28,
    slug: "tea-leaves",
    values: ["rim", "anchor"],
    picks: ["Rim", "Anchor"],
    action: "Read my cup marks",
  },
  {
    id: 29,
    slug: "coffee-grounds",
    values: ["cup", "two_humped_camel"],
    picks: ["Cup", "Camel with two humps"],
    action: "Compare my grounds",
  },
  {
    id: 30,
    slug: "candle-lore",
    values: ["high", "persistent", "persisted", "hypothetical"],
    picks: [
      "High",
      "Persistent",
      "Persisted after reported correction",
      "Hypothetical example",
    ],
    action: "Compare the flame record",
  },
  {
    id: 31,
    slug: "water-signs",
    values: ["perceived_fogginess", "subjective", "source_context"],
    picks: [
      "Perceived fogginess",
      "Subjective",
      "Rainwater, dark bowl, soft gaze",
    ],
    action: "Open the water reference",
  },
  {
    id: 32,
    slug: "weather-lore",
    values: ["hake", "east_west", "bedfordshire"],
    picks: ["Hake-shaped cloud", "East–west axis", "Bedfordshire"],
    action: "Compare my sky note",
  },
  {
    id: 34,
    slug: "stone-table",
    values: ["onyx", "2:-1"],
    picks: ["Onyx", "Place stone at x 2, y -1"],
    action: "Read my stone placement",
  },
  {
    id: 35,
    slug: "bone-archive",
    values: ["9A+9B"],
    picks: ["Compare 9A and 9B"],
    action: "Open the documentary record",
  },
  {
    id: 37,
    slug: "letter-lot",
    values: ["gao-alpha"],
    picks: ["Alpha"],
    action: "Open this letter account",
  },
  {
    id: 38,
    slug: "bird-signs",
    values: ["crow", "call", "left"],
    picks: ["Crow", "Call located on that side", "Left"],
    action: "Compare my bird record",
  },
  {
    id: 39,
    slug: "roman-cases",
    values: ["liver_head", "absent", "sound"],
    picks: ["Liver head", "Absent", "Sound"],
    action: "Compare the written account",
  },
];
export async function openSign(page, slug, origin = "") {
  await page.goto(origin + "/#" + slug);
  await page.locator(".sign-intro h1").waitFor();
}
export async function alignSign(page, selector = ".sign-stage") {
  await page
    .locator(selector)
    .first()
    .evaluate((e) => e.scrollIntoView({ block: "start", behavior: "instant" }));
}
export async function perform(
  page,
  journey,
  onChoice = () => Promise.resolve(),
) {
  const stage = page.locator(".sign-stage");
  for (const pick of journey.picks) {
    await stage.getByRole("button", { name: pick, exact: true }).click();
    await onChoice();
  }
  const pending = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/world-of-signs") &&
      r.request().method() === "POST",
  );
  const start = performance.now();
  await stage
    .getByRole("button", { name: journey.action, exact: true })
    .click();
  const response = await pending;
  if (!response.ok()) throw new Error(await response.text());
  const data = await response.json();
  const request = response.request().postDataJSON();
  await page.locator(".sign-result").waitFor();
  return { ...data, request, actionMs: Math.round(performance.now() - start) };
}
