from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class OcrResultadosPaginas(Base):
    __tablename__ = "ocr_resultados_paginas"
    id = Column(Integer, primary_key=True, index=True)
    documento_id = Column(Integer, ForeignKey("documentos_lote.id"), nullable=False)
    numero_pagina = Column(Integer, nullable=False)
    bloques_raw_json = Column(String(None))  # NVARCHAR(MAX) equivalent in standard SQL
    campos_parseados = Column(String(None))
    confianza_promedio = Column(Numeric(5, 2))
    estado = Column(String(50))
    tiempo_proceso_ms = Column(Integer)
    processed_at = Column(DateTime, default=func.now())

    documento = relationship("DocumentosLote", back_populates="paginas")
