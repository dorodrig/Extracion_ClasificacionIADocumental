# HU-03 — Integración AWS Textract: Extracción OCR Página por Página

## Metadatos

| Campo                        | Valor                                                              |
| ---------------------------- | ------------------------------------------------------------------ |
| **ID**                       | HU-03                                                              |
| **Épica**                    | Extracción OCR y Procesamiento Documental                          |
| **Esfuerzo Principal**       | ⚙️ Backend (AWS SDK, lógica de OCR, gestión de confidencia)        |
| **Prioridad**                | 🔴 Alta — Núcleo del pipeline de extracción                        |
| **Story Points Estimados**   | 13                                                                 |
| **Sprint Sugerido**          | Sprint 1                                                           |
| **Roles Involucrados**       | Sistema (sin intervención humana directa)                          |

---

## Historia de Usuario

> **Como** Sistema de automatización GRM,
> **Quiero** conectarme a AWS Textract mediante el SDK de AWS configurado con credenciales de entorno, procesar cada página de un documento de forma síncrona y consolidar los resultados de extracción de texto y campos,
> **Para que** el pipeline disponga de los datos OCR completos y estructurados de cada documento dentro de los tiempos de SLA establecidos, garantizando una confianza mínima del 95% en cada campo extraído.

---

## Descripción Funcional

Este módulo es el motor de reconocimiento óptico de caracteres del sistema. Recibe como entrada los documentos segmentados página por página desde HU-02 y produce como salida los datos OCR estructurados listos para el Agente de Contexto (HU-04).

### Configuración de credenciales (ENV)
Las credenciales de AWS se configuran exclusivamente mediante variables de entorno del servidor/aplicación:
```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=...
```
El sistema **nunca** debe tener credenciales hardcodeadas en el código fuente.

### Flujo de procesamiento por página
1. Recibir página individual (imagen o PDF de 1 página)
2. Invocar `textract:detect_document_text` o `textract:analyze_document` (con FeatureTypes según regla)
3. Parsear la respuesta de Textract: extraer bloques de texto, tablas, formularios según el tipo de documento
4. Evaluar el score de confianza de cada bloque extraído
5. Marcar campos con confianza < 95% como "bajo confianza"
6. Almacenar resultado de la página en la BD como parte del documento padre
7. Repetir hasta completar todas las páginas
8. Consolidar resultados de todas las páginas en el objeto de documento completo

### SLA por tipo de documento
| Tipo de documento    | Páginas típicas | Tiempo máximo permitido |
|----------------------|-----------------|--------------------------|
| Pequeño (1-3 págs)   | 1 a 3           | ≤ 60 segundos            |
| Grande (4+ págs)     | 4 o más         | ≤ 120 segundos           |

---

## Criterios de Aceptación (BDD / Gherkin)

### CA-01 — Carga de credenciales AWS desde variables de entorno
```gherkin
Dado que el sistema va a iniciar una conexión con AWS Textract
Cuando el módulo de OCR se inicializa
Entonces el sistema carga las credenciales AWS exclusivamente desde variables de entorno: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY y AWS_DEFAULT_REGION
  Y si alguna variable de entorno obligatoria está ausente o vacía, el sistema lanza error: "Credenciales AWS no configuradas. Verifica las variables de entorno."
  Y registra el error en el log de auditoría sin exponer los valores de las credenciales
```

### CA-02 — Procesamiento síncrono página por página
```gherkin
Dado que el lote de documentos tiene páginas segmentadas disponibles en la ruta temporal
Cuando el módulo OCR inicia el procesamiento de un documento
Entonces el sistema invoca AWS Textract de forma síncrona para cada página individual del documento
  Y espera la respuesta completa de cada página antes de procesar la siguiente
  Y mantiene el orden secuencial de páginas durante el procesamiento
  Y registra en BD el resultado OCR de cada página con referencia al documento padre
```

### CA-03 — Evaluación del score de confianza por campo/bloque
```gherkin
Dado que AWS Textract retorna la respuesta de extracción para una página
Cuando el sistema parsea los bloques de texto y campos extraídos
Entonces evalúa el score de confianza de cada bloque individualmente
  Y clasifica cada bloque como "Alta confianza" (≥95%) o "Baja confianza" (<95%)
  Y almacena el score de confianza junto al valor extraído para cada bloque
  Y marca el documento como "requiere revisión" si uno o más campos críticos tienen confianza <95%
```

### CA-04 — Manejo de error de conexión con AWS Textract
```gherkin
Dado que el módulo OCR intenta invocar AWS Textract
Cuando ocurre un error de conexión (timeout, credenciales inválidas, límite de cuota superado)
Entonces el sistema registra el error específico en el log de auditoría con: tipo de error, código HTTP, timestamp, página afectada
  Y marca la página como "error OCR" en la tabla de documentos_paginas
  Y reintenta la invocación hasta 3 veces con backoff exponencial (1s, 2s, 4s)
  Y si los 3 reintentos fallan, marca el documento completo como "Error en OCR" y lo mueve a la cola de revisión humana
```

