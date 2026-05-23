from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.db.models.usuarios import usuario_cliente

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    identificacion = Column(String(50), nullable=True, unique=True)
    
    # Relación N:M con usuarios
    usuarios = relationship("Usuario", secondary=usuario_cliente, back_populates="clientes")
