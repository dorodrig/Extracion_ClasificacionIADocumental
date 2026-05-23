from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.db.models.usuarios import Usuario, Cliente
from app.schemas.usuarios import UsuarioCreate
from app.core.security import create_salt, hash_password

def get_usuarios(db: Session) -> List[Usuario]:
    return db.query(Usuario).all()

def create_usuario(db: Session, usuario_in: UsuarioCreate) -> Usuario:
    if db.query(Usuario).filter(Usuario.cedula == usuario_in.cedula).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cédula ya está registrada")
        
    salt = create_salt()
    hashed_password = hash_password(usuario_in.password, salt)
    
    nuevo_usuario = Usuario(
        cedula=usuario_in.cedula,
        nombre=usuario_in.nombre,
        rol=usuario_in.rol,
        salt=salt,
        hashed_password=hashed_password,
        activo=True,
        intentos_fallidos=0
    )
    
    if usuario_in.cliente_ids:
        clientes = db.query(Cliente).filter(Cliente.id.in_(usuario_in.cliente_ids)).all()
        nuevo_usuario.clientes = clientes
        
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def get_clientes_by_usuario(db: Session, usuario_id: int) -> List[Cliente]:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario.clientes
