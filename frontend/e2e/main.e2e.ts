// 🇨🇺 PACKFY CUBA - Tests E2E Principales v4.0

import { test, expect } from "@playwright/test";

// Configuración común
test.beforeEach(async ({ page }) => {
  // Interceptar llamadas a API para datos consistentes
  await page.route("**/api/envios**", async (route) => {
    const mockData = {
      count: 2,
      results: [
        {
          id: 1,
          numero_guia: "TEST123456",
          estado_actual: "PENDIENTE",
          remitente_nombre: "Juan Pérez",
          destinatario_nombre: "María García",
          descripcion: "Paquete de prueba",
          peso: 2.5,
        },
        {
          id: 2,
          numero_guia: "TEST789012",
          estado_actual: "EN_TRANSITO",
          remitente_nombre: "Ana López",
          destinatario_nombre: "Carlos Ruiz",
          descripcion: "Otro paquete",
          peso: 1.0,
        },
      ],
    };
    await route.fulfill({ json: mockData });
  });
});

test.describe("Navegación Principal", () => {
  test("debe cargar la página de inicio", async ({ page }) => {
    await page.goto("/");

    // Verificar que el título esté presente
    await expect(page).toHaveTitle(/PACKFY CUBA/i);

    // Verificar elementos principales del navbar
    await expect(page.locator('[data-testid="navbar"]')).toBeVisible();
    await expect(page.locator('[data-testid="logo"]')).toBeVisible();
  });

  test("debe navegar entre secciones principales", async ({ page }) => {
    await page.goto("/");

    // Navegar a envíos
    await page.click('[data-testid="nav-envios"]');
    await expect(page.locator("h1")).toContainText("Envíos");

    // Navegar a rastreo
    await page.click('[data-testid="nav-rastreo"]');
    await expect(page.locator("h1")).toContainText("Rastrear");

    // Verificar URL cambios
    expect(page.url()).toContain("/rastreo");
  });

  test("debe ser responsive en dispositivos móviles", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");

    // Verificar que el menú hamburguesa esté visible
    await expect(
      page.locator('[data-testid="mobile-menu-button"]')
    ).toBeVisible();

    // Abrir menú móvil
    await page.click('[data-testid="mobile-menu-button"]');
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
  });
});

test.describe("Gestión de Envíos", () => {
  test("debe mostrar lista de envíos", async ({ page }) => {
    await page.goto("/envios");

    // Esperar a que cargue la lista
    await expect(page.locator('[data-testid="envios-lista"]')).toBeVisible();

    // Verificar que se muestran los envíos mockeados
    await expect(page.locator("text=TEST123456")).toBeVisible();
    await expect(page.locator("text=TEST789012")).toBeVisible();

    // Verificar estados
    await expect(page.locator("text=PENDIENTE")).toBeVisible();
    await expect(page.locator("text=EN_TRANSITO")).toBeVisible();
  });

  test("debe abrir modal de crear envío", async ({ page }) => {
    await page.goto("/envios");

    // Hacer clic en botón de crear
    await page.click('[data-testid="crear-envio-btn"]');

    // Verificar que el modal se abre
    await expect(
      page.locator('[data-testid="modal-crear-envio"]')
    ).toBeVisible();

    // Verificar campos del formulario
    await expect(page.locator('[name="numero_guia"]')).toBeVisible();
    await expect(page.locator('[name="remitente_nombre"]')).toBeVisible();
    await expect(page.locator('[name="destinatario_nombre"]')).toBeVisible();
  });

  test("debe validar formulario de envío", async ({ page }) => {
    await page.goto("/envios");
    await page.click('[data-testid="crear-envio-btn"]');

    // Intentar enviar formulario vacío
    await page.click('[data-testid="submit-envio"]');

    // Verificar mensajes de error
    await expect(page.locator("text=campo requerido")).toBeVisible();

    // Llenar campos requeridos
    await page.fill('[name="numero_guia"]', "NEW123456");
    await page.fill('[name="remitente_nombre"]', "Nuevo Remitente");
    await page.fill('[name="destinatario_nombre"]', "Nuevo Destinatario");

    // Verificar que errores desaparecen
    await expect(page.locator("text=campo requerido")).not.toBeVisible();
  });

  test("debe filtrar envíos por búsqueda", async ({ page }) => {
    await page.goto("/envios");

    // Esperar a que cargue la lista
    await expect(page.locator('[data-testid="envios-lista"]')).toBeVisible();

    // Buscar por número de guía
    await page.fill('[data-testid="search-input"]', "TEST123");

    // Verificar filtrado
    await expect(page.locator("text=TEST123456")).toBeVisible();
    await expect(page.locator("text=TEST789012")).not.toBeVisible();

    // Limpiar búsqueda
    await page.fill('[data-testid="search-input"]', "");
    await expect(page.locator("text=TEST789012")).toBeVisible();
  });

  test("debe cambiar estado de envío", async ({ page }) => {
    await page.goto("/envios");

    // Hacer clic en envío específico
    await page.click('[data-testid="envio-TEST123456"]');

    // Cambiar estado
    await page.click('[data-testid="cambiar-estado-btn"]');
    await page.selectOption('[name="nuevo_estado"]', "EN_TRANSITO");
    await page.fill('[name="observaciones"]', "Cambio de estado E2E");
    await page.click('[data-testid="confirmar-cambio-estado"]');

    // Verificar cambio exitoso (dependiendo de implementación)
    await expect(page.locator("text=Estado actualizado")).toBeVisible();
  });
});

