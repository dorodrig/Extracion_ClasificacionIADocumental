from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class DocumentosLote(Base):
    __tablename__ = "documentos_lote"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String(255), nullable=False)
    estado = Column(String(50), default="PENDIENTE")
    
    # Relación con OcrResultadosPaginas
    paginas = relationship("OcrResultadosPaginas", back_populates="documento", cascade="all, delete-orphan")
