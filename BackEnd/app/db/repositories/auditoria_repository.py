from sqlalchemy.orm import Session
from app.db.models.auditoria import LogProceso, LogAuditoriaUsuario, LogIAInvocaciones
from app.schemas.auditoria import LogProcesoCreate, LogAuditoriaUsuarioCreate, LogIAInvocacionesCreate
from typing import List, Dict, Any

class AuditoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_log_proceso(self, data: LogProcesoCreate) -> LogProceso:
        db_obj = LogProceso(**data.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def create_log_auditoria_usuario(self, data: LogAuditoriaUsuarioCreate) -> LogAuditoriaUsuario:
        db_obj = LogAuditoriaUsuario(**data.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def create_log_ia_invocacion(self, data: LogIAInvocacionesCreate) -> LogIAInvocaciones:
        db_obj = LogIAInvocaciones(**data.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_historial_documento(self, documento_id: int) -> List[Dict[str, Any]]:
        # This approach retrieves each type separately and merges them in Python
        # to simplify returning a common schema.
        
        procesos = self.db.query(LogProceso).filter(LogProceso.documento_id == documento_id).all()
        auditorias = self.db.query(LogAuditoriaUsuario).filter(LogAuditoriaUsuario.documento_id == documento_id).all()
        invocaciones = self.db.query(LogIAInvocaciones).filter(LogIAInvocaciones.documento_id == documento_id).all()

        historial = []
        for p in procesos:
            historial.append({
                "id": p.id,
                "tipo_log": "proceso",
                "documento_id": p.documento_id,
                "created_at": p.created_at,
                "estado_anterior": p.estado_anterior,
                "estado_nuevo": p.estado_nuevo,
                "mensaje": p.mensaje
            })
            
        for a in auditorias:
            historial.append({
                "id": a.id,
                "tipo_log": "auditoria_usuario",
                "documento_id": a.documento_id,
                "created_at": a.created_at,
                "usuario_id": a.usuario_id,
                "accion": a.accion,
                "detalles": a.detalles
            })
            
        for i in invocaciones:
            historial.append({
                "id": i.id,
                "tipo_log": "ia_invocacion",
                "documento_id": i.documento_id,
                "created_at": i.created_at,
                "proveedor": i.proveedor,
                "endpoint_invocado": i.endpoint_invocado,
                "tiempo_respuesta_ms": i.tiempo_respuesta_ms,
                "exitoso": i.exitoso
            })
            
        # Sort by created_at ascending
        historial.sort(key=lambda x: x["created_at"])
        return historial
