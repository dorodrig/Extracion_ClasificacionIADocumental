# HU-06 — Validación Humana: Lista de Pendientes y Visor de Documentos para Operario

## Metadatos

| Campo                        | Valor                                                                      |
| ---------------------------- | -------------------------------------------------------------------------- |
| **ID**                       | HU-06                                                                      |
| **Épica**                    | Validación Humana y Gestión de Excepciones                                 |
| **Esfuerzo Principal**       | 🖥️ Frontend UI + ⚙️ Backend (API de pendientes, acciones correctivas)      |
| **Prioridad**                | 🔴 Alta — Garantiza la tasa de éxito del 100% del pipeline                 |
| **Story Points Estimados**   | 8                                                                          |
| **Sprint Sugerido**          | Sprint 2                                                                   |
| **Roles Involucrados**       | Operario de Digitalización                                                 |

---

## Historia de Usuario

> **Como** Operario de Digitalización,
> **Quiero** ver una lista de documentos que el pipeline automático no pudo procesar completamente, acceder a un visor que me muestre el documento junto con los datos extraídos y el motivo del rechazo, y poder corregir campos individuales o enviar una instrucción al Agente de Clasificación para que resuelva los errores,
> **Para que** ningún documento quede sin clasificar y el proceso tenga una tasa de éxito del 100% con mínima intervención humana.

---

## Descripción Funcional

Esta historia cubre la pantalla de trabajo principal del Operario durante y después del procesamiento de un lote.

### Panel de Documentos Pendientes
- Lista de todos los documentos con estado "Pendiente Revisión Humana"
- Columnas: nombre del archivo, motivo del rechazo, lote de origen, cliente, fecha/hora de entrada a pendientes, tiempo en cola
- Ordenable y filtrable por: cliente, motivo de rechazo, fecha, estado de acción

### Visor de Documentos (componente clave)
- Visualización del documento (PDF o imagen) incrustada en la interfaz web
- Panel lateral con los datos extraídos por el OCR y el Agente de Contexto
- Indicadores visuales de los campos con problemas (resaltados en amarillo/rojo)
- Herramienta de zoom, navegación por páginas y rotación del documento

### Modos de resolución
| Modo | Condición | Acción del Operario |
|------|-----------|---------------------|
| Corrección directa | 1 campo incorrecto o faltante | Editar el campo directamente en el formulario del visor |
| Instrucción al agente | 2 o más errores complejos | Escribir una instrucción en texto libre y enviar al Agente de Clasificación |

---

## Criterios de Aceptación (BDD / Gherkin)

### CA-01 — Visualización de la lista de documentos pendientes
```gherkin
Dado que el operario accede a la sección "Documentos Pendientes"
Cuando la pantalla carga
Entonces el sistema muestra una tabla con todos los documentos en estado "Pendiente Revisión Humana"
  Y cada fila muestra: nombre de archivo, cliente, lote de origen, motivo de rechazo resumido, fecha de entrada a la cola, tiempo en cola (ej: "hace 5 min")
  Y la tabla permite ordenar por cualquier columna
  Y si no hay documentos pendientes, muestra el mensaje: "✓ No hay documentos pendientes. Todo el lote fue procesado exitosamente."
```

### CA-02 — Filtrado y búsqueda en la lista de pendientes
```gherkin
Dado que el operario visualiza la lista de documentos pendientes
Cuando aplica filtros en la interfaz
Entonces puede filtrar por: cliente (dropdown), motivo de rechazo (dropdown), rango de fechas (date picker)
  Y puede buscar por nombre de archivo (campo de texto libre)
  Y los resultados se actualizan en tiempo real al aplicar los filtros
  Y puede limpiar todos los filtros con el botón "Limpiar Filtros"
```

