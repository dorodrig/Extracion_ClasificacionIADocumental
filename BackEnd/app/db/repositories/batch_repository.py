from sqlalchemy.orm import Session
from app.domain.ports.batch_repository import BatchRepositoryPort
from app.domain.models.batch import Batch
from app.db.models.batches import LoteProcesamiento

class BatchRepository(BatchRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, batch: Batch) -> Batch:
        db_batch = LoteProcesamiento(
            batch_id=batch.batch_id,
            regla_id=batch.regla_id,
            cliente_id=batch.cliente_id,
            operario_id=batch.operario_id,
            modo_ingesta=batch.modo_ingesta,
            ruta_temporal=batch.ruta_temporal,
            estado=batch.estado,
            created_at=batch.created_at,
            completed_at=batch.completed_at
        )
        self.db.add(db_batch)
        self.db.commit()
        self.db.refresh(db_batch)
        
        batch.id = db_batch.id
        return batch
