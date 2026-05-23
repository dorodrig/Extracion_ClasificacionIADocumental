from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class Batch:
    id: int
    batch_id: UUID
    regla_id: int
    cliente_id: int
    operario_id: int
    modo_ingesta: str
    ruta_temporal: Optional[str]
    total_docs: Optional[int]
    total_paginas: Optional[int]
    estado: str
    created_at: datetime
    completed_at: Optional[datetime]
