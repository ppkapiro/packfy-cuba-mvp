// 🇨🇺 PACKFY - TEST DE BÚSQUEDA POR NOMBRES
// Ejecuta este script en la consola del navegador para probar las nuevas funciones

console.log("🚀 Iniciando pruebas de búsqueda por nombres...");

// Test de búsqueda por remitente
async function testBusquedaRemitente() {
  console.log("\n👤 === PRUEBA BÚSQUEDA POR REMITENTE ===");

  const nombres = ["Juan", "Maria", "Carlos", "Ana"];

  for (const nombre of nombres) {
    try {
      console.log(`\n🔍 Buscando remitente: "${nombre}"`);
      const response = await fetch(
        `/api/envios/buscar_por_remitente/?nombre=${encodeURIComponent(nombre)}`
      );

      if (response.ok) {
        const data = await response.json();
        console.log(
          `✅ Encontrados ${data.count} envío(s) para remitente "${nombre}"`
        );
        data.results.slice(0, 3).forEach((envio) => {
          console.log(
            `   📦 ${envio.numero_guia}: ${envio.remitente_nombre} → ${envio.destinatario_nombre} (${envio.estado_display})`
          );
        });
        if (data.count > 3) {
          console.log(`   ... y ${data.count - 3} más`);
        }
      } else {
        const error = await response.json();
        console.log(`❌ Error para "${nombre}":`, error.error);
      }
    } catch (error) {
      console.error(`💥 Error de red para "${nombre}":`, error);
    }
  }
}

// Test de búsqueda por destinatario
async function testBusquedaDestinatario() {
  console.log("\n📍 === PRUEBA BÚSQUEDA POR DESTINATARIO ===");

  const nombres = ["Maria", "Carmen", "Pedro", "Ana"];

  for (const nombre of nombres) {
    try {
      console.log(`\n🔍 Buscando destinatario: "${nombre}"`);
      const response = await fetch(
        `/api/envios/buscar_por_destinatario/?nombre=${encodeURIComponent(
          nombre
        )}`
      );

      if (response.ok) {
        const data = await response.json();
        console.log(
          `✅ Encontrados ${data.count} envío(s) para destinatario "${nombre}"`
        );
        data.results.slice(0, 3).forEach((envio) => {
          console.log(
            `   📦 ${envio.numero_guia}: ${envio.remitente_nombre} → ${envio.destinatario_nombre} (${envio.estado_display})`
          );
        });
        if (data.count > 3) {
          console.log(`   ... y ${data.count - 3} más`);
        }
      } else {
        const error = await response.json();
        console.log(`❌ Error para "${nombre}":`, error.error);
      }
    } catch (error) {
      console.error(`💥 Error de red para "${nombre}":`, error);
    }
  }
}

// Test de búsquedas sin resultados
async function testBusquedaSinResultados() {
  console.log("\n🔍 === PRUEBA BÚSQUEDAS SIN RESULTADOS ===");

  try {
    console.log("\n🔍 Buscando remitente inexistente...");
    const response1 = await fetch(
      "/api/envios/buscar_por_remitente/?nombre=NoExiste"
    );
    const data1 = await response1.json();
    console.log("📄 Respuesta remitente inexistente:", data1);

    console.log("\n🔍 Buscando destinatario inexistente...");
    const response2 = await fetch(
      "/api/envios/buscar_por_destinatario/?nombre=TampocoExiste"
    );
    const data2 = await response2.json();
    console.log("📄 Respuesta destinatario inexistente:", data2);
  } catch (error) {
    console.error("💥 Error en pruebas sin resultados:", error);
  }
}

// Ejecutar todas las pruebas
async function ejecutarTodasLasPruebas() {
  console.log("🎯 INICIANDO BATERÍA COMPLETA DE PRUEBAS\n");

  await testBusquedaRemitente();
  await testBusquedaDestinatario();
  await testBusquedaSinResultados();

  console.log("\n🎉 ¡TODAS LAS PRUEBAS COMPLETADAS!");
  console.log("\n📋 RESUMEN DE DATOS DISPONIBLES:");
  console.log("Remitentes: Juan, Maria, Carlos, Ana");
  console.log("Destinatarios: Maria, Carmen, Pedro, Ana");
  console.log("\n🌐 Ahora puedes probar en la interfaz web:");
  console.log("1. Ve a https://localhost:5173/rastreo");
  console.log('2. Selecciona "Nombre del Remitente" y busca "Juan"');
  console.log('3. Selecciona "Nombre del Destinatario" y busca "Maria"');
}

// Iniciar pruebas automáticamente
ejecutarTodasLasPruebas();
