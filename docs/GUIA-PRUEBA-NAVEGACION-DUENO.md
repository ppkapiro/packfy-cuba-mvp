# 🔍 GUÍA DE PRUEBA - NAVEGACIÓN DUEÑO

**Estado:** Implementación completada, en fase de testing
**Fecha:** 2025-01-20
**Servidor:** http://localhost:5175 (con debug)

---

## 🎯 CREDENCIALES DE PRUEBA

### Usuario Dueño:

- **Email:** dueno@packfy.com
- **Password:** dueno123!
- **Rol:** dueno
- **Empresa:** Debería tener una empresa asignada

---

## 📋 PASOS PARA PROBAR

### 1. Abrir la Aplicación

- URL: http://localhost:5175/login
- Usar las credenciales del usuario dueño

### 2. Verificar Debug Info

En la esquina superior derecha debe aparecer un panel negro con:

- ✅ Información del usuario
- ✅ Información de la empresa
- ✅ **Rol: dueno** (esto es crucial)
- ✅ Navegación: AdminNavigation

### 3. Buscar la Navegación de Dueño

Después del login, debe aparecer una barra de navegación con:

- 📊 **Dashboard** (enlace a /admin/dashboard)
- 👥 **Gestión de Usuarios** (dropdown)
- 📈 **Reportes** (dropdown)
- ⚙️ **Configuración**
- 🔗 **Admin Django**

### 4. Probar Dashboard Administrativo

- Navegar a: http://localhost:5175/admin/dashboard
- Debe mostrar métricas ejecutivas
- Cards con información de envíos, usuarios, finanzas

---

## 🐛 DEBUGGING

### Si NO aparece la navegación de dueño:

#### 1. Verificar Debug Info

- ¿Aparece el panel de debug en la esquina?
- ¿El rol muestra "dueno"?
- ¿Hay información de empresa?

#### 2. Verificar Consola del Navegador (F12)

Buscar mensajes que empiecen con "Layout:":

```
Layout: Renderizando Layout, usuario: {objeto}
Layout: empresaActual: {objeto}
Layout: perfilActual: {objeto}
Layout: rol actual: dueno
Layout: ¿Es dueño? true
Layout: Renderizando AdminNavigation para dueño
```

#### 3. Verificar Red (F12 > Network)

- ¿Se cargan los archivos CSS de navegación?
- ¿Hay errores 404 en archivos de navegación?

### Si el debug info muestra rol incorrecto:

#### 1. Verificar Base de Datos

```python
# En Django shell
from usuarios.models import PerfilUsuario
perfil = PerfilUsuario.objects.get(usuario__email='dueno@packfy.com')
print(f"Rol: {perfil.rol}")
print(f"Empresa: {perfil.empresa}")
```

#### 2. Verificar API Response

En Network tab, buscar llamadas a:

- `/api/auth/me/`
- `/api/tenant/profile/`

---

## 🔧 TROUBLESHOOTING

### Problema: "No se ve navegación diferente"

**Solución:**

1. Hard refresh (Ctrl+Shift+R)
2. Verificar que el servidor esté en puerto 5175
3. Limpiar localStorage y cookies

### Problema: "Usuario no tiene rol dueño"

**Solución:**

1. Verificar en Django admin: http://localhost:8000/admin/
2. Buscar usuario dueno@packfy.com
3. Verificar que tenga PerfilUsuario con rol='dueno'

### Problema: "Errores en consola"

**Solución:**

1. Verificar que todos los archivos de navegación existan
2. Verificar imports en Layout.tsx
3. Verificar que no haya errores de TypeScript

---

## 📁 ARCHIVOS RELEVANTES

### Frontend:

```
src/components/
├── Layout.tsx                     (navegación contextual)
├── NavigationDebugInfo.tsx        (debug panel)
└── navigation/
    ├── AdminNavigation.tsx        (navegación dueño)
    ├── StandardNavigation.tsx     (navegación normal)
    └── index.ts                   (exports)

src/pages/
└── AdminDashboard.tsx             (dashboard ejecutivo)

src/styles/
├── admin-navigation.css           (estilos navegación)
├── admin-dashboard.css            (estilos dashboard)
└── unified-system.css             (navegación base)
```

### Backend:

```
usuarios/models.py                 (PerfilUsuario)
usuarios/views.py                  (API endpoints)
```

---

## ✅ CHECKLIST DE VERIFICACIÓN

- [ ] Servidor frontend en puerto 5175
- [ ] Servidor backend en puerto 8000
- [ ] Usuario dueno@packfy.com existe
- [ ] Usuario tiene rol 'dueno' en PerfilUsuario
- [ ] Usuario tiene empresa asignada
- [ ] Debug panel aparece en esquina superior derecha
- [ ] Debug panel muestra rol 'dueno'
- [ ] Navegación muestra enlaces administrativos
- [ ] /admin/dashboard carga correctamente
- [ ] Dashboard muestra métricas

---

## 🎯 RESULTADO ESPERADO

Cuando todo funcione correctamente:

1. **Login exitoso** con dueno@packfy.com
2. **Debug panel** muestra información completa
3. **Navegación administrativa** visible en header
4. **Dashboard ejecutivo** accesible y funcional
5. **Métricas** se cargan desde la API

---

_🇨🇺 Packfy Cuba v3.0 - Sistema Unificado_
_Navegación Inteligente Basada en Roles_
