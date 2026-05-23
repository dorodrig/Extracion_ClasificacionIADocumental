import re
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from app.schemas.ai_agents import CleanDataPackage
from app.domain.ports.gemini_port import GeminiPort
from app.domain.ports.storage_port import StoragePort
from app.db.repositories.clasificacion_repository import ClasificacionRepository
from app.db.models.documentos_clasificados import DocumentoClasificado
from app.db.models.batches import DocumentoLote
from app.core.exceptions import GRMException

logger = logging.getLogger("grm.ai_agents.classification_agent")

class ClassificationAgent:
    def __init__(
        self, 
        gemini_port: GeminiPort, 
        storage_port: StoragePort, 
        repo: ClasificacionRepository
    ):
        self.gemini_port = gemini_port
        self.storage_port = storage_port
        self.repo = repo

    def sanitize_path_element(self, text: str) -> str:
        """Sanitiza variables para uso seguro en rutas de Windows/Linux."""
        if not text or text == "SIN_DATO":
            return "SIN_DATO"
        # Eliminar acentos, caracteres raros, y reemplazar espacios por guión bajo
        import unicodedata
        text = unicodedata.normalize('NFKD', str(text)).encode('ASCII', 'ignore').decode('utf-8')
        text = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', text)
        return text.strip('_').upper()

    async def process_document(self, data_package: CleanDataPackage, rule_pattern: str, source_file_path: str, base_dest_path: str, batch_id: str, cliente_id: int):
        """Ejecuta el pipeline de clasificación para un documento."""
        try:
            logger.info(f"Iniciando clasificación para doc_id={data_package.documento_id}")

            # CA-01: Verificación de completitud
            if not data_package.datos_completos:
                logger.warning(f"Paquete de datos incompleto para doc_id={data_package.documento_id}. Enviando a revisión.")
                self.repo.update_documento_estado(data_package.documento_id, "pendiente_revision", "Datos incompletos desde ContextAgent")
                return
            
            # CA-03: Resolver ambigüedades con Gemini
            # Se inyecta la regla para que la IA entienda qué variables necesita
            logger.debug("Llamando a Gemini para resolución de ambigüedades")
            resolucion = await self.gemini_port.resolve_ambiguities(data_package.model_dump(), rule_pattern)
            
            variables_resueltas = resolucion.get("variables_resueltas", {})
            razonamiento = resolucion.get("razonamiento", "Sin razonamiento")
            
            logger.info(f"Gemini razonamiento: {razonamiento}")

            # CA-02 & CA-07: Construcción de ruta y sanitización
            # Reemplazar tokens en la regla. Ej: "/{CC}/{NOMBRE_COMPLETO}/{TIPO_DOCUMENTO}/{NOMBRE_ARCHIVO}"
            relative_path = rule_pattern
            # Asumimos que rule_pattern usa sintaxis de llaves, ej: /{CC}/...
            tokens = re.findall(r'\{([^}]+)\}', rule_pattern)
            
            for token in tokens:
                # Usar valor de Gemini si existe, o del paquete extraído directo
                valor_crudo = variables_resueltas.get(token) or data_package.campos_extraidos.get(token, "SIN_DATO")
                valor_limpio = self.sanitize_path_element(str(valor_crudo))
                relative_path = relative_path.replace(f"{{{token}}}", valor_limpio)
            
            # Limpiar posible doble slash
            relative_path = os.path.normpath(relative_path.lstrip('/\\'))
            
            final_dest_dir = os.path.join(base_dest_path, os.path.dirname(relative_path))
            final_file_name = os.path.basename(relative_path)
            if not final_file_name:
                final_file_name = "documento_desconocido.pdf"
                
            # CA-04: Creación de carpetas
            self.storage_port.create_directory_recursively(final_dest_dir)
            
            # CA-08: Manejo de duplicados
            target_file_path = os.path.join(final_dest_dir, final_file_name)
            safe_target_path = self.storage_port.get_safe_filepath(target_file_path)
            
            if target_file_path != safe_target_path:
                logger.warning(f"Conflicto de nombres. Guardando como {os.path.basename(safe_target_path)}")

            # CA-05: Copia física e integridad
            self.storage_port.copy_file(source_file_path, safe_target_path)
            if not self.storage_port.verify_file_integrity(source_file_path, safe_target_path):
                raise GRMException("Fallo en verificación de integridad post-copia.")

            # CA-06, CA-09, CA-13: Persistencia en BD
            doc_clasificado = DocumentoClasificado(
                cliente_id=cliente_id,
                batch_id=batch_id,
                regla_id=data_package.regla_id,
                documento_id=data_package.documento_id,
                campos_extraidos_json={
                    "crudo": data_package.campos_extraidos,
                    "gemini_normalizado": variables_resueltas,
                    "razonamiento": razonamiento
                },
                ruta_destino_final=safe_target_path,
                tipo_documento=data_package.tipo_documento_detectado
            )
            
            self.repo.upsert_documento_clasificado(doc_clasificado)
            self.repo.update_documento_estado(data_package.documento_id, "Clasificado Exitosamente")
            
            logger.info(f"Clasificación exitosa doc_id={data_package.documento_id} en {safe_target_path}")

        except Exception as e:
            # CA-12: Manejo de errores
            logger.error(f"Error procesando doc_id={data_package.documento_id}: {str(e)}")
            self.repo.update_documento_estado(data_package.documento_id, "Error de Escritura", str(e))

