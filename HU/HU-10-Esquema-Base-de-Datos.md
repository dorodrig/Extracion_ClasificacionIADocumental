# HU-10 — Diseño del Esquema de Base de Datos Relacional (SQL Server)

## Metadatos

| Campo                        | Valor                                                                 |
| ---------------------------- | --------------------------------------------------------------------- |
| **ID**                       | HU-10                                                                 |
| **Épica**                    | Infraestructura y Persistencia de Datos                               |
| **Esfuerzo Principal**       | ⚙️ Backend (DBA / Schema Design, migraciones, índices, relaciones)    |
| **Prioridad**                | 🔴 Alta — Bloqueante estructural para todo el sistema                 |
| **Story Points Estimados**   | 8                                                                     |
| **Sprint Sugerido**          | Sprint 1 (schema base) + Sprint 2 (tablas de agentes y logs)         |
| **Roles Involucrados**       | Sistema (sin intervención de usuario final)                           |

---

## Historia de Usuario

> **Como** equipo de desarrollo de GRM,
> **Quiero** un esquema de base de datos relacional en SQL Server, con tablas separadas pero relacionadas para gestionar usuarios, clientes, reglas de trabajo, lotes de procesamiento, resultados OCR, datos de agentes, documentos clasificados, tablas de pendientes y logs de auditoría,
> **Para que** el sistema tenga una capa de persistencia coherente, normalizada y consulable que soporte todas las funcionalidades del pipeline y el portal de cliente sin inconsistencias de datos.

---

## Descripción Funcional

Esta HU centraliza el diseño del esquema de base de datos completo. Las tablas fueron definidas individualmente en cada HU; esta historia las consolida, establece las relaciones entre ellas, define índices de performance y documenta las consideraciones de almacenamiento de documentos.

### Consideraciones de almacenamiento de documentos

| Opción                      | Tecnología        | Estado en el Piloto                                          |
|-----------------------------|-------------------|--------------------------------------------------------------|
| **Referencia a ruta local** | SQL Server        | ✅ IMPLEMENTADO en el piloto (columna `ruta_destino_final`)   |
| **Almacenamiento en Base64**| PostgreSQL / SQL Server (FILESTREAM) | 🔲 PREPARADO pero no activo en el piloto |
| **Almacenamiento FILESTREAM**| SQL Server       | 🔲 Evaluación futura — SQL Server sí soporta almacenamiento de archivos binarios |

La arquitectura de columnas `ruta_origen` y `ruta_destino_final` en la tabla `documentos_clasificados` permite migrar al almacenamiento en BD sin cambios en el schema, solo agregando la columna `contenido_b64` o activando FILESTREAM.

---

## Criterios de Aceptación (BDD / Gherkin)

### CA-01 — Existencia y correcta creación del schema completo
```gherkin
Dado que el desarrollador ejecuta el script de migración inicial en SQL Server
Cuando el script se ejecuta sin errores
Entonces las siguientes tablas son creadas con sus columnas, tipos de dato y restricciones correctas:
    | Tabla                          | Descripción                                          |
    | usuarios                       | Usuarios del sistema (todos los roles)               |
    | clientes                       | Clientes de GRM                                      |
    | usuarios_clientes               | Relación N:N usuario-cliente                        |
    | reglas_trabajo                  | Reglas de trabajo por cliente                       |
    | reglas_trabajo_historial        | Historial de versiones de reglas                    |
    | lotes_procesamiento             | Sesiones de ingesta (batch)                         |
    | documentos_lote                 | Documentos individuales dentro de un lote           |
    | ocr_resultados_paginas          | Resultados OCR por página                           |
    | agente_contexto_resultados      | Output del Agente de Contexto                       |
    | documentos_clasificados         | Documentos procesados y organizados                 |
    | documentos_pendientes           | Documentos en cola de revisión humana               |
    | log_proceso                     | Log del pipeline por documento                      |
    | log_auditoria_usuario           | Acciones de usuarios                                |
    | log_ia_invocaciones             | Invocaciones a Textract y Gemini                    |
    | log_seguridad                   | Eventos de seguridad                                |
```

