from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.database import Base

class DocumentoPendiente(Base):
    __tablename__ = "documentos_pendientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False, index=True)
    batch_id = Column(String(50), nullable=False, index=True)
    documento_id = Column(Integer, ForeignKey("documentos_lote.id"), nullable=False, unique=True)
    
    motivo_rechazo = Column(String(500), nullable=True)
    campos_extraidos_json = Column(JSON, nullable=True)
    estado = Column(String(50), nullable=False, default="pendiente") # pendiente, corregido, descartado
    
    # Preparado para futuro CA-05
    # contenido_b64 = Column(String, doc="Contenido en base64 del documento", nullable=True)
    
    operario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
