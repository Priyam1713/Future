const rooms = [
  [5, "horary"],
  [6, "mundane"],
  [7, "astrocartography"],
  [8, "palmistry"],
  [9, "face-reading"],
  [10, "phrenology"],
  [11, "moleosophy"],
  [12, "podomancy"],
  [13, "graphology"],
  [14, "aura"],
  [15, "iridology"],
  [40, "compass"],
];
const entries = {
  8: "Strongly sloping",
  9: "Forehead",
  10: "9 · Constructiveness",
  11: "Arm. (Right or Left.)",
  12: "Many long lines and strokes on the soles",
  13: "Ascending handwriting",
  14: "Pure pale rose",
  15: "Stomach",
};
export const journeys = rooms.map(([id, slug]) => ({
  id,
  slug,
  entry: entries[id],
}));
export const button = (page, name) =>
  page.getByRole("button", { name, exact: true });
export const align = (page, selector = ".folio-stage") =>
  page
    .locator(selector)
    .first()
    .evaluate((el) =>
      el.scrollIntoView({ block: "start", behavior: "instant" }),
    );
export async function openRoom(page, journey, origin = "") {
  await page.goto(origin + "/#" + journey.slug);
  await page.locator(".folio-stage").waitFor();
}
export async function perform(page, { id, entry }, pause = async () => {}) {
  const stage = page.locator(".folio-stage");
  if (id === 8) {
    await button(stage, "Head line").click();
    await pause();
    await button(stage, "Left hand").click();
    await pause();
  }
  if (id === 40) {
    await stage.getByLabel("Uncertainty ± (°)", { exact: true }).fill("0.2");
    await stage
      .getByRole("combobox", { name: "North reference", exact: true })
      .selectOption("magnetic");
    await pause();
    await stage.getByLabel("What the bearing describes").selectOption("door");
  }
  const pending = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/sky-manuscript") &&
      r.request().method() === "POST",
  );
  const start = performance.now();
  await button(
    stage,
    id < 8
      ? "Explore the teaching example"
      : id === 40
        ? "Classify the bearing"
        : entry,
  ).click();
  const response = await pending;
  if (!response.ok()) throw Error(await response.text());
  const data = await response.json();
  await stage.locator(".result-leaf").first().waitFor();
  return {
    request: response.request().postDataJSON(),
    ...data,
    actionMs: Math.round(performance.now() - start),
  };
}
