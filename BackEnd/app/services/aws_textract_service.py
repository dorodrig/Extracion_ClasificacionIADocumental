import boto3
import time
import logging
from typing import List, Dict, Any, Union
from app.core.config import settings

logger = logging.getLogger(__name__)

class AWSTextractService:
    def __init__(self):
        try:
            self.client = boto3.client(
                'textract',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_default_region
            )
        except Exception as e:
            logger.error(f"Error initializing AWS Textract client: {e}")
            raise

    def process_page_bytes(self, page_bytes: bytes, use_analyze: bool = False) -> Dict[str, Any]:
        """
        Envía una página (en bytes) a AWS Textract.
        Implementa reintentos con backoff exponencial: 1s, 2s, 4s.
        Si use_analyze es True, usa analyze_document (para FORMS/TABLES).
        De lo contrario, detect_document_text (Texto general/Endoso).
        """
        retries = [1, 2, 4]
        attempt = 0
        
        while attempt <= len(retries):
            try:
                start_time = time.time()
                
                if use_analyze:
                    response = self.client.analyze_document(
                        Document={'Bytes': page_bytes},
                        FeatureTypes=['FORMS', 'TABLES']
                    )
                else:
                    response = self.client.detect_document_text(
                        Document={'Bytes': page_bytes}
                    )
                    
                end_time = time.time()
                elapsed_ms = int((end_time - start_time) * 1000)
                
                # Check SLA (assuming single page processing here, SLA < 60s for 1-3 pages)
                if elapsed_ms > 60000:
                    logger.warning(f"SLA Superado en llamada a Textract: {elapsed_ms}ms")
                    
                response['__elapsed_ms'] = elapsed_ms
                return response
                
            except Exception as e:
                logger.warning(f"Error en AWS Textract (Intento {attempt + 1}): {e}")
                if attempt < len(retries):
                    time.sleep(retries[attempt])
                    attempt += 1
                else:
                    logger.error("Todos los reintentos fallaron. Error en OCR.")
                    raise RuntimeError("Error en OCR por fallos de AWS Textract") from e
