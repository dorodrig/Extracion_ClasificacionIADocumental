from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[str] = None
