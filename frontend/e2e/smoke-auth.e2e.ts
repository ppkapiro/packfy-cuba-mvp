import { test, expect } from "@playwright/test";

// Smoke E2E: login -> dashboard -> logout

test.describe("Smoke Auth", () => {
  test("login dashboard logout", async ({ page }) => {
    // Ir al login
    await page.goto("/login");
    await expect(page).toHaveURL(/.*login.*/i);

    // Completar formulario
    await page.getByLabel(/correo/i).fill("admin@packfy.cu");
    await page.getByLabel(/contraseña/i).fill("admin123");

    // Enviar
    await page.getByRole("button", { name: /iniciar\s+sesión/i }).click();

    // Esperar redirección al dashboard
    await page.waitForURL(/.*dashboard.*/i, { timeout: 15000 });
    await expect(page.getByRole("heading", { level: 1 })).toContainText(
      /dashboard/i
    );

    // Abrir menú usuario y cerrar sesión (Layout muestra botón "Salir")
    await page.getByRole("button", { name: /salir/i }).click();

    // Debe volver a login
    await page.waitForURL(/.*login.*/i, { timeout: 10000 });
    await expect(page).toHaveURL(/.*login.*/i);
  });
});
