# Solicitud de Aprobación - Backend HU-02

**Para:** Arquitecto Líder
**De:** Agente Backend
**Fecha:** 2026-05-23
**Rama:** `HU2_CA1-CA4_DevDamian_ITEREACION1`

## Resumen del plan propuesto
Implementación del endpoint REST `POST /api/v1/batches` para la creación inicial de lotes de procesamiento, ya sea mediante Escáner o Carpeta Local (CA-01 a CA-04 de HU-02). Se incluye el schema de base de datos (`lotes_procesamiento`), modelos Pydantic, capa de servicio, y capa API REST bajo Clean Architecture y la Gobernanza.

## Archivos que se crearán/modificarán
- `BackEnd/app/db/models/batches.py` [NEW]
- `BackEnd/app/schemas/batches.py` [NEW]
- `BackEnd/app/domain/models/batch.py` [NEW]
- `BackEnd/app/services/batch_service.py` [NEW]
- `BackEnd/app/api/v1/endpoints/batches.py` [NEW]
- `BackEnd/app/api/v1/router.py` [MODIFY]

## Decisiones técnicas clave
- Se usará el wrapper `APIResponse` exigido por Gobernanza §3.2.
- Validación restrictiva de `modo_ingesta` ("scanner" o "carpeta") usando Enum/Pydantic Validators.
- El `batch_id` (UUID) se generará a nivel servicio al registrar el lote, estado inicial "preparando".
- Se protegerá el endpoint con dependencias RBAC (roles admitidos: `admin`, `operario`).

## Preguntas para el Arquitecto
1. ¿Asumimos que el esquema de BD base (por HU-10) ya incluye las tablas relacionadas como `reglas_trabajo` y `clientes` para las Foreign Keys, o debo crear mocks transitorios?
2. La ruta temporal especifica el formato `/temp/{batch_id}/{timestamp}/`. ¿El backend local debe crear efectivamente esta carpeta en disco en el endpoint POST, o solo generará el registro del path para que un paso posterior la cree (CA-07)? (Por defecto asumiré solo el guardado de la ruta esperada).

## Riesgos Identificados
- Dependencia de Foreign Keys (`regla_id`, `cliente_id`, `operario_id`). Si no existen los registros previos, podría haber fallos de integridad referencial durante las pruebas manuales locales.
