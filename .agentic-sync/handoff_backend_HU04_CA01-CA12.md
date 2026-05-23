# Handoff — Backend — HU-04
## Iteración: 1-DEV-HU-4

| Campo                    | Valor                                             |
|--------------------------|---------------------------------------------------|
| **Archivo**              | `handoff_backend_HU04_CA01-CA12.md`               |
| **Rol Destino**          | Agente Backend                                    |
| **HU de Origen**         | HU-04 — Agente de Contexto IA (Google Gemini)     |
| **CAs Asignados**        | CA-01 al CA-12                                    |
| **CAs Excluidos**        | Ninguno                                           |
| **Rama Git**             | `HU1_CA1-CA6_DEVDAVID_ITEREACION1`                |
| **Iteración**            | 1-DEV-HU-4                                        |
| **Fecha de Generación**  | 2026-05-23                                        |
| **Generado Por**         | Agente Arquitecto Líder (Orquestador)             |
| **Gobernanza**           | v1.0.0 — Gobernanza_Arquitectura.md               |

## Alineación Arquitectónica

### Stack Tecnológico Validado
- [x] Backend: Python 3.12 + FastAPI + Celery + SQLAlchemy + `google-generativeai`
- [x] Modelo IA: Google Gemini 1.5 Pro
- [x] Estructura: Clean Architecture (Servicios de Dominio, Adapters para IA)

### Riesgos Identificados
> R-IA-1: Respuestas no deterministas. Mitigación: Forzar retorno en JSON estructurado y validar schema (Pydantic) estrictamente (CA-03).
> R-IA-2: Contaminación de contexto. Mitigación: Sesión fresca por cada documento procesado (CA-10).

## Criterios de Aceptación Asignados al Backend

- **CA-01**: Construir prompt dinámico mezclando reglas de HU-01 con texto OCR de HU-03. Sin mezclar clientes.
- **CA-02**: Invocar SDK de Gemini usando `GEMINI_API_KEY`. NUNCA hardcodear.
- **CA-03**: Parsear JSON. Si es inválido, reintentar hasta 2 veces. Si falla, estado "Error de IA - Respuesta inválida".
- **CA-04**: Validar campos obligatorios y tipos. Si todo es correcto `datos_completos = true`, si no `false`.
- **CA-05**: Si `datos_completos = false`, estado "Pendiente Revisión Humana" con `motivo_rechazo`.
- **CA-06**: Si `datos_completos = true`, estado "Datos Limpios - Listo para Clasificación".
- **CA-07**: Comparar tipo detectado vs regla. Si confianza es alta pero difiere, alertar. Si es totalmente distinto, marcar `datos_completos = false`.
- **CA-08**: Timeout (30s) y reintentos (x3) para la API de Gemini (Backoff exponencial).
- **CA-09**: Log de tokens y duraciones en `log_ia_invocaciones` para control de costos.
- **CA-10**: Aislar invocaciones. NUNCA enviar historial previo a la API.
- **CA-11**: Normalizar números de identificación (ej. borrar puntos) y fechas (ISO 8601).
- **CA-12**: Consolidar en `agente_contexto_resultados`. Crear la migración respectiva en Alembic.

## Especificaciones Técnicas — Backend

### Modelo de Datos (SQLAlchemy) a extender
```python
class AgenteContextoResultados(Base):
    __tablename__ = "agente_contexto_resultados"
    id = Column(Integer, primary_key=True, index=True)
    documento_id = Column(Integer, ForeignKey("documentos_lote.id"))
    regla_id = Column(Integer, ForeignKey("reglas_trabajo.id"))
    tipo_doc_detectado = Column(String(100))
    campos_extraidos_json = Column(String(None))
    datos_completos = Column(Boolean)
    motivo_rechazo = Column(String(500))
    modelo_ia = Column(String(100))
    tokens_entrada = Column(Integer)
    tokens_salida = Column(Integer)
    duracion_ms = Column(Integer)
    estado = Column(String(50))
    processed_at = Column(DateTime, default=func.now())
```

## INSTRUCCIONES OPERATIVAS PARA EL AGENTE

> **PROTOCOLO DE EJECUCIÓN — LEE ESTO COMPLETO ANTES DE ACTUAR**

1. **Inicia en modo `PLANNING`**: Elabora un plan de implementación en `implementation_plan.md`.
2. **PROHIBIDO pedirle al Humano que apruebe tu plan.** El humano es solo un cartero.
3. **Guarda tu solicitud de revisión** en:
   `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
4. **Dile al Humano exactamente este mensaje:**
   > "He dejado mi solicitud de revisión en la ruta acordada:
   > `C:\zData\ExtracionDatosIA\.agentic-sync\approval_request_Backend.md`
   > Llévasela al Arquitecto Líder y regrésame su respuesta."
5. **Espera la respuesta del Arquitecto.** Solo tras recibir aprobación, pasa a modo `EXECUTION`.
6. **Al terminar la ejecución:** Genera un `walkthrough.md` y avisa al Humano.
