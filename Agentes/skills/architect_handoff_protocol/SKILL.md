# 📋 SKILL — Protocolo de Handoff del Arquitecto Líder
## Sistema GRM — Arquitectura Multi-Agente Estricta

**Versión:** 1.1.0  
**Autor:** Agente Arquitecto Líder (Orquestador)  
**Fecha:** 2026-05-22  
**Ruta canónica:** `C:\zData\ExtracionDatosIA\Agentes\skills\architect_handoff_protocol\SKILL.md`

---

> ⚠️ **DOCUMENTO NORMATIVO:** Este SKILL define la estructura formal, las reglas obligatorias y el protocolo de comunicación que el Arquitecto Líder DEBE seguir al crear archivos de delegación (Handoffs) para los agentes especialistas (Backend, Frontend, QA). Ningún Handoff puede generarse sin adherirse a este protocolo.

---

## 1. Definición y Propósito

Un **Handoff** es un contrato técnico unidireccional que el Arquitecto Líder produce y deposita en el buzón compartido (`C:\zData\ExtracionDatosIA\.agentic-sync\`) para que un agente especialista lo ejecute. El Handoff contiene TODO lo que el agente necesita para planificar e implementar su trabajo sin necesidad de información adicional.

### Principios fundamentales:
1. **Autosuficiencia** — El Handoff debe ser ejecutable por el agente sin preguntar al Humano por contexto adicional.
2. **Aislamiento** — Cada Handoff contiene solo la información relevante para su rol. No filtra detalles de otros roles.
3. **Trazabilidad** — Cada Handoff referencia la HU, los CAs, la Gobernanza y la iteración de origen.
4. **Verificabilidad** — Cada Handoff define criterios de éxito medibles que el Arquitecto puede auditar.

---

## 2. Nomenclatura de Archivos

### 2.1 Handoffs de delegación
```
handoff_{rol}_{HU-ID}_{CA-IDs}.md
```

**Ejemplos:**
```
handoff_backend_HU01_CA01-CA05-CA06.md
handoff_frontend_HU01_CA01-CA02-CA03.md
handoff_qa_HU01_CA01-CA13.md
```

### 2.2 Solicitudes de aprobación (generadas por los agentes)
```
approval_request_{rol}.md
```

### 2.3 Violaciones de arquitectura
```
architecture_violation_{HU-ID}.md
```

### 2.4 Matriz de cobertura
```
coverage_matrix.md
```

### 2.5 Acta de cierre
```
cierre_iteracion_{iteracion}_{HU-ID}.md
```

---

## 3. Estructura Formal del Handoff

Todo Handoff DEBE contener las siguientes secciones en este orden exacto. Las secciones marcadas con `[OBLIGATORIO]` no pueden omitirse.

---

### Sección 1: Metadatos [OBLIGATORIO]

```markdown
# Handoff — {ROL} — {HU-ID}
## Iteración: {nombre_iteración}

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_{rol}_{HU-ID}_{CAs}.md`                  |
| **Rol Destino**          | Agente {Backend|Frontend|QA}                       |
| **HU de Origen**         | HU-{XX} — {Título de la HU}                       |
| **CAs Asignados**        | CA-{XX}, CA-{YY}, CA-{ZZ}                          |
| **CAs Excluidos**        | CA-{WW} (Motivo: {justificación de exclusión})     |
| **Rama Git**             | `{nombre_de_rama}`                                 |
| **Iteración**            | {nombre_iteración}                                 |
| **Fecha de Generación**  | {YYYY-MM-DD HH:MM}                                |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)              |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                |
```

### Sección 2: Alineación Arquitectónica [OBLIGATORIO]

Esta sección confirma que el trabajo delegado respeta la Gobernanza Tecnológica del proyecto.

```markdown
## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI 0.115 + SQLAlchemy + Alembic
- [x] Frontend: React 18 + TypeScript + Vite 5
- [x] Estilos: SASS/SCSS (preprocesador) — CSS puro como fallback justificado
- [x] Base de Datos: SQL Server 2019+ (SQLAlchemy ORM)
- [x] SDKs: google-generativeai (Gemini) + boto3 (Textract)
- [x] Cola: Celery 5 + Redis

### Patrón Arquitectónico
- [x] Clean Architecture (Ports & Adapters)
- [x] Capas: Infraestructura → Aplicación → Dominio
- [x] Inversión de Dependencias (Ports/Interfaces en capa dominio)

### Preparación Cloud-Ready
- [x] Adapters reemplazables sin cambiar dominio
- [x] Variables de entorno externalizadas (.env)
- [x] CERO credenciales hardcodeadas

### ISO/IEC 25010
- [x] Mantenibilidad: Modularidad, modificabilidad, testeabilidad
- [x] Seguridad: JWT + RBAC + aislamiento de contexto IA
- [x] Eficiencia de Desempeño: Paginación, índices, async/Celery

### Riesgos Identificados
> Documentar riesgos arquitectónicos específicos para este Handoff.
> Referencia: Sección de Riesgos de PO_Skills.md (R-01 a R-07)
```

### Sección 3: Contexto de la Historia de Usuario [OBLIGATORIO]

```markdown
## Historia de Usuario — Contexto

> **Como** {rol del usuario},
> **Quiero** {acción que desea realizar},
> **Para que** {beneficio esperado}.

### Descripción Funcional
{Resumen conciso de la funcionalidad descrita en la HU, filtrado SOLO a lo relevante para este rol}
```

### Sección 4: Criterios de Aceptación Asignados [OBLIGATORIO]

Copiar textualmente el contenido Gherkin de cada CA asignado desde la HU original.

```markdown
## Criterios de Aceptación

### CA-{XX} — {Título del CA}
```gherkin
{Copiar contenido Gherkin íntegro de la HU}
```

**Notas de implementación para el agente:**
> {Indicaciones técnicas específicas del Arquitecto: endpoints a usar, tablas involucradas, 
> componentes React esperados, etc. Esta es la sección donde el Arquitecto agrega valor 
> interpretando el CA para el rol específico}
```

### Sección 5: Especificaciones Técnicas por Rol [OBLIGATORIO]

El contenido de esta sección varía según el rol destino:

#### Para Handoff Backend:
```markdown
## Especificaciones Técnicas — Backend

### Estructura de Directorios
> Referencia: Gobernanza §2.2 — Estructura de directorios obligatoria del Backend
{Listar archivos a crear/modificar con rutas absolutas}

### Endpoints API REST
| Método | Ruta                  | Descripción            | Auth    |
|--------|-----------------------|------------------------|---------|
| {HTTP} | `/api/v1/{recurso}`   | {Descripción}          | {roles} |

### Schemas Pydantic (Entrada/Salida)
{Definir los schemas con campos, tipos y validaciones}

### Modelo de Datos (SQLAlchemy)
{Tablas involucradas, relaciones, columnas de auditoría}

### Integraciones SDK
> Si aplica: documentar llamadas a Google Gemini o AWS Textract
{Adapter a usar, parámetros, manejo de errores}

### Reglas de Negocio
{Listar reglas de dominio que el agente debe implementar}
```

#### Para Handoff Frontend:
```markdown
## Especificaciones Técnicas — Frontend

### Estructura de Directorios
> Referencia: Gobernanza §4.1 — Estructura de directorios obligatoria del Frontend
{Listar componentes a crear/modificar con rutas absolutas}

### Componentes React
| Componente           | Ubicación                        | Props principales        |
|----------------------|----------------------------------|--------------------------|
| {NombreComponente}   | `src/components/{area}/{File}`   | {props tipadas}          |

### Endpoints a Consumir (del Backend)
| Método | Ruta                  | Descripción            | Schema Respuesta   |
|--------|-----------------------|------------------------|--------------------|
| {HTTP} | `/api/v1/{recurso}`   | {Descripción}          | `APIResponse<T>`   |

### TypeScript Interfaces (Espejo de Schemas Pydantic)
{Definir interfaces que corresponden a los schemas del Backend}

### Estado Global (Zustand)
{Si aplica: stores a crear o modificar}

### Referencia de Mockups
> Si existen mockups textuales en `C:\zData\ExtracionDatosIA\HU\HU-Mockups\`, 
> referenciarlos aquí con ruta absoluta.
> Si existen mockups imágenes PNG en `C:\zData\ExtracionDatosIA\Mockups\`,
> el agente Frontend DEBE leerlos e interpretarlos como la referencia visual
> OBLIGATORIA para la maquetación de componentes.

### Estilos SASS/SCSS
> Referencia: Gobernanza §4.3 — Estándares de estilos del Frontend

| Elemento | Convención |
|----------|------------|
| Preprocesador | SASS/SCSS (instalado vía `sass` en `devDependencies`) |
| Entry point | `src/styles/main.scss` — importa todos los parciales |
| Variables | `src/styles/_variables.scss` — Design tokens (colores, tipografía, espaciado, bordes, sombras) |
| Mixins | `src/styles/_mixins.scss` — Reutilizables (responsive breakpoints, animaciones, flexbox helpers) |
| Reset | `src/styles/_reset.scss` — Normalize/reset base |
| Tipografía | `src/styles/_typography.scss` — Sistema tipográfico (fuentes, tamaños, pesos) |
| Layout | `src/styles/_layout.scss` — Grid system, contenedores, espaciado global |
| Componentes | `ComponentName.module.scss` junto al `.tsx` — Estilos modulares con CSS Modules |
| Nombrado clases | kebab-case (`class="card-header"`) |
| Nesting máximo | 3 niveles de profundidad (evitar over-nesting) |
| !important | PROHIBIDO (excepto overrides de librerías externas justificados) |
| Inline styles | PROHIBIDO en componentes React |
| CSS-in-JS | NO PERMITIDO — todo se maneja vía SCSS modules o SCSS global |

#### Estructura de archivos SCSS:
```
FrontEnd/src/styles/
├── _variables.scss       ← $color-primary, $font-family-base, $spacing-unit, $border-radius...
├── _mixins.scss          ← @mixin respond-to($breakpoint), @mixin flex-center, @mixin transition...
├── _reset.scss           ← box-sizing, margin, padding, font reset
├── _typography.scss      ← h1-h6, p, .text-{size}, .font-{weight}
├── _layout.scss          ← .container, .grid, .flex-row, .flex-col
└── main.scss             ← @use 'variables'; @use 'mixins'; @use 'reset'; ...

FrontEnd/src/components/{area}/
├── ComponentName.tsx
└── ComponentName.module.scss
```
```

#### Para Handoff QA:
```markdown
## Especificaciones Técnicas — QA

### Estrategia de Testing
| Tipo de Test     | Herramienta          | Alcance                       |
|------------------|----------------------|-------------------------------|
| Unitario Backend | pytest + pytest-asyncio | Servicios de dominio        |
| Unitario Frontend| Vitest + RTL         | Componentes críticos          |
| Integración API  | pytest + TestClient  | Endpoints REST                |
| E2E (si aplica)  | Playwright           | Flujos principales            |

### Casos de Prueba por CA
{Para cada CA asignado, definir los escenarios de test específicos}

### Validación ISO/IEC 25010
| Característica        | Verificación requerida                          |
|-----------------------|-------------------------------------------------|
| Mantenibilidad        | {Verificación específica}                       |
| Seguridad             | {Verificación específica}                       |
| Eficiencia Desempeño  | {Verificación específica}                       |

### NFR/QA Strategy
> Referencia a la estrategia NFR/QA proporcionada por el Humano Cartero
{Documentar la estrategia y cómo se mapea a los CAs}

### Cobertura Mínima Requerida
- Backend: ≥80% por servicio de dominio
- Frontend: Componentes críticos (AuthGuard, DocumentViewer, formularios)
```

### Sección 6: Estándares de Código Aplicables [OBLIGATORIO]

```markdown
## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zData\ExtracionDatosIA\Documentancion\Gobernanza_Arquitectura.md`

### Estándares aplicables a este Handoff:
- {Listar secciones específicas de la Gobernanza relevantes para este rol}
- {Ej: §3.1 Nombrado Python, §3.2 Endpoints REST, §3.3 Excepciones, etc.}

### Convención de Commits (Conventional Commits)
```
feat({HU-ID}): {descripción en español}
```
```

### Sección 7: Dependencias y Pre-condiciones [OBLIGATORIO]

```markdown
## Dependencias y Pre-condiciones

### Requiere completado antes:
- [ ] {Listar HUs, CAs o Handoffs previos que deben estar completados}

### Produce entregables para:
- [ ] {Listar qué Handoffs futuros dependen de este trabajo}

### Archivos que NO debe modificar (fuera de su jurisdicción):
- {Listar archivos protegidos para este rol}
```

### Sección 8: Instrucciones Operativas [OBLIGATORIO]

Esta sección es IDÉNTICA en TODOS los Handoffs. No debe modificarse.

```markdown
## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_{ROL}.md`
   
   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_{ROL}.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama {RAMA}. Avísale al Arquitecto."*
```

---

## 4. Reglas de Segmentación por Rol

El Arquitecto Líder segmenta los CAs de una HU según esta matriz de responsabilidad:

| Tipo de trabajo                                   | Agente Responsable |
|---------------------------------------------------|--------------------|
| Endpoints API REST, servicios, repositorios       | **Backend**        |
| Integraciones SDK (Gemini, Textract)              | **Backend**        |
| Workers Celery, colas de procesamiento            | **Backend**        |
| Schemas Pydantic, validaciones de entrada         | **Backend**        |
| Modelos SQLAlchemy, migraciones Alembic           | **Backend**        |
| Excepciones de dominio                            | **Backend**        |
| Componentes React, páginas, vistas                | **Frontend**       |
| Estilos SASS/SCSS, design tokens, mixins          | **Frontend**       |
| Maquetación según Mockups PNG de referencia        | **Frontend**       |
| Hooks personalizados, servicios API (axios)       | **Frontend**       |
| Estado global (Zustand), React Query              | **Frontend**       |
| TypeScript interfaces (espejo schemas)            | **Frontend**       |
| Protección de rutas (AuthGuard), RBAC UI          | **Frontend**       |
| Visor PDF, WebSockets cliente                     | **Frontend**       |
| Tests unitarios (pytest, vitest)                  | **QA**             |
| Tests de integración API                          | **QA**             |
| Tests E2E (Playwright)                            | **QA**             |
| Validación ISO/IEC 25010                          | **QA**             |
| Validación de seguridad (penetración básica)      | **QA**             |
| Validación de cobertura de código                 | **QA**             |

### CAs que generan trabajo dual (Backend + Frontend)
Algunos CAs requieren trabajo en ambos roles. En ese caso, el Arquitecto:
1. Crea un Handoff Backend con la lógica de servidor del CA.
2. Crea un Handoff Frontend con la parte visual/interacción del CA.
3. Indica en ambos Handoffs la dependencia cruzada en la Sección 7.

---

## 5. Reglas de Exclusión Semántica

Cuando el Humano Cartero proporciona un **filtro de exclusión** (ej: "Solo piloto local, excluir AWS Cloud"):

1. El Arquitecto lee cada CA de la HU solicitada.
2. Si la redacción del CA hace referencia semántica a funcionalidad excluida, el CA se descarta.
3. En la tabla de metadatos del Handoff, se documenta cada exclusión:

```markdown
| CA Excluido | Motivo de Exclusión                                           |
|-------------|---------------------------------------------------------------|
| CA-{XX}     | Referencia a {funcionalidad excluida}: "{texto del CA}"       |
```

4. Los CAs excluidos NO aparecen en la Sección 4 del Handoff.

---

## 6. Protocolo de Aprobación

### 6.1 Flujo de aprobación
```
Agente Especialista → approval_request_{ROL}.md → Humano Cartero → Arquitecto Líder
                                                                         ↓
                                                              Evalúa contra Gobernanza
                                                                         ↓
                                                            ┌─ Aprobado → Humano copia texto al agente
                                                            └─ Rechazado → Humano copia observaciones al agente
```

### 6.2 Criterios de evaluación del Arquitecto
El Arquitecto evalúa las solicitudes de aprobación contra:

1. **Adherencia a la Gobernanza** — ¿Respeta el stack, la estructura, los estándares de código?
2. **Clean Architecture** — ¿Las capas están bien separadas? ¿Los adapters son reemplazables?
3. **Cloud-Ready** — ¿La implementación propuesta permitirá migrar a AWS sin cambiar el dominio?
4. **ISO 25010** — ¿Cumple con las subcaracterísticas de calidad aplicables?
5. **Seguridad** — ¿CERO credenciales en código? ¿RBAC en endpoints? ¿JWT correcto?
6. **Convenciones** — ¿Nombrado correcto? ¿Conventional Commits? ¿Docstrings?

### 6.3 Formato de veredicto

**Aprobación:**
```markdown
## ✅ APROBACIÓN — Agente {ROL}

Tu plan ha sido revisado y aprobado por el Arquitecto Líder.

**Observaciones:**
- {Observaciones menores si las hay}

**Autorización:**
Procede a modo `EXECUTION`. Codifica, commitea y pushea a la rama `{RAMA}`.
```

**Rechazo:**
```markdown
## ❌ RECHAZO — Agente {ROL}

Tu plan ha sido revisado y rechazado por el Arquitecto Líder.

**Motivo del rechazo:**
- {Violación específica identificada}

**Acción requerida:**
- {Instrucciones específicas para corregir el plan}

**Reintentos restantes:** {N}/2

Corrige tu plan y genera un nuevo `approval_request_{ROL}.md`.
```

---

## 7. Protocolo de Auditoría Post-Ejecución (Fase 4)

Cuando el Humano avisa que los especialistas hicieron push:

### 7.1 Checklist de auditoría
```markdown
## Auditoría de Código — {HU-ID} — Agente {ROL}

### Gobernanza Técnica
- [ ] Estructura de directorios correcta (§2.2 Backend / §4.1 Frontend)
- [ ] Nombrado de archivos correcto (§3.1 / §4.2)
- [ ] Endpoints siguen convención REST (§3.2)
- [ ] Excepciones de dominio tipadas (§3.3)
- [ ] Logging con logger, sin print() (§3.5)

### Clean Architecture
- [ ] Sin acoplamiento directo entre capas
- [ ] Adapters implementan Ports (interfaces abstractas)
- [ ] Servicios no acceden directamente a la BD (usan Repository)

### Seguridad
- [ ] CERO credenciales hardcodeadas
- [ ] Endpoints protegidos con @require_role
- [ ] .env no commiteado (verificar .gitignore)

### Estilos SASS/SCSS (solo para auditoría de Handoffs Frontend)
- [ ] Estilos escritos en SCSS (no inline styles, no CSS-in-JS)
- [ ] Variables SCSS definidas en _variables.scss (design tokens)
- [ ] Componentes usan CSS Modules (*.module.scss)
- [ ] Nesting SCSS no excede 3 niveles de profundidad
- [ ] Sin !important (excepto overrides justificados de librerías)
- [ ] Maquetación fiel a los Mockups PNG de referencia (si existen)
- [ ] Clases nombradas en kebab-case

### Cloud-Ready
- [ ] Storage vía StoragePort (no rutas hardcodeadas)
- [ ] Configuración via pydantic-settings
- [ ] Sin dependencias a infraestructura local en dominio

### ISO 25010
- [ ] Tests con cobertura ≥80%
- [ ] Docstrings en servicios y funciones de negocio
- [ ] Migraciones Alembic con downgrade()
```

### 7.2 Política de bloqueo
- **Máximo 2 reintentos** por agente antes de escalar formalmente.
- Cada violación se documenta en `architecture_violation_{HU-ID}.md`.
- Si la violación es CRÍTICA (credenciales expuestas, SQL raw en endpoints), se bloquea inmediatamente sin reintentos.

---

## 8. Trazabilidad — Matriz de Cobertura

La matriz de cobertura (`coverage_matrix.md`) se actualiza al cierre de cada iteración:

```markdown
# Matriz de Cobertura — Iteración {nombre_iteración}

| HU    | CA    | Agente    | Estado     | Handoff              | Fecha Cierre |
|-------|-------|-----------|------------|----------------------|--------------|
| HU-01 | CA-01 | Backend   | ✅ Aprobado | handoff_backend_...  | YYYY-MM-DD   |
| HU-01 | CA-01 | Frontend  | ✅ Aprobado | handoff_frontend_... | YYYY-MM-DD   |
| HU-01 | CA-08 | Backend   | ⏳ En curso | handoff_backend_...  | —            |
| HU-01 | CA-16 | —         | ❌ Excluido | — (Motivo: ...)      | —            |
```

**Estados válidos:** `⏳ En curso` | `📋 Planificado` | `🔍 En revisión` | `✅ Aprobado` | `❌ Excluido` | `🚫 Rechazado` | `🔁 Reintento`

---

## 9. Acta de Cierre de Iteración

```markdown
# Acta de Cierre — Iteración {nombre_iteración} — {HU-ID}

## Resumen Ejecutivo
- **CAs ejecutados:** {N}/{M} (porcentaje)
- **CAs excluidos:** {lista con justificación}
- **Rechazos:** {N} (detalle de violaciones)
- **Rama:** `{rama_git}`
- **Fecha de cierre:** {YYYY-MM-DD}

## Validación de Gobernanza
- Stack respetado: ✅/❌
- Clean Architecture respetada: ✅/❌
- Cloud-Ready validado: ✅/❌
- ISO 25010 cumplida: ✅/❌

## Métricas
| Métrica                    | Valor       |
|----------------------------|-------------|
| CAs completados            | {N}         |
| CAs excluidos              | {N}         |
| Aprobaciones a primer intento | {N}      |
| Rechazos                   | {N}         |
| Reintentos totales         | {N}         |
| Violaciones críticas       | {N}         |

## Lecciones Aprendidas
{Documentar mejoras para futuras iteraciones}

## Firma
- **Arquitecto Líder:** Agente Orquestador GRM
- **Fecha:** {YYYY-MM-DD}
```

---

## 10. Changelog del SKILL

| Versión | Fecha       | Autor                | Cambios                                            |
|---------|-------------|----------------------|----------------------------------------------------|
| v1.0.0  | 2026-05-22  | Arquitecto Líder GRM | Versión inicial — Protocolo completo de Handoffs   |
| v1.1.0  | 2026-05-22  | Arquitecto Líder GRM | SASS/SCSS como estándar de estilos Frontend. Mockups PNG como referencia visual obligatoria. Estructura SCSS detallada en Handoff Frontend. Checklist auditoría ampliado con 7 puntos SCSS |

---

*SKILL generado por el Agente Arquitecto Líder (Orquestador) — Proyecto GRM Document Intelligence*  
*Fuente de verdad para la delegación multi-agente estricta*
