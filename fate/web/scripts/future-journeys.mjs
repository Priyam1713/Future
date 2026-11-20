export const rooms = [
  [24, "automatic-writing"],
  [26, "akashic"],
  [43, "remote-viewing"],
  [44, "prophetic-dreams"],
  [45, "intuitive-prediction"],
  [46, "deja-reve"],
  [49, "forecast-models"],
  [50, "quantum-circuit"],
  [51, "forecast-updates"],
  [52, "population-dynamics"],
  [53, "digital-twin"],
  [54, "cellular-automata"],
  [55, "intention-classifier"],
  [56, "causal-graphs"],
  [57, "collective-forecasts"],
  [58, "prediction-market"],
  [59, "lorenz-chaos"],
  [60, "scenario-trees"],
].map(([id, slug]) => ({ id, slug }));
export const button = (root, name) =>
  root.getByRole("button", { name, exact: true });
export const align = (page, selector = ".future-stage") =>
  page
    .locator(selector)
    .first()
    .evaluate((e) => e.scrollIntoView({ block: "start", behavior: "instant" }));
const matches = (r, path) =>
  r.url().endsWith(path) && r.request().method() === "POST";
export async function exchange(page, path, action) {
  const waiting = page.waitForResponse((r) => matches(r, path));
  const start = performance.now();
  await action();
  const response = await waiting;
  if (!response.ok()) throw Error(await response.text());
  return {
    wire: response.request().postDataJSON(),
    response: await response.json(),
    elapsedMs: Math.round(performance.now() - start),
  };
}
export const vault = (page, action) =>
  exchange(page, "/api/archive-session", action);
export async function open(page, room, origin = "") {
  await page.goto(origin + "/#" + room.slug);
  await page.locator(".future-stage").waitFor();
}
export async function runPublic(page, room, origin = "") {
  const waiting = page.waitForResponse((r) => matches(r, "/api/future-study"));
  const begun = performance.now();
  await open(page, room, origin);
  if (room.id === 44)
    await button(page, "Skip to a simulated ledger →").click();
  if (room.id < 49) await button(page, "Open the example").click();
  const r = await waiting;
  if (!r.ok()) throw Error(await r.text());
  const data = await r.json();
  await page.locator(".future-reading .result-leaf").waitFor();
  return {
    wire: r.request().postDataJSON(),
    ...data,
    actionMs: Math.round(performance.now() - begun),
  };
}
export async function blindTrial(
  viewer,
  judge,
  origin = "",
  pause = async () => {},
) {
  const room = rooms.find((r) => r.id === 43);
  await open(viewer, room, origin);
  await align(viewer);
  await viewer.getByRole("checkbox", { name: /share my transcript/ }).check();
  const started = await vault(viewer, () =>
    button(viewer, "Seal a new target").click(),
  );
  await viewer
    .getByLabel("Viewer transcript")
    .fill("Public QA impression: sharp corners and a dark field.");
  await pause(viewer);
  const locked = await vault(viewer, () =>
    button(viewer, "Lock transcript").click(),
  );
  await pause(viewer);
  await open(judge, room, origin);
  await judge.getByText("I have a judge invitation", { exact: true }).click();
  await judge
    .locator("details[open]")
    .getByLabel("Session code", { exact: true })
    .fill(locked.response.invite);
  const opened = await vault(judge, () =>
    button(judge, "Open session").click(),
  );
  await align(judge);
  const picks = judge
    .getByRole("group", { name: "Blind candidate ordering" })
    .getByRole("button");
  for (const candidate of await picks.all()) {
    await candidate.click();
    await pause(judge);
  }
  const revealed = await vault(judge, () =>
    button(judge, "Lock ranks and open the seal").click(),
  );
  await align(judge);
  const retrieved = await vault(viewer, () =>
    button(viewer, "Check for locked ranks").click(),
  );
  await align(viewer);
  return { started, locked, opened, revealed, retrieved };
}
