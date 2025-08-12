// 🇨🇺 PACKFY - TEST DIRECTO DE TRACKING API
// Ejecuta este script en la consola del navegador

console.log("🚀 Iniciando prueba directa de tracking...");

// Test completo de la API de tracking
async function testTrackingAPI() {
  const guiaTest = "TEST001";

  console.log(`📦 Probando tracking para guía: ${guiaTest}`);

  try {
    // 1. Test directo al proxy
    console.log("🔄 1. Probando fetch directo al proxy...");
    const response = await fetch(
      `/api/envios/rastrear/?numero_guia=${guiaTest}`
    );

    console.log("📊 Response status:", response.status);
    console.log("📊 Response headers:", [...response.headers.entries()]);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("✅ Respuesta exitosa:", data);

    // 2. Test con error handling
    console.log("🔄 2. Test con guía inexistente...");
    const errorResponse = await fetch(
      "/api/envios/rastrear/?numero_guia=NOEXISTE"
    );
    console.log("📊 Error response status:", errorResponse.status);

    if (errorResponse.status === 404) {
      const errorData = await errorResponse.json();
      console.log("✅ Error handling correcto:", errorData);
    }

    // 3. Test sin parámetros
    console.log("🔄 3. Test sin parámetros...");
    const noParamsResponse = await fetch("/api/envios/rastrear/");
    console.log("📊 No params status:", noParamsResponse.status);

    return data;
  } catch (error) {
    console.error("❌ Error en test:", error);
    throw error;
  }
}

// Ejecutar test
testTrackingAPI()
  .then((result) => {
    console.log("🎉 Test completado exitosamente!");
    console.log("📄 Resultado final:", result);
  })
  .catch((error) => {
    console.error("💥 Test falló:", error);
  });

// Test adicional con XMLHttpRequest (alternativo)
function testWithXHR() {
  console.log("🔄 Probando con XMLHttpRequest...");

  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/api/envios/rastrear/?numero_guia=TEST001", true);

  xhr.onload = function () {
    if (xhr.status === 200) {
      console.log("✅ XHR Success:", JSON.parse(xhr.responseText));
    } else {
      console.error("❌ XHR Error:", xhr.status, xhr.responseText);
    }
  };

  xhr.onerror = function () {
    console.error("❌ XHR Network Error");
  };

  xhr.send();
}

// Ejecutar test XHR también
setTimeout(testWithXHR, 2000);

console.log("📝 Tests programados. Revisa los resultados arriba...");
