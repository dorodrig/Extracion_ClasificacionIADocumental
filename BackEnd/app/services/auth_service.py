from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from app.db.models.usuarios import Usuario
from app.core.security import verify_password, create_access_token
from app.schemas.auth import TokenResponse

def authenticate_user(db: Session, cedula: str, password: str) -> TokenResponse:
    usuario = db.query(Usuario).filter(Usuario.cedula == cedula).first()
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        
    if not usuario.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")
        
    # Verificar bloqueo
    if usuario.bloqueado_hasta:
        # Check timezone awareness, ensuring both are aware or naive.
        bloqueado_hasta_tz = usuario.bloqueado_hasta
        if bloqueado_hasta_tz.tzinfo is None:
            bloqueado_hasta_tz = bloqueado_hasta_tz.replace(tzinfo=timezone.utc)
            
        if bloqueado_hasta_tz > datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cuenta bloqueada temporalmente")
        
    if not verify_password(password, usuario.salt, usuario.hashed_password):
        usuario.intentos_fallidos += 1
        if usuario.intentos_fallidos >= 5:
            usuario.bloqueado_hasta = datetime.now(timezone.utc) + timedelta(minutes=15)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        
    # Autenticación exitosa
    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    db.commit()
    
    # Cliente asociado (si existe, tomamos el primero por defecto o None)
    cliente_id = usuario.clientes[0].id if usuario.clientes else None
    
    access_token = create_access_token(
        data={"usuario_id": usuario.id, "rol": usuario.rol, "cliente_id": cliente_id}
    )
    return TokenResponse(access_token=access_token, token_type="bearer")
