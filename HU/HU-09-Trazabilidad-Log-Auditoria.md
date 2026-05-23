# HU-09 — Trazabilidad, Auditoría y Log de Procesos

## Metadatos

| Campo                        | Valor                                                                      |
| ---------------------------- | -------------------------------------------------------------------------- |
| **ID**                       | HU-09                                                                      |
| **Épica**                    | Trazabilidad y Gobierno del Proceso                                        |
| **Esfuerzo Principal**       | ⚙️ Backend (Tablas de auditoría, interceptores, API de consulta de logs)   |
| **Prioridad**                | 🟡 Media — Crítica para el control del proceso en producción               |
| **Story Points Estimados**   | 5                                                                          |
| **Sprint Sugerido**          | Sprint 2 (implementación base) + Sprint 3 (UI de consulta para Admin)     |
| **Roles Involucrados**       | Sistema (escritura automática), Administrador (consulta)                   |

---

## Historia de Usuario

> **Como** Administrador del sistema GRM,
> **Quiero** que cada paso del pipeline (ingesta, OCR, Agente de Contexto, Agente de Clasificación, validación humana, entrega) quede registrado de forma automática en tablas de auditoría con información detallada,
> **Para que** pueda rastrear el ciclo de vida completo de cualquier documento, identificar cuellos de botella, auditar intervenciones humanas y garantizar la trazabilidad total del proceso ante cualquier discrepancia o incidente.

---

## Descripción Funcional

El sistema de trazabilidad es transversal a todo el pipeline. **No es un módulo aislado** — cada HU escribe en las tablas de log automáticamente. Esta HU define el esquema unificado, los eventos a registrar y la interfaz de consulta.

### Eventos registrables por etapa

| Etapa                   | Eventos clave                                                                     |
|-------------------------|-----------------------------------------------------------------------------------|
| Autenticación           | Login exitoso, login fallido, cierre de sesión, bloqueo de cuenta                |
| Reglas de Trabajo       | Creación, actualización, versionamiento de regla                                 |
| Ingesta                 | Inicio de lote, archivos agregados, archivos omitidos (formato inválido), inicio de procesamiento |
| OCR (AWS Textract)      | Inicio/fin de procesamiento por página, score de confianza, errores, SLA superado |
| Agente de Contexto      | Invocación Gemini, tokens usados, resultado (datos_completos=T/F), errores de API |
| Agente de Clasificación | Construcción de ruta, creación de carpetas, copia de archivo, inserción en BD, errores |
| Validación Humana       | Documento asignado a operario, corrección directa, instrucción enviada, descarte  |
| Portal Cliente          | Login, consulta de documento, descarga, intento de acceso no autorizado           |

### Tipos de log
1. **log_proceso**: Eventos del pipeline por documento (quién lo procesó, cuándo, resultado)
2. **log_auditoria_usuario**: Acciones de usuarios (logins, cambios, intervenciones)
3. **log_ia_invocaciones**: Detalle de cada llamada a Gemini y Textract (performance y costos)
4. **log_seguridad**: Intentos de acceso no autorizado, cuentas bloqueadas

---

## Criterios de Aceptación (BDD / Gherkin)

### CA-01 — Registro automático de cada etapa del pipeline por documento
```gherkin
Dado que cualquier etapa del pipeline procesa un documento (OCR, Agente de Contexto, Clasificación, etc.)
Cuando la etapa inicia o finaliza
Entonces el sistema escribe automáticamente un registro en log_proceso con:
    - documento_id, batch_id, lote_id
    - etapa: 'ingesta' | 'ocr' | 'contexto_ia' | 'clasificacion' | 'validacion_humana' | 'entrega'
    - agente: 'sistema' | 'textract' | 'gemini_contexto' | 'gemini_clasificacion' | 'operario_{id}'
    - resultado: 'exitoso' | 'pendiente_humano' | 'error'
    - detalle_json: información adicional específica de la etapa
    - timestamp_inicio, timestamp_fin, duracion_ms
```

