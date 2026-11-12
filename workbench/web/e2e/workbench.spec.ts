import { test, expect } from "@playwright/test";
import { mkdirSync } from "node:fs";
const key = () => ({ "Idempotency-Key": crypto.randomUUID() });
test('palmistry starts with photo intake and no silent sample run',async({page})=>{
 await page.goto('/');await page.getByLabel('Search techniques').fill('Palmistry');await page.locator('.engine-card').filter({has:page.getByRole('heading',{name:'Palmistry',exact:true})}).click();await expect(page.getByRole('heading',{name:'Start with your palm photo'})).toBeVisible();await page.getByRole('button',{name:'Run technique',exact:true}).click();await expect(page.getByRole('alert')).toContainText('Analyze your palm photo');await expect(page.getByRole('button',{name:'Analyze palm photo'})).toBeDisabled();
});
test("all 54 engines run from their actual browser forms", async ({
  page,
  request,
}) => {
  const registry = await (await request.get("/api/registry")).json();
  await page.goto("/");
  await expect(page.locator(".engine-card")).toHaveCount(54);
  mkdirSync("../screenshots", { recursive: true });
  await page.screenshot({
    path: "../screenshots/explorer-desktop.png",
    fullPage: false,
  });
  for (const engine of registry.entries) {
    await page
      .locator(".engine-card")
      .filter({
        has: page.getByRole("heading", { name: engine.name, exact: true }),
      })
      .click();
    await expect(
      page.getByRole("heading", { name: engine.name, exact: true }),
    ).toBeVisible();
    await page.getByRole('button',{name:'Load verified sample'}).click();
    const response = page.waitForResponse(
      (r) =>
        r.url().endsWith("/api/sessions") && r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "Run technique", exact: true })
      .click();
    const r = await response;
    expect(r.status(), `#${engine.technique_id}`).toBe(200);
    const v = await r.json();
    expect(v.result.native_error, `#${engine.technique_id}`).toBeNull();
    await expect(
      page.locator(".results .badge").filter({ hasText: "returned" }),
    ).toBeVisible();
    await page
      .locator("nav")
      .getByRole("button", { name: "Explore", exact: true })
      .click();
    await expect(page.locator(".engine-card")).toHaveCount(54);
  }
});
test("discovery, invalid native request, operation boundary and dark tablet layout", async ({
  page,
  request,
}) => {
  await page.goto("/");
  await page.getByLabel("Search techniques").fill("Numerology");
  await expect(
    page
      .locator(".engine-card")
      .filter({
        has: page.getByRole("heading", { name: "Numerology", exact: true }),
      }),
  ).toHaveCount(1);
  await page
    .locator(".engine-card")
    .filter({
      has: page.getByRole("heading", { name: "Numerology", exact: true }),
    })
    .click();
  await page.getByRole('button',{name:'Load verified sample'}).click();
  await page.getByLabel("birth", { exact: true }).fill("not-a-date");
  await page
    .getByRole("button", { name: "Validate input", exact: true })
    .click();
  await expect(page.locator(".results")).toContainText("native_rejected");
  await page.getByRole("button", { name: "Load verified sample" }).click();
  await page
    .getByRole("button", { name: "Run technique", exact: true })
    .click();
  await expect(page.locator(".results")).toContainText("returned");
  const sample = await (await request.get("/api/techniques/4")).json();
  const unsupported = await request.post("/api/validate", {
    data: { ...sample.sample, operation: "unsupported" },
  });
  expect(unsupported.status()).toBe(422);
  await page.getByRole("button", { name: "Toggle color theme" }).click();
  await expect(page.locator("html")).toHaveClass("dark");
  await page.setViewportSize({ width: 820, height: 1180 });
  await page.screenshot({ path: "../screenshots/studio-tablet-dark.png" });
});
test("consented participant, case, blind freeze/lock/reveal and local deletion", async ({
  page,
  request,
}) => {
  await page.goto("/");
  await page
    .locator("nav")
    .getByRole("button", { name: "Cases", exact: true })
    .click();
  await page
    .getByLabel("Nickname (optional)", { exact: true })
    .fill("Voluntary browser fixture");
  await page.getByLabel("Blind", { exact: true }).check();
  await page.getByLabel("Participant explicitly consents").check();
  await page
    .getByRole("button", { name: "Create participant", exact: true })
    .click();
  await expect(
    page.locator(".record").filter({ hasText: "Voluntary browser fixture" }),
  ).toBeVisible();
  const participants = await (await request.get("/api/records")).json();
  const p = participants.find(
    (v: any) =>
      v.kind === "participant" && v.nickname === "Voluntary browser fixture",
  );
  await page.getByLabel("Participant", { exact: true }).selectOption(p.id);
  await page
    .getByLabel("Case title", { exact: true })
    .fill("Consented browser blind case");
  await page.getByRole("button", { name: "Create case", exact: true }).click();
  await expect(
    page.locator(".record").filter({ hasText: "Consented browser blind case" }),
  ).toBeVisible();
  await page
    .locator(".record")
    .filter({ hasText: "Consented browser blind case" })
    .getByRole("button", { name: "Run a technique" })
    .click();
  await page.getByLabel("Search techniques").fill("Numerology");
  await page
    .locator(".engine-card")
    .filter({
      has: page.getByRole("heading", { name: "Numerology", exact: true }),
    })
    .click();
  await page.getByRole('button',{name:'Load verified sample'}).click();
  await page.getByText("Session context & mode", { exact: true }).click();
  await page
    .getByText("Testing mode", { exact: true })
    .locator("..")
    .getByRole("combobox")
    .selectOption("blind");
  await page
    .getByLabel("Hidden answer (assessor setup)", { exact: true })
    .fill("secret-browser-answer");
  await page
    .getByRole("button", { name: "Run technique", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Record interpretation before reveal" }),
  ).toBeVisible();
  expect((await request.get("/api/export")).status()).toBe(200);
  expect(await (await request.get("/api/export")).text()).not.toContain(
    "secret-browser-answer",
  );
  await expect(page.getByRole("button", { name: "Reveal answer" })).toHaveCount(
    0,
  );
  await page
    .getByLabel("Immutable interpretation", { exact: true })
    .fill("Interpretation recorded before reveal");
  await page
    .getByRole("button", { name: "Lock interpretation", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Reveal answer" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Reveal answer" }).click();
  await expect(page.locator(".blind-box")).toContainText(
    "secret-browser-answer",
  );
  await page
    .getByLabel("Independent assessor", { exact: true })
    .fill("Independent browser assessor");
  await page.getByRole("button", { name: "Record feedback" }).click();
  await page
    .locator("nav")
    .getByRole("button", { name: "Cases", exact: true })
    .click();
  await page
    .locator(".record")
    .filter({ hasText: "Voluntary browser fixture" })
    .getByRole("button", { name: "Delete participant" })
    .click();
  await page.getByRole("button", { name: "Confirm local deletion" }).click();
  await expect(
    page.locator(".record").filter({ hasText: "Voluntary browser fixture" }),
  ).toHaveCount(0);
});
test("prospective UI creates pending forecast then independent resolution and exact scoring", async ({
  page,
  request,
}) => {
  await request.post("/__test__/clock", {
    data: { at: "2030-01-01T00:00:00Z" },
  });
  await page.goto("/");
  await page
    .locator("nav")
    .getByRole("button", { name: "Blind & forecast", exact: true })
    .click();
  const fields: Record<string, string> = {
    "Unambiguous future event":
      "Will fixture event occur in the independently logged window?",
    "Probability (0–1 or fraction)": "3/5",
    "Forecast cutoff (local time)": "2030-01-02T00:00",
    "Complete observation window end (local time)": "2030-01-03T00:00",
    "Positive resolution rule": "Event logged within window",
    "Negative resolution rule": "No event in complete log",
    "Independent resolution source / locator":
      "local:independent-browser-fixture",
    "Self-authored protocol / evidence snapshot":
      "Self-authored test protocol, not empirical data",
    "Forecast reasoning": "Declared test judgment",
  };
  for (const [label, value] of Object.entries(fields))
    await page.getByLabel(label, { exact: true }).fill(value);
  await page.getByLabel("I confirm binary clarity").check();
  await page.getByRole("button", { name: "Lock prospective forecast" }).click();
  await expect(
    page
      .locator(".record")
      .filter({ hasText: fields["Unambiguous future event"] }),
  ).toBeVisible();
  await page
    .locator(".record")
    .filter({ hasText: fields["Unambiguous future event"] })
    .getByRole("button", { name: "Inspect / resolve" })
    .click();
  const rows = await (await request.get("/api/records")).json();
  const s = rows.find(
    (v: any) =>
      v.kind === "study" && v.title === fields["Unambiguous future event"],
  );
  expect(s.report.coverage.matched).toBe(0);
  expect(s.report.cases[0].outcome_status).toBe("unrecorded");
  await request.post("/__test__/clock", {
    data: { at: "2030-01-04T00:00:00Z" },
  });
  await page
    .getByLabel("Outcome known at (local time)", { exact: true })
    .fill("2030-01-03T05:30");
  await page
    .getByLabel("Independent assessor", { exact: true })
    .fill("Separate assessor");
  await page
    .getByLabel("Resolution reason", { exact: true })
    .fill("Independent complete log");
  await page
    .getByLabel("Self-authored independent outcome evidence snapshot", {
      exact: true,
    })
    .fill("Complete log records event; synthetic browser fixture");
  const response = page.waitForResponse((r) => r.url().endsWith("/outcome"));
  await page
    .getByRole("button", { name: "Record outcome / disposition" })
    .click();
  const r = await response;
  expect(r.status()).toBe(200);
  const scored = await r.json();
  expect(scored.report.model.brier.exact).toBe("4/25");
  expect(scored.report.baseline.brier.exact).toBe("1/4");
  await page
    .locator("nav")
    .getByRole("button", { name: "Research", exact: true })
    .click();
  await expect(page.locator(".metrics")).toContainText("Eligible Scored");
});
test("portable export import, tamper rejection, idempotency and privacy boundaries", async ({
  page,
  request,
}) => {
  await page.goto("/");
  await page
    .locator("nav")
    .getByRole("button", { name: "Research", exact: true })
    .click();
  const exportResponse = await request.get("/api/export");
  const exactExport = await exportResponse.text();
  const e = await exportResponse.json();
  const pendingDownload = page.waitForEvent("download");
  await page.getByRole("button", { name: "JSON export", exact: true }).click();
  const file = await pendingDownload;
  const stream = await file.createReadStream();
  const chunks: Buffer[] = [];
  for await (const chunk of stream!) chunks.push(Buffer.from(chunk));
  expect(Buffer.concat(chunks).toString("utf8")).toBe(exactExport);
  await page.getByLabel("Import JSON", { exact: true }).setInputFiles({
    name: "fixture.json",
    mimeType: "application/json",
    buffer: Buffer.from(exactExport),
  });
  await expect(page.getByRole("alert")).toHaveCount(0);
  const imported = await request.post("/api/import", {
    data: exactExport,
    headers: { ...key(), "Content-Type": "application/json" },
  });
  expect(imported.status()).toBe(200);
  expect((await imported.json()).imported).toBe(0);
  const bad = structuredClone(e);
  bad.sha256 = "0".repeat(64);
  expect(
    (await request.post("/api/import", { data: bad, headers: key() })).status(),
  ).toBe(422);
  const sample = await (await request.get("/api/techniques/4")).json();
  const headers = key();
  const body = { request: sample.sample, origin: "sample" };
  const a = await (
    await request.post("/api/sessions", { data: body, headers })
  ).json();
  const b = await (
    await request.post("/api/sessions", { data: body, headers })
  ).json();
  expect(a.id).toBe(b.id);
  const countBefore = (await (await request.get("/api/records")).json()).length;
  await page
    .locator("nav")
    .getByRole("button", { name: "Cases", exact: true })
    .click();
  await page.getByText(/^Unlinked local runs & forecasts \(/).click();
  await page
    .getByRole("button", { name: "Delete unlinked record", exact: true })
    .first()
    .click();
  await page.getByRole("button", { name: "Confirm local deletion" }).click();
  await expect
    .poll(async () => (await (await request.get("/api/records")).json()).length)
    .toBe(countBefore - 1);
  expect(
    (
      await request.get("/api/records", {
        headers: { Origin: "https://foreign.example" },
      })
    ).status(),
  ).toBe(403);
  expect(
    (
      await request.post("/api/validate", {
        data: '{"x":1,"x":2}',
        headers: { "Content-Type": "application/json" },
      })
    ).status(),
  ).toBe(422);
});

test('personal tarot question and monthly observations run without demonstration data',async({page})=>{
 await page.goto('/');await page.getByLabel('Search techniques').fill('Tarot');await page.locator('.engine-card').first().click();await page.getByLabel('Your question',{exact:true}).fill('How can I organize my study time?');await page.getByRole('button',{name:'Prepare my card draw'}).click();let response=page.waitForResponse(r=>r.url().endsWith('/api/sessions')&&r.request().method()==='POST');await page.getByRole('button',{name:'Run technique',exact:true}).click();let result=await(await response).json();expect(result.result.native_error).toBeNull();expect(result.origin).toBe('manual');
 await page.locator('nav').getByRole('button',{name:'Explore',exact:true}).click();await page.getByLabel('Search techniques').fill('AI Predictive');await page.locator('.engine-card').first().click();await page.getByLabel('Monthly observations: YYYY-MM, value').fill('2026-01, 10\n2026-02, 12\n2026-03, 14');await page.getByLabel('Measurement units').fill('counts');await page.getByLabel('Where did these observations come from?').fill('My test measurements');await page.getByLabel('Forecast method').selectOption('drift');await page.getByText('These are my own observations and I have permission to use them').click();await page.getByRole('button',{name:'Prepare monthly forecast'}).click();await expect(page.getByRole('heading',{name:'Forecast your monthly measurements'})).toHaveCount(0);response=page.waitForResponse(r=>r.url().endsWith('/api/sessions')&&r.request().method()==='POST');await page.getByRole('button',{name:'Run technique',exact:true}).click();result=await(await response).json();expect(result.result.native_error).toBeNull();expect(result.result.native_output.result.cells[0].prediction.exact).toBe('16');
});