test.describe("Rastreo Público", () => {
  test("debe permitir rastrear envío público", async ({ page }) => {
    await page.goto("/rastreo");

    // Verificar formulario de rastreo
    await expect(page.locator('[data-testid="rastreo-form"]')).toBeVisible();
    await expect(page.locator('[name="numero_guia"]')).toBeVisible();

    // Ingresar número de guía
    await page.fill('[name="numero_guia"]', "TEST123456");
    await page.click('[data-testid="rastrear-btn"]');

    // Verificar resultados (mock del API)
    await expect(page.locator("text=Juan Pérez")).toBeVisible();
    await expect(page.locator("text=María García")).toBeVisible();
    await expect(page.locator("text=PENDIENTE")).toBeVisible();
  });

  test("debe mostrar error con número inválido", async ({ page }) => {
    // Mock error response
    await page.route("**/api/seguimiento**", async (route) => {
      await route.fulfill({
        status: 404,
        json: { error: "Envío no encontrado" },
      });
    });

    await page.goto("/rastreo");

    // Ingresar número inválido
    await page.fill('[name="numero_guia"]', "INVALID123");
    await page.click('[data-testid="rastrear-btn"]');

    // Verificar mensaje de error
    await expect(page.locator("text=Envío no encontrado")).toBeVisible();
  });

  test("debe mostrar historial de estados", async ({ page }) => {
    // Mock con historial
    await page.route("**/api/seguimiento**", async (route) => {
      const mockData = {
        numero_guia: "TEST123456",
        estado_actual: "EN_TRANSITO",
        historial: [
          { estado: "PENDIENTE", fecha: "2024-01-15T10:00:00Z" },
          { estado: "EN_TRANSITO", fecha: "2024-01-16T14:30:00Z" },
        ],
      };
      await route.fulfill({ json: mockData });
    });

    await page.goto("/rastreo");
    await page.fill('[name="numero_guia"]', "TEST123456");
    await page.click('[data-testid="rastrear-btn"]');

    // Verificar historial
    await expect(
      page.locator('[data-testid="historial-estados"]')
    ).toBeVisible();
    await expect(page.locator("text=PENDIENTE")).toBeVisible();
    await expect(page.locator("text=EN_TRANSITO")).toBeVisible();
  });
});

test.describe("Autenticación", () => {
  test("debe redirigir a login cuando no autenticado", async ({ page }) => {
    await page.goto("/envios");

    // Verificar redirección a login
    await expect(page).toHaveURL(/.*login.*/i);
    await expect(page.locator('[data-testid="login-form"]')).toBeVisible();
  });

  test("debe permitir login con credenciales válidas", async ({ page }) => {
    // Mock successful login
    await page.route("**/api/auth/login**", async (route) => {
      await route.fulfill({
        json: {
          access: "mock-access-token",
          refresh: "mock-refresh-token",
          user: { id: 1, username: "testuser" },
        },
      });
    });

    await page.goto("/login");

    // Llenar formulario de login
    await page.fill('[name="username"]', "testuser");
    await page.fill('[name="password"]', "testpass");
    await page.click('[data-testid="login-submit"]');

    // Verificar redirección exitosa
    await expect(page).toHaveURL("/");
    await expect(page.locator("text=Bienvenido")).toBeVisible();
  });

  test("debe mostrar error con credenciales inválidas", async ({ page }) => {
    // Mock failed login
    await page.route("**/api/auth/login**", async (route) => {
      await route.fulfill({
        status: 401,
        json: { error: "Credenciales inválidas" },
      });
    });

    await page.goto("/login");

    await page.fill('[name="username"]', "wronguser");
    await page.fill('[name="password"]', "wrongpass");
    await page.click('[data-testid="login-submit"]');

    // Verificar mensaje de error
    await expect(page.locator("text=Credenciales inválidas")).toBeVisible();
    await expect(page).toHaveURL("/login");
  });
});

test.describe("Performance y Accesibilidad", () => {
  test("debe cargar rápidamente", async ({ page }) => {
    const startTime = Date.now();
    await page.goto("/");
    const loadTime = Date.now() - startTime;

    // Verificar que carga en menos de 3 segundos
    expect(loadTime).toBeLessThan(3000);
  });

  test("debe tener elementos accesibles", async ({ page }) => {
    await page.goto("/");

    // Verificar landmarks principales
    await expect(page.locator('nav[role="navigation"]')).toBeVisible();
    await expect(page.locator("main")).toBeVisible();

    // Verificar alt text en imágenes
    const images = page.locator("img");
    const count = await images.count();
    for (let i = 0; i < count; i++) {
      const alt = await images.nth(i).getAttribute("alt");
      expect(alt).toBeTruthy();
    }
  });

  test("debe funcionar con teclado", async ({ page }) => {
    await page.goto("/");

    // Navegar con Tab
    await page.keyboard.press("Tab");
    await page.keyboard.press("Tab");

    // Verificar que hay elementos focusables
    const focusedElement = page.locator(":focus");
    await expect(focusedElement).toBeVisible();

    // Activar con Enter
    await page.keyboard.press("Enter");
  });
});
