# Solicitud de Revisión — Backend — HU-01 Parte 2 (CA-07 a CA-13)

| Campo                   | Valor                                              |
|-------------------------|----------------------------------------------------|
| **Rol Solicitante**     | Agente Backend (Desarrollador)                     |
| **Iteración**           | 2-DEV-HU-1                                        |
| **Rama Git**            | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **CAs Cubiertos**       | CA-07, CA-10, CA-11, CA-12, CA-13                  |
| **Fecha**               | 2026-05-23                                        |
| **Estado**              | PENDIENTE DE APROBACIÓN                            |

## Resumen del Plan

### CA-07 — Validación del patrón de carpeta de salida
- Nueva función `validate_patron_carpeta()` en `rule_validation.py`
- Extrae variables `{var}` del patrón y verifica que al menos una coincida con un campo en `campos_extraer`
- Nueva excepción `InvalidPatronCarpetaException`
- Se integra en `validate_rule_data()` invocada en CREATE y UPDATE

### CA-10 — Versionamiento automático con histórico
- Nuevo modelo `ReglasTrabajoHistorial` en `rule_history_db.py`
- Nueva migración Alembic `002_create_reglas_trabajo_historial`
- Tabla: `id, regla_id, version, snapshot_json, modificado_por, modificado_at`
- En `repository.update()`: se guarda snapshot antes de aplicar cambios
- Versión se incrementa automáticamente (comportamiento existente, ahora con historial)

### CA-11 — Duplicar regla
- Nuevo endpoint `POST /api/v1/rules/{id}/duplicate`
- Clona la regla con copia profunda de `campos_extraer`
- Nombre con sufijo `" (Copia)"`, incremental si ya existe
- Reinicia `version = 1`

### CA-12 — Validación nombre único con HTTP 409
- Nuevo exception handler específico para `RuleNameAlreadyExistsException → 409 Conflict`
- Refuerzo del manejo existente (antes retornaba 400 genérico)

### CA-13 — Validación modo_entrada
- Ya implementada en Sprint anterior (`validate_modo_entrada()`)
- Se refuerza con documentación. Sin cambio funcional.

## Archivos a Modificar/Crear

| Acción   | Archivo                                                |
|----------|--------------------------------------------------------|
| MODIFY   | `app/domain/exceptions.py`                             |
| MODIFY   | `app/domain/rules/rule_validation.py`                  |
| NEW      | `app/db/models/rule_history_db.py`                     |
| NEW      | `alembic/versions/002_create_reglas_trabajo_historial.py` |
| MODIFY   | `app/db/repositories/rule_repository.py`               |
| MODIFY   | `app/services/rule_service.py`                         |
| MODIFY   | `app/api/v1/endpoints/rules.py`                        |
| MODIFY   | `app/main.py`                                          |
| MODIFY   | `tests/test_rule_validation.py`                        |
| MODIFY   | `tests/test_rules_api.py`                              |

## Riesgos Mitigados

- **R-05**: Duplicación usa `json.loads(json.dumps(...))` para copia profunda segura + sufijo incremental para unicidad.
- **R-06**: Regex `\{(\w+)\}` extrae variables y se comparan case-insensitive contra `campos_extraer`.

## Verificación Propuesta

```bash
python -m pytest tests/ -v
```

- Todos los tests existentes CA-01 a CA-06 deben seguir pasando (backward compatible)
- Nuevos tests para CA-07, CA-10, CA-11, CA-12, CA-13
