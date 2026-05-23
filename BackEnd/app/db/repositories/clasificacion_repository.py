from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.dialects.mssql import insert
from datetime import datetime

from app.db.models.documentos_clasificados import DocumentoClasificado
from app.db.models.batches import DocumentoLote, LoteProcesamiento
from app.core.exceptions import GRMException
import logging

logger = logging.getLogger("grm.db.repositories.clasificacion")

class ClasificacionRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def upsert_documento_clasificado(self, doc_clasificado: DocumentoClasificado) -> DocumentoClasificado:
        """Realiza un UPSERT en la tabla documentos_clasificados."""
        try:
            # En SQLAlchemy con mssql o dialectos genéricos, upsert puede ser manual o con on_conflict_do_update.
            # Como SQL Server no soporta on_conflict genérico de forma nativa en SQLAlchemy viejo, usaremos un select + update/insert manual
            # o merge de SQLAlchemy. `merge` es ideal para UPSERT si la primary key o unique key está seteada en el objeto.
            # Aquí documento_id es Unique.
            
            existing = self.db.query(DocumentoClasificado).filter_by(documento_id=doc_clasificado.documento_id).first()
            if existing:
                existing.campos_extraidos_json = doc_clasificado.campos_extraidos_json
                existing.ruta_destino_final = doc_clasificado.ruta_destino_final
                existing.tipo_documento = doc_clasificado.tipo_documento
                existing.timestamp_clasificacion = datetime.now()
                self.db.commit()
                self.db.refresh(existing)
                return existing
            else:
                self.db.add(doc_clasificado)
                self.db.commit()
                self.db.refresh(doc_clasificado)
                return doc_clasificado
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error en UPSERT de DocumentoClasificado: {str(e)}")
            raise GRMException(f"Fallo al guardar clasificación: {str(e)}")

    def update_documento_estado(self, documento_id: int, estado: str, error_detalle: str = None):
        """Actualiza el estado en documentos_lote."""
        try:
            doc = self.db.query(DocumentoLote).filter(DocumentoLote.id == documento_id).first()
            if doc:
                doc.estado = estado
                if error_detalle:
                    doc.error_detalle = error_detalle
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error al actualizar estado del documento {documento_id}: {str(e)}")
            raise GRMException(f"Fallo al actualizar estado: {str(e)}")

    def check_lote_completado(self, lote_id: int):
        """Verifica si todos los documentos del lote están procesados y genera un resumen."""
        try:
            total = self.db.query(DocumentoLote).filter(DocumentoLote.lote_id == lote_id).count()
            pendientes = self.db.query(DocumentoLote).filter(
                DocumentoLote.lote_id == lote_id,
                DocumentoLote.estado.in_(["pendiente", "preparando", "procesando"])
            ).count()
            
            if pendientes == 0 and total > 0:
                lote = self.db.query(LoteProcesamiento).filter(LoteProcesamiento.id == lote_id).first()
                if lote:
                    lote.estado = "completado"
                    lote.completed_at = datetime.now()
                    self.db.commit()
                    logger.info(f"Lote {lote_id} completado.")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error al verificar lote completado {lote_id}: {str(e)}")
