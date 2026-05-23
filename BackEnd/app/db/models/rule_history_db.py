"""
Modelo SQLAlchemy ORM para la tabla reglas_trabajo_historial.

Gobernanza §2.2 — app/db/models/
Gobernanza §5.1 — Nombrado SQL Server (snake_case, plural, español del dominio).
"""
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    func,
)

from app.db.database import Base


class ReglasTrabajoHistorial(Base):
    """
    ORM Model para la tabla reglas_trabajo_historial.

    Almacena el historial de versiones de las reglas de trabajo.
    """

    __tablename__ = "reglas_trabajo_historial"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="PK auto-incremental",
    )
    regla_id = Column(
        Integer,
        nullable=False,
        index=True,
        comment="FK a la regla original (reglas_trabajo.id)",
    )
    version = Column(
        Integer,
        nullable=False,
        comment="Versión de la regla que se está guardando",
    )
    snapshot_json = Column(
        Text,  # NVARCHAR(MAX) en SQL Server
        nullable=False,
        comment="Estado completo de la regla al momento de modificarla (JSON)",
    )
    modificado_por = Column(
        Integer,
        nullable=True,
        comment="FK al usuario que realizó la modificación (nullable hasta HU-08)",
    )
    modificado_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="Fecha y hora en que se guardó este snapshot",
    )

    def __repr__(self) -> str:
        return (
            f"<ReglasTrabajoHistorial(id={self.id}, regla_id={self.regla_id}, "
            f"version={self.version})>"
        )
