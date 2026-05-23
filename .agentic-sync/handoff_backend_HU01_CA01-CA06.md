# Handoff — Backend — HU-01
## Iteración: 1-DEV-HU-1

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_backend_HU01_CA01-CA06.md`               |
| **Rol Destino**          | Agente Backend                                    |
| **HU de Origen**         | HU-01 — Configuración y Gestión de Reglas de Trabajo del Cliente |
| **CAs Asignados**        | CA-01, CA-02, CA-03, CA-04, CA-05, CA-06          |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-1                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI 0.115 + SQLAlchemy + Alembic
- [x] Frontend: React 18 + TypeScript + Vite 5
- [x] Estilos: SASS/SCSS (preprocesador) — CSS puro como fallback justificado
- [x] Base de Datos: SQL Server 2019+ (SQLAlchemy ORM)
- [x] SDKs: google-generativeai (Gemini) + boto3 (Textract)
- [x] Cola: Celery 5 + Redis

### Patrón Arquitectónico
- [x] Clean Architecture (Ports & Adapters)
- [x] Capas: Infraestructura → Aplicación → Dominio
- [x] Inversión de Dependencias (Ports/Interfaces en capa dominio)

### Preparación Cloud-Ready
- [x] Adapters reemplazables sin cambiar dominio
- [x] Variables de entorno externalizadas (.env)
- [x] CERO credenciales hardcodeadas

### ISO/IEC 25010
- [x] Mantenibilidad: Modularidad, modificabilidad, testeabilidad
- [x] Seguridad: JWT + RBAC + aislamiento de contexto IA
- [x] Eficiencia de Desempeño: Paginación, índices, async/Celery

### Riesgos Identificados
> R-03: Manejo incorrecto de transacciones SQL. Asegurar que las operaciones de creación y actualización (CAs 04, 05, 06) sean atómicas. El campo `campos_extraer` debe almacenarse como JSON válido.

## Historia de Usuario — Contexto

> **Como** Operario de Digitalización o Administrador del sistema,
> **Quiero** crear, visualizar, editar y seleccionar Reglas de Trabajo configuradas por cliente,
> **Para que** el sistema de extracción y clasificación sepa exactamente qué campos extraer, con qué estructura organizar los documentos en carpetas y bajo qué parámetros operar, sin ambigüedad ni intervención manual adicional.

### Descripción Funcional
Implementación de la gestión de Reglas de Trabajo (CRUD básico). El backend debe proveer endpoints para consultar reglas por cliente, obtener el detalle de una regla, y crear/actualizar reglas. Se requiere validación estricta de campos obligatorios (cliente, nombre, tipo_doc, patron_carpeta, modo_entrada, campos_extraer) y nombres únicos por cliente.

## Criterios de Aceptación

### CA-01 — Primer acceso de cliente sin reglas previas
```gherkin
Dado que el operario ha seleccionado un cliente que NO tiene reglas registradas en el sistema
Cuando el sistema carga la sección "Reglas de Trabajo"
Entonces el sistema muestra el formulario de creación de regla completamente vacío
  Y muestra el mensaje informativo: "Este cliente no tiene reglas configuradas. Crea la primera regla."
  Y el botón "Guardar Regla" permanece deshabilitado hasta que todos los campos obligatorios estén completos
```
**Notas de implementación para el agente:**
> Backend: Implementar endpoint `GET /api/v1/rules?cliente_id={id}` que retorne una lista vacía `[]` si no hay reglas.

### CA-02 — Visualización del listado de reglas de un cliente con reglas existentes
```gherkin
Dado que el cliente seleccionado tiene una o más reglas registradas
Cuando el operario accede a la sección "Reglas de Trabajo"
Entonces el sistema muestra una tabla/listado con todas las reglas del cliente
  Y cada fila muestra: Nombre de regla, Tipo de documento, Fecha de creación, Última modificación, Versión
  Y cada fila ofrece los botones de acción: "Editar", "Iniciar Proceso", "Ver Detalle"
```
**Notas de implementación para el agente:**
> Backend: El mismo endpoint `GET /api/v1/rules?cliente_id={id}` debe retornar la lista de reglas serializadas correctamente con sus campos base, ordenadas por fecha de creación o modificación (descendente).

### CA-03 — Carga de regla existente para edición
```gherkin
Dado que el operario visualiza el listado de reglas del cliente
Cuando hace clic en el botón "Editar" sobre una regla específica
Entonces el sistema carga el formulario con todos los valores actuales de esa regla pre-rellenados
  Y todos los campos del formulario están en modo editable
  Y el botón principal del formulario muestra el texto "Actualizar Regla" (no "Guardar Regla")
```
**Notas de implementación para el agente:**
> Backend: Implementar endpoint `GET /api/v1/rules/{id}` que retorne el detalle completo de la regla, incluyendo el JSON parseado de `campos_extraer`.

### CA-04 — Creación de una nueva regla adicional para cliente con reglas existentes
```gherkin
Dado que el cliente ya tiene al menos una regla registrada
Cuando el operario hace clic en el botón "Nueva Regla"
Entonces el sistema abre el formulario de regla completamente vacío
  Y genera un nuevo ID único para la nueva regla
  Y las reglas existentes del cliente no son modificadas ni sobreescritas
