// Script para debuggear problemas de conexión frontend-backend
// Ejecutar en la consola del navegador

console.log("🔍 DIAGNÓSTICO PACKFY FRONTEND-BACKEND");

// Test 1: Verificar configuración de API
console.log("1. Verificando configuración de API...");
try {
  // Simular importación del API client
  console.log("URL actual:", window.location.href);
  console.log("Hostname:", window.location.hostname);
  console.log("Port:", window.location.port);
} catch (e) {
  console.error("Error en configuración:", e);
}

// Test 2: Probar health check
console.log("2. Probando health check...");
fetch("/api/health/")
  .then((response) => response.json())
  .then((data) => console.log("✅ Health check OK:", data))
  .catch((error) => console.error("❌ Health check falló:", error));

// Test 3: Probar login sin tenant
console.log("3. Probando login sin tenant...");
fetch("/api/auth/login/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    email: "superadmin@packfy.com",
    password: "super123!",
  }),
})
  .then((response) => {
    console.log("Status sin tenant:", response.status);
    return response.json();
  })
  .then((data) => console.log("Respuesta sin tenant:", data))
  .catch((error) => console.error("❌ Login sin tenant falló:", error));

// Test 4: Probar login con tenant
console.log("4. Probando login con tenant...");
fetch("/api/auth/login/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-Tenant-Slug": "packfy-express",
  },
  body: JSON.stringify({
    email: "superadmin@packfy.com",
    password: "super123!",
  }),
})
  .then((response) => {
    console.log("✅ Status con tenant:", response.status);
    return response.json();
  })
  .then((data) => {
    console.log("✅ Respuesta con tenant:", data);
    if (data.access) {
      console.log(
        "🎉 LOGIN EXITOSO! Token:",
        data.access.substring(0, 20) + "..."
      );

      // Test 5: Probar endpoint protegido
      console.log("5. Probando endpoint protegido...");
      return fetch("/api/usuarios/me/", {
        headers: {
          Authorization: `Bearer ${data.access}`,
          "X-Tenant-Slug": "packfy-express",
        },
      });
    }
  })
  .then((response) => {
    if (response) {
      console.log("Status /me/:", response.status);
      return response.json();
    }
  })
  .then((data) => {
    if (data) {
      console.log("✅ Usuario actual:", data);
    }
  })
  .catch((error) => console.error("❌ Login con tenant falló:", error));

console.log("🔍 Diagnóstico completado. Revisa los resultados arriba.");
