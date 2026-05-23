# Handoff — Backend — HU-05
## Iteración: 3 -DEV-HU-5

| Campo                    | Valor                                                        |
|--------------------------|--------------------------------------------------------------|
| **Archivo**              | `handoff_backend_HU05_CA01-CA13.md`                          |
| **Rol Destino**          | Agente Backend                                               |
| **HU de Origen**         | HU-05 — Agente de Clasificación IA (Google Gemini)           |
| **CAs Asignados**        | CA-01 a CA-13                                                |
| **CAs Excluidos**        | Ninguno                                                      |
| **Rama Git**             | `HU2_CA1-CA4_DevDamian_ITEREACION1`                          |
| **Iteración**            | 3 -DEV-HU-5                                                  |
| **Fecha de Generación**  | 2026-05-23                                                   |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)                        |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md                          |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI 0.115 + SQLAlchemy + Alembic
- [x] Frontend: N/A (Proceso de fondo)
- [x] Estilos: N/A
- [x] Base de Datos: SQL Server 2019+
- [x] Cola: Celery 5 + Redis
- [x] SDKs: google-generativeai

### Patrón Arquitectónico
- [x] Clean Architecture (Ports & Adapters)
- [x] Capas: Infraestructura → Aplicación → Dominio
- [x] Inversión de Dependencias (Uso de `StoragePort` existente para interactuar con FS)

### Preparación Cloud-Ready
- [x] Adapters reemplazables sin cambiar dominio (Storage local reemplazable por S3)
- [x] Variables de entorno externalizadas (.env)
- [x] CERO credenciales hardcodeadas (Gemini API Key via env)

### ISO/IEC 25010
- [x] Mantenibilidad: Aislamiento del agente IA en `services/ai_agents/`
- [x] Seguridad: Aislamiento de contexto por documento
- [x] Eficiencia: Procesamiento en background vía Worker (simulado si Celery aún no está full implementado)

### Riesgos Identificados
> R-01: Fallo de concurrencia al crear carpetas si múltiples workers procesan al mismo tiempo. Debe mitigarse usando `os.makedirs(exist_ok=True)`.
> R-02: Fallos en el SDK de Gemini por cuotas o timeout. Implementar lógica de reintentos.

## Historia de Usuario — Contexto

> **Como** Sistema de automatización GRM,
> **Quiero** que el Agente de Clasificación IA tome el Paquete de Datos Limpios del Agente de Contexto y ejecute dos acciones coordinadas: poblar la base de datos del cliente con los campos extraídos Y organizar físicamente los documentos en la carpeta de salida según el patrón de la regla de trabajo,
> **Para que** al final del pipeline todos los documentos del lote estén correctamente clasificados.

### Descripción Funcional
El agente tomará datos ya extraídos, usará Gemini para resolver ambigüedades en la asignación al patrón de la carpeta (ej. `/{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/{NOMBRE_ARCHIVO}`), creará las carpetas, moverá el documento y registrará todo en la base de datos de manera atómica (UPSERT).

## Criterios de Aceptación

### CA-01 — Recepción del Paquete de Datos Limpios
```gherkin
Dado que el Agente de Contexto (HU-04) ha generado un Paquete de Datos Limpios con datos_completos = true
Cuando el Agente de Clasificación recibe el paquete
Entonces verifica que el paquete contiene: documento_id, campos_extraidos con todos los campos obligatorios, tipo_documento_detectado y regla_id
  Y si el paquete está incompleto o malformado, registra el error y devuelve el documento a la cola de revisión humana
  Y NO procede con la clasificación si el paquete es inválido
```
> **Nota del Arquitecto:** Para esta iteración aislada de HU-05, debes crear un esquema (Pydantic) `CleanDataPackage` que actúe como contrato de entrada. Como HU-04 no está, deberás mockear la entrada para las pruebas locales.

### CA-02 — Construcción de la ruta de destino usando el patrón de la regla
```gherkin
Dado que el agente tiene el paquete de datos limpios y la regla de trabajo activa con su patrón de carpeta
Cuando el agente construye la ruta de destino del documento
Entonces reemplaza cada variable del patrón por el valor correspondiente del campo extraído:
    Ejemplo: patrón "/{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/{NOMBRE_ARCHIVO}"
    → "/CC123456789/DAVID_RODRIGUEZ/PAGARE/pagare_001.pdf"
  Y sanitiza los valores para uso en rutas de archivo (elimina caracteres especiales, espacios por guión bajo)
  Y si un valor del patrón está vacío o nulo, usa el placeholder "SIN_DATO" en la ruta
```

