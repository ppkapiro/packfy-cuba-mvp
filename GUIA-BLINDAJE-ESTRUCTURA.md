# 🛡️ GUÍA DE BLINDAJE DE ESTRUCTURA

## ¿Para qué sirve?

Este sistema protege la estructura de usuarios y autenticación durante el desarrollo de multitenancy. Si algo se daña durante las iteraciones, puedes restaurar rápidamente el estado estable.

## 📁 Archivos creados

- `blindar_estructura.py` - Script principal de blindaje
- `restaurar_estructura_YYYYMMDD_HHMMSS.py` - Script de restauración automática
- `backups_estructura/estructura_documentada_YYYYMMDD_HHMMSS.json` - Credenciales y documentación

## 🔄 Cómo usar

### Para crear respaldo:

```bash
python blindar_estructura.py
```

### Para restaurar estructura:

```bash
python restaurar_estructura_20250820_095645.py
```

## 👥 Usuarios blindados

| Rol                | Email                     | Password         | Acceso           |
| ------------------ | ------------------------- | ---------------- | ---------------- |
| **Superadmin**     | superadmin@packfy.com     | super123!        | Frontend + Admin |
| **Dueño**          | dueno@packfy.com          | dueno123!        | Frontend + Admin |
| **Operador Miami** | miami@packfy.com          | miami123!        | Frontend         |
| **Operador Cuba**  | cuba@packfy.com           | cuba123!         | Frontend         |
| **Remitentes**     | remitente[1-3]@packfy.com | remitente123!    | Frontend         |
| **Destinatarios**  | destinatario[1-3]@cuba.cu | destinatario123! | Frontend         |

## ✅ Estado verificado

- ✅ **API Authentication**: Todos los 10 usuarios pueden hacer login via API
- ✅ **Admin Panel**: superadmin y dueño pueden acceder al panel de administración
- ✅ **Perfiles**: Todos los usuarios tienen PerfilUsuario asociado a empresa "Packfy Express"
- ✅ **Permisos**: is_staff/is_superuser configurados correctamente

## 🚨 Cuándo usar la restauración

- Si se pierden usuarios durante migraciones
- Si se corrompen permisos de acceso
- Si falla la autenticación después de cambios
- Antes de iteraciones arriesgadas

## 🔧 Notas técnicas

- Los scripts son autocontenidos (configuran Django automáticamente)
- Compatible con estructura de multitenancy actual
- Preserva la empresa "Packfy Express" (slug: packfy-express)
- Credenciales consistentes para testing

---

**Última actualización**: 20 Agosto 2025 - v1.0
