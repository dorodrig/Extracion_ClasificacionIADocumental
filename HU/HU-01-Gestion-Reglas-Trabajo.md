# HU-01 — Configuración y Gestión de Reglas de Trabajo del Cliente

## Metadatos

| Campo                        | Valor                                                        |
| ---------------------------- | ------------------------------------------------------------ |
| **ID**                       | HU-01                                                        |
| **Épica**                    | Configuración del Sistema                                    |
| **Esfuerzo Principal**       | 🖥️ Frontend UI + ⚙️ Backend (API REST + SQL Server)         |
| **Prioridad**                | 🔴 Alta — Bloqueante para el resto del flujo                 |
| **Story Points Estimados**   | 13                                                           |
| **Sprint Sugerido**          | Sprint 1                                                     |
| **Roles Involucrados**       | Operario de Digitalización, Administrador                    |

---

## Historia de Usuario

> **Como** Operario de Digitalización o Administrador del sistema,
> **Quiero** crear, visualizar, editar y seleccionar Reglas de Trabajo configuradas por cliente,
> **Para que** el sistema de extracción y clasificación sepa exactamente qué campos extraer, con qué estructura organizar los documentos en carpetas y bajo qué parámetros operar, sin ambigüedad ni intervención manual adicional.

---

## Descripción Funcional

Una **Regla de Trabajo** es la unidad de configuración central del sistema GRM. Cada regla pertenece a un cliente y contiene los siguientes elementos configurables:

| # | Elemento                         | Descripción                                                                 |
|---|----------------------------------|-----------------------------------------------------------------------------|
| 1 | **Selección del cliente**        | Dropdown con clientes registrados en el sistema                             |
| 2 | **Tipo de documento**            | Ej: Pagaré, Endoso, Cédula de Ciudadanía, Carta Laboral                    |
| 3 | **Campos a extraer**             | Lista dinámica: nombre del campo + tipo de dato + obligatorio (S/N)         |
| 4 | **Patrón de carpeta de salida**  | Ej: `/{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/{NOMBRE_ARCHIVO}.pdf`         |
| 5 | **Modo de entrada**              | Escáner por lotes / Carpeta local (uno a uno)                               |
| 6 | **Umbral de confianza OCR**      | Fijo en ≥95% — visible, no editable por el operario                        |

Un cliente puede tener **múltiples reglas**. Al acceder, si ya tiene reglas registradas, el sistema mostrará un listado con acciones de selección, edición o inicio de proceso. Si no tiene reglas, mostrará directamente el formulario de creación.

---

## Criterios de Aceptación (BDD / Gherkin)

### CA-01 — Primer acceso de cliente sin reglas previas
```gherkin
Dado que el operario ha seleccionado un cliente que NO tiene reglas registradas en el sistema
Cuando el sistema carga la sección "Reglas de Trabajo"
Entonces el sistema muestra el formulario de creación de regla completamente vacío
  Y muestra el mensaje informativo: "Este cliente no tiene reglas configuradas. Crea la primera regla."
  Y el botón "Guardar Regla" permanece deshabilitado hasta que todos los campos obligatorios estén completos
```

### CA-02 — Visualización del listado de reglas de un cliente con reglas existentes
```gherkin
Dado que el cliente seleccionado tiene una o más reglas registradas
Cuando el operario accede a la sección "Reglas de Trabajo"
Entonces el sistema muestra una tabla/listado con todas las reglas del cliente
  Y cada fila muestra: Nombre de regla, Tipo de documento, Fecha de creación, Última modificación, Versión
  Y cada fila ofrece los botones de acción: "Editar", "Iniciar Proceso", "Ver Detalle"
```

### CA-03 — Carga de regla existente para edición
```gherkin
Dado que el operario visualiza el listado de reglas del cliente
Cuando hace clic en el botón "Editar" sobre una regla específica
Entonces el sistema carga el formulario con todos los valores actuales de esa regla pre-rellenados
  Y todos los campos del formulario están en modo editable
  Y el botón principal del formulario muestra el texto "Actualizar Regla" (no "Guardar Regla")
```

