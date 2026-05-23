import os
import glob
import logging
from typing import Optional
from sqlalchemy.orm import Session
from fastapi.concurrency import run_in_threadpool

from app.services.ocr_processing_service import OCRProcessingService
from app.services.contexto_ia_service import ContextoIAService
from app.db.repositories.batch_repository import BatchRepository
# Asumimos la existencia o inyección del Agente de Clasificación si corresponde.
# En la implementación actual, ContextoIAService devuelve 'listo_clasificacion' o 'pendiente_humano'
# La actualización de estados la haremos directamente sobre los repositorios si no hay un agente separado.

logger = logging.getLogger("grm.pipeline")

class PipelineOrchestratorService:
    def __init__(self, db: Session):
        self.db = db
        self.ocr_service = OCRProcessingService(db)
        self.contexto_service = ContextoIAService(db)
        self.batch_repo = BatchRepository(db)

    async def process_batch_pipeline(self, batch_id: str, regla_id: int):
        """
        Orquesta el flujo BPMN completo en segundo plano.
        Ingesta (ya preparada) -> OCR -> Contexto IA -> Clasificación/Dudas (Pendientes)
        """
        logger.info(f"Iniciando Pipeline Orquestador para lote {batch_id}")
        
        batch = self.batch_repo.get_by_batch_id(batch_id)
        if not batch:
            logger.error(f"Lote {batch_id} no encontrado para orquestación.")
            return

        if not batch.ruta_temporal or not os.path.exists(batch.ruta_temporal):
            logger.error(f"Ruta temporal no válida para lote {batch_id}: {batch.ruta_temporal}")
            self.batch_repo.update_estado(batch_id, "error_pipeline")
            return

        # Actualizar estado a procesando_ocr
        self.batch_repo.update_estado(batch_id, "procesando_ocr")
        
        # 1. Obtener todos los documentos físicos en la ruta temporal
        archivos = glob.glob(os.path.join(batch.ruta_temporal, "*.*"))
        if not archivos:
            logger.warning(f"No hay archivos en la ruta temporal para lote {batch_id}")
            self.batch_repo.update_estado(batch_id, "completado_vacio")
            return

        # Simularemos documento_id en DB basado en el batch (el IngestionService debería haberlos creado,
        # pero si no, usaremos un ID temporal o crearemos un registro de documento si corresponde).
        # Para la integración actual, pasaremos un documento_id genérico basado en el índice.
        # CA-02 de OCR requiere documento_id. Asumiremos que el lote en sí ya tiene su trazabilidad.
        # Crearemos o usaremos ids de documentos generados.
        from app.db.models.documento_db import Documento
        
        errores = 0
        procesados = 0

        for idx, archivo in enumerate(archivos):
            nombre_archivo = os.path.basename(archivo)
            logger.info(f"Procesando archivo {nombre_archivo} del lote {batch_id}")
            
            # Registrar documento en BD si no existe (simplificado)
            nuevo_doc = Documento(
                lote_id=batch.id,
                nombre_archivo=nombre_archivo,
                ruta_almacenamiento=archivo,
                estado="procesando_ocr"
            )
            self.db.add(nuevo_doc)
            self.db.commit()
            self.db.refresh(nuevo_doc)
            
            documento_id = nuevo_doc.id

            try:
                # 2. Invocar OCR
                await self.ocr_service.process_page(
                    documento_id=documento_id,
                    page_number=1, # Simplificación: 1 página por archivo en lote dividido
                    file_path=archivo,
                    use_analyze=False
                )
                nuevo_doc.estado = "ocr_completado"
                self.db.commit()
            except Exception as e:
                logger.error(f"Error en OCR para doc {documento_id}: {e}")
                nuevo_doc.estado = "error_ocr"
                self.db.commit()
                errores += 1
                continue

            try:
                # 3. Invocar Contexto IA
                nuevo_doc.estado = "procesando_ia"
                self.db.commit()
                
                resultado_ia = await self.contexto_service.procesar_documento(
                    documento_id=documento_id,
                    regla_id=regla_id
                )
                
                # 4. Enrutamiento BPMN (Clasificación vs Humano)
                if resultado_ia.estado == "listo_clasificacion":
                    nuevo_doc.estado = "clasificado"
                    # Aquí iría la llamada al ClassificationAgent
                elif resultado_ia.estado == "pendiente_humano":
                    nuevo_doc.estado = "pendiente_revision"
                else:
                    nuevo_doc.estado = "error_ia"

                self.db.commit()
                procesados += 1
                
            except Exception as e:
                logger.error(f"Error en Contexto IA para doc {documento_id}: {e}")
                nuevo_doc.estado = "error_ia"
                self.db.commit()
                errores += 1

        # Finalizar lote
        estado_final = "completado" if errores == 0 else "completado_con_errores"
        self.batch_repo.update_estado(batch_id, estado_final)
        logger.info(f"Pipeline completado para lote {batch_id}. Estado: {estado_final}")

