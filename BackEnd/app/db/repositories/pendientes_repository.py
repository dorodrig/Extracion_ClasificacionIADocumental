from sqlalchemy.orm import Session
from sqlalchemy import or_, String
from app.db.models.documentos_pendientes import DocumentoPendiente
from app.db.models.contexto_resultado_db import AgenteContextoResultados
from app.db.models.documentos_lote import DocumentoLote, LoteProcesamiento
import json
from typing import Optional, Dict, Any, List

class PendientesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_pendientes(self, skip: int = 0, limit: int = 100, query: Optional[str] = None, cliente_id: Optional[int] = None):
        db_query = self.db.query(AgenteContextoResultados, DocumentoLote, LoteProcesamiento).join(
            DocumentoLote, AgenteContextoResultados.documento_id == DocumentoLote.id
        ).join(
            LoteProcesamiento, DocumentoLote.lote_id == LoteProcesamiento.id
        ).filter(AgenteContextoResultados.estado == "pendiente_humano")
        
        if cliente_id:
            db_query = db_query.filter(LoteProcesamiento.cliente_id == cliente_id)
            
        if query:
            db_query = db_query.filter(
                or_(
                    LoteProcesamiento.batch_id.cast(String).ilike(f"%{query}%"),
                    AgenteContextoResultados.motivo_rechazo.ilike(f"%{query}%")
                )
            )
            
        total = db_query.count()
        db_query = db_query.order_by(AgenteContextoResultados.id.desc())
        results = db_query.offset(skip).limit(limit).all()
        
        items = []
        for res, doc, lote in results:
            res.cliente_id = lote.cliente_id
            res.batch_id = str(lote.batch_id)
            res.created_at = res.processed_at
            res.updated_at = res.processed_at
            if isinstance(res.campos_extraidos_json, str):
                try:
                    res.campos_extraidos_json = json.loads(res.campos_extraidos_json)
                except:
                    pass
            items.append(res)
            
        return items, total

    def get_pendiente_by_id(self, pendiente_id: int):
        result = self.db.query(AgenteContextoResultados, DocumentoLote, LoteProcesamiento).join(
            DocumentoLote, AgenteContextoResultados.documento_id == DocumentoLote.id
        ).join(
            LoteProcesamiento, DocumentoLote.lote_id == LoteProcesamiento.id
        ).filter(AgenteContextoResultados.id == pendiente_id).first()
        
        if result:
            res, doc, lote = result
            res.cliente_id = lote.cliente_id
            res.batch_id = str(lote.batch_id)
            res.created_at = res.processed_at
            res.updated_at = res.processed_at
            if isinstance(res.campos_extraidos_json, str):
                try:
                    res.campos_extraidos_json = json.loads(res.campos_extraidos_json)
                except:
                    pass
            return res
        return None

    def update_pendiente_status(self, pendiente_id: int, estado: str, campos_corregidos: Optional[Dict[str, Any]] = None):
        result = self.db.query(AgenteContextoResultados, DocumentoLote, LoteProcesamiento).join(
            DocumentoLote, AgenteContextoResultados.documento_id == DocumentoLote.id
        ).join(
            LoteProcesamiento, DocumentoLote.lote_id == LoteProcesamiento.id
        ).filter(AgenteContextoResultados.id == pendiente_id).first()
        
        if result:
            res, doc, lote = result
            res.estado = estado
            if campos_corregidos is not None:
                res.campos_extraidos_json = json.dumps(campos_corregidos, ensure_ascii=False)
            self.db.commit()
            self.db.refresh(res)
            
            res.cliente_id = lote.cliente_id
            res.batch_id = str(lote.batch_id)
            res.created_at = res.processed_at
            res.updated_at = res.processed_at
            if isinstance(res.campos_extraidos_json, str):
                try:
                    res.campos_extraidos_json = json.loads(res.campos_extraidos_json)
                except:
                    pass
            return res
        return None

    def update_pendiente_rechazo(self, pendiente_id: int, motivo: str):
        result = self.db.query(AgenteContextoResultados, DocumentoLote, LoteProcesamiento).join(
            DocumentoLote, AgenteContextoResultados.documento_id == DocumentoLote.id
        ).join(
            LoteProcesamiento, DocumentoLote.lote_id == LoteProcesamiento.id
        ).filter(AgenteContextoResultados.id == pendiente_id).first()
        
        if result:
            res, doc, lote = result
            res.estado = "descartado"
            res.motivo_rechazo = motivo
            self.db.commit()
            self.db.refresh(res)
            
            res.cliente_id = lote.cliente_id
            res.batch_id = str(lote.batch_id)
            res.created_at = res.processed_at
            res.updated_at = res.processed_at
            if isinstance(res.campos_extraidos_json, str):
                try:
                    res.campos_extraidos_json = json.loads(res.campos_extraidos_json)
                except:
                    pass
            return res
        return None
