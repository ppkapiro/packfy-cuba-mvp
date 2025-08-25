// 🇨🇺 PACKFY - TEST DE API DESDE NAVEGADOR
// Copia y pega este código en la consola del navegador para probar la conectividad

console.log("🚀 Iniciando test de conectividad API...");

// Test 1: Verificar configuración de API
console.log("📍 URL actual:", window.location.href);
console.log("🌐 Host:", window.location.hostname);
console.log("🔌 Puerto:", window.location.port);

// Test 2: Probar fetch directo al proxy
fetch("/api/")
  .then((response) => {
    console.log(
      "✅ Respuesta proxy /api/:",
      response.status,
      response.statusText
    );
    return response.text();
  })
  .then((data) => {
    console.log("📄 Contenido respuesta /api/:", data);
  })
  .catch((error) => {
    console.error("❌ Error en /api/:", error);
  });

// Test 3: Probar endpoint específico de tracking
fetch("/api/tracking/test-guia/")
  .then((response) => {
    console.log("📦 Respuesta tracking:", response.status, response.statusText);
    return response.text();
  })
  .then((data) => {
    console.log("📄 Contenido tracking:", data);
  })
  .catch((error) => {
    console.error("❌ Error en tracking:", error);
  });

// Test 4: Verificar CORS
fetch("/api/", {
  method: "OPTIONS",
})
  .then((response) => {
    console.log("🔧 Headers CORS:", response.headers);
    console.log("✅ CORS Status:", response.status);
  })
  .catch((error) => {
    console.error("❌ Error CORS:", error);
  });

console.log("🏁 Tests iniciados. Revisa los resultados arriba...");
