# 📱 GUIA TESTING MÓVIL - PACKFY PWA

## 🔧 PROBLEMAS SOLUCIONADOS

### ✅ 1. Loop de Instalación
- **Detección mejorada** de app instalada (5 métodos)
- **Parámetro `homescreen=1`** en start_url del manifest
- **Logs de debugging** en consola para diagnosticar

### ✅ 2. Credenciales Móvil
- **Inputs optimizados** para móvil (font-size: 16px evita zoom iOS)
- **Touch targets** mínimo 44px
- **Estilos standalone** mode específicos
- **Z-index** management mejorado

### ✅ 3. Indicadores Visuales
- **Indicador "📱 App"** en header cuando está instalada
- **Status banner** mejorado para apps instaladas
- **PWAStatusIndicator** component en Layout

## 📱 CREDENCIALES DE TESTING

### Para testing rápido:
```
Email: admin@packfy.test
Password: admin123
```

### Credenciales alternativas:
```
Email: test@test.com  
Password: 123456
```

## 🧪 PROTOCOLO DE TESTING

### PASO 1: Testing en Navegador Móvil
1. **Abrir**: http://192.168.12.179:5173
2. **Login** con credenciales de testing
3. **Verificar** que no aparece prompt instalación si ya está instalada
4. **Comprobar** que inputs funcionan correctamente

### PASO 2: Instalación PWA
1. **Android Chrome**: Menú → "Agregar a pantalla de inicio"
2. **iOS Safari**: Compartir → "Agregar a pantalla de inicio"
3. **Verificar** que aparece icono en homescreen

### PASO 3: Testing App Instalada
1. **Abrir app** desde homescreen
2. **Verificar indicador** "📱 App" en header
3. **Login** - debería funcionar sin problemas
4. **No debería** aparecer prompt de instalación

### PASO 4: Testing Offline
1. **Desactivar WiFi/datos**
2. **Abrir app** instalada
3. **Verificar** página offline personalizada
4. **Reactivar conexión** y verificar funcionamiento

## 🐛 DEBUGGING

### Abrir DevTools Móvil:
1. **Android**: Chrome → Menú → "Más herramientas" → "Herramientas para desarrolladores"
2. **iOS**: Safari → Desarrollar → [Dispositivo]

### Logs a buscar:
```
🔍 PWA Detection: {isStandalone, isIOSStandalone, ...}
✅ PWA: Detectada como instalada
🚫 PWA: Ya instalada, omitiendo prompt
📱 PWA: Prompt de instalación disponible
🎉 PWA: Ejecutándose en modo standalone
```

## 🔄 SI PERSISTEN PROBLEMAS

### Reset Completo:
1. **Desinstalar** app del dispositivo
2. **Limpiar caché** del navegador
3. **Recargar** http://192.168.12.179:5173
4. **Reinstalar** app

### Verificar Service Worker:
1. DevTools → Application → Service Workers
2. Verificar que está "Activated and is running"
3. Si hay problemas: "Unregister" y recargar

---

## 📞 TESTING INMEDIATO REQUERIDO

**URL**: http://192.168.12.179:5173  
**Credenciales**: admin@packfy.test / admin123

¿Puedes probar ahora y reportar si:
1. Los inputs permiten escribir credenciales?
2. Aparece el indicador "📱 App" cuando está instalada?
3. Se evita el loop de instalación?
