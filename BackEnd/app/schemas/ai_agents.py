from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class CleanDataPackage(BaseModel):
    documento_id: int = Field(..., description="ID del documento en la BD")
    campos_extraidos: Dict[str, Any] = Field(..., description="Campos extraídos y limpios, incluyendo obligatorios")
    tipo_documento_detectado: str = Field(..., description="Tipo de documento detectado")
    regla_id: int = Field(..., description="ID de la regla de clasificación a aplicar")
    datos_completos: bool = Field(default=True, description="Indica si los datos están completos o requieren revisión")
