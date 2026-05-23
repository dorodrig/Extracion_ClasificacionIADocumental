from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.common import APIResponse
from app.services.auth_service import authenticate_user
import logging

logger = logging.getLogger("grm.api.auth")
router = APIRouter()

@router.post("/token", response_model=APIResponse[TokenResponse])
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint para iniciar sesión y obtener JWT.
    Bloquea cuenta por 15 minutos al superar 5 intentos fallidos.
    """
    try:
        token_response = authenticate_user(db, login_data.cedula, login_data.password)
        return APIResponse(success=True, data=token_response, message="Inicio de sesión exitoso")
    except HTTPException as he:
        logger.warning(f"Intento de login fallido para {login_data.cedula}: {he.detail}")
        return APIResponse(success=False, error=he.detail)
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return APIResponse(success=False, error="Error interno del servidor")
