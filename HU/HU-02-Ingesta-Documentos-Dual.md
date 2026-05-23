# HU-02 — Ingesta Dual de Documentos (Escáner por Lotes / Carpeta Local)

## Metadatos

| Campo                        | Valor                                                            |
| ---------------------------- | ---------------------------------------------------------------- |
| **ID**                       | HU-02                                                            |
| **Épica**                    | Ingesta y Preprocesamiento de Documentos                         |
| **Esfuerzo Principal**       | 🖥️ Frontend UI + ⚙️ Backend (Gestión de archivos + Cola)        |
| **Prioridad**                | 🔴 Alta — Punto de entrada al pipeline de procesamiento          |
| **Story Points Estimados**   | 8                                                                |
| **Sprint Sugerido**          | Sprint 1                                                         |
| **Roles Involucrados**       | Operario de Digitalización                                       |

---

## Historia de Usuario

> **Como** Operario de Digitalización,
> **Quiero** seleccionar el modo de ingesta de documentos (escáner por lotes o carpeta local) y enviar los archivos al pipeline de procesamiento,
> **Para que** el sistema inicie automáticamente el flujo de extracción OCR con los documentos correctos y en el orden adecuado, sin necesidad de intervención manual adicional.

---

## Descripción Funcional

Esta historia cubre el primer paso activo del pipeline tras la selección de una Regla de Trabajo. El operario tiene **dos modos de ingesta** según lo definido en la regla:

### Modo 1 — Escáner (por lotes)
- El sistema activa la integración con el escáner local (driver TWAIN/WIA)
- El escáner puede digitalizar múltiples documentos en una sola sesión
- Los archivos generados se agrupan como un lote y se envían al pipeline
- Formato de salida del escáner: PDF (multi-página o por documento)

### Modo 2 — Carpeta Local (uno a uno)
- El operario selecciona una carpeta local mediante un selector de directorio nativo
- El sistema lista todos los archivos PDF/imagen dentro de esa carpeta
- Procesa los documentos secuencialmente, uno a uno, en orden alfabético de nombre de archivo
- Soporta: PDF, JPG, PNG, TIFF

### Preprocesamiento común
- Los PDFs multi-página deben ser **segmentados página por página** antes de enviarse a AWS Textract
- El sistema genera una **ruta de trabajo temporal** para almacenar las páginas divididas
- Al finalizar el OCR de todas las páginas, el sistema **reconstruye el documento PDF completo** para el Agente de Clasificación
- Se genera un **identificador único de lote** (`batch_id`) para rastrear todos los documentos de esta sesión

---

## Criterios de Aceptación (BDD / Gherkin)

### CA-00 — Decisión explícita del modo de ingesta tras "Iniciar Proceso" (Punto de decisión BPMN: ¿Necesita escáner?)
```gherkin
Dado que el operario ha hecho clic en "Iniciar Proceso" sobre una Regla de Trabajo seleccionada
Cuando el sistema procesa la acción de inicio
Entonces antes de cargar la pantalla de ingesta completa, el sistema presenta al operario una pantalla de decisión de modo con la pregunta: "¿Cómo deseas ingresar los documentos?"
  Y muestra dos opciones como elementos de selección visual diferenciados:
      | Opción                        | Ícono | Descripción                                      |
      | Escáner (por lotes)           | 🖨    | Digitaliza múltiples documentos en una sesión    |
      | Carpeta local (uno a uno)     | 📁    | Selecciona una carpeta del equipo y procesa       |
  Y la opción guardada en la Regla de Trabajo activa aparece preseleccionada visualmente
  Y el operario puede confirmar la opción preseleccionada O cambiarla por la opción contraria
  Y el botón "Continuar" solo se habilita cuando una opción está seleccionada
  Y al hacer clic en "Continuar", el sistema registra el modo elegido en el lote (batch) y carga la pantalla de ingesta correspondiente
  Y si el operario cancela desde esta pantalla de decisión, regresa al listado de Reglas de Trabajo sin iniciar ningún lote
```

### CA-01 — Presentación de la pantalla de ingesta según modo confirmado por el operario
```gherkin
Dado que el operario ha confirmado el modo de ingesta en la pantalla de decisión (CA-00)
Cuando el sistema carga la pantalla de ingesta
Entonces el sistema carga la pantalla correspondiente al modo confirmado por el operario (Escáner o Carpeta)
  Y muestra el nombre de la regla activa y el cliente en la cabecera de la pantalla
  Y el modo de ingesta ya no es cambiable en esta pantalla (fue confirmado en el paso anterior)
```

### CA-02 — Activación del escáner en modo "Escáner por lotes"
```gherkin
Dado que el modo de ingesta es "Escáner por lotes"
Cuando el operario hace clic en "Iniciar Escáner"
Entonces el sistema intenta conectarse con el escáner local disponible vía driver del sistema
  Y si la conexión es exitosa, muestra el estado "Escáner conectado ✓" con el nombre del dispositivo
  Y si no detecta escáner, muestra el mensaje de error: "No se detectó ningún escáner. Verifica la conexión y el driver."
  Y no avanza al siguiente paso si el escáner no está conectado
```

