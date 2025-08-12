# 🇨🇺 PACKFY CUBA - GUÍA DE TESTING COMPLETA

## ✅ ESTADO ACTUAL DEL SISTEMA

### 🔧 Infraestructura

- **Frontend**: https://localhost:5173 ✅ Funcionando
- **Backend**: http://localhost:8000 ✅ Funcionando
- **Base de Datos**: PostgreSQL en puerto 5433 ✅ Funcionando
- **Proxy**: Vite proxy redirige /api → backend ✅ Configurado

### 📦 Datos de Prueba Disponibles

- **TEST001**: EN_TRANSITO (Juan Pérez → María García)
- **TEST002**: ENTREGADO (Ana López → Carlos Ruiz)
- **CU001**: RECIBIDO (José García → María López)
- **CU002**: EN_TRANSITO (Ana García → Carlos Pérez)

---

## 🧪 PRUEBAS MANUALES

### 1. Prueba de API Directa (Terminal)

```bash
# Probar backend directo
curl "http://localhost:8000/api/envios/rastrear/?numero_guia=TEST001"

# Probar a través del proxy frontend
curl -k "https://localhost:5173/api/envios/rastrear/?numero_guia=TEST001"
```

### 2. Prueba en Navegador (Consola F12)

```javascript
// Copiar y pegar en la consola del navegador en https://localhost:5173
fetch("/api/envios/rastrear/?numero_guia=TEST001")
  .then((response) => response.json())
  .then((data) => console.log("✅ Respuesta:", data))
  .catch((error) => console.error("❌ Error:", error));
```

### 3. Prueba de Interfaz de Usuario

1. Ir a: https://localhost:5173/rastreo
2. Seleccionar "Número de Guía"
3. Escribir: TEST001
4. Hacer clic en "Buscar Envíos"
5. Verificar en F12 → Console los logs detallados

---

## 🔍 COMPONENTES ACTUALIZADOS

### TrackingPageFixed.tsx

- ✅ Logging detallado en consola
- ✅ Mapeo correcto de respuesta del backend
- ✅ Manejo de errores mejorado
- ✅ Panel de debug en la interfaz
- ✅ Tipado TypeScript correcto

### API Service (api.ts)

- ✅ Configuración automática de baseURL
- ✅ Método trackPublic para rastreo público
- ✅ Proxy configuration funcionando

### Backend (envios/views.py)

- ✅ Endpoint público /api/envios/rastrear/
- ✅ Rate limiting implementado
- ✅ Respuesta JSON estructurada

---

## 🐛 DEBUGGING

### Si el rastreo no funciona:

1. **Verificar logs del frontend:**

```bash
docker logs packfy-frontend --tail 20
```

2. **Verificar logs del backend:**

```bash
docker logs packfy-backend --tail 20
```

3. **Abrir F12 → Console en el navegador y revisar:**

   - Logs de TrackingPageFixed
   - Errores de red
   - Respuestas de API

4. **Probar scripts de debug:**
   - `test-api-browser.js`
   - `test-tracking-direct.js`

### Errores Comunes y Soluciones:

- **"No se puede conectar"** → Verificar que los contenedores estén running
- **404 Not Found** → Verificar URL del endpoint en el backend
- **CORS errors** → Verificar configuración del proxy en vite.config.ts
- **Blank page** → Verificar que React esté cargando correctamente

---

## 🚀 NEXT STEPS

1. **Test completo de la búsqueda por guía**
2. **Implementar búsqueda por remitente/destinatario**
3. **Agregar más datos de prueba**
4. **Optimizar la interfaz de usuario**

---

## 📞 SOPORTE

Si encuentras problemas:

1. Revisar logs en Docker
2. Verificar console del navegador (F12)
3. Probar scripts de debug incluidos
4. Verificar que todos los contenedores estén healthy

**Comando rápido de health check:**

```bash
docker ps
curl -k https://localhost:5173
curl http://localhost:8000/api/
```

---

**Última actualización:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Estado del sistema:** ✅ FUNCIONAL - Listo para testing