### CA-02 — Integridad referencial entre tablas principales
```gherkin
Dado que el schema está creado en SQL Server
Cuando se verifican las Foreign Keys
Entonces las siguientes relaciones de integridad referencial están implementadas:
    | Tabla hija                  | Columna FK          | Tabla padre              |
    | reglas_trabajo              | cliente_id          | clientes                 |
    | reglas_trabajo              | created_by          | usuarios                 |
    | reglas_trabajo_historial    | regla_id            | reglas_trabajo           |
    | lotes_procesamiento         | regla_id            | reglas_trabajo           |
    | lotes_procesamiento         | cliente_id          | clientes                 |
    | lotes_procesamiento         | operario_id         | usuarios                 |
    | documentos_lote             | lote_id             | lotes_procesamiento      |
    | ocr_resultados_paginas      | documento_id        | documentos_lote          |
    | agente_contexto_resultados  | documento_id        | documentos_lote          |
    | agente_contexto_resultados  | regla_id            | reglas_trabajo           |
    | documentos_clasificados     | documento_id        | documentos_lote          |
    | documentos_clasificados     | cliente_id          | clientes                 |
    | documentos_pendientes       | documento_id        | documentos_lote          |
    | documentos_pendientes       | operario_id         | usuarios                 |
    | log_auditoria_usuario       | usuario_id          | usuarios                 |
```

### CA-03 — Separación clara entre datos de imagen y datos extraídos
```gherkin
Dado que el sistema almacena información de documentos procesados
Cuando se consultan los datos de un documento
Entonces es posible obtener de forma independiente:
    - Los datos de referencia de la imagen/archivo: desde documentos_lote (ruta_original, ruta_destino_final, nombre_archivo)
    - Los datos extraídos por el OCR: desde ocr_resultados_paginas (campos_parseados_json por página)
    - Los datos validados y limpios del Agente de Contexto: desde agente_contexto_resultados (campos_extraidos_json)
    - Los datos clasificados finales: desde documentos_clasificados (campos_json, tipo_documento, ruta_destino_final)
  Y estas tablas están relacionadas por documento_id permitiendo JOINs completos para consultas transversales
```

### CA-04 — Soporte a consultas de documentos por cliente con campos dinámicos
```gherkin
Dado que los campos a extraer son dinámicos (definidos en cada Regla de Trabajo)
Cuando el sistema realiza consultas de documentos del cliente para el portal web
Entonces la columna campos_json en documentos_clasificados almacena los campos en formato JSON
  Y SQL Server permite consultas sobre el JSON mediante JSON_VALUE() o OPENJSON()
  Y el sistema puede filtrar documentos por valor de un campo específico usando estas funciones
  Y el tiempo de respuesta de estas consultas no supera 500ms para hasta 10.000 documentos por cliente
```

### CA-05 — Columna preparada para almacenamiento futuro de documentos en BD
```gherkin
Dado que el piloto usa referencias a rutas locales para los documentos
Cuando el desarrollador revisa la tabla documentos_clasificados
Entonces encuentra la columna ruta_destino_final (NVARCHAR 500) que es la referencia activa en el piloto
  Y encuentra comentado (o en una migración futura documentada) el campo contenido_b64 NVARCHAR(MAX) para Base64
  Y encuentra en la documentación la referencia a la activación de SQL Server FILESTREAM como alternativa binaria
  Y la columna contenido_b64 puede activarse mediante una migración ALTER TABLE sin afectar las filas existentes
```

### CA-06 — Índices de performance en columnas de consulta frecuente
```gherkin
Dado que el sistema realiza consultas frecuentes sobre tablas de alto volumen
Cuando el schema es desplegado
Entonces los siguientes índices están creados:
    | Tabla                      | Columna(s) indexada(s)       | Tipo           |
    | documentos_lote            | lote_id, estado              | Non-clustered  |
    | documentos_clasificados    | cliente_id, tipo_documento   | Non-clustered  |
    | documentos_clasificados    | batch_id                     | Non-clustered  |
    | documentos_pendientes      | cliente_id, estado_revision  | Non-clustered  |
    | log_proceso                | documento_id, etapa          | Non-clustered  |
    | log_ia_invocaciones        | documento_id, servicio       | Non-clustered  |
    | usuarios                   | cedula                       | Unique Index   |
    | clientes                   | nit_cc                       | Unique Index   |
```

