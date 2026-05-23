# Acta de Cierre — Iteración 1 -DEV-HU-2 — HU-02

## Resumen Ejecutivo
- **CAs ejecutados:** 4/4 (CA-01, CA-02, CA-03, CA-04) — 100% de la selección
- **CAs excluidos:** Ninguno de la selección
- **QA omitido:** Sí — por decisión de tiempo del proyecto (riesgo documentado)
- **Rechazos:** 1 (Backend — violación Clean Architecture: servicio acoplado al ORM)
- **Rama:** `HU2_CA1-CA4_DevDamian_ITEREACION1`
- **Fecha de cierre:** 2026-05-23

## Inventario de Entregables

### Backend — ✅ Aprobado (tras corrección)
| Archivo | Estado | Observaciones |
|---------|--------|---------------|
| `BackEnd/app/api/v1/endpoints/batches.py` | ✅ | POST `/api/v1/batches`, RBAC correcto, APIResponse, logging |
| `BackEnd/app/services/batch_service.py` | ✅ | Use Case correcto, inyección de repositorio (Port) |
| `BackEnd/app/domain/models/batch.py` | ✅ | Entidad de dominio pura (dataclass), sin ORM |
| `BackEnd/app/domain/ports/batch_repository.py` | ✅ | Interfaz abstracta `BatchRepositoryPort` |
| `BackEnd/app/db/models/batches.py` | ✅ | Modelos SQLAlchemy `LoteProcesamiento` + `DocumentoLote` |
| `BackEnd/app/db/repositories/batch_repository.py` | ✅ | Adapter que implementa `BatchRepositoryPort` |
| `BackEnd/app/schemas/batches.py` | ✅ | `BatchCreate` con validador de `modo_ingesta`, `BatchResponse` |

### Frontend — ✅ Aprobado (con observaciones menores)
| Archivo | Estado | Observaciones |
|---------|--------|---------------|
| `FrontEnd/src/components/intake/IntakeDashboard.tsx` | ✅ | Paso 1 (selección modo) + Paso 2 (módulo condicional) |
| `FrontEnd/src/components/intake/ScannerModule.tsx` | ✅ | Mock TWAIN, conexión simulada, captura |
| `FrontEnd/src/components/intake/FolderModule.tsx` | ✅ | `webkitdirectory`, filtrado de extensiones |
| `FrontEnd/src/components/intake/DocumentList.tsx` | ✅ | Tabla de documentos, selección, eliminación |
| `FrontEnd/src/store/batchStore.ts` | ✅ | Zustand store completo, tipado correcto |
| `FrontEnd/src/services/api.ts` | ✅ | Axios centralizado con interceptor JWT |
| `FrontEnd/src/services/batchService.ts` | ✅ | Mock fallback aprobado por el Arquitecto |
| `FrontEnd/src/styles/abstracts/_variables.scss` | ✅ | Design tokens definidos |
| `FrontEnd/src/styles/abstracts/_mixins.scss` | ✅ | Mixins reutilizables |
| `FrontEnd/src/styles/base/_reset.scss` | ✅ | Reset global con tokens |
| `FrontEnd/src/styles/main.scss` | ✅ | Solo `@use` (sin estilos directos) |
| 4x `*.module.scss` | ✅ | CSS Modules por componente |

## Validación de Gobernanza

| Criterio | Backend | Frontend |
|----------|---------|----------|
| Stack respetado | ✅ | ✅ |
| Clean Architecture | ✅ (tras corrección) | ✅ |
| Cloud-Ready | ✅ StoragePort definido | N/A |
| CERO credenciales | ✅ | ✅ |
| Nombrado convención | ✅ snake_case Python | ✅ PascalCase React |
| RBAC endpoints | ✅ `require_role` | N/A |
| SCSS / Design System | N/A | ✅ (observaciones menores) |
| Conventional Commits | ✅ | ✅ |

## Observaciones Pendientes (Deuda Técnica)
1. **Inline styles en Frontend** (6 ocurrencias) — DEBEN migrarse a SCSS en Iteración 2
2. **Campo `mode` vs `modo_ingesta`** en batchService.ts — desalineación con schema Pydantic
3. **Faltan `_typography.scss` y `_layout.scss`** en la estructura de estilos
4. **QA no ejecutado** — sin tests unitarios ni de integración para Iteración 1

## Métricas

| Métrica                       | Valor   |
|-------------------------------|---------|
| CAs completados               | 4       |
| CAs excluidos                 | 0       |
| Aprobaciones a primer intento | 1 (Frontend) |
| Rechazos                      | 1 (Backend — acoplamiento ORM) |
| Reintentos totales            | 1       |
| Violaciones críticas          | 0       |
| Cobertura de tests            | 0% (QA omitido) |

## Lecciones Aprendidas
1. **Reforzar Clean Architecture en los Handoffs**: El primer intento del Backend acopló la sesión de BD directamente al servicio. El Handoff debe ser más explícito sobre la necesidad del patrón Repository desde la primera entrega.
2. **Inline styles como hábito**: El agente Frontend tiende a usar `style={{}}` para ajustes rápidos. Se debe insistir en la auditoría de SCSS de forma preventiva en los Handoffs.
3. **Omisión de QA acumula riesgo**: Sin tests, las regresiones en iteraciones futuras serán más costosas de identificar. Se recomienda planificar una iteración de QA retroactiva.

## Firma
- **Arquitecto Líder:** Agente Orquestador GRM
- **Fecha:** 2026-05-23
