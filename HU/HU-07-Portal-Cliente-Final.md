# HU-07 — Portal Web de Consulta para Cliente Final

## Metadatos

| Campo                        | Valor                                                                    |
| ---------------------------- | ------------------------------------------------------------------------ |
| **ID**                       | HU-07                                                                    |
| **Épica**                    | Portal de Consulta y Entrega al Cliente                                  |
| **Esfuerzo Principal**       | 🖥️ Frontend UI + ⚙️ Backend (API de consulta, visor de documentos)       |
| **Prioridad**                | 🟡 Media — Entrega de valor al cliente final                             |
| **Story Points Estimados**   | 8                                                                        |
| **Sprint Sugerido**          | Sprint 3                                                                 |
| **Roles Involucrados**       | Cliente Final                                                            |

---

## Historia de Usuario

> **Como** Cliente Final de GRM,
> **Quiero** acceder a un portal web donde pueda consultar mis documentos digitalizados, ver los datos extraídos de cada uno, visualizar el documento original y navegar por la estructura de carpetas donde fueron organizados,
> **Para que** pueda acceder a mi información de forma autónoma, segura y organizada, sin necesidad de contactar al equipo operativo para buscar documentos.

---

## Descripción Funcional

El portal del cliente es la interfaz de entrega final del sistema GRM. El cliente accede con su Cédula de Ciudadanía y contraseña, y tiene acceso **exclusivo a su propia información**, sin posibilidad de ver datos de otros clientes.

### Secciones del Portal

#### 1. Dashboard Principal
- Resumen: total de documentos procesados, tipos de documentos, última fecha de procesamiento
- Acceso rápido a últimos documentos procesados

#### 2. Explorador de Documentos (Vista árbol de carpetas)
- Navegación visual de la estructura de carpetas generada por el Agente de Clasificación
- Árbol expandible: `/CC/{NOMBRE}/{TIPO_DOC}/`
- Al hacer clic en un documento del árbol, abre el visor

#### 3. Tabla de Documentos
- Lista de todos sus documentos con: tipo, nombre de archivo, fecha de procesamiento, campos clave extraídos (ej: CC, nombre)
- Búsqueda por campos, filtros por tipo de documento y fechas

#### 4. Visor de Documentos (solo lectura)
- Renderizado del documento original (PDF/imagen) en pantalla
- Panel lateral con los datos extraídos y validados
- Sin posibilidad de edición (solo lectura para el cliente)

---

## Criterios de Aceptación (BDD / Gherkin)

### CA-01 — Acceso al portal con credenciales del cliente
```gherkin
Dado que el cliente accede a la URL del portal web de GRM
Cuando el sistema presenta la pantalla de login
Entonces el cliente puede autenticarse ingresando su Número de Cédula de Ciudadanía y contraseña
  Y tras la autenticación exitosa, el sistema redirige al Dashboard del cliente
  Y el nombre del cliente se muestra en la cabecera del portal: "Bienvenido, {NOMBRE_COMPLETO}"
```

### CA-02 — Visualización del Dashboard con resumen de documentos
```gherkin
Dado que el cliente ha iniciado sesión exitosamente en el portal
Cuando el sistema carga el Dashboard
Entonces muestra las siguientes métricas del cliente:
    | Métrica                                | Descripción                                   |
    | Total de documentos procesados         | Número total de documentos en el sistema      |
    | Tipos de documentos                    | Distribución por tipo (Pagaré, Cédula, etc.)  |
    | Fecha del último procesamiento         | Fecha y hora del lote más reciente            |
    | Documentos nuevos (últimas 24h)        | Contador con acceso directo                   |
  Y el Dashboard solo muestra información del cliente autenticado, sin datos de otros clientes
```

### CA-03 — Explorador de carpetas con árbol de navegación
```gherkin
Dado que el cliente accede a la sección "Mis Documentos"
Cuando el sistema carga el explorador
Entonces muestra un árbol de carpetas expandible con la estructura generada por el agente:
    /{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/
  Y cada nodo del árbol es expandible/colapsable con clic
  Y los archivos (hojas del árbol) muestran el ícono del tipo de archivo y el nombre del documento
  Y al hacer clic en un archivo del árbol, abre el visor de documentos (CA-05)
```

### CA-04 — Tabla de documentos con búsqueda y filtros
```gherkin
Dado que el cliente accede a la sección "Lista de Documentos"
Cuando el sistema carga la tabla
Entonces muestra todos sus documentos en una tabla paginada con las columnas:
    | Columna               | Descripción                                        |
    | Nombre de archivo     | Nombre del documento con ícono de tipo             |
    | Tipo de documento     | Pagaré / Cédula / Endoso / etc.                    |
    | Campos clave          | CC, Nombre (valores extraídos principales)          |
    | Fecha de procesamiento| Fecha y hora en que fue clasificado                |
    | Acciones              | Botón "Ver Documento"                              |
  Y permite filtrar por: tipo de documento (dropdown), rango de fechas
  Y permite buscar por texto en los campos clave (número de cédula, nombre)
```