```
**Notas de implementación para el agente:**
> Backend: Implementar endpoint `POST /api/v1/rules`. Generará el ID automáticamente (IDENTITY en BD).

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
**Notas de implementación para el agente:**
> Backend: El schema Pydantic `RuleCreate` debe validar la obligatoriedad de estos campos. `campos_extraer` debe ser una lista de al menos 1 elemento.

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
**Notas de implementación para el agente:**
> Backend: Pydantic schema para `CampoExtraer` (nombre, tipo, obligatorio). Validación a nivel de dominio: prohibir nombres duplicados (case-insensitive) dentro del array de campos de la regla antes de insertar en DB.

## Especificaciones Técnicas — Backend

### Estructura de Directorios
> Referencia: Gobernanza §2.2 — Estructura de directorios obligatoria del Backend
- `app/api/v1/endpoints/rules.py`
- `app/domain/models/rule.py`
- `app/domain/rules/rule_validation.py`
- `app/schemas/rule_schema.py`
- `app/services/rule_service.py`
- `app/db/repositories/rule_repository.py`
- `app/db/models/rule_db.py`

### Endpoints API REST
| Método | Ruta                        | Descripción                          | Auth    |
|--------|-----------------------------|--------------------------------------|---------|
| GET    | `/api/v1/rules`             | Listar reglas (query: cliente_id)    | Adm/Ope |
| GET    | `/api/v1/rules/{id}`        | Obtener detalle de una regla         | Adm/Ope |
| POST   | `/api/v1/rules`             | Crear nueva regla                    | Adm/Ope |
| PUT    | `/api/v1/rules/{id}`        | Actualizar regla                     | Adm/Ope |

### Schemas Pydantic (Entrada/Salida)
- `CampoExtraer`: nombre (str), tipo (str), obligatorio (bool).
- `RuleCreate`: cliente_id, nombre, tipo_documento, campos_extraer (List[CampoExtraer], min_length=1), patron_carpeta, modo_entrada.
- `RuleResponse`: Hereda de RuleCreate + id, version, activa, created_at, updated_at.

### Modelo de Datos (SQLAlchemy)
- Tabla `reglas_trabajo`: id, cliente_id, nombre, tipo_documento, campos_extraer (NVARCHAR(MAX) JSON), patron_carpeta, modo_entrada, umbral_ocr (default 95.00), version (default 1), activa (default 1), created_by, created_at, updated_at.

### Reglas de Negocio
- Ningún nombre de campo dentro de `campos_extraer` puede repetirse en la misma regla.
- `campos_extraer` debe contener al menos 1 campo.
- `modo_entrada` debe ser 'scanner' o 'carpeta'.

## Estándares de Código — Referencia Gobernanza

> El agente DEBE adherirse a los estándares definidos en la Gobernanza Arquitectónica:
> Ruta: `C:\zData\ExtracionDatosIA\Documentancion\Gobernanza_Arquitectura.md`

### Estándares aplicables a este Handoff:
- §3.1 Nombrado Python (snake_case)
- §3.2 Endpoints REST (plurales, versión v1)
- §3.3 Excepciones de dominio tipadas (GRMException)
- §3.4 Clean Architecture (Separación Repository/Service)

### Convención de Commits (Conventional Commits)
```
feat(HU-01): implementación endpoints CRUD para Reglas de Trabajo
```

## Dependencias y Pre-condiciones

### Requiere completado antes:
- [x] HU-10 (Schema BD) - Asumimos tabla base. Si la tabla no existe en Alembic, debes crear la migración.
- [x] HU-08 (Auth) - Usar mock temporal para Auth Guard si HU-08 no está lista en código, pero respetar inyección de dependencias.

### Produce entregables para:
- [ ] Frontend HU-01 (consumirá estos endpoints)

### Archivos que NO debe modificar (fuera de su jurisdicción):
- Cualquier archivo en `FrontEnd/`

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
   - Analiza cada CA asignado y desglosa las tareas técnicas.
   - Identifica riesgos y dependencias.
   - Estima el esfuerzo por tarea.

2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El Humano es solo un cartero. No tiene autoridad técnica para aprobar ni rechazar planes.

3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
   
   El archivo debe contener:
   - Resumen del plan propuesto
   - Archivos que planeas crear/modificar (con rutas absolutas)
   - Decisiones técnicas clave tomadas
   - Preguntas para el Arquitecto (si las hay)
   - Riesgos identificados

4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."

5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación explícita del Arquitecto Líder (transmitida por el Humano Cartero), pasa a modo `EXECUTION`.

6. **En modo `EXECUTION`:**
   - Codifica siguiendo estrictamente los estándares de la Gobernanza.
   - Haz `git add`, `git commit` (con Conventional Commits) y `git push` a la rama indicada.
   - Actualiza el `task.md` con el progreso.

7. **Al terminar la ejecución:**
   - Genera un `walkthrough.md` con resumen de cambios.
   - Notifica al Humano: *"He completado mi trabajo. Los cambios están en la rama HU1_CA1-CA6_DEVDAVID_ITEREACION1. Avísale al Arquitecto."*
