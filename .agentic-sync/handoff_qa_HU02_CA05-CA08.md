# Handoff — QA — HU-02
## Iteración: 2 -DEV-HU-2

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_qa_HU02_CA05-CA08.md`                               |
| **Rol Destino**          | Agente QA                                                    |
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
- [x] Estilos: SASS/SCSS
- [x] Base de Datos: SQL Server 2019+
- [x] Cola: Celery 5 + Redis

### ISO/IEC 25010
- [x] Mantenibilidad: Cobertura ≥80%, tests independientes entre sí
- [x] Seguridad: Tests de autenticación en endpoints `/prepare` y `/status`
- [x] Eficiencia: Test de performance en segmentación PDF con archivos de prueba reales

### Riesgos Identificados
> CA-06 requiere archivos PDF reales (o fixtures sintéticos) de múltiples páginas para los tests de integración. El agente QA debe crear fixtures de PDF de prueba que no contengan datos reales de clientes.

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización,
> **Quiero** ver avisos claros sobre archivos incompatibles y un indicador de progreso,
> **Para que** tenga visibilidad completa del estado de preparación del lote.

### Descripción Funcional
Validar el preprocesamiento de documentos: filtrado por formato, segmentación PDF, creación de ruta temporal y progreso de ingesta, tanto en el Backend (lógica de negocio) como en el Frontend (presentación al usuario).

## Criterios de Aceptación

### CA-05 — Validación de formatos de archivo
```gherkin
Dado que el sistema lista los archivos de una carpeta seleccionada
Cuando detecta archivos con extensiones no soportadas (ej: .docx, .xlsx, .txt)
Entonces el sistema excluye esos archivos del listado de procesamiento
  Y muestra un aviso informativo: "Se omitieron N archivo(s) con formato no compatible: [lista de archivos]"
  Y continúa el proceso solo con los archivos soportados
```

### CA-06 — Segmentación de PDF multi-página
```gherkin
Dado que un documento PDF contiene más de una página
Cuando el operario hace clic en "Enviar a Procesamiento"
Entonces el sistema divide automáticamente cada PDF multi-página en páginas individuales
  Y almacena las páginas segmentadas en la ruta de trabajo temporal del sistema
  Y mantiene la referencia de a qué documento padre pertenece cada página segmentada
  Y registra el número total de páginas a procesar en el log de la sesión
```

### CA-07 — Generación de ruta de trabajo temporal
```gherkin
Dado que el operario ha enviado los documentos a procesamiento
Cuando el sistema prepara los archivos para el pipeline
Entonces genera una carpeta temporal con la estructura: /temp/{batch_id}/{timestamp}/
  Y copia o mueve los archivos segmentados a esa ruta temporal
  Y asegura que la ruta temporal es accesible por el módulo backend de OCR (HU-03)
  Y registra la ruta temporal en el log de la sesión como parte del batch_id
```

### CA-08 — Indicador de progreso de ingesta
```gherkin
Dado que el operario ha enviado los documentos a procesamiento
Cuando el sistema procesa y prepara los archivos
Entonces muestra una barra de progreso o indicador de carga con el estado actual
  Y muestra el texto: "Preparando N de M documentos..."
  Y al finalizar la preparación, redirige automáticamente a la pantalla de monitoreo del proceso OCR
