import uuid
from datetime import datetime
from app.schemas.batches import BatchCreate, BatchResponse
from app.domain.models.batch import Batch
from app.domain.ports.batch_repository import BatchRepositoryPort
from app.core.exceptions import BatchCreationException

class BatchService:
    def __init__(self, batch_repository: BatchRepositoryPort):
        self.batch_repo = batch_repository

    def create_batch(self, batch_in: BatchCreate, operario_id: int) -> BatchResponse:
        try:
            new_batch_id = uuid.uuid4()
            timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
            ruta_temporal = f"/temp/{new_batch_id}/{timestamp_str}/"

            nuevo_lote = Batch(
                id=0,
                batch_id=new_batch_id,
                regla_id=batch_in.regla_id,
                cliente_id=batch_in.cliente_id,
                operario_id=operario_id,
                modo_ingesta=batch_in.modo_ingesta,
                ruta_temporal=ruta_temporal,
                total_docs=None,
                total_paginas=None,
                estado="preparando",
                created_at=datetime.now(),
                completed_at=None
            )

            saved_batch = self.batch_repo.save(nuevo_lote)

            return BatchResponse(
                id=saved_batch.id,
                batch_id=saved_batch.batch_id,
                estado=saved_batch.estado,
                created_at=saved_batch.created_at
            )
        except Exception as e:
            raise BatchCreationException(f"Error al crear el lote: {str(e)}")
