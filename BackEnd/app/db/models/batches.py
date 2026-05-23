from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class LoteProcesamiento(Base):
    __tablename__ = "lotes_procesamiento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(UNIQUEIDENTIFIER, default=uuid.uuid4, unique=True, index=True)
    regla_id = Column(Integer, ForeignKey("reglas_trabajo.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    operario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    modo_ingesta = Column(String(50), nullable=False)
    ruta_temporal = Column(String(500), nullable=True)
    total_docs = Column(Integer, nullable=True)
    total_paginas = Column(Integer, nullable=True)
    estado = Column(String(50), default="preparando")
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)


class DocumentoLote(Base):
    __tablename__ = "documentos_lote"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lote_id = Column(Integer, ForeignKey("lotes_procesamiento.id"), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    ruta_original = Column(String(500), nullable=True)
    ruta_temporal = Column(String(500), nullable=True)
    total_paginas = Column(Integer, nullable=True)
    estado = Column(String(50), default="pendiente")
    error_detalle = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
