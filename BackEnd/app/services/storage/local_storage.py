import os
import shutil
from app.domain.ports.storage_port import StoragePort
from app.core.config import settings
from app.core.exceptions import StorageException

class LocalStorageAdapter(StoragePort):
    def create_temp_directory(self, batch_id: str, timestamp: str) -> str:
        try:
            ruta = os.path.join(settings.temp_dir, str(batch_id), timestamp)
            os.makedirs(ruta, exist_ok=True)
            return ruta
        except Exception as e:
            raise StorageException(f"Error al crear directorio temporal: {str(e)}")

    def copy_file(self, source_path: str, dest_path: str) -> str:
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(source_path, dest_path)
            return dest_path
        except Exception as e:
            raise StorageException(f"Error al copiar archivo de {source_path} a {dest_path}: {str(e)}")
