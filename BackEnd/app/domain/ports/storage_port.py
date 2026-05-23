import abc

class StoragePort(abc.ABC):
    @abc.abstractmethod
    def create_temp_directory(self, batch_id: str, timestamp: str) -> str:
        """Crea y retorna la ruta de trabajo temporal para un lote."""
        pass
    
    @abc.abstractmethod
    def copy_file(self, source_path: str, dest_path: str) -> str:
        """Copia un archivo al destino y retorna la nueva ruta."""
        pass
