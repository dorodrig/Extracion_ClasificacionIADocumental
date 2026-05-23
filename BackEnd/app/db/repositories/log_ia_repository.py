"""
Repository para la tabla log_ia_invocaciones.

HU-04, CA-09 — Registro de invocaciones a la API de Gemini
para control de costos y análisis de rendimiento.

Gobernanza §3.4 — Capa de infraestructura (Repository Pattern).
"""
import logging
from sqlalchemy.orm import Session

from app.db.models.log_ia_invocacion_db import LogIAInvocacion

logger = logging.getLogger("grm.log_ia_repository")


class LogIARepository:
    """Repository para operaciones sobre log_ia_invocaciones."""

    def __init__(self, db: Session):
        self.db = db

    def registrar(self, log: LogIAInvocacion) -> LogIAInvocacion:
        """
        Registra una invocación a la API de IA.

        Args:
            log: Instancia del modelo con los datos de la invocación.

        Returns:
            La instancia persistida con id asignado.
        """
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        logger.info(
            "Invocación IA registrada: id=%d, documento_id=%d, "
            "modelo=%s, exitoso=%s, tokens_in=%s, tokens_out=%s",
            log.id,
            log.documento_id,
            log.modelo,
            log.exitoso,
            log.tokens_entrada,
            log.tokens_salida,
        )
        return log

    def listar_por_documento(
        self, documento_id: int
    ) -> list[LogIAInvocacion]:
        """
        Lista todas las invocaciones IA para un documento.

        Args:
            documento_id: ID del documento a consultar.

        Returns:
            Lista de registros de invocación ordenados por fecha.
        """
        return (
            self.db.query(LogIAInvocacion)
            .filter(LogIAInvocacion.documento_id == documento_id)
            .order_by(LogIAInvocacion.invocado_at.desc())
            .all()
        )
