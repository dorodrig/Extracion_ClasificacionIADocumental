# Solicitud de Revisión — Agente Backend — HU-01 CA-01 a CA-06

| Campo | Valor |
|---|---|
| **Agente** | Backend |
| **Rama** | `HU1_CA1-CA6_DEVDAVID_ITEREACION1` |
| **Fecha** | 2026-05-23 |
| **Estado** | PENDIENTE APROBACIÓN ARQUITECTO |

---

## Resumen del Plan Propuesto

Implementación completa del CRUD de Reglas de Trabajo para la HU-01 (CA-01 a CA-06). Se creará toda la estructura backend desde cero siguiendo Clean Architecture (Ports & Adapters) según la Gobernanza v1.1.0.

### Endpoints a implementar:
| Método | Ruta | Descripción | HTTP Code |
|---|---|---|---|
| GET | `/api/v1/rules?cliente_id={id}` | Listar reglas por cliente | 200 |
| GET | `/api/v1/rules/{id}` | Detalle de una regla | 200 |
| POST | `/api/v1/rules` | Crear nueva regla | 201 |
| PUT | `/api/v1/rules/{id}` | Actualizar regla | 200 |

---

## Archivos que planeo crear (rutas absolutas)

### Estructura Base
- `C:\zData\ExtracionDatosIA\BackEnd\app\main.py` — Entry point FastAPI
- `C:\zData\ExtracionDatosIA\BackEnd\app\__init__.py`
- `C:\zData\ExtracionDatosIA\BackEnd\app\core\config.py` — Settings (pydantic-settings)
- `C:\zData\ExtracionDatosIA\BackEnd\app\core\dependencies.py` — get_db + mock auth
- `C:\zData\ExtracionDatosIA\BackEnd\app\core\__init__.py`
- `C:\zData\ExtracionDatosIA\BackEnd\app\db\database.py` — Engine + SessionLocal
- `C:\zData\ExtracionDatosIA\BackEnd\app\db\__init__.py`

### Capa de Dominio
- `C:\zData\ExtracionDatosIA\BackEnd\app\domain\models\rule.py` — Entidad pura
- `C:\zData\ExtracionDatosIA\BackEnd\app\domain\rules\rule_validation.py` — Reglas de negocio
- `C:\zData\ExtracionDatosIA\BackEnd\app\domain\exceptions.py` — GRMException hierarchy
- `C:\zData\ExtracionDatosIA\BackEnd\app\domain\__init__.py`
- `C:\zData\ExtracionDatosIA\BackEnd\app\domain\models\__init__.py`
- `C:\zData\ExtracionDatosIA\BackEnd\app\domain\rules\__init__.py`

### Capa de Infraestructura
- `C:\zData\ExtracionDatosIA\BackEnd\app\db\models\rule_db.py` — SQLAlchemy Model
- `C:\zData\ExtracionDatosIA\BackEnd\app\db\models\__init__.py`
- `C:\zData\ExtracionDatosIA\BackEnd\app\db\repositories\rule_repository.py` — Repository Pattern
- `C:\zData\ExtracionDatosIA\BackEnd\app\db\repositories\__init__.py`

### Capa de Aplicación
- `C:\zData\ExtracionDatosIA\BackEnd\app\services\rule_service.py` — Use Case / Service
- `C:\zData\ExtracionDatosIA\BackEnd\app\services\__init__.py`

### Capa API
- `C:\zData\ExtracionDatosIA\BackEnd\app\schemas\rule_schema.py` — Pydantic Schemas
- `C:\zData\ExtracionDatosIA\BackEnd\app\schemas\__init__.py`
- `C:\zData\ExtracionDatosIA\BackEnd\app\api\v1\endpoints\rules.py` — Endpoints REST
- `C:\zData\ExtracionDatosIA\BackEnd\app\api\v1\endpoints\__init__.py`
- `C:\zData\ExtracionDatosIA\BackEnd\app\api\v1\router.py` — Router registry
- `C:\zData\ExtracionDatosIA\BackEnd\app\api\v1\__init__.py`
- `C:\zData\ExtracionDatosIA\BackEnd\app\api\__init__.py`

### Configuración
- `C:\zData\ExtracionDatosIA\BackEnd\requirements.txt`
- `C:\zData\ExtracionDatosIA\BackEnd\.env.example`

### Tests
- `C:\zData\ExtracionDatosIA\BackEnd\tests\__init__.py`
- `C:\zData\ExtracionDatosIA\BackEnd\tests\test_rule_validation.py`
- `C:\zData\ExtracionDatosIA\BackEnd\tests\test_rules_api.py`

---

## Decisiones Técnicas Clave

1. **Mock de Auth Guard**: HU-08 no está implementada. Se crea `require_role` como mock que permite todas las solicitudes, pero con la interfaz correcta de `Depends()` para reemplazar fácilmente cuando HU-08 esté lista.

2. **`campos_extraer` como JSON en NVARCHAR(MAX)**: Siguiendo Gobernanza §5.2. Se serializa con `json.dumps()` al guardar y `json.loads()` al leer.

3. **Validación de nombres duplicados case-insensitive**: CA-06 requiere que no haya campos con el mismo nombre. Se normaliza a `lower()` antes de comparar.

4. **APIResponse genérico**: Toda respuesta envuelta en `APIResponse(success, data, message, error)` según Gobernanza §3.2.

5. **Transacciones atómicas**: `create` y `update` usan `try/commit/except/rollback` para garantizar atomicidad (mitigación R-03).

6. **Version auto-incremento**: En `PUT /rules/{id}`, el campo `version` se incrementa automáticamente.

---

## Riesgos Identificados

| ID | Riesgo | Severidad | Mitigación |
|---|---|---|---|
| R-03 | Manejo incorrecto de transacciones SQL | Alta | try/commit/except/rollback en repositorio |
| R-AUTH | HU-08 no disponible | Media | Mock temporal con Depends(), interfaz lista para inyección |
| R-DB | Tabla `reglas_trabajo` podría no existir | Media | Se asume existente por HU-10. Si no existe, se crea migration Alembic |
| R-JSON | Datos corruptos en `campos_extraer` | Baja | Validación Pydantic antes de serializar + try/except al deserializar |

---

## Preguntas para el Arquitecto (si las hay)

1. **¿La tabla `reglas_trabajo` ya existe en la BD?** El handoff indica HU-10 completada, pero no encontré scripts SQL. Si no existe, crearé la migración Alembic.

2. **¿Se requiere soft-delete para reglas?** La Gobernanza menciona `activo BIT DEFAULT 1` y el handoff no lista DELETE endpoint. Asumo que por ahora no se implementa DELETE, pero el campo `activa` está en el modelo.

3. **¿El `created_by` debe ser obligatorio?** Con el mock de auth no tendremos usuario real. Propongo hacerlo nullable hasta que HU-08 esté integrada.

---

## Alineación con Gobernanza

- [x] §2.2 Estructura de directorios obligatoria
- [x] §3.1 Nombrado Python (snake_case)
- [x] §3.2 Endpoints REST (plurales, versión v1, APIResponse)
- [x] §3.3 Excepciones de dominio tipadas (GRMException)
- [x] §3.4 Clean Architecture (Repository/Service/Endpoint)
- [x] §3.5 Logging con `logging.getLogger("grm.*")`
- [x] §6.1 Variables de entorno externalizadas
- [x] §12.2 Conventional Commits