### CA-03 — Uso de Google Gemini para razonamiento sobre el patrón de organización
```gherkin
Dado que el agente debe resolver ambigüedades en la asignación de valores a variables del patrón
Cuando el valor de un campo puede interpretarse de múltiples formas (ej: nombres con abreviaciones, CC con formatos variados)
Entonces el agente invoca Google Gemini con el contexto del paquete de datos limpios y el patrón de carpeta
  Y Gemini determina el valor normalizado más apropiado para cada variable del patrón
  Y el agente registra el razonamiento de Gemini en el log de trazabilidad del documento
```

### CA-04 — Creación física de carpetas en el sistema de archivos local
```gherkin
Dado que la ruta de destino ha sido calculada correctamente
Cuando el agente procede con la organización física del documento
Entonces crea recursivamente todas las carpetas del path de destino que no existan aún
  Y si una carpeta del path ya existe, la reutiliza sin eliminar su contenido previo
  Y si ocurre un error de permisos al crear la carpeta, registra el error y marca el documento como "Error de Escritura"
```
> **Nota del Arquitecto:** Usa el `StoragePort` y `local_storage.py` (creado en HU-02 CA-07) agregando los métodos faltantes para soportar estas operaciones si es necesario.

### CA-05 — Copia del documento a la ruta de destino final
```gherkin
Dado que la estructura de carpetas de destino ha sido creada exitosamente
Cuando el agente mueve el documento a su ruta de destino
Entonces copia el documento original (PDF/imagen) a la ruta de destino calculada
  Y verifica que el archivo copiado no está corrupto (comparación de tamaño o hash MD5)
  Y registra en BD la ruta_destino_final del documento
  Y si la verificación de integridad falla, registra el error y retiene el original sin eliminarlo
```

### CA-06 — Persistencia de datos extraídos en la base de datos del cliente
```gherkin
Dado que el documento ha sido clasificado y copiado a su ruta de destino exitosamente
Cuando el agente guarda los datos en BD
Entonces inserta un registro en la tabla documentos_clasificados con:
    - cliente_id, batch_id, regla_id, documento_id
    - Todos los campos extraídos con sus valores (como columnas o JSON según el schema)
    - ruta_destino_final
    - tipo_documento
    - timestamp_clasificacion
  Y si ya existe un registro para el mismo documento (reprocesamiento), lo actualiza (UPSERT) sin duplicar
```
> **Nota del Arquitecto:** Debes crear el modelo SQLAlchemy `DocumentoClasificado` en `app/db/models/` y la migración correspondiente si no existe.

### CA-07 — Agrupación inteligente de múltiples documentos de la misma persona
```gherkin
Dado que el lote contiene múltiples documentos que pertenecen a la misma persona (mismo CC)
Cuando el agente procesa cada documento del lote
Entonces agrupa automáticamente todos los documentos de la misma persona bajo el mismo directorio raíz (/{CC}/{NOMBRE}/)
  Y crea subdirectorios por tipo de documento dentro del directorio de la persona
  Y no crea directorios duplicados si el directorio de la persona ya existe de un procesamiento previo
```

### CA-08 — Manejo de nombres de archivo duplicados en la ruta de destino
```gherkin
Dado que el agente intenta copiar un documento a una ruta donde ya existe un archivo con el mismo nombre
Cuando detecta el conflicto de nombre
Entonces renombra el nuevo archivo agregando un sufijo incremental: pagare.pdf → pagare_001.pdf → pagare_002.pdf
  Y registra el renombramiento en el log de auditoría con: nombre original, nombre final, ruta destino
  Y notifica el evento al operario como una advertencia en el resumen del lote
```

### CA-09 — Actualización del estado del documento en el pipeline
```gherkin
Dado que el Agente de Clasificación completa exitosamente la organización y persistencia de un documento
Cuando actualiza el estado en la tabla de seguimiento
Entonces marca el documento con estado "Clasificado Exitosamente" en documentos_lote
  Y registra en la tabla log_proceso: documento_id, paso="clasificacion_completada", timestamp, agente="clasificacion", resultado="exitoso"
  Y el documento queda disponible para consulta en el portal web del cliente (HU-07)
```

### CA-10 — Generación del resumen de clasificación del lote
```gherkin
Dado que el agente ha procesado todos los documentos del lote
Cuando el último documento del lote ha sido clasificado o ha sido marcado para revisión
Entonces genera un resumen del lote con:
    - Total documentos clasificados exitosamente
    - Total documentos enviados a revisión humana
    - Total documentos con error
    - Estructura de carpetas creada (árbol de directorios)
    - Tiempo total de procesamiento del lote
  Y persiste el resumen en la tabla lotes_procesamiento con estado final
  Y notifica al operario que el lote ha concluido su procesamiento automático
```

