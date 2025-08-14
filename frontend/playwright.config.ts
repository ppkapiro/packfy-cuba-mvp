// 🇨🇺 PACKFY CUBA - Configuración Playwright E2E v4.0

import { defineConfig, devices } from "@playwright/test";

/**
 * Configuración de Playwright para tests End-to-End
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: "./e2e",

  /* Ejecutar tests en paralelo dentro de archivos */
  fullyParallel: true,

  /* Fallar si quedan archivos de test en repo */
  forbidOnly: !!process.env.CI,

  /* Reintentos en CI */
  retries: process.env.CI ? 2 : 0,

  /* Workers en paralelo */
  workers: process.env.CI ? 1 : undefined,

  /* Configuración de reportes */
  reporter: [
    ["html"],
    ["json", { outputFile: "./e2e-results/results.json" }],
    ["junit", { outputFile: "./e2e-results/junit.xml" }],
  ],

  /* Configuración global para todos tests */
  use: {
    /* URL base para el comando await page.goto('/') */
    baseURL: process.env.E2E_BASE_URL || "http://localhost:5173",

    /* Recopilar trace en primer retry */
    trace: "on-first-retry",

    /* Screenshots solo en fallos */
    screenshot: "only-on-failure",

    /* Video solo en fallos */
    video: "retain-on-failure",

    /* Timeout global para acciones */
    actionTimeout: 10000,

    /* Timeout para navegación */
    navigationTimeout: 30000,
  },

  /* Configuración de proyectos para diferentes navegadores */
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },

    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },

    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },

    /* Tests en dispositivos móviles */
    {
      name: "Mobile Chrome",
      use: { ...devices["Pixel 5"] },
    },
    {
      name: "Mobile Safari",
      use: { ...devices["iPhone 12"] },
    },

    /* Tests en Microsoft Edge */
    {
      name: "Microsoft Edge",
      use: { ...devices["Desktop Edge"], channel: "msedge" },
    },

    /* Tests en Google Chrome */
    {
      name: "Google Chrome",
      use: { ...devices["Desktop Chrome"], channel: "chrome" },
    },
  ],

  /* Configuración del servidor de desarrollo */
  webServer: {
    command: "npm run dev",
    url: "http://localhost:5173",
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },

  /* Timeout global para tests */
  timeout: 30000,

  /* Timeout para expect assertions */
  expect: {
    timeout: 5000,
  },

  /* Directorio de salida para artifacts */
  outputDir: "./e2e-results/",

  /* Configuración de test match */
  testMatch: "**/*.e2e.{js,ts}",
});