### CA-04 — Creación de una nueva regla adicional para cliente con reglas existentes
```gherkin
Dado que el cliente ya tiene al menos una regla registrada
Cuando el operario hace clic en el botón "Nueva Regla"
Entonces el sistema abre el formulario de regla completamente vacío
  Y genera un nuevo ID único para la nueva regla
  Y las reglas existentes del cliente no son modificadas ni sobreescritas
```

### CA-05 — Validación de campos obligatorios al guardar
```gherkin
Dado que el operario intenta guardar o actualizar una regla de trabajo
Cuando hace clic en "Guardar Regla" o "Actualizar Regla"
Entonces el sistema valida que los campos obligatorios estén completos:
    | Campo obligatorio                        |
    | Cliente seleccionado                     |
    | Nombre de la regla                       |
    | Tipo de documento                        |
    | Al menos 1 campo a extraer definido      |
    | Patrón de carpeta de salida              |
    | Modo de entrada seleccionado             |
  Y si algún campo obligatorio está vacío, muestra un mensaje de error inline junto al campo
  Y no persiste la regla en base de datos hasta que todos los campos obligatorios estén completos
```

### CA-06 — Definición dinámica de campos a extraer
```gherkin
Dado que el operario está configurando los campos a extraer dentro de una regla
Cuando agrega un campo mediante el componente dinámico de campos
Entonces el sistema permite agregar N campos, cada uno con:
    | Propiedad        | Descripción                                           |
    | Nombre del campo | Texto libre (ej: "Número de Cédula")                  |
    | Tipo de dato     | Texto / Número / Fecha / Identificación               |
    | Obligatorio      | Checkbox Sí/No                                        |
  Y permite eliminar cualquier campo con un botón de eliminación por fila
  Y el sistema valida que no existan dos campos con el mismo nombre dentro de la misma regla
  Y muestra un error inline si se detecta un nombre de campo duplicado
```

### CA-07 — Configuración y validación del patrón de carpeta de salida
```gherkin
Dado que el operario ingresa el patrón de estructura de carpeta de salida
Cuando escribe el patrón usando variables dinámicas entre llaves (ej: /{CC}/{NOMBRE_COMPLETO}/{TIPO_DOC})
Entonces el sistema muestra en tiempo real una vista previa del patrón con valores de ejemplo
  Y valida que el patrón contenga al menos una variable dinámica que corresponda a un campo a extraer definido
  Y almacena el patrón exacto en base de datos para ser consumido por el Agente de Clasificación
  Y si una variable del patrón no existe como campo definido, muestra advertencia: "Variable {CAMPO} no está definida como campo a extraer"
```

### CA-08 — Umbral de confianza OCR fijo y visible
```gherkin
Dado que el operario accede al formulario de creación o edición de una regla
Cuando visualiza el campo "Umbral de Confianza OCR"
Entonces el sistema muestra el valor fijo de 95% en modo solo lectura (campo deshabilitado)
  Y muestra un ícono de información con tooltip: "El sistema descartará cualquier campo con confianza OCR inferior al 95%. Este valor es estándar del proceso."
  Y este valor no es modificable por el rol Operario ni por el rol Cliente
```

### CA-09 — Inicio del proceso de extracción desde una regla
```gherkin
Dado que el operario selecciona una regla del listado del cliente
Cuando hace clic en el botón "Iniciar Proceso"
Entonces el sistema presenta al operario la pantalla de decisión de modo de ingesta: "¿Cómo deseas ingresar los documentos?" (ver HU-02 CA-00)
  Y preselecciona en esa pantalla de decisión el modo guardado en la regla (Escáner o Carpeta)
  Y solo tras confirmar el modo de ingesta, el sistema redirige a la pantalla de ingesta de documentos (HU-02)
  Y bloquea la posibilidad de cambiar la regla una vez que el modo ha sido confirmado y el proceso está activo
  Y si el operario cancela desde la pantalla de decisión de modo, regresa al listado de reglas sin iniciar ningún lote
```

