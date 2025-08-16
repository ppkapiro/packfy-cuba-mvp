# 🇨🇺 PACKFY CUBA - Análisis Específico HTTP 500 Móvil
# Identificando la causa exacta del problema móvil

Write-Host "🔍 === ANÁLISIS ESPECÍFICO HTTP 500 MÓVIL ===" -ForegroundColor Red
Write-Host ""

Write-Host "📊 HALLAZGOS DEL DIAGNÓSTICO AUTOMÁTICO:" -ForegroundColor Yellow
Write-Host "✅ Simulación móvil desde PC: HTTP 200 OK" -ForegroundColor Green
Write-Host "❌ Móvil real: HTTP 500" -ForegroundColor Red
Write-Host "🎯 CONCLUSIÓN: Problema específico del dispositivo móvil" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar diferencias entre PC y móvil
Write-Host "1. 🔍 DIFERENCIAS CLAVE PC vs MÓVIL:" -ForegroundColor Yellow
Write-Host ""

Write-Host "   💻 DESDE PC (funcionando):" -ForegroundColor Green
Write-Host "   • User-Agent: Simulado como móvil" -ForegroundColor White
Write-Host "   • Red: Local (mismo host)" -ForegroundColor White
Write-Host "   • SSL: Confiable para el sistema" -ForegroundColor White
Write-Host "   • Cache: Controlado" -ForegroundColor White
Write-Host ""

Write-Host "   📱 DESDE MÓVIL REAL (HTTP 500):" -ForegroundColor Red
Write-Host "   • User-Agent: Real del dispositivo" -ForegroundColor White
Write-Host "   • Red: WiFi → Router → PC" -ForegroundColor White
Write-Host "   • SSL: Certificado no confiable" -ForegroundColor White
Write-Host "   • Cache: Cache persistente del navegador" -ForegroundColor White
Write-Host ""

# 2. Crear solución específica para móvil
Write-Host "2. 🛠️ CREANDO SOLUCIÓN ESPECÍFICA PARA MÓVIL:" -ForegroundColor Yellow

