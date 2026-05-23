"""
Stub models para tablas referenciadas por ForeignKeys.

Estas tablas (clientes, usuarios) serán implementadas formalmente
en HU-08 (Auth & RBAC). Estos stubs permiten que SQLAlchemy
pueda crear las tablas en tests y en migraciones.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Cliente(Base):
    """Stub: tabla clientes — TODO(HU-08): Implementación real."""
    __tablename__ = "clientes"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    nit = Column(String(50), nullable=True, unique=True)
    created_at = Column(DateTime, default=func.now())


class Usuario(Base):
    """Stub: tabla usuarios — TODO(HU-08): Implementación real."""
    __tablename__ = "usuarios"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    cedula = Column(String(50), nullable=True, unique=True)
    rol = Column(String(50), nullable=False, default="operario")
    cliente_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
