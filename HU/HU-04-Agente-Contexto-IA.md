# HU-04 — Agente de Contexto IA (Google Gemini): Interpretación y Limpieza de Datos OCR

## Metadatos

| Campo                        | Valor                                                                    |
| ---------------------------- | ------------------------------------------------------------------------ |
| **ID**                       | HU-04                                                                    |
| **Épica**                    | Agentes de Inteligencia Artificial                                       |
| **Esfuerzo Principal**       | ⚙️ Backend (Google Gemini SDK, lógica de IA, pipeline de datos)          |
| **Prioridad**                | 🔴 Alta — Puente entre OCR crudo y clasificación inteligente             |
| **Story Points Estimados**   | 13                                                                       |
| **Sprint Sugerido**          | Sprint 2                                                                 |
| **Roles Involucrados**       | Sistema (sin intervención humana directa)                                |

---

## Historia de Usuario

> **Como** Sistema de automatización GRM,
> **Quiero** que el Agente de Contexto IA interprete los datos OCR crudos de cada documento junto con las reglas de negocio del cliente (campos a extraer, tipo de documento, patrón de carpeta) usando el SDK de Google Gemini,
> **Para que** el pipeline disponga de datos limpios, estructurados y semánticamente validados, listos para ser procesados por el Agente de Clasificación (HU-05) sin ambigüedad ni datos sucios.

---

## Descripción Funcional

El **Agente de Contexto** es el primer agente de IA del pipeline. Su responsabilidad es actuar como intérprete semántico entre el output crudo de AWS Textract y los requerimientos de negocio del cliente.

### Entradas del Agente
1. **Datos OCR consolidados** del documento (output de HU-03): texto extraído, campos, scores de confianza por página
2. **Regla de Trabajo activa** del cliente (de HU-01): lista de campos a extraer, tipos de dato, obligatorios, patrón de carpeta
3. **Tipo de documento** esperado según la regla

### Proceso del Agente
1. Construir un prompt estructurado con: datos OCR + instrucciones de extracción según la regla
2. Invocar Google Gemini API (vía SDK) con el prompt construido
3. Recibir respuesta estructurada (JSON) con los campos extraídos y validados
4. Aplicar validaciones post-IA: tipos de dato, campos obligatorios presentes, valores no nulos
5. Producir el **"Paquete de Datos Limpios"** para el Agente de Clasificación
6. Si el documento no supera la validación, marcarlo como "pendiente revisión humana"

### Configuración de la conexión Gemini
```
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-1.5-pro  # o el modelo que se defina como estándar del proyecto
```

### Salida del Agente (Paquete de Datos Limpios)
```json
{
  "documento_id": "...",
  "batch_id": "...",
  "regla_id": "...",
  "tipo_documento_detectado": "Pagaré",
  "campos_extraidos": [
    { "nombre": "CC", "valor": "123456789", "confianza_ocr": 98.5, "validado_ia": true },
    { "nombre": "NOMBRE_COMPLETO", "valor": "David Rodríguez", "confianza_ocr": 97.1, "validado_ia": true }
  ],
  "datos_completos": true,
  "motivo_rechazo": null
}
```

---

## Criterios de Aceptación (BDD / Gherkin)

### CA-01 — Construcción del prompt con datos OCR y reglas de negocio
```gherkin
Dado que el Agente de Contexto recibe los datos OCR consolidados de un documento y la Regla de Trabajo activa
Cuando el agente prepara la invocación a Google Gemini
Entonces construye un prompt que incluye:
    - Los campos a extraer definidos en la regla (nombres, tipos de dato, obligatoriedad)
    - El texto OCR completo del documento con los scores de confianza por campo
    - El tipo de documento esperado según la regla
    - Instrucción explícita de retornar la respuesta en formato JSON estructurado
  Y el prompt no incluye información de otros clientes ni de otras reglas
```

### CA-02 — Invocación a Google Gemini mediante SDK
```gherkin
Dado que el prompt ha sido construido correctamente
Cuando el agente invoca la API de Google Gemini
Entonces usa el SDK oficial de Google Gemini con la clave API cargada desde variable de entorno GEMINI_API_KEY
  Y si la variable de entorno está ausente o vacía, lanza error: "Clave de API de Gemini no configurada"
  Y registra en el log: modelo invocado, timestamp de inicio, tokens utilizados (input/output)
```

### CA-03 — Parseo y validación de la respuesta JSON de Gemini
```gherkin
Dado que el Agente de Contexto recibe la respuesta de Google Gemini
Cuando procesa la respuesta
Entonces valida que la respuesta es un JSON válido y estructurado
  Y si Gemini retorna texto no estructurado o un JSON inválido, el agente realiza hasta 2 reintentos con el mismo prompt
  Y si tras los reintentos la respuesta no es válida, marca el documento como "Error de IA - Respuesta inválida" y lo envía a revisión humana
```

### CA-04 — Validación de campos obligatorios en el paquete de datos limpios
```gherkin
Dado que el Agente de Contexto ha parseado la respuesta de Gemini
Cuando evalúa los campos extraídos contra la regla de trabajo
Entonces verifica que todos los campos marcados como "obligatorio" en la regla tienen un valor no nulo y no vacío
  Y verifica que los tipos de dato son consistentes (ej: campo tipo "Identificación" contiene solo números)
  Y si todos los campos obligatorios están presentes y válidos, establece datos_completos = true
  Y si algún campo obligatorio está ausente, nulo o con valor incoherente, establece datos_completos = false
```