### CA-11 — Ejecución de instrucción correctiva enviada por el operario (reprocesamiento)
```gherkin
Dado que el operario ha corregido un documento en revisión humana y ha enviado una instrucción clara al agente (HU-06)
Cuando el Agente de Clasificación recibe la instrucción correctiva
Entonces reinterpreta el documento con el contexto de la instrucción adicional del operario
  Y vuelve a ejecutar el flujo desde el paso CA-02 (construcción de ruta) con los datos corregidos
  Y registra en el log de auditoría: documento_id, instrucción del operario, timestamp de reprocesamiento, resultado final
  Y si el reprocesamiento es exitoso, mueve el documento de la cola de pendientes a "Clasificado"
```

### CA-12 — Manejo de error de escritura en sistema de archivos
```gherkin
Dado que el agente intenta crear carpetas o copiar archivos al sistema de archivos local
Cuando ocurre un error de permisos, disco lleno o ruta inaccesible
Entonces registra el error en el log de auditoría con: ruta intentada, tipo de error, timestamp
  Y marca el documento como "Error de Escritura" en documentos_lote
  Y mueve el documento a la cola de revisión humana con descripción del error
  Y NO elimina el archivo original del lote
```

### CA-13 — Trazabilidad completa del documento procesado
```gherkin
Dado que un documento ha sido procesado por el Agente de Clasificación (exitosamente o con error)
Cuando el agente finaliza su procesamiento para ese documento
Entonces el registro completo del documento en BD incluye:
    - Ruta original del documento fuente
    - Ruta temporal usada en el pipeline
    - Ruta de destino final
    - Todos los campos extraídos con valores y confianza
    - Timestamps de cada etapa: ingesta, OCR, contexto IA, clasificación
    - Estado final del documento
  Y este registro es la fuente de verdad para el portal web del cliente (HU-07)
```

## Especificaciones Técnicas — Backend

### Estructura de Directorios
Archivos a crear/modificar:
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\ai_agents\classification_agent.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\schemas\ai_agents.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\domain\ports\gemini_port.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\ai_agents\gemini_adapter.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\db\models\documentos_clasificados.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\db\repositories\clasificacion_repository.py`
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\services\storage\local_storage.py` (Actualizar)
- `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\BackEnd\app\domain\ports\storage_port.py` (Actualizar)

### Modelo de Datos (SQLAlchemy)
Crear la tabla `documentos_clasificados` de acuerdo a las Notas Técnicas de la HU-05 (JSON para campos_json, soporte de UPSERT). Si falta el modelo `documentos_lote` base, créalo mínimamente para asegurar las Foreing Keys, o usa relaciones simples por ID mientras tanto.

### Integraciones SDK
- **Google Gemini SDK:** Implementar llamadas estructurales (Structured Outputs) pidiendo a Gemini que devuelva el razonamiento de ambigüedad y las variables clave del patrón resueltas. 
- La inyección de la API KEY debe ser via `settings.gemini_api_key`.

### Reglas de Negocio
- Sanitización obligatoria de nombres de archivos y rutas: Sin acentos, sin caracteres especiales (solo alfanuméricos y guiones `_`, `-`).
- Duplicados en almacenamiento resueltos vía sufijo numérico progresivo (`_001`, `_002`).
- UPSERT en BD si un `documento_id` es procesado dos veces (CA-11).

## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zproyecto\extraccion\Extracion_ClasificacionIADocumental\Documentancion\Gobernanza_Arquitectura.md`

### Estándares aplicables a este Handoff:
- §3.1 Nombrado Python (`snake_case`, etc.)
- §3.3 Excepciones (`GRMException`)
- §3.4 Configuración de entorno (`pydantic-settings`)
- §3.5 Logging (Logger `grm.classification_agent`)

### Convención de Commits (Conventional Commits)
```
feat(HU-05): agente clasificador base con soporte gemini
```

## Dependencias y Pre-condiciones

### Requiere completado antes:
- [x] StoragePort base (HU-02)

### Produce entregables para:
- [ ] Tareas asíncronas en Celery (HU-05)
- [ ] Consultas de Portal Cliente (HU-07)

### Archivos que NO debe modificar (fuera de su jurisdicción):
- Frontend components.

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
