# 📘 Plan Maestro de Actualización y Evolución – Packfy Cuba (v4.x → v5.x)

> Documento vivo. Actualízalo con cada cambio relevante. Usa Pull Requests para modificar y mantener historial.

---

## 🧭 Meta General

Construir una plataforma de gestión de envíos sólida, segura, escalable y optimizada para experiencia móvil, con ciclos de entrega predecibles y métricas claras de calidad.

---

## 📌 Estado actual (2025-08-15)

- Fase 1 – Hardening: Completada.
- Fase 2 – Seguridad y Observabilidad: Completada (JWT blacklist, RequestID, /metrics, logging JSON, rate limit base, cabeceras seguridad).
- Fase 3 – Performance y UX: En progreso (backend listo: cache rastreo, estadísticas matview+fallback+cache, paginación segura; pendiente ajustes frontend).
- Fase 4 – Asíncrono/Escalabilidad: Pendiente (iniciar Celery para notificaciones/correos).
- Fase 5 – Calidad Continua: En progreso (workflow CI multi-OS, lint Ruff, cobertura XML/HTML; cobertura actual ~33% → objetivo 40%/55%/70%).
- Fase 6 – Optimización Avanzada: Pendiente.

KPIs: CI verde; cobertura ~33%; endpoints críticos con cache y métricas operativas.

---

## 🏁 Objetivos Estratégicos

| Nº  | Objetivo                                        | Indicador de Éxito                      | Horizonte      |
| --- | ----------------------------------------------- | --------------------------------------- | -------------- |
| 1   | Endurecer seguridad (auth, CORS, secretos)      | 0 findings críticos en escaneo básico   | Corto (Fase 1) |
| 2   | Mejorar confiabilidad identificadores de envíos | 0 colisiones / 0 condiciones de carrera | Corto          |
| 3   | Reducir latencia endpoints clave                | P95 < 250ms (envío rastreo)             | Medio          |
| 4   | Implementar monitoreo + métricas                | Dashboard básico (errores, throughput)  | Medio          |
| 5   | Aumentar cobertura de pruebas                   | Cobertura backend ≥ 70%                 | Medio          |
| 6   | Preparar escalado horizontal                    | Stateless + caché controlada            | Largo          |
| 7   | UX móvil consistente y ligera                   | Lighthouse Perf ≥ 85 móvil              | Medio          |
| 8   | Automatizar pipeline CI/CD                      | Pipeline completo verde                 | Largo          |

---

## 🗂 Alcance del Plan

Incluye: backend (Django REST), frontend (React/Vite), infraestructura (Docker, Redis, PostgreSQL), seguridad, rendimiento, DX, monitoreo y gobernanza técnica.

Excluye (por ahora): facturación, pasarelas de pago, multi‑idioma completo, internacionalización de formatos avanzados, integraciones externas de terceros.

---

## 🛠 Fases Principales (Roadmap Iterativo)

### Fase 1 – Hardening Inicial (Semana 1)

- Extraer secretos a entorno (.env / variables) y eliminar `SECRET_KEY` hardcodeado.
- Corregir duplicidad `BLACKLIST_AFTER_ROTATION` en SIMPLE_JWT.
- Implementar generación robusta de `numero_guia` (Secuencia PostgreSQL o UUID + formato PKF).
- Limitar CORS (lista blanca en settings_prod; toggle claro en dev).
- Ajustar API client para priorizar `VITE_API_BASE_URL` y fallback.
- Índices DB: `(estado_actual, fecha_creacion)`, trigram opcional nombres si frecuencia de búsqueda lo amerita.
- Añadir script migración + test mínimo de concurrencia.

### Fase 2 – Seguridad y Observabilidad (Semanas 2–3)

- Activar `rest_framework_simplejwt.token_blacklist` + flujo logout real.
- Rate limiting con Redis (endpoints públicos: rastrear, búsquedas). DRF throttles + middleware unificado.
- Endpoint `/health` y `/metrics` (Prometheus client).
- Logging estructurado JSON (user_id, request_id, latency, path).
- Cabeceras avanzadas: HSTS, COOP, CORP, CSP con nonces.

#### Detalle Fase 2 (Tracking Inicial)

