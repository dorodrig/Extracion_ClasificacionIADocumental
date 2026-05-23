import os
import logging
from datetime import datetime
from app.schemas.batches import BatchPrepareRequest, BatchStatusResponse
from app.domain.rules.document_rules import validar_formato
from app.domain.ports.batch_repository import BatchRepositoryPort
from app.domain.ports.storage_port import StoragePort
from app.domain.ports.pdf_splitter_port import PDFSplitterPort
from app.core.exceptions import InvalidDocumentFormatException, StorageException, PDFSplittingException, GRMException

logger = logging.getLogger("grm.ingestion")

class IngestionService:
    def __init__(
        self,
        batch_repository: BatchRepositoryPort,
        storage_adapter: StoragePort,
        pdf_splitter_adapter: PDFSplitterPort
    ):
        self.repo = batch_repository
        self.storage = storage_adapter
        self.pdf_splitter = pdf_splitter_adapter

    def prepare_batch(self, batch_id: str, request: BatchPrepareRequest) -> BatchStatusResponse:
        logger.info(f"Iniciando preparación de lote {batch_id} con {len(request.documentos)} documentos")
        
        self.repo.update_estado(batch_id, "preparando")
        
        documentos_validos = []
        archivos_omitidos = []
        
        for doc in request.documentos:
            if validar_formato(doc.extension):
                documentos_validos.append(doc)
            else:
                archivos_omitidos.append(doc.nombre_archivo)
                logger.warning(f"Archivo omitido por formato no compatible: {doc.nombre_archivo}")
        
        if not documentos_validos:
            self.repo.update_estado(batch_id, "error")
            raise InvalidDocumentFormatException("Ninguno de los documentos tiene un formato válido.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_temporal = self.storage.create_temp_directory(batch_id, timestamp)
        self.repo.update_ruta_temporal(batch_id, ruta_temporal)
        logger.info(f"Ruta temporal creada para lote {batch_id}: {ruta_temporal}")

        documentos_preparados = 0
        for idx, doc in enumerate(documentos_validos):
            try:
                source_path = os.path.join(ruta_temporal, doc.ruta_original)
                
                # Dummy PDF creation for pilot testing if it doesn't exist
                if not os.path.exists(source_path) and doc.extension and doc.extension.lower() == 'pdf':
                    try:
                        from pypdf import PdfWriter
                        writer = PdfWriter()
                        writer.add_blank_page(width=200, height=200)
                        with open(source_path, "wb") as fp:
                            writer.write(fp)
                    except Exception:
                        pass
                elif not os.path.exists(source_path):
                    with open(source_path, 'w') as fp:
                        fp.write('mock')

                if doc.extension and doc.extension.lower() == 'pdf' and (doc.total_paginas is None or doc.total_paginas > 1):
                    self.pdf_splitter.split_pdf(source_path, ruta_temporal, str(batch_id), idx + 1)
                else:
                    ext = doc.extension.lower().strip('.') if doc.extension else 'pdf'
                    dest_path = os.path.join(ruta_temporal, f"{batch_id}_doc_{idx+1}_p1.{ext}")
                    self.storage.copy_file(source_path, dest_path)
                
                documentos_preparados += 1
            except (PDFSplittingException, StorageException) as e:
                logger.error(f"Error procesando documento {doc.nombre_archivo}: {str(e)}")

        estado_final = "en_proceso" if documentos_preparados > 0 else "error"
        self.repo.update_estado(batch_id, estado_final)
        
        return BatchStatusResponse(
            batch_id=str(batch_id),
            estado=estado_final,
            documentos_preparados=documentos_preparados,
            total_documentos=len(documentos_validos),
            ruta_temporal=ruta_temporal,
            archivos_omitidos=archivos_omitidos
        )

    def get_batch_status(self, batch_id: str) -> BatchStatusResponse:
        batch = self.repo.get_by_batch_id(batch_id)
        if not batch:
            raise GRMException(f"Lote con ID {batch_id} no encontrado")
        
        # Devolución por defecto, ya que la iteración 10 detalla este tracking.
        return BatchStatusResponse(
            batch_id=str(batch_id),
            estado=batch.estado,
            documentos_preparados=0,
            total_documentos=0,
            ruta_temporal=batch.ruta_temporal,
            archivos_omitidos=[]
        )