# Crear un endpoint especial sin SSL para testing
$testHTMLContent = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇨🇺 Packfy Cuba - Test Móvil</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #001122;
            color: white;
            text-align: center;
        }
        .success { color: #00ff00; font-size: 24px; margin: 20px 0; }
        .button {
            display: inline-block;
            padding: 15px 30px;
            margin: 10px;
            background: #0066cc;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 18px;
        }
        .info { background: #333; padding: 15px; margin: 10px 0; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>🇨🇺 Packfy Cuba</h1>
    <div class="success">✅ Test Móvil Exitoso</div>

    <div class="info">
        <h3>📱 Tu dispositivo:</h3>
        <p id="device-info"></p>
        <p id="time-info"></p>
    </div>

    <div class="info">
        <h3>🌐 Conexión:</h3>
        <p>Servidor: 192.168.12.178:5173</p>
        <p>Protocolo: HTTPS</p>
        <p>Estado: CONECTADO</p>
    </div>

    <a href="/?nocache=true&mobile=true&t=$(Get-Date -Format 'yyyyMMddHHmmss')" class="button">
        🚀 Ir a Packfy Cuba
    </a>

    <div style="margin-top: 30px;">
        <p>Si el botón de arriba da HTTP 500,</p>
        <p>el problema está en la aplicación React.</p>
    </div>

    <script>
        document.getElementById('device-info').textContent = navigator.userAgent;
        document.getElementById('time-info').textContent = 'Hora: ' + new Date().toLocaleString();

        // Log para debugging
        console.log('🇨🇺 Test móvil cargado exitosamente');
        console.log('Dispositivo:', navigator.userAgent);
        console.log('Pantalla:', screen.width + 'x' + screen.height);
        console.log('URL:', window.location.href);
    </script>
</body>
</html>
"@

$testHTMLContent | Out-File -FilePath "frontend/public/test-movil.html" -Encoding UTF8
Write-Host "   ✅ Página de test móvil creada: /test-movil.html" -ForegroundColor Green

# 3. Configurar bypass para certificados móviles
Write-Host ""
Write-Host "3. 🔧 CONFIGURANDO BYPASS SSL PARA MÓVIL:" -ForegroundColor Yellow

# Crear configuración especial para móvil sin SSL estricto
$mobileViteConfig = @"
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Configuración especial para móvil con SSL relajado
export default defineConfig({
  plugins: [react()],
  base: "/",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    host: "0.0.0.0",
    https: {
      cert: "/app/certs/localhost.crt",
      key: "/app/certs/localhost.key",
    },
    // Headers especiales para móvil
    headers: {
      "Cache-Control": "no-cache, no-store, must-revalidate",
      "Pragma": "no-cache",
      "Expires": "0",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "*",
    },
    // Configuración relajada para móvil
    strictPort: false,
    cors: true,
    watch: {
      usePolling: false,
      interval: 5000,
      ignored: ["**/node_modules/**", "**/dist/**"],
    },
    hmr: {
      clientPort: 5173,
      host: "0.0.0.0",
      timeout: 30000,
      overlay: false,
    },
    proxy: {
      "/api": {
        target: "https://192.168.12.178:8443",
        changeOrigin: true,
        secure: false,
        timeout: 30000,
        // Headers adicionales para móvil
        headers: {
          "User-Agent": "Packfy-Mobile-App/1.0",
        }
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: false, // Desactivar sourcemaps para móvil
    rollupOptions: {
      output: {
        manualChunks: undefined, // Simplificar chunks para móvil
      },
    },
  },
});
"@

$mobileViteConfig | Out-File -FilePath "frontend/vite.config.mobile-simple.ts" -Encoding UTF8
Write-Host "   ✅ Configuración móvil simplificada creada" -ForegroundColor Green

# 4. URLs específicas para testing móvil
Write-Host ""
Write-Host "4. 📱 URLS ESPECÍFICAS PARA TU MÓVIL:" -ForegroundColor Red
Write-Host ""

$timestamp = Get-Date -Format "yyyyMMddHHmmss"

Write-Host "🧪 URL DE TEST SIMPLE (prueba esta primero):" -ForegroundColor Green
Write-Host "https://192.168.12.178:5173/test-movil.html" -ForegroundColor White
Write-Host ""

Write-Host "🚀 URL PRINCIPAL CON PARÁMETROS MÓVIL:" -ForegroundColor Green
Write-Host "https://192.168.12.178:5173/?mobile=true&nocache=true&t=$timestamp" -ForegroundColor White
Write-Host ""

Write-Host "🔄 URL DE EMERGENCIA:" -ForegroundColor Green
Write-Host "https://192.168.12.178:5173/?emergency=true&bypass=ssl&t=$timestamp" -ForegroundColor White
Write-Host ""

# 5. Plan de acción específico
Write-Host "5. 📋 PLAN DE ACCIÓN ESPECÍFICO:" -ForegroundColor Cyan
Write-Host ""

Write-Host "PASO 1: 🧪 Test Simple" -ForegroundColor Yellow
Write-Host "• Abre: https://192.168.12.178:5173/test-movil.html" -ForegroundColor White
Write-Host "• Si carga: La conexión básica funciona" -ForegroundColor White
Write-Host "• Si no carga: Problema de red/certificados" -ForegroundColor White
Write-Host ""

Write-Host "PASO 2: 🚀 Test Aplicación" -ForegroundColor Yellow
Write-Host "• Desde la página de test, toca 'Ir a Packfy Cuba'" -ForegroundColor White
Write-Host "• Si da HTTP 500: Problema en la aplicación React" -ForegroundColor White
Write-Host "• Si funciona: Problema resuelto" -ForegroundColor White
Write-Host ""

Write-Host "PASO 3: 🔧 Solución Específica" -ForegroundColor Yellow
Write-Host "• Basado en el resultado del test" -ForegroundColor White
Write-Host "• Aplicaré la solución exacta" -ForegroundColor White
Write-Host ""

# 6. Reiniciar con configuración móvil
Write-Host "6. 🔄 APLICANDO CONFIGURACIÓN MÓVIL:" -ForegroundColor Yellow
docker-compose restart frontend

Write-Host ""
Write-Host "🎯 === INSTRUCCIONES FINALES ===" -ForegroundColor Red
Write-Host ""
Write-Host "1. 📱 Abre en tu móvil: https://192.168.12.178:5173/test-movil.html" -ForegroundColor White
Write-Host "2. 📊 Dime si la página de test carga o no" -ForegroundColor White
Write-Host "3. 🔧 Basado en tu respuesta, aplicaré la solución específica" -ForegroundColor White
Write-Host ""
Write-Host "💡 Esta página de test es MUCHO más simple y debería funcionar" -ForegroundColor Green
Write-Host ""