```

## Especificaciones Técnicas — QA

### Estrategia de Testing

| Tipo de Test       | Herramienta             | Alcance                                                      |
|--------------------|-------------------------|--------------------------------------------------------------|
| Unitario Backend   | pytest + pytest-asyncio | `document_rules.py`, `pdf_splitter.py`, `local_storage.py`, `ingestion_service.py` |
| Integración API    | pytest + TestClient     | `POST /api/v1/batches/{batch_id}/prepare`, `GET /api/v1/batches/{batch_id}/status` |
| Unitario Frontend  | Vitest + RTL            | `OmittedFilesAlert`, `IngestionProgress`, polling logic      |
| E2E (si aplica)    | Playwright              | Flujo completo: selección carpeta → omitidos → progreso → completado |

### Casos de Prueba por CA

#### CA-05 — Backend: Validación de formatos
| Test ID | Escenario | Entrada | Resultado Esperado |
|---------|-----------|---------|-------------------|
| T-05-B-01 | Solo archivos válidos | `[doc.pdf, img.jpg, scan.png]` | Sin omitidos, 3 procesados |
| T-05-B-02 | Mix válidos e inválidos | `[doc.pdf, reporte.xlsx, foto.jpg, carta.docx]` | 2 procesados, 2 omitidos |
| T-05-B-03 | Solo inválidos | `[reporte.xlsx, carta.docx]` | Error 422, 0 procesados |
| T-05-F-01 | Alerta visible en UI | Backend retorna `archivos_omitidos: ["carta.docx"]` | `OmittedFilesAlert` renderiza con cuenta 1 |
| T-05-F-02 | Sin omitidos | Backend retorna `archivos_omitidos: []` | `OmittedFilesAlert` NO renderiza |

#### CA-06 — Backend: Segmentación PDF
| Test ID | Escenario | Entrada | Resultado Esperado |
|---------|-----------|---------|-------------------|
| T-06-B-01 | PDF 1 página | PDF fixture 1 página | No se segmenta, se copia como página única |
| T-06-B-02 | PDF 3 páginas | PDF fixture 3 páginas | 3 archivos generados en ruta temporal |
| T-06-B-03 | Imagen JPG | Archivo JPG | Tratado como página única, sin segmentación |
| T-06-B-04 | PDF corrupto | Archivo PDF inválido | Excepción `PDFSplittingException` correctamente manejada |
| T-06-B-05 | Referencia padre | PDF 3 páginas con `doc_id=5` | Cada página tiene referencia a `lote_id` y `documento_id=5` |

#### CA-07 — Backend: Ruta temporal
| Test ID | Escenario | Resultado Esperado |
|---------|-----------|-------------------|
| T-07-B-01 | Creación exitosa | Carpeta `{TEMP_DIR}/{batch_id}/{timestamp}/` existe en filesystem |
| T-07-B-02 | Persistencia en BD | Campo `ruta_temporal` en `lotes_procesamiento` actualizado |
| T-07-B-03 | TEMP_DIR desde settings | `settings.TEMP_DIR` usada, NUNCA ruta hardcodeada |
| T-07-B-04 | Permisos de escritura | Si carpeta no puede crearse → `StorageException` con log de error |

#### CA-08 — Backend + Frontend: Progreso
| Test ID | Escenario | Resultado Esperado |
|---------|-----------|-------------------|
| T-08-B-01 | Estado inicial | `GET /status` retorna `estado: 'preparando'` al crear el lote |
| T-08-B-02 | Estado completado | `GET /status` retorna `estado: 'completado'` tras preparar todos los docs |
| T-08-B-03 | Autenticación requerida | `GET /status` sin JWT → 401 Unauthorized |
| T-08-F-01 | Polling activo | Componente `IngestionProgress` llama al endpoint cada 1.5s mientras `estado != 'completado'` |
| T-08-F-02 | Redirección al completar | Al recibir `estado: 'completado'`, se invoca `onComplete()` |
| T-08-F-03 | Limpieza de intervalo | Al desmontar el componente, `clearInterval` es invocado (no memory leak) |

### Validación ISO/IEC 25010

| Característica        | Verificación requerida                                             |
|-----------------------|--------------------------------------------------------------------|
| Mantenibilidad        | Cobertura ≥80% en `ingestion_service.py`, `pdf_splitter.py`, `local_storage.py` |
| Seguridad             | Endpoints `/prepare` y `/status` requieren JWT válido + rol `operario` o `admin` |
| Eficiencia Desempeño  | Segmentación de PDF de 10 páginas debe completarse en < 5 segundos |
| Integrabilidad        | `StoragePort` y `PDFSplitterPort` son interfaces abstractas correctamente definidas |

### Cobertura Mínima Requerida
- Backend `document_rules.py`: 100% (lógica de dominio crítica)
- Backend `ingestion_service.py`: ≥80%
- Backend `pdf_splitter.py`: ≥80%
- Backend `local_storage.py`: ≥80%
- Frontend `IngestionProgress.tsx`: Casos principales de polling y redirección
- Frontend `OmittedFilesAlert.tsx`: Render condicional

### Fixtures de Prueba Requeridos
```
tests/fixtures/
├── sample_single_page.pdf    ← PDF 1 página (sin datos reales)
├── sample_multi_page.pdf     ← PDF 3 páginas (sin datos reales)
├── sample_image.jpg          ← Imagen JPG de prueba
├── sample_corrupt.pdf        ← PDF corrupto para test de error
└── sample_invalid.docx       ← Archivo no soportado
```

## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\Documentancion\Gobernanza_Arquitectura.md`

### Convención de Commits (Conventional Commits)
```
test(HU-02): descripción en español
```

## Dependencias y Pre-condiciones

### Requiere completado antes:
- [ ] Backend HU-02 CA-05 a CA-08 completado y en rama
- [ ] Frontend HU-02 CA-05/CA-08 completado y en rama

### Archivos que NO debe modificar:
- Código de producción en `BackEnd/app/` o `FrontEnd/src/` (solo archivos de test)

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA y los casos de prueba definidos.
   - Identifica fixtures necesarios.
   - Estima el esfuerzo por suite de tests.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero.

3. **Guarda tu solicitud de revisión** en:
   `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_QA.md`

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\.agentic-sync\approval_request_QA.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.**

6. **En modo `EXECUTION`:**
   - Crea los fixtures y los tests siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` y `git push` a la rama indicada.

7. **Al terminar:**
   - Genera un `walkthrough.md` con resumen de cobertura obtenida.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU2_CA1-CA4_DevDamian_ITEREACION1. Avísale al Arquitecto."*