| Nº  | Tarea                          | Estado | Notas                              |
| --- | ------------------------------ | ------ | ---------------------------------- |
| 2.1 | Activar token blacklist JWT    | Done   | App añadida a INSTALLED_APPS       |
| 2.2 | Middleware request_id          | Done   | `RequestIDMiddleware` implementado |
| 2.3 | Endpoint /metrics placeholder  | Done   | Devuelve 501 hasta instrumentación |
| 2.4 | Diseño estructura logging JSON | Done   | Formatter JSON + handlers en prod  |
| 2.5 | Rate limiting (borrador)       | Done   | Middleware + fallback memoria      |
| 2.6 | Cabeceras seguridad avanzadas  | Done   | HSTS + CSP preliminar configurados |
| 2.7 | Métricas Prometheus (exporter) | Done   | Counters & histogram + endpoint    |

### Fase 3 – Performance y UX (Semanas 4–5)

- Cache corto (30–60s) para rastreo de envío. (Done 30s inicial)
- Pre‑agregados de estadísticas (tabla/materialized view) + endpoint `envios/estadisticas/` (Done: matview + fallback + cache).
- Paginación e hist. paginado (limitar tamaño respuesta).
- Refactor API client: refresh automático token, abort y timeout, retry exponencial GET.
- Code splitting + análisis bundle.

### Fase 4 – Asíncrono y Escalabilidad (Semanas 6–7)

- Celery (cola: notificaciones estado / correos).
- Configuración para workers + beat.
- Posible extracción futura de tracking a microservicio (evaluación técnica, no ejecución aún).

### Fase 5 – Calidad Continua (Semanas 8–9)

- Pipeline CI: lint, tests, coverage gate, build imágenes.
- Dependabot / Renovate.
- Auditorías seguridad automatizadas (pip-audit, npm audit) en CI.

### Fase 6 – Optimización Avanzada (Iterativa)

- Feature toggles centralizados.
- A/B pequeños en interfaz (navegación / formulario simple vs avanzado).
- Instrumentación OpenTelemetry básica (trazas API críticas).

---

## 🔄 Ciclo de Trabajo Recomendado (Sprint Loop)

1. Planificación: seleccionar tarjetas priorizadas (según fase actual).
2. Diseño técnico ligero (ADR si afecta arquitectura).
3. Implementación + pruebas locales.
4. Pull Request: checklist + revisión.
5. Merge → despliegue staging.
6. Validación métricas y logs → producción (si aplica).

---

## 🧪 Estrategia de Pruebas

| Tipo         | Enfoque                                             | Herramientas            |
| ------------ | --------------------------------------------------- | ----------------------- |
| Unitarias    | Modelos, servicios auth, utilidades                 | pytest, pytest-django   |
| Integración  | API endpoints críticos (login, envío CRUD, rastreo) | APIClient               |
| Carga Ligera | Rastrear (burst 50 req)                             | locust / k6 (posterior) |
| Frontend     | Hooks servicios + componentes clave                 | vitest + RTL            |
| Seguridad    | JWT flows, rate limit, enumeración pública          | pytest parametrizado    |

Cobertura objetivo incremental: 40% → 55% → 70%.

---

## 📊 Métricas (KPIs) & Observabilidad

| KPI                           | Fuente              | Umbral Inicial |
| ----------------------------- | ------------------- | -------------- |
| P95 Latencia /envios/rastrear | Middleware métricas | < 250 ms       |
| Errores 5xx / día             | Logs agregados      | < 5            |
| Tasa fallos login             | Logs auth           | < 3%           |
| Cobertura backend             | Coverage report     | ≥ 70%          |
| Tiempo build CI               | Pipeline            | < 6 min        |

Prometheus métricas sugeridas: `packfy_request_latency_seconds`, `packfy_request_total{status=..}`, `packfy_auth_fail_total`, `packfy_envio_estado_changes_total`.

---

## 🧩 Cambios de Datos (Data Evolution)

| Cambio                         | Tipo      | Fase | Acción                             |
| ------------------------------ | --------- | ---- | ---------------------------------- |
| Nueva secuencia guía           | Migración | F1   | Crear secuencia + default en campo |
| Índices compuestos             | Migración | F1   | Add index concurrently (si prod)   |
| Materialized view estadísticas | Opcional  | F3   | Script refresh + cron Celery       |

