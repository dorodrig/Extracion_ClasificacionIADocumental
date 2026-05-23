# 🧠 Knowledge Base del Arquitecto Líder — Memoria Persistente
## Sistema GRM — Extracción y Clasificación Documental con IA

**Versión:** 1.1.0  
**Última actualización:** 2026-05-22  
**Propósito:** Archivo de recuperación de contexto para combatir la amnesia del agente.  
**Ruta:** `C:\zData\ExtracionDatosIA\Agentes\Arquitecto_Lider_KnowledgeBase.md`

---

> ⚠️ **INSTRUCCIÓN PARA EL AGENTE:**
> Si estás leyendo este archivo, es porque necesitas recuperar tu contexto completo.
> Lee CADA sección. NO omitas ninguna. Al terminar, confirma al Humano:
> *"He recuperado mi contexto completo. Estoy listo para operar."*

---

## 1. ¿QUIÉN ERES?

Eres el **Agente Arquitecto Líder (Orquestador)** del Proyecto GRM.
- **NO escribes código.** Solo planificas, delegas, evalúas y auditas.
- **Tu herramienta principal** son los archivos de Handoff que depositas en `.agentic-sync/`.
- **Tu ley máxima** es la Gobernanza Arquitectónica del proyecto.
- **Tu protocolo formal** está definido en el SKILL.md del handoff protocol.

**Tu System Prompt completo está en:**
`C:\zData\ExtracionDatosIA\Agentes\Arquitecto_Lider_SystemPrompt.md`

---

## 2. ¿QUÉ ES EL PROYECTO GRM?

**GRM Document Intelligence** es un sistema web local (On-Premise) que automatiza la digitalización, extracción y clasificación de documentos financieros bancarios (pagarés, endosos, cédulas, cartas laborales) usando:

1. **AWS Textract** — OCR síncrono página por página (confianza ≥95%)
2. **Google Gemini** — Dos agentes IA:
   - Agente de Contexto: OCR crudo → Paquete de Datos Limpios
   - Agente de Clasificación: Datos limpios → Carpetas organizadas + BD
3. **SQL Server 2019** — 15 tablas relacionales
4. **FastAPI + React** — Interfaz web localhost

### Pipeline BPMN completo:
```
Reglas de Trabajo (HU-01) → Ingesta (HU-02) → OCR Textract (HU-03) → 
Agente Contexto (HU-04) → ¿Datos completos? → 
  Sí → Agente Clasificación (HU-05) → Portal Cliente (HU-07)
  No → Revisión Humana (HU-06) → Agente Clasificación (HU-05)
```

### Roles:
| Rol | Acceso | JWT |
|-----|--------|-----|
| Administrador | Total | 8h |
| Operario | Selecciona cliente → opera | 8h |
| Cliente Final | Solo lectura de sus docs | 30min |

---

## 3. STACK TECNOLÓGICO (MEMORIZAR — NO CAMBIAR)

```
BACKEND:
  - Python 3.12
  - FastAPI 0.115 + Uvicorn
  - SQLAlchemy ORM + Alembic (migraciones)
  - Celery 5 + Redis (cola de procesamiento)
  - Pydantic v2 + pydantic-settings (.env)
  - google-generativeai (SDK Gemini)
  - boto3 (SDK AWS Textract)
  - pytest + pytest-asyncio (testing)

FRONTEND:
  - React 18 + TypeScript
  - Vite 5 (dev server puerto 5173)
  - Zustand (estado global)
  - @tanstack/react-query (estado servidor)
  - Axios (HTTP client)
  - react-pdf (visor PDF)
  - SASS/SCSS (preprocesador de estilos — CSS Modules por componente)
  - Vitest + React Testing Library (testing)

BASE DE DATOS:
  - SQL Server 2019+ (Express en piloto)
  - Puerto: 1433 (localhost\SQLEXPRESS)
  - BD: GRM_DB
  - Collation: SQL_Latin1_General_CP1_CI_AS

SERVICIOS:
  - Backend: http://localhost:8000
  - Frontend: http://localhost:5173
  - Redis: redis://localhost:6379/0
  - API Docs: http://localhost:8000/docs
```

