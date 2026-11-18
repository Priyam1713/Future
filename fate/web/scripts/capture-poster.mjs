// Offline-only art pipeline. Capture the exact sphere scene with no React UI.
import { chromium } from "playwright";
import { readdirSync, writeFileSync } from "node:fs";
const file = readdirSync("dist/assets").find(
  (name) => name.startsWith("createOrbScene-") && name.endsWith(".js"),
);
if (!file) throw new Error("Build the frontend first.");
const browser = await chromium.launch({
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
});
try {
  const page = await browser.newPage({
    viewport: { width: 1200, height: 900 },
    deviceScaleFactor: 2,
  });
  await page.goto(process.env.FATE_CAPTURE_URL || "http://127.0.0.1:8010");
  const data = await page.evaluate(async (file) => {
    const module = await import("/assets/" + file);
    const namespace = Object.values(module).find(
      (value) =>
        value && typeof value === "object" && "createOrbScene" in value,
    );
    const createOrbScene = module.createOrbScene || namespace?.createOrbScene;
    if (!createOrbScene)
      throw new Error("Renderer export not found in the built module.");
    const host = document.createElement("div");
    host.style.cssText = "width:600px;height:600px;position:fixed;left:0;top:0";
    document.body.append(host);
    const scene = await createOrbScene(
      host,
      { reduced: true, paused: true },
      new AbortController().signal,
      () => {},
    );
    try {
      return await scene.snapshot();
    } finally {
      scene.destroy();
      host.remove();
    }
  }, file);
  writeFileSync(
    "../design/sources/orb-poster-v2.png",
    Buffer.from(data.split(",")[1], "base64"),
  );
  console.log("Saved a renderer-derived still, with no text or controls.");
} finally {
  await browser.close();
}
