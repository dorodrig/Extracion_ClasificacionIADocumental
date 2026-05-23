"""
Schemas Pydantic de entrada/salida para Reglas de Trabajo.

Gobernanza §2.2 — app/schemas/
Gobernanza §3.2 — Estructura de respuesta APIResponse obligatoria.

Schemas:
    - CampoExtraerSchema: Definición de un campo individual a extraer.
    - RuleCreate: Datos requeridos para crear una regla (POST).
    - RuleUpdate: Datos requeridos para actualizar una regla (PUT).
    - RuleResponse: Respuesta con todos los campos de la regla.
    - APIResponse[T]: Wrapper genérico de respuesta de la API.
"""
from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Wrapper de respuesta genérico — Gobernanza §3.2
# ---------------------------------------------------------------------------

class APIResponse(BaseModel, Generic[T]):
    """
    Wrapper genérico obligatorio para TODAS las respuestas de la API GRM.

    Gobernanza §3.2:
    - success: Indica si la operación fue exitosa.
    - data: Payload de la respuesta (genérico).
    - message: Mensaje descriptivo para el usuario.
    - error: Mensaje de error (solo en respuestas fallidas).
    """
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Schemas de CampoExtraer — CA-06
# ---------------------------------------------------------------------------

class CampoExtraerSchema(BaseModel):
    """
    Schema para un campo individual dentro de campos_extraer.

    CA-06: Cada campo tiene nombre, tipo de dato y flag de obligatoriedad.
    El tipo debe ser uno de: Texto, Número, Fecha, Identificación.
    """
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nombre del campo a extraer (ej: 'Número de Cédula')",
    )
    tipo: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Tipo de dato: Texto, Número, Fecha, Identificación",
    )
    obligatorio: bool = Field(
        default=False,
        description="Indica si el campo es obligatorio en la extracción",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Número de Cédula",
                "tipo": "Identificación",
                "obligatorio": True,
            }
        }
    )


# ---------------------------------------------------------------------------
# Schemas de Regla de Trabajo — CA-01 a CA-06
# ---------------------------------------------------------------------------

class RuleCreate(BaseModel):
    """
    Schema de entrada para crear una nueva regla de trabajo (POST).

    CA-05: Todos los campos listados son obligatorios.
    CA-06: campos_extraer debe tener al menos 1 elemento.
    """
    cliente_id: int = Field(
        ...,
        gt=0,
        description="ID del cliente propietario de la regla",
    )
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nombre descriptivo de la regla",
    )
    tipo_documento: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Tipo de documento que la regla procesa",
    )
    campos_extraer: list[CampoExtraerSchema] = Field(
        ...,
        min_length=1,
        description="Lista de campos a extraer (mínimo 1)",
    )
    patron_carpeta: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Patrón para organizar carpetas de salida",
    )
    modo_entrada: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Modo de ingesta: 'scanner' o 'carpeta'",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "cliente_id": 1,
                "nombre": "Regla Cédulas Colombianas",
                "tipo_documento": "Cédula de Ciudadanía",
                "campos_extraer": [
                    {
                        "nombre": "Número de Cédula",
                        "tipo": "Identificación",
                        "obligatorio": True,
                    },
                    {
                        "nombre": "Nombre Completo",
                        "tipo": "Texto",
                        "obligatorio": True,
                    },
                    {
                        "nombre": "Fecha de Expedición",
                        "tipo": "Fecha",
                        "obligatorio": False,
                    },
                ],
                "patron_carpeta": "{cliente}/{tipo_doc}/{año}/{mes}",
                "modo_entrada": "scanner",
            }
        }
    )


class RuleUpdate(BaseModel):
    """
    Schema de entrada para actualizar una regla existente (PUT).

    Misma estructura que RuleCreate. El ID y version se manejan
    internamente; el cliente_id se valida contra la regla existente.
    """
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nombre descriptivo de la regla",
    )
    tipo_documento: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Tipo de documento que la regla procesa",
    )
    campos_extraer: list[CampoExtraerSchema] = Field(
        ...,
        min_length=1,
        description="Lista de campos a extraer (mínimo 1)",
    )
    patron_carpeta: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Patrón para organizar carpetas de salida",
    )
    modo_entrada: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Modo de ingesta: 'scanner' o 'carpeta'",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Regla Cédulas Colombianas v2",
                "tipo_documento": "Cédula de Ciudadanía",
                "campos_extraer": [
                    {
                        "nombre": "Número de Cédula",
                        "tipo": "Identificación",
                        "obligatorio": True,
                    },
                ],
                "patron_carpeta": "{cliente}/{tipo_doc}/{año}/{mes}",
                "modo_entrada": "carpeta",
            }
        }
    )


class RuleResponse(BaseModel):
    """
    Schema de respuesta con todos los campos de una regla de trabajo.

    Incluye campos computados: id, version, activa, created_at, updated_at.
    CA-02: Los listados incluyen nombre, tipo_documento, created_at, updated_at, version.
    CA-03: El detalle incluye campos_extraer parseado como lista de objetos.
    """
    id: int
    cliente_id: int
    nombre: str
    tipo_documento: str
    campos_extraer: list[CampoExtraerSchema]
    patron_carpeta: str
    modo_entrada: str
    umbral_ocr: float
    version: int
    activa: bool
    created_by: Optional[int] = None  # TODO(HU-08): Make created_by mandatory once Auth is integrated.
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
