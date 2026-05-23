# Solicitud de Revisión — Agente Frontend — HU-07

| Campo | Valor |
|---|---|
| **Agente** | Frontend Developer |
| **HU** | HU-07 — Portal Web de Consulta para Cliente Final |
| **CAs** | CA-01 al CA-12 |
| **Rama** | `HU1_CA1-CA6_DEVDAVID_ITEREACION1` |
| **Fecha** | 2026-05-23 |
| **Estado** | PLANNING — Pendiente aprobación del Arquitecto Líder |

---

## Resumen del Plan

Se propone implementar el **Portal Web de Consulta para Cliente Final** con las siguientes características principales:

### Arquitectura
- **Layout Separado**: Se crea un `PortalLayout` light theme completamente independiente del Layout operario (dark theme) existente.
- **Rutas**: Todas bajo `/cliente/*` — Login, Dashboard, Documentos, Explorador, Visor, Acceso Denegado.
- **Estado**: Zustand (`clientStore`) para sesión; React Query para data fetching de `/api/v1/cliente/*`.
- **Backend**: Se consumirán los 6 endpoints existentes en `BackEnd/app/api/v1/endpoints/cliente.py`.

### Archivos Nuevos (27 archivos)
- **8 archivos SCSS** (light theme tokens, layout portal, dashboard, explorador, documentos, visor, login, errores)
- **1 archivo de tipos** (`types/cliente.ts`)
- **1 servicio** (`services/clienteService.ts`)
- **5 hooks** (dashboard, documentos, carpetas, detalle, session timeout)
- **8 componentes portal** (Layout, Dashboard, Explorer, FolderTree, DocumentList, Viewer, Login, AccessDenied)
- **1 página** (`ClientePortalPage.tsx`)

### Archivos Modificados (3 archivos)
- `main.scss` — agregar @use de los nuevos SCSS
- `clientStore.ts` — agregar estado de sesión portal
- `App.tsx` — agregar rutas `/cliente/*`

### Cobertura de CAs
| CA | Implementación |
|---|---|
| CA-01 | Login mock con redirección a Dashboard |
| CA-02 | Dashboard con 4 tarjetas de métricas + tabla últimos docs |
| CA-03 | Explorador con árbol colapsable (35%) + contenido (65%) |
| CA-04 | Tabla paginada con filtros (tipo, fecha, búsqueda) |
| CA-05/06 | Visor readonly PDF/IMG + panel metadatos + zoom/paginación |
| CA-07 | Botón "Descargar" en visor con Content-Disposition |
| CA-08 | Pantalla 403 "Acceso Denegado" + interceptor Axios |
| CA-09 | Banner azul "Documentos en proceso" en Dashboard |
| CA-10 | Timer inactividad 30 min → redirigir a Login |
| CA-11 | Responsive Desktop + Tablet (mixins respond-to) |
| CA-12 | Mini-árbol visual de ubicación en panel lateral del visor |

### Alineación con Gobernanza
- ✅ SCSS/BEM con prefijo `grm-` — nunca CSS inline
- ✅ Variables SCSS para todos los valores de diseño
- ✅ `@use` / `@forward` (no `@import`)
- ✅ TypeScript estricto — todas las props tipadas
- ✅ React Query para data fetching, Zustand para estado global
- ✅ Axios centralizado con interceptors
- ✅ PascalCase componentes, camelCase hooks/services

### Plan completo
Ver: `implementation_plan.md` en el directorio de artefactos del agente.

---

## Preguntas / Confirmaciones

1. **Login Mock**: HU-08 (Auth) no está implementada. Se creará un login mock que simule autenticación y setee `isAuthenticated=true` en Zustand. ¿Es aceptable?
2. **Descargas**: Se usará el endpoint `/api/v1/cliente/documentos/{id}/descargar` directamente con un `<a href>` target. ¿Se requiere algo adicional para el sección "Descargas" del menú lateral?

---

**Estado: Esperando aprobación del Arquitecto Líder para proceder a EXECUTION.**
