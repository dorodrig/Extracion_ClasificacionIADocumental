import logging
from sqlalchemy.orm import Session
from app.db.repositories.auditoria_repository import AuditoriaRepository
from app.schemas.auditoria import LogProcesoCreate, LogAuditoriaUsuarioCreate, LogIAInvocacionesCreate, DocumentoHistorialResponse

logger = logging.getLogger(__name__)

class AuditoriaService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AuditoriaRepository(db)

    def registrar_log_proceso(self, data: LogProcesoCreate) -> bool:
        try:
            self.repository.create_log_proceso(data)
            return True
        except Exception as e:
            logger.error(f"Error al registrar log de proceso: {e}")
            self.db.rollback()
            return False

    def registrar_auditoria_usuario(self, data: LogAuditoriaUsuarioCreate) -> bool:
        try:
            self.repository.create_log_auditoria_usuario(data)
            return True
        except Exception as e:
            logger.error(f"Error al registrar auditoria de usuario: {e}")
            self.db.rollback()
            return False

    def registrar_llamada_ia(self, data: LogIAInvocacionesCreate) -> bool:
        try:
            self.repository.create_log_ia_invocacion(data)
            return True
        except Exception as e:
            logger.error(f"Error al registrar invocacion IA: {e}")
            self.db.rollback()
            return False

    def obtener_historial_documento(self, documento_id: int) -> DocumentoHistorialResponse:
        historial_dicts = self.repository.get_historial_documento(documento_id)
        return DocumentoHistorialResponse(
            documento_id=documento_id,
            historial=historial_dicts
        )
