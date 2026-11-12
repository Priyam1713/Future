import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./e2e",
  timeout: 180000,
  workers: 1,
  retries: 0,
  use: {
    channel: process.env.FUTURE_TEST_BROWSER || undefined,
    baseURL: "http://127.0.0.1:8765",
    viewport: { width: 1440, height: 1000 },
    launchOptions: { args: ["--disable-gpu"] },
    trace: "retain-on-failure",
  },
  reporter: [["list"], ["json", { outputFile: "../browser-acceptance.json" }]],
  webServer: {
    command: "python -m workbench.e2e_server",
    cwd: "../..",
    url: "http://127.0.0.1:8765/api/registry",
    timeout: 30000,
    reuseExistingServer: false,
  },
});
