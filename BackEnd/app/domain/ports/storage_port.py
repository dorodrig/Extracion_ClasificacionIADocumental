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

    @abc.abstractmethod
    def create_directory_recursively(self, path: str) -> None:
        """Crea un directorio y todos sus padres si no existen."""
        pass

    @abc.abstractmethod
    def get_safe_filepath(self, dest_path: str) -> str:
        """Si el archivo ya existe, retorna una ruta con sufijo (e.g. _001) para evitar colisión."""
        pass

    @abc.abstractmethod
    def verify_file_integrity(self, source_path: str, dest_path: str) -> bool:
        """Comprueba que el archivo copiado tenga el mismo tamaño que el origen."""
        pass