### CA-05 — Consolidación de resultados de todas las páginas de un documento
```gherkin
Dado que el sistema ha completado el OCR de todas las páginas individuales de un documento
Cuando la última página es procesada exitosamente
Entonces el sistema consolida los bloques extraídos de todas las páginas en un único objeto de documento
  Y mantiene la referencia de número de página para cada bloque de texto consolidado
  Y calcula el score de confianza global del documento como el promedio ponderado de todos los bloques
  Y actualiza el estado del documento a "OCR Completado" en la tabla de documentos_lote
```

### CA-06 — Control del SLA de procesamiento
```gherkin
Dado que el sistema está procesando un documento
Cuando el tiempo acumulado de procesamiento supera el umbral de SLA:
    | Páginas   | Tiempo máximo |
    | 1 a 3     | 60 segundos   |
    | 4 o más   | 120 segundos  |
Entonces el sistema registra un evento de "SLA Superado" en el log de auditoría
  Y continúa el procesamiento (no cancela)
  Y notifica al sistema de monitoreo con alerta de SLA excedido
  Y expone el tiempo real de procesamiento en el dashboard de estado del lote
```

### CA-07 — Uso del tipo de análisis Textract según el tipo de documento
```gherkin
Dado que la Regla de Trabajo activa especifica un tipo de documento
Cuando el módulo OCR prepara la invocación a AWS Textract
Entonces selecciona la modalidad de análisis apropiada:
    | Tipo de documento              | Modalidad Textract                        |
    | Texto general / Endoso         | detect_document_text                      |
    | Formulario con campos/valores  | analyze_document con FORMS                |
    | Tablas numéricas / Pagaré      | analyze_document con TABLES               |
  Y aplica la modalidad definida para todas las páginas del documento
```

### CA-08 — Almacenamiento granular de resultados OCR por página
```gherkin
Dado que AWS Textract retorna exitosamente los resultados de una página
Cuando el sistema almacena los resultados
Entonces guarda en la tabla ocr_resultados_paginas: documento_id, numero_pagina, bloques_json (respuesta raw de Textract), campos_extraidos_json (campos parseados con sus scores), timestamp_procesamiento
  Y la respuesta raw de Textract se almacena sin modificaciones para trazabilidad completa
```

### CA-09 — Procesamiento de imágenes JPG/PNG/TIFF además de PDF
```gherkin
Dado que el lote contiene imágenes en formato JPG, PNG o TIFF (no PDF)
Cuando el módulo OCR procesa esos archivos
Entonces convierte la imagen al formato requerido por Textract (bytes o referencia S3)
  Y la procesa como una "página única" del documento
  Y la consolida igual que una página PDF dentro del objeto de documento
```

### CA-10 — Indicador de progreso de OCR para el panel de monitoreo
```gherkin
Dado que el módulo OCR está procesando un lote de documentos
Cuando el sistema actualiza el estado de cada página procesada
Entonces actualiza en tiempo real (o near-real-time) el registro de progreso en BD:
    - Páginas procesadas vs. total
    - Documentos completados vs. total
    - Documentos con error vs. total
  Y este progreso es consultable por el frontend para mostrar el estado del lote al operario
```

### CA-11 — Manejo de página en blanco o ilegible
```gherkin
Dado que Textract procesa una página del documento
Cuando la respuesta de Textract retorna 0 bloques de texto o confianza promedio <50%
Entonces el sistema clasifica esa página como "Página en blanco o ilegible"
  Y registra el evento en el log con: documento_id, número de página, motivo
  Y agrega la página al reporte de revisión humana junto con el documento padre
  Y continúa procesando las demás páginas del documento sin interrumpir el lote
```

### CA-12 — Limpieza de archivos temporales tras procesamiento exitoso
```gherkin
Dado que el módulo OCR ha completado exitosamente el procesamiento de todos los documentos del lote
Cuando el sistema confirma que los datos OCR están almacenados en BD
Entonces elimina los archivos de la carpeta temporal del lote ({temp}/{batch_id}/)
  Y registra la limpieza en el log de auditoría con: batch_id, archivos eliminados, timestamp
  Y mantiene únicamente las referencias a la ruta original de los documentos fuente
```

---

## Notas Técnicas

### Base de Datos (SQL Server)
```sql
CREATE TABLE ocr_resultados_paginas (
    id                  INT IDENTITY PRIMARY KEY,
    documento_id        INT FOREIGN KEY REFERENCES documentos_lote(id),
    numero_pagina       INT NOT NULL,
    bloques_raw_json    NVARCHAR(MAX),   -- Respuesta raw de Textract
    campos_parseados    NVARCHAR(MAX),   -- JSON: [{campo, valor, confianza, obligatorio}]
    confianza_promedio  DECIMAL(5,2),
    estado              NVARCHAR(50),    -- 'completado' | 'baja_confianza' | 'error' | 'en_blanco'
    tiempo_proceso_ms   INT,
    processed_at        DATETIME DEFAULT GETDATE()
);
```

### Librerías requeridas
- `boto3` (Python AWS SDK) o `@aws-sdk/client-textract` (Node.js)
- Variables de entorno: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`

### Dependencias
- **Depende de**: HU-02 (Ingesta — provee ruta temporal y batch_id)
- **Bloquea a**: HU-04 (Agente de Contexto — recibe datos OCR consolidados)
