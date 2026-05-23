# Handoff — Frontend — HU-02
## Iteración: 2 -DEV-HU-2

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_frontend_HU02_CA05-CA08.md`                         |
| **Rol Destino**          | Agente Frontend                                              |
| **HU de Origen**         | HU-02 — Ingesta Dual de Documentos (Escáner/Carpeta)         |
| **CAs Asignados**        | CA-05, CA-08                                                 |
| **CAs Excluidos**        | CA-06 (segmentación PDF — lógica exclusiva de servidor, sin interacción UI), CA-07 (creación de carpeta temporal — lógica exclusiva de servidor, sin interacción UI directa) |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`                          |
| **Iteración**            | 2 -DEV-HU-2                                                  |
| **Fecha de Generación**  | 2026-05-23 12:24                                             |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)                        |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                          |

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
- [x] Mantenibilidad: Componentes reutilizables y tipados
- [x] Seguridad: JWT en todas las llamadas axios
- [x] Eficiencia de Desempeño: Polling optimizado para CA-08 (evitar polling excesivo)

### Riesgos Identificados
> CA-08 usa polling al endpoint `GET /api/v1/batches/{batch_id}/status`. Implementar con un intervalo razonable (1-2 segundos) usando `setInterval` limpiado correctamente en `useEffect` cleanup para evitar memory leaks.

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización,
> **Quiero** ver avisos claros sobre archivos incompatibles y un indicador de progreso durante la preparación,
> **Para que** tenga visibilidad del estado del proceso sin intervención manual adicional.

### Descripción Funcional (filtrado a responsabilidad Frontend)
- **CA-05**: Cuando el Backend responde con archivos omitidos (extensiones inválidas), el Frontend debe mostrar el aviso informativo correspondiente en la UI del `FolderModule`.
- **CA-08**: Al confirmar el envío (`POST /api/v1/batches/{batch_id}/prepare`), mostrar una barra de progreso o spinner con el texto "Preparando N de M documentos..." consultando periódicamente el endpoint de status. Al completarse, redirigir al panel de monitoreo OCR.

> **NOTA IMPORTANTE:** El filtrado de extensiones se realiza en el Frontend (ya implementado en Iteración 1 del `FolderModule`) Y se valida también en el Backend. El Frontend en CA-05 debe manejar la respuesta del Backend si retorna archivos omitidos adicionales que no fueron capturados localmente.

## Criterios de Aceptación

### CA-05 — Validación de formatos de archivo en carpeta local (responsabilidad UI)
```gherkin
Dado que el sistema lista los archivos de una carpeta seleccionada
Cuando detecta archivos con extensiones no soportadas (ej: .docx, .xlsx, .txt)
Entonces el sistema excluye esos archivos del listado de procesamiento
  Y muestra un aviso informativo: "Se omitieron N archivo(s) con formato no compatible: [lista de archivos]"
  Y continúa el proceso solo con los archivos soportados
```
**Notas de implementación para el agente:**
> El `FolderModule` ya filtra localmente. En esta iteración, el aviso debe integrarse también con la respuesta del Backend cuando el endpoint `/prepare` devuelva `archivos_omitidos`. Crear o mejorar el componente `OmittedFilesAlert` en `src/components/intake/` que reciba la lista y la renderice de forma clara. No usar inline styles — todo en SCSS.

### CA-08 — Indicador de progreso de ingesta
```gherkin
Dado que el operario ha enviado los documentos a procesamiento
Cuando el sistema procesa y prepara los archivos
Entonces muestra una barra de progreso o indicador de carga con el estado actual
  Y muestra el texto: "Preparando N de M documentos..."
  Y al finalizar la preparación, redirige automáticamente a la pantalla de monitoreo del proceso OCR
```
**Notas de implementación para el agente:**
> Crear el componente `IngestionProgress.tsx` en `src/components/intake/`. Al hacer clic en "Confirmar y Enviar", el `DocumentList` llama a `batchService.prepareBatch(batch_id, documentos)`. Mientras el estado sea `preparando` o `en_proceso`, mostrar el indicador consultando `batchService.getBatchStatus(batch_id)` cada 1.5 segundos. Al recibir `estado: 'completado'`, limpiar el intervalo y redirigir. Al recibir `estado: 'error'`, mostrar mensaje de error con opción de reintentar.

## Especificaciones Técnicas — Frontend

### Estructura de Directorios
> Referencia: Gobernanza §4.1 — Estructura de directorios obligatoria del Frontend

**Archivos NUEVOS a crear:**
```
FrontEnd/src/components/intake/OmittedFilesAlert.tsx
FrontEnd/src/components/intake/OmittedFilesAlert.module.scss
FrontEnd/src/components/intake/IngestionProgress.tsx
FrontEnd/src/components/intake/IngestionProgress.module.scss
```

