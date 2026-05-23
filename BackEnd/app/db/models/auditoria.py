from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.database import Base

class LogProceso(Base):
    __tablename__ = "log_proceso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, ForeignKey("documentos_lote.id", ondelete="SET NULL"), nullable=True, index=True)
    estado_anterior = Column(String(50), nullable=True)
    estado_nuevo = Column(String(50), nullable=False)
    mensaje = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=func.now(), nullable=False)

class LogAuditoriaUsuario(Base):
    __tablename__ = "log_auditoria_usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, ForeignKey("documentos_lote.id", ondelete="SET NULL"), nullable=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True, index=True)
    accion = Column(String(100), nullable=False) # e.g. correccion_directa, instruccion_ia, descarte
    detalles = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=func.now(), nullable=False)


