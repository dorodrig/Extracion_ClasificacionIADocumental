import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.schemas.batches import BatchCreate, BatchResponse
from app.db.models.batches import LoteProcesamiento
from app.core.exceptions import BatchCreationException

class BatchService:
    def __init__(self, db: Session):
        self.db = db

    def create_batch(self, batch_in: BatchCreate, operario_id: int) -> BatchResponse:
        try:
            new_batch_id = uuid.uuid4()
            timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
            ruta_temporal = f"/temp/{new_batch_id}/{timestamp_str}/"

            nuevo_lote = LoteProcesamiento(
                batch_id=new_batch_id,
                regla_id=batch_in.regla_id,
                cliente_id=batch_in.cliente_id,
                operario_id=operario_id,
                modo_ingesta=batch_in.modo_ingesta,
                ruta_temporal=ruta_temporal,
                estado="preparando"
            )

            self.db.add(nuevo_lote)
            self.db.commit()
            self.db.refresh(nuevo_lote)

            return BatchResponse.model_validate(nuevo_lote)
        except Exception as e:
            self.db.rollback()
            raise BatchCreationException(f"Error al crear el lote: {str(e)}")
