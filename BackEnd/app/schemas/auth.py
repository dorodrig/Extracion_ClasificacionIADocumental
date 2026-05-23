from pydantic import BaseModel

class LoginRequest(BaseModel):
    cedula: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