### CA-02 — Registro de intervenciones humanas del Operario
```gherkin
Dado que el Operario realiza cualquier acción sobre un documento pendiente (corrección, instrucción, descarte)
Cuando la acción es ejecutada y confirmada
Entonces el sistema registra en log_auditoria_usuario:
    - usuario_id (operario), cliente_id
    - accion: 'correccion_directa' | 'instruccion_agente' | 'descarte'
    - documento_id, batch_id
    - campos_modificados_json: [{campo, valor_anterior, valor_nuevo}] (para corrección directa)
    - instruccion_texto: texto de la instrucción enviada al agente
    - timestamp
  Y este registro establece que el documento fue procesado con "intervención humana" (flag: intervencion_humana=true)
```

### CA-03 — Registro de invocaciones a AWS Textract
```gherkin
Dado que el módulo OCR realiza una invocación a AWS Textract
Cuando la invocación completa (exitosa o con error)
Entonces el sistema registra en log_ia_invocaciones:
    - documento_id, numero_pagina, tipo_invocacion (detect_text | analyze_document)
    - estado_respuesta: 'exitoso' | 'error'
    - codigo_error (si aplica), mensaje_error (si aplica)
    - duracion_ms, confianza_promedio_obtenida
    - timestamp
```

### CA-04 — Registro de invocaciones a Google Gemini
```gherkin
Dado que el Agente de Contexto o el Agente de Clasificación realizan una invocación a Google Gemini
Cuando la invocación completa (exitosa o con error)
Entonces el sistema registra en log_ia_invocaciones:
    - documento_id, agente: 'contexto' | 'clasificacion'
    - modelo_gemini (ej: gemini-1.5-pro)
    - tokens_entrada, tokens_salida, costo_estimado
    - estado_respuesta: 'exitoso' | 'respuesta_invalida' | 'timeout' | 'error_api'
    - intentos_realizados (1, 2 o 3)
    - duracion_ms, timestamp
```

### CA-05 — Consulta del historial de un documento por el Administrador
```gherkin
Dado que el Administrador accede al panel de administración y busca un documento específico
Cuando selecciona el documento y abre su "Historial de Proceso"
Entonces el sistema muestra una línea de tiempo visual con todos los eventos de log_proceso para ese documento:
    ⬤ [timestamp] Ingesta iniciada — Lote {batch_id}
    ⬤ [timestamp] OCR completado — Confianza: 97.2% — Duración: 12s
    ⬤ [timestamp] Agente de Contexto — Datos completos: Sí — Tokens: 850
    ⬤ [timestamp] Agente de Clasificación — Clasificado en: /CC123/DAVID/PAGARE/
    ⬤ [timestamp] Disponible en portal cliente
  Y la línea de tiempo muestra el tiempo transcurrido entre cada etapa
```

### CA-06 — Panel de logs del Administrador con filtros
```gherkin
Dado que el Administrador accede a la sección "Logs y Auditoría"
Cuando el sistema carga el panel
Entonces muestra una tabla paginada de eventos de auditoría
  Y permite filtrar por: tipo de log (proceso, usuario, IA, seguridad), rango de fechas, cliente, batch_id, usuario específico, etapa del proceso, resultado (exitoso/error)
  Y permite exportar los logs filtrados a CSV
  Y los logs se muestran en orden cronológico descendente (más recientes primero)
```

### CA-07 — Dashboard de métricas del pipeline para el Administrador
```gherkin
Dado que el Administrador accede al dashboard de administración
Cuando el sistema carga las métricas
Entonces muestra indicadores calculados desde los logs:
    | Métrica                                    | Descripción                                   |
    | Documentos procesados hoy / esta semana    | Totales del pipeline                          |
    | Tasa de éxito automatizada                 | % documentos sin intervención humana          |
    | Tasa de intervención humana                | % documentos que requirieron operario         |
    | Tiempo promedio por documento              | Desde ingesta hasta clasificación             |
    | Errores de OCR (últimas 24h)              | Conteo y porcentaje                           |
    | Tokens Gemini consumidos (acumulado)       | Para control de costos                        |
```

