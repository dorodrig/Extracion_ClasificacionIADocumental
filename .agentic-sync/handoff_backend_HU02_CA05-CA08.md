# Handoff — Backend — HU-02
## Iteración: 2 -DEV-HU-2

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_backend_HU02_CA05-CA08.md`                          |
| **Rol Destino**          | Agente Backend                                               |
| **HU de Origen**         | HU-02 — Ingesta Dual de Documentos (Escáner/Carpeta)         |
| **CAs Asignados**        | CA-05, CA-06, CA-07, CA-08                                   |
| **CAs Excluidos**        | Ninguno de la selección actual.                              |
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
- [x] Adapters reemplazables sin cambiar dominio — el StoragePort (CA-07) DEBE ser un Adapter
- [x] Variables de entorno externalizadas (.env) — TEMP_DIR configurado desde .env
- [x] CERO credenciales hardcodeadas

### ISO/IEC 25010
- [x] Mantenibilidad: Módulos de manipulación de archivos aislados en Adapters
- [x] Seguridad: JWT + RBAC en todos los endpoints nuevos
- [x] Eficiencia de Desempeño: Operaciones de archivos asíncronas donde sea posible

### Riesgos Identificados
> CA-06 (segmentación PDF) requiere una librería de manipulación PDF. Se DEBE usar `pypdf` (nombre actual del paquete, previamente `PyPDF2`). No usar alternativas fuera del stack aprobado sin autorización del Arquitecto.
> CA-07: La ruta de trabajo temporal NUNCA debe ser hardcodeada. Debe provenir de la variable de entorno `TEMP_DIR` (definida en `.env`) más el patrón `/{batch_id}/{timestamp}/`.

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización,
> **Quiero** seleccionar el modo de ingesta de documentos y enviar los archivos al pipeline,
> **Para que** el sistema inicie automáticamente el flujo de extracción OCR con los documentos correctos.

### Descripción Funcional (filtrado a responsabilidad Backend)
Esta iteración cubre el preprocesamiento real de los archivos: validación de formatos (CA-05), segmentación PDF página por página (CA-06), creación de la ruta de trabajo temporal en disco (CA-07), y provisión de un endpoint de consulta del progreso de la ingesta (CA-08).

## Criterios de Aceptación

### CA-05 — Validación de formatos de archivo en carpeta local
```gherkin
Dado que el sistema lista los archivos de una carpeta seleccionada
Cuando detecta archivos con extensiones no soportadas (ej: .docx, .xlsx, .txt)
Entonces el sistema excluye esos archivos del listado de procesamiento
  Y muestra un aviso informativo: "Se omitieron N archivo(s) con formato no compatible: [lista de archivos]"
  Y continúa el proceso solo con los archivos soportados
```
**Notas de implementación para el agente:**
> Implementar una función de utilidad en `app/domain/rules/document_rules.py` con la lista de extensiones permitidas (`ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif'}`). Esta regla de dominio es reutilizable por otros servicios. El endpoint que recibe la lista de archivos (parte de la confirmación del envío al pipeline) debe invocar esta regla antes de proceder. El resultado de archivos omitidos debe incluirse en la respuesta de la API para que el Frontend lo muestre.

### CA-06 — Segmentación de PDF multi-página antes del procesamiento OCR
```gherkin
Dado que un documento PDF contiene más de una página
Cuando el operario hace clic en "Enviar a Procesamiento"
Entonces el sistema divide automáticamente cada PDF multi-página en páginas individuales
  Y almacena las páginas segmentadas en la ruta de trabajo temporal del sistema
  Y mantiene la referencia de a qué documento padre pertenece cada página segmentada
  Y registra el número total de páginas a procesar en el log de la sesión
```
**Notas de implementación para el agente:**
> Crear `app/services/storage/pdf_splitter.py` que implemente la interfaz `PDFSplitterPort` (definida en `app/domain/ports/pdf_splitter_port.py`). Usar la librería `pypdf` para la segmentación. Cada página resultante debe guardarse como `{batch_id}_doc_{doc_id}_p{page_num}.pdf` dentro de la ruta temporal. La referencia al documento padre (`lote_id`, `documento_id`) debe persistirse en la tabla `documentos_lote` (columna `ruta_temporal` para cada página).

### CA-07 — Generación de ruta de trabajo temporal
```gherkin
Dado que el operario ha enviado los documentos a procesamiento
Cuando el sistema prepara los archivos para el pipeline
Entonces genera una carpeta temporal con la estructura: /temp/{batch_id}/{timestamp}/
  Y copia o mueve los archivos segmentados a esa ruta temporal
  Y asegura que la ruta temporal es accesible por el módulo backend de OCR (HU-03)
  Y registra la ruta temporal en el log de la sesión como parte del batch_id
```
**Notas de implementación para el agente:**
> Crear `app/services/storage/local_storage.py` como implementación del `StoragePort` (ya definido en la arquitectura). Este Adapter crea la carpeta física con `os.makedirs(ruta, exist_ok=True)`. La raíz de la ruta temporal debe venir de `settings.TEMP_DIR` (pydantic-settings desde `.env`). Actualizar la tabla `lotes_procesamiento` con `ruta_temporal` una vez que la carpeta sea creada exitosamente. El endpoint `POST /api/v1/batches/{batch_id}/prepare` activa este proceso.