### CA-03 — Apertura del visor de documentos desde la lista
```gherkin
Dado que el operario visualiza la lista de documentos pendientes
Cuando hace clic en "Revisar" sobre un documento específico
Entonces el sistema abre la vista del visor de documentos para ese documento
  Y muestra el documento (PDF/imagen) renderizado en el panel izquierdo de la pantalla
  Y muestra en el panel derecho: campos extraídos por el agente con sus valores y niveles de confianza
  Y resalta visualmente en rojo los campos que causaron el rechazo
  Y muestra el "Motivo de Rechazo" del agente de forma prominente en la cabecera del panel derecho
```

### CA-04 — Navegación por páginas del documento en el visor
```gherkin
Dado que el operario tiene un documento abierto en el visor
Cuando el documento tiene más de una página
Entonces el sistema muestra controles de navegación: botones "Página anterior" y "Página siguiente"
  Y muestra el indicador de página actual: "Página 2 de 5"
  Y permite zoom in/out con controles en pantalla y rueda del ratón
  Y permite rotar la página (90° sentido horario) para documentos digitalizados en orientación incorrecta
```

### CA-05 — Corrección directa de un campo individual (1 error)
```gherkin
Dado que el operario tiene el visor abierto y el motivo de rechazo es 1 campo faltante o incorrecto
Cuando el operario hace clic en el campo problemático del panel derecho
Entonces el campo se vuelve editable directamente en el panel
  Y muestra el valor actual (si lo hay) y permite escribir el valor correcto
  Y al terminar la edición, el operario hace clic en "Guardar Corrección"
  Y el sistema valida que el valor ingresado es del tipo correcto (Texto, Número, Fecha, Identificación)
  Y si la validación es exitosa, el documento es enviado de vuelta al Agente de Clasificación (HU-05) con el campo corregido
```

### CA-06 — Envío de instrucción al agente (2 o más errores)
```gherkin
Dado que el operario tiene el visor abierto y detecta 2 o más errores o una situación compleja
Cuando el operario hace clic en "Enviar Instrucción al Agente"
Entonces el sistema muestra un campo de texto libre prominente con el placeholder: "Describe claramente la corrección necesaria para este documento..."
  Y el operario escribe la instrucción (ej: "El CC del titular es 987654321. El nombre correcto es MARIA ALEJANDRA GARCIA. El tipo de documento es Pagaré, no Endoso.")
  Y hace clic en "Enviar al Agente"
  Y el sistema registra la instrucción del operario en el log de auditoría con: operario_id, timestamp, instrucción
  Y envía el documento con la instrucción al Agente de Clasificación (HU-05) para reprocesamiento
  Y actualiza el estado del documento en la lista a "En reprocesamiento..."
```

### CA-07 — Seguimiento del resultado del reprocesamiento
```gherkin
Dado que el operario ha enviado un documento a reprocesamiento (corrección directa o instrucción al agente)
Cuando el Agente de Clasificación completa el reprocesamiento
Entonces el sistema actualiza automáticamente el estado del documento en la lista del operario
  Y si el reprocesamiento fue exitoso, elimina el documento de la lista de pendientes con indicador "✓ Clasificado"
  Y si el reprocesamiento falló nuevamente, mantiene el documento en la lista con el nuevo motivo de rechazo del agente
  Y el operario puede volver a abrir el visor para una nueva ronda de corrección
```

### CA-08 — Descarte manual de un documento pendiente
```gherkin
Dado que el operario evalúa que un documento es irrecuperable o no corresponde al proceso
Cuando hace clic en "Descartar Documento" dentro del visor
Entonces el sistema muestra un diálogo de confirmación con campo obligatorio de "Motivo de descarte"
  Y si el operario confirma y proporciona el motivo, el sistema cambia el estado del documento a "Descartado"
  Y registra en el log de auditoría: operario_id, motivo, timestamp
  Y el documento desaparece de la lista de pendientes activos
  Y queda disponible en el historial de documentos descartados para revisión del Administrador
```

### CA-09 — Indicador de tiempo en cola y priorización
```gherkin
Dado que hay múltiples documentos en la lista de pendientes
Cuando la lista está cargada
Entonces el sistema calcula y muestra el tiempo que lleva cada documento en la cola
  Y resalta en color ámbar los documentos con más de 15 minutos en cola
  Y resalta en color rojo los documentos con más de 60 minutos en cola
  Y permite al operario ordenar la lista por "Tiempo en cola (mayor a menor)" para priorizar la revisión
```

