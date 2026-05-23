# Solicitud de Revisión — Backend — HU-04

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Agente Solicitante**   | Agente Backend                                    |
| **HU**                   | HU-04 — Agente de Contexto IA (Google Gemini)     |
| **CAs Cubiertos**        | CA-01 al CA-12 (todos)                            |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-4                                        |
| **Fecha de Solicitud**   | 2026-05-23                                        |
| **Estado**               | ⏳ Pendiente Revisión del Arquitecto               |

---

## Resumen del Plan

He elaborado un plan de implementación completo para HU-04 que cubre los 12 criterios de aceptación. El plan sigue estrictamente la **Clean Architecture** definida en la Gobernanza.

### Archivos a Crear (15 nuevos)

| Archivo | Propósito | CAs |
|---------|-----------|-----|
| `app/db/models/contexto_resultado_db.py` | Modelo ORM `AgenteContextoResultados` | CA-12 |
| `app/db/models/log_ia_invocacion_db.py` | Modelo ORM `LogIAInvocacion` | CA-09 |
| `app/domain/exceptions_ia.py` | Excepciones tipadas IA (`GRMException` hierarchy) | CA-02, CA-03, CA-07, CA-08 |
| `app/domain/rules/normalizer.py` | Normalización: Identificación, Fecha, Texto | CA-11 |
| `app/services/gemini_adapter.py` | Adapter SDK Gemini (timeout, retries, aislamiento) | CA-02, CA-08, CA-10 |
| `app/services/prompt_builder.py` | Prompt dinámico: reglas HU-01 + datos OCR HU-03 | CA-01 |
| `app/services/contexto_ia_service.py` | Orquestador principal del agente | CA-03–CA-07, CA-09, CA-11, CA-12 |
| `app/db/repositories/contexto_resultado_repository.py` | Repository para `agente_contexto_resultados` | CA-12 |
| `app/db/repositories/log_ia_repository.py` | Repository para `log_ia_invocaciones` | CA-09 |
| `app/schemas/contexto_schema.py` | Schemas Pydantic de entrada/salida | CA-12 |
| `app/api/v1/endpoints/contexto.py` | Endpoints REST (`/contexto-ia/procesar`, `/resultado`) | Todos |
| `alembic/versions/003_create_agente_contexto_resultados.py` | Migración Alembic (ambas tablas) | CA-12 |
| `tests/test_normalizer.py` | Tests unitarios normalización | CA-11 |
| `tests/test_prompt_builder.py` | Tests unitarios prompt builder | CA-01, CA-10 |
| `tests/test_contexto_ia_service.py` | Tests integración con mock Gemini | CA-03–CA-09, CA-11, CA-12 |

### Archivos a Modificar (5)

| Archivo | Cambio |
|---------|--------|
| `requirements.txt` | + `google-generativeai>=0.8.0` |
| `app/core/config.py` | Activar settings Gemini |
| `.env.example` | Descomentar variables Gemini |
| `app/db/models/__init__.py` | Exportar nuevos modelos |
| `alembic/env.py` | Importar nuevos modelos |
| `app/api/v1/router.py` | Registrar router contexto |

---

## Decisiones de Diseño

1. **GeminiAdapter como Adapter de Infraestructura**: Siguiendo Clean Architecture, el adapter es reemplazable sin tocar el dominio. Si mañana se cambia Gemini por otro modelo, solo se sustituye este archivo.

2. **Invocación one-shot (CA-10)**: Cada llamada a Gemini usa `generate_content()` sin chat/historial. No se reutiliza sesión entre documentos.

3. **Backoff exponencial (CA-08)**: 2s, 4s, 8s para errores de API. Separado del reintento por JSON inválido (CA-03) que reintenta inmediatamente hasta 2 veces.

4. **Dos tipos de reintento**:
   - **CA-03**: Reintento por parseo JSON (2 reintentos, mismo prompt) — lógica en `contexto_ia_service`
   - **CA-08**: Reintento por timeout/error HTTP (3 reintentos, backoff) — lógica en `gemini_adapter`

5. **Normalización post-IA (CA-11)**: Se aplica DESPUÉS de recibir la respuesta de Gemini, preservando el valor original para trazabilidad.

---

## Preguntas para el Arquitecto

> Ninguna pregunta pendiente. El handoff y la HU-04 son suficientemente detallados para proceder.

---

## Solicitud

Solicito aprobación del Arquitecto Líder para proceder a la fase de **EJECUCIÓN** del plan descrito. El plan cumple con:

- [x] Gobernanza §2.2 — Estructura de directorios
- [x] Gobernanza §3.3 — Excepciones tipadas (GRMException)
- [x] Gobernanza §3.4 — Clean Architecture
- [x] Gobernanza §5.1 — Nombrado SQL (snake_case, plural, español)
- [x] Gobernanza §5.2 — Columnas de auditoría
- [x] Gobernanza §6.1 — Cero credenciales hardcodeadas
- [x] Handoff HU-04 — Todos los CAs del CA-01 al CA-12
- [x] Riesgos R-IA-1 y R-IA-2 mitigados
