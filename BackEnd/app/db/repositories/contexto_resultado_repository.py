"""
Repository para la tabla agente_contexto_resultados.

HU-04, CA-12 — Acceso a datos de resultados del Agente de Contexto IA.
Gobernanza §3.4 — Capa de infraestructura (Repository Pattern).
"""
import logging
from sqlalchemy.orm import Session

from app.db.models.contexto_resultado_db import AgenteContextoResultados

logger = logging.getLogger("grm.contexto_resultado_repository")


class ContextoResultadoRepository:
    """Repository para operaciones CRUD sobre agente_contexto_resultados."""

    def __init__(self, db: Session):
        self.db = db

    def crear(self, resultado: AgenteContextoResultados) -> AgenteContextoResultados:
        """
        Persiste un nuevo resultado del agente de contexto.

        Args:
            resultado: Instancia del modelo con los datos a persistir.

        Returns:
            La instancia persistida con id asignado.
        """
        self.db.add(resultado)
        self.db.commit()
        self.db.refresh(resultado)
        logger.info(
            "Resultado de contexto IA creado: id=%d, documento_id=%d, estado=%s",
            resultado.id,
            resultado.documento_id,
            resultado.estado,
        )
        return resultado

    def obtener_por_documento(
        self, documento_id: int
    ) -> AgenteContextoResultados | None:
        """
        Obtiene el resultado del agente de contexto para un documento.

        Args:
            documento_id: ID del documento a consultar.

        Returns:
            El resultado o None si no existe.
        """
        return (
            self.db.query(AgenteContextoResultados)
            .filter(AgenteContextoResultados.documento_id == documento_id)
            .first()
        )

    def listar_por_estado(
        self, estado: str, limit: int = 50
    ) -> list[AgenteContextoResultados]:
        """
        Lista resultados filtrados por estado.

        Args:
            estado: Estado a filtrar (listo_clasificacion, pendiente_humano, error_ia).
            limit: Máximo de resultados a retornar.

        Returns:
            Lista de resultados con el estado indicado.
        """
        return (
            self.db.query(AgenteContextoResultados)
            .filter(AgenteContextoResultados.estado == estado)
            .order_by(AgenteContextoResultados.processed_at.desc())
            .limit(limit)
            .all()
        )
