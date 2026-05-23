import os
import shutil
from pathlib import Path
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

    def create_directory_recursively(self, path: str) -> None:
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            raise StorageException(f"Error al crear directorios en {path}: {str(e)}")

    def get_safe_filepath(self, dest_path: str) -> str:
        """Devuelve una ruta segura sin colisiones agregando _001, _002 si existe."""
        if not os.path.exists(dest_path):
            return dest_path
        
        path_obj = Path(dest_path)
        directory = path_obj.parent
        stem = path_obj.stem
        suffix = path_obj.suffix
        
        counter = 1
        while True:
            new_name = f"{stem}_{counter:03d}{suffix}"
            new_path = directory / new_name
            if not new_path.exists():
                return str(new_path)
            counter += 1

    def verify_file_integrity(self, source_path: str, dest_path: str) -> bool:
        try:
            source_size = os.path.getsize(source_path)
            dest_size = os.path.getsize(dest_path)
            return source_size == dest_size
        except OSError:
            return False
