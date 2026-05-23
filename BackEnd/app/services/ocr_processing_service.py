import os
import json
import logging
from sqlalchemy.orm import Session
from fastapi.concurrency import run_in_threadpool
from app.db.models.ocr_db import OcrResultadosPaginas
from app.services.aws_textract_service import AWSTextractService

logger = logging.getLogger(__name__)

class OCRProcessingService:
    def __init__(self, db: Session):
        self.db = db
        self.aws_service = AWSTextractService()

    def _parse_blocks(self, textract_response: dict) -> tuple[str, float]:
        blocks = textract_response.get("Blocks", [])
        if not blocks:
            return "[]", 0.0

        parsed_data = []
        total_confidence = 0.0
        count = 0

        for block in blocks:
            if block["BlockType"] in ["LINE", "WORD"]:
                conf = block.get("Confidence", 0.0)
                total_confidence += conf
                count += 1
                parsed_data.append({
                    "text": block.get("Text", ""),
                    "confidence": conf,
                    "type": block["BlockType"]
                })

        avg_confidence = total_confidence / count if count > 0 else 0.0
        return json.dumps(parsed_data), avg_confidence

    async def process_page(self, documento_id: int, page_number: int, file_path: str, use_analyze: bool = False):
        """
        CA-02: Procesamiento síncrono por página (dentro de un threadpool para no bloquear event loop)
        """
        logger.info(f"Procesando documento {documento_id}, página {page_number}")
        
        try:
            # CA-09: Leer bytes de la imagen
            with open(file_path, "rb") as f:
                page_bytes = f.read()

            # Llamada al servicio AWS, enviada al threadpool para evitar bloqueo (R-AWS-2)
            response = await run_in_threadpool(
                self.aws_service.process_page_bytes,
                page_bytes,
                use_analyze
            )

            # Parsear bloques (CA-03, CA-05)
            campos_parseados, avg_confidence = self._parse_blocks(response)
            
            # Identificar páginas en blanco (CA-11)
            blocks_count = len(response.get("Blocks", []))
            if blocks_count == 0 or avg_confidence < 50.0:
                estado = "Página en Blanco"
            elif avg_confidence < 95.0:
                estado = "Baja confianza"
            else:
                estado = "OCR Completado"

            # Guardar en BD (CA-08)
            resultado = OcrResultadosPaginas(
                documento_id=documento_id,
                numero_pagina=page_number,
                bloques_raw_json=json.dumps(response),
                campos_parseados=campos_parseados,
                confianza_promedio=avg_confidence,
                estado=estado,
                tiempo_proceso_ms=response.get("__elapsed_ms", 0)
            )
            self.db.add(resultado)
            self.db.commit()
            
            # CA-12: Eliminar archivo temporal
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Archivo temporal eliminado: {file_path}")

            return resultado

        except Exception as e:
            logger.error(f"Error procesando página {page_number} del doc {documento_id}: {e}")
            
            # Guardar estado de error en la BD si falla
            resultado = OcrResultadosPaginas(
                documento_id=documento_id,
                numero_pagina=page_number,
                estado="Error en OCR",
                tiempo_proceso_ms=0
            )
            self.db.add(resultado)
            self.db.commit()
            raise
