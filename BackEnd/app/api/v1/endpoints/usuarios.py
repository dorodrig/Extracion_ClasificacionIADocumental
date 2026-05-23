from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse, ClienteResponse
from app.schemas.common import APIResponse
from app.services.usuarios_service import get_usuarios, create_usuario, get_clientes_by_usuario
from app.core.dependencies import require_role
from app.db.models.usuarios import Usuario
import logging

logger = logging.getLogger("grm.api.usuarios")
router = APIRouter()

@router.get("/", response_model=APIResponse[List[UsuarioResponse]])
def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["administrador"]))
):
    """Lista todos los usuarios. Requiere rol Administrador."""
    try:
        usuarios = get_usuarios(db)
        return APIResponse(success=True, data=usuarios, message="Usuarios listados exitosamente")
    except Exception as e:
        logger.error(f"Error listar_usuarios: {str(e)}")
        return APIResponse(success=False, error="Error interno del servidor")

@router.post("/", response_model=APIResponse[UsuarioResponse])
def registrar_usuario(
    usuario_in: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["administrador"]))
):
    """Crea un nuevo usuario. Requiere rol Administrador."""
    try:
        nuevo_usuario = create_usuario(db, usuario_in)
        return APIResponse(success=True, data=nuevo_usuario, message="Usuario creado exitosamente")
    except HTTPException as he:
        return APIResponse(success=False, error=he.detail)
    except Exception as e:
        logger.error(f"Error registrar_usuario: {str(e)}")
        return APIResponse(success=False, error="Error interno del servidor")

@router.get("/clientes", response_model=APIResponse[List[ClienteResponse]])
def listar_mis_clientes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["operario", "administrador"]))
):
    """Lista los clientes asociados al usuario actual."""
    try:
        clientes = get_clientes_by_usuario(db, current_user.id)
        return APIResponse(success=True, data=clientes, message="Clientes listados exitosamente")
    except HTTPException as he:
        return APIResponse(success=False, error=he.detail)
    except Exception as e:
        logger.error(f"Error listar_mis_clientes: {str(e)}")
        return APIResponse(success=False, error="Error interno del servidor")