### CA-05 — Visor de documentos para el cliente (solo lectura)
```gherkin
Dado que el cliente hace clic en "Ver Documento" o en un archivo del árbol de carpetas
Cuando el sistema abre el visor
Entonces muestra el documento original (PDF/imagen) renderizado en el panel principal
  Y muestra en el panel lateral todos los campos extraídos con sus valores validados
  Y todos los campos del panel lateral están en modo solo lectura (no editables por el cliente)
  Y muestra la ruta de organización del documento: "Ubicado en: /CC123456789/DAVID_RODRIGUEZ/PAGARE/"
```

### CA-06 — Navegación por páginas del documento en el visor
```gherkin
Dado que el cliente tiene un documento multipágina abierto en el visor
Cuando navega el documento
Entonces dispone de controles: "Página anterior", "Página siguiente", indicador "Página X de N"
  Y puede hacer zoom in/out con controles en pantalla
  Y puede descargar el documento en formato PDF haciendo clic en el botón "Descargar"
```

### CA-07 — Descarga de documentos
```gherkin
Dado que el cliente visualiza un documento en el visor
Cuando hace clic en el botón "Descargar"
Entonces el sistema descarga el archivo PDF original al equipo del cliente
  Y el nombre del archivo descargado corresponde al nombre original del documento
  Y el sistema registra en el log de auditoría: cliente_id, documento_id, acción="descarga", timestamp
```

### CA-08 — Aislamiento total de datos por cliente
```gherkin
Dado que el cliente está autenticado en el portal
Cuando accede a cualquier sección del portal (Dashboard, Explorador, Lista, Visor)
Entonces el sistema filtra automáticamente todos los datos para mostrar exclusivamente los documentos del cliente autenticado
  Y si un cliente intenta acceder directamente a la URL de un documento de otro cliente (ej: /api/documentos/{id_ajeno}), el sistema retorna HTTP 403 Forbidden
  Y registra el intento de acceso no autorizado en el log de seguridad
```

### CA-09 — Indicador de estado de documentos pendientes del cliente
```gherkin
Dado que el cliente accede al portal y tiene documentos que aún están en cola de revisión humana
Cuando el Dashboard carga
Entonces muestra una sección "Documentos en proceso" con el conteo de documentos que aún están siendo revisados
  Y muestra el estado: "X documento(s) en revisión por el equipo de digitalización"
  Y NO muestra el contenido de los documentos pendientes hasta que hayan sido clasificados exitosamente
```

### CA-10 — Sesión de usuario y cierre de sesión
```gherkin
Dado que el cliente está autenticado en el portal
Cuando su sesión supera el tiempo de inactividad de 30 minutos sin interacción
Entonces el sistema cierra automáticamente la sesión y redirige al login con el mensaje: "Tu sesión ha expirado por inactividad. Inicia sesión nuevamente."
  Y cuando el cliente hace clic en "Cerrar Sesión", el sistema invalida el token de sesión y redirige al login
  Y el sistema confirma el cierre de sesión con el mensaje: "Has cerrado sesión exitosamente."
```

### CA-11 — Diseño responsive y accesible
```gherkin
Dado que el cliente accede al portal desde diferentes dispositivos
Cuando el sistema renderiza el portal en pantallas de escritorio (≥1024px) o tablets (768px-1023px)
Entonces el layout se adapta correctamente a cada tamaño de pantalla
  Y todos los elementos interactivos tienen contraste suficiente (WCAG AA mínimo)
  Y el visor de documentos es funcional en ambas resoluciones
```

### CA-12 — Visualización de la estructura de carpetas del documento en el visor
```gherkin
Dado que el cliente visualiza un documento en el visor
Cuando el panel de información del documento está cargado
Entonces el sistema muestra la estructura de carpetas donde está organizado el documento de forma visual
  Ejemplo:
  📁 CC123456789
    └── 📁 DAVID_RODRIGUEZ
        └── 📁 PAGARE
            └── 📄 pagare_001.pdf  ← (documento actual)
  Y esta visualización ayuda al cliente a entender el sistema de organización de sus documentos
```

---

## Notas Técnicas

### Endpoints API REST (solo lectura para cliente)
| Método | Ruta                                           | Descripción                                        |
|--------|------------------------------------------------|----------------------------------------------------|
| GET    | `/api/cliente/dashboard`                        | Métricas del cliente autenticado                   |
| GET    | `/api/cliente/documentos`                       | Lista paginada de documentos del cliente           |
| GET    | `/api/cliente/documentos/{id}`                  | Detalle de un documento (datos + campos)           |
| GET    | `/api/cliente/documentos/{id}/archivo`          | Servir el archivo PDF/imagen para el visor         |
| GET    | `/api/cliente/carpetas`                         | Árbol de carpetas del cliente                      |
| GET    | `/api/cliente/documentos/{id}/descargar`        | Descarga del archivo                               |

### Consideraciones de Seguridad
- Todos los endpoints requieren JWT válido con claim `cliente_id`
- El backend valida en CADA petición que el `documento_id` solicitado pertenece al `cliente_id` del JWT
- Los archivos son servidos por el backend (streaming), nunca exponiendo la ruta física del servidor

### Dependencias
- **Depende de**: HU-05 (documentos clasificados disponibles), HU-08 (Auth — rol Cliente)
- **Extensión futura**: Integración con WhatsApp Business Chatbot (HU opcional — activar si el Dev lo requiere)