---

## 4. PATRÓN ARQUITECTÓNICO

**Clean Architecture (Ports & Adapters)** — 4 capas:

```
┌─────────────────────────────────────────────────────┐
│ INFRAESTRUCTURA (Adapters)                          │
│   app/api/          → Endpoints FastAPI             │
│   app/db/           → SQLAlchemy Repositories       │
│   app/workers/      → Celery Tasks                  │
│   app/services/ocr/ → TextractAdapter (AWS SDK)     │
│   app/services/storage/ → LocalStorageAdapter       │
├─────────────────────────────────────────────────────┤
│ APLICACIÓN (Use Cases)                              │
│   app/services/     → rules, batch, classification  │
│   app/services/ai_agents/ → context, classification │
├─────────────────────────────────────────────────────┤
│ DOMINIO (Entities + Business Rules)                 │
│   app/domain/models/ → Entidades puras (sin ORM)    │
│   app/domain/ports/  → Interfaces abstractas        │
│   app/domain/rules/  → Validaciones de negocio      │
└─────────────────────────────────────────────────────┘
```

**Regla clave:** Los Adapters (infra) son REEMPLAZABLES sin cambiar el dominio.
Esto permite migrar de On-Premise a AWS Cloud cambiando solo los Adapters.

### Estructura de Estilos SASS/SCSS
```
FrontEnd/src/styles/
├── _variables.scss       ← Design tokens: $color-primary, $font-family-base, $spacing-unit
├── _mixins.scss          ← @mixin respond-to(), @mixin flex-center, @mixin transition
├── _reset.scss           ← Normalize/reset base (box-sizing, margins, fonts)
├── _typography.scss      ← Sistema tipográfico (h1-h6, pesos, tamaños)
├── _layout.scss          ← Grid, contenedores, flexbox utilities
└── main.scss             ← Entry point (@use de todos los parciales)

Cada componente:
  ComponentName.tsx + ComponentName.module.scss (CSS Modules)
```

---

## 5. INVENTARIO COMPLETO DE HUs Y CAs

### HU-01 — Configuración y Gestión de Reglas de Trabajo
**Sprint 1 | 13 SP | Frontend + Backend | 13 CAs**
- CA-01: Primer acceso sin reglas → formulario vacío
- CA-02: Listado de reglas con acciones (Editar, Iniciar, Ver)
- CA-03: Carga de regla para edición (pre-rellenado)
- CA-04: Creación de nueva regla adicional
- CA-05: Validación de campos obligatorios al guardar
- CA-06: Campos dinámicos a extraer (nombre, tipo, obligatorio)
- CA-07: Patrón de carpeta de salida con variables dinámicas
- CA-08: Umbral OCR fijo 95% (solo lectura, tooltip info)
- CA-09: Inicio de proceso desde regla → pantalla de decisión de modo
- CA-10: Versionamiento automático al actualizar (v1→v2, auditoría)
- CA-11: Persistencia para futuros proyectos + botón "Duplicar"
- CA-12: Validación nombre único de regla por cliente
- CA-13: Selección de modo de entrada (Escáner/Carpeta)
- **Tablas:** reglas_trabajo, reglas_trabajo_historial
- **Depende de:** HU-08 | **Bloquea:** HU-02, HU-04, HU-05

### HU-02 — Ingesta Dual de Documentos (Escáner/Carpeta)
**Sprint 1 | 8 SP | Frontend + Backend | 13 CAs (CA-00 a CA-12)**
- CA-00: Decisión explícita del modo tras "Iniciar Proceso"
- CA-01: Pantalla de ingesta según modo confirmado
- CA-02: Activación del escáner (driver TWAIN/WIA)
- CA-03: Captura de lote por escáner
- CA-04: Selección carpeta local (diálogo nativo)
- CA-05: Validación formatos (PDF/JPG/PNG/TIFF, excluir otros)
- CA-06: Segmentación PDF multi-página antes de OCR
- CA-07: Generación ruta temporal /temp/{batch_id}/{timestamp}/
- CA-08: Indicador de progreso de ingesta
- CA-09: Resumen de volumen pre-envío + eliminar docs individuales
- CA-10: Manejo de archivos corruptos/protegidos
- CA-11: Reconstrucción del PDF tras OCR de páginas
- CA-12: Cancelación de ingesta antes del envío
- **Tablas:** lotes_procesamiento, documentos_lote
- **Depende de:** HU-01, HU-08 | **Bloquea:** HU-03

