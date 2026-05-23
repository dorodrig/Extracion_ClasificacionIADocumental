"""
Modelo SQLAlchemy ORM para la tabla reglas_trabajo.

Gobernanza §2.2 — app/db/models/
Gobernanza §5.1 — Nombrado SQL Server (snake_case, plural, español del dominio).
Gobernanza §5.2 — Columnas de auditoría obligatorias + JSON en NVARCHAR(MAX).
"""
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    func,
)

from app.db.database import Base


class ReglasTrabajo(Base):
    """
    ORM Model para la tabla reglas_trabajo en SQL Server.

    Almacena la configuración de reglas de trabajo por cliente,
    incluyendo los campos a extraer como JSON en NVARCHAR(MAX).

    Columnas de auditoría: created_at, updated_at, created_by (§5.2).
    Soft-delete: campo activa (BIT DEFAULT 1) — no se implementa endpoint
    DELETE en HU-01.
    """

    __tablename__ = "reglas_trabajo"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="PK auto-incremental (IDENTITY)",
    )
    cliente_id = Column(
        Integer,
        nullable=False,
        index=True,
        comment="FK al cliente propietario de la regla",
    )
    nombre = Column(
        String(255),
        nullable=False,
        comment="Nombre descriptivo de la regla de trabajo",
    )
    tipo_documento = Column(
        String(255),
        nullable=False,
        comment="Tipo de documento que la regla procesa",
    )
    campos_extraer = Column(
        Text,  # NVARCHAR(MAX) en SQL Server — almacena JSON
        nullable=False,
        comment=(
            "JSON array de campos a extraer. "
            'Estructura: [{"nombre": "...", "tipo": "...", "obligatorio": true}]'
        ),
    )
    patron_carpeta = Column(
        String(500),
        nullable=False,
        comment="Patrón para organizar carpetas de salida",
    )
    modo_entrada = Column(
        String(50),
        nullable=False,
        comment="Modo de ingesta: 'scanner' o 'carpeta'",
    )
    umbral_ocr = Column(
        Float,
        nullable=False,
        default=95.00,
        comment="Umbral mínimo de confianza OCR (default 95.00%)",
    )
    version = Column(
        Integer,
        nullable=False,
        default=1,
        comment="Versión de la regla (auto-incremento en cada PUT)",
    )
    activa = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Soft-delete flag — True = activa, False = eliminada",
    )
    created_by = Column(
        Integer,
        nullable=True,  # TODO(HU-08): Make created_by mandatory once Auth is integrated.
        comment="FK al usuario creador (nullable hasta integrar HU-08)",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="Fecha y hora de creación del registro",
    )
    updated_at = Column(
        DateTime,
        nullable=True,
        onupdate=func.now(),
        comment="Fecha y hora de última modificación",
    )

    def __repr__(self) -> str:
        return (
            f"<ReglasTrabajo(id={self.id}, cliente_id={self.cliente_id}, "
            f"nombre='{self.nombre}', version={self.version})>"
        )