### CA-07 — Script de migración versionado y ejecutable
```gherkin
Dado que el desarrollador necesita desplegar el schema en un nuevo entorno
Cuando ejecuta el script de migración V1__initial_schema.sql
Entonces el script es idempotente (usa CREATE TABLE IF NOT EXISTS o DROP/CREATE en transacción)
  Y se ejecuta completamente sin errores en SQL Server 2019 o superior
  Y al finalizar crea un registro en la tabla schema_migrations con: version, descripción, timestamp_ejecucion
  Y el script puede ejecutarse nuevamente sin duplicar tablas ni datos
```

### CA-08 — Relaciones entre tablas de log y tablas principales
```gherkin
Dado que las tablas de log necesitan relacionarse con los documentos del pipeline
Cuando se verifica el schema de las tablas de log
Entonces log_proceso.documento_id referencia documentos_lote.id
  Y log_auditoria_usuario.documento_id referencia documentos_lote.id (nullable — no todos los eventos son de documento)
  Y log_ia_invocaciones.documento_id referencia documentos_lote.id
  Y las tablas de log usan FK con ON DELETE SET NULL para evitar cascadas destructivas
```

### CA-09 — Soporte a consultas de historial del cliente
```gherkin
Dado que el portal del cliente requiere listar todos sus documentos clasificados con filtros
Cuando el backend ejecuta la consulta de documentos del cliente
Entonces la consulta principal es:
    SELECT dc.*, dl.nombre_archivo, dl.ruta_destino_final
    FROM documentos_clasificados dc
    JOIN documentos_lote dl ON dc.documento_id = dl.id
    WHERE dc.cliente_id = @cliente_id
    ORDER BY dc.clasificado_at DESC
  Y esta consulta retorna resultados en menos de 500ms para hasta 10.000 documentos
  Y soporta paginación mediante OFFSET/FETCH NEXT
```

### CA-10 — Gestión de la tabla de pendientes como cola de trabajo
```gherkin
Dado que el sistema usa documentos_pendientes como cola de trabajo del operario
Cuando el operario consulta sus documentos pendientes
Entonces la consulta filtra por: cliente_id (del contexto de sesión del operario) y estado_revision IN ('pendiente', 'reprocesando')
  Y la cola soporta actualización atómica del estado usando UPDATE con WHERE estado='pendiente' para evitar condiciones de carrera
  Y cuando un documento es resuelto, su estado cambia a 'resuelto' y el tiempo_resolucion se registra automáticamente
```

---

## Schema Completo Consolidado (Diagrama de Relaciones)

```
usuarios ─────────────────────────┐
    │ 1:N                          │ N:N (via usuarios_clientes)
    │                              │
reglas_trabajo ◄── clientes ───────┘
    │ 1:N
    │
lotes_procesamiento
    │ 1:N
    │
documentos_lote
    │ 1:N              │ 1:1              │ 1:1
    │                  │                  │
ocr_resultados    agente_contexto    documentos_clasificados
_paginas           _resultados
                                          │ 1:1 (opcional)
                                     documentos_pendientes

Tablas de Log (referencia a documentos_lote):
├── log_proceso
├── log_auditoria_usuario
├── log_ia_invocaciones
└── log_seguridad
```

---

## Notas Técnicas

### Requisitos del entorno
- **SQL Server**: 2019 o superior (o SQL Server Express para el piloto)
- **Collation recomendada**: `SQL_Latin1_General_CP1_CI_AS` (case-insensitive para búsquedas de texto)
- **Compatibilidad JSON**: SQL Server 2016+ (disponible en todas las versiones modernas)

### Herramienta de migraciones
Se recomienda usar un sistema de migraciones versionado:
- **Python**: Alembic (si el backend es Python/SQLAlchemy)
- **Node.js**: Knex.js migrations o Prisma
- O scripts SQL versionados manuales en la carpeta `/db/migrations/`

### Dependencias
- **Esta HU bloquea**: TODAS las demás HU — el schema debe existir antes de que cualquier módulo pueda persistir datos
- **Es consumida por**: HU-01 a HU-09 (todas las tablas del schema son usadas por alguna HU)
