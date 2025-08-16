import { defineConfig, devices } from "@playwright/test";

// 🇨🇺 Config Playwright E2E mínima para dev local (servidor ya levantado en 5173)
export default defineConfig({
  testDir: "./e2e",
  testMatch: "**/*.e2e.{ts,tsx,js}",
  reporter: [["list"]],
  use: {
    baseURL: process.env.E2E_BASE_URL || "http://localhost:5173",
    headless: true,
    ignoreHTTPSErrors: true, // Certificado dev
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  // No lanzamos webServer: usamos el que corre en Docker
});
