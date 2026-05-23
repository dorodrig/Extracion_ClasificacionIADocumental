"""
Entidades de dominio puras para Reglas de Trabajo.

Gobernanza §2.2 — app/domain/models/
Estas clases representan el concepto de negocio sin dependencia de ORM,
frameworks o infraestructura.
"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CampoExtraer:
    """
    Representa un campo individual a extraer de un documento.

    Atributos:
        nombre: Nombre del campo (ej: "Número de Cédula").
        tipo: Tipo de dato esperado — Texto, Número, Fecha, Identificación.
        obligatorio: Indica si el campo es requerido en la extracción.
    """
    nombre: str
    tipo: str
    obligatorio: bool = False


@dataclass
class Rule:
    """
    Entidad de dominio: Regla de Trabajo.

    Define la configuración que el sistema GRM usa para saber qué campos
    extraer de un tipo de documento, cómo organizar las carpetas de salida
    y bajo qué modo de entrada operar.

    Atributos:
        id: Identificador único (generado por BD).
        cliente_id: FK al cliente propietario de la regla.
        nombre: Nombre descriptivo de la regla.
        tipo_documento: Tipo de documento que la regla procesa.
        campos_extraer: Lista de campos a extraer del documento.
        patron_carpeta: Patrón para organizar carpetas de salida.
        modo_entrada: Modo de ingesta — 'scanner' o 'carpeta'.
        umbral_ocr: Umbral mínimo de confianza OCR (default 95.00).
        version: Versión de la regla (auto-incremento en cada actualización).
        activa: Indica si la regla está activa (soft-delete).
        created_by: ID del usuario que creó la regla (nullable hasta HU-08).
        created_at: Fecha de creación.
        updated_at: Fecha de última modificación.
    """
    cliente_id: int
    nombre: str
    tipo_documento: str
    campos_extraer: list[CampoExtraer]
    patron_carpeta: str
    modo_entrada: str
    id: int | None = None
    umbral_ocr: float = 95.00
    version: int = 1
    activa: bool = True
    created_by: int | None = None  # TODO(HU-08): Make created_by mandatory once Auth is integrated.
    created_at: datetime | None = None
    updated_at: datetime | None = None
