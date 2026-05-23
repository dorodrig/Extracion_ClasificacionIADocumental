from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.models.documentos_pendientes import DocumentoPendiente
from typing import Optional, Dict, Any, List

class PendientesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_pendientes(self, skip: int = 0, limit: int = 100, query: Optional[str] = None, cliente_id: Optional[int] = None):
        db_query = self.db.query(DocumentoPendiente).filter(DocumentoPendiente.estado == "pendiente")
        
        if cliente_id:
            db_query = db_query.filter(DocumentoPendiente.cliente_id == cliente_id)
            
        if query:
            db_query = db_query.filter(
                or_(
                    DocumentoPendiente.batch_id.ilike(f"%{query}%"),
                    DocumentoPendiente.motivo_rechazo.ilike(f"%{query}%")
                )
            )
            
        total = db_query.count()
        items = db_query.offset(skip).limit(limit).all()
        return items, total

    def get_pendiente_by_id(self, pendiente_id: int) -> Optional[DocumentoPendiente]:
        return self.db.query(DocumentoPendiente).filter(DocumentoPendiente.id == pendiente_id).first()

    def update_pendiente_status(self, pendiente_id: int, estado: str, campos_corregidos: Optional[Dict[str, Any]] = None) -> Optional[DocumentoPendiente]:
        db_pendiente = self.get_pendiente_by_id(pendiente_id)
        if db_pendiente:
            db_pendiente.estado = estado
            if campos_corregidos is not None:
                db_pendiente.campos_extraidos_json = campos_corregidos
            self.db.commit()
            self.db.refresh(db_pendiente)
        return db_pendiente

    def update_pendiente_rechazo(self, pendiente_id: int, motivo: str) -> Optional[DocumentoPendiente]:
        db_pendiente = self.get_pendiente_by_id(pendiente_id)
        if db_pendiente:
            db_pendiente.estado = "descartado"
            db_pendiente.motivo_rechazo = motivo
            self.db.commit()
            self.db.refresh(db_pendiente)
        return db_pendiente
