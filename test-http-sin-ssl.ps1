# 🇨🇺 PACKFY CUBA - TEST HTTP SIN SSL PARA MÓVIL
# Confirmando hipótesis de problema SSL

Write-Host "🔧 === TEST HTTP SIN SSL - CONFIRMACIÓN HIPÓTESIS ===" -ForegroundColor Green
Write-Host ""

Write-Host "🎯 OBJETIVO: Confirmar si el problema es el certificado SSL" -ForegroundColor Yellow
Write-Host ""

# 1. Verificar que el backend HTTP esté funcionando
Write-Host "1. 🔍 VERIFICANDO BACKEND HTTP (Puerto 8000):" -ForegroundColor Yellow

try {
    $backendHTTP = curl -s -w "%{http_code}" "http://192.168.12.178:8000" 2>$null
    if ($backendHTTP -eq "200") {
        Write-Host "   ✅ Backend HTTP funcionando: Estado $backendHTTP" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Backend HTTP problema: Estado $backendHTTP" -ForegroundColor Red
    }
}
catch {
    Write-Host "   ❌ Error conectando a backend HTTP: $($_.Exception.Message)" -ForegroundColor Red
}

# 2. Crear configuración Vite temporal sin SSL
Write-Host ""
Write-Host "2. 🛠️ CREANDO CONFIGURACIÓN VITE SIN SSL:" -ForegroundColor Yellow

