from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.database import Base

class DocumentoClasificado(Base):
    __tablename__ = "documentos_clasificados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, nullable=False, index=True)
    batch_id = Column(String(50), nullable=False, index=True)
    regla_id = Column(Integer, nullable=False)
    documento_id = Column(Integer, ForeignKey("documentos_lote.id"), nullable=False, unique=True)
    
    campos_extraidos_json = Column(JSON, nullable=False)
    ruta_destino_final = Column(String(500), nullable=False)
    tipo_documento = Column(String(100), nullable=False)
    
    # Preparado para futuro CA-05
    # contenido_b64 = Column(String, doc="Contenido en base64 del documento clasificado", nullable=True)
    
    timestamp_clasificacion = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
