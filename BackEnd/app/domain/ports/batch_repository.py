import abc
from app.domain.models.batch import Batch

class BatchRepositoryPort(abc.ABC):
    @abc.abstractmethod
    def save(self, batch: Batch) -> Batch:
        pass