### CA-08 — Indicador de progreso de ingesta
```gherkin
Dado que el operario ha enviado los documentos a procesamiento
Cuando el sistema procesa y prepara los archivos
Entonces muestra una barra de progreso o indicador de carga con el estado actual
  Y muestra el texto: "Preparando N de M documentos..."
  Y al finalizar la preparación, redirige automáticamente a la pantalla de monitoreo del proceso OCR
```
**Notas de implementación para el agente:**
> Crear endpoint `GET /api/v1/batches/{batch_id}/status` que devuelva el estado actual del lote y el progreso (`documentos_preparados`, `total_documentos`, `estado`). Este endpoint será consultado periódicamente por el Frontend (polling). El campo `estado` en `lotes_procesamiento` ya contempla los valores: `preparando`, `en_proceso`, `completado`, `error`. Actualizar el estado del lote a medida que avanza el preprocesamiento.

## Especificaciones Técnicas — Backend

### Estructura de Directorios
> Referencia: Gobernanza §2.2 — Estructura de directorios obligatoria del Backend

**Archivos NUEVOS a crear:**
```
BackEnd/app/domain/rules/document_rules.py          ← ALLOWED_EXTENSIONS + validar_formato()
BackEnd/app/domain/ports/pdf_splitter_port.py       ← PDFSplitterPort (interfaz abstracta)
BackEnd/app/domain/ports/storage_port.py            ← StoragePort (interfaz abstracta)
BackEnd/app/services/storage/pdf_splitter.py        ← Adapter: implementa PDFSplitterPort con pypdf
BackEnd/app/services/storage/local_storage.py       ← Adapter: implementa StoragePort con os/filesystem
BackEnd/app/services/ingestion_service.py           ← Use Case: orquesta CA-05, CA-06, CA-07
```

**Archivos a MODIFICAR:**
```
BackEnd/app/api/v1/endpoints/batches.py             ← Agregar POST /prepare y GET /status
BackEnd/app/db/repositories/batch_repository.py     ← Agregar métodos update_ruta_temporal, update_estado
BackEnd/app/domain/ports/batch_repository.py        ← Agregar métodos a la interfaz
BackEnd/requirements.txt                            ← Agregar pypdf
```

### Endpoints API REST
| Método | Ruta                                    | Descripción                                         | Auth              |
|--------|-----------------------------------------|-----------------------------------------------------|-------------------|
| POST   | `/api/v1/batches/{batch_id}/prepare`    | Inicia preprocesamiento: validar, segmentar, ruta temporal | `operario`, `admin` |
| GET    | `/api/v1/batches/{batch_id}/status`     | Consulta el estado y progreso actual del lote       | `operario`, `admin` |

### Schemas Pydantic (Entrada/Salida)
**Entrada — POST /prepare:**
```python
class BatchPrepareRequest(BaseModel):
    documentos: list[DocumentoIngestado]  # nombre, extension, ruta_original, pages
    
class DocumentoIngestado(BaseModel):
    nombre_archivo: str
    extension: str  # validado contra ALLOWED_EXTENSIONS
    ruta_original: str
    total_paginas: int | None = None
```

**Salida — GET /status:**
```python
class BatchStatusResponse(BaseModel):
    batch_id: str
    estado: str  # 'preparando' | 'en_proceso' | 'completado' | 'error'
    documentos_preparados: int
    total_documentos: int
    ruta_temporal: str | None
    archivos_omitidos: list[str]  # extensiones inválidas detectadas
```

### Modelo de Datos (SQLAlchemy)
- Tabla `lotes_procesamiento`: actualizar `ruta_temporal`, `estado`, `total_docs`, `total_paginas`
- Tabla `documentos_lote`: actualizar `ruta_temporal` (ruta de páginas individuales), `total_paginas`, `estado`

### Reglas de Negocio
1. `ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif'}` — definidas en la capa de dominio
2. Si TODOS los documentos son inválidos, retornar error 422 con detalle
3. La segmentación PDF solo aplica a archivos PDF con `total_paginas > 1`
4. JPG/PNG/TIFF se tratan como página única (no se segmentan)
5. La ruta temporal es: `{settings.TEMP_DIR}/{batch_id}/{timestamp}/`
6. Loggear cada etapa con `logger.info()` — NUNCA `print()`

## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\Documentancion\Gobernanza_Arquitectura.md`

### Estándares aplicables a este Handoff:
- §3.1 Nombrado Python: snake_case funciones, PascalCase clases, SCREAMING_SNAKE_CASE constantes
- §3.2 Endpoints REST: `/api/v1/` + sustantivos plurales + `APIResponse` wrapper obligatorio
- §3.3 Excepciones: jerarquía `GRMException` — crear `InvalidDocumentFormatException`, `PDFSplittingException`, `StorageException`
- §3.4 Seguridad: `@require_role` en todos los endpoints, TEMP_DIR desde `.env`
- §3.5 Logging: `logger = logging.getLogger("grm.ingestion")` — NUNCA `print()`

### Convención de Commits (Conventional Commits)
```
feat(HU-02): descripción en español
```

## Dependencias y Pre-condiciones

### Requiere completado antes:
- [x] Backend HU-02 CA-01 a CA-04 (batch_id ya existe al crear el lote — ✅ completado en Iteración 1)
- [ ] HU-10 (tablas `lotes_procesamiento` y `documentos_lote` con todas las columnas)

### Produce entregables para:
- [ ] Handoff Frontend HU-02 CA-05/CA-08 (consume `/prepare` y `/status`)
- [ ] Handoff Backend HU-03 (AWS Textract consume la ruta temporal generada en CA-07)

### Archivos que NO debe modificar (fuera de su jurisdicción):
- Cualquier archivo en `FrontEnd/`
- Mockups y documentación en `HU/`

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Backend.md`

   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_Backend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU2_CA1-CA4_DevDamian_ITEREACION1. Avísale al Arquitecto."*