---

## 🔐 Checklist Seguridad (Mantener Actualizado)

- [x] SECRET_KEY fuera del repo
- [ ] CORS restringido en prod (pendiente verificación final)
- [ ] CSP activa (prod)
- [ ] HSTS activo
- [x] JWT blacklist operativo
- [ ] Rate limiting verificado (Redis) (actualmente fallback memoria)
- [ ] No endpoints públicos con datos PII excesivos
- [ ] Dependencias auditadas última semana

---

## ⚡ Performance Checklist

- [ ] Índices aplicados
- [ ] N+1 auditado en listados
- [ ] Cache rastreo operativo
- [ ] Pre‑agregados estadísticas
- [ ] Bundle frontend < 250KB gzip inicial
- [ ] Imágenes optimizadas / lazy

---

## 🛡 Riesgos y Mitigaciones

| Riesgo                        | Impacto | Prob. | Mitigación                            |
| ----------------------------- | ------- | ----- | ------------------------------------- |
| Condición carrera número guía | Alto    | Media | Secuencia DB (F1)                     |
| Abuse endpoints públicos      | Medio   | Alta  | Rate limit + captcha ligero si escala |
| Fuga PII en logs              | Alto    | Media | Filtro logging + revisión PR          |
| Tokens no invalidados         | Alto    | Media | Blacklist + rotación F2               |
| Latencia elevada en búsquedas | Medio   | Media | Índices + cache F3                    |
| Falta visibilidad errores     | Alto    | Media | Prometheus + alerting básico F2       |

---

## 🧱 Arquitectura Objetivo (Resumen)

- Monolito Django modular → listo para extracción futura de dominio "tracking".
- Servicios de soporte: PostgreSQL, Redis, (futuro) Celery worker.
- Frontend: SPA modular + PWA + code splitting.
- Observabilidad: logs estructurados + métricas + (futuro) tracing.
- Seguridad por capas: headers estrictos, JWT reforzado, rate limiting, validación entradas.

---

## 🗃 Estructura de Carpetas Reforzada (Propuesta Incremental)

```
backend/
  config/
    settings_base.py
    settings_development.py
    settings_production.py
  envios/
    services/
    selectors/
    serializers.py
frontend/
  src/
    services/
      httpClient.ts
      envios.ts
      auth.ts
    domain/
    components/
```

---

## ⚙️ Estándares de Código

- Python: black (line-length 88 opcional), isort, flake8 / pylint selectivo.
- TypeScript: ESLint (reglas strict), no `any` sin justificar.
- Commits convencionales (`feat:`, `fix:`, `chore:`, `docs:`...).
- PR Checklist (plantilla): pruebas, migraciones, docs, riesgos, rollback.

---

## 🔄 Flujo JWT Propuesto (Fase 2)

1. Login → access (30m) + refresh (7d) + device hash opcional.
2. Refresh rota refresh token (blacklist anterior) si `ROTATE_REFRESH_TOKENS=True`.
3. Logout: blacklist access + refresh.
4. Middleware añade `request_id` para correlación.

---

## 🧰 Tareas Detalladas por Fase

### Fase 1 (Hardening) – Detalle

| Nº  | Tarea                            | Owner | Estado | Notas                                |
| --- | -------------------------------- | ----- | ------ | ------------------------------------ |
| 1   | Extraer SECRET_KEY               |       | Done   | settings_base creado + guard en prod |
| 2   | Limpiar SIMPLE_JWT duplicado     |       | Done   | Config consolidada en settings_base  |
| 3   | Nueva estrategia numero_guia     |       | Done   | UUID corto implementado (PKF + hex)  |
| 4   | Índices DB                       |       | Done   | Migración 0002 creada                |
| 5   | Refactor API baseURL             |       | Done   | api.ts prioriza VITE_API_BASE_URL    |
| 6   | README corrección versión Django |       | Done   | Versión Django 4.2.x LTS corregida   |
| 7   | Crear endpoint /health           |       | Done   | /health añadido                      |
| 8   | Test concurrencia guía           |       | Done   | Test + script run_tests.ps1          |