$viteConfigHTTP = @"
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 🚨 CONFIGURACIÓN TEMPORAL HTTP (SIN SSL) PARA TEST MÓVIL
export default defineConfig({
  plugins: [react()],
  base: "/",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5174, // Puerto diferente para evitar conflictos
    host: "0.0.0.0",
    // ❌ SIN HTTPS - Solo HTTP
    https: false,
    // Headers para móvil
    headers: {
      "Cache-Control": "no-cache, no-store, must-revalidate",
      "Pragma": "no-cache",
      "Expires": "0",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "*",
    },
    cors: true,
    strictPort: false,
    watch: {
      usePolling: false,
      interval: 5000,
      ignored: ["**/node_modules/**", "**/dist/**"],
    },
    hmr: {
      clientPort: 5174,
      host: "0.0.0.0",
      timeout: 30000,
      overlay: false,
    },
    proxy: {
      "/api": {
        target: "http://192.168.12.178:8000", // ❌ SIN HTTPS
        changeOrigin: true,
        secure: false, // Importante para HTTP
        timeout: 30000,
        headers: {
          "User-Agent": "Packfy-Test-HTTP/1.0",
        }
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
});
"@

$viteConfigHTTP | Out-File -FilePath "frontend/vite.config.http-test.ts" -Encoding UTF8
Write-Host "   ✅ Configuración HTTP creada: vite.config.http-test.ts" -ForegroundColor Green

# 3. Crear script de docker temporal sin SSL
Write-Host ""
Write-Host "3. 🐳 CREANDO DOCKER COMPOSE TEMPORAL HTTP:" -ForegroundColor Yellow

$dockerComposeHTTP = @"
# 🚨 DOCKER COMPOSE TEMPORAL - SOLO HTTP (SIN SSL)
version: '3.8'

services:
  frontend-http-test:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: packfy-frontend-http-test
    ports:
      - "5174:5174"
    environment:
      - NODE_ENV=development
      - VITE_API_URL=http://192.168.12.178:8000
      - VITE_APP_TITLE=Packfy Cuba HTTP Test
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --config vite.config.http-test.ts --port 5174 --host 0.0.0.0
    networks:
      - packfy-http-test
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5174"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend-http-test:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: packfy-backend-http-test
    ports:
      - "8001:8000"  # Solo HTTP, puerto diferente
    environment:
      - DEBUG=True
      - DJANGO_ALLOWED_HOSTS=192.168.12.178,localhost,127.0.0.1
      - DJANGO_CORS_ALLOWED_ORIGINS=http://192.168.12.178:5174,http://localhost:5174
      - USE_HTTPS=false  # ❌ SIN HTTPS
    volumes:
      - ./backend:/app
      - ./backend/media:/app/media
      - ./backend/static:/app/static
    networks:
      - packfy-http-test
    restart: unless-stopped
    depends_on:
      - db-http-test
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

  db-http-test:
    image: postgres:15
    container_name: packfy-db-http-test
    environment:
      - POSTGRES_DB=packfy_http_test
      - POSTGRES_USER=packfy
      - POSTGRES_PASSWORD=packfy123
    volumes:
      - packfy_http_test_data:/var/lib/postgresql/data
    networks:
      - packfy-http-test
    restart: unless-stopped

  redis-http-test:
    image: redis:7-alpine
    container_name: packfy-redis-http-test
    networks:
      - packfy-http-test
    restart: unless-stopped

volumes:
  packfy_http_test_data:

networks:
  packfy-http-test:
    driver: bridge
"@

$dockerComposeHTTP | Out-File -FilePath "docker-compose.http-test.yml" -Encoding UTF8
Write-Host "   ✅ Docker Compose HTTP creado: docker-compose.http-test.yml" -ForegroundColor Green

# 4. Crear página de test específica para móvil HTTP
Write-Host ""
Write-Host "4. 📱 CREANDO PÁGINA DE TEST HTTP PARA MÓVIL:" -ForegroundColor Yellow

$testPageHTTP = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇨🇺 Packfy Cuba - Test HTTP Móvil</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: linear-gradient(135deg, #001122 0%, #003366 100%);
            color: white;
            text-align: center;
            min-height: 100vh;
            margin: 0;
        }
        .container { max-width: 600px; margin: 0 auto; }
        .success { color: #00ff00; font-size: 28px; margin: 20px 0; }
        .warning { color: #ff6600; font-size: 20px; margin: 15px 0; }
        .button {
            display: inline-block;
            padding: 15px 30px;
            margin: 15px;
            background: linear-gradient(135deg, #0066cc, #3385d6);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 18px;
            border: 2px solid #0066cc;
            transition: all 0.3s ease;
        }
        .button:hover {
            background: linear-gradient(135deg, #3385d6, #0066cc);
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,102,204,0.3);
        }
        .info {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #00ff00;
        }
        .test-result {
            background: rgba(0,255,0,0.1);
            border: 2px solid #00ff00;
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
        }
        .protocol { font-size: 24px; color: #ff6600; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🇨🇺 Packfy Cuba</h1>
        <div class="protocol">📡 PROTOCOLO: HTTP (Sin SSL)</div>
        <div class="success">✅ Test HTTP Móvil</div>

        <div class="warning">
            🚨 IMPORTANTE: Esta es una prueba temporal sin HTTPS
        </div>

        <div class="info">
            <h3>📱 Información del Dispositivo:</h3>
            <p><strong>User-Agent:</strong> <span id="device-info"></span></p>
            <p><strong>Pantalla:</strong> <span id="screen-info"></span></p>
            <p><strong>Hora:</strong> <span id="time-info"></span></p>
            <p><strong>URL:</strong> <span id="url-info"></span></p>
        </div>

        <div class="info">
            <h3>🌐 Configuración de Conexión:</h3>
            <p><strong>Servidor:</strong> 192.168.12.178:5174</p>
            <p><strong>Protocolo:</strong> HTTP (Puerto 5174)</p>
            <p><strong>Backend:</strong> http://192.168.12.178:8001</p>
            <p><strong>SSL:</strong> ❌ DESHABILITADO</p>
        </div>

        <div class="test-result">
            <h3>🧪 RESULTADO DEL TEST:</h3>
            <p>Si puedes ver esta página, significa que:</p>
            <p>✅ La conexión HTTP funciona correctamente</p>
            <p>✅ El problema era el certificado SSL</p>
            <p>✅ Tu móvil puede conectarse sin HTTPS</p>
        </div>

        <a href="javascript:testAPI()" class="button">
            🔧 Test API Backend
        </a>

        <a href="javascript:testLogin()" class="button">
            🔑 Test Login HTTP
        </a>

        <div id="api-result" style="margin-top: 20px;"></div>

        <div style="margin-top: 40px; font-size: 14px; color: #999;">
            <p>💡 Este test confirma si el problema HTTP 500 era causado por SSL</p>
            <p>🔒 En producción se usará un certificado SSL válido</p>
        </div>
    </div>

    <script>
        // Mostrar información del dispositivo
        document.getElementById('device-info').textContent = navigator.userAgent;
        document.getElementById('screen-info').textContent = screen.width + 'x' + screen.height;
        document.getElementById('time-info').textContent = new Date().toLocaleString();
        document.getElementById('url-info').textContent = window.location.href;

        // Log inicial
        console.log('🇨🇺 Test HTTP móvil cargado exitosamente');
        console.log('🌐 Protocolo:', window.location.protocol);
        console.log('📱 Dispositivo:', navigator.userAgent);

        // Test API Backend
        async function testAPI() {
            const resultDiv = document.getElementById('api-result');
            resultDiv.innerHTML = '<p>🔄 Probando conexión con API...</p>';

            try {
                const response = await fetch('/api/health/', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (response.ok) {
                    resultDiv.innerHTML = '<div style="color: #00ff00;">✅ API Backend responde correctamente (HTTP ' + response.status + ')</div>';
                } else {
                    resultDiv.innerHTML = '<div style="color: #ff6600;">⚠️ API responde con estado: HTTP ' + response.status + '</div>';
                }
            } catch (error) {
                resultDiv.innerHTML = '<div style="color: #ff0000;">❌ Error conectando a API: ' + error.message + '</div>';
            }
        }

        // Test Login HTTP
        async function testLogin() {
            const resultDiv = document.getElementById('api-result');
            resultDiv.innerHTML = '<p>🔑 Probando endpoint de login...</p>';

            try {
                const response = await fetch('/api/auth/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: 'test',
                        password: 'test'
                    })
                });

                const status = response.status;
                if (status === 401 || status === 400) {
                    resultDiv.innerHTML = '<div style="color: #00ff00;">✅ Endpoint de login accesible (HTTP ' + status + ' - credenciales incorrectas es normal)</div>';
                } else if (status === 500) {
                    resultDiv.innerHTML = '<div style="color: #ff0000;">❌ HTTP 500 detectado - El problema persiste sin SSL</div>';
                } else {
                    resultDiv.innerHTML = '<div style="color: #ff6600;">⚠️ Respuesta inesperada: HTTP ' + status + '</div>';
                }
            } catch (error) {
                resultDiv.innerHTML = '<div style="color: #ff0000;">❌ Error en test login: ' + error.message + '</div>';
            }
        }
    </script>
</body>
</html>
"@

$testPageHTTP | Out-File -FilePath "frontend/public/test-http-movil.html" -Encoding UTF8
Write-Host "   ✅ Página de test HTTP creada: test-http-movil.html" -ForegroundColor Green

# 5. Iniciar el test HTTP
Write-Host ""
Write-Host "5. 🚀 INICIANDO TEST HTTP SIN SSL:" -ForegroundColor Yellow

Write-Host "   🔄 Construyendo contenedores HTTP..." -ForegroundColor White
docker-compose -f docker-compose.http-test.yml build --no-cache

Write-Host "   🚀 Iniciando servicios HTTP..." -ForegroundColor White
docker-compose -f docker-compose.http-test.yml up -d

# 6. Verificar que los servicios estén funcionando
Write-Host ""
Write-Host "6. ✅ VERIFICANDO SERVICIOS HTTP:" -ForegroundColor Yellow

Start-Sleep 10

try {
    $frontendTest = curl -s -w "%{http_code}" "http://192.168.12.178:5174" 2>$null
    if ($frontendTest -eq "200") {
        Write-Host "   ✅ Frontend HTTP: Puerto 5174 funcionando" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Frontend HTTP: Estado $frontendTest" -ForegroundColor Red
    }
}
catch {
    Write-Host "   ❌ Error verificando frontend HTTP" -ForegroundColor Red
}

try {
    $backendTest = curl -s -w "%{http_code}" "http://192.168.12.178:8001" 2>$null
    if ($backendTest -eq "200") {
        Write-Host "   ✅ Backend HTTP: Puerto 8001 funcionando" -ForegroundColor Green
    }
    else {
        Write-Host "   ❌ Backend HTTP: Estado $backendTest" -ForegroundColor Red
    }
}
catch {
    Write-Host "   ❌ Error verificando backend HTTP" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 === INSTRUCCIONES PARA TEST MÓVIL ===" -ForegroundColor Red
Write-Host ""

Write-Host "📱 ABRE EN TU MÓVIL (SIN HTTPS):" -ForegroundColor Green
Write-Host "http://192.168.12.178:5174/test-http-movil.html" -ForegroundColor White
Write-Host ""

Write-Host "🧪 PASOS DEL TEST:" -ForegroundColor Yellow
Write-Host "1. ✅ Si la página carga → Problema era SSL" -ForegroundColor White
Write-Host "2. 🔧 Toca 'Test API Backend' → Verifica conectividad" -ForegroundColor White
Write-Host "3. 🔑 Toca 'Test Login HTTP' → Verifica autenticación" -ForegroundColor White
Write-Host "4. 📊 Reporta todos los resultados" -ForegroundColor White
Write-Host ""

Write-Host "🎯 RESULTADO ESPERADO:" -ForegroundColor Cyan
Write-Host "• Si funciona HTTP pero no HTTPS → Problema SSL confirmado" -ForegroundColor White
Write-Host "• Si falla igual → Problema más profundo" -ForegroundColor White
Write-Host ""

Write-Host "🔄 PARA DETENER EL TEST:" -ForegroundColor Yellow
Write-Host "docker-compose -f docker-compose.http-test.yml down" -ForegroundColor White
Write-Host ""
