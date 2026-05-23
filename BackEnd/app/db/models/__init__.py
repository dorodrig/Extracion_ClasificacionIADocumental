# app/db/models/__init__.py
from app.db.database import Base

# Modelos principales y tablas de relacion
from app.db.models.clientes import Cliente
from app.db.models.usuarios import Usuario, usuario_cliente
from app.db.models.rule_db import ReglasTrabajo
from app.db.models.rule_history_db import ReglasTrabajoHistorial
from app.db.models.documentos_lote import LoteProcesamiento, DocumentoLote
from app.db.models.ocr_db import OcrResultadosPaginas
from app.db.models.contexto_resultado_db import AgenteContextoResultados
from app.db.models.documentos_clasificados import DocumentoClasificado
from app.db.models.documentos_pendientes import DocumentoPendiente

# Tablas de Log
from app.db.models.auditoria import LogProceso, LogAuditoriaUsuario
from app.db.models.log_ia_invocacion_db import LogIAInvocacion