### CA-05 — Enrutamiento de documentos incompletos a cola de revisión humana
```gherkin
Dado que el Agente de Contexto evalúa un documento y determina que datos_completos = false
Cuando registra el resultado de la evaluación
Entonces almacena el documento con estado "Pendiente Revisión Humana" en la tabla de pendientes
  Y registra el motivo_rechazo con detalle específico: qué campo(s) están ausentes o inválidos
  Y coloca el documento en la cola de revisión visible para el Operario (HU-06)
  Y NO pasa el documento al Agente de Clasificación (HU-05)
```

### CA-06 — Enrutamiento de documentos completos al Agente de Clasificación
```gherkin
Dado que el Agente de Contexto evalúa un documento y determina que datos_completos = true
Cuando el paquete de datos limpios está listo
Entonces almacena el paquete en la tabla agente_contexto_resultados con estado "Datos Limpios - Listo para Clasificación"
  Y dispara el Agente de Clasificación (HU-05) con el paquete de datos limpios como entrada
  Y registra en el log de auditoría: documento_id, timestamp, campos validados, modelo Gemini utilizado
```

### CA-07 — Detección del tipo de documento por el agente
```gherkin
Dado que el agente procesa el texto OCR de un documento
Cuando el tipo de documento detectado por Gemini difiere del tipo esperado según la regla
Entonces el agente registra el conflicto: tipo_esperado vs. tipo_detectado
  Y si el tipo detectado tiene confianza >90% (según el razonamiento del agente), agrega una alerta al paquete de datos
  Y si el tipo detectado es completamente diferente (ej: recibo de agua en lugar de pagaré), establece datos_completos = false con motivo "Tipo de documento incorrecto"
```

### CA-08 — Manejo de timeout o error de la API de Gemini
```gherkin
Dado que el agente invoca la API de Google Gemini
Cuando la API no responde dentro de 30 segundos o retorna un error HTTP (5xx)
Entonces el agente reintenta la invocación hasta 3 veces con backoff exponencial
  Y si los 3 reintentos fallan, marca el documento como "Error de IA - API no disponible"
  Y registra el error completo en el log de auditoría: código de error, mensaje, intentos realizados
  Y mueve el documento a la cola de revisión humana con el motivo del error visible para el operario
```

### CA-09 — Registro de tokens y costos de la invocación Gemini
```gherkin
Dado que el agente completa una invocación a Google Gemini (exitosa o con error)
Cuando procesa la metadata de respuesta de la API
Entonces registra en la tabla log_ia_invocaciones: documento_id, modelo, tokens_entrada, tokens_salida, duracion_ms, timestamp, costo_estimado (si disponible en la API)
  Y este registro es utilizable para análisis de costos y optimización del sistema
```

### CA-10 — Aislamiento de contexto por documento (sin contaminación cruzada)
```gherkin
Dado que el agente procesa múltiples documentos del mismo lote en secuencia
Cuando construye el prompt para cada documento
Entonces el contexto de cada invocación es completamente independiente
  Y no incluye datos OCR ni resultados de documentos anteriores en el mismo prompt
  Y cada invocación comienza con un contexto fresco (sin historial de conversación previo)
```

### CA-11 — Normalización de valores extraídos
```gherkin
Dado que Gemini retorna valores extraídos que pueden tener variaciones de formato
Cuando el agente procesa los valores de campos tipo Identificación o Fecha
Entonces normaliza los valores:
    | Tipo          | Normalización aplicada                                        |
    | Identificación| Solo dígitos, sin puntos ni espacios (ej: "1.234.567" → "1234567") |
    | Fecha         | Formato ISO 8601 (YYYY-MM-DD)                                 |
    | Texto         | Trim de espacios extremos, capitalización estándar            |
  Y almacena tanto el valor normalizado como el valor original del OCR para trazabilidad
```

### CA-12 — Generación del paquete de datos limpios completo
```gherkin
Dado que el agente ha completado exitosamente la validación de todos los campos
Cuando construye el Paquete de Datos Limpios
Entonces incluye en el paquete:
    - documento_id, batch_id, regla_id
    - tipo_documento_detectado
    - campos_extraidos (con nombre, valor normalizado, valor_original, confianza_ocr, validado_ia)
    - datos_completos (boolean)
    - motivo_rechazo (null si datos_completos=true)
    - numero_paginas_procesadas
    - modelo_ia_utilizado
    - timestamp_procesamiento
  Y persiste el paquete en la tabla agente_contexto_resultados en SQL Server
```

---

## Notas Técnicas

### Base de Datos (SQL Server)
```sql
CREATE TABLE agente_contexto_resultados (
    id                      INT IDENTITY PRIMARY KEY,
    documento_id            INT FOREIGN KEY REFERENCES documentos_lote(id),
    regla_id                INT FOREIGN KEY REFERENCES reglas_trabajo(id),
    tipo_doc_detectado      NVARCHAR(100),
    campos_extraidos_json   NVARCHAR(MAX),   -- JSON del paquete de datos limpios
    datos_completos         BIT,
    motivo_rechazo          NVARCHAR(500),
    modelo_ia               NVARCHAR(100),
    tokens_entrada          INT,
    tokens_salida           INT,
    duracion_ms             INT,
    estado                  NVARCHAR(50),    -- 'listo_clasificacion' | 'pendiente_humano' | 'error_ia'
    processed_at            DATETIME DEFAULT GETDATE()
);
```

### Variables de entorno requeridas
```
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-1.5-pro
GEMINI_TIMEOUT_SECONDS=30
GEMINI_MAX_RETRIES=3
```

### Dependencias
- **Depende de**: HU-03 (datos OCR consolidados), HU-01 (Regla de Trabajo activa)
- **Bloquea a**: HU-05 (Agente de Clasificación — recibe paquete de datos limpios)
- **Alimenta**: HU-06 (documentos con datos_completos=false van a cola de revisión humana)
