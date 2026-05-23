# HU-05 — Agente de Clasificación IA (Google Gemini): Organización Documental y Persistencia

## Metadatos

| Campo                        | Valor                                                                        |
| ---------------------------- | ---------------------------------------------------------------------------- |
| **ID**                       | HU-05                                                                        |
| **Épica**                    | Agentes de Inteligencia Artificial                                           |
| **Esfuerzo Principal**       | ⚙️ Backend (Google Gemini SDK, gestión de sistema de archivos, SQL Server)   |
| **Prioridad**                | 🔴 Alta — Produce el resultado final del pipeline automatizado               |
| **Story Points Estimados**   | 13                                                                           |
| **Sprint Sugerido**          | Sprint 2                                                                     |
| **Roles Involucrados**       | Sistema (sin intervención humana directa en el flujo feliz)                  |

---

## Historia de Usuario

> **Como** Sistema de automatización GRM,
> **Quiero** que el Agente de Clasificación IA tome el Paquete de Datos Limpios del Agente de Contexto y ejecute dos acciones coordinadas: poblar la base de datos del cliente con los campos extraídos Y organizar físicamente los documentos en la carpeta de salida según el patrón de la regla de trabajo,
> **Para que** al final del pipeline todos los documentos del lote estén correctamente clasificados, agrupados por persona (CC, nombre) y tipo de documento, y la información esté disponible para consulta en la interfaz web del cliente.

---

## Descripción Funcional

El **Agente de Clasificación** es el segundo y último agente de IA del pipeline automatizado. Recibe documentos con datos limpios y validados, y ejecuta la organización documental inteligente.

### Caso de uso principal: Lote desordenado
Un lote puede contener 20 documentos de diferentes personas, mezclados y sin orden. Por ejemplo:
- `doc001.pdf` → Pagaré de CC 123456789 (David Rodríguez)
- `doc002.pdf` → Cédula de CC 987654321 (María García)
- `doc003.pdf` → Endoso de CC 123456789 (David Rodríguez)
- `doc004.pdf` → Pagaré de CC 111222333 (Carlos López)

El agente los agrupa inteligentemente y crea la estructura:
```
/carpeta_salida/
  ├── CC123456789/
  │   └── DAVID_RODRIGUEZ/
  │       ├── PAGARE/
  │       │   └── pagare.pdf
  │       └── ENDOSO/
  │           └── endoso.pdf
  ├── CC987654321/
  │   └── MARIA_GARCIA/
  │       └── CEDULA/
  │           └── cedula.pdf
  └── CC111222333/
      └── CARLOS_LOPEZ/
          └── PAGARE/
              └── pagare.pdf
```

### Acciones del Agente
1. Recibir el Paquete de Datos Limpios de HU-04
2. Usar Google Gemini para razonar sobre el patrón de carpeta definido en la regla y los valores de los campos extraídos
3. Construir la ruta de destino para cada documento usando el patrón: `/{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/{NOMBRE_ARCHIVO}`
4. Crear físicamente las carpetas necesarias en el sistema de archivos local
5. Copiar/mover el documento original a su ruta de destino
6. Insertar/actualizar los registros en la BD del cliente con los campos extraídos y la ruta final del documento
7. Marcar el documento como "Clasificado Exitosamente" en la tabla de seguimiento

---

## Criterios de Aceptación (BDD / Gherkin)

### CA-01 — Recepción del Paquete de Datos Limpios
```gherkin
Dado que el Agente de Contexto (HU-04) ha generado un Paquete de Datos Limpios con datos_completos = true
Cuando el Agente de Clasificación recibe el paquete
Entonces verifica que el paquete contiene: documento_id, campos_extraidos con todos los campos obligatorios, tipo_documento_detectado y regla_id
  Y si el paquete está incompleto o malformado, registra el error y devuelve el documento a la cola de revisión humana
  Y NO procede con la clasificación si el paquete es inválido
```

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

---

## Notas Técnicas

### Base de Datos (SQL Server)
```sql
CREATE TABLE documentos_clasificados (
    id                      INT IDENTITY PRIMARY KEY,
    documento_id            INT FOREIGN KEY REFERENCES documentos_lote(id),
    cliente_id              INT FOREIGN KEY REFERENCES clientes(id),
    batch_id                UNIQUEIDENTIFIER,
    regla_id                INT FOREIGN KEY REFERENCES reglas_trabajo(id),
    tipo_documento          NVARCHAR(100),
    campos_json             NVARCHAR(MAX),   -- JSON con todos los campos extraídos y sus valores
    ruta_origen             NVARCHAR(500),
    ruta_destino_final      NVARCHAR(500),
    nombre_archivo_final    NVARCHAR(300),
    estado                  NVARCHAR(50),    -- 'clasificado' | 'pendiente_humano' | 'error'
    clasificado_at          DATETIME DEFAULT GETDATE(),
    reprocesado             BIT DEFAULT 0,
    instruccion_operario    NVARCHAR(MAX)    -- Instrucción del operario si hubo intervención
);
```

### Dependencias
- **Depende de**: HU-04 (Paquete de Datos Limpios del Agente de Contexto)
- **Alimenta**: HU-07 (Portal web del cliente — datos clasificados disponibles para consulta)
- **Recibe retroalimentación de**: HU-06 (Validación humana — instrucciones correctivas del operario)
