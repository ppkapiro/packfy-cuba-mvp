# Changelog


## [Multi-Tenant v1.0] - 2025-08-20

### ✅ Implementado
- **Sistema Multi-Tenant Completo**
  - Backend con middleware de tenant context
  - Frontend con TenantContext y TenantSelector
  - Aislamiento de datos por empresa
  - Integración AuthContext → TenantContext

- **Seguridad Multi-Tenant**
  - Headers X-Tenant-Slug requeridos
  - Filtrado automático en queryset
  - Permisos por rol y empresa

- **UX Mejorada**
  - Selector de empresa en header
  - Cambio dinámico entre empresas
  - Estado persistente en localStorage

### 🔧 Técnico
- Middleware: `middleware/tenant_middleware.py`
- Context: `middleware/tenant_context.py`
- Frontend: `contexts/TenantContext.tsx`
- Component: `components/TenantSelector/`

### 🐛 Corregido
- Cache de Docker resuelto con rebuild
- Sincronización AuthContext → TenantContext
- Headers automáticos en requests API
- Errores 403 por falta de tenant slug

### 📋 Testing
- Credenciales: admin@packfy.com / admin123
- Empresa: Miami Shipping Co (miami-shipping-2)
- Logs: TenantContext en consola Chrome


Todos los cambios notables del proyecto.
