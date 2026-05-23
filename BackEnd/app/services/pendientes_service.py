from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, Tuple
from app.db.repositories.pendientes_repository import PendientesRepository
from app.schemas.pendientes import (
    DocumentoPendienteResponse,
    DocumentoPendienteVisorResponse,
    CorreccionDirectaRequest,
    InstruccionClasificacionRequest,
    DescarteRequest,
    ListaPendientesResponse
)
from app.core.websockets import manager
from app.services.auditoria_service import AuditoriaService
from app.schemas.auditoria import LogAuditoriaUsuarioCreate

class PendientesService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PendientesRepository(db)
        self.auditoria_service = AuditoriaService(db)

    def list_pendientes(self, skip: int = 0, limit: int = 100, query: Optional[str] = None, cliente_id: Optional[int] = None) -> ListaPendientesResponse:
        items, total = self.repository.get_pendientes(skip, limit, query, cliente_id)
        return ListaPendientesResponse(
            items=[DocumentoPendienteResponse.model_validate(item) for item in items],
            total=total
        )

    def get_visor_data(self, pendiente_id: int) -> Optional[DocumentoPendienteVisorResponse]:
        item = self.repository.get_pendiente_by_id(pendiente_id)
        if not item:
            return None
        return DocumentoPendienteVisorResponse.model_validate(item)

    async def corregir_documento(self, pendiente_id: int, usuario_id: int, correccion_data: CorreccionDirectaRequest) -> bool:
        item = self.repository.update_pendiente_status(pendiente_id, "corregido", correccion_data.campos_corregidos)
        if item:
            self.auditoria_service.registrar_auditoria_usuario(
                LogAuditoriaUsuarioCreate(
                    documento_id=item.documento_id,
                    usuario_id=usuario_id,
                    accion="correccion_directa",
                    detalles={"campos_corregidos": correccion_data.campos_corregidos}
                )
            )
            await manager.broadcast({
                "type": "STATUS_UPDATE",
                "documento_id": item.documento_id,
                "pendiente_id": item.id,
                "estado": "corregido"
            })
            return True
        return False

    async def enviar_instruccion(self, pendiente_id: int, usuario_id: int, instruccion_data: InstruccionClasificacionRequest) -> bool:
        item = self.repository.update_pendiente_status(pendiente_id, "pendiente_instruccion")
        if item:
            self.auditoria_service.registrar_auditoria_usuario(
                LogAuditoriaUsuarioCreate(
                    documento_id=item.documento_id,
                    usuario_id=usuario_id,
                    accion="instruccion_ia",
                    detalles={"instruccion": instruccion_data.instruccion}
                )
            )
            # Here we would theoretically trigger the AI classification agent queue
            # with the specific instruction.
            await manager.broadcast({
                "type": "INSTRUCTION_SENT",
                "documento_id": item.documento_id,
                "pendiente_id": item.id,
                "estado": "pendiente_instruccion"
            })
            return True
        return False

    async def descartar_documento(self, pendiente_id: int, usuario_id: int, descarte_data: DescarteRequest) -> bool:
        item = self.repository.update_pendiente_rechazo(pendiente_id, descarte_data.motivo_descarte)
        if item:
            self.auditoria_service.registrar_auditoria_usuario(
                LogAuditoriaUsuarioCreate(
                    documento_id=item.documento_id,
                    usuario_id=usuario_id,
                    accion="descarte",
                    detalles={"motivo_descarte": descarte_data.motivo_descarte}
                )
            )
            await manager.broadcast({
                "type": "STATUS_UPDATE",
                "documento_id": item.documento_id,
                "pendiente_id": item.id,
                "estado": "descartado"
            })
            return True
        return False