### CA-10 — Visualización del panel de datos extraídos en el visor
```gherkin
Dado que el operario tiene el visor de documentos abierto
Cuando el panel derecho de datos está cargado
Entonces el sistema muestra para cada campo:
    | Elemento                   | Detalle                                           |
    | Nombre del campo           | Nombre definido en la regla de trabajo            |
    | Valor extraído             | Valor obtenido por el OCR + Agente de Contexto    |
    | Score de confianza OCR     | Porcentaje (ej: 97.3%)                            |
    | Estado de validación IA    | ✓ Válido / ⚠ Baja confianza / ✗ No encontrado    |
    | Obligatorio                | Indicador Sí/No                                   |
  Y los campos con estado "✗ No encontrado" o "⚠ Baja confianza" están resaltados visualmente
```

### CA-11 — Acceso rápido al lote de origen desde el visor
```gherkin
Dado que el operario tiene el visor de documentos abierto
Cuando hace clic en el enlace del lote de origen (batch_id) en la cabecera del visor
Entonces el sistema muestra el resumen completo del lote: estado global, documentos procesados, pendientes, errores
  Y permite al operario navegar entre los documentos pendientes del mismo lote sin regresar a la lista principal
```

### CA-12 — Actualización en tiempo real de la lista de pendientes
```gherkin
Dado que el operario tiene la lista de pendientes abierta mientras el pipeline procesa un lote
Cuando el Agente de Contexto (HU-04) marca un nuevo documento como "Pendiente Revisión Humana"
Entonces el nuevo documento aparece automáticamente en la lista del operario sin necesidad de recargar la página
  Y se muestra una notificación discreta: "Nuevo documento pendiente agregado: {nombre_archivo}"
```

---

## Notas Técnicas

### Base de Datos (SQL Server)
```sql
CREATE TABLE documentos_pendientes (
    id                  INT IDENTITY PRIMARY KEY,
    documento_id        INT FOREIGN KEY REFERENCES documentos_lote(id),
    cliente_id          INT FOREIGN KEY REFERENCES clientes(id),
    motivo_rechazo      NVARCHAR(500),
    motivo_detalle      NVARCHAR(MAX),   -- Respuesta completa del agente
    campos_problema     NVARCHAR(MAX),   -- JSON: [{"campo": "CC", "problema": "nulo"}]
    estado_revision     NVARCHAR(50) DEFAULT 'pendiente', -- pendiente|en_revision|reprocesando|resuelto|descartado
    instruccion_operario NVARCHAR(MAX),
    operario_id         INT FOREIGN KEY REFERENCES usuarios(id),
    tiempo_entrada_cola DATETIME DEFAULT GETDATE(),
    tiempo_resolucion   DATETIME,
    intentos_resolucion INT DEFAULT 0
);
```

### Endpoints API REST
| Método | Ruta                                      | Descripción                                           |
|--------|-------------------------------------------|-------------------------------------------------------|
| GET    | `/api/pendientes?cliente_id={id}`          | Listar documentos pendientes                          |
| GET    | `/api/pendientes/{id}/visor`               | Obtener datos completos para el visor                 |
| PUT    | `/api/pendientes/{id}/correccion`          | Enviar corrección directa de campo                    |
| POST   | `/api/pendientes/{id}/instruccion-agente`  | Enviar instrucción al Agente de Clasificación         |
| PUT    | `/api/pendientes/{id}/descartar`           | Descartar documento con motivo                        |

### Dependencias
- **Depende de**: HU-04 (documentos marcados como pendientes), HU-08 (Auth — rol Operario)
- **Alimenta a**: HU-05 (documentos devueltos al Agente de Clasificación con correcciones/instrucciones)
- **Registra en**: HU-09 (Log de auditoría — toda intervención humana queda registrada)
