from sqlalchemy.orm import Session
from app.db.models.documentos_clasificados import DocumentoClasificado
from typing import Dict, Any, Optional

class ClasificacionRepo:
    def __init__(self, db: Session):
        self.db = db

    def upsert_clasificacion(
        self,
        documento_id: int,
        cliente_id: int,
        batch_id: str,
        regla_id: int,
        campos_extraidos: Dict[str, Any],
        ruta_destino: str,
        tipo_documento: str
    ) -> DocumentoClasificado:
        
        doc = self.db.query(DocumentoClasificado).filter_by(documento_id=documento_id).first()
        if not doc:
            doc = DocumentoClasificado(
                documento_id=documento_id,
                cliente_id=cliente_id,
                batch_id=batch_id,
                regla_id=regla_id,
                campos_extraidos_json=campos_extraidos,
                ruta_destino_final=ruta_destino,
                tipo_documento=tipo_documento
            )
            self.db.add(doc)
        else:
            doc.cliente_id = cliente_id
            doc.batch_id = batch_id
            doc.regla_id = regla_id
            doc.campos_extraidos_json = campos_extraidos
            doc.ruta_destino_final = ruta_destino
            doc.tipo_documento = tipo_documento
            
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def get_by_documento_id(self, documento_id: int) -> Optional[DocumentoClasificado]:
        return self.db.query(DocumentoClasificado).filter_by(documento_id=documento_id).first()
