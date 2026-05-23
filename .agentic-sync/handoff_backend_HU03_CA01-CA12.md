# Handoff — Backend — HU-03
## Iteración: 1-DEV-HU-3

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_backend_HU03_CA01-CA12.md`               |
| **Rol Destino**          | Agente Backend                                    |
| **HU de Origen**         | HU-03 — Integración AWS Textract OCR              |
| **CAs Asignados**        | CA-01 al CA-12                                    |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-3                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI 0.115 + SQLAlchemy + Alembic + Celery 5 + boto3
- [x] Storage: Clean Architecture Ports & Adapters (No hardcoded credentials)

### Riesgos Identificados
> R-AWS-1: Consumo excesivo de cuota o rate limits de Textract. Implementar retry con backoff exponencial.
> R-AWS-2: Bloqueo del Event Loop de FastAPI. El llamado síncrono a AWS SDK (`boto3`) debe envolverse en `run_in_threadpool` o preferiblemente ejecutarse dentro de un Worker de Celery.

## Criterios de Aceptación Asignados al Backend

- **CA-01**: Cargar `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` usando pydantic-settings. Lanzar error claro si no existen y loggear. NUNCA hardcodear.
- **CA-02**: Procesamiento síncrono por página manteniendo secuencialidad.
- **CA-03**: Parsear bloques. Si confianza < 95%, marcar "Baja confianza".
- **CA-04**: Manejar errores de AWS (timeout, límites). Loggear. Reintentos (1s, 2s, 4s). Si fallan, marcar como "Error en OCR".
- **CA-05**: Consolidar páginas en un solo objeto de documento. Calcular score promedio. Estado "OCR Completado".
- **CA-06**: SLA de tiempo (1-3 págs <= 60s, 4+ págs <= 120s). Si se pasa, loggear "SLA Superado" y emitir alerta (no cancelar).
- **CA-07**: `detect_document_text` para Texto general/Endoso. `analyze_document` (FORMS/TABLES) para otros.
- **CA-08**: Guardar resultado en tabla `ocr_resultados_paginas` (incluyendo raw json y parseado). *Debes crear la migración Alembic para esta tabla*.
- **CA-09**: Procesar JPG/PNG/TIFF leyendo bytes a Textract.
- **CA-10**: Actualizar estado en BD en tiempo real para que el Frontend lo consulte (crear endpoint `GET /api/v1/ocr/progress/{batch_id}`).
- **CA-11**: Identificar páginas en blanco (<50% confianza o 0 bloques).
- **CA-12**: Eliminar archivos temporales tras completar exitosamente, documentando en log.

## Especificaciones Técnicas — Backend

### Modelo de Datos (SQLAlchemy) a extender
```python
class OcrResultadosPaginas(Base):
    __tablename__ = "ocr_resultados_paginas"
    id = Column(Integer, primary_key=True, index=True)
    documento_id = Column(Integer, ForeignKey("documentos_lote.id"))
    numero_pagina = Column(Integer, nullable=False)
    bloques_raw_json = Column(String(None))
    campos_parseados = Column(String(None))
    confianza_promedio = Column(Numeric(5, 2))
    estado = Column(String(50))
    tiempo_proceso_ms = Column(Integer)
    processed_at = Column(DateTime, default=func.now())
```

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.**
3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
6. **Al terminar la ejecución:** Genera un `walkthrough.md` y avisa al Humano.