### CA-10 — Versionamiento automático al actualizar una regla existente
```gherkin
Dado que el operario modifica campos de una regla existente y hace clic en "Actualizar Regla"
Cuando el sistema procesa el guardado exitoso
Entonces el sistema incrementa el número de versión de la regla (ej: v1 → v2)
  Y registra en la tabla de auditoría: usuario que modificó, fecha/hora, campos modificados (campo anterior vs. nuevo valor), versión nueva
  Y la versión anterior queda archivada en base de datos (soft delete / histórico), NO eliminada
  Y el listado de reglas muestra siempre la versión más reciente como activa
```

### CA-11 — Persistencia de reglas para uso en futuros proyectos
```gherkin
Dado que el operario guarda una regla exitosamente para un cliente
Cuando el mismo cliente inicia un nuevo proyecto en el futuro
Entonces la regla sigue disponible en el listado del cliente
  Y el operario puede seleccionarla directamente para iniciar proceso
  Y el operario puede hacer clic en "Duplicar Regla" para usarla como base para una nueva configuración sin modificar la original
```

### CA-12 — Validación de nombre único de regla por cliente
```gherkin
Dado que el operario intenta guardar una regla con un nombre que ya existe para el mismo cliente
Cuando hace clic en "Guardar Regla"
Entonces el sistema detecta el conflicto de nombre duplicado
  Y muestra el mensaje de error: "Ya existe una regla con el nombre '{nombre}' para este cliente. Por favor usa un nombre diferente."
  Y no persiste la nueva regla hasta que el nombre sea único para ese cliente
```

### CA-13 — Selección de modo de entrada de documentos en la regla
```gherkin
Dado que el operario está configurando una regla de trabajo
Cuando selecciona el campo "Modo de Entrada"
Entonces el sistema muestra dos opciones: "Escáner (por lotes)" y "Carpeta local (uno a uno)"
  Y persiste esta selección como parte de la regla
  Y al iniciar el proceso, el sistema preconfigura la pantalla de ingesta (HU-02) según el modo definido en la regla
```

---

## Notas Técnicas

### Base de Datos (SQL Server)
```sql
-- Tabla principal de reglas
CREATE TABLE reglas_trabajo (
    id              INT IDENTITY PRIMARY KEY,
    cliente_id      INT NOT NULL FOREIGN KEY REFERENCES clientes(id),
    nombre          NVARCHAR(200) NOT NULL,
    tipo_documento  NVARCHAR(100) NOT NULL,
    campos_extraer  NVARCHAR(MAX),  -- JSON: [{nombre, tipo, obligatorio}]
    patron_carpeta  NVARCHAR(500) NOT NULL,
    modo_entrada    NVARCHAR(50) NOT NULL,  -- 'scanner' | 'carpeta'
    umbral_ocr      DECIMAL(5,2) DEFAULT 95.00,
    version         INT DEFAULT 1,
    activa          BIT DEFAULT 1,
    created_by      INT FOREIGN KEY REFERENCES usuarios(id),
    created_at      DATETIME DEFAULT GETDATE(),
    updated_at      DATETIME
);

-- Historial de versiones de reglas
CREATE TABLE reglas_trabajo_historial (
    id              INT IDENTITY PRIMARY KEY,
    regla_id        INT FOREIGN KEY REFERENCES reglas_trabajo(id),
    version         INT,
    snapshot_json   NVARCHAR(MAX),  -- JSON completo de la regla en esa versión
    modificado_por  INT FOREIGN KEY REFERENCES usuarios(id),
    modificado_at   DATETIME DEFAULT GETDATE()
);
```

### Endpoints API REST
| Método | Ruta                        | Descripción                          |
|--------|-----------------------------|--------------------------------------|
| GET    | `/api/rules?cliente_id={id}` | Listar reglas de un cliente          |
| GET    | `/api/rules/{id}`            | Obtener detalle de una regla         |
| POST   | `/api/rules`                 | Crear nueva regla                    |
| PUT    | `/api/rules/{id}`            | Actualizar regla (genera versión)    |
| POST   | `/api/rules/{id}/duplicate`  | Duplicar regla existente             |

---

## Dependencias
- **Bloqueado por**: HU-08 (Roles y Autenticación — el operario debe estar autenticado y haber seleccionado un cliente)
- **Bloquea a**: HU-02 (Ingesta de Documentos), HU-04 (Agente de Contexto), HU-05 (Agente de Clasificación)
