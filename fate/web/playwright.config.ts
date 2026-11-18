import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./e2e",
  timeout: 90000,
  workers: 1,
  retries: 0,
  use: {
    baseURL: "http://127.0.0.1:8010",
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    launchOptions: {
      args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
    },
    trace: "retain-on-failure",
  },
  reporter: [["list"], ["json", { outputFile: "../browser-acceptance.json" }]],
  webServer: {
    command: "python -m fate --no-build",
    cwd: "../..",
    url: "http://127.0.0.1:8010/api/health",
    reuseExistingServer: false,
    timeout: 30000,
  },
});