**Archivos a MODIFICAR:**
```
FrontEnd/src/components/intake/DocumentList.tsx     ← Integrar OmittedFilesAlert + llamada a prepare
FrontEnd/src/services/batchService.ts               ← Agregar prepareBatch() y getBatchStatus()
FrontEnd/src/store/batchStore.ts                    ← Agregar estado de progreso
```

### Componentes React
| Componente             | Ubicación                        | Props principales                                 |
|------------------------|----------------------------------|---------------------------------------------------|
| `OmittedFilesAlert`    | `src/components/intake/`         | `omittedFiles: string[]`, `count: number`         |
| `IngestionProgress`    | `src/components/intake/`         | `batchId: string`, `onComplete: () => void`        |

### Endpoints a Consumir (del Backend)
| Método | Ruta                                        | Descripción                           | Schema Respuesta             |
|--------|---------------------------------------------|---------------------------------------|------------------------------|
| POST   | `/api/v1/batches/{batch_id}/prepare`        | Inicia preprocesamiento del lote      | `APIResponse<BatchStatusResponse>` |
| GET    | `/api/v1/batches/{batch_id}/status`         | Consulta progreso del lote            | `APIResponse<BatchStatusResponse>` |

### TypeScript Interfaces (Espejo de Schemas Pydantic)
```typescript
interface BatchStatusResponse {
  batch_id: string;
  estado: 'preparando' | 'en_proceso' | 'completado' | 'error';
  documentos_preparados: number;
  total_documentos: number;
  ruta_temporal: string | null;
  archivos_omitidos: string[];
}

interface BatchPrepareRequest {
  documentos: DocumentoIngestado[];
}

interface DocumentoIngestado {
  nombre_archivo: string;
  extension: string;
  ruta_original: string;
  total_paginas?: number;
}
```

### Estado Global (Zustand)
Modificar `src/store/batchStore.ts` para agregar:
- `batchProgress: { preparados: number; total: number } | null`
- `setBatchProgress: (progress) => void`

### Referencia de Mockups
> **Mockup Textual:** `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\HU\HU-Mockups\MOCKUP-HU-02-Ingesta-Documentos.md`
> **Mockup PNG (OBLIGATORIO):** `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\Mockups\HU-02-Ingesta-Documentos-Desktop.png`
> El agente Frontend DEBE leer e interpretar la imagen PNG como referencia visual OBLIGATORIA.
> La fidelidad visual al mockup es un criterio de aceptación.

### Estilos SASS/SCSS
> Referencia: Gobernanza §4.7 — Estándares SCSS / Design System GRM

**Corrección pendiente de Iteración 1 (OBLIGATORIO en esta iteración):**
Los inline styles detectados en la auditoría de Iteración 1 DEBEN ser migrados a clases SCSS:
- `IntakeDashboard.tsx` L34 → mover a `IntakeDashboard.module.scss`
- `ScannerModule.tsx` L78 → mover a `ScannerModule.module.scss`
- `FolderModule.tsx` L71 → mover a `FolderModule.module.scss`
- `DocumentList.tsx` L37, L64, L100 → mover a `DocumentList.module.scss`

**Nuevos estilos requeridos:**
- `OmittedFilesAlert.module.scss`: estilo de aviso usando `$color-warning` y `rgba($color-warning, 0.1)` para background
- `IngestionProgress.module.scss`: barra de progreso animada usando `$color-primary`, transición CSS

| Elemento | Convención |
|----------|------------|
| Preprocesador | SASS/SCSS |
| Componentes | `ComponentName.module.scss` junto al `.tsx` |
| Inline styles | **PROHIBIDO** — incluyendo corrección de deuda técnica de iteración 1 |

## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\Documentancion\Gobernanza_Arquitectura.md`

### Estándares aplicables a este Handoff:
- §4.2 TypeScript/React: Props tipadas, NUNCA `any`
- §4.3 Llamadas API: axios centralizado con interceptor JWT
- §4.7 SCSS: **Eliminar TODOS los inline styles** de los componentes de Iteración 1

### Convención de Commits (Conventional Commits)
```
feat(HU-02): descripción en español
fix(HU-02): corrección de inline styles (deuda técnica iteración 1)
```

## Dependencias y Pre-condiciones

### Requiere completado antes:
- [x] Frontend HU-02 CA-01 a CA-04 (componentes `FolderModule`, `DocumentList` ya existentes)
- [ ] Backend HU-02 CA-05 a CA-08 (endpoints `/prepare` y `/status` deben estar disponibles)

### Produce entregables para:
- [ ] Handoff QA HU-02 CA-05/CA-08 (para tests de integración UI)

### Archivos que NO debe modificar (fuera de su jurisdicción):
- Cualquier archivo en `BackEnd/`
- Archivos de estilos globales que no sean de la feature de intake

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Incluye la corrección de inline styles de Iteración 1 como tarea explícita.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Frontend.md`

   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Frontend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU2_CA1-CA4_DevDamian_ITEREACION1. Avísale al Arquitecto."*