### CA-03 — Captura de lote de documentos mediante escáner
```gherkin
Dado que el escáner está conectado y activo
Cuando el operario realiza la digitalización de los documentos
Entonces el sistema recibe los archivos generados y los lista en pantalla con: nombre de archivo, número de páginas, tamaño en MB
  Y asigna un batch_id único a toda la sesión de escaneo
  Y muestra el conteo total de documentos y páginas capturadas
  Y habilita el botón "Enviar a Procesamiento" una vez que al menos un documento ha sido capturado
```

### CA-04 — Selección de carpeta local en modo "Carpeta local"
```gherkin
Dado que el modo de ingesta es "Carpeta local (uno a uno)"
Cuando el operario hace clic en "Seleccionar Carpeta"
Entonces el sistema abre el diálogo nativo de selección de directorios del sistema operativo
  Y tras la selección, lista todos los archivos soportados (PDF, JPG, PNG, TIFF) dentro de la carpeta seleccionada
  Y muestra para cada archivo: nombre, extensión, tamaño en MB, número de páginas (si es PDF)
  Y si la carpeta no contiene archivos soportados, muestra: "La carpeta seleccionada no contiene documentos compatibles."
```

### CA-05 — Validación de formatos de archivo en carpeta local
```gherkin
Dado que el sistema lista los archivos de una carpeta seleccionada
Cuando detecta archivos con extensiones no soportadas (ej: .docx, .xlsx, .txt)
Entonces el sistema excluye esos archivos del listado de procesamiento
  Y muestra un aviso informativo: "Se omitieron N archivo(s) con formato no compatible: [lista de archivos]"
  Y continúa el proceso solo con los archivos soportados
```

### CA-06 — Segmentación de PDF multi-página antes del procesamiento OCR
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

### CA-09 — Validación del volumen del lote antes del envío
```gherkin
Dado que el operario ha listado los documentos a enviar
Cuando el sistema calcula el total de páginas del lote
Entonces muestra un resumen previo al envío: "Total de documentos: N | Total de páginas: P | Tamaño total: X MB"
  Y permite al operario eliminar documentos individuales del lote antes de confirmar el envío
  Y el botón "Confirmar y Enviar" solo se habilita si hay al menos 1 documento en el lote
```

### CA-10 — Manejo de error en archivos corruptos o ilegibles
```gherkin
Dado que el sistema intenta procesar un archivo del lote
Cuando detecta que un archivo está corrupto, protegido con contraseña o no puede ser leído
Entonces marca ese archivo con estado "Error de lectura ⚠️" en el listado
  Y continúa el procesamiento de los demás archivos del lote
  Y registra el error en el log de auditoría con: nombre del archivo, error específico, timestamp
  Y al finalizar el lote, muestra un resumen de archivos con error para revisión del operario
```

### CA-11 — Reconstrucción del PDF completo tras el procesamiento OCR de páginas
```gherkin
Dado que el sistema ha completado el OCR de todas las páginas individuales de un documento PDF
Cuando el pipeline de OCR confirma el procesamiento exitoso de todas las páginas
Entonces el sistema reagrupa los datos extraídos de cada página en un objeto de documento completo
  Y reconstruye la referencia al PDF original completo (no genera un nuevo PDF, referencia el original)
  Y pasa el documento completo con todos sus datos OCR consolidados al Agente de Contexto (HU-04)
```

### CA-12 — Cancelación del proceso de ingesta antes del envío
```gherkin
Dado que el operario ha listado documentos pero aún no ha confirmado el envío
Cuando hace clic en "Cancelar"
Entonces el sistema muestra un diálogo de confirmación: "¿Deseas cancelar la ingesta? Los documentos listados no serán procesados."
  Y si confirma, limpia el listado y elimina los archivos de la ruta temporal
  Y regresa a la pantalla de selección de Regla de Trabajo sin pérdida de configuración
```

---

## Notas Técnicas

### Base de Datos (SQL Server)
```sql
CREATE TABLE lotes_procesamiento (
    id              INT IDENTITY PRIMARY KEY,
    batch_id        UNIQUEIDENTIFIER DEFAULT NEWID(),
    regla_id        INT FOREIGN KEY REFERENCES reglas_trabajo(id),
    cliente_id      INT FOREIGN KEY REFERENCES clientes(id),
    operario_id     INT FOREIGN KEY REFERENCES usuarios(id),
    modo_ingesta    NVARCHAR(50),  -- 'scanner' | 'carpeta'
    ruta_temporal   NVARCHAR(500),
    total_docs      INT,
    total_paginas   INT,
    estado          NVARCHAR(50) DEFAULT 'preparando',  -- preparando | en_proceso | completado | error
    created_at      DATETIME DEFAULT GETDATE(),
    completed_at    DATETIME
);

CREATE TABLE documentos_lote (
    id              INT IDENTITY PRIMARY KEY,
    lote_id         INT FOREIGN KEY REFERENCES lotes_procesamiento(id),
    nombre_archivo  NVARCHAR(300),
    ruta_original   NVARCHAR(500),
    ruta_temporal   NVARCHAR(500),
    total_paginas   INT,
    estado          NVARCHAR(50) DEFAULT 'pendiente',  -- pendiente | procesando | completado | error
    error_detalle   NVARCHAR(MAX),
    created_at      DATETIME DEFAULT GETDATE()
);
```

### Dependencias
- **Depende de**: HU-01 (Reglas de Trabajo — debe existir regla activa), HU-08 (Auth)
- **Bloquea a**: HU-03 (AWS Textract — recibe la ruta temporal y el batch_id)
