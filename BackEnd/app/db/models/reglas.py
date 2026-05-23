from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.db.database import Base

class ReglaTrabajo(Base):
    __tablename__ = "reglas_trabajo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=True)
    
    # Cliente al que pertenece la regla (opcional, o puede aplicar a todos)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    
    configuracion_json = Column(JSON, nullable=False)
    activa = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