### HU-03 — Integración AWS Textract OCR
**Sprint 1 | 13 SP | Backend (AWS SDK) | 12 CAs**
- CA-01: Credenciales AWS desde variables de entorno (no hardcoded)
- CA-02: Procesamiento síncrono página por página
- CA-03: Score confianza por campo (≥95% alta, <95% baja)
- CA-04: Manejo error conexión (3 reintentos, backoff exponencial)
- CA-05: Consolidación de todas las páginas en documento completo
- CA-06: Control SLA (≤60s 1-3 págs, ≤120s 4+ págs)
- CA-07: Tipo análisis según tipo doc (detect_text vs analyze_document)
- CA-08: Almacenamiento granular por página (raw JSON + parseado)
- CA-09: Procesamiento de JPG/PNG/TIFF como página única
- CA-10: Indicador progreso OCR para panel monitoreo
- CA-11: Manejo página en blanco/ilegible
- CA-12: Limpieza archivos temporales tras procesamiento exitoso
- **Tablas:** ocr_resultados_paginas
- **Depende de:** HU-02 | **Bloquea:** HU-04

### HU-04 — Agente de Contexto IA (Google Gemini)
**Sprint 2 | 13 SP | Backend (Gemini SDK) | 12 CAs**
- CA-01: Prompt con datos OCR + reglas (sin info de otros clientes)
- CA-02: Invocación Gemini SDK con API key desde .env
- CA-03: Parseo y validación respuesta JSON (2 reintentos si inválida)
- CA-04: Validación campos obligatorios (datos_completos = true/false)
- CA-05: Enrutamiento docs incompletos → cola revisión humana (HU-06)
- CA-06: Enrutamiento docs completos → Agente Clasificación (HU-05)
- CA-07: Detección tipo documento (conflicto tipo_esperado vs detectado)
- CA-08: Manejo timeout/error Gemini (3 reintentos, backoff)
- CA-09: Registro tokens y costos en log_ia_invocaciones
- CA-10: Aislamiento de contexto (sin contaminación entre documentos)
- CA-11: Normalización valores (CC→solo dígitos, fecha→ISO 8601)
- CA-12: Paquete de Datos Limpios completo (JSON estructurado)
- **Tablas:** agente_contexto_resultados
- **Depende de:** HU-03, HU-01 | **Bloquea:** HU-05 | **Alimenta:** HU-06

### HU-05 — Agente de Clasificación IA (Google Gemini)
**Sprint 2 | 13 SP | Backend (Gemini + Filesystem) | 13 CAs**
- CA-01: Recepción del Paquete de Datos Limpios (validación)
- CA-02: Construcción ruta destino con patrón /{CC}/{NOMBRE}/{TIPO}/{ARCHIVO}
- CA-03: Gemini razona sobre ambigüedades del patrón
- CA-04: Creación física de carpetas (recursiva, permisos)
- CA-05: Copia documento a destino (verificación hash MD5)
- CA-06: Persistencia datos extraídos en BD (UPSERT)
- CA-07: Agrupación por CC (misma persona → mismo directorio)
- CA-08: Manejo nombres duplicados (sufijo incremental _001)
- CA-09: Actualización estado "Clasificado Exitosamente"
- CA-10: Resumen del lote (clasificados, revisión, errores, árbol)
- CA-11: Reprocesamiento con instrucción correctiva del operario
- CA-12: Manejo error escritura filesystem
- CA-13: Trazabilidad completa (todas las rutas, timestamps, estados)
- **Tablas:** documentos_clasificados
- **Depende de:** HU-04 | **Alimenta:** HU-07 | **Recibe de:** HU-06

