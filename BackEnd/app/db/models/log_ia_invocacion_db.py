"""
Modelo SQLAlchemy ORM para la tabla log_ia_invocaciones.

HU-04, CA-09 — Registra cada invocación a la API de Gemini
con tokens consumidos, duración y resultado para control de costos.

Gobernanza §5.1 — Nombrado SQL (snake_case, plural, español).
"""
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)

from app.db.database import Base


class LogIAInvocacion(Base):
    """
    ORM Model para la tabla log_ia_invocaciones.

    Cada fila representa una invocación individual a la API de Gemini,
    exitosa o fallida. Permite análisis de costos y optimización.
    """

    __tablename__ = "log_ia_invocaciones"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="PK auto-incremental (IDENTITY)",
    )
    documento_id = Column(
        Integer,
        ForeignKey("documentos_lote.id"),
        nullable=False,
        index=True,
        comment="FK al documento que originó la invocación",
    )
    modelo = Column(
        String(100),
        nullable=False,
        comment="Nombre del modelo IA invocado (ej: gemini-1.5-pro)",
    )
    tokens_entrada = Column(
        Integer,
        nullable=True,
        comment="Tokens de entrada (prompt) consumidos",
    )
    tokens_salida = Column(
        Integer,
        nullable=True,
        comment="Tokens de salida (respuesta) generados",
    )
    duracion_ms = Column(
        Integer,
        nullable=True,
        comment="Duración de la invocación en milisegundos",
    )
    exitoso = Column(
        Boolean,
        nullable=False,
        comment="True si la invocación fue exitosa",
    )
    error_mensaje = Column(
        String(500),
        nullable=True,
        comment="Mensaje de error si la invocación falló",
    )
    invocado_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="Timestamp de la invocación",
    )

    def __repr__(self) -> str:
        return (
            f"<LogIAInvocacion(id={self.id}, "
            f"documento_id={self.documento_id}, "
            f"modelo='{self.modelo}', "
            f"exitoso={self.exitoso})>"
        )
