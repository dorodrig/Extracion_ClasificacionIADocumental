from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.db.models.documento_db import DocumentosLote
from app.db.models.ocr_db import OcrResultadosPaginas

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.get("/progress/{batch_id}")
def get_ocr_progress(batch_id: int, db: Session = Depends(get_db)):
    """
    CA-10: Obtener el progreso del procesamiento OCR para un lote de documentos.
    Retorna el estado general y el detalle por página.
    """
    lote = db.query(DocumentosLote).filter(DocumentosLote.id == batch_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Batch no encontrado")

    paginas = db.query(OcrResultadosPaginas).filter(OcrResultadosPaginas.documento_id == batch_id).all()
    
    total_paginas = len(paginas)
    paginas_completadas = sum(1 for p in paginas if p.estado in ["OCR Completado", "Baja confianza", "Página en Blanco", "Error en OCR"])
    
    detalles = [
        {
            "numero_pagina": p.numero_pagina,
            "estado": p.estado,
            "confianza_promedio": float(p.confianza_promedio) if p.confianza_promedio else None,
            "tiempo_proceso_ms": p.tiempo_proceso_ms
        }
        for p in paginas
    ]

    return {
        "batch_id": batch_id,
        "nombre_archivo": lote.nombre_archivo,
        "estado_lote": lote.estado,
        "progreso": {
            "total_paginas": total_paginas,
            "paginas_completadas": paginas_completadas,
            "porcentaje": (paginas_completadas / total_paginas * 100) if total_paginas > 0 else 0
        },
        "detalles_paginas": detalles
    }