### HU-06 — Validación Humana: Pendientes y Visor Operario
**Sprint 2 | 8 SP | Frontend + Backend | 12 CAs**
- CA-01: Tabla pendientes (archivo, cliente, motivo, tiempo en cola)
- CA-02: Filtrado/búsqueda (cliente, motivo, fechas, nombre archivo)
- CA-03: Visor documento (PDF izq + datos extraídos der, campos rojos)
- CA-04: Navegación páginas, zoom, rotación
- CA-05: Corrección directa campo individual (1 error)
- CA-06: Instrucción texto libre al agente (2+ errores)
- CA-07: Seguimiento resultado reprocesamiento (auto-actualiza estado)
- CA-08: Descarte manual con motivo obligatorio
- CA-09: Indicador tiempo en cola (ámbar >15min, rojo >60min)
- CA-10: Panel datos extraídos con confianza y estado validación IA
- CA-11: Acceso rápido al lote de origen
- CA-12: Actualización en tiempo real (WebSocket)
- **Tablas:** documentos_pendientes
- **Depende de:** HU-04, HU-08 | **Alimenta:** HU-05 | **Registra en:** HU-09

### HU-07 — Portal Web Cliente Final
**Sprint 3 | 8 SP | Frontend + Backend | 12 CAs**
- CA-01: Login con cédula + contraseña → dashboard
- CA-02: Dashboard métricas (docs procesados, tipos, última fecha)
- CA-03: Explorador carpetas (árbol expandible /{CC}/{NOMBRE}/{TIPO}/)
- CA-04: Tabla documentos paginada con búsqueda y filtros
- CA-05: Visor documentos solo lectura (PDF + datos)
- CA-06: Navegación páginas, zoom, descarga
- CA-07: Descarga PDF original
- CA-08: Aislamiento total por cliente (HTTP 403 si doc ajeno)
- CA-09: Indicador docs en proceso ("X en revisión")
- CA-10: Sesión expira 30min inactividad + cierre manual
- CA-11: Diseño responsive (desktop ≥1024px + tablet 768px)
- CA-12: Visualización estructura carpetas en visor
- **Endpoints:** solo GET /api/cliente/* (lectura)
- **Depende de:** HU-05, HU-08

### HU-08 — Gestión de Roles y Autenticación
**Sprint 1 | 8 SP | Frontend + Backend | 12 CAs**
- CA-01: Login unificado (cédula + contraseña, toggle visibilidad)
- CA-02: Autenticación SHA-256 + JWT → redirección por rol
- CA-03: Selección cliente obligatoria para Operario
- CA-04: Credenciales incorrectas (no revelar cuál, 5 intentos → bloqueo 15min)
- CA-05: Protección rutas por rol (403 Forbidden + log)
- CA-06: Gestión usuarios por Admin (crear, activar/desactivar, resetear pass)
- CA-07: Creación usuario (nombre, cédula, rol, pass temporal, SHA-256+salt)
- CA-08: Expiración sesión (cliente 30min, operario/admin 8h)
- CA-09: Cambio de cliente activo (advertencia si lote en curso)
- CA-10: Gestión clientes por Admin (crear, asociar operarios N:N)
- CA-11: Cierre sesión explícito (invalidar JWT, limpiar storage)
- CA-12: Hash SHA-256 + salt 32 bytes, campos separados, NUNCA plain text
- **Tablas:** usuarios, clientes, usuarios_clientes
- **Bloquea:** TODAS las HU con UI

### HU-09 — Trazabilidad, Auditoría y Log
**Sprint 2 | 5 SP | Backend + Admin UI | 10 CAs**
- CA-01: Registro automático cada etapa pipeline (log_proceso)
- CA-02: Registro intervenciones humanas (log_auditoria_usuario)
- CA-03: Registro invocaciones Textract (log_ia_invocaciones)
- CA-04: Registro invocaciones Gemini (log_ia_invocaciones)
- CA-05: Historial documento por Admin (línea de tiempo visual)
- CA-06: Panel logs Admin con filtros + export CSV
- CA-07: Dashboard métricas pipeline (tasa éxito, intervención, tokens)
- CA-08: Trazabilidad de reprocesados (iteraciones, motivos, resultado)
- CA-09: Eventos seguridad (login fallido, bloqueo, acceso no autorizado)
- CA-10: Retención 90 días proceso, 1 año auditoría/seguridad
- **Tablas:** log_proceso, log_auditoria_usuario, log_ia_invocaciones, log_seguridad
- **Transversal:** todas las HU escriben en estas tablas

### HU-10 — Esquema de Base de Datos (SQL Server)
**Sprint 1 | 8 SP | Backend (DBA) | 10 CAs**
- CA-01: 15 tablas creadas con tipos correctos
- CA-02: Integridad referencial (FKs entre todas las tablas)
- CA-03: Separación datos imagen vs. datos extraídos
- CA-04: JSON dinámico consultable (JSON_VALUE, OPENJSON), <500ms/10K docs
- CA-05: Columna preparada para Base64 futuro (contenido_b64)
- CA-06: 8 índices non-clustered en columnas de consulta frecuente
- CA-07: Script migración V1 idempotente + tabla schema_migrations
- CA-08: Relaciones log → documentos_lote (ON DELETE SET NULL)
- CA-09: Consulta historial cliente con paginación OFFSET/FETCH <500ms
- CA-10: documentos_pendientes como cola (UPDATE atómico anti-race-condition)
- **15 Tablas:** usuarios, clientes, usuarios_clientes, reglas_trabajo,
  reglas_trabajo_historial, lotes_procesamiento, documentos_lote,
  ocr_resultados_paginas, agente_contexto_resultados, documentos_clasificados,
  documentos_pendientes, log_proceso, log_auditoria_usuario,
  log_ia_invocaciones, log_seguridad
- **Bloquea:** TODAS las HU

---

## 6. MOCKUPS DISPONIBLES

| HU | Ruta del Mockup |
|----|------------------|
| HU-01 | `C:\zData\ExtracionDatosIA\HU\HU-Mockups\MOCKUP-HU-01-Reglas-Trabajo.md` |
| HU-02 | `C:\zData\ExtracionDatosIA\HU\HU-Mockups\MOCKUP-HU-02-Ingesta-Documentos.md` |
| HU-06 | `C:\zData\ExtracionDatosIA\HU\HU-Mockups\MOCKUP-HU-06-Validacion-Operario.md` |
| HU-07 | `C:\zData\ExtracionDatosIA\HU\HU-Mockups\MOCKUP-HU-07-Portal-Cliente.md` |
| HU-08 | `C:\zData\ExtracionDatosIA\HU\HU-Mockups\MOCKUP-HU-08-Login-Autenticacion.md` |

### 6.2 Mockups Imagen (PNG) — Referencia Visual para Maquetación

| Tipo | Ruta |
|------|------|
| Imágenes PNG | `C:\zData\ExtracionDatosIA\Mockups\*.png` |

> **REGLA PARA HANDOFFS FRONTEND:**
> Cuando existan imágenes PNG en la ruta de Mockups para la HU que se está orquestando,
> el Handoff Frontend DEBE incluir:
> 1. La ruta absoluta de cada PNG relacionado con la HU.
> 2. La instrucción: *"Lee e interpreta las imágenes PNG como referencia visual OBLIGATORIA
>    para la maquetación. La fidelidad visual al mockup es un criterio de aceptación."*
> 3. Si NO existen PNGs para esa HU, documentar: *"Sin mockup imagen disponible.
>    Usar mockup textual (MD) y criterio del agente para la maquetación."*

---

## 7. ESTÁNDARES DE CÓDIGO — RESUMEN RÁPIDO

### Backend Python
- Funciones/variables: `snake_case`
- Clases: `PascalCase`
- Constantes: `SCREAMING_SNAKE_CASE`
- Archivos: `snake_case.py`
- Endpoints: `/api/v1/` + sustantivos plurales + kebab-case
- Respuestas: `APIResponse(success, data, message, error)`
- Excepciones: `GRMException` hierarchy (NUNCA silenciar, NUNCA Exception genérica)
- Config: `pydantic-settings` desde `.env` (CERO hardcoded)
- Logger: `logging.getLogger("grm.{module}")` (NUNCA print())

### Frontend TypeScript/React
- Componentes: `PascalCase.tsx`
- Hooks/servicios: `camelCase.ts`
- Props: Interfaces tipadas (NUNCA `any`)
- Estado global: Zustand
- Estado servidor: React Query
- HTTP: axios centralizado con interceptors JWT
- Rutas protegidas: `AuthGuard` con `allowedRoles`

### Frontend Estilos SASS/SCSS
- Preprocesador: SASS/SCSS (paquete `sass` en devDependencies)
- Entry point: `src/styles/main.scss`
- Variables: `src/styles/_variables.scss` (design tokens)
- Mixins: `src/styles/_mixins.scss` (responsive, animaciones, helpers)
- Componentes: `ComponentName.module.scss` junto al `.tsx` (CSS Modules)
- Clases: kebab-case (`card-header`, `btn-primary`)
- Nesting: Máximo 3 niveles de profundidad
- `!important`: PROHIBIDO (excepto overrides justificados de librerías)
- Inline styles: PROHIBIDO en componentes React
- CSS-in-JS: NO PERMITIDO — todo se maneja vía SCSS
- Fallback: CSS puro solo si se justifica documentadamente
- Mockups: Los componentes DEBEN maquetarse fieles a los PNG de `C:\zData\ExtracionDatosIA\Mockups\`

### Base de Datos SQL Server
- Tablas: `snake_case` plural español
- Columnas: `snake_case`
- Índices: `IX_{tabla}_{columna}`, `UX_{tabla}_{columna}`
- FKs: `FK_{hijo}_{padre}`
- Auditoría obligatoria: `created_at`, `updated_at`, `created_by`
- Soft delete: `activo BIT DEFAULT 1`
- JSON: `NVARCHAR(MAX)` (nunca TEXT)
- PKs: `INT IDENTITY(1,1)`
- Batch IDs: `UNIQUEIDENTIFIER DEFAULT NEWID()`

### Commits
```
feat(HU-XX): descripción en español
fix(HU-XX): corrección de bug
docs: documentación
test: agregar tests
refactor: sin cambio de comportamiento
```

---

## 8. MAPA DE ARCHIVOS DEL PROYECTO

```
C:\zData\ExtracionDatosIA\
│
├── Agentes\
│   ├── Arquitecto_Lider_SystemPrompt.md    ← TU DEFINICIÓN (este agente)
│   ├── Arquitecto_Lider_KnowledgeBase.md   ← ESTE ARCHIVO (memoria)
│   ├── Agente_PO_SystemPrompt.md           ← Agente Product Owner
│   ├── PO_Skills.md                        ← Skills del PO
│   ├── infraestructura_installer.md        ← Agente Infraestructura
│   └── skills\
│       └── architect_handoff_protocol\
│           └── SKILL.md                    ← Protocolo formal de Handoffs
│
├── Mockups\                                ← IMÁGENES PNG de referencia visual para maquetación
│
├── BackEnd\                                ← VACÍO (awaiting Sprint 1)
│   └── app\                                ← Estructura Clean Architecture
│
├── FrontEnd\                               ← VACÍO (awaiting Sprint 1)
│   └── src\                                ← Estructura React 18 + TS
│       ├── services\                 ← API services (axios)
│       ├── store\                    ← Zustand stores
│       ├── styles\                   ← SASS/SCSS (design tokens, mixins, layout)
│       │   ├── _variables.scss
│       │   ├── _mixins.scss
│       │   ├── _reset.scss
│       │   ├── _typography.scss
│       │   ├── _layout.scss
│       │   └── main.scss
│       ├── types\                    ← TypeScript interfaces
│
├── Documentancion\
│   └── Gobernanza_Arquitectura.md          ← LEY DEL PROYECTO (1286 líneas)
│
├── HU\
│   ├── HU-01-Gestion-Reglas-Trabajo.md     ← hasta HU-10
│   ├── ...
│   ├── HU-10-Esquema-Base-de-Datos.md
│   └── HU-Mockups\
│       ├── MOCKUP-HU-01, 02, 06, 07, 08
│
├── Mockups\                                ← Vacío (mockups en HU/HU-Mockups/)
│
├── ScrpitBaseDatos\                        ← Scripts SQL / migraciones
│
└── .agentic-sync\                          ← BUZÓN DE DELEGACIÓN (se crea al orquestar)
    ├── handoff_backend_HU{XX}_CA{YY}.md
    ├── handoff_frontend_HU{XX}_CA{YY}.md
    ├── handoff_qa_HU{XX}_CA{YY}.md
    ├── approval_request_{ROL}.md
    ├── architecture_violation_{HU}.md
    ├── coverage_matrix.md
    └── cierre_iteracion_{ITER}_{HU}.md
```

---

## 9. DOCUMENTOS QUE DEBES LEER AL INICIAR

| Prioridad | Documento | Ruta | Cuándo leer |
|-----------|-----------|------|-------------|
| 🔴 1 | Knowledge Base (este archivo) | `Agentes\Arquitecto_Lider_KnowledgeBase.md` | SIEMPRE al inicio |
| 🔴 2 | Gobernanza Arquitectónica | `Documentancion\Gobernanza_Arquitectura.md` | SIEMPRE al inicio |
| 🔴 3 | SKILL Handoff Protocol | `Agentes\skills\architect_handoff_protocol\SKILL.md` | Antes de crear Handoffs |
| 🟡 4 | HU específica | `HU\HU-{XX}-*.md` | Al recibir solicitud |
| 🟡 5 | Mockup de HU | `HU\HU-Mockups\MOCKUP-HU-{XX}-*.md` | Si existe, para Frontend |

---

## 10. PREGUNTAS FRECUENTES (FAQ)

**P: ¿Puedo escribir código en los Handoffs?**
R: NO. Los Handoffs contienen especificaciones técnicas, no código. El código lo escribe el agente especialista.

**P: ¿Puedo aprobar un plan sin leer la Gobernanza?**
R: NO. TODA aprobación requiere verificación contra la Gobernanza.

**P: ¿Qué hago si un CA referenciado no existe en la HU?**
R: Reporta al Humano Cartero: "El CA-XX no existe en la HU-YY. Los CAs válidos son CA-01 a CA-{último}."

**P: ¿Qué hago si el Humano me pide escribir código?**
R: Responde: "Mi rol como Arquitecto Líder no incluye la escritura de código. Debo delegarlo mediante un Handoff al agente {Backend/Frontend} correspondiente."

**P: ¿Qué hago si no recuerdo el stack?**
R: Lee la sección 3 de este documento o la Gobernanza §1.

**P: ¿Qué hago si el agente especialista propone una tecnología fuera del stack?**
R: RECHAZA el plan. Solo se permite el stack definido en la Gobernanza.

**P: ¿Cuántos reintentos tiene un agente antes de escalar?**
R: Máximo 2 reintentos. Violaciones CRÍTICAS (credenciales expuestas) se bloquean sin reintentos.

**P: ¿Debo crear el directorio .agentic-sync?**
R: Sí, se crea automáticamente al escribir el primer Handoff.

**P: ¿En qué orden se ejecutan los agentes?**
R: SECUENCIAL OBLIGATORIO: 1️⃣ Backend → 2️⃣ Frontend → 3️⃣ QA

**P: ¿Puedo delegar CAs de distintas HUs en un solo Handoff?**
R: NO. Cada Handoff corresponde a una sola HU. CAs de diferentes HUs van en Handoffs separados.

---

## 11. CHANGELOG

| Versión | Fecha       | Cambios                                                 |
|---------|-------------|---------------------------------------------------------|
| v1.0.0  | 2026-05-22  | Versión inicial — Inventario completo de 10 HUs/120 CAs |
| v1.1.0  | 2026-05-22  | SASS/SCSS agregado al stack, estándares Frontend, estructura de archivos SCSS, Mockups PNG como referencia visual obligatoria |

---

*Knowledge Base del Agente Arquitecto Líder — Proyecto GRM Document Intelligence*
*Archivo de recuperación de memoria — Fuente de verdad complementaria*
