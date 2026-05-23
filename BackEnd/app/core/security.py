import hashlib
import os
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings
from typing import Optional

def create_salt() -> str:
    """Genera un salt dinámicamente con os.urandom."""
    return os.urandom(32).hex()

def hash_password(password: str, salt: str) -> str:
    """Aplica SHA-256 + Salt estricto a las especificaciones."""
    salted_password = password + salt
    return hashlib.sha256(salted_password.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, salt: str, hashed_password: str) -> bool:
    """Verifica la contraseña plana contra el hash y salt guardados."""
    return hash_password(plain_password, salt) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Genera un JWT con claims dados."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_access_token(token: str):
    """Decodifica un token JWT y retorna los claims si es válido."""
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return decoded_token
    except jwt.PyJWTError:
        return None
