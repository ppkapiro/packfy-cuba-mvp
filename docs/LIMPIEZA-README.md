# 🧹 ORGANIZACIÓN POST-LIMPIEZA

## 📁 Estructura Reorganizada

### `/docs/`

- **`historiales/`**: Documentación histórica de desarrollo y cambios
- Contiene todos los archivos `.md` de procesos de desarrollo

### `/scripts-dev/`

- **Scripts de desarrollo y diagnóstico**
- **`powershell/`**: Scripts PowerShell de desarrollo y testing

### Root limpio

- Solo archivos esenciales de configuración y scripts de producción
- `README.md`, `CHANGELOG.md`, `STATUS.md`, `TROUBLESHOOTING.md`
- Scripts principales de gestión del proyecto

## 🎯 Criterios de Limpieza Aplicados

✅ **MANTENIDOS EN ROOT:**

- Scripts de configuración principal
- Documentación esencial
- Scripts de gestión de producción

📁 **ORGANIZADOS EN `/scripts-dev/`:**

- Scripts de diagnóstico (`diagnostico_*.py`)
- Scripts de análisis (`analisis_*.py`)
- Scripts de verificación (`verificar_*.py`)
- Scripts de creación de datos de prueba
- Scripts de reset y limpieza temporal

📚 **ARCHIVADOS EN `/docs/`:**

- Historiales de desarrollo
- Documentación de procesos
- Reportes de cambios y mejoras

## 🔄 Mantenimiento

Para futuras limpiezas, usar el mismo criterio:

- Root solo para producción
- `/scripts-dev/` para desarrollo
- `/docs/` para documentación
