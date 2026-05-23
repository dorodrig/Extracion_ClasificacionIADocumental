from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base

usuario_cliente = Table(
    'usuarios_clientes', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id', ondelete="CASCADE"), primary_key=True),
    Column('cliente_id', Integer, ForeignKey('clientes.id', ondelete="CASCADE"), primary_key=True)
)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False) # admin, operario, cliente
    intentos_fallidos = Column(Integer, default=0, nullable=False)
    bloqueado_hasta = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    # Relación N:M con clientes
    clientes = relationship("Cliente", secondary=usuario_cliente, back_populates="usuarios")
