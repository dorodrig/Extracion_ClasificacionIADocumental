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

    def update_ruta_temporal(self, batch_id: str, ruta_temporal: str) -> None:
        db_batch = self.db.query(LoteProcesamiento).filter(LoteProcesamiento.batch_id == batch_id).first()
        if db_batch:
            db_batch.ruta_temporal = ruta_temporal
            self.db.commit()

    def update_estado(self, batch_id: str, estado: str) -> None:
        db_batch = self.db.query(LoteProcesamiento).filter(LoteProcesamiento.batch_id == batch_id).first()
        if db_batch:
            db_batch.estado = estado
            self.db.commit()

    def get_by_batch_id(self, batch_id: str) -> Batch:
        db_batch = self.db.query(LoteProcesamiento).filter(LoteProcesamiento.batch_id == batch_id).first()
        if not db_batch:
            return None
        return Batch(
            batch_id=db_batch.batch_id,
            regla_id=db_batch.regla_id,
            cliente_id=db_batch.cliente_id,
            operario_id=db_batch.operario_id,
            modo_ingesta=db_batch.modo_ingesta,
            ruta_temporal=db_batch.ruta_temporal,
            estado=db_batch.estado,
            created_at=db_batch.created_at,
            completed_at=db_batch.completed_at
        )
