"""
Schemas Pydantic de entrada/salida para el Agente de Contexto IA.

HU-04 — Schemas para procesar documentos con Gemini y retornar
paquetes de datos limpios.

Gobernanza §2.2 — app/schemas/
Gobernanza §3.2 — Estructura de respuesta APIResponse obligatoria.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Schemas de campos extraídos — CA-11, CA-12
# ---------------------------------------------------------------------------

class CampoExtraidoSchema(BaseModel):
    """
    Schema para un campo individual extraído por el Agente de Contexto IA.

    CA-11: Incluye valor_original para trazabilidad.
    CA-12: Parte del paquete de datos limpios.
    """
    nombre: str = Field(
        ...,
        description="Nombre del campo extraído (ej: 'Número de Cédula')",
    )
    valor: Optional[str] = Field(
        None,
        description="Valor normalizado del campo extraído",
    )
    valor_original: Optional[str] = Field(
        None,
        description="Valor original sin normalizar (trazabilidad CA-11)",
    )
    confianza_ocr: float = Field(
        default=0.0,
        description="Score de confianza OCR del valor",
    )
    validado_ia: bool = Field(
        default=False,
        description="True si la IA validó el valor como correcto",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Número de Cédula",
                "valor": "1234567",
                "valor_original": "1.234.567",
                "confianza_ocr": 98.5,
                "validado_ia": True,
            }
        }
    )


# ---------------------------------------------------------------------------
# Schemas de request/response — CA-01 a CA-12
# ---------------------------------------------------------------------------

class ContextoProcessRequest(BaseModel):
    """
    Schema de entrada para procesar un documento con el Agente de Contexto IA.

    El endpoint recibe documento_id y regla_id, y el servicio obtiene
    los datos OCR y la regla de la BD.
    """
    documento_id: int = Field(
        ...,
        gt=0,
        description="ID del documento a procesar (debe tener OCR completado)",
    )
    regla_id: int = Field(
        ...,
        gt=0,
        description="ID de la regla de trabajo a aplicar",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "documento_id": 1,
                "regla_id": 1,
            }
        }
    )


class ContextoResultadoResponse(BaseModel):
    """
    Schema de respuesta con el paquete de datos limpios del Agente de Contexto IA.

    CA-12: Incluye todos los campos del paquete de datos limpios.
    """
    id: int
    documento_id: int
    regla_id: int
    tipo_doc_detectado: Optional[str] = None
    campos_extraidos: list[CampoExtraidoSchema]
    datos_completos: bool
    motivo_rechazo: Optional[str] = None
    modelo_ia: str
    tokens_entrada: Optional[int] = None
    tokens_salida: Optional[int] = None
    duracion_ms: Optional[int] = None
    estado: str
    processed_at: datetime

    model_config = ConfigDict(from_attributes=True)
