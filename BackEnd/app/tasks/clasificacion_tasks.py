from app.core.celery_app import celery_app
from app.db.database import SessionLocal
from app.services.clasificacion_ia_service import ClasificacionIAService

@celery_app.task(name="app.tasks.clasificacion_tasks.clasificar_documento_task")
def clasificar_documento_task(payload: dict):
    db = SessionLocal()
    try:
        service = ClasificacionIAService(db)
        result = service.clasificar_documento(payload)
        return result
    finally:
        db.close()
