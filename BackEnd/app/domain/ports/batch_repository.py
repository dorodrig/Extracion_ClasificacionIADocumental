import abc
from app.domain.models.batch import Batch

class BatchRepositoryPort(abc.ABC):
    @abc.abstractmethod
    def save(self, batch: Batch) -> Batch:
        pass

    @abc.abstractmethod
    def update_ruta_temporal(self, batch_id: str, ruta_temporal: str) -> None:
        pass

    @abc.abstractmethod
    def update_estado(self, batch_id: str, estado: str) -> None:
        pass

    @abc.abstractmethod
    def get_by_batch_id(self, batch_id: str) -> Batch:
        pass