(Replica tablas para Fases 2+ según avance.)

---

## 📝 Registro de Decisiones (ADR lightweight)

Formato: `docs/adrs/ADR-<número>-<slug>.md`

- ADR-001: Estrategia identificadores de envíos.
- ADR-002: Política rate limiting público.
- ADR-003: Esquema logging estructurado.

(Agregar según se creen.)

---

## 📒 Sección de Actualizaciones (Changelog Resumido)

| Fecha      | Versión / Fase     | Cambio                                                                     | Autor        |
| ---------- | ------------------ | -------------------------------------------------------------------------- | ------------ |
| 2025-08-15 | Inicio             | Creación del plan maestro                                                  | AI Assistant |
| 2025-08-15 | Fase 1 (Hardening) | Settings base, numero_guia UUID, tests base                                | AI Assistant |
| 2025-08-15 | Fase 2 (Seg/Obs)   | JWT blacklist, RequestID, /metrics, logging JSON, rate limit base, headers | AI Assistant |
| 2025-08-15 | Fase 3 (Perf/UX)   | Cache rastreo, matview+fallback+cache, paginación segura                   | AI Assistant |
| 2025-08-15 | Fase 5 (Calidad)   | CI multi-OS, lint (Ruff), cobertura XML/HTML, runner PowerShell            | AI Assistant |

> Mantener esta tabla breve; detalles extensos en PRs / commits.

---

## 🧪 Plantilla de PR (Sugerida)

```
Título: feat(F1): <descripción breve>

Resumen:
- Qué cambia
- Motivación

Checklist:
[ ] Tests agregados / actualizados
[ ] Migraciones ejecutadas
[ ] Docs/plan actualizado
[ ] Riesgos evaluados
[ ] Estrategia rollback

Riesgos:
- ...
Rollback:
- revert commit / dropear migración X
```

---

## 🚨 Estrategia de Rollback

| Tipo Cambio             | Rollback                     | Tiempo Estimado |
| ----------------------- | ---------------------------- | --------------- |
| Solo código             | Git revert                   | < 5 min         |
| Migración schema simple | `migrate <app> <prev>`       | 5–10 min        |
| Migración destructiva   | Backup + restore             | 30+ min         |
| Config infra            | Revert env / imagen anterior | < 10 min        |

---

## 📍 Próximos Pasos Inmediatos (Activables Ahora)

1. Aumentar cobertura backend a ≥ 40% (luego 55%): más tests en envíos (cambiar_estado, búsquedas), permisos y notificaciones.
2. Iniciar Fase 4: esqueleto Celery (worker/beat) y mover notificaciones/correos a tareas asíncronas.
3. Continuar Fase 3 en frontend: refactor http client (refresh/timeout/retry) y code splitting.
4. Añadir “coverage gate” en CI cuando superemos 55% para fijar umbral mínimo.

---

## 🔁 Mantenimiento del Documento

- Actualizar tablas de tareas al cerrar cada PR.
- Al final de cada semana: sección Changelog.
- Refactor mayor → añadir ADR.
- Revisión formal del plan cada 4 semanas.

---

## ✅ Estado Inicial de Salud (Snapshot 2025-08-15)

| Aspecto         | Estado | Nota                                          |
| --------------- | ------ | --------------------------------------------- |
| Seguridad       | ⚠️     | CORS abierto, SECRET_KEY expuesto             |
| Seguridad       | 🟡     | CORS abierto (dev), SECRET_KEY protegido prod |
| Identificadores | ⚠️     | Posible carrera numero_guia                   |
| Identificadores | 🟢     | UUID corto implementado, test pendiente       |
| Performance     | 🟡     | Sin índices específicos, sin cache selectiva  |
| Observabilidad  | ⚠️     | Sin métricas, logging no estructurado         |
| Pruebas         | 🟡     | Cobertura desconocida                         |
| Infra           | 🟢     | Compose funcional, Redis y Postgres ok        |
| Frontend API    | 🟡     | BaseURL heurística, sin refresh auto          |

Leyenda: 🟢 OK / 🟡 Mejorable / ⚠️ Crítico

---

## © Gestión

Mantener consistencia con licencia del repositorio y estándares de contribución.

---

Fin del documento.