### CA-08 — Trazabilidad de documentos reprocesados
```gherkin
Dado que un documento fue procesado, rechazado, corregido por el operario y reprocesado por el agente
Cuando el Administrador consulta el historial del documento
Entonces el sistema muestra TODAS las iteraciones del proceso para ese documento, incluyendo:
    - Número de iteración (1er intento, 2do intento, etc.)
    - Motivo de rechazo de cada iteración fallida
    - Intervención del operario (si hubo) con timestamp y texto de instrucción
    - Resultado final de cada iteración
  Y queda claro en el historial qué porcentaje del procesamiento fue automatizado vs. asistido por humano
```

### CA-09 — Registro de eventos de seguridad
```gherkin
Dado que ocurre cualquier evento relacionado con seguridad de acceso
Cuando el sistema detecta el evento
Entonces registra en log_seguridad:
    | Evento                                        | Campos registrados                              |
    | Login fallido                                 | cedula_intentada, IP, timestamp, intento_N      |
    | Cuenta bloqueada                              | usuario_id, timestamp_bloqueo, timestamp_desbloqueo |
    | Acceso no autorizado a recurso               | usuario_id, recurso_solicitado, HTTP_403, timestamp |
    | Cambio de contraseña                          | usuario_id, modificado_por, timestamp           |
  Y los logs de seguridad son accesibles solo para el rol Administrador
```

### CA-10 — Retención y política de logs
```gherkin
Dado que el sistema acumula logs de proceso continuamente
Cuando los registros de log_proceso superan 90 días de antigüedad
Entonces el sistema (o el administrador manualmente) puede ejecutar la tarea de archivado
  Y los logs archivados se marcan como "archivados" (soft-delete) en BD
  Y los logs de auditoría de intervención humana se retienen por mínimo 1 año
  Y los logs de seguridad se retienen por mínimo 1 año
  Y el sistema nunca elimina logs de forma permanente automática durante el piloto
```

---

## Notas Técnicas

### Base de Datos (SQL Server)
```sql
-- Log principal del pipeline por documento
CREATE TABLE log_proceso (
    id              INT IDENTITY PRIMARY KEY,
    documento_id    INT FOREIGN KEY REFERENCES documentos_lote(id),
    batch_id        UNIQUEIDENTIFIER,
    etapa           NVARCHAR(50),
    agente          NVARCHAR(100),
    resultado       NVARCHAR(50),
    detalle_json    NVARCHAR(MAX),
    ts_inicio       DATETIME,
    ts_fin          DATETIME,
    duracion_ms     INT,
    intervencion_humana BIT DEFAULT 0
);

-- Log de acciones de usuarios
CREATE TABLE log_auditoria_usuario (
    id              INT IDENTITY PRIMARY KEY,
    usuario_id      INT FOREIGN KEY REFERENCES usuarios(id),
    cliente_id      INT,
    documento_id    INT,
    accion          NVARCHAR(100),
    detalle_json    NVARCHAR(MAX),
    timestamp       DATETIME DEFAULT GETDATE()
);

-- Log de invocaciones a servicios de IA
CREATE TABLE log_ia_invocaciones (
    id              INT IDENTITY PRIMARY KEY,
    documento_id    INT,
    numero_pagina   INT,
    servicio        NVARCHAR(50),   -- 'textract' | 'gemini'
    agente          NVARCHAR(50),   -- 'contexto' | 'clasificacion'
    modelo          NVARCHAR(100),
    tokens_entrada  INT,
    tokens_salida   INT,
    estado          NVARCHAR(50),
    codigo_error    NVARCHAR(50),
    duracion_ms     INT,
    intentos        INT DEFAULT 1,
    timestamp       DATETIME DEFAULT GETDATE()
);

-- Log de seguridad
CREATE TABLE log_seguridad (
    id              INT IDENTITY PRIMARY KEY,
    usuario_id      INT,
    cedula_intentada NVARCHAR(20),
    evento          NVARCHAR(100),
    detalle         NVARCHAR(500),
    ip_origen       NVARCHAR(50),
    timestamp       DATETIME DEFAULT GETDATE()
);
```

### Dependencias
- **Transversal**: Todas las HU (01-08) escriben en las tablas de log de esta HU
- **Consume datos de**: Todas las HU del pipeline
- **Expone datos a**: Panel del Administrador (Dashboard y Logs)
